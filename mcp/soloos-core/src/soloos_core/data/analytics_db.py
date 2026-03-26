"""
SoloOS V10 — DuckDB Analytics Store

Persists revenue events, user events, and sync state for KPI computation.
Database lives at ~/.soloos/analytics.duckdb — created on first use.

Env vars: none required (DuckDB is file-based).

Fail-open: if duckdb is not installed, all methods log a warning and return
empty/zero results. The rest of the system continues to function.

Usage:
    from soloos_core.data.analytics_db import get_analytics_db

    db = get_analytics_db()
    db.insert_events("revenue_events", [{"id": "ch_123", ...}])
    mrr = db.get_current_mrr()          # -> 4250.0
    trend = db.get_mrr_trend(months=6)  # -> [{"month": ..., "mrr_dollars": ...}, ...]
    arpu = db.get_current_arpu()        # -> 85.0  (Phase E)
    ret  = db.get_recent_retention()    # -> {"day7": 0.42, ...}  (Phase E)
"""

import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# DuckDB availability check (lazy, fail-open)
# ─────────────────────────────────────────────────────────────

_duckdb_available: Optional[bool] = None


def _check_duckdb() -> bool:
    global _duckdb_available
    if _duckdb_available is None:
        try:
            import duckdb  # noqa: F401
            _duckdb_available = True
        except ImportError:
            logger.warning(
                "duckdb not installed — analytics_db is a no-op. "
                "Install with: pip install 'soloos-core[analytics]' or pip install duckdb"
            )
            _duckdb_available = False
    return _duckdb_available


# ─────────────────────────────────────────────────────────────
# Schema SQL
# ─────────────────────────────────────────────────────────────

_SCHEMA_SQL = """
-- Revenue events (from Stripe connector)
CREATE TABLE IF NOT EXISTS revenue_events (
    id VARCHAR PRIMARY KEY,
    source VARCHAR NOT NULL,
    event_type VARCHAR NOT NULL,
    customer_id VARCHAR,
    amount_cents INTEGER,
    currency VARCHAR DEFAULT 'usd',
    mrr_delta_cents INTEGER,
    metadata JSON,
    occurred_at TIMESTAMP NOT NULL,
    synced_at TIMESTAMP DEFAULT current_timestamp
);

-- User/product events (from PostHog/Mixpanel)
CREATE TABLE IF NOT EXISTS user_events (
    id VARCHAR PRIMARY KEY,
    source VARCHAR NOT NULL,
    event_name VARCHAR NOT NULL,
    user_id VARCHAR,
    properties JSON,
    occurred_at TIMESTAMP NOT NULL,
    synced_at TIMESTAMP DEFAULT current_timestamp
);

-- Sync state (last successful sync per source)
CREATE TABLE IF NOT EXISTS sync_state (
    source VARCHAR PRIMARY KEY,
    last_synced_at TIMESTAMP,
    last_cursor VARCHAR,
    status VARCHAR DEFAULT 'ok'
);
"""

_VIEWS_SQL = """
-- MRR as of today
CREATE VIEW IF NOT EXISTS v_mrr AS
SELECT
    date_trunc('month', occurred_at) AS month,
    SUM(mrr_delta_cents) / 100.0 AS mrr_dollars
FROM revenue_events
GROUP BY 1 ORDER BY 1;

-- Monthly churn rate
CREATE VIEW IF NOT EXISTS v_churn AS
SELECT
    date_trunc('month', occurred_at) AS month,
    COUNT(CASE WHEN mrr_delta_cents < 0 AND event_type LIKE '%deleted%' THEN 1 END) AS churned,
    COUNT(DISTINCT customer_id) AS total_customers
FROM revenue_events
GROUP BY 1;
"""


# ─────────────────────────────────────────────────────────────
# AnalyticsDB class
# ─────────────────────────────────────────────────────────────

