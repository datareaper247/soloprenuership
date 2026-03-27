"""
Append-only audit log for all autonomous actions.
Path: ~/.soloos/audit.jsonl
Format: one JSON object per line.

{
  "id": "uuid",
  "ts": "2026-03-26T07:00:00Z",
  "action": "send_email",
  "tier": 2,
  "agent_id": "founder",
  "params": {...},              # PII redacted for email/support actions
  "reasoning": "...",
  "status": "executed",
  "result": {...},
  "duration_ms": 340
}
"""

from __future__ import annotations

import json
import uuid
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_AUDIT_PATH = Path.home() / ".soloos" / "audit.jsonl"


class AuditLog:
    def __init__(self, path: Path | None = None) -> None:
        self._path = path or _AUDIT_PATH
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass  # fail-open: log calls will also fail gracefully

    def log(self, entry: dict) -> str:
        """Append entry to audit log. Returns audit_id. Never raises."""
        audit_id = str(uuid.uuid4())
        record = {
            "id": audit_id,
            "ts": datetime.now(timezone.utc).isoformat(),
            **entry,
        }
        try:
            with self._path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, default=str) + "\n")
        except Exception as exc:
            logger.warning("AuditLog.log failed (non-fatal): %s", exc)
        return audit_id

    def query(self, filters: dict) -> list[dict]:
        """Return entries matching all filter key=value pairs."""
        results: list[dict] = []
        if not self._path.exists():
            return results
        try:
            with self._path.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if all(record.get(k) == v for k, v in filters.items()):
                        results.append(record)
        except Exception as exc:
            logger.warning("AuditLog.query failed (non-fatal): %s", exc)
        return results

    def get_stats(self, hours: int = 24) -> dict:
        """Return action counts and status summary for last N hours."""
        from datetime import timedelta

        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        counts: dict[str, int] = {}
        statuses: dict[str, int] = {}
        total = 0

        if not self._path.exists():
            return {"total": 0, "by_action": {}, "by_status": {}, "hours": hours}

        try:
            with self._path.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    ts_str = record.get("ts", "")
                    try:
                        ts = datetime.fromisoformat(ts_str)
                        if ts < cutoff:
                            continue
                    except Exception:
                        continue
                    total += 1
                    action = record.get("action", "unknown")
                    status = record.get("status", "unknown")
                    counts[action] = counts.get(action, 0) + 1
                    statuses[status] = statuses.get(status, 0) + 1
        except Exception as exc:
            logger.warning("AuditLog.get_stats failed (non-fatal): %s", exc)

        return {
            "total": total,
            "by_action": counts,
            "by_status": statuses,
            "hours": hours,
        }

    def export(self, path: Path) -> None:
        """Copy audit log to given path."""
        if not self._path.exists():
            path.write_text("")
            return
        try:
            path.write_text(self._path.read_text(encoding="utf-8"), encoding="utf-8")
        except Exception as exc:
            logger.warning("AuditLog.export failed (non-fatal): %s", exc)


_audit_log: AuditLog | None = None


def get_audit_log() -> AuditLog:
    global _audit_log
    if _audit_log is None:
        _audit_log = AuditLog()
    return _audit_log
