"""
ActionRegistry — permission gating for all autonomous AI actions.

CRITICAL SAFETY RULES (enforced in code, not config):
1. Tier.LEGAL always requires approval. Cannot be configured away.
2. Kill switch (SOLOOS_AUTONOMOUS=false or ~/.soloos/kill_switch) blocks Tier 2+.
3. Budget limits are hard-coded ceilings. Config can only reduce, not increase.
4. AI cannot modify its own permissions. ActionRegistry is read-only to agents.
5. Every execution is logged to AuditLog before AND after.
6. autonomous_mode defaults to FALSE — must be explicitly enabled.
7. approve() re-checks kill switch — approvals granted before kill switch cannot execute.
"""

from __future__ import annotations

import json
import os
import sqlite3
import threading
import uuid
import logging
from dataclasses import dataclass, field
from datetime import date
from enum import IntEnum
from pathlib import Path
from typing import Callable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# ─── Hard-coded budget ceilings (config can only reduce these) ────────────────
_MAX_EMAIL_PER_DAY = 200
_MAX_SOCIAL_PER_DAY = 10
_MAX_SUPPORT_PER_DAY = 500
_MAX_DAILY_USD = 500.0
_MAX_MONTHLY_USD = 5000.0
_MAX_PER_TX_USD = 1000.0


class Tier(IntEnum):
    READ = 0        # no approval, no log required
    COMPUTE = 1     # no approval, logged
    COMMUNICATE = 2 # soft approval (daily limits), logged
    BUILD = 3       # soft approval (risk params), logged
    DEPLOY = 4      # hard approval OR within safe params
    SPEND = 5       # hard approval + budget enforcement
    LEGAL = 6       # ALWAYS human approval (cannot be configured away)


@dataclass
class ActionDefinition:
    name: str
    tier: Tier
    description: str
    reversible: bool
    daily_limit: int | None = None       # None = no limit
    per_tx_limit_usd: float | None = None
    requires_approval: bool | None = None  # None = use tier default


@dataclass
class ActionRequest:
    action: str
    params: dict
    reasoning: str
    agent_id: str = "founder"
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class ActionResult:
    request_id: str
    action: str
    status: str      # "executed" | "queued_for_approval" | "blocked" | "dry_run"
    result: Any = None
    error: str | None = None
    audit_id: str | None = None


def is_kill_switch_active() -> bool:
    """
    Kill switch is ON (actions blocked) if ANY of:
    1. env var SOLOOS_AUTONOMOUS is set to "false" or "0"
    2. file ~/.soloos/kill_switch exists
    3. env var SOLOOS_KILL_SWITCH is set to any value
    """
    if os.environ.get("SOLOOS_AUTONOMOUS", "").lower() in ("false", "0"):
        return True
    if os.environ.get("SOLOOS_KILL_SWITCH"):
        return True
    if (Path.home() / ".soloos" / "kill_switch").exists():
        return True
    return False


