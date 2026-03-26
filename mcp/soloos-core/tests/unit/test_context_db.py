"""
Unit tests for data/context_db.py — SQLite operational store.

All tests use a temporary directory so they never touch ~/.soloos/context.db.
Tests verify: schema init, CRUD operations, migration idempotency, kill signal
queries, feedback logging, session logging, and fail-open behaviour.
"""

import pytest
import tempfile
from pathlib import Path


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _make_db(tmp_path: Path):
    """Return a ContextDB backed by a temporary directory."""
    from soloos_core.data.context_db import ContextDB
    return ContextDB(db_path=tmp_path / "test_context.db")


# ─────────────────────────────────────────────────────────────
# 1. Schema initialisation
# ─────────────────────────────────────────────────────────────

def test_db_init_creates_file(tmp_path):
    """ContextDB creates the SQLite file on first use."""
    db_path = tmp_path / "test_context.db"
    from soloos_core.data.context_db import ContextDB
    db = ContextDB(db_path=db_path)
    assert db.is_available(), "DB should be available after init"
    assert db_path.exists(), "SQLite file should exist on disk"


def test_schema_init_is_idempotent(tmp_path):
    """Creating ContextDB twice against the same file does not raise."""
    from soloos_core.data.context_db import ContextDB
    db_path = tmp_path / "idempotent.db"
    db1 = ContextDB(db_path=db_path)
    db2 = ContextDB(db_path=db_path)
    assert db1.is_available()
    assert db2.is_available()
    # Stats should work on both handles
    assert isinstance(db1.get_stats(), dict)
    assert isinstance(db2.get_stats(), dict)


# ─────────────────────────────────────────────────────────────
# 2. Decisions CRUD
# ─────────────────────────────────────────────────────────────

def test_upsert_and_get_decision(tmp_path):
    """upsert_decision stores a row retrievable by get_decision."""
    db = _make_db(tmp_path)
    ok = db.upsert_decision(
        id="FL-001",
        date="2026-03-26",
        situation="Need to pick a pricing model",
        decision="Go with flat $49/mo",
        kill_signal="If fewer than 3 signups at this price in 14 days",
        kill_signal_date="2026-04-09",
        outcome=None,
        outcome_date="2026-04-26",
        tags="Decision",
    )
    assert ok, "upsert_decision should return True on success"

    row = db.get_decision("FL-001")
    assert row is not None, "get_decision should return the stored row"
    assert row["id"] == "FL-001"
    assert row["decision"] == "Go with flat $49/mo"
    assert row["kill_signal_date"] == "2026-04-09"


def test_upsert_decision_is_idempotent(tmp_path):
    """Upserting the same id twice keeps the latest data (INSERT OR REPLACE)."""
    db = _make_db(tmp_path)
    db.upsert_decision(id="FL-002", date="2026-03-26",
                       situation="v1", decision="v1 decision")
    db.upsert_decision(id="FL-002", date="2026-03-27",
                       situation="v2", decision="v2 decision")

    row = db.get_decision("FL-002")
    assert row["decision"] == "v2 decision", "Second upsert should overwrite"

    # Only one row should exist
    all_rows = db.list_decisions()
    assert sum(1 for r in all_rows if r["id"] == "FL-002") == 1


def test_update_decision_outcome(tmp_path):
    """update_decision_outcome fills the outcome field."""
    db = _make_db(tmp_path)
    db.upsert_decision(id="FL-003", date="2026-03-26",
                       situation="Test", decision="Launch")
    updated = db.update_decision_outcome(
        id="FL-003", outcome="3 customers signed up", outcome_date="2026-04-01"
    )
    assert updated, "update_decision_outcome should return True"
    row = db.get_decision("FL-003")
    assert row["outcome"] == "3 customers signed up"
    assert row["outcome_date"] == "2026-04-01"


def test_list_decisions_returns_all(tmp_path):
    """list_decisions returns all inserted rows."""
    db = _make_db(tmp_path)
    for i in range(5):
        db.upsert_decision(id=f"FL-{i:03d}", date="2026-03-26",
                           situation=f"s{i}", decision=f"d{i}")
    rows = db.list_decisions()
    assert len(rows) == 5


# ─────────────────────────────────────────────────────────────
# 3. Kill signal query
# ─────────────────────────────────────────────────────────────

def test_get_pending_kill_signals(tmp_path):
    """get_pending_kill_signals returns only rows with kill_signal and no outcome."""
    db = _make_db(tmp_path)
    # Has kill signal, no outcome → should appear
    db.upsert_decision(id="FL-010", date="2026-03-26",
                       situation="s", decision="d",
                       kill_signal="If no signups", kill_signal_date="2026-04-10",
                       outcome=None)
    # Has kill signal AND outcome → should NOT appear
    db.upsert_decision(id="FL-011", date="2026-03-26",
                       situation="s", decision="d",
                       kill_signal="If no signups", kill_signal_date="2026-04-10",
                       outcome="Got 5 signups")
    # No kill signal → should NOT appear
    db.upsert_decision(id="FL-012", date="2026-03-26",
                       situation="s", decision="d")

    pending = db.get_pending_kill_signals()
    ids = {r["id"] for r in pending}
    assert "FL-010" in ids
    assert "FL-011" not in ids
    assert "FL-012" not in ids


