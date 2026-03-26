"""
Unit tests for data/analytics_db.py — DuckDB analytics store.

All tests are designed to pass whether or not duckdb is installed:
  - Tests that need a real DB use pytest.importorskip("duckdb") and a tmp_path DB.
  - Tests that verify fail-open behaviour mock duckdb away entirely.
  - The singleton isolation tests reset the module-level _db between runs.
"""

import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _reset_module_state():
    """Reset module-level cache so tests don't bleed into each other."""
    import soloos_core.data.analytics_db as mod
    mod._db = None
    mod._duckdb_available = None


def _make_db_in(tmp_path: Path):
    """Return an AnalyticsDB pointed at a fresh tmp file (skips if no duckdb)."""
    pytest.importorskip("duckdb")
    from soloos_core.data.analytics_db import AnalyticsDB
    return AnalyticsDB(db_path=str(tmp_path / "test_analytics.duckdb"))


# ─────────────────────────────────────────────────────────────
# Test 1 — fail-open when duckdb not installed
# ─────────────────────────────────────────────────────────────

def test_analytics_db_fail_open_when_duckdb_missing(caplog):
    """AnalyticsDB is importable and usable even when duckdb is absent."""
    _reset_module_state()

    with patch.dict("sys.modules", {"duckdb": None}):
        # Force re-evaluation of availability
        import soloos_core.data.analytics_db as mod
        mod._duckdb_available = None

        with caplog.at_level(logging.WARNING, logger="soloos_core.data.analytics_db"):
            from soloos_core.data.analytics_db import AnalyticsDB
            db = AnalyticsDB()

        # All methods return empty/zero — never raise
        assert db.get_current_mrr() == 0.0
        assert db.get_mrr_trend() == []
        assert db.get_churn_rate() == 0.0
        assert db.get_sync_state("stripe") == {}
        assert db.insert_events("revenue_events", [{"id": "x"}]) == 0
        assert db.query("SELECT 1") == []
        assert db.has_data() is False

    _reset_module_state()


# ─────────────────────────────────────────────────────────────
# Test 2 — schema is idempotent (init can be called many times)
# ─────────────────────────────────────────────────────────────

def test_schema_init_is_idempotent(tmp_path):
    """Calling AnalyticsDB() twice on the same file does not raise."""
    pytest.importorskip("duckdb")
    from soloos_core.data.analytics_db import AnalyticsDB

    db_path = str(tmp_path / "idem.duckdb")
    db1 = AnalyticsDB(db_path=db_path)
    db2 = AnalyticsDB(db_path=db_path)  # second init on same file

    assert db1._initialized is True
    assert db2._initialized is True
    db1.close()
    db2.close()


# ─────────────────────────────────────────────────────────────
# Test 3 — insert_events + query round-trip
# ─────────────────────────────────────────────────────────────

def test_insert_and_query_revenue_events(tmp_path):
    """Inserted rows are retrievable via query()."""
    db = _make_db_in(tmp_path)

    rows = [
        {
            "id": "ch_001",
            "source": "stripe",
            "event_type": "charge.succeeded",
            "customer_id": "cus_abc",
            "amount_cents": 4900,
            "currency": "usd",
            "mrr_delta_cents": 4900,
            "metadata": '{}',
            "occurred_at": "2024-01-15 10:00:00",
        }
    ]
    n = db.insert_events("revenue_events", rows)
    assert n == 1

    results = db.query("SELECT id, amount_cents FROM revenue_events WHERE id = ?", ["ch_001"])
    assert len(results) == 1
    assert results[0]["id"] == "ch_001"
    assert results[0]["amount_cents"] == 4900
    db.close()


# ─────────────────────────────────────────────────────────────
# Test 4 — insert is idempotent (PRIMARY KEY conflict ignored)
# ─────────────────────────────────────────────────────────────

def test_insert_events_idempotent_on_duplicate(tmp_path):
    """Inserting the same row twice does not raise and count stays at 1."""
    db = _make_db_in(tmp_path)

    row = {
        "id": "ch_dup",
        "source": "stripe",
        "event_type": "charge.succeeded",
        "customer_id": "cus_dup",
        "amount_cents": 1000,
        "currency": "usd",
        "mrr_delta_cents": 1000,
        "metadata": '{}',
        "occurred_at": "2024-02-01 00:00:00",
    }
    db.insert_events("revenue_events", [row])
    db.insert_events("revenue_events", [row])  # same id — must not error

    results = db.query("SELECT COUNT(*) AS n FROM revenue_events WHERE id = ?", ["ch_dup"])
    assert results[0]["n"] == 1
    db.close()


# ─────────────────────────────────────────────────────────────
# Test 5 — get_current_mrr sums mrr_delta_cents correctly
# ─────────────────────────────────────────────────────────────

