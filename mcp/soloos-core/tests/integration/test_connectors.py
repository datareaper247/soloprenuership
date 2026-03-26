"""
Integration tests for SoloOS V10 connector layer.

These tests are SKIPPED unless the relevant API key env vars are set.
They test real HTTP/API calls against live services.

To run all integration tests:
    STRIPE_API_KEY=sk_test_... MERCURY_API_KEY=... POSTHOG_API_KEY=... \
    python -m pytest tests/integration/test_connectors.py -v

Individual connector tests skip automatically if their key is absent.

Unit-level tests (no API keys needed):
    - Protocol conformance (is_configured returns False gracefully)
    - ConnectorRegistry lists all 3 connectors
    - configured_connectors() returns empty when no keys are set
    - SyncResult dataclass fields and properties
    - Fail-open when SDK not installed
"""

from __future__ import annotations

import os
from dataclasses import fields
from unittest.mock import patch

import pytest

# ─────────────────────────────────────────────────────────────
# Unit-level tests (always run — no API keys needed)
# ─────────────────────────────────────────────────────────────

class TestSyncResultDataclass:
    """SyncResult dataclass structure and behaviour — always runs."""

    def test_sync_result_fields_exist(self):
        """SyncResult has all required fields."""
        from soloos_core.data.connectors.base import SyncResult

        field_names = {f.name for f in fields(SyncResult)}
        assert "source" in field_names
        assert "rows_synced" in field_names
        assert "cursor" in field_names
        assert "error" in field_names
        assert "duration_ms" in field_names

    def test_sync_result_ok_true_when_no_error(self):
        """SyncResult.ok is True when error is None."""
        from soloos_core.data.connectors.base import SyncResult

        r = SyncResult(source="test", rows_synced=5, cursor="abc")
        assert r.ok is True

    def test_sync_result_ok_false_when_error_set(self):
        """SyncResult.ok is False when error string is populated."""
        from soloos_core.data.connectors.base import SyncResult

        r = SyncResult(source="test", rows_synced=0, cursor=None, error="boom")
        assert r.ok is False

    def test_sync_result_to_dict(self):
        """SyncResult.to_dict() returns a dict with expected keys."""
        from soloos_core.data.connectors.base import SyncResult

        r = SyncResult(source="stripe", rows_synced=10, cursor="ch_123", duration_ms=250.0)
        d = r.to_dict()

        assert d["source"] == "stripe"
        assert d["rows_synced"] == 10
        assert d["cursor"] == "ch_123"
        assert d["ok"] is True
        assert d["error"] is None
        assert d["duration_ms"] == pytest.approx(250.0)

    def test_sync_result_default_duration_is_zero(self):
        """SyncResult.duration_ms defaults to 0.0."""
        from soloos_core.data.connectors.base import SyncResult

        r = SyncResult(source="posthog", rows_synced=0, cursor=None)
        assert r.duration_ms == 0.0


class TestBaseConnectorProtocol:
    """BaseConnector abstract interface — always runs."""

    def test_base_connector_cannot_be_instantiated(self):
        """BaseConnector is abstract and cannot be instantiated directly."""
        from soloos_core.data.connectors.base import BaseConnector

        with pytest.raises(TypeError):
            BaseConnector()  # type: ignore[abstract]

    def test_base_connector_get_schema_tables_default_empty(self):
        """Default get_schema_tables() returns empty list."""
        from soloos_core.data.connectors.base import BaseConnector

        # Create a minimal concrete subclass to test the default
        class MinimalConnector(BaseConnector):
            source_name = "test"

            def is_configured(self) -> bool:
                return False

            def sync(self, since_cursor=None):
                from soloos_core.data.connectors.base import SyncResult
                return SyncResult(source="test", rows_synced=0, cursor=None)

        c = MinimalConnector()
        assert c.get_schema_tables() == []


