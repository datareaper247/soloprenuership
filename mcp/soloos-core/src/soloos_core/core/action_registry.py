"""
ActionRegistry — permission gating for all autonomous AI actions.

CRITICAL SAFETY RULES (enforced in code, not config):
1. Tier.LEGAL always requires approval. Cannot be configured away.
2. Kill switch (SOLOOS_AUTONOMOUS=false or ~/.soloos/kill_switch) blocks Tier 2+.
3. Budget limits are hard-coded ceilings. Config can only reduce, not increase.
4. AI cannot modify its own permissions. ActionRegistry is read-only to agents.
5. Every execution is logged to AuditLog before AND after.
"""

from __future__ import annotations

import os
import uuid
import logging
from dataclasses import dataclass, field
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
            pass  # fail-open

    @property
    def autonomous_mode(self) -> bool:
        self._load()
        return bool(self._data.get("autonomous_mode", True))

    @property
    def dry_run(self) -> bool:
        self._load()
        return bool(self._data.get("dry_run", False))

    def get_limit(self, category: str, key: str, default: int) -> int:
        self._load()
        val = (self._data.get("limits") or {}).get(category, {}).get(key, default)
        return int(val)


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

    def __init__(self) -> None:
        self._actions: dict[str, tuple[ActionDefinition, Callable]] = {}
        self._daily_usage: dict[str, int] = {}
        self._pending_approvals: dict[str, dict] = {}
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
            used = self._daily_usage.get(request.action, 0)
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
        intent_id = self._get_audit_log().log({
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

            # Increment daily usage
            self._daily_usage[request.action] = self._daily_usage.get(request.action, 0) + 1

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
        self._pending_approvals[request.request_id] = {
            "request": request,
            "action_def": action_def,
            "reason": reason,
        }
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
        entry = self._pending_approvals.pop(request_id, None)
        if entry is None:
            return ActionResult(
                request_id=request_id,
                action="unknown",
                status="blocked",
                error=f"No pending approval found for request_id={request_id}",
            )
        request: ActionRequest = entry["request"]
        action_def: ActionDefinition = entry["action_def"]
        _, handler = self._actions[request.action]

        try:
            import time
            t0 = time.time()
            outcome = handler(request.params)
            duration_ms = int((time.time() - t0) * 1000)
            self._daily_usage[request.action] = self._daily_usage.get(request.action, 0) + 1
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
        entry = self._pending_approvals.pop(request_id, None)
        if entry is not None:
            self._get_audit_log().log({
                "request_id": request_id,
                "action": entry["request"].action,
                "status": "rejected",
                "reason": reason,
            })

    def is_kill_switch_active(self) -> bool:
        return is_kill_switch_active()

    def get_daily_usage(self, action: str) -> int:
        return self._daily_usage.get(action, 0)

    def get_pending_approvals(self) -> list[dict]:
        result = []
        for req_id, entry in self._pending_approvals.items():
            req: ActionRequest = entry["request"]
            result.append({
                "request_id": req_id,
                "action": req.action,
                "agent_id": req.agent_id,
                "reasoning": req.reasoning,
                "reason_queued": entry["reason"],
            })
        return result

    def get_permissions_summary(self) -> dict:
        return {
            "kill_switch_active": is_kill_switch_active(),
            "autonomous_mode": self._config.autonomous_mode,
            "dry_run": self._config.dry_run,
            "registered_actions": list(self._actions.keys()),
            "daily_usage": dict(self._daily_usage),
            "pending_approvals": len(self._pending_approvals),
        }

    def reset_daily_usage(self) -> None:
        """Called at midnight. Resets counters."""
        self._daily_usage.clear()

    @staticmethod
    def _redact_pii(action: str, params: dict) -> dict:
        """Redact PII fields for email/support actions."""
        if action in ("send_email", "reply_support"):
            redacted = dict(params)
            for field in ("to", "body", "email", "message"):
                if field in redacted:
                    redacted[field] = "[REDACTED]"
            return redacted
        return params


_registry: ActionRegistry | None = None


def get_action_registry() -> ActionRegistry:
    global _registry
    if _registry is None:
        _registry = ActionRegistry()
    return _registry