def test_get_current_mrr_computes_correctly(tmp_path):
    """get_current_mrr returns the sum of all mrr_delta_cents / 100."""
    db = _make_db_in(tmp_path)

    events = [
        {
            "id": f"ev_{i}",
            "source": "stripe",
            "event_type": "charge.succeeded",
            "customer_id": f"cus_{i}",
            "amount_cents": 5000,
            "currency": "usd",
            "mrr_delta_cents": 5000,
            "metadata": '{}',
            "occurred_at": f"2024-0{i+1}-01 00:00:00",
        }
        for i in range(3)  # 3 events × $50 = $150
    ]
    db.insert_events("revenue_events", events)

    mrr = db.get_current_mrr()
    assert mrr == pytest.approx(150.0)
    db.close()


# ─────────────────────────────────────────────────────────────
# Test 6 — get_current_mrr returns 0.0 on empty table
# ─────────────────────────────────────────────────────────────

def test_get_current_mrr_empty_returns_zero(tmp_path):
    """get_current_mrr returns 0.0 when revenue_events table is empty."""
    db = _make_db_in(tmp_path)
    assert db.get_current_mrr() == 0.0
    db.close()


# ─────────────────────────────────────────────────────────────
# Test 7 — sync_state upsert + retrieval
# ─────────────────────────────────────────────────────────────

def test_sync_state_update_and_retrieve(tmp_path):
    """update_sync_state persists a cursor that get_sync_state can read back."""
    db = _make_db_in(tmp_path)

    db.update_sync_state("stripe", "ch_last_cursor_abc")
    state = db.get_sync_state("stripe")

    assert state["source"] == "stripe"
    assert state["last_cursor"] == "ch_last_cursor_abc"
    assert state["status"] == "ok"
    db.close()


# ─────────────────────────────────────────────────────────────
# Test 8 — get_sync_state returns {} for unknown source
# ─────────────────────────────────────────────────────────────

def test_get_sync_state_unknown_source_returns_empty(tmp_path):
    """get_sync_state returns {} when source has never been synced."""
    db = _make_db_in(tmp_path)
    assert db.get_sync_state("unknown_source") == {}
    db.close()


# ─────────────────────────────────────────────────────────────
# Test 9 — has_data reflects table emptiness
# ─────────────────────────────────────────────────────────────

def test_has_data_reflects_table_state(tmp_path):
    """has_data() returns False when empty, True after an insert."""
    db = _make_db_in(tmp_path)
    assert db.has_data() is False

    db.insert_events("revenue_events", [{
        "id": "ev_hd",
        "source": "stripe",
        "event_type": "charge.succeeded",
        "customer_id": "cus_hd",
        "amount_cents": 1000,
        "currency": "usd",
        "mrr_delta_cents": 1000,
        "metadata": '{}',
        "occurred_at": "2024-03-01 00:00:00",
    }])

    assert db.has_data() is True
    db.close()


# ─────────────────────────────────────────────────────────────
# Test 10 — v_mrr view is queryable after data inserted
# ─────────────────────────────────────────────────────────────

def test_v_mrr_view_queryable(tmp_path):
    """v_mrr view returns month-aggregated MRR after data is inserted."""
    db = _make_db_in(tmp_path)

    db.insert_events("revenue_events", [
        {
            "id": "ev_v1",
            "source": "stripe",
            "event_type": "charge.succeeded",
            "customer_id": "cus_v1",
            "amount_cents": 9900,
            "currency": "usd",
            "mrr_delta_cents": 9900,
            "metadata": '{}',
            "occurred_at": "2024-06-15 00:00:00",
        }
    ])

    rows = db.query("SELECT mrr_dollars FROM v_mrr")
    assert len(rows) >= 1
    assert rows[0]["mrr_dollars"] == pytest.approx(99.0)
    db.close()


# ─────────────────────────────────────────────────────────────
# Test 11 — get_analytics_db() returns the same singleton
# ─────────────────────────────────────────────────────────────

def test_get_analytics_db_returns_singleton():
    """get_analytics_db() returns the same object on repeated calls."""
    _reset_module_state()
    from soloos_core.data.analytics_db import get_analytics_db

    db1 = get_analytics_db()
    db2 = get_analytics_db()
    assert db1 is db2
    _reset_module_state()


# ─────────────────────────────────────────────────────────────
# Test 12 — query returns [] on bad SQL without raising
# ─────────────────────────────────────────────────────────────

def test_query_bad_sql_returns_empty_no_raise(tmp_path):
    """query() with invalid SQL returns [] and does not raise."""
    db = _make_db_in(tmp_path)
    result = db.query("SELECT * FROM table_that_does_not_exist_xyz")
    assert result == []
    db.close()
