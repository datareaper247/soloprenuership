"""
DNS management via Cloudflare API.
Config: CLOUDFLARE_TOKEN + CLOUDFLARE_ZONE_ID
Dep: httpx (lazy)
Creates: A records, CNAME records, TXT records
"""

from __future__ import annotations

import logging
import os

from .base_action import BaseAction, ActionOutcome

logger = logging.getLogger(__name__)

_VALID_TYPES = ("A", "CNAME", "TXT", "MX", "AAAA")


class DnsAction(BaseAction):
    action_name = "manage_dns"

    def is_configured(self) -> bool:
        return bool(os.environ.get("CLOUDFLARE_TOKEN") and os.environ.get("CLOUDFLARE_ZONE_ID"))

    def validate_params(self, params: dict) -> str | None:
        record_type = params.get("type", "").upper()
        if record_type not in _VALID_TYPES:
            return f"Missing or invalid param: type. Must be one of {_VALID_TYPES}"
        if not params.get("name"):
            return "Missing required param: name"
        if not params.get("content"):
            return "Missing required param: content"
        return None

    def execute(self, params: dict) -> ActionOutcome:
        err = self.validate_params(params)
        if err:
            return ActionOutcome(success=False, data={}, error=err)

        if not self.is_configured():
            return ActionOutcome(
                success=False,
                data={},
                error="DnsAction not configured: CLOUDFLARE_TOKEN + CLOUDFLARE_ZONE_ID required",
            )

        try:
            import httpx  # type: ignore[import]
        except ImportError:
            return ActionOutcome(success=False, data={}, error="httpx not installed")

        try:
            token = os.environ["CLOUDFLARE_TOKEN"]
            zone_id = os.environ["CLOUDFLARE_ZONE_ID"]

            operation = params.get("operation", "create")  # create|update|delete

            if operation == "delete":
                return self._delete_record(httpx, token, zone_id, params)
            return self._create_or_update_record(httpx, token, zone_id, params, operation)

        except Exception as exc:
            logger.warning("DnsAction failed: %s", exc)
            return ActionOutcome(success=False, data={}, error=str(exc))

    def _create_or_update_record(self, httpx, token: str, zone_id: str, params: dict, operation: str) -> ActionOutcome:
        payload = {
            "type": params["type"].upper(),
            "name": params["name"],
            "content": params["content"],
            "ttl": params.get("ttl", 3600),
            "proxied": params.get("proxied", False),
        }

        resp = httpx.post(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload,
            timeout=15,
        )
        if resp.status_code >= 400:
            return ActionOutcome(success=False, data={}, error=f"Cloudflare error {resp.status_code}: {resp.text[:200]}")

        data = resp.json()
        record = data.get("result", {})
        return ActionOutcome(success=True, data={
            "record_id": record.get("id"),
            "name": record.get("name"),
            "type": record.get("type"),
            "content": record.get("content"),
        })

    def _delete_record(self, httpx, token: str, zone_id: str, params: dict) -> ActionOutcome:
        record_id = params.get("record_id")
        if not record_id:
            return ActionOutcome(success=False, data={}, error="record_id required for delete operation")

        resp = httpx.delete(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        if resp.status_code >= 400:
            return ActionOutcome(success=False, data={}, error=f"Cloudflare delete error {resp.status_code}")
        return ActionOutcome(success=True, data={"deleted_id": record_id})