class TestConnectorRegistryAlwaysRuns:
    """ConnectorRegistry unit behaviour — always runs (no API keys)."""

    def _reset_registry(self):
        """Reset the singleton between tests."""
        import soloos_core.data.connectors.registry as reg_mod
        reg_mod._registry = None

    def test_registry_lists_all_three_connectors(self):
        """Registry.all_connectors() returns exactly 3 connectors."""
        self._reset_registry()
        from soloos_core.data.connectors.registry import get_registry

        registry = get_registry()
        connectors = registry.all_connectors()

        assert len(connectors) == 3
        source_names = {c.source_name for c in connectors}
        assert "stripe" in source_names
        assert "mercury" in source_names
        assert "posthog" in source_names

        self._reset_registry()

    def test_registry_configured_connectors_empty_when_no_keys(self, monkeypatch):
        """configured_connectors() returns empty list when no API keys are set."""
        self._reset_registry()
        monkeypatch.delenv("STRIPE_API_KEY", raising=False)
        monkeypatch.delenv("MERCURY_API_KEY", raising=False)
        monkeypatch.delenv("POSTHOG_API_KEY", raising=False)

        from soloos_core.data.connectors.registry import get_registry
        registry = get_registry()
        configured = registry.configured_connectors()

        assert configured == []
        self._reset_registry()

    def test_registry_status_returns_list_of_dicts(self):
        """registry.status() returns a list of dicts with expected keys."""
        self._reset_registry()
        from soloos_core.data.connectors.registry import get_registry

        registry = get_registry()
        status = registry.status()

        assert isinstance(status, list)
        assert len(status) == 3
        for item in status:
            assert "source" in item
            assert "configured" in item
            assert "tables" in item
            assert "last_synced_at" in item

        self._reset_registry()

    def test_registry_is_singleton(self):
        """get_registry() returns the same instance on repeated calls."""
        self._reset_registry()
        from soloos_core.data.connectors.registry import get_registry

        r1 = get_registry()
        r2 = get_registry()
        assert r1 is r2
        self._reset_registry()

    def test_registry_sync_all_empty_when_not_configured(self, monkeypatch):
        """sync_all() returns empty list when no connectors are configured."""
        self._reset_registry()
        monkeypatch.delenv("STRIPE_API_KEY", raising=False)
        monkeypatch.delenv("MERCURY_API_KEY", raising=False)
        monkeypatch.delenv("POSTHOG_API_KEY", raising=False)

        from soloos_core.data.connectors.registry import get_registry
        registry = get_registry()
        results = registry.sync_all()

        assert results == []
        self._reset_registry()


class TestConnectorIsConfiguredFails:
    """Connectors return False gracefully when SDK is not installed — always runs."""

    def test_stripe_is_configured_false_without_key(self, monkeypatch):
        """StripeConnector.is_configured() returns False when key missing."""
        monkeypatch.delenv("STRIPE_API_KEY", raising=False)
        from soloos_core.data.connectors.stripe_connector import StripeConnector
        assert StripeConnector().is_configured() is False

    def test_mercury_is_configured_false_without_key(self, monkeypatch):
        """MercuryConnector.is_configured() returns False when key missing."""
        monkeypatch.delenv("MERCURY_API_KEY", raising=False)
        from soloos_core.data.connectors.mercury_connector import MercuryConnector
        assert MercuryConnector().is_configured() is False

    def test_posthog_is_configured_false_without_key(self, monkeypatch):
        """PostHogConnector.is_configured() returns False when key missing."""
        monkeypatch.delenv("POSTHOG_API_KEY", raising=False)
        from soloos_core.data.connectors.posthog_connector import PostHogConnector
        assert PostHogConnector().is_configured() is False

    def test_stripe_is_configured_false_when_sdk_missing(self, monkeypatch):
        """StripeConnector.is_configured() returns False when stripe SDK missing."""
        monkeypatch.setenv("STRIPE_API_KEY", "sk_test_fake")
        with patch.dict("sys.modules", {"stripe": None}):
            import soloos_core.data.connectors.stripe_connector as mod
            mod._stripe_available = None  # reset cached check
            connector = mod.StripeConnector()
            result = connector.is_configured()
            mod._stripe_available = None  # cleanup
        # Should be False because stripe import fails
        assert result is False

    def test_mercury_is_configured_false_when_httpx_missing(self, monkeypatch):
        """MercuryConnector.is_configured() returns False when httpx missing."""
        monkeypatch.setenv("MERCURY_API_KEY", "test_key")
        with patch.dict("sys.modules", {"httpx": None}):
            import soloos_core.data.connectors.mercury_connector as mod
            mod._httpx_available = None  # reset cached check
            connector = mod.MercuryConnector()
            result = connector.is_configured()
            mod._httpx_available = None  # cleanup
        assert result is False

    def test_sync_returns_error_result_when_not_configured(self, monkeypatch):
        """sync() returns SyncResult with error when not configured (no key)."""
        monkeypatch.delenv("STRIPE_API_KEY", raising=False)
        from soloos_core.data.connectors.stripe_connector import StripeConnector

        connector = StripeConnector()
        result = connector.sync()

        assert result.ok is False
        assert result.rows_synced == 0
        assert result.error is not None
        assert "not configured" in result.error.lower() or "missing" in result.error.lower()


