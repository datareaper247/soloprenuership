"""
SoloOS V10 Phase B — SQLite Operational Store

Provides a structured SQLite backend for decisions, experiments, sessions,
and feedback. Dual-written alongside existing markdown files for safety.

DB path: ~/.soloos/context.db
Deps:    sqlite3 (stdlib only — zero new deps)

Migration:
  On first init, reads existing markdown entries via log_manager and imports
  them into SQLite. Sets a migration_done flag. Idempotent — safe to call
  multiple times.

Fail-open everywhere: if SQLite is unavailable for any reason, all methods
log a warning and return safe defaults. The caller is never interrupted.
"""

import json
import logging
import sqlite3
import uuid
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

_DB_PATH = Path.home() / ".soloos" / "context.db"

# ─────────────────────────────────────────────────────────────
# Schema DDL
# ─────────────────────────────────────────────────────────────

_DDL = [
    """
    CREATE TABLE IF NOT EXISTS decisions (
        id TEXT PRIMARY KEY,
        date TEXT NOT NULL,
        situation TEXT NOT NULL,
        decision TEXT NOT NULL,
        kill_signal TEXT,
        kill_signal_date TEXT,
        outcome TEXT,
        outcome_date TEXT,
        tags TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS experiments (
        id TEXT PRIMARY KEY,
        hypothesis TEXT NOT NULL,
        status TEXT DEFAULT 'running',
        started_at TEXT,
        completed_at TEXT,
        result TEXT,
        notes TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        started_at TEXT NOT NULL,
        context_snapshot TEXT,
        tools_used TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS feedback (
        id TEXT PRIMARY KEY,
        call_id TEXT NOT NULL,
        tool_name TEXT,
        rating INTEGER,
        reason TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )
    """,
    # sync_state doubles as a migration flag store
    """
    CREATE TABLE IF NOT EXISTS sync_state (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at TEXT DEFAULT (datetime('now'))
    )
    """,
]


# ─────────────────────────────────────────────────────────────
# ContextDB class
# ─────────────────────────────────────────────────────────────

