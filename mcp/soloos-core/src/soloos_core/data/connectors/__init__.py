"""
SoloOS V10 — Data Connectors Package

Provides fail-open connectors for external data sources:
  - Stripe  (revenue events, MRR)
  - Mercury (bank balances, transactions)
  - PostHog (user events, retention)

All connectors implement BaseConnector and are fail-open:
if the required SDK is not installed or env vars are missing,
is_configured() returns False and sync() returns a SyncResult with an error.

Usage:
    from soloos_core.data.connectors import get_registry

    registry = get_registry()
    for result in registry.sync_all():
        print(result)
"""

from .base import BaseConnector, SyncResult
from .registry import ConnectorRegistry, get_registry

__all__ = [
    "BaseConnector",
    "SyncResult",
    "ConnectorRegistry",
    "get_registry",
]