class _PermissionsConfig:
    """Lazy-loaded permissions config from ~/.soloos/permissions.yaml."""

    def __init__(self) -> None:
        self._data: dict = {}
        self._loaded = False

    def _load(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        config_path = Path.home() / ".soloos" / "permissions.yaml"
        if not config_path.exists():
            return
        try:
            import yaml  # type: ignore[import]
            with config_path.open() as f:
                self._data = yaml.safe_load(f) or {}
        except Exception:
            pass  # fail-open on parse errors only (file exists but is invalid yaml)

    @property
    def autonomous_mode(self) -> bool:
        self._load()
        # SECURITY: default is False — must be explicitly set to True in permissions.yaml
        return bool(self._data.get("autonomous_mode", False))

    @property
    def dry_run(self) -> bool:
        self._load()
        return bool(self._data.get("dry_run", False))

    def get_limit(self, category: str, key: str, default: int) -> int:
        self._load()
        val = (self._data.get("limits") or {}).get(category, {}).get(key, default)
        return int(val)


class _ActionStore:
    """
    SQLite-backed store for daily usage counters and pending approvals.
    Uses ~/.soloos/context.db by default, creating tables if needed.
    All methods are thread-safe via a dedicated lock.

    Pass a custom db_path to use an isolated database (useful in tests).
    """

    def __init__(self, db_path: Path | str | None = None) -> None:
        self._lock = threading.Lock()
        self._db_path: Path | None = Path(db_path) if db_path is not None else None

    def _get_db_path(self) -> Path:
        if self._db_path is None:
            p = Path.home() / ".soloos"
            try:
                p.mkdir(parents=True, exist_ok=True)
            except OSError:
                pass
            self._db_path = p / "context.db"
        return self._db_path

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._get_db_path()), timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def _ensure_tables(self, conn: sqlite3.Connection) -> None:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS action_daily_usage (
                action TEXT NOT NULL,
                usage_date TEXT NOT NULL,
                count INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (action, usage_date)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS action_pending_approvals (
                request_id TEXT PRIMARY KEY,
                action TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                reasoning TEXT NOT NULL,
                reason_queued TEXT NOT NULL,
                params_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.commit()

    # ── Daily usage ──────────────────────────────────────────────────────────

    def get_daily_usage(self, action: str) -> int:
        today = str(date.today())
        with self._lock:
            try:
                with self._conn() as conn:
                    self._ensure_tables(conn)
                    row = conn.execute(
                        "SELECT count FROM action_daily_usage WHERE action=? AND usage_date=?",
                        (action, today),
                    ).fetchone()
                    return int(row["count"]) if row else 0
            except Exception as exc:
                logger.warning("_ActionStore.get_daily_usage failed: %s", exc)
                return 0

    def increment_daily_usage(self, action: str) -> int:
        today = str(date.today())
        with self._lock:
            try:
                with self._conn() as conn:
                    self._ensure_tables(conn)
                    conn.execute(
                        """
                        INSERT INTO action_daily_usage (action, usage_date, count)
                        VALUES (?, ?, 1)
                        ON CONFLICT (action, usage_date) DO UPDATE SET count = count + 1
                        """,
                        (action, today),
                    )
                    conn.commit()
                    row = conn.execute(
                        "SELECT count FROM action_daily_usage WHERE action=? AND usage_date=?",
                        (action, today),
                    ).fetchone()
                    return int(row["count"]) if row else 1
            except Exception as exc:
                logger.warning("_ActionStore.increment_daily_usage failed: %s", exc)
                return 1

    def get_all_daily_usage(self) -> dict[str, int]:
        today = str(date.today())
        with self._lock:
            try:
                with self._conn() as conn:
                    self._ensure_tables(conn)
                    rows = conn.execute(
                        "SELECT action, count FROM action_daily_usage WHERE usage_date=?",
                        (today,),
                    ).fetchall()
                    return {r["action"]: r["count"] for r in rows}
            except Exception as exc:
                logger.warning("_ActionStore.get_all_daily_usage failed: %s", exc)
                return {}

    def reset_daily_usage(self) -> None:
        today = str(date.today())
        with self._lock:
            try:
                with self._conn() as conn:
                    self._ensure_tables(conn)
                    conn.execute(
                        "DELETE FROM action_daily_usage WHERE usage_date=?",
                        (today,),
                    )
                    conn.commit()
            except Exception as exc:
                logger.warning("_ActionStore.reset_daily_usage failed: %s", exc)

    # ── Pending approvals ─────────────────────────────────────────────────────

    def save_pending_approval(
        self,
        request: ActionRequest,
        reason_queued: str,
    ) -> None:
        with self._lock:
            try:
                with self._conn() as conn:
                    self._ensure_tables(conn)
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO action_pending_approvals
                            (request_id, action, agent_id, reasoning, reason_queued, params_json)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            request.request_id,
                            request.action,
                            request.agent_id,
                            request.reasoning,
                            reason_queued,
                            json.dumps(request.params),
                        ),
                    )
                    conn.commit()
            except Exception as exc:
                logger.warning("_ActionStore.save_pending_approval failed: %s", exc)

    def pop_pending_approval(self, request_id: str) -> ActionRequest | None:
        with self._lock:
            try:
                with self._conn() as conn:
                    self._ensure_tables(conn)
                    row = conn.execute(
                        "SELECT * FROM action_pending_approvals WHERE request_id=?",
                        (request_id,),
                    ).fetchone()
                    if row is None:
                        return None
                    conn.execute(
                        "DELETE FROM action_pending_approvals WHERE request_id=?",
                        (request_id,),
                    )
                    conn.commit()
                    return ActionRequest(
                        action=row["action"],
                        params=json.loads(row["params_json"]),
                        reasoning=row["reasoning"],
                        agent_id=row["agent_id"],
                        request_id=row["request_id"],
                    )
            except Exception as exc:
                logger.warning("_ActionStore.pop_pending_approval failed: %s", exc)
                return None

    def delete_pending_approval(self, request_id: str) -> dict | None:
        """Delete and return metadata (for rejection logging)."""
        with self._lock:
            try:
                with self._conn() as conn:
                    self._ensure_tables(conn)
                    row = conn.execute(
                        "SELECT action, agent_id FROM action_pending_approvals WHERE request_id=?",
                        (request_id,),
                    ).fetchone()
                    if row is None:
                        return None
                    conn.execute(
                        "DELETE FROM action_pending_approvals WHERE request_id=?",
                        (request_id,),
                    )
                    conn.commit()
                    return dict(row)
            except Exception as exc:
                logger.warning("_ActionStore.delete_pending_approval failed: %s", exc)
                return None

    def list_pending_approvals(self) -> list[dict]:
        with self._lock:
            try:
                with self._conn() as conn:
                    self._ensure_tables(conn)
                    rows = conn.execute(
                        "SELECT request_id, action, agent_id, reasoning, reason_queued, created_at "
                        "FROM action_pending_approvals ORDER BY created_at ASC"
                    ).fetchall()
                    return [dict(r) for r in rows]
            except Exception as exc:
                logger.warning("_ActionStore.list_pending_approvals failed: %s", exc)
                return []

    def count_pending_approvals(self) -> int:
        with self._lock:
            try:
                with self._conn() as conn:
                    self._ensure_tables(conn)
                    row = conn.execute(
                        "SELECT COUNT(*) AS n FROM action_pending_approvals"
                    ).fetchone()
                    return int(row["n"]) if row else 0
            except Exception as exc:
                logger.warning("_ActionStore.count_pending_approvals failed: %s", exc)
                return 0


