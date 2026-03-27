"""Unit tests for FounderLoop."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from soloos_core.agent.founder_loop import FounderLoop
from soloos_core.agent.task_queue import TaskQueue
from soloos_core.agent.world_model import WorldModel


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _tmp_path() -> Path:
    return Path(tempfile.mktemp(suffix=".db"))


def _make_loop_with_mocks(monkeypatch, kill_switch=False):
    """
    Return a FounderLoop with all heavy dependencies mocked:
    - WorldModel backed by an isolated SQLite file
    - TaskQueue backed by an isolated SQLite file
    - AgentExecutor replaced with a stub
    - AuditLog silently no-op
    - Kill switch state controlled by parameter
    """
    wm = WorldModel(db_path=_tmp_path())
    queue = TaskQueue(db_path=_tmp_path())

    # Stub executor that always succeeds
    mock_executor = MagicMock()
    mock_executor.run.return_value = {
        "result": "stub result",
        "actions_taken": [],
        "reasoning": "stub",
        "status": "completed",
    }

    # Stub audit log — get_stats must return a plain dict (run_evening_review json.dumps it)
    mock_audit = MagicMock()
    mock_audit.log.return_value = "audit-id-123"
    mock_audit.get_stats.return_value = {"total": 0, "by_status": {}}

    loop = FounderLoop()

    monkeypatch.setattr(
        "soloos_core.agent.founder_loop.is_kill_switch_active",
        lambda: kill_switch,
    )
    monkeypatch.setattr(
        "soloos_core.agent.founder_loop.get_world_model",
        lambda: wm,
    )
    monkeypatch.setattr(
        "soloos_core.agent.founder_loop.get_task_queue",
        lambda: queue,
    )
    monkeypatch.setattr(
        "soloos_core.agent.founder_loop.get_executor",
        lambda: mock_executor,
    )
    monkeypatch.setattr(
        "soloos_core.agent.founder_loop.get_audit_log",
        lambda: mock_audit,
    )

    return loop, wm, queue, mock_executor, mock_audit


# ─── Kill switch ──────────────────────────────────────────────────────────────

def test_run_once_blocked_when_kill_switch_active(monkeypatch):
    loop, *_ = _make_loop_with_mocks(monkeypatch, kill_switch=True)
    result = loop.run_once()
    assert result["status"] == "blocked"


def test_morning_session_blocked_when_kill_switch_active(monkeypatch):
    loop, *_ = _make_loop_with_mocks(monkeypatch, kill_switch=True)
    result = loop.run_morning_session()
    assert "blocked" in result.lower()


def test_handle_event_blocked_when_kill_switch_active(monkeypatch):
    loop, *_ = _make_loop_with_mocks(monkeypatch, kill_switch=True)
    result = loop.handle_event("stripe.charge.succeeded", {})
    assert result["status"] == "blocked"


# ─── No tasks ─────────────────────────────────────────────────────────────────

def test_run_once_idle_when_no_tasks(monkeypatch):
    loop, wm, queue, executor, _ = _make_loop_with_mocks(monkeypatch)
    # Queue is empty, world model has no churn signal to generate a task
    result = loop.run_once()
    assert result["status"] == "idle"
    executor.run.assert_not_called()


# ─── Happy path ───────────────────────────────────────────────────────────────

def test_run_once_processes_queued_task(monkeypatch):
    loop, wm, queue, executor, audit = _make_loop_with_mocks(monkeypatch)
    task_id = queue.enqueue("morning_brief", {"source": "test"}, priority=1)

    result = loop.run_once()

    assert result["status"] == "completed"
    assert result["task_type"] == "morning_brief"
    executor.run.assert_called_once()

    # Task should be marked done in queue
    recent = queue.list_recent()
    done = [t for t in recent if t["id"] == task_id]
    assert done[0]["status"] == "done"


def test_run_once_marks_task_failed_on_executor_error(monkeypatch):
    loop, wm, queue, executor, audit = _make_loop_with_mocks(monkeypatch)
    executor.run.side_effect = RuntimeError("boom")
    task_id = queue.enqueue("bad_task", {})

    result = loop.run_once()

    assert result["status"] == "error"
    assert "boom" in result["error"]


# ─── Churn auto-task ─────────────────────────────────────────────────────────

def test_run_once_generates_churn_task_when_high_churn(monkeypatch):
    loop, wm, queue, executor, _ = _make_loop_with_mocks(monkeypatch)

    # Patch refresh() to return high-churn model so the loop generates a task
    high_churn_model = {
        "metrics": {"churn_rate": 0.10, "mrr": 2000, "active_customers": 10},
        "goals": {},
        "experiments": [],
        "decisions": [],
        "market_signals": [],
        "agent_state": {},
        "refreshed_at": "2026-01-01T00:00:00",
        "data_sources_ok": {"sqlite": True, "duckdb": False},
    }
    wm.refresh = lambda: high_churn_model

    result = loop.run_once()

    assert result["status"] == "completed"
    assert result["task_type"] == "analyze_churn"
    executor.run.assert_called_once()
    call_kwargs = executor.run.call_args
    task_arg = call_kwargs[1].get("task") or call_kwargs[0][0]
    assert task_arg["task_type"] == "analyze_churn"


# ─── handle_event routing ─────────────────────────────────────────────────────

def test_handle_event_stripe_charge_enqueues_welcome(monkeypatch):
    loop, wm, queue, executor, _ = _make_loop_with_mocks(monkeypatch)
    result = loop.handle_event("stripe.charge.succeeded", {"customer_id": "cus_123"})
    assert result["status"] == "queued"
    assert result["task_type"] == "welcome_new_customer"
    pending = queue.list_pending()
    assert len(pending) == 1
    assert pending[0]["task_type"] == "welcome_new_customer"


def test_handle_event_github_pr_enqueues_review(monkeypatch):
    loop, wm, queue, executor, _ = _make_loop_with_mocks(monkeypatch)
    result = loop.handle_event("github.pull_request.opened", {"pr_number": 42})
    assert result["task_type"] == "review_pr"


def test_handle_event_unknown_enqueues_generic(monkeypatch):
    loop, wm, queue, executor, _ = _make_loop_with_mocks(monkeypatch)
    result = loop.handle_event("unknown.event.type", {"data": "test"})
    assert result["task_type"] == "handle_generic_event"


def test_handle_event_returns_task_id(monkeypatch):
    loop, wm, queue, executor, _ = _make_loop_with_mocks(monkeypatch)
    result = loop.handle_event("stripe.customer.subscription.deleted", {})
    assert "task_id" in result
    assert result["task_id"]  # non-empty


# ─── morning session ──────────────────────────────────────────────────────────

def test_morning_session_returns_summary_string(monkeypatch):
    loop, wm, queue, executor, _ = _make_loop_with_mocks(monkeypatch)
    result = loop.run_morning_session()
    assert isinstance(result, str)
    assert "Morning Session" in result


# ─── evening review ───────────────────────────────────────────────────────────

def test_evening_review_returns_summary_string(monkeypatch):
    loop, wm, queue, executor, _ = _make_loop_with_mocks(monkeypatch)
    result = loop.run_evening_review()
    assert isinstance(result, str)
    assert "Evening Review" in result
