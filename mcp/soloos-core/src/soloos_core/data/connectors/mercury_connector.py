"""
SoloOS V10 — Mercury Banking Connector

Syncs Mercury bank account balances and transactions to the DuckDB
banking_events table.

Env vars required:
    MERCURY_API_KEY — Mercury API key (from mercury.com → Settings → API)

Optional:
    (none)

Mercury API base: https://api.mercury.com/api/v1
Endpoints used:
    GET /accounts                         — list accounts + balances
    GET /account/{account_id}/transactions — paginated transactions

Writes to: banking_events table (created inline on first sync if not present).
Idempotent: duplicate transaction IDs silently ignored via ON CONFLICT DO NOTHING.

SDK:
    httpx>=0.27.0  (optional dep — install with pip install 'soloos-core[connectors]')
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

_MERCURY_BASE = "https://api.mercury.com/api/v1"

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
# Schema for banking_events table
# ─────────────────────────────────────────────────────────────

_BANKING_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS banking_events (
    id VARCHAR PRIMARY KEY,
    source VARCHAR NOT NULL DEFAULT 'mercury',
    account_id VARCHAR NOT NULL,
    event_type VARCHAR NOT NULL,
    amount_cents INTEGER,
    currency VARCHAR DEFAULT 'usd',
    direction VARCHAR,
    counterparty_name VARCHAR,
    description VARCHAR,
    status VARCHAR,
    metadata JSON,
    occurred_at TIMESTAMP NOT NULL,
    synced_at TIMESTAMP DEFAULT current_timestamp
);
"""

_ACCOUNT_BALANCE_SQL = """
CREATE TABLE IF NOT EXISTS banking_balances (
    account_id VARCHAR PRIMARY KEY,
    account_name VARCHAR,
    current_balance_cents INTEGER,
    available_balance_cents INTEGER,
    currency VARCHAR DEFAULT 'usd',
    account_type VARCHAR,
    synced_at TIMESTAMP DEFAULT current_timestamp
);
"""


# ─────────────────────────────────────────────────────────────
# MercuryConnector
# ─────────────────────────────────────────────────────────────

class MercuryConnector(BaseConnector):
    """
    Syncs Mercury bank transactions to banking_events table in DuckDB.

    Creates the banking_events and banking_balances tables on first use.
    Uses httpx for HTTP requests (no official Mercury SDK).
    """

    source_name = "mercury"

    def is_configured(self) -> bool:
        """Return True only if MERCURY_API_KEY is set AND httpx is installed."""
        try:
            return bool(os.environ.get("MERCURY_API_KEY")) and _check_httpx()
        except Exception:
            return False

    def get_schema_tables(self) -> list[str]:
        return ["banking_events", "banking_balances"]

    def sync(self, since_cursor: Optional[str] = None) -> SyncResult:
        """
        Fetch Mercury account balances and transactions, write to DuckDB.

        Args:
            since_cursor: ISO date string (YYYY-MM-DD) for incremental sync.
                          None = fetch last 90 days of transactions.

        Returns:
            SyncResult with rows_synced, new cursor (latest transaction date),
            and optional error.
        """
        if not self.is_configured():
            return SyncResult(
                source=self.source_name,
                rows_synced=0,
                cursor=since_cursor,
                error="Mercury not configured: MERCURY_API_KEY missing or httpx not installed",
            )

        try:
            import httpx
            from soloos_core.data.analytics_db import get_analytics_db

            api_key = os.environ["MERCURY_API_KEY"]
            db = get_analytics_db()

            # Ensure banking tables exist
            _ensure_banking_tables(db)

            headers = {"Authorization": f"Bearer {api_key}"}
            rows: list[dict] = []
            new_cursor = since_cursor

            # ── Step 1: Fetch accounts + balances ────────────────────
            balance_rows: list[dict] = []
            try:
                with httpx.Client(timeout=30.0) as client:
                    resp = client.get(f"{_MERCURY_BASE}/accounts", headers=headers)
                    resp.raise_for_status()
                    accounts_data = resp.json()
                    accounts = accounts_data.get("accounts", [])

                    for acct in accounts:
                        balance_rows.append(_account_to_balance_row(acct))

                    # ── Step 2: Fetch transactions per account ────────
                    start_date = since_cursor or (
                        datetime.now(timezone.utc) - timedelta(days=90)
                    ).strftime("%Y-%m-%d")

                    for acct in accounts:
                        acct_id = acct.get("id", "")
                        if not acct_id:
                            continue

                        offset = 0
                        limit = 100
                        has_more = True

                        while has_more:
                            txn_resp = client.get(
                                f"{_MERCURY_BASE}/account/{acct_id}/transactions",
                                headers=headers,
                                params={
                                    "limit": limit,
                                    "offset": offset,
                                    "start": start_date,
                                },
                            )
                            txn_resp.raise_for_status()
                            txn_data = txn_resp.json()
                            transactions = txn_data.get("transactions", [])

                            for txn in transactions:
                                row = _transaction_to_row(txn, acct_id)
                                rows.append(row)
                                # Track most recent transaction date as cursor
                                txn_date = txn.get("postedAt", txn.get("createdAt", ""))
                                if txn_date and (new_cursor is None or txn_date > new_cursor):
                                    new_cursor = txn_date[:10]  # YYYY-MM-DD

                            if len(transactions) < limit:
                                has_more = False
                            else:
                                offset += limit

            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                if status_code == 401:
                    return SyncResult(
                        source=self.source_name,
                        rows_synced=0,
                        cursor=since_cursor,
                        error="Mercury authentication failed: invalid API key",
                    )
                return SyncResult(
                    source=self.source_name,
                    rows_synced=0,
                    cursor=since_cursor,
                    error=f"Mercury API HTTP {status_code}: {exc}",
                )
            except httpx.RequestError as exc:
                return SyncResult(
                    source=self.source_name,
                    rows_synced=0,
                    cursor=since_cursor,
                    error=f"Mercury network error: {exc}",
                )

            # Write balances (upsert)
            if balance_rows and db._ensure_conn():
                for br in balance_rows:
                    try:
                        db._conn.execute(
                            """
                            INSERT INTO banking_balances
                                (account_id, account_name, current_balance_cents,
                                 available_balance_cents, currency, account_type, synced_at)
                            VALUES (?, ?, ?, ?, ?, ?, current_timestamp)
                            ON CONFLICT (account_id) DO UPDATE SET
                                current_balance_cents = excluded.current_balance_cents,
                                available_balance_cents = excluded.available_balance_cents,
                                synced_at = excluded.synced_at
                            """,
                            [
                                br["account_id"], br["account_name"],
                                br["current_balance_cents"], br["available_balance_cents"],
                                br["currency"], br["account_type"],
                            ],
                        )
                    except Exception as exc:
                        logger.warning("mercury_connector: balance upsert failed — %s", exc)

            # Write transactions
            inserted = db.insert_events("banking_events", rows) if rows else 0

            # Update sync state
            if new_cursor:
                db.update_sync_state(self.source_name, new_cursor)

            logger.info(
                "mercury_connector: synced %d transactions (%d inserted), cursor=%s",
                len(rows), inserted, new_cursor,
            )

            return SyncResult(
                source=self.source_name,
                rows_synced=inserted,
                cursor=new_cursor,
            )

        except Exception as exc:
            logger.warning("mercury_connector: unexpected error — %s", exc)
            return SyncResult(
                source=self.source_name,
                rows_synced=0,
                cursor=since_cursor,
                error=f"Unexpected error: {exc}",
            )


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _ensure_banking_tables(db) -> None:
    """Create banking_events and banking_balances tables if they don't exist."""
    if not db._ensure_conn():
        return
    try:
        db._conn.execute(_BANKING_TABLE_SQL)
        db._conn.execute(_ACCOUNT_BALANCE_SQL)
    except Exception as exc:
        logger.warning("mercury_connector: could not create banking tables — %s", exc)


