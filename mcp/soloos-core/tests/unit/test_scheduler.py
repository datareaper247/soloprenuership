"""
Tests for src/soloos_core/core/scheduler.py — Phase F

Covers:
  1. Config loading — safe defaults when file absent
  2. Config loading — template copied to ~/.soloos/ when file absent
  3. Deep merge preserves defaults for missing keys
  4. Job listing — returns all known jobs with correct structure
  5. run_now with unknown job returns descriptive error string
  6. run_now with data_sync_job succeeds and returns expected string
  7. deliver() with no channels configured returns empty list
  8. deliver_slack with empty webhook_url returns False (no-op)
  9. deliver_ntfy with empty topic returns False (no-op)
 10. scheduler_status() returns required keys
 11. scheduler_configure() returns saved/config_path keys
 12. _NoOpScheduler.run_now falls through to job function
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _import_scheduler():
    """Import scheduler module fresh (handles optional APScheduler)."""
    import soloos_core.core.scheduler as sched
    return sched


# ─────────────────────────────────────────────────────────────
# 1. Config loading — safe defaults when config file absent
# ─────────────────────────────────────────────────────────────

def test_load_config_returns_safe_defaults_when_file_missing(tmp_path):
    """_load_config() must return safe defaults when ~/.soloos/scheduler-config.yaml absent."""
    sched = _import_scheduler()
    missing_path = tmp_path / "no-such-file.yaml"

    with patch.object(sched, "_CONFIG_PATH", missing_path):
        # Patch _maybe_copy_template to be a no-op so we don't write files
        with patch.object(sched, "_maybe_copy_template"):
            config = sched._load_config()

    assert config["enabled"] is False
    assert "jobs" in config
    assert "delivery" in config
    # All jobs disabled by default
    for job_cfg in config["jobs"].values():
        assert job_cfg["enabled"] is False


# ─────────────────────────────────────────────────────────────
# 2. Config loading — template copy attempted when file absent
# ─────────────────────────────────────────────────────────────

def test_load_config_attempts_template_copy_when_file_missing(tmp_path):
    """_load_config() must call _maybe_copy_template when config file is missing."""
    sched = _import_scheduler()
    missing_path = tmp_path / "no-such-file.yaml"

    with patch.object(sched, "_CONFIG_PATH", missing_path):
        with patch.object(sched, "_maybe_copy_template") as mock_copy:
            sched._load_config()

    mock_copy.assert_called_once()


# ─────────────────────────────────────────────────────────────
# 3. Deep merge preserves defaults for missing keys
# ─────────────────────────────────────────────────────────────

def test_deep_merge_fills_missing_keys():
    """_deep_merge must fill keys present in base but absent in override."""
    sched = _import_scheduler()

    base = {"a": 1, "b": {"x": 10, "y": 20}, "c": "keep"}
    override = {"b": {"x": 99}}  # y missing, c not overridden

    result = sched._deep_merge(base, override)

    assert result["a"] == 1          # untouched
    assert result["b"]["x"] == 99    # overridden
    assert result["b"]["y"] == 20    # filled from base
    assert result["c"] == "keep"     # untouched


def test_deep_merge_override_wins_for_scalars():
    """_deep_merge override must win for scalar values."""
    sched = _import_scheduler()

    base = {"enabled": False, "timezone": "UTC"}
    override = {"enabled": True}

    result = sched._deep_merge(base, override)
    assert result["enabled"] is True
    assert result["timezone"] == "UTC"  # base preserved


# ─────────────────────────────────────────────────────────────
# 4. Job listing — correct structure for all known jobs
# ─────────────────────────────────────────────────────────────

def test_list_jobs_returns_all_known_jobs(tmp_path):
    """list_jobs() must return an entry for every known job with required keys."""
    sched_mod = _import_scheduler()

    with patch.object(sched_mod, "_CONFIG_PATH", tmp_path / "no-config.yaml"):
        with patch.object(sched_mod, "_maybe_copy_template"):
            # Reset singleton so it picks up the patched config path
            with patch.object(sched_mod, "_scheduler_instance", None):
                scheduler = sched_mod._NoOpScheduler()
                jobs = scheduler.list_jobs()

    assert isinstance(jobs, list)
    assert len(jobs) > 0

    required_keys = {"name", "config_key", "enabled", "cron", "next_run", "status"}
    for job in jobs:
        assert required_keys.issubset(job.keys()), f"Job missing keys: {job}"

    # All known job ids must appear
    job_names = {j["name"] for j in jobs}
    expected = {"morning_brief_job", "kill_signal_check_job", "data_sync_job", "weekly_review_job"}
    assert expected.issubset(job_names)


# ─────────────────────────────────────────────────────────────
# 5. run_now with unknown job returns descriptive error
# ─────────────────────────────────────────────────────────────

def test_run_now_unknown_job_returns_error_string():
    """run_now() with an unrecognised job name must return an error string, not raise."""
    sched_mod = _import_scheduler()
    scheduler = sched_mod._NoOpScheduler()

    result = scheduler.run_now("nonexistent_job_xyz")

    assert isinstance(result, str)
    assert "Unknown job" in result or "nonexistent_job_xyz" in result


# ─────────────────────────────────────────────────────────────
# 6. run_now with data_sync_job succeeds
# ─────────────────────────────────────────────────────────────

def test_run_now_data_sync_job_returns_string():
    """run_now('data_sync_job') must complete without raising and return a string."""
    sched_mod = _import_scheduler()
    scheduler = sched_mod._NoOpScheduler()

    result = scheduler.run_now("data_sync_job")

    assert isinstance(result, str)
    # The data_sync job logs "sync not yet configured"
    assert "sync" in result.lower() or "data" in result.lower()


# ─────────────────────────────────────────────────────────────
# 7. deliver() with no channels returns empty list
# ─────────────────────────────────────────────────────────────

def test_deliver_no_channels_returns_empty_list(tmp_path, monkeypatch):
    """deliver() must return [] when no delivery channels are configured."""
    sched_mod = _import_scheduler()

    # Clear env vars that could provide channel config
    for var in ("SOLOOS_SLACK_WEBHOOK", "SOLOOS_NTFY_TOPIC", "SOLOOS_EMAIL_TO"):
        monkeypatch.delenv(var, raising=False)

    # Point config to a missing file (safe defaults = all delivery empty)
    with patch.object(sched_mod, "_CONFIG_PATH", tmp_path / "no-config.yaml"):
        with patch.object(sched_mod, "_maybe_copy_template"):
            result = sched_mod.deliver("test message", subject="Test")

    assert result == []


# ─────────────────────────────────────────────────────────────
# 8. deliver_slack with empty webhook_url returns False
# ─────────────────────────────────────────────────────────────

def test_deliver_slack_empty_url_returns_false():
    """deliver_slack() must return False immediately when webhook_url is empty."""
    sched_mod = _import_scheduler()
    result = sched_mod.deliver_slack("hello", "")
    assert result is False


# ─────────────────────────────────────────────────────────────
# 9. deliver_ntfy with empty topic returns False
# ─────────────────────────────────────────────────────────────

def test_deliver_ntfy_empty_topic_returns_false():
    """deliver_ntfy() must return False immediately when topic is empty."""
    sched_mod = _import_scheduler()
    result = sched_mod.deliver_ntfy("hello", "")
    assert result is False


# ─────────────────────────────────────────────────────────────
# 10. scheduler_status() returns required keys
# ─────────────────────────────────────────────────────────────

def test_scheduler_status_returns_required_keys(tmp_path, monkeypatch):
    """scheduler_status() must return a dict with all required top-level keys."""
    sched_mod = _import_scheduler()

    for var in ("SOLOOS_SLACK_WEBHOOK", "SOLOOS_NTFY_TOPIC", "SOLOOS_EMAIL_TO"):
        monkeypatch.delenv(var, raising=False)

    with patch.object(sched_mod, "_CONFIG_PATH", tmp_path / "no-config.yaml"):
        with patch.object(sched_mod, "_maybe_copy_template"):
            with patch.object(sched_mod, "_scheduler_instance", None):
                status = sched_mod.scheduler_status()

    required = {
        "scheduler_enabled",
        "timezone",
        "config_path",
        "config_exists",
        "delivery_channels_configured",
        "jobs",
        "apscheduler_available",
    }
    assert required.issubset(status.keys())
    assert isinstance(status["jobs"], list)
    assert isinstance(status["delivery_channels_configured"], list)


# ─────────────────────────────────────────────────────────────
# 11. scheduler_configure() returns expected keys
# ─────────────────────────────────────────────────────────────

def test_scheduler_configure_returns_expected_keys(tmp_path):
    """scheduler_configure() must return a dict with saved/config_path/job keys."""
    sched_mod = _import_scheduler()

    with patch.object(sched_mod, "_CONFIG_PATH", tmp_path / "scheduler-config.yaml"):
        result = sched_mod.scheduler_configure(
            job_name="morning_brief",
            enabled=True,
            cron="0 8 * * *",
        )

    required = {"job", "config_key", "enabled", "cron", "saved", "config_path", "note"}
    assert required.issubset(result.keys())
    assert result["enabled"] is True


# ─────────────────────────────────────────────────────────────
# 12. _NoOpScheduler.run_now falls through to actual job function
# ─────────────────────────────────────────────────────────────

def test_noop_scheduler_run_now_calls_job_function():
    """_NoOpScheduler.run_now must call the mapped job function, not be a pure no-op."""
    sched_mod = _import_scheduler()

    called = []

    def _mock_fn():
        called.append(True)
        return "mock result"

    scheduler = sched_mod._NoOpScheduler()

    with patch.dict(sched_mod._JOB_FUNCTIONS, {"data_sync_job": _mock_fn}):
        result = scheduler.run_now("data_sync_job")

    assert len(called) == 1, "Job function should have been called once"
    assert result == "mock result"


# ─────────────────────────────────────────────────────────────
# 13. get_scheduler() singleton is stable
# ─────────────────────────────────────────────────────────────

def test_get_scheduler_returns_same_instance():
    """get_scheduler() must return the same object on repeated calls (singleton)."""
    sched_mod = _import_scheduler()

    with patch.object(sched_mod, "_scheduler_instance", None):
        s1 = sched_mod.get_scheduler()
        s2 = sched_mod.get_scheduler()

    # After resetting, both calls (within same patch context) may differ, but
    # calling again without patching should return the cached one.
    s3 = sched_mod.get_scheduler()
    s4 = sched_mod.get_scheduler()
    assert s3 is s4, "Singleton must return identical object on repeated calls"


# ─────────────────────────────────────────────────────────────
# 14. deliver_email with missing smtp_host returns False
# ─────────────────────────────────────────────────────────────

def test_deliver_email_missing_host_returns_false():
    """deliver_email() must return False without raising when smtp_host is missing."""
    sched_mod = _import_scheduler()
    result = sched_mod.deliver_email(
        subject="Test",
        body="hello",
        config={"email_to": "a@b.com", "email_smtp_host": ""},
    )
    assert result is False


# ─────────────────────────────────────────────────────────────
# 15. scheduler_run_now helper returns correct structure
# ─────────────────────────────────────────────────────────────

def test_scheduler_run_now_helper_returns_dict():
    """scheduler_run_now() helper must return dict with job_name/result/available_jobs."""
    sched_mod = _import_scheduler()

    result = sched_mod.scheduler_run_now("data_sync_job")

    assert isinstance(result, dict)
    assert "job_name" in result
    assert "result" in result
    assert "available_jobs" in result
    assert result["job_name"] == "data_sync_job"
    assert isinstance(result["available_jobs"], list)