class AnalyticsDB:
    """
    DuckDB-backed analytics store for SoloOS revenue and user event data.

    All public methods are fail-open: if DuckDB is unavailable or a query
    errors, the method logs a warning and returns an empty/zero value instead
    of raising.
    """

    def __init__(self, db_path: str = "~/.soloos/analytics.duckdb"):
        self._db_path = Path(db_path).expanduser()
        self._conn = None
        self._initialized = False

        if _check_duckdb():
            self._connect_and_init()

    # ── Internal helpers ────────────────────────────────────────

    def _connect_and_init(self) -> None:
        """Open (or create) the DuckDB file and apply schema. Idempotent."""
        try:
            import duckdb
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = duckdb.connect(str(self._db_path))
            self._conn.execute(_SCHEMA_SQL)
            self._conn.execute(_VIEWS_SQL)
            self._initialized = True
        except Exception as exc:
            logger.warning("analytics_db: failed to connect/init — %s", exc)
            self._conn = None
            self._initialized = False

    def _ensure_conn(self) -> bool:
        """Return True if a usable connection exists (lazy reconnect on failure)."""
        if self._conn is not None and self._initialized:
            return True
        if _check_duckdb():
            self._connect_and_init()
        return self._initialized

    def _rows_to_dicts(self, rel) -> list[dict]:
        """Convert a DuckDB relation / fetchall result + description to list[dict]."""
        try:
            description = rel.description
            rows = rel.fetchall()
            cols = [d[0] for d in description]
            return [dict(zip(cols, row)) for row in rows]
        except Exception as exc:
            logger.warning("analytics_db: _rows_to_dicts failed — %s", exc)
            return []

    # ── Public API ──────────────────────────────────────────────

    def insert_events(self, table: str, rows: list[dict]) -> int:
        """
        Insert rows into the given table. Conflicts on PRIMARY KEY are ignored
        (idempotent — safe to call multiple times with the same data).

        Returns the number of rows successfully inserted.
        """
        if not rows:
            return 0
        if not self._ensure_conn():
            logger.warning("analytics_db: insert_events skipped — no DuckDB connection")
            return 0

        inserted = 0
        for row in rows:
            cols = ", ".join(row.keys())
            placeholders = ", ".join("?" * len(row))
            sql = (
                f"INSERT OR IGNORE INTO {table} ({cols}) VALUES ({placeholders})"
            )
            try:
                self._conn.execute(sql, list(row.values()))
                inserted += 1
            except Exception:
                # DuckDB uses INSERT OR REPLACE syntax; fall back to ON CONFLICT DO NOTHING
                try:
                    sql_alt = (
                        f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) "
                        f"ON CONFLICT DO NOTHING"
                    )
                    self._conn.execute(sql_alt, list(row.values()))
                    inserted += 1
                except Exception as exc:
                    logger.warning("analytics_db: insert failed for row — %s", exc)

        return inserted

    def query(self, sql: str, params: list = None) -> list[dict]:
        """
        Execute a raw SQL query and return results as a list of dicts.
        Returns [] on any error or if DuckDB is unavailable.
        """
        if not self._ensure_conn():
            logger.warning("analytics_db: query skipped — no DuckDB connection")
            return []
        try:
            rel = self._conn.execute(sql, params or [])
            return self._rows_to_dicts(rel)
        except Exception as exc:
            logger.warning("analytics_db: query failed — %s | sql=%s", exc, sql)
            return []

    def get_current_mrr(self) -> float:
        """
        Return the cumulative MRR (sum of all mrr_delta_cents / 100).
        Returns 0.0 if no data or DuckDB unavailable.
        """
        rows = self.query(
            "SELECT COALESCE(SUM(mrr_delta_cents), 0) / 100.0 AS mrr "
            "FROM revenue_events"
        )
        if not rows:
            return 0.0
        return float(rows[0].get("mrr", 0.0) or 0.0)

    def get_mrr_trend(self, months: int = 6) -> list[dict]:
        """
        Return month-by-month MRR for the last N months.
        Each item: {"month": <datetime>, "mrr_dollars": <float>}
        Returns [] if no data or DuckDB unavailable.
        """
        sql = """
            SELECT
                date_trunc('month', occurred_at) AS month,
                SUM(mrr_delta_cents) / 100.0 AS mrr_dollars
            FROM revenue_events
            WHERE occurred_at >= current_date - INTERVAL (?) MONTH
            GROUP BY 1
            ORDER BY 1
        """
        return self.query(sql, [months])

    def get_churn_rate(self) -> float:
        """
        Return the most recent month's churn rate as a fraction (0.0–1.0).
        Formula: churned_customers / total_customers for the latest month.
        Returns 0.0 if insufficient data or DuckDB unavailable.
        """
        rows = self.query(
            """
            SELECT
                churned,
                total_customers
            FROM v_churn
            ORDER BY month DESC
            LIMIT 1
            """
        )
        if not rows:
            return 0.0
        row = rows[0]
        total = row.get("total_customers") or 0
        churned = row.get("churned") or 0
        if total == 0:
            return 0.0
        return round(churned / total, 4)

    def get_current_arpu(self) -> Optional[float]:
        """
        Return ARPU (Average Revenue Per User) for the last 30 days.

        Formula: total revenue in last 30 days / count of distinct customers
        who had any revenue event in that window.

        Returns None if no data in the last 30 days or DuckDB unavailable.
        Returns 0.0 only when customers exist but revenue sums to zero.
        """
        rows = self.query(
            """
            SELECT
                COALESCE(SUM(amount_cents), 0) / 100.0 AS total_revenue,
                COUNT(DISTINCT customer_id) AS customer_count
            FROM revenue_events
            WHERE occurred_at >= current_date - INTERVAL 30 DAY
              AND amount_cents > 0
            """
        )
        if not rows:
            return None
        row = rows[0]
        customer_count = row.get("customer_count") or 0
        total_revenue = float(row.get("total_revenue") or 0.0)
        if customer_count == 0:
            return None
        return round(total_revenue / customer_count, 2)

    def get_recent_retention(self) -> dict:
        """
        Return retention metrics derived from user_events if available.

        Computes day-7 retention: fraction of users who had an event on day 0
        who also had an event on or after day 7.

        Returns a dict with available keys:
          - "day7": float 0.0–1.0 (None if insufficient data)
          - "cohort_size": int
          - "source": "user_events" | "no_data"

        Returns {"source": "no_data"} if user_events table is empty or
        DuckDB is unavailable. Never raises.
        """
        # Check if user_events has any rows
        count_rows = self.query("SELECT COUNT(*) AS n FROM user_events")
        if not count_rows or (count_rows[0].get("n") or 0) == 0:
            return {"source": "no_data"}

        # Day-7 retention: users with event on day 0 who return by day 7
        rows = self.query(
            """
            WITH cohort AS (
                SELECT
                    user_id,
                    MIN(occurred_at) AS first_seen
                FROM user_events
                WHERE user_id IS NOT NULL
                GROUP BY user_id
            ),
            retained AS (
                SELECT DISTINCT
                    c.user_id
                FROM cohort c
                JOIN user_events e ON e.user_id = c.user_id
                WHERE e.occurred_at >= c.first_seen + INTERVAL 7 DAY
            )
            SELECT
                COUNT(DISTINCT c.user_id) AS cohort_size,
                COUNT(DISTINCT r.user_id) AS returned_day7
            FROM cohort c
            LEFT JOIN retained r ON r.user_id = c.user_id
            """
        )
        if not rows:
            return {"source": "no_data"}

        row = rows[0]
        cohort_size = int(row.get("cohort_size") or 0)
        returned = int(row.get("returned_day7") or 0)

        if cohort_size == 0:
            return {"source": "no_data"}

        day7 = round(returned / cohort_size, 4)
        return {
            "day7": day7,
            "cohort_size": cohort_size,
            "returned_day7": returned,
            "source": "user_events",
        }

    def get_sync_state(self, source: str) -> dict:
        """
        Return sync state for the given source (e.g. "stripe").
        Returns {} if not found or DuckDB unavailable.
        """
        rows = self.query(
            "SELECT * FROM sync_state WHERE source = ?", [source]
        )
        return rows[0] if rows else {}

    def update_sync_state(self, source: str, cursor: str) -> None:
        """
        Upsert sync state for the given source with the provided cursor.
        No-op if DuckDB is unavailable.
        """
        if not self._ensure_conn():
            logger.warning("analytics_db: update_sync_state skipped — no DuckDB connection")
            return
        try:
            self._conn.execute(
                """
                INSERT INTO sync_state (source, last_cursor, last_synced_at, status)
                VALUES (?, ?, current_timestamp, 'ok')
                ON CONFLICT (source) DO UPDATE SET
                    last_cursor = excluded.last_cursor,
                    last_synced_at = excluded.last_synced_at,
                    status = excluded.status
                """,
                [source, cursor],
            )
        except Exception as exc:
            logger.warning("analytics_db: update_sync_state failed — %s", exc)

    def has_data(self) -> bool:
        """Return True if any revenue_events rows exist."""
        rows = self.query("SELECT COUNT(*) AS n FROM revenue_events")
        if not rows:
            return False
        return (rows[0].get("n") or 0) > 0

    def close(self) -> None:
        """Close the DuckDB connection if open."""
        if self._conn is not None:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None
            self._initialized = False


