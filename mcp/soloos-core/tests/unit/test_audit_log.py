"""Tests for AuditLog — append-only action audit trail."""

import json
import tempfile
from pathlib import Path

from soloos_core.core.audit_log import AuditLog


def _tmp_log() -> AuditLog:
    p = Path(tempfile.mktemp(suffix=".jsonl"))
    return AuditLog(path=p)


def test_log_creates_file_and_returns_id():
    log = _tmp_log()
    audit_id = log.log({"action": "test", "status": "executed"})
    assert audit_id
    assert log._path.exists()


def test_log_appends_not_overwrites():
    log = _tmp_log()
    id1 = log.log({"action": "a", "status": "executed"})
    id2 = log.log({"action": "b", "status": "executed"})
    lines = [l for l in log._path.read_text().splitlines() if l.strip()]
    assert len(lines) == 2
    ids = [json.loads(l)["id"] for l in lines]
    assert id1 in ids
    assert id2 in ids


def test_log_never_raises_on_bad_path():
    log = AuditLog(path=Path("/nonexistent_dir/audit.jsonl"))
    # Should not raise
    audit_id = log.log({"action": "test"})
    assert audit_id  # still returns an ID


def test_query_filter_by_status():
    log = _tmp_log()
    log.log({"action": "a", "status": "executed"})
    log.log({"action": "b", "status": "blocked"})
    log.log({"action": "c", "status": "executed"})

    executed = log.query({"status": "executed"})
    assert len(executed) == 2
    blocked = log.query({"status": "blocked"})
    assert len(blocked) == 1


def test_query_empty_if_no_match():
    log = _tmp_log()
    log.log({"action": "a", "status": "executed"})
    results = log.query({"status": "nonexistent"})
    assert results == []


def test_query_returns_empty_list_when_file_missing():
    log = AuditLog(path=Path("/tmp/does_not_exist_ever.jsonl"))
    results = log.query({"status": "executed"})
    assert results == []


def test_get_stats_returns_expected_keys():
    log = _tmp_log()
    log.log({"action": "send_email", "status": "executed"})
    log.log({"action": "send_email", "status": "executed"})
    log.log({"action": "post_tweet", "status": "dry_run"})

    stats = log.get_stats(hours=24)
    assert "total" in stats
    assert "by_action" in stats
    assert "by_status" in stats
    assert stats["total"] >= 3
    assert stats["by_action"].get("send_email", 0) >= 2


def test_get_stats_empty_file():
    log = _tmp_log()
    stats = log.get_stats()
    assert stats["total"] == 0


def test_export_copies_file():
    log = _tmp_log()
    log.log({"action": "x", "status": "executed"})

    export_path = Path(tempfile.mktemp(suffix=".jsonl"))
    log.export(export_path)
    assert export_path.exists()
    content = export_path.read_text()
    assert '"action"' in content


def test_each_entry_has_id_and_ts():
    log = _tmp_log()
    log.log({"action": "test"})
    line = json.loads(log._path.read_text().strip())
    assert "id" in line
    assert "ts" in line
    assert "action" in line
