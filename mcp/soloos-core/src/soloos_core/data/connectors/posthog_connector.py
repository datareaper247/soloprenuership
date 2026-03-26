"""
SoloOS V10 — PostHog Connector

Syncs PostHog events to the DuckDB user_events table.

Env vars required:
    POSTHOG_API_KEY — PostHog personal API key (from PostHog → Settings → Personal API Keys)

Optional:
    POSTHOG_HOST    — PostHog host (default: https://app.posthog.com)
                      Set to your self-hosted URL if not using PostHog Cloud.

PostHog API endpoint used:
    GET {host}/api/event/          — paginated event list
    GET {host}/api/person/         — person properties (for user enrichment)

Writes to: user_events table in AnalyticsDB.
Idempotent: duplicate event IDs silently ignored via ON CONFLICT DO NOTHING.

SDK:
    httpx>=0.27.0  (optional dep — install with pip install 'soloos-core[connectors]')
    If not installed, is_configured() returns False and sync() returns error SyncResult.

Note: The posthog>=3.0.0 Python SDK is for *sending* events (client-side).
For *reading* events we use the PostHog Query API via httpx directly.
The posthog optional dep is listed in pyproject.toml for completeness (capture usage).
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.parse import urljoin

from .base import BaseConnector, SyncResult

logger = logging.getLogger(__name__)

_DEFAULT_POSTHOG_HOST = "https://app.posthog.com"

# ─────────────────────────────────────────────────────────────
# SDK availability (lazy, fail-open)
# ─────────────────────────────────────────────────────────────

_httpx_available: Optional[bool] = None


def _check_httpx() -> bool:
    global _httpx_available
    if _httpx_available is None:
        try:
            import httpx  # noqa: F401
            _httpx_available = True
        except ImportError:
            _httpx_available = False
    return _httpx_available


# ─────────────────────────────────────────────────────────────
# PostHogConnector
# ─────────────────────────────────────────────────────────────

class PostHogConnector(BaseConnector):
    """
    Syncs PostHog events to user_events table in DuckDB.

    Uses the PostHog Query API (personal API key required for read access).
    Falls back gracefully when httpx is not installed or key is absent.
    """

    source_name = "posthog"

    def is_configured(self) -> bool:
        """Return True only if POSTHOG_API_KEY is set AND httpx is installed."""
        try:
            return bool(os.environ.get("POSTHOG_API_KEY")) and _check_httpx()
        except Exception:
            return False

    def get_schema_tables(self) -> list[str]:
        return ["user_events"]

    def sync(self, since_cursor: Optional[str] = None) -> SyncResult:
        """
        Fetch PostHog events and upsert into user_events.

        Args:
            since_cursor: ISO datetime string (after= param) for incremental sync.
                          None = fetch last 30 days of events.

        Returns:
            SyncResult with rows_synced, new cursor (latest event timestamp),
            and optional error.
        """
        if not self.is_configured():
            return SyncResult(
                source=self.source_name,
                rows_synced=0,
                cursor=since_cursor,
                error="PostHog not configured: POSTHOG_API_KEY missing or httpx not installed",
            )

        try:
            import httpx
            from soloos_core.data.analytics_db import get_analytics_db

            api_key = os.environ["POSTHOG_API_KEY"]
            host = os.environ.get("POSTHOG_HOST", _DEFAULT_POSTHOG_HOST).rstrip("/")
            db = get_analytics_db()

            # Determine time window
            if since_cursor:
                after_dt = since_cursor
            else:
                cutoff = datetime.now(timezone.utc) - timedelta(days=30)
                after_dt = cutoff.strftime("%Y-%m-%dT%H:%M:%S")

            rows: list[dict] = []
            new_cursor = since_cursor
            next_url: Optional[str] = f"{host}/api/event/"
            page_count = 0
            max_pages = 50  # Safety cap to avoid infinite loops

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            with httpx.Client(timeout=30.0) as client:
                while next_url and page_count < max_pages:
                    params: dict = {}
                    # Only add after param on first page (next_url carries pagination)
                    if page_count == 0:
                        params["after"] = after_dt
                        params["limit"] = 100

                    try:
                        resp = client.get(next_url, headers=headers, params=params if page_count == 0 else {})
                        resp.raise_for_status()
                        data = resp.json()
                    except httpx.HTTPStatusError as exc:
                        status_code = exc.response.status_code
                        if status_code == 401:
                            return SyncResult(
                                source=self.source_name,
                                rows_synced=0,
                                cursor=since_cursor,
                                error="PostHog authentication failed: invalid API key",
                            )
                        if status_code == 403:
                            return SyncResult(
                                source=self.source_name,
                                rows_synced=0,
                                cursor=since_cursor,
                                error="PostHog access denied: personal API key may lack read permissions",
                            )
                        return SyncResult(
                            source=self.source_name,
                            rows_synced=0,
                            cursor=since_cursor,
                            error=f"PostHog API HTTP {status_code}: {exc}",
                        )
                    except httpx.RequestError as exc:
                        return SyncResult(
                            source=self.source_name,
                            rows_synced=0,
                            cursor=since_cursor,
                            error=f"PostHog network error: {exc}",
                        )

                    events = data.get("results", [])
                    next_url = data.get("next")

                    for event in events:
                        row = _event_to_row(event)
                        rows.append(row)
                        # Track latest event timestamp as cursor
                        ts = event.get("timestamp", "")
                        if ts and (new_cursor is None or ts > new_cursor):
                            new_cursor = ts

                    page_count += 1

                    if not events:
                        break

            # Write to DuckDB
            inserted = db.insert_events("user_events", rows) if rows else 0

            # Update sync state
            if new_cursor:
                db.update_sync_state(self.source_name, new_cursor)

            logger.info(
                "posthog_connector: synced %d events (%d inserted, %d pages), cursor=%s",
                len(rows), inserted, page_count, new_cursor,
            )

            return SyncResult(
                source=self.source_name,
                rows_synced=inserted,
                cursor=new_cursor,
            )

        except Exception as exc:
            logger.warning("posthog_connector: unexpected error — %s", exc)
            return SyncResult(
                source=self.source_name,
                rows_synced=0,
                cursor=since_cursor,
                error=f"Unexpected error: {exc}",
            )


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _event_to_row(event: dict) -> dict:
    """Convert a PostHog event dict to a user_events row."""
    event_id = str(event.get("id", "") or event.get("uuid", ""))
    event_name = event.get("event", "unknown")
    user_id = (
        event.get("distinct_id", "")
        or event.get("person", {}).get("distinct_ids", [""])[0]
        if isinstance(event.get("person"), dict)
        else event.get("person", "") or ""
    )

    # Normalize timestamp
    ts = event.get("timestamp", "") or "1970-01-01T00:00:00Z"
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        occurred_at = dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        occurred_at = "1970-01-01 00:00:00"

    # Build compact properties (exclude PII-heavy or very large fields)
    raw_properties = event.get("properties", {}) or {}
    properties = json.dumps({
        k: v for k, v in raw_properties.items()
        if k not in ("$ip", "$user_agent", "$raw_user_agent")
        and not k.startswith("$performance_")
    })

    return {
        "id": event_id,
        "source": "posthog",
        "event_name": event_name,
        "user_id": str(user_id) if user_id else "",
        "properties": properties,
        "occurred_at": occurred_at,
    }


# ─────────────────────────────────────────────────────────────
# Smoke test
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    connector = PostHogConnector()
    print(f"Configured: {connector.is_configured()}")
    if connector.is_configured():
        result = connector.sync()
        print(f"Sync result: {result}")
    else:
        print("Set POSTHOG_API_KEY and install httpx to run sync.")