# ─────────────────────────────────────────────────────────────
# Module-level singleton
# ─────────────────────────────────────────────────────────────

_db: Optional[AnalyticsDB] = None


def get_analytics_db() -> AnalyticsDB:
    """
    Return the module-level AnalyticsDB singleton.
    Thread-safe for reads; concurrent writes should use application-level locking.
    """
    global _db
    if _db is None:
        _db = AnalyticsDB()
    return _db


# ─────────────────────────────────────────────────────────────
# Smoke test (python -m soloos_core.data.analytics_db)
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    print("=== analytics_db smoke test ===")
    db = get_analytics_db()
    print(f"DuckDB available : {_check_duckdb()}")
    print(f"DB path          : {db._db_path}")
    print(f"Initialized      : {db._initialized}")
    print(f"Current MRR      : ${db.get_current_mrr():,.2f}")
    print(f"Has data         : {db.has_data()}")
    print(f"MRR trend (3mo)  : {json.dumps(db.get_mrr_trend(3), default=str)}")
    print(f"Churn rate       : {db.get_churn_rate():.2%}")
    print(f"Current ARPU     : {db.get_current_arpu()}")
    print(f"Recent retention : {db.get_recent_retention()}")
    print(f"Sync state(stripe): {db.get_sync_state('stripe')}")
    print("=== done ===")
