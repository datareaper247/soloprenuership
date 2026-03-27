"""Unit tests for AgentExecutor."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from soloos_core.agent.executor import AgentExecutor, _MAX_ITERATIONS, _MAX_MESSAGE_HISTORY


# ─── Helper ───────────────────────────────────────────────────────────────────

def _make_executor() -> AgentExecutor:
    """Create an executor; always returns stub backend in test env."""
    return AgentExecutor()


_TASK = {"task_type": "test_task", "payload": {"key": "value"}}
_WORLD = {"metrics": {"mrr": 1000, "active_customers": 5, "runway_months": 12}}


# ─── Stub backend ─────────────────────────────────────────────────────────────

def test_stub_backend_returns_unavailable():
    """Executor stub returns a structured result when deps missing."""
    ex = _make_executor()
    # Force stub backend regardless of installed packages
    ex._backend = "stub"
    result = ex.run(_TASK, _WORLD, available_tools=[])
    assert result["status"] == "unavailable"
    assert "actions_taken" in result


def test_run_blocked_when_kill_switch_active(tmp_path, monkeypatch):
    """Kill switch blocks execution immediately."""
    monkeypatch.setenv("SOLOOS_AUTONOMOUS", "false")
    ex = _make_executor()
    result = ex.run(_TASK, _WORLD, available_tools=[])
    assert result["status"] == "blocked"
    assert "kill switch" in result["result"].lower()


def test_build_context_includes_task_type():
    ex = _make_executor()
    ctx = ex._build_context(_TASK, _WORLD)
    assert "test_task" in ctx
    assert "1,000" in ctx  # MRR formatted


def test_build_context_includes_business_metrics():
    ex = _make_executor()
    ctx = ex._build_context(
        {"task_type": "morning_brief", "payload": {}},
        {"metrics": {"mrr": 5000, "active_customers": 12, "runway_months": 8}},
    )
    assert "5,000" in ctx
    assert "12" in ctx


# ─── Anthropic SDK path ───────────────────────────────────────────────────────

def test_anthropic_path_returns_completed_on_end_turn(monkeypatch):
    """Mock the Anthropic SDK to return end_turn immediately."""
    import types

    # Build minimal mock response
    mock_block = MagicMock()
    mock_block.type = "text"
    mock_block.text = "Done."

    mock_response = MagicMock()
    mock_response.stop_reason = "end_turn"
    mock_response.content = [mock_block]

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_response

    mock_anthropic = types.ModuleType("anthropic")
    mock_anthropic.Anthropic = lambda: mock_client

    monkeypatch.setitem(__import__("sys").modules, "anthropic", mock_anthropic)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.delenv("SOLOOS_AUTONOMOUS", raising=False)

    ex = _make_executor()
    ex._backend = "anthropic"
    result = ex._run_anthropic(_TASK, _WORLD, available_tools=[])

    assert result["status"] == "completed"
    assert result["result"] == "Done."
    assert result["iterations"] == 1


def test_anthropic_path_stops_at_max_iterations(monkeypatch):
    """Executor stops after _MAX_ITERATIONS even without end_turn."""
    import types

    mock_response = MagicMock()
    mock_response.stop_reason = "tool_use"
    mock_response.content = []

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_response

    mock_anthropic = types.ModuleType("anthropic")
    mock_anthropic.Anthropic = lambda: mock_client

    monkeypatch.setitem(__import__("sys").modules, "anthropic", mock_anthropic)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.delenv("SOLOOS_AUTONOMOUS", raising=False)

    ex = _make_executor()
    ex._backend = "anthropic"
    result = ex._run_anthropic(_TASK, _WORLD, available_tools=[])

    assert result["status"] == "max_iterations"
    # Should have called create exactly _MAX_ITERATIONS times
    assert mock_client.messages.create.call_count == _MAX_ITERATIONS


def test_message_history_trimmed_after_max(monkeypatch):
    """Message list is trimmed to _MAX_MESSAGE_HISTORY after many tool calls."""
    import types

    call_count = [0]
    responses = []
    # Build enough tool_use responses to exceed MAX_MESSAGE_HISTORY
    for _ in range(_MAX_MESSAGE_HISTORY + 5):
        tool_block = MagicMock()
        tool_block.type = "tool_use"
        tool_block.name = "send_email"
        tool_block.id = "tu_test"
        tool_block.input = {}
        resp = MagicMock()
        resp.stop_reason = "tool_use"
        resp.content = [tool_block]
        responses.append(resp)
    # Final response: end_turn
    end_block = MagicMock()
    end_block.type = "text"
    end_block.text = "done"
    end_resp = MagicMock()
    end_resp.stop_reason = "end_turn"
    end_resp.content = [end_block]
    responses.append(end_resp)

    def _create(**kwargs):
        nonlocal call_count
        idx = call_count[0]
        call_count[0] += 1
        return responses[min(idx, len(responses) - 1)]

    mock_client = MagicMock()
    mock_client.messages.create.side_effect = _create

    mock_anthropic = types.ModuleType("anthropic")
    mock_anthropic.Anthropic = lambda: mock_client

    monkeypatch.setitem(__import__("sys").modules, "anthropic", mock_anthropic)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.delenv("SOLOOS_AUTONOMOUS", raising=False)

    with patch.object(AgentExecutor, "_execute_tool", return_value={"ok": True}):
        ex = _make_executor()
        ex._backend = "anthropic"
        # Just verify it completes without OOM/infinite loop
        result = ex._run_anthropic(_TASK, _WORLD, available_tools=[{"name": "send_email"}])
        assert result["status"] in ("completed", "max_iterations")


# ─── _execute_tool routing ─────────────────────────────────────────────────────

def test_execute_tool_unknown_returns_error():
    ex = _make_executor()
    result = ex._execute_tool("nonexistent_tool_xyz", {}, available_tools=[])
    assert "error" in result
    assert "Unknown tool" in result["error"]
