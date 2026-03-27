"""
Customer support reply action.
Config:
    INTERCOM_TOKEN for Intercom
    CRISP_WEBSITE_ID + CRISP_TOKEN for Crisp
Dep: httpx (lazy)
Daily limit: 100 replies (enforced by ActionRegistry)
"""

from __future__ import annotations

import logging
import os

from .base_action import BaseAction, ActionOutcome

logger = logging.getLogger(__name__)


class SupportAction(BaseAction):
    action_name = "reply_support"

    def is_configured(self) -> bool:
        has_intercom = bool(os.environ.get("INTERCOM_TOKEN"))
        has_crisp = bool(os.environ.get("CRISP_WEBSITE_ID") and os.environ.get("CRISP_TOKEN"))
        return has_intercom or has_crisp

    def validate_params(self, params: dict) -> str | None:
        if not params.get("conversation_id"):
            return "Missing required param: conversation_id"
        if not params.get("message"):
            return "Missing required param: message"
        return None

    def execute(self, params: dict) -> ActionOutcome:
        err = self.validate_params(params)
        if err:
            return ActionOutcome(success=False, data={}, error=err)

        if not self.is_configured():
            return ActionOutcome(
                success=False,
                data={},
                error="SupportAction not configured: INTERCOM_TOKEN or CRISP_WEBSITE_ID+CRISP_TOKEN missing",
            )

        try:
            import httpx  # type: ignore[import]
        except ImportError:
            return ActionOutcome(success=False, data={}, error="httpx not installed")

        try:
            provider = params.get("provider", "auto")
            if provider == "crisp" or (provider == "auto" and os.environ.get("CRISP_WEBSITE_ID")):
                return self._reply_crisp(httpx, params)
            return self._reply_intercom(httpx, params)
        except Exception as exc:
            logger.warning("SupportAction failed: %s", exc)
            return ActionOutcome(success=False, data={}, error=str(exc))

    def _reply_intercom(self, httpx, params: dict) -> ActionOutcome:
        token = os.environ["INTERCOM_TOKEN"]
        conv_id = params["conversation_id"]
        message = params["message"]

        resp = httpx.post(
            f"https://api.intercom.io/conversations/{conv_id}/reply",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json={"message_type": "comment", "type": "admin", "body": message},
            timeout=15,
        )
        if resp.status_code >= 400:
            return ActionOutcome(success=False, data={}, error=f"Intercom error {resp.status_code}: {resp.text[:200]}")
        return ActionOutcome(success=True, data={"provider": "intercom", "conversation_id": conv_id})

    def _reply_crisp(self, httpx, params: dict) -> ActionOutcome:
        import base64
        website_id = os.environ["CRISP_WEBSITE_ID"]
        token = os.environ["CRISP_TOKEN"]
        session_id = params["conversation_id"]
        message = params["message"]

        creds = base64.b64encode(token.encode()).decode()
        resp = httpx.post(
            f"https://api.crisp.chat/v1/website/{website_id}/conversation/{session_id}/message",
            headers={
                "Authorization": f"Basic {creds}",
                "Content-Type": "application/json",
            },
            json={"type": "text", "from": "operator", "origin": "chat", "content": message},
            timeout=15,
        )
        if resp.status_code >= 400:
            return ActionOutcome(success=False, data={}, error=f"Crisp error {resp.status_code}: {resp.text[:200]}")
        return ActionOutcome(success=True, data={"provider": "crisp", "session_id": session_id})