def _account_to_balance_row(acct: dict) -> dict:
    """Convert Mercury account dict to a banking_balances row."""
    balance = acct.get("currentBalance", 0.0) or 0.0
    available = acct.get("availableBalance", balance) or balance

    return {
        "account_id": acct.get("id", ""),
        "account_name": acct.get("name", ""),
        "current_balance_cents": int(balance * 100),
        "available_balance_cents": int(available * 100),
        "currency": acct.get("currency", "USD").lower(),
        "account_type": acct.get("type", ""),
    }


def _transaction_to_row(txn: dict, account_id: str) -> dict:
    """Convert a Mercury transaction dict to a banking_events row."""
    txn_id = txn.get("id", "")
    amount = txn.get("amount", 0.0) or 0.0
    currency = txn.get("currency", "USD") or "USD"

    # Mercury uses "credit"/"debit" direction
    direction = txn.get("direction", "")

    # Signed amount: credit = positive (money in), debit = negative (money out)
    amount_cents = int(amount * 100)
    if direction == "debit":
        amount_cents = -abs(amount_cents)

    occurred_at = txn.get("postedAt") or txn.get("createdAt") or "1970-01-01T00:00:00Z"
    # Normalize to "YYYY-MM-DD HH:MM:SS"
    try:
        dt = datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
        occurred_at = dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        occurred_at = "1970-01-01 00:00:00"

    counterparty = txn.get("counterpartyName", "") or ""
    description = txn.get("note", "") or txn.get("externalMemo", "") or ""
    status = txn.get("status", "")

    metadata = json.dumps({
        "counterparty_id": txn.get("counterpartyId", ""),
        "bank_description": txn.get("bankDescription", ""),
        "reason_for_failure": txn.get("reasonForFailure", ""),
        "kind": txn.get("kind", ""),
    })

    return {
        "id": txn_id,
        "source": "mercury",
        "account_id": account_id,
        "event_type": f"transaction.{direction or 'unknown'}",
        "amount_cents": amount_cents,
        "currency": currency.lower(),
        "direction": direction,
        "counterparty_name": counterparty,
        "description": description,
        "status": status,
        "metadata": metadata,
        "occurred_at": occurred_at,
    }


# ─────────────────────────────────────────────────────────────
# Smoke test
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    connector = MercuryConnector()
    print(f"Configured: {connector.is_configured()}")
    if connector.is_configured():
        result = connector.sync()
        print(f"Sync result: {result}")
    else:
        print("Set MERCURY_API_KEY and install httpx to run sync.")