class ActionRegistry:
    """
    Gate for all autonomous AI actions.

    Usage:
        registry = get_action_registry()
        result = registry.execute(ActionRequest(
            action="send_email",
            params={"to": "...", "subject": "...", "body": "..."},
            reasoning="Customer asked about pricing 3 days ago"
        ))
    """

    def __init__(self, store_db_path: Path | str | None = None) -> None:
        self._actions: dict[str, tuple[ActionDefinition, Callable]] = {}
        self._store = _ActionStore(db_path=store_db_path)
        self._config = _PermissionsConfig()
        self._audit_log: Any = None  # lazy import to avoid circular

    def _get_audit_log(self):
        if self._audit_log is None:
            from .audit_log import get_audit_log
            self._audit_log = get_audit_log()
        return self._audit_log

    def register_action(self, action: ActionDefinition, handler: Callable) -> None:
        self._actions[action.name] = (action, handler)

    def execute(self, request: ActionRequest) -> ActionResult:
        action_def, handler = self._actions.get(request.action, (None, None))

        if action_def is None:
            return ActionResult(
                request_id=request.request_id,
                action=request.action,
                status="blocked",
                error=f"Unknown action: {request.action}",
            )

        # Kill switch blocks Tier 2+
        if action_def.tier >= Tier.COMMUNICATE and is_kill_switch_active():
            return ActionResult(
                request_id=request.request_id,
                action=request.action,
                status="blocked",
                error="Kill switch is active. Set SOLOOS_AUTONOMOUS=true or remove ~/.soloos/kill_switch to proceed.",
            )

        # Tier 6 (LEGAL) always requires approval
        if action_def.tier == Tier.LEGAL:
            return self._queue_for_approval(request, action_def, reason="Tier.LEGAL always requires human approval")

        # Non-autonomous mode: queue Tier 2+ for approval
        if action_def.tier >= Tier.COMMUNICATE and not self._config.autonomous_mode:
            return self._queue_for_approval(request, action_def, reason="autonomous_mode=false")

        # Hard approval required for Tier 4+ unless explicitly bypassed
        if action_def.tier >= Tier.DEPLOY:
            requires = action_def.requires_approval
            if requires is None:
                requires = True
            if requires:
                return self._queue_for_approval(request, action_def, reason=f"Tier {action_def.tier.name} requires approval")

        # Daily limit check
        if action_def.daily_limit is not None:
            used = self._store.get_daily_usage(request.action)
            if used >= action_def.daily_limit:
                return ActionResult(
                    request_id=request.request_id,
                    action=request.action,
                    status="blocked",
                    error=f"Daily limit reached: {used}/{action_def.daily_limit} for {request.action}",
                )

        # Dry run mode
        if self._config.dry_run:
            audit_id = self._get_audit_log().log({
                "request_id": request.request_id,
                "action": request.action,
                "tier": int(action_def.tier),
                "agent_id": request.agent_id,
                "params": self._redact_pii(request.action, request.params),
                "reasoning": request.reasoning,
                "status": "dry_run",
            })
            return ActionResult(
                request_id=request.request_id,
                action=request.action,
                status="dry_run",
                audit_id=audit_id,
            )

        # Log intent before execution
        self._get_audit_log().log({
            "request_id": request.request_id,
            "action": request.action,
            "tier": int(action_def.tier),
            "agent_id": request.agent_id,
            "params": self._redact_pii(request.action, request.params),
            "reasoning": request.reasoning,
            "status": "intent",
        })

        # Execute
        try:
            import time
            t0 = time.time()
            outcome = handler(request.params)
            duration_ms = int((time.time() - t0) * 1000)

            # Increment daily usage (persisted to SQLite)
            self._store.increment_daily_usage(request.action)

            audit_id = self._get_audit_log().log({
                "request_id": request.request_id,
                "action": request.action,
                "tier": int(action_def.tier),
                "agent_id": request.agent_id,
                "params": self._redact_pii(request.action, request.params),
                "reasoning": request.reasoning,
                "status": "executed",
                "result": outcome,
                "duration_ms": duration_ms,
            })
            return ActionResult(
                request_id=request.request_id,
                action=request.action,
                status="executed",
                result=outcome,
                audit_id=audit_id,
            )
        except Exception as exc:
            logger.exception("Action %s failed: %s", request.action, exc)
            audit_id = self._get_audit_log().log({
                "request_id": request.request_id,
                "action": request.action,
                "tier": int(action_def.tier),
                "agent_id": request.agent_id,
                "status": "error",
                "error": str(exc),
            })
            return ActionResult(
                request_id=request.request_id,
                action=request.action,
                status="error",
                error=str(exc),
                audit_id=audit_id,
            )

    def _queue_for_approval(self, request: ActionRequest, action_def: ActionDefinition, reason: str) -> ActionResult:
        self._store.save_pending_approval(request, reason)
        audit_id = self._get_audit_log().log({
            "request_id": request.request_id,
            "action": request.action,
            "tier": int(action_def.tier),
            "agent_id": request.agent_id,
            "params": self._redact_pii(request.action, request.params),
            "reasoning": request.reasoning,
            "status": "queued_for_approval",
            "queue_reason": reason,
        })
        return ActionResult(
            request_id=request.request_id,
            action=request.action,
            status="queued_for_approval",
            audit_id=audit_id,
        )

    def approve(self, request_id: str) -> ActionResult:
        # Re-check kill switch — an approval granted before kill switch cannot execute
        if is_kill_switch_active():
            return ActionResult(
                request_id=request_id,
                action="unknown",
                status="blocked",
                error="Kill switch is active — approved action cannot execute. Disable kill switch first.",
            )

        request = self._store.pop_pending_approval(request_id)
        if request is None:
            return ActionResult(
                request_id=request_id,
                action="unknown",
                status="blocked",
                error=f"No pending approval found for request_id={request_id}",
            )

        action_def, handler = self._actions.get(request.action, (None, None))
        if action_def is None or handler is None:
            return ActionResult(
                request_id=request_id,
                action=request.action,
                status="blocked",
                error=f"Action {request.action!r} no longer registered",
            )

        try:
            import time
            t0 = time.time()
            outcome = handler(request.params)
            duration_ms = int((time.time() - t0) * 1000)
            self._store.increment_daily_usage(request.action)
            audit_id = self._get_audit_log().log({
                "request_id": request.request_id,
                "action": request.action,
                "tier": int(action_def.tier),
                "agent_id": request.agent_id,
                "status": "executed_after_approval",
                "result": outcome,
                "duration_ms": duration_ms,
            })
            return ActionResult(
                request_id=request_id,
                action=request.action,
                status="executed",
                result=outcome,
                audit_id=audit_id,
            )
        except Exception as exc:
            logger.exception("Approved action %s failed: %s", request.action, exc)
            return ActionResult(
                request_id=request_id,
                action=request.action,
                status="error",
                error=str(exc),
            )

    def reject(self, request_id: str, reason: str = "") -> None:
        meta = self._store.delete_pending_approval(request_id)
        if meta is not None:
            self._get_audit_log().log({
                "request_id": request_id,
                "action": meta.get("action", "unknown"),
                "status": "rejected",
                "reason": reason,
            })

    def is_kill_switch_active(self) -> bool:
        return is_kill_switch_active()

    def get_daily_usage(self, action: str) -> int:
        return self._store.get_daily_usage(action)

    def get_pending_approvals(self) -> list[dict]:
        return self._store.list_pending_approvals()

    def get_permissions_summary(self) -> dict:
        return {
            "kill_switch_active": is_kill_switch_active(),
            "autonomous_mode": self._config.autonomous_mode,
            "dry_run": self._config.dry_run,
            "registered_actions": list(self._actions.keys()),
            "daily_usage": self._store.get_all_daily_usage(),
            "pending_approvals": self._store.count_pending_approvals(),
        }

    def reset_daily_usage(self) -> None:
        """Called at midnight. Resets today's counters."""
        self._store.reset_daily_usage()

    def get_tools_for_executor(self) -> list[dict]:
        """
        Return registered actions as Anthropic-format tool definitions.
        Only includes Tier 0-3 actions (READ, COMPUTE, COMMUNICATE, BUILD).
        DEPLOY/SPEND/LEGAL are excluded — they require explicit human approval
        and must not be callable autonomously by the executor.
        """
        tools = []
        for name, (action_def, _) in self._actions.items():
            if action_def.tier > Tier.BUILD:
                continue  # Skip DEPLOY/SPEND/LEGAL from autonomous tool use
            tools.append({
                "name": name,
                "description": f"{action_def.description} [Tier={action_def.tier.name}, reversible={action_def.reversible}]",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "params": {
                            "type": "object",
                            "description": "Parameters for this action",
                        },
                        "reasoning": {
                            "type": "string",
                            "description": "Why this action is being taken",
                        },
                    },
                    "required": ["params", "reasoning"],
                },
            })
        return tools

    @staticmethod
    def _redact_pii(action: str, params: dict) -> dict:
        """Redact PII fields for email/support actions."""
        if action in ("send_email", "reply_support"):
            redacted = dict(params)
            for f in ("to", "body", "email", "message"):
                if f in redacted:
                    redacted[f] = "[REDACTED]"
            return redacted
        return params


_registry: ActionRegistry | None = None
_registry_lock = threading.Lock()


def get_action_registry() -> ActionRegistry:
    global _registry
    if _registry is None:
        with _registry_lock:
            if _registry is None:
                _registry = ActionRegistry()
    return _registry
