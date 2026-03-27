"""
SQLite-backed task queue for autonomous agent operations.
DB: reuses ~/.soloos/context.db (adds 'agent_tasks' table)

Schema:
    CREATE TABLE agent_tasks (
        id TEXT PRIMARY KEY,
        task_type TEXT NOT NULL,
        priority INTEGER DEFAULT 5,
        payload TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT,
        started_at TEXT,
        completed_at TEXT,
        result TEXT,
        error TEXT,
        retry_count INTEGER DEFAULT 0,
        max_retries INTEGER DEFAULT 3,
        agent_id TEXT DEFAULT 'founder'
    );
"""

from __future__ import annotations

import json
import logging
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DB_PATH = Path.home() / ".soloos" / "context.db"

_DDL = """
CREATE TABLE IF NOT EXISTS agent_tasks (
    id TEXT PRIMARY KEY,
    task_type TEXT NOT NULL,
    priority INTEGER DEFAULT 5,
    payload TEXT,
    status TEXT DEFAULT 'pending',
    created_at TEXT,
    started_at TEXT,
    completed_at TEXT,
    result TEXT,
    error TEXT,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    agent_id TEXT DEFAULT 'founder'
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class TaskQueue:
    def __init__(self, db_path: Path | None = None) -> None:
        self._path = db_path or _DB_PATH
        self._init_db()

    def _init_db(self) -> None:
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._conn() as conn:
                conn.execute(_DDL)
        except Exception as exc:
            logger.warning("TaskQueue._init_db failed (non-fatal): %s", exc)

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._path))
        conn.row_factory = sqlite3.Row
        return conn

    def enqueue(self, task_type: str, payload: dict, priority: int = 5, agent_id: str = "founder") -> str:
        """Add task to queue. Returns task_id."""
        task_id = str(uuid.uuid4())
        try:
            with self._conn() as conn:
                conn.execute(
                    """INSERT INTO agent_tasks
                       (id, task_type, priority, payload, status, created_at, agent_id)
                       VALUES (?, ?, ?, ?, 'pending', ?, ?)""",
                    (task_id, task_type, priority, json.dumps(payload), _now(), agent_id),
                )
        except Exception as exc:
            logger.warning("TaskQueue.enqueue failed: %s", exc)
        return task_id

    def dequeue(self, agent_id: str | None = None) -> dict | None:
        """
        Get highest-priority pending task (lowest priority number = highest urgency).

        Uses BEGIN IMMEDIATE to prevent two concurrent workers from claiming the
        same task between the SELECT and UPDATE (TOCTOU race condition).
        """
        conn = self._conn()
        try:
            conn.execute("BEGIN IMMEDIATE")
            if agent_id:
                row = conn.execute(
                    """SELECT * FROM agent_tasks
                       WHERE status='pending' AND agent_id=?
                       ORDER BY priority ASC, created_at ASC LIMIT 1""",
                    (agent_id,),
                ).fetchone()
            else:
                row = conn.execute(
                    """SELECT * FROM agent_tasks
                       WHERE status='pending'
                       ORDER BY priority ASC, created_at ASC LIMIT 1"""
                ).fetchone()

            if row is None:
                conn.rollback()
                return None

            task_id = row["id"]
            started = _now()
            updated = conn.execute(
                "UPDATE agent_tasks SET status='running', started_at=? WHERE id=? AND status='pending'",
                (started, task_id),
            ).rowcount

            if updated == 0:
                # Race: another worker claimed it between our SELECT and UPDATE
                conn.rollback()
                return None

            conn.commit()
            d = self._row_to_dict(row)
            d["status"] = "running"
            d["started_at"] = started
            return d
        except Exception as exc:
            try:
                conn.rollback()
            except Exception:
                pass
            logger.warning("TaskQueue.dequeue failed: %s", exc)
            return None
        finally:
            conn.close()

    def complete(self, task_id: str, result: dict) -> None:
        try:
            with self._conn() as conn:
                conn.execute(
                    "UPDATE agent_tasks SET status='done', completed_at=?, result=? WHERE id=?",
                    (_now(), json.dumps(result), task_id),
                )
        except Exception as exc:
            logger.warning("TaskQueue.complete failed: %s", exc)

    def fail(self, task_id: str, error: str) -> None:
        try:
            with self._conn() as conn:
                row = conn.execute(
                    "SELECT retry_count, max_retries FROM agent_tasks WHERE id=?", (task_id,)
                ).fetchone()
                if row:
                    retry_count = (row["retry_count"] or 0) + 1
                    if retry_count < (row["max_retries"] or 3):
                        conn.execute(
                            "UPDATE agent_tasks SET status='pending', retry_count=?, error=? WHERE id=?",
                            (retry_count, error, task_id),
                        )
                    else:
                        conn.execute(
                            "UPDATE agent_tasks SET status='failed', retry_count=?, error=?, completed_at=? WHERE id=?",
                            (retry_count, error, _now(), task_id),
                        )
        except Exception as exc:
            logger.warning("TaskQueue.fail failed: %s", exc)

    def cancel(self, task_id: str) -> None:
        try:
            with self._conn() as conn:
                conn.execute(
                    "UPDATE agent_tasks SET status='cancelled', completed_at=? WHERE id=?",
                    (_now(), task_id),
                )
        except Exception as exc:
            logger.warning("TaskQueue.cancel failed: %s", exc)

    def list_pending(self) -> list[dict]:
        try:
            with self._conn() as conn:
                rows = conn.execute(
                    "SELECT * FROM agent_tasks WHERE status='pending' ORDER BY priority ASC, created_at ASC"
                ).fetchall()
                return [self._row_to_dict(r) for r in rows]
        except Exception as exc:
            logger.warning("TaskQueue.list_pending failed: %s", exc)
            return []

    def list_recent(self, hours: int = 24) -> list[dict]:
        from datetime import timedelta
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        try:
            with self._conn() as conn:
                rows = conn.execute(
                    "SELECT * FROM agent_tasks WHERE created_at >= ? ORDER BY created_at DESC",
                    (cutoff,),
                ).fetchall()
                return [self._row_to_dict(r) for r in rows]
        except Exception as exc:
            logger.warning("TaskQueue.list_recent failed: %s", exc)
            return []

    def stats(self) -> dict:
        try:
            with self._conn() as conn:
                rows = conn.execute(
                    "SELECT status, COUNT(*) as cnt FROM agent_tasks GROUP BY status"
                ).fetchall()
                return {r["status"]: r["cnt"] for r in rows}
        except Exception as exc:
            logger.warning("TaskQueue.stats failed: %s", exc)
            return {}

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict:
        d = dict(row)
        if d.get("payload"):
            try:
                d["payload"] = json.loads(d["payload"])
            except Exception:
                pass
        if d.get("result"):
            try:
                d["result"] = json.loads(d["result"])
            except Exception:
                pass
        return d


_queue: TaskQueue | None = None


def get_task_queue() -> TaskQueue:
    global _queue
    if _queue is None:
        _queue = TaskQueue()
    return _queue