class ContextDB:
    """
    SQLite operational store for SoloOS context data.

    All public methods are fail-open: they catch every exception, log a
    warning, and return a safe default (None, [], False, etc.) so that
    callers — especially log_manager.py dual-write paths — are never
    interrupted.
    """

    def __init__(self, db_path: Path = _DB_PATH) -> None:
        self._db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._available = False
        self._init()

    # ── Lifecycle ──────────────────────────────────────────────

    def _init(self) -> None:
        """Open connection and create schema. Fail-open."""
        try:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            for ddl in _DDL:
                self._conn.execute(ddl)
            self._conn.commit()
            self._available = True
            self._run_migration()
        except Exception as exc:
            logger.warning("context_db: init failed — %s", exc)
            self._available = False

    def is_available(self) -> bool:
        return self._available

    def close(self) -> None:
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass

    # ── Internal helpers ───────────────────────────────────────

    def _execute(self, sql: str, params: tuple = ()) -> Optional[sqlite3.Cursor]:
        """Run a statement, commit, return cursor. Returns None on failure."""
        if not self._available or not self._conn:
            return None
        try:
            cur = self._conn.execute(sql, params)
            self._conn.commit()
            return cur
        except Exception as exc:
            logger.warning("context_db: execute failed — %s | sql=%s", exc, sql[:80])
            return None

    def _fetchall(self, sql: str, params: tuple = ()) -> list[dict]:
        """Run a SELECT and return list of dicts. Returns [] on failure."""
        if not self._available or not self._conn:
            return []
        try:
            cur = self._conn.execute(sql, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        except Exception as exc:
            logger.warning("context_db: fetchall failed — %s", exc)
            return []

    def _fetchone(self, sql: str, params: tuple = ()) -> Optional[dict]:
        """Run a SELECT and return first row as dict. Returns None on failure."""
        rows = self._fetchall(sql, params)
        return rows[0] if rows else None

    # ── Sync / migration flag ──────────────────────────────────

    def get_sync_state(self, key: str) -> Optional[str]:
        row = self._fetchone("SELECT value FROM sync_state WHERE key = ?", (key,))
        return row["value"] if row else None

    def set_sync_state(self, key: str, value: str) -> None:
        self._execute(
            "INSERT OR REPLACE INTO sync_state (key, value, updated_at) "
            "VALUES (?, ?, datetime('now'))",
            (key, value),
        )

    # ── Migration ──────────────────────────────────────────────

    def _run_migration(self) -> None:
        """
        One-time import of existing markdown entries into SQLite.
        Safe to call multiple times — idempotent via migration_done flag.
        """
        try:
            if self.get_sync_state("migration_done") == "1":
                return

            # Import founder-log entries as decisions
            from soloos_core.log_manager import load_log  # lazy import — avoids circular
            entries = load_log()
            imported = 0
            for entry in entries:
                success = self.upsert_decision(
                    id=entry.id,
                    date=entry.date,
                    situation=entry.context,
                    decision=entry.summary,
                    kill_signal=entry.kill_signal,
                    kill_signal_date=entry.kill_signal_due,
                    outcome=None if entry.outcome == "PENDING OUTCOME" else entry.outcome,
                    outcome_date=entry.outcome_due,
                    tags=entry.type,
                )
                if success:
                    imported += 1

            self.set_sync_state("migration_done", "1")
            logger.info("context_db: migration complete — %d entries imported", imported)
        except Exception as exc:
            logger.warning("context_db: migration failed (non-fatal) — %s", exc)
            # Do NOT set migration_done so it retries next time

    # ── Decisions CRUD ─────────────────────────────────────────

    def upsert_decision(
        self,
        id: str,
        date: str,
        situation: str,
        decision: str,
        kill_signal: Optional[str] = None,
        kill_signal_date: Optional[str] = None,
        outcome: Optional[str] = None,
        outcome_date: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> bool:
        """Insert or replace a decision row. Returns True on success."""
        cur = self._execute(
            """
            INSERT OR REPLACE INTO decisions
                (id, date, situation, decision, kill_signal, kill_signal_date,
                 outcome, outcome_date, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (id, date, situation, decision, kill_signal, kill_signal_date,
             outcome, outcome_date, tags),
        )
        return cur is not None

    def get_decision(self, id: str) -> Optional[dict]:
        return self._fetchone("SELECT * FROM decisions WHERE id = ?", (id,))

    def list_decisions(self, limit: int = 100) -> list[dict]:
        return self._fetchall(
            "SELECT * FROM decisions ORDER BY date DESC LIMIT ?", (limit,)
        )

    def update_decision_outcome(
        self, id: str, outcome: str, outcome_date: Optional[str] = None
    ) -> bool:
        cur = self._execute(
            "UPDATE decisions SET outcome = ?, outcome_date = ? WHERE id = ?",
            (outcome, outcome_date, id),
        )
        return cur is not None and cur.rowcount > 0

    def get_pending_kill_signals(self) -> list[dict]:
        """Return decisions that have a kill_signal but no outcome recorded."""
        return self._fetchall(
            """
            SELECT * FROM decisions
            WHERE kill_signal IS NOT NULL
              AND (outcome IS NULL OR outcome = '')
            ORDER BY kill_signal_date ASC
            """
        )

    # ── Experiments CRUD ───────────────────────────────────────

    def upsert_experiment(
        self,
        id: str,
        hypothesis: str,
        status: str = "running",
        started_at: Optional[str] = None,
        completed_at: Optional[str] = None,
        result: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> bool:
        cur = self._execute(
            """
            INSERT OR REPLACE INTO experiments
                (id, hypothesis, status, started_at, completed_at, result, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (id, hypothesis, status, started_at, completed_at, result, notes),
        )
        return cur is not None

    def get_experiment(self, id: str) -> Optional[dict]:
        return self._fetchone("SELECT * FROM experiments WHERE id = ?", (id,))

    def list_experiments(self, status: Optional[str] = None) -> list[dict]:
        if status:
            return self._fetchall(
                "SELECT * FROM experiments WHERE status = ? ORDER BY started_at DESC",
                (status,),
            )
        return self._fetchall("SELECT * FROM experiments ORDER BY started_at DESC")

    # ── Sessions ───────────────────────────────────────────────

    def log_session(
        self,
        id: Optional[str] = None,
        started_at: Optional[str] = None,
        context_snapshot: Optional[dict] = None,
        tools_used: Optional[list] = None,
    ) -> Optional[str]:
        """Log a session start. Returns session id on success, None on failure."""
        session_id = id or str(uuid.uuid4())
        from datetime import datetime
        ts = started_at or datetime.utcnow().isoformat()
        snapshot_json = json.dumps(context_snapshot) if context_snapshot else None
        tools_json = json.dumps(tools_used) if tools_used else None
        cur = self._execute(
            "INSERT OR IGNORE INTO sessions (id, started_at, context_snapshot, tools_used) "
            "VALUES (?, ?, ?, ?)",
            (session_id, ts, snapshot_json, tools_json),
        )
        return session_id if cur is not None else None

    # ── Feedback ───────────────────────────────────────────────

    def log_feedback(
        self,
        call_id: str,
        tool_name: Optional[str] = None,
        rating: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> bool:
        feedback_id = str(uuid.uuid4())
        cur = self._execute(
            "INSERT INTO feedback (id, call_id, tool_name, rating, reason) "
            "VALUES (?, ?, ?, ?, ?)",
            (feedback_id, call_id, tool_name, rating, reason),
        )
        return cur is not None

    def list_feedback(self, limit: int = 50) -> list[dict]:
        return self._fetchall(
            "SELECT * FROM feedback ORDER BY created_at DESC LIMIT ?", (limit,)
        )

    # ── Stats ──────────────────────────────────────────────────

    def get_stats(self) -> dict:
        """Return row counts per table for observability."""
        if not self._available:
            return {"available": False}
        tables = ["decisions", "experiments", "sessions", "feedback"]
        counts = {}
        for t in tables:
            rows = self._fetchone(f"SELECT COUNT(*) AS n FROM {t}")
            counts[t] = rows["n"] if rows else 0
        return {
            "available": True,
            "db_path": str(self._db_path),
            **counts,
        }


# ─────────────────────────────────────────────────────────────
# Module-level singleton (lazy, fail-open)
# ─────────────────────────────────────────────────────────────

_db: Optional[ContextDB] = None


def get_context_db() -> ContextDB:
    """Return the module-level ContextDB singleton. Never raises."""
    global _db
    if _db is None:
        try:
            _db = ContextDB()
        except Exception as exc:
            logger.warning("context_db: singleton init failed — %s", exc)
            # Return a non-available stub so callers can still call methods safely
            _db = _UnavailableContextDB()
    return _db


class _UnavailableContextDB(ContextDB):
    """Stub returned when SQLite is completely unavailable."""

    def __init__(self) -> None:
        # Skip full init — just mark unavailable
        self._db_path = _DB_PATH
        self._conn = None
        self._available = False


# ─────────────────────────────────────────────────────────────
# Smoke test
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        db = ContextDB(db_path=Path(tmp) / "test.db")
        assert db.is_available(), "DB should be available"
        ok = db.upsert_decision(
            id="FL-001",
            date="2026-03-26",
            situation="Testing smoke test",
            decision="Run the smoke test",
            kill_signal="If test fails",
            kill_signal_date="2026-04-26",
        )
        assert ok, "upsert_decision should succeed"
        row = db.get_decision("FL-001")
        assert row is not None and row["decision"] == "Run the smoke test"
        stats = db.get_stats()
        # Migration may have imported entries from existing markdown — use >= 1
        assert stats["decisions"] >= 1
        print("context_db smoke test: PASSED")
