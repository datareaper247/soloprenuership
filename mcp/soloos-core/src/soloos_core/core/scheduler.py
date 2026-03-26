"""
SoloOS V10 — Background Scheduler (Phase F)

Runs periodic founder-intelligence jobs using APScheduler 3.x.
Delivers results via Slack webhook, ntfy.sh, or SMTP email.

Config file: ~/.soloos/scheduler-config.yaml
  - Created from template on first run (all jobs disabled by default in template)
  - If file missing: safe defaults (all jobs disabled, no delivery)

Env vars (override config file values):
  SOLOOS_SLACK_WEBHOOK  — Slack incoming webhook URL
  SOLOOS_NTFY_TOPIC     — ntfy.sh topic name
  SOLOOS_EMAIL_TO       — recipient email address
  SOLOOS_EMAIL_SMTP_HOST
  SOLOOS_EMAIL_SMTP_PORT (default 587)
  SOLOOS_EMAIL_USER
  SOLOOS_EMAIL_PASS

APScheduler is imported lazily so a missing package never breaks server startup.
All delivery functions fail open — errors are logged and execution continues.

Usage:
    from soloos_core.core.scheduler import get_scheduler
    sched = get_scheduler()
    sched.start()           # starts background thread, non-blocking
    sched.list_jobs()       # [{"name": ..., "next_run": ..., "enabled": ...}]
    sched.run_now("morning_brief_job")
    sched.stop()
"""

from __future__ import annotations

import logging
import os
import shutil
import smtplib
import threading
import warnings
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────

_CONFIG_PATH = Path.home() / ".soloos" / "scheduler-config.yaml"
_TEMPLATE_PATH = Path(__file__).parent / "scheduler-config-template.yaml"


# ─────────────────────────────────────────────────────────────
# Config loading (fail-open)
# ─────────────────────────────────────────────────────────────

_SAFE_DEFAULTS: dict[str, Any] = {
    "enabled": False,
    "timezone": "America/New_York",
    "delivery": {
        "slack_webhook_url": "",
        "ntfy_topic": "",
        "email_to": "",
        "email_smtp_host": "",
        "email_smtp_port": 587,
        "email_user": "",
        "email_pass": "",
    },
    "jobs": {
        "morning_brief": {"enabled": False, "cron": "0 7 * * *"},
        "kill_signal_check": {"enabled": False, "cron": "0 9 * * *"},
        "data_sync": {"enabled": False, "cron": "0 * * * *"},
        "weekly_review": {"enabled": False, "cron": "0 9 * * 1"},
        "monthly_investor_draft": {"enabled": False, "cron": "0 8 1 * *"},
    },
}


def _load_config() -> dict[str, Any]:
    """
    Load scheduler config from ~/.soloos/scheduler-config.yaml.

    If the file does not exist, copies the template to ~/.soloos/ (with
    instructions) and returns safe defaults (all jobs disabled).
    If yaml parsing fails, returns safe defaults and logs a warning.
    """
    if not _CONFIG_PATH.exists():
        _maybe_copy_template()
        return _SAFE_DEFAULTS.copy()

    try:
        with _CONFIG_PATH.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        # Merge with safe defaults so missing keys never cause KeyErrors
        merged = _deep_merge(_SAFE_DEFAULTS, data)
        return merged
    except Exception as exc:
        logger.warning("scheduler: failed to parse config at %s: %s — using safe defaults", _CONFIG_PATH, exc)
        return _SAFE_DEFAULTS.copy()


