"""
SoloOS V10 — BaseConnector Protocol and SyncResult dataclass

All connectors in this package implement BaseConnector.

Rules every connector MUST follow:
  1. is_configured() — never raises; returns False if env vars are missing or
     the required SDK is not installed.
  2. sync() — never raises; returns SyncResult with error field populated on
     failure. Writes to AnalyticsDB using insert_events(). Idempotent.
  3. get_schema_tables() — returns the list of DuckDB table names the connector
     writes to (used by connector_status tool for diagnostics).

Env vars: connector-specific (see each subclass docstring).
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SyncResult:
    """
    Returned by BaseConnector.sync() after every sync attempt.

    Fields:
        source      — connector name (e.g. "stripe")
        rows_synced — number of rows successfully written to AnalyticsDB
        cursor      — pagination cursor for next incremental sync (None if full sync)
        error       — human-readable error string if sync partially or fully failed
        duration_ms — wall-clock time for the sync in milliseconds
    """

    source: str
    rows_synced: int
    cursor: Optional[str]
    error: Optional[str] = None
    duration_ms: float = 0.0

    @property
    def ok(self) -> bool:
        """True when there was no error."""
        return self.error is None

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "rows_synced": self.rows_synced,
            "cursor": self.cursor,
            "error": self.error,
            "duration_ms": round(self.duration_ms, 1),
            "ok": self.ok,
        }


class BaseConnector(ABC):
    """
    Abstract base for all SoloOS data connectors.

    Subclasses must set the class attribute `source_name` and implement
    `is_configured()` and `sync()`.
    """

    source_name: str = "unknown"

    @abstractmethod
    def is_configured(self) -> bool:
        """
        Return True only if all required env vars are set AND the required
        SDK/library is importable.

        Must never raise — return False on any exception.
        """

    @abstractmethod
    def sync(self, since_cursor: Optional[str] = None) -> SyncResult:
        """
        Fetch new events since `since_cursor` and write them to AnalyticsDB.

        Contract:
          - Must be idempotent: duplicate events are silently ignored via
            PRIMARY KEY conflict handling in AnalyticsDB.insert_events().
          - Must fail open: catch ALL exceptions and return a SyncResult
            with error= populated instead of raising.
          - Must update sync_state in AnalyticsDB on success.

        Args:
            since_cursor: Opaque pagination cursor from a previous SyncResult.
                          None means full historical sync (last 90 days).

        Returns:
            SyncResult with rows_synced, cursor, and optional error.
        """

    def get_schema_tables(self) -> list[str]:
        """
        Return the list of DuckDB table names this connector writes to.
        Used by connector_status for diagnostics.
        Override in subclasses.
        """
        return []

    def _timed_sync(self, since_cursor: Optional[str] = None) -> SyncResult:
        """
        Wrapper that calls sync() and populates duration_ms automatically.
        Use this in registry.sync_all() instead of calling sync() directly.
        """
        t0 = time.monotonic()
        result = self.sync(since_cursor=since_cursor)
        result.duration_ms = (time.monotonic() - t0) * 1000.0
        return result
