"""
SoloOS V10 — Observability Layer

Every tool call is logged as a JSON line to ~/.soloos/logs/tool_calls.jsonl.

Fields per entry:
  ts            ISO timestamp
  tool_name     str
  call_id       8-char hex
  duration_ms   int
  success       bool
  error         str (if failed)
  cache_hit     bool (if applicable)
  args_preview  first 100 chars of args (for debugging, not PII)

Query with:
  jq 'select(.tool_name == "council_brief") | .duration_ms' ~/.soloos/logs/tool_calls.jsonl
  jq 'select(.success == false)' ~/.soloos/logs/tool_calls.jsonl
  jq -s 'group_by(.tool_name) | map({tool: .[0].tool_name, calls: length, avg_ms: (map(.duration_ms) | add / length)})' ~/.soloos/logs/tool_calls.jsonl

Fail-open: if structlog is unavailable, observability is silently disabled.
"""

import time
import uuid
from functools import wraps
from pathlib import Path

_log = None
_log_available = False


def _get_logger():
    global _log, _log_available
    if _log is not None:
        return _log, _log_available

    try:
        import structlog

        log_dir = Path.home() / ".soloos" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "tool_calls.jsonl"

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.WriteLoggerFactory(
                file=log_file.open("a", encoding="utf-8")
            ),
        )
        _log = structlog.get_logger()
        _log_available = True
    except ImportError:
        _log = _NoOpLogger()
        _log_available = False
    except Exception:
        _log = _NoOpLogger()
        _log_available = False

    return _log, _log_available


class _NoOpLogger:
    """Silently swallows all log calls when structlog is unavailable."""
    def info(self, *a, **kw): pass
    def error(self, *a, **kw): pass
    def warning(self, *a, **kw): pass


def instrument_tool(fn):
    """
    Decorator for MCP tool functions.

    Wraps the function to:
    - Log every call with timing + success/failure
    - Add a call_id for correlation
    - Never break the tool on logging failure (fail-open)

    Usage:
        @mcp.tool()
        @instrument_tool
        def my_tool(param: str) -> str:
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        log, _ = _get_logger()
        call_id = uuid.uuid4().hex[:8]
        start = time.perf_counter()

        try:
            result = fn(*args, **kwargs)
            duration_ms = int((time.perf_counter() - start) * 1000)
            try:
                log.info(
                    "tool_call",
                    tool_name=fn.__name__,
                    call_id=call_id,
                    duration_ms=duration_ms,
                    success=True,
                    args_preview=str(args)[:100] if args else "",
                )
            except Exception:
                pass
            return result
        except Exception as exc:
            duration_ms = int((time.perf_counter() - start) * 1000)
            try:
                log.error(
                    "tool_call_failed",
                    tool_name=fn.__name__,
                    call_id=call_id,
                    duration_ms=duration_ms,
                    success=False,
                    error=str(exc)[:200],
                )
            except Exception:
                pass
            raise

    return wrapper


def log_event(event: str, **fields):
    """
    Log a named event with arbitrary fields.

    Usage:
        log_event("cache_hit", tool="council_brief", key_hash="abc123")
        log_event("kill_signal_blocked", entry_id="FL-007", days_overdue=3)
    """
    log, _ = _get_logger()
    try:
        log.info(event, **fields)
    except Exception:
        pass


def get_log_stats(period_hours: int = 24) -> dict:
    """
    Read tool_calls.jsonl and compute basic stats.

    Returns: {tool_name: {calls, avg_ms, errors}} dict
    Useful for `analyze_self` tool.
    """
    import json
    from datetime import datetime, timedelta

    log_file = Path.home() / ".soloos" / "logs" / "tool_calls.jsonl"
    if not log_file.exists():
        return {"status": "no_log_file", "entries": 0}

    cutoff = datetime.now() - timedelta(hours=period_hours)
    stats: dict[str, dict] = {}
    total = 0
    errors = 0

    try:
        with log_file.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    # Filter by time if timestamp present
                    ts_str = entry.get("ts") or entry.get("timestamp")
                    if ts_str:
                        try:
                            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00").replace("+00:00", ""))
                            if ts < cutoff:
                                continue
                        except Exception:
                            pass

                    tool = entry.get("tool_name", "unknown")
                    dur = entry.get("duration_ms", 0)
                    success = entry.get("success", True)

                    if tool not in stats:
                        stats[tool] = {"calls": 0, "total_ms": 0, "errors": 0}
                    stats[tool]["calls"] += 1
                    stats[tool]["total_ms"] += dur
                    if not success:
                        stats[tool]["errors"] += 1
                        errors += 1
                    total += 1
                except (json.JSONDecodeError, Exception):
                    continue
    except Exception as e:
        return {"status": "error", "message": str(e)}

    # Compute averages
    result = {
        "total_calls": total,
        "total_errors": errors,
        "period_hours": period_hours,
        "tools": {}
    }
    for tool, s in sorted(stats.items(), key=lambda x: -x[1]["calls"]):
        avg_ms = s["total_ms"] // s["calls"] if s["calls"] > 0 else 0
        result["tools"][tool] = {
            "calls": s["calls"],
            "avg_ms": avg_ms,
            "errors": s["errors"],
            "error_rate": round(s["errors"] / s["calls"], 3) if s["calls"] > 0 else 0,
        }

    return result
