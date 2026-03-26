"""
SoloOS V10 — ConnectorRegistry

Discovers all available connectors, reports their configuration status,
and orchestrates sync_all() for the scheduler's data_sync_job.

Usage:
    from soloos_core.data.connectors.registry import get_registry

    registry = get_registry()

    # Check which connectors are ready
    for c in registry.configured_connectors():
        print(c.source_name, "is ready to sync")

    # Sync all configured connectors
    results = registry.sync_all()
    for r in results:
        print(r.source, r.rows_synced, r.error)

Env vars: none required directly — individual connectors read their own env vars.
"""

from __future__ import annotations

import logging
from typing import Optional

from .base import BaseConnector, SyncResult
from .stripe_connector import StripeConnector
from .mercury_connector import MercuryConnector
from .posthog_connector import PostHogConnector

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# ConnectorRegistry
# ─────────────────────────────────────────────────────────────

class ConnectorRegistry:
    """
    Central registry for all SoloOS data connectors.

    Connectors are instantiated once at registry creation time.
    The registry is a singleton — use get_registry() to obtain it.
    """

    def __init__(self) -> None:
        self._connectors: list[BaseConnector] = [
            StripeConnector(),
            MercuryConnector(),
            PostHogConnector(),
        ]

    def all_connectors(self) -> list[BaseConnector]:
        """Return all registered connectors (configured or not)."""
        return list(self._connectors)

    def configured_connectors(self) -> list[BaseConnector]:
        """
        Return only connectors that are fully configured (env vars set + SDK installed).
        Never raises — connectors with errors are silently excluded.
        """
        result = []
        for connector in self._connectors:
            try:
                if connector.is_configured():
                    result.append(connector)
            except Exception as exc:
                logger.warning(
                    "registry: is_configured() raised for %s — %s",
                    getattr(connector, "source_name", "unknown"),
                    exc,
                )
        return result

    def sync_all(self) -> list[SyncResult]:
        """
        Sync all configured connectors sequentially.

        Uses each connector's _timed_sync() so duration_ms is populated.
        Reads last cursor from AnalyticsDB sync_state table for incremental syncs.
        Never raises — errors are captured in SyncResult.error.

        Returns:
            List of SyncResult, one per configured connector.
            Empty list if no connectors are configured.
        """
        from soloos_core.data.analytics_db import get_analytics_db

        results: list[SyncResult] = []
        db = get_analytics_db()

        for connector in self.configured_connectors():
            source = connector.source_name
            try:
                # Load last cursor from sync_state for incremental sync
                state = db.get_sync_state(source)
                last_cursor: Optional[str] = state.get("last_cursor") if state else None

                logger.info("registry: syncing %s (cursor=%s)", source, last_cursor)
                result = connector._timed_sync(since_cursor=last_cursor)
                results.append(result)

                if result.ok:
                    logger.info(
                        "registry: %s sync complete — %d rows in %.0fms",
                        source, result.rows_synced, result.duration_ms,
                    )
                else:
                    logger.warning(
                        "registry: %s sync error — %s",
                        source, result.error,
                    )

            except Exception as exc:
                logger.warning("registry: sync crashed for %s — %s", source, exc)
                results.append(SyncResult(
                    source=source,
                    rows_synced=0,
                    cursor=None,
                    error=f"Registry sync crash: {exc}",
                ))

        return results

    def status(self) -> list[dict]:
        """
        Return a status dict for every connector including:
          - source_name
          - is_configured
          - tables it writes to
          - last_synced_at (from sync_state)
          - last_cursor
          - status

        Never raises.
        """
        from soloos_core.data.analytics_db import get_analytics_db
        db = get_analytics_db()

        result = []
        for connector in self._connectors:
            source = connector.source_name
            try:
                configured = connector.is_configured()
            except Exception:
                configured = False

            try:
                tables = connector.get_schema_tables()
            except Exception:
                tables = []

            try:
                state = db.get_sync_state(source) or {}
            except Exception:
                state = {}

            result.append({
                "source": source,
                "configured": configured,
                "tables": tables,
                "last_synced_at": state.get("last_synced_at"),
                "last_cursor": state.get("last_cursor"),
                "sync_status": state.get("status", "never_synced" if not state else "unknown"),
            })

        return result


# ─────────────────────────────────────────────────────────────
# Module-level singleton
# ─────────────────────────────────────────────────────────────

_registry: Optional[ConnectorRegistry] = None


def get_registry() -> ConnectorRegistry:
    """
    Return the module-level ConnectorRegistry singleton.
    Thread-safe for reads (registry is stateless between syncs).
    """
    global _registry
    if _registry is None:
        _registry = ConnectorRegistry()
    return _registry


# ─────────────────────────────────────────────────────────────
# Smoke test
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    registry = get_registry()
    print("=== connector registry smoke test ===")
    print(f"All connectors   : {[c.source_name for c in registry.all_connectors()]}")
    print(f"Configured       : {[c.source_name for c in registry.configured_connectors()]}")
    print(f"Status           :")
    print(json.dumps(registry.status(), indent=2, default=str))
    print("=== done ===")