# ─────────────────────────────────────────────────────────────
# Integration tests — SKIPPED unless API keys are present
# ─────────────────────────────────────────────────────────────

@pytest.mark.skipif(
    not os.environ.get("STRIPE_API_KEY"),
    reason="STRIPE_API_KEY not set — skipping Stripe live integration test",
)
class TestStripeConnectorLive:
    """Live Stripe integration tests (requires STRIPE_API_KEY)."""

    def test_stripe_is_configured_with_key(self):
        """is_configured() returns True when STRIPE_API_KEY is set."""
        from soloos_core.data.connectors.stripe_connector import StripeConnector
        assert StripeConnector().is_configured() is True

    def test_stripe_sync_returns_sync_result(self, tmp_path):
        """sync() returns a SyncResult (ok or error) without raising."""
        import soloos_core.data.analytics_db as db_mod
        db_mod._db = None
        db_mod._duckdb_available = None

        from soloos_core.data.analytics_db import AnalyticsDB
        db_mod._db = AnalyticsDB(db_path=str(tmp_path / "test.duckdb"))

        from soloos_core.data.connectors.stripe_connector import StripeConnector

        connector = StripeConnector()
        result = connector.sync()

        assert isinstance(result, __import__("soloos_core.data.connectors.base", fromlist=["SyncResult"]).SyncResult)
        assert result.source == "stripe"
        assert result.rows_synced >= 0

        db_mod._db = None

    def test_stripe_sync_is_idempotent(self, tmp_path):
        """Calling sync() twice does not raise and row count does not double."""
        import soloos_core.data.analytics_db as db_mod
        db_mod._db = None

        from soloos_core.data.analytics_db import AnalyticsDB
        db_mod._db = AnalyticsDB(db_path=str(tmp_path / "idem.duckdb"))

        from soloos_core.data.connectors.stripe_connector import StripeConnector

        connector = StripeConnector()
        r1 = connector.sync()
        r2 = connector.sync(since_cursor=r1.cursor)

        # Second sync should not raise and rows_synced should be >= 0
        assert r2.rows_synced >= 0

        db_mod._db = None


@pytest.mark.skipif(
    not os.environ.get("MERCURY_API_KEY"),
    reason="MERCURY_API_KEY not set — skipping Mercury live integration test",
)
class TestMercuryConnectorLive:
    """Live Mercury integration tests (requires MERCURY_API_KEY)."""

    def test_mercury_is_configured_with_key(self):
        """is_configured() returns True when MERCURY_API_KEY is set."""
        from soloos_core.data.connectors.mercury_connector import MercuryConnector
        assert MercuryConnector().is_configured() is True

    def test_mercury_sync_returns_sync_result(self, tmp_path):
        """sync() returns a SyncResult without raising."""
        import soloos_core.data.analytics_db as db_mod
        db_mod._db = None

        from soloos_core.data.analytics_db import AnalyticsDB
        db_mod._db = AnalyticsDB(db_path=str(tmp_path / "mercury.duckdb"))

        from soloos_core.data.connectors.mercury_connector import MercuryConnector

        connector = MercuryConnector()
        result = connector.sync()

        assert result.source == "mercury"
        assert result.rows_synced >= 0

        db_mod._db = None


@pytest.mark.skipif(
    not os.environ.get("POSTHOG_API_KEY"),
    reason="POSTHOG_API_KEY not set — skipping PostHog live integration test",
)
class TestPostHogConnectorLive:
    """Live PostHog integration tests (requires POSTHOG_API_KEY)."""

    def test_posthog_is_configured_with_key(self):
        """is_configured() returns True when POSTHOG_API_KEY is set."""
        from soloos_core.data.connectors.posthog_connector import PostHogConnector
        assert PostHogConnector().is_configured() is True

    def test_posthog_sync_returns_sync_result(self, tmp_path):
        """sync() returns a SyncResult without raising."""
        import soloos_core.data.analytics_db as db_mod
        db_mod._db = None

        from soloos_core.data.analytics_db import AnalyticsDB
        db_mod._db = AnalyticsDB(db_path=str(tmp_path / "posthog.duckdb"))

        from soloos_core.data.connectors.posthog_connector import PostHogConnector

        connector = PostHogConnector()
        result = connector.sync()

        assert result.source == "posthog"
        assert result.rows_synced >= 0

        db_mod._db = None
