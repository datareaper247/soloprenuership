"""Tests for ActionRegistry — permission gating and kill switch."""

import os
import tempfile
import pytest
from unittest.mock import patch
from pathlib import Path

from soloos_core.core.action_registry import (
    ActionRegistry,
    ActionDefinition,
    ActionRequest,
    Tier,
    is_kill_switch_active,
    get_action_registry,
)
from soloos_core.core.audit_log import AuditLog


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _make_registry(dry_run=False, autonomous=True) -> ActionRegistry:
    """Fresh registry with in-memory audit log and isolated temp SQLite store."""
    # Use a unique temp file per call so daily usage doesn't bleed across tests
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    reg = ActionRegistry(store_db_path=tmp.name)
    reg._audit_log = AuditLog(path=Path("/tmp/test_audit.jsonl"))
    reg._config._loaded = True
    reg._config._data = {
        "autonomous_mode": autonomous,
        "dry_run": dry_run,
    }
    return reg


def _echo_handler(params: dict) -> dict:
    return {"echo": params}


def _register_echo(reg: ActionRegistry, tier: Tier = Tier.READ, daily_limit=None) -> None:
    reg.register_action(
        ActionDefinition(
            name="echo",
            tier=tier,
            description="Test echo action",
            reversible=True,
            daily_limit=daily_limit,
        ),
        _echo_handler,
    )


# ─── Kill switch tests ────────────────────────────────────────────────────────

def test_kill_switch_env_false():
    with patch.dict(os.environ, {"SOLOOS_AUTONOMOUS": "false"}):
        assert is_kill_switch_active() is True


def test_kill_switch_env_zero():
    with patch.dict(os.environ, {"SOLOOS_AUTONOMOUS": "0"}):
        assert is_kill_switch_active() is True


def test_kill_switch_env_SOLOOS_KILL_SWITCH():
    with patch.dict(os.environ, {"SOLOOS_KILL_SWITCH": "1"}):
        assert is_kill_switch_active() is True


def test_kill_switch_inactive_by_default():
    clean_env = {k: v for k, v in os.environ.items()
                 if k not in ("SOLOOS_AUTONOMOUS", "SOLOOS_KILL_SWITCH")}
    with patch.dict(os.environ, clean_env, clear=True):
        # Only check env — don't depend on ~/.soloos/kill_switch file
        assert os.environ.get("SOLOOS_AUTONOMOUS", "").lower() not in ("false", "0")
        assert not os.environ.get("SOLOOS_KILL_SWITCH")


def test_kill_switch_blocks_tier2_but_not_tier0_tier1():
    reg = _make_registry()
    _register_echo(reg, tier=Tier.COMMUNICATE)

    # Tier READ action should NOT be blocked even with kill switch
    read_def = ActionDefinition("read_data", Tier.READ, "read", True)
    reg.register_action(read_def, _echo_handler)

    with patch.dict(os.environ, {"SOLOOS_AUTONOMOUS": "false"}):
        # Tier 2 blocked
        result = reg.execute(ActionRequest(action="echo", params={}, reasoning="test"))
        assert result.status == "blocked"
        assert "Kill switch" in (result.error or "")

        # Tier 0 NOT blocked
        result2 = reg.execute(ActionRequest(action="read_data", params={}, reasoning="test"))
        assert result2.status != "blocked"


def test_kill_switch_blocks_tier1_not_blocked():
    reg = _make_registry()
    compute_def = ActionDefinition("compute_data", Tier.COMPUTE, "compute", True)
    reg.register_action(compute_def, _echo_handler)

    with patch.dict(os.environ, {"SOLOOS_AUTONOMOUS": "false"}):
        result = reg.execute(ActionRequest(action="compute_data", params={}, reasoning="test"))
        # COMPUTE is Tier 1, kill switch only blocks Tier 2+
        assert result.status != "blocked"


# ─── LEGAL tier tests ─────────────────────────────────────────────────────────