# ─────────────────────────────────────────────────────────────
# 4. Experiments CRUD
# ─────────────────────────────────────────────────────────────

def test_upsert_and_get_experiment(tmp_path):
    """upsert_experiment stores and get_experiment retrieves correctly."""
    db = _make_db(tmp_path)
    ok = db.upsert_experiment(
        id="EXP-001",
        hypothesis="Landing page CTA change will increase signups by 20%",
        status="running",
        started_at="2026-03-20",
    )
    assert ok
    exp = db.get_experiment("EXP-001")
    assert exp is not None
    assert exp["hypothesis"].startswith("Landing page")
    assert exp["status"] == "running"


def test_list_experiments_filters_by_status(tmp_path):
    """list_experiments(status=...) returns only matching rows."""
    db = _make_db(tmp_path)
    db.upsert_experiment(id="EXP-A", hypothesis="H1", status="running")
    db.upsert_experiment(id="EXP-B", hypothesis="H2", status="completed")
    db.upsert_experiment(id="EXP-C", hypothesis="H3", status="running")

    running = db.list_experiments(status="running")
    assert len(running) == 2
    assert all(r["status"] == "running" for r in running)

    completed = db.list_experiments(status="completed")
    assert len(completed) == 1


# ─────────────────────────────────────────────────────────────
# 5. Sessions
# ─────────────────────────────────────────────────────────────

def test_log_session_returns_id(tmp_path):
    """log_session returns a non-None string id."""
    db = _make_db(tmp_path)
    sid = db.log_session(started_at="2026-03-26T09:00:00",
                         context_snapshot={"mrr": "$5K"},
                         tools_used=["check_kill_signals_tool"])
    assert sid is not None
    assert isinstance(sid, str)
    assert len(sid) > 0


# ─────────────────────────────────────────────────────────────
# 6. Feedback
# ─────────────────────────────────────────────────────────────

def test_log_feedback_and_list(tmp_path):
    """log_feedback stores a row, list_feedback returns it."""
    db = _make_db(tmp_path)
    ok = db.log_feedback(
        call_id="call-abc123",
        tool_name="council_brief",
        rating=5,
        reason="Saved me from a bad hire",
    )
    assert ok
    rows = db.list_feedback()
    assert len(rows) >= 1
    assert any(r["call_id"] == "call-abc123" for r in rows)


# ─────────────────────────────────────────────────────────────
# 7. Stats
# ─────────────────────────────────────────────────────────────

def test_get_stats_returns_counts(tmp_path):
    """get_stats returns a dict with per-table row counts."""
    db = _make_db(tmp_path)
    db.upsert_decision(id="FL-099", date="2026-03-26",
                       situation="s", decision="d")
    db.upsert_experiment(id="EXP-Z", hypothesis="H")

    stats = db.get_stats()
    assert stats["available"] is True
    assert stats["decisions"] >= 1
    assert stats["experiments"] >= 1
    assert "db_path" in stats


# ─────────────────────────────────────────────────────────────
# 8. Migration idempotency (sync_state flag)
# ─────────────────────────────────────────────────────────────

def test_migration_flag_is_idempotent(tmp_path):
    """set_sync_state / get_sync_state work correctly and are idempotent."""
    db = _make_db(tmp_path)

    # Initially None
    val = db.get_sync_state("migration_done")
    # May already be "1" if migration ran from existing markdown (OK either way)
    assert val in (None, "1")

    # Explicitly set
    db.set_sync_state("migration_done", "1")
    assert db.get_sync_state("migration_done") == "1"

    # Set again — should not raise
    db.set_sync_state("migration_done", "1")
    assert db.get_sync_state("migration_done") == "1"


# ─────────────────────────────────────────────────────────────
# 9. Fail-open — unavailable DB never raises
# ─────────────────────────────────────────────────────────────

def test_unavailable_db_never_raises():
    """_UnavailableContextDB returns safe defaults on all public calls."""
    from soloos_core.data.context_db import _UnavailableContextDB
    db = _UnavailableContextDB()
    assert not db.is_available()
    # All these should return safe defaults, never raise
    assert db.get_decision("FL-001") is None
    assert db.list_decisions() == []
    assert db.upsert_decision("FL-001", "2026-01-01", "s", "d") is False
    assert db.list_experiments() == []
    assert db.get_pending_kill_signals() == []
    assert db.log_feedback("call-x") is False
    assert db.list_feedback() == []
    stats = db.get_stats()
    assert stats["available"] is False


# ─────────────────────────────────────────────────────────────
# 10. Singleton accessor
# ─────────────────────────────────────────────────────────────

def test_get_context_db_returns_instance():
    """get_context_db() returns a ContextDB instance without raising."""
    from soloos_core.data.context_db import get_context_db
    db = get_context_db()
    assert db is not None
    # Should be callable
    stats = db.get_stats()
    assert isinstance(stats, dict)
