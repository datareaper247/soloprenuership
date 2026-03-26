"""
SoloOS V10 — Stripe Connector

Syncs Stripe charge events to the DuckDB revenue_events table.

Env vars required:
    STRIPE_API_KEY — Stripe secret key (sk_live_... or sk_test_...)

Optional:
    (none)

Behavior:
    - On first sync (no cursor): fetches charges from the last 90 days.
    - On incremental sync: uses starting_after cursor (last charge ID seen).
    - Computes mrr_delta_cents per charge:
        charge.succeeded  → +amount (new revenue signal)
        customer.subscription.deleted → -ARPU (churn signal, estimated as avg charge)
    - Writes to: revenue_events table in AnalyticsDB.
    - Idempotent: duplicate charge IDs are ignored via ON CONFLICT DO NOTHING.

SDK:
    stripe>=7.0.0  (optional dep — install with pip install 'soloos-core[connectors]')
    If not installed, is_configured() returns False and sync() returns error SyncResult.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from .base import BaseConnector, SyncResult

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# SDK availability (lazy, fail-open)
# ─────────────────────────────────────────────────────────────

_stripe_available: Optional[bool] = None


def _check_stripe() -> bool:
    global _stripe_available
    if _stripe_available is None:
        try:
            import stripe  # noqa: F401
            _stripe_available = True
        except ImportError:
            _stripe_available = False
    return _stripe_available


# ─────────────────────────────────────────────────────────────
# StripeConnector
# ─────────────────────────────────────────────────────────────

class StripeConnector(BaseConnector):
    """
    Syncs Stripe charges to revenue_events table in DuckDB.

    Reads STRIPE_API_KEY from environment. Falls back gracefully when
    the stripe SDK is not installed or the key is absent.
    """

    source_name = "stripe"

    def is_configured(self) -> bool:
        """Return True only if STRIPE_API_KEY is set AND stripe SDK is installed."""
        try:
            return bool(os.environ.get("STRIPE_API_KEY")) and _check_stripe()
        except Exception:
            return False

    def get_schema_tables(self) -> list[str]:
        return ["revenue_events"]

    def sync(self, since_cursor: Optional[str] = None) -> SyncResult:
        """
        Fetch charges from Stripe and upsert into revenue_events.

        Args:
            since_cursor: Last charge ID from previous sync (starting_after param).
                          None = fetch last 90 days of charges.

        Returns:
            SyncResult with rows_synced, new cursor (last charge ID), and optional error.
        """
        if not self.is_configured():
            return SyncResult(
                source=self.source_name,
                rows_synced=0,
                cursor=since_cursor,
                error="Stripe not configured: STRIPE_API_KEY missing or stripe SDK not installed",
            )

        try:
            import stripe
            from soloos_core.data.analytics_db import get_analytics_db

            stripe.api_key = os.environ["STRIPE_API_KEY"]
            db = get_analytics_db()

            rows: list[dict] = []
            new_cursor: Optional[str] = since_cursor
            has_more = True
            page_cursor: Optional[str] = since_cursor

            # On first sync, fetch last 90 days
            created_gte: Optional[int] = None
            if since_cursor is None:
                cutoff = datetime.now(timezone.utc) - timedelta(days=90)
                created_gte = int(cutoff.timestamp())

            while has_more:
                params: dict = {"limit": 100}
                if page_cursor:
                    params["starting_after"] = page_cursor
                elif created_gte is not None:
                    params["created"] = {"gte": created_gte}

                try:
                    response = stripe.Charge.list(**params)
                except stripe.error.AuthenticationError as exc:
                    return SyncResult(
                        source=self.source_name,
                        rows_synced=0,
                        cursor=since_cursor,
                        error=f"Stripe authentication failed: {exc}",
                    )
                except stripe.error.StripeError as exc:
                    return SyncResult(
                        source=self.source_name,
                        rows_synced=0,
                        cursor=since_cursor,
                        error=f"Stripe API error: {exc}",
                    )

                charges = response.get("data", [])
                has_more = response.get("has_more", False)

                for charge in charges:
                    row = _charge_to_row(charge)
                    rows.append(row)
                    # Cursor advances to most-recently seen charge ID
                    if new_cursor is None or charge["id"] > (new_cursor or ""):
                        new_cursor = charge["id"]

                # Advance page cursor for next page
                if charges:
                    page_cursor = charges[-1]["id"]
                else:
                    has_more = False

            # Write to DuckDB
            inserted = db.insert_events("revenue_events", rows) if rows else 0

            # Update sync state
            if new_cursor:
                db.update_sync_state(self.source_name, new_cursor)

            logger.info(
                "stripe_connector: synced %d charges (%d inserted), cursor=%s",
                len(rows), inserted, new_cursor,
            )

            return SyncResult(
                source=self.source_name,
                rows_synced=inserted,
                cursor=new_cursor,
            )

        except Exception as exc:
            logger.warning("stripe_connector: unexpected error — %s", exc)
            return SyncResult(
                source=self.source_name,
                rows_synced=0,
                cursor=since_cursor,
                error=f"Unexpected error: {exc}",
            )


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _charge_to_row(charge: dict) -> dict:
    """
    Convert a Stripe Charge object to a revenue_events row dict.

    mrr_delta_cents logic:
      - succeeded charges contribute +amount_cents (new revenue signal)
      - failed/refunded charges contribute 0 (not yet churned-subscriber signal)
    """
    charge_id = charge.get("id", "")
    amount = charge.get("amount", 0)
    currency = charge.get("currency", "usd")
    status = charge.get("status", "")
    customer_id = charge.get("customer", "") or ""
    created_ts = charge.get("created", 0)

    # Compute MRR delta: only count succeeded charges as positive MRR signal
    mrr_delta = amount if status == "succeeded" else 0

    # Convert unix timestamp to ISO string
    occurred_at = (
        datetime.fromtimestamp(created_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        if created_ts
        else "1970-01-01 00:00:00"
    )

    # Build compact metadata
    metadata = json.dumps({
        "status": status,
        "description": charge.get("description", ""),
        "payment_method_details": charge.get("payment_method_details", {}).get("type", ""),
        "invoice": charge.get("invoice", ""),
    })

    return {
        "id": charge_id,
        "source": "stripe",
        "event_type": f"charge.{status}",
        "customer_id": customer_id,
        "amount_cents": amount,
        "currency": currency,
        "mrr_delta_cents": mrr_delta,
        "metadata": metadata,
        "occurred_at": occurred_at,
    }


# ─────────────────────────────────────────────────────────────
# Smoke test
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    connector = StripeConnector()
    print(f"Configured: {connector.is_configured()}")
    if connector.is_configured():
        result = connector.sync()
        print(f"Sync result: {result}")
    else:
        print("Set STRIPE_API_KEY and install stripe SDK to run sync.")
