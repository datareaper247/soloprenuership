"""
Email action via Resend (https://resend.com).
Config: RESEND_API_KEY env var
Dep: resend>=2.0.0 (lazy import)

Usage:
    EmailAction().execute({
        "to": "customer@example.com",
        "from": "ai@yourcompany.com",
        "subject": "Re: your question",
        "body": "Hi ...",
        "reply_to": "support@yourcompany.com"
    })
"""

from __future__ import annotations

import logging
import os

from .base_action import BaseAction, ActionOutcome

logger = logging.getLogger(__name__)

_REQUIRED_PARAMS = ("to", "subject", "body")


class EmailAction(BaseAction):
    action_name = "send_email"

    def is_configured(self) -> bool:
        return bool(os.environ.get("RESEND_API_KEY"))

    def validate_params(self, params: dict) -> str | None:
        missing = [k for k in _REQUIRED_PARAMS if not params.get(k)]
        if missing:
            return f"Missing required params: {', '.join(missing)}"
        return None

    def execute(self, params: dict) -> ActionOutcome:
        err = self.validate_params(params)
        if err:
            return ActionOutcome(success=False, data={}, error=err)

        if not self.is_configured():
            return ActionOutcome(
                success=False,
                data={},
                error="EmailAction not configured: RESEND_API_KEY missing",
            )

        try:
            import resend  # type: ignore[import]

            api_key = os.environ["RESEND_API_KEY"]
            resend.api_key = api_key

            from_addr = params.get("from", os.environ.get("RESEND_FROM_EMAIL", "ai@example.com"))
            payload: dict = {
                "from": from_addr,
                "to": [params["to"]] if isinstance(params["to"], str) else params["to"],
                "subject": params["subject"],
                "html": params.get("html") or f"<p>{params['body']}</p>",
                "text": params.get("body"),
            }
            if params.get("reply_to"):
                payload["reply_to"] = params["reply_to"]

            result = resend.Emails.send(payload)
            return ActionOutcome(success=True, data={"id": result.get("id"), "status": "sent"})

        except ImportError:
            return ActionOutcome(
                success=False,
                data={},
                error="resend package not installed. Run: pip install 'soloos-core[actions]'",
            )
        except Exception as exc:
            logger.warning("EmailAction failed: %s", exc)
            return ActionOutcome(success=False, data={}, error=str(exc))