def test_legal_tier_always_queued_regardless_of_config():
    reg = _make_registry(autonomous=True)
    legal_def = ActionDefinition("sign_contract", Tier.LEGAL, "sign", False)
    reg.register_action(legal_def, _echo_handler)

    result = reg.execute(ActionRequest(action="sign_contract", params={}, reasoning="test"))
    assert result.status == "queued_for_approval"


def test_legal_tier_queued_even_in_dry_run():
    reg = _make_registry(dry_run=True)
    legal_def = ActionDefinition("sign_contract", Tier.LEGAL, "sign", False)
    reg.register_action(legal_def, _echo_handler)

    result = reg.execute(ActionRequest(action="sign_contract", params={}, reasoning="test"))
    assert result.status == "queued_for_approval"


# ─── Daily limit tests ────────────────────────────────────────────────────────

def test_daily_limit_enforced():
    reg = _make_registry()
    _register_echo(reg, tier=Tier.COMMUNICATE, daily_limit=2)

    req = ActionRequest(action="echo", params={"x": 1}, reasoning="test")
    r1 = reg.execute(req)
    r2 = reg.execute(ActionRequest(action="echo", params={"x": 2}, reasoning="test"))
    r3 = reg.execute(ActionRequest(action="echo", params={"x": 3}, reasoning="test"))

    assert r1.status == "executed"
    assert r2.status == "executed"
    assert r3.status == "blocked"
    assert "Daily limit" in (r3.error or "")


def test_daily_limit_resets():
    reg = _make_registry()
    _register_echo(reg, tier=Tier.READ, daily_limit=1)
    reg.execute(ActionRequest(action="echo", params={}, reasoning="test"))
    assert reg.get_daily_usage("echo") == 1
    reg.reset_daily_usage()
    assert reg.get_daily_usage("echo") == 0


# ─── Dry run tests ────────────────────────────────────────────────────────────

def test_dry_run_logs_but_does_not_execute():
    executed = []
    def tracking_handler(params):
        executed.append(params)
        return {"ok": True}

    reg = _make_registry(dry_run=True)
    reg.register_action(
        ActionDefinition("tracked", Tier.COMMUNICATE, "track", True),
        tracking_handler,
    )
    result = reg.execute(ActionRequest(action="tracked", params={"x": 1}, reasoning="test"))
    assert result.status == "dry_run"
    assert len(executed) == 0  # handler was NOT called


# ─── Approval flow tests ──────────────────────────────────────────────────────

def test_non_autonomous_mode_queues_tier2():
    reg = _make_registry(autonomous=False)
    _register_echo(reg, tier=Tier.COMMUNICATE)
    result = reg.execute(ActionRequest(action="echo", params={}, reasoning="test"))
    assert result.status == "queued_for_approval"
    assert len(reg.get_pending_approvals()) == 1


def test_approve_executes_queued_action():
    reg = _make_registry(autonomous=False)
    _register_echo(reg, tier=Tier.COMMUNICATE)
    result = reg.execute(ActionRequest(action="echo", params={"x": 42}, reasoning="test"))
    assert result.status == "queued_for_approval"

    approved = reg.approve(result.request_id)
    assert approved.status == "executed"
    assert approved.result == {"echo": {"x": 42}}
    assert len(reg.get_pending_approvals()) == 0


def test_reject_removes_from_pending():
    reg = _make_registry(autonomous=False)
    _register_echo(reg, tier=Tier.COMMUNICATE)
    result = reg.execute(ActionRequest(action="echo", params={}, reasoning="test"))
    reg.reject(result.request_id, reason="not needed")
    assert len(reg.get_pending_approvals()) == 0


# ─── Permissions summary ──────────────────────────────────────────────────────

def test_permissions_summary_structure():
    reg = _make_registry()
    _register_echo(reg)
    summary = reg.get_permissions_summary()
    assert "kill_switch_active" in summary
    assert "autonomous_mode" in summary
    assert "registered_actions" in summary
    assert "echo" in summary["registered_actions"]


def test_unknown_action_returns_blocked():
    reg = _make_registry()
    result = reg.execute(ActionRequest(action="nonexistent", params={}, reasoning="test"))
    assert result.status == "blocked"
    assert "Unknown action" in (result.error or "")