def _maybe_copy_template() -> None:
    """Copy the bundled template to ~/.soloos/ if it exists."""
    try:
        config_dir = _CONFIG_PATH.parent
        config_dir.mkdir(parents=True, exist_ok=True)
        if _TEMPLATE_PATH.exists():
            shutil.copy(_TEMPLATE_PATH, _CONFIG_PATH)
            logger.info(
                "scheduler: created %s from template — edit to enable jobs and delivery channels",
                _CONFIG_PATH,
            )
        else:
            logger.debug("scheduler: template not found at %s — using safe defaults only", _TEMPLATE_PATH)
    except Exception as exc:
        logger.warning("scheduler: could not copy template: %s", exc)


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base (base provides missing keys)."""
    result = base.copy()
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def _update_config_key(job_name: str, enabled: bool, cron: str) -> bool:
    """
    Persist a job change (enabled/cron) back to the config file.
    Returns True on success, False on failure (fail-open).
    """
    try:
        config_dir = _CONFIG_PATH.parent
        config_dir.mkdir(parents=True, exist_ok=True)
        # Load current or create fresh
        if _CONFIG_PATH.exists():
            with _CONFIG_PATH.open(encoding="utf-8") as fh:
                data: dict = yaml.safe_load(fh) or {}
        else:
            data = _SAFE_DEFAULTS.copy()

        data.setdefault("jobs", {})
        data["jobs"].setdefault(job_name, {})
        data["jobs"][job_name]["enabled"] = enabled
        if cron:
            data["jobs"][job_name]["cron"] = cron

        with _CONFIG_PATH.open("w", encoding="utf-8") as fh:
            yaml.dump(data, fh, default_flow_style=False, allow_unicode=True)
        return True
    except Exception as exc:
        logger.warning("scheduler: failed to persist config update: %s", exc)
        return False


# ─────────────────────────────────────────────────────────────
# Delivery functions (all fail-open, return bool)
# ─────────────────────────────────────────────────────────────

def deliver_slack(message: str, webhook_url: str) -> bool:
    """POST message to a Slack incoming webhook. Returns True on HTTP 200."""
    if not webhook_url:
        return False
    try:
        import httpx  # optional dep — part of [connectors] extra
        resp = httpx.post(webhook_url, json={"text": message}, timeout=10)
        if resp.status_code == 200:
            return True
        logger.warning("scheduler: Slack delivery returned HTTP %s", resp.status_code)
        return False
    except ImportError:
        # httpx not installed — try urllib
        try:
            import json as _json
            import urllib.request
            data = _json.dumps({"text": message}).encode("utf-8")
            req = urllib.request.Request(
                webhook_url,
                data=data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status == 200
        except Exception as exc:
            logger.warning("scheduler: Slack delivery failed (urllib fallback): %s", exc)
            return False
    except Exception as exc:
        logger.warning("scheduler: Slack delivery failed: %s", exc)
        return False


def deliver_ntfy(message: str, topic: str) -> bool:
    """POST message to ntfy.sh/{topic}. Returns True on success."""
    if not topic:
        return False
    url = f"https://ntfy.sh/{topic}"
    try:
        import httpx
        resp = httpx.post(url, content=message.encode("utf-8"), timeout=10)
        return resp.status_code < 300
    except ImportError:
        try:
            import urllib.request
            data = message.encode("utf-8")
            req = urllib.request.Request(url, data=data)
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status < 300
        except Exception as exc:
            logger.warning("scheduler: ntfy delivery failed (urllib fallback): %s", exc)
            return False
    except Exception as exc:
        logger.warning("scheduler: ntfy delivery failed: %s", exc)
        return False


def deliver_email(subject: str, body: str, config: dict) -> bool:
    """
    Send email via SMTP (stdlib smtplib). Returns True on success.

    config keys: email_to, email_smtp_host, email_smtp_port,
                 email_user, email_pass
    """
    to_addr = config.get("email_to", "")
    smtp_host = config.get("email_smtp_host", "")
    smtp_port = int(config.get("email_smtp_port", 587))
    user = config.get("email_user", "")
    password = config.get("email_pass", "")

    if not (to_addr and smtp_host):
        return False

    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = user or "soloos@localhost"
        msg["To"] = to_addr

        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            if user and password:
                server.login(user, password)
            server.sendmail(msg["From"], [to_addr], msg.as_string())
        return True
    except Exception as exc:
        logger.warning("scheduler: email delivery failed: %s", exc)
        return False


def deliver(message: str, subject: str = "") -> list[str]:
    """
    Deliver message to all configured channels.

    Reads delivery config from ~/.soloos/scheduler-config.yaml and
    SOLOOS_* env vars (env vars take priority over file).

    Returns list of channel names that succeeded (e.g. ["slack", "ntfy"]).
    Always fail-open — never raises.
    """
    config = _load_config()
    delivery_cfg = config.get("delivery", {})

    # Env vars override config file
    slack_url = (
        os.environ.get("SOLOOS_SLACK_WEBHOOK")
        or delivery_cfg.get("slack_webhook_url", "")
    )
    ntfy_topic = (
        os.environ.get("SOLOOS_NTFY_TOPIC")
        or delivery_cfg.get("ntfy_topic", "")
    )
    email_to = os.environ.get("SOLOOS_EMAIL_TO") or delivery_cfg.get("email_to", "")

    # Build effective email config
    email_config = {
        "email_to": email_to,
        "email_smtp_host": (
            os.environ.get("SOLOOS_EMAIL_SMTP_HOST")
            or delivery_cfg.get("email_smtp_host", "")
        ),
        "email_smtp_port": (
            os.environ.get("SOLOOS_EMAIL_SMTP_PORT")
            or delivery_cfg.get("email_smtp_port", 587)
        ),
        "email_user": (
            os.environ.get("SOLOOS_EMAIL_USER")
            or delivery_cfg.get("email_user", "")
        ),
        "email_pass": (
            os.environ.get("SOLOOS_EMAIL_PASS")
            or delivery_cfg.get("email_pass", "")
        ),
    }

    successes: list[str] = []

    if slack_url and deliver_slack(message, slack_url):
        successes.append("slack")

    if ntfy_topic and deliver_ntfy(message, ntfy_topic):
        successes.append("ntfy")

    if email_to and deliver_email(subject or "SoloOS Notification", message, email_config):
        successes.append("email")

    return successes


# ─────────────────────────────────────────────────────────────
# Job implementations (call SoloOS tool functions)
# ─────────────────────────────────────────────────────────────

def _run_morning_brief_job() -> str:
    """Call run_morning_intelligence() and deliver result."""
    try:
        from ..tools.intelligence import run_morning_intelligence
        result = run_morning_intelligence()
        # result is a dict; convert to readable string for delivery
        if isinstance(result, dict):
            import json
            message = json.dumps(result, indent=2)
        else:
            message = str(result)
        channels = deliver(message, subject="SoloOS Morning Brief")
        logger.info("scheduler: morning_brief_job completed, delivered to: %s", channels)
        return f"morning_brief_job done — channels: {channels}"
    except Exception as exc:
        logger.warning("scheduler: morning_brief_job failed: %s", exc)
        return f"morning_brief_job error: {exc}"


def _run_kill_signal_check_job() -> str:
    """Call check_kill_signals_tool() and deliver if overdue signals exist."""
    try:
        from ..tools.memory import check_kill_signals_tool
        result = check_kill_signals_tool()
        # Only deliver if there are overdue signals (result contains "OVERDUE" text)
        if "OVERDUE" in result or "overdue" in result.lower():
            channels = deliver(result, subject="SoloOS Kill Signal Alert")
            logger.info("scheduler: kill_signal_check_job — overdue signals found, delivered to: %s", channels)
            return f"kill_signal_check_job — overdue found, delivered to: {channels}"
        logger.info("scheduler: kill_signal_check_job — no overdue signals")
        return "kill_signal_check_job — no overdue signals"
    except Exception as exc:
        logger.warning("scheduler: kill_signal_check_job failed: %s", exc)
        return f"kill_signal_check_job error: {exc}"


def _run_data_sync_job() -> str:
    """Placeholder data sync job — logs intent, no-op until connectors configured."""
    logger.info("scheduler: data_sync not yet configured — skipping")
    return "data_sync: sync not yet configured"


def _run_weekly_review_job() -> str:
    """Weekly review — calls run_morning_intelligence() with extended context."""
    try:
        from ..tools.intelligence import run_morning_intelligence
        result = run_morning_intelligence()
        if isinstance(result, dict):
            import json
            message = "WEEKLY REVIEW\n\n" + json.dumps(result, indent=2)
        else:
            message = "WEEKLY REVIEW\n\n" + str(result)
        channels = deliver(message, subject="SoloOS Weekly Review")
        logger.info("scheduler: weekly_review_job completed, delivered to: %s", channels)
        return f"weekly_review_job done — channels: {channels}"
    except Exception as exc:
        logger.warning("scheduler: weekly_review_job failed: %s", exc)
        return f"weekly_review_job error: {exc}"


# Map job names to callable functions
_JOB_FUNCTIONS: dict[str, Any] = {
    "morning_brief_job": _run_morning_brief_job,
    "kill_signal_check_job": _run_kill_signal_check_job,
    "data_sync_job": _run_data_sync_job,
    "weekly_review_job": _run_weekly_review_job,
}

# Config key → job id mapping (config uses underscores without _job suffix)
_CONFIG_TO_JOB_ID: dict[str, str] = {
    "morning_brief": "morning_brief_job",
    "kill_signal_check": "kill_signal_check_job",
    "data_sync": "data_sync_job",
    "weekly_review": "weekly_review_job",
    "monthly_investor_draft": "weekly_review_job",  # placeholder reuses weekly fn
}


# ─────────────────────────────────────────────────────────────
# APScheduler wrapper (lazy import, fail-open stub on ImportError)
# ─────────────────────────────────────────────────────────────

class _NoOpScheduler:
    """
    Stub scheduler returned when APScheduler is not installed.
    All methods are safe no-ops so the MCP server always starts cleanly.
    """

    def start(self) -> None:
        logger.warning(
            "scheduler: APScheduler not installed — jobs will not run. "
            "Install with: pip install 'apscheduler>=3.10.0'"
        )

    def stop(self) -> None:
        pass

    def run_now(self, job_name: str) -> str:
        fn = _JOB_FUNCTIONS.get(job_name)
        if fn is None:
            return f"Unknown job '{job_name}'. Available: {list(_JOB_FUNCTIONS)}"
        # Run synchronously even without APScheduler
        return fn()

    def list_jobs(self) -> list[dict]:
        config = _load_config()
        jobs_cfg = config.get("jobs", {})
        result = []
        for cfg_key, job_id in _CONFIG_TO_JOB_ID.items():
            job_cfg = jobs_cfg.get(cfg_key, {})
            result.append({
                "name": job_id,
                "config_key": cfg_key,
                "enabled": job_cfg.get("enabled", False),
                "cron": job_cfg.get("cron", ""),
                "next_run": "N/A (APScheduler not installed)",
                "status": "stub",
            })
        return result

    def next_run(self, job_name: str) -> str:
        return f"N/A (APScheduler not installed) for job '{job_name}'"


class SoloOSScheduler:
    """
    Background scheduler for SoloOS founder-intelligence jobs.

    Reads job schedule from ~/.soloos/scheduler-config.yaml.
    Uses APScheduler 3.x BackgroundScheduler with ThreadPoolExecutor.
    All jobs fail open — an error in one job never crashes the scheduler.

    Thread safety: start()/stop() are idempotent and thread-safe.
    """

    def __init__(self) -> None:
        self._scheduler: Any = None
        self._lock = threading.Lock()
        self._started = False
        self._config: dict[str, Any] = {}

    def _build_scheduler(self) -> Any:
        """Lazily import APScheduler and construct BackgroundScheduler."""
        # Suppress APScheduler deprecation warnings on Python 3.12+
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.executors.pool import ThreadPoolExecutor as APThreadPoolExecutor

        self._config = _load_config()
        tz = self._config.get("timezone", "America/New_York")

        executors = {"default": APThreadPoolExecutor(max_workers=3)}
        job_defaults = {
            "coalesce": True,      # run only once if multiple triggers missed
            "max_instances": 1,    # never overlap
            "misfire_grace_time": 300,  # 5-minute grace window for misfires
        }

        sched = BackgroundScheduler(
            executors=executors,
            job_defaults=job_defaults,
            timezone=tz,
        )
        return sched

    def _register_jobs(self) -> None:
        """Register enabled jobs from config onto the scheduler."""
        from apscheduler.triggers.cron import CronTrigger

        jobs_cfg = self._config.get("jobs", {})
        global_enabled = self._config.get("enabled", False)

        for cfg_key, job_id in _CONFIG_TO_JOB_ID.items():
            job_cfg = jobs_cfg.get(cfg_key, {})
            job_enabled = global_enabled and job_cfg.get("enabled", False)
            if not job_enabled:
                continue

            cron_expr = job_cfg.get("cron", "")
            fn = _JOB_FUNCTIONS.get(job_id)
            if fn is None or not cron_expr:
                continue

            try:
                # Parse "min hour dom mon dow" cron expression
                parts = cron_expr.strip().split()
                if len(parts) == 5:
                    minute, hour, day, month, day_of_week = parts
                    trigger = CronTrigger(
                        minute=minute,
                        hour=hour,
                        day=day,
                        month=month,
                        day_of_week=day_of_week,
                    )
                else:
                    logger.warning("scheduler: invalid cron '%s' for job '%s' — skipping", cron_expr, job_id)
                    continue

                # Wrap job to catch all exceptions (fail-open)
                def _safe_job(func=fn, name=job_id):
                    try:
                        func()
                    except Exception as exc:
                        logger.error("scheduler: job '%s' raised unhandled error: %s", name, exc)

                self._scheduler.add_job(
                    _safe_job,
                    trigger=trigger,
                    id=job_id,
                    name=job_id,
                    replace_existing=True,
                )
                logger.info("scheduler: registered job '%s' with cron '%s'", job_id, cron_expr)
            except Exception as exc:
                logger.warning("scheduler: failed to register job '%s': %s", job_id, exc)

    def start(self) -> None:
        """Start the background scheduler (non-blocking). Idempotent."""
        with self._lock:
            if self._started:
                return
            try:
                self._scheduler = self._build_scheduler()
                self._register_jobs()
                self._scheduler.start()
                self._started = True
                logger.info("scheduler: started with timezone=%s", self._config.get("timezone"))
            except Exception as exc:
                logger.warning("scheduler: failed to start: %s", exc)
                self._started = False

    def stop(self) -> None:
        """Stop the background scheduler gracefully. Idempotent."""
        with self._lock:
            if not self._started or self._scheduler is None:
                return
            try:
                self._scheduler.shutdown(wait=False)
            except Exception as exc:
                logger.warning("scheduler: error during stop: %s", exc)
            finally:
                self._started = False

    def run_now(self, job_name: str) -> str:
        """
        Manually trigger a job immediately (runs in current thread).
        Works whether or not the scheduler is started.
        Returns the job result string.
        """
        fn = _JOB_FUNCTIONS.get(job_name)
        if fn is None:
            available = list(_JOB_FUNCTIONS.keys())
            return f"Unknown job '{job_name}'. Available: {available}"
        try:
            result = fn()
            return result
        except Exception as exc:
            logger.warning("scheduler: run_now('%s') failed: %s", job_name, exc)
            return f"run_now error for '{job_name}': {exc}"

    def list_jobs(self) -> list[dict]:
        """Return list of all known jobs with config + next_run info."""
        config = _load_config()
        jobs_cfg = config.get("jobs", {})
        global_enabled = config.get("enabled", False)
        result = []

        for cfg_key, job_id in _CONFIG_TO_JOB_ID.items():
            job_cfg = jobs_cfg.get(cfg_key, {})
            job_enabled = global_enabled and job_cfg.get("enabled", False)

            next_run_str = "not scheduled"
            if self._started and self._scheduler is not None and job_enabled:
                try:
                    job = self._scheduler.get_job(job_id)
                    if job and job.next_run_time:
                        next_run_str = job.next_run_time.isoformat()
                except Exception:
                    next_run_str = "unknown"

            result.append({
                "name": job_id,
                "config_key": cfg_key,
                "enabled": job_enabled,
                "cron": job_cfg.get("cron", ""),
                "next_run": next_run_str,
                "status": "running" if (self._started and job_enabled) else "idle",
            })

        return result

    def next_run(self, job_name: str) -> str:
        """Return ISO timestamp of next scheduled run for a job, or descriptive string."""
        if not self._started or self._scheduler is None:
            return f"scheduler not started — '{job_name}' not scheduled"
        try:
            job = self._scheduler.get_job(job_name)
            if job is None:
                return f"job '{job_name}' not registered (check if enabled in config)"
            if job.next_run_time is None:
                return f"job '{job_name}' registered but no next_run_time (paused?)"
            return job.next_run_time.isoformat()
        except Exception as exc:
            return f"error getting next_run for '{job_name}': {exc}"


# ─────────────────────────────────────────────────────────────
# Module-level singleton
# ─────────────────────────────────────────────────────────────

_scheduler_instance: SoloOSScheduler | _NoOpScheduler | None = None
_scheduler_lock = threading.Lock()


def get_scheduler() -> "SoloOSScheduler | _NoOpScheduler":
    """
    Return the module-level scheduler singleton.

    Returns SoloOSScheduler if APScheduler is installed,
    _NoOpScheduler stub otherwise (so server always starts cleanly).
    """
    global _scheduler_instance

    if _scheduler_instance is not None:
        return _scheduler_instance

    with _scheduler_lock:
        if _scheduler_instance is not None:
            return _scheduler_instance

        try:
            import apscheduler  # noqa: F401 — presence check only
            _scheduler_instance = SoloOSScheduler()
        except ImportError:
            logger.warning(
                "scheduler: apscheduler not installed — using no-op stub. "
                "Install with: pip install 'apscheduler>=3.10.0'"
            )
            _scheduler_instance = _NoOpScheduler()

    return _scheduler_instance


# ─────────────────────────────────────────────────────────────
# MCP tool helper functions (called by server.py)
# ─────────────────────────────────────────────────────────────

def scheduler_status() -> dict:
    """
    Return scheduler status: jobs, next run times, delivery channels configured.
    Used by the scheduler_status MCP tool in server.py.
    """
    sched = get_scheduler()
    config = _load_config()
    delivery_cfg = config.get("delivery", {})

    # Determine which delivery channels are configured (env or config)
    channels_configured = []
    if os.environ.get("SOLOOS_SLACK_WEBHOOK") or delivery_cfg.get("slack_webhook_url"):
        channels_configured.append("slack")
    if os.environ.get("SOLOOS_NTFY_TOPIC") or delivery_cfg.get("ntfy_topic"):
        channels_configured.append("ntfy")
    if os.environ.get("SOLOOS_EMAIL_TO") or delivery_cfg.get("email_to"):
        channels_configured.append("email")

    return {
        "scheduler_enabled": config.get("enabled", False),
        "timezone": config.get("timezone", "America/New_York"),
        "config_path": str(_CONFIG_PATH),
        "config_exists": _CONFIG_PATH.exists(),
        "delivery_channels_configured": channels_configured,
        "jobs": sched.list_jobs(),
        "apscheduler_available": not isinstance(sched, _NoOpScheduler),
        "started": getattr(sched, "_started", False),
    }


def scheduler_run_now(job_name: str) -> dict:
    """
    Trigger a job immediately. Returns result dict.
    Used by the scheduler_run_now MCP tool in server.py.
    """
    sched = get_scheduler()
    result = sched.run_now(job_name)
    return {
        "job_name": job_name,
        "result": result,
        "available_jobs": list(_JOB_FUNCTIONS.keys()),
    }


def scheduler_configure(job_name: str, enabled: bool, cron: str = "") -> dict:
    """
    Update config file for a job (enabled state and optionally cron expression).
    Used by the scheduler_configure MCP tool in server.py.
    """
    # Normalise job_name — accept both "morning_brief" and "morning_brief_job"
    cfg_key = job_name.replace("_job", "")

    success = _update_config_key(cfg_key, enabled, cron)
    return {
        "job": job_name,
        "config_key": cfg_key,
        "enabled": enabled,
        "cron": cron or "(unchanged)",
        "saved": success,
        "config_path": str(_CONFIG_PATH),
        "note": "Restart the scheduler (or MCP server) for changes to take effect.",
    }


# ─────────────────────────────────────────────────────────────
# Smoke test
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    print("=== SoloOS Scheduler smoke test ===")
    sched = get_scheduler()
    print(f"Scheduler type: {type(sched).__name__}")
    print(f"\nJob list:\n{json.dumps(sched.list_jobs(), indent=2)}")
    print(f"\nStatus:\n{json.dumps(scheduler_status(), indent=2)}")
    print("\nrun_now(data_sync_job):", sched.run_now("data_sync_job"))
    print("\nDone.")
