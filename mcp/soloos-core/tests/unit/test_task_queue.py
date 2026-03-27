"""Tests for TaskQueue and WorldModel (Next-2a)."""

import tempfile
from pathlib import Path

import pytest

from soloos_core.agent.task_queue import TaskQueue
from soloos_core.agent.world_model import WorldModel


def _tmp_queue() -> TaskQueue:
    p = Path(tempfile.mktemp(suffix=".db"))
    return TaskQueue(db_path=p)


def _tmp_world() -> WorldModel:
    p = Path(tempfile.mktemp(suffix=".db"))
    return WorldModel(db_path=p)


# ─── TaskQueue CRUD ───────────────────────────────────────────────────────────

def test_enqueue_returns_id():
    q = _tmp_queue()
    task_id = q.enqueue("morning_brief", {"hello": "world"})
    assert task_id


def test_dequeue_returns_highest_priority():
    q = _tmp_queue()
    q.enqueue("low_prio", {}, priority=8)
    q.enqueue("high_prio", {}, priority=1)
    q.enqueue("mid_prio", {}, priority=5)

    task = q.dequeue()
    assert task is not None
    assert task["task_type"] == "high_prio"


def test_dequeue_returns_none_when_empty():
    q = _tmp_queue()
    assert q.dequeue() is None


def test_dequeue_marks_as_running():
    q = _tmp_queue()
    q.enqueue("test_task", {})
    task = q.dequeue()
    assert task["status"] == "running"


def test_complete_marks_done():
    q = _tmp_queue()
    task_id = q.enqueue("test", {})
    q.dequeue()
    q.complete(task_id, {"result": "ok"})
    recent = q.list_recent()
    done = [t for t in recent if t["id"] == task_id]
    assert done[0]["status"] == "done"


def test_fail_retries_then_fails():
    q = _tmp_queue()
    task_id = q.enqueue("test", {})
    # max_retries defaults to 3
    for _ in range(3):
        q.dequeue()  # set to running
        q.fail(task_id, "error")

    # After 3 retries, should be 'failed'
    recent = q.list_recent()
    failed = [t for t in recent if t["id"] == task_id]
    assert failed[0]["status"] == "failed"


def test_cancel_marks_cancelled():
    q = _tmp_queue()
    task_id = q.enqueue("test", {})
    q.cancel(task_id)
    recent = q.list_recent()
    t = [x for x in recent if x["id"] == task_id][0]
    assert t["status"] == "cancelled"


def test_list_pending_returns_only_pending():
    q = _tmp_queue()
    id1 = q.enqueue("a", {})
    id2 = q.enqueue("b", {})
    q.dequeue()  # removes one from pending

    pending = q.list_pending()
    assert len(pending) == 1


def test_dequeue_filters_by_agent_id():
    q = _tmp_queue()
    q.enqueue("for_founder", {}, agent_id="founder")
    q.enqueue("for_marketing", {}, agent_id="marketing")

    task = q.dequeue(agent_id="marketing")
    assert task is not None
    assert task["task_type"] == "for_marketing"


def test_stats_returns_counts_by_status():
    q = _tmp_queue()
    q.enqueue("a", {})
    q.enqueue("b", {})
    stats = q.stats()
    assert stats.get("pending", 0) == 2


def test_payload_deserialized_correctly():
    q = _tmp_queue()
    payload = {"key": "value", "number": 42, "list": [1, 2, 3]}
    task_id = q.enqueue("test", payload)
    task = q.dequeue()
    assert isinstance(task["payload"], dict)
    assert task["payload"] == payload


# ─── WorldModel ───────────────────────────────────────────────────────────────

def test_world_model_refresh_returns_dict():
    wm = _tmp_world()
    result = wm.refresh()
    assert isinstance(result, dict)
    assert "metrics" in result
    assert "goals" in result
    assert "refreshed_at" in result


def test_world_model_get_uses_cache():
    wm = _tmp_world()
    wm.refresh()
    r1 = wm.get()
    r2 = wm.get()
    assert r1["refreshed_at"] == r2["refreshed_at"]


def test_world_model_get_section():
    wm = _tmp_world()
    wm.refresh()
    metrics = wm.get_section("metrics")
    assert isinstance(metrics, dict)
    assert "mrr" in metrics


def test_world_model_update_goals():
    wm = _tmp_world()
    wm.refresh()
    wm.update_goals({"mrr_target": 10000, "next_milestone": "10 customers"})
    goals = wm.get_section("goals")
    assert goals["mrr_target"] == 10000
    assert goals["next_milestone"] == "10 customers"


def test_world_model_update_agent_state():
    wm = _tmp_world()
    wm.refresh()
    wm.update_agent_state({"notes": ["test note"]})
    state = wm.get_section("agent_state")
    assert state["notes"] == ["test note"]
    assert state["last_run"] is not None


def test_world_model_get_context_for_agent():
    wm = _tmp_world()
    wm.refresh()
    ctx = wm.get_context_for_agent("FounderAgent")
    assert "FounderAgent" in ctx
    assert "MRR" in ctx
