"""
Persistent World Model — the AI's understanding of the business at any moment.

Reads from: DuckDB (analytics), SQLite (decisions, experiments)
Writes to: SQLite (world_model_state table)
Refreshes: on demand or triggered by significant events
"""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DB_PATH = Path.home() / ".soloos" / "context.db"

_DDL = """
CREATE TABLE IF NOT EXISTS world_model_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot TEXT NOT NULL,
    refreshed_at TEXT NOT NULL,
    section TEXT DEFAULT 'full'
);
"""

_EMPTY_MODEL: dict = {
    "metrics": {
        "mrr": 0,
        "arr": 0,
        "churn_rate": 0,
        "nps": None,
        "active_customers": 0,
        "runway_months": None,
    },
    "goals": {
        "mrr_target": None,
        "pmf_score": None,
        "next_milestone": None,
        "kill_signals": [],
    },
    "experiments": [],
    "decisions": [],
    "market_signals": [],
    "agent_state": {
        "last_run": None,
        "pending_tasks": 0,
        "notes": [],
    },
    "refreshed_at": None,
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class WorldModel:
    def __init__(self, db_path: Path | None = None) -> None:
        self._path = db_path or _DB_PATH
        self._cache: dict | None = None
        self._init_db()

    def _init_db(self) -> None:
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._conn() as conn:
                conn.execute(_DDL)
        except Exception as exc:
            logger.warning("WorldModel._init_db failed: %s", exc)

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._path))
        conn.row_factory = sqlite3.Row
        return conn

    def refresh(self) -> dict:
        """Recompute world model from all sources."""
        model = dict(_EMPTY_MODEL)
        model["metrics"] = dict(_EMPTY_MODEL["metrics"])
        model["goals"] = dict(_EMPTY_MODEL["goals"])
        model["agent_state"] = dict(_EMPTY_MODEL["agent_state"])
        model["refreshed_at"] = _now()
        model["data_sources_ok"] = {}  # health flag: tracks which sources succeeded

        # Pull metrics from context DB if available
        try:
            model.update(self._pull_from_sqlite())
            model["data_sources_ok"]["sqlite"] = True
        except Exception as exc:
            logger.warning("WorldModel.refresh sqlite pull failed: %s", exc)
            model["data_sources_ok"]["sqlite"] = False

        # Auto-sync Stripe if configured and stale (>1 hour since last sync)
        self._maybe_sync_stripe()

        # Pull from analytics DB (DuckDB) if available
        try:
            result = self._pull_from_analytics()
            model.update(result)
            model["data_sources_ok"]["duckdb"] = True
        except Exception as exc:
            logger.debug("WorldModel.refresh duckdb pull skipped: %s", exc)
            model["data_sources_ok"]["duckdb"] = False

        self._cache = model
        self._persist(model)
        return model

    def _pull_from_sqlite(self) -> dict:
        """Pull recent decisions and experiments from context.db."""
        updates: dict = {}
        with self._conn() as conn:
            # Recent decisions
            try:
                rows = conn.execute(
                    "SELECT * FROM decisions ORDER BY created_at DESC LIMIT 5"
                ).fetchall()
                updates["decisions"] = [dict(r) for r in rows]
            except Exception:
                pass

            # Running experiments
            try:
                rows = conn.execute(
                    "SELECT * FROM experiments WHERE status='running' ORDER BY started_at DESC LIMIT 10"
                ).fetchall()
                updates["experiments"] = [dict(r) for r in rows]
            except Exception:
                pass

            # Pending tasks count
            try:
                row = conn.execute(
                    "SELECT COUNT(*) as cnt FROM agent_tasks WHERE status='pending'"
                ).fetchone()
                if row:
                    updates.setdefault("agent_state", {})["pending_tasks"] = row["cnt"]
            except Exception:
                pass

        return updates

    def _maybe_sync_stripe(self) -> None:
        """
        Trigger an incremental Stripe sync if:
          - STRIPE_API_KEY is set and stripe SDK is installed
          - Last sync was more than 1 hour ago (or never ran)
        Runs silently — errors are logged at DEBUG level only.
        """
        import os
        if not os.environ.get("STRIPE_API_KEY"):
            return
        try:
            from datetime import timedelta
            from soloos_core.data.analytics_db import get_analytics_db
            from soloos_core.data.connectors.stripe_connector import StripeConnector

            connector = StripeConnector()
            if not connector.is_configured():
                return

            db = get_analytics_db()
            state = db.get_sync_state("stripe")
            last_synced_at = state.get("last_synced_at")

            if last_synced_at:
                # Parse the timestamp returned by DuckDB (already a datetime or ISO string)
                if isinstance(last_synced_at, str):
                    from datetime import datetime as _dt
                    last_synced_at = _dt.fromisoformat(last_synced_at.replace(" ", "T"))
                age = datetime.now(timezone.utc) - last_synced_at.replace(tzinfo=timezone.utc)
                if age < timedelta(hours=1):
                    logger.debug("WorldModel: Stripe sync skipped — synced %.0f min ago", age.total_seconds() / 60)
                    return

            cursor = state.get("last_cursor")
            result = connector.sync(since_cursor=cursor)
            if result.error:
                logger.debug("WorldModel: Stripe auto-sync failed — %s", result.error)
            else:
                logger.info("WorldModel: Stripe auto-sync — %d rows", result.rows_synced)
        except Exception as exc:
            logger.debug("WorldModel._maybe_sync_stripe: %s", exc)

    def _pull_from_analytics(self) -> dict:
        """Pull MRR and key metrics from analytics DuckDB if available."""
        analytics_path = Path.home() / ".soloos" / "analytics.duckdb"
        if not analytics_path.exists():
            return {}

        try:
            import duckdb  # type: ignore[import]
            conn = duckdb.connect(str(analytics_path), read_only=True)
            # Try to get latest MRR snapshot
            try:
                row = conn.execute(
                    "SELECT mrr, arr, active_customers FROM metrics_daily ORDER BY date DESC LIMIT 1"
                ).fetchone()
                if row:
                    return {"metrics": {"mrr": row[0], "arr": row[1], "active_customers": row[2]}}
            except Exception:
                pass
            finally:
                conn.close()
        except ImportError:
            pass
        return {}

    def _persist(self, model: dict) -> None:
        try:
            with self._conn() as conn:
                conn.execute(
                    "INSERT INTO world_model_state (snapshot, refreshed_at) VALUES (?, ?)",
                    (json.dumps(model, default=str), _now()),
                )
                # Keep only last 100 snapshots
                conn.execute(
                    "DELETE FROM world_model_state WHERE id NOT IN "
                    "(SELECT id FROM world_model_state ORDER BY id DESC LIMIT 100)"
                )
        except Exception as exc:
            logger.warning("WorldModel._persist failed: %s", exc)

    def get(self) -> dict:
        """Return current cached snapshot, refresh if none."""
        if self._cache is None:
            # Try loading from DB first
            try:
                with self._conn() as conn:
                    row = conn.execute(
                        "SELECT snapshot FROM world_model_state ORDER BY id DESC LIMIT 1"
                    ).fetchone()
                    if row:
                        self._cache = json.loads(row["snapshot"])
                        return self._cache
            except Exception:
                pass
            return self.refresh()
        return self._cache

    def get_section(self, key: str) -> dict:
        """Get a specific section of the world model."""
        return self.get().get(key, {})

    def update_goals(self, goals: dict) -> None:
        model = self.get()
        model.setdefault("goals", {}).update(goals)
        self._cache = model
        self._persist(model)

    def update_agent_state(self, state: dict) -> None:
        model = self.get()
        model.setdefault("agent_state", {}).update(state)
        model["agent_state"]["last_run"] = _now()
        self._cache = model
        self._persist(model)

    def get_context_for_agent(self, agent_role: str) -> str:
        """Return formatted context string for LLM prompt."""
        model = self.get()
        metrics = model.get("metrics", {})
        goals = model.get("goals", {})

        lines = [
            f"## Business Context for {agent_role}",
            f"MRR: ${metrics.get('mrr', 0):,.0f}",
            f"Active customers: {metrics.get('active_customers', 0)}",
            f"Churn rate: {metrics.get('churn_rate', 0):.1%}" if metrics.get('churn_rate') else "Churn rate: unknown",
            f"Runway: {metrics.get('runway_months', 'unknown')} months",
            "",
            "## Current Goals",
        ]
        if goals.get("next_milestone"):
            lines.append(f"Next milestone: {goals['next_milestone']}")
        if goals.get("kill_signals"):
            lines.append(f"Active kill signals: {len(goals['kill_signals'])}")

        # Pending experiments
        experiments = model.get("experiments", [])
        if experiments:
            lines.append(f"\n## Running Experiments ({len(experiments)})")
            for exp in experiments[:3]:
                lines.append(f"- {exp.get('hypothesis', 'Unknown')}")

        return "\n".join(lines)


_world_model: WorldModel | None = None


def get_world_model() -> WorldModel:
    global _world_model
    if _world_model is None:
        _world_model = WorldModel()
    return _world_model
