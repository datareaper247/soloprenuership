"""
Social media posting action.
Config:
    TWITTER_BEARER_TOKEN + TWITTER_API_KEY + TWITTER_API_SECRET + TWITTER_ACCESS_TOKEN + TWITTER_ACCESS_SECRET
    BUFFER_TOKEN (alternative — schedules posts)
Dep: httpx (lazy)
Daily limit: 3 posts per platform (enforced by ActionRegistry)
"""

from __future__ import annotations

import logging
import os

from .base_action import BaseAction, ActionOutcome

logger = logging.getLogger(__name__)


class SocialAction(BaseAction):
    action_name = "post_social"

    def is_configured(self) -> bool:
        has_twitter = bool(
            os.environ.get("TWITTER_API_KEY")
            and os.environ.get("TWITTER_API_SECRET")
            and os.environ.get("TWITTER_ACCESS_TOKEN")
            and os.environ.get("TWITTER_ACCESS_SECRET")
        )
        has_buffer = bool(os.environ.get("BUFFER_TOKEN"))
        return has_twitter or has_buffer

    def validate_params(self, params: dict) -> str | None:
        if not params.get("content"):
            return "Missing required param: content"
        if len(params["content"]) > 280 and params.get("platform", "twitter") == "twitter":
            return "Twitter content exceeds 280 characters"
        return None

    def execute(self, params: dict) -> ActionOutcome:
        err = self.validate_params(params)
        if err:
            return ActionOutcome(success=False, data={}, error=err)

        if not self.is_configured():
            return ActionOutcome(
                success=False,
                data={},
                error="SocialAction not configured: TWITTER_API_KEY or BUFFER_TOKEN missing",
            )

        platform = params.get("platform", "twitter")
        content = params["content"]

        try:
            import httpx  # type: ignore[import]
        except ImportError:
            return ActionOutcome(success=False, data={}, error="httpx not installed")

        try:
            if os.environ.get("BUFFER_TOKEN"):
                return self._post_buffer(httpx, content, platform)
            return self._post_twitter(httpx, content)
        except Exception as exc:
            logger.warning("SocialAction failed: %s", exc)
            return ActionOutcome(success=False, data={}, error=str(exc))

    def _post_twitter(self, httpx, content: str) -> ActionOutcome:
        import base64
        import hmac
        import hashlib
        import time
        import urllib.parse
        import uuid

        api_key = os.environ["TWITTER_API_KEY"]
        api_secret = os.environ["TWITTER_API_SECRET"]
        access_token = os.environ["TWITTER_ACCESS_TOKEN"]
        access_secret = os.environ["TWITTER_ACCESS_SECRET"]

        url = "https://api.twitter.com/2/tweets"
        oauth_ts = str(int(time.time()))
        oauth_nonce = uuid.uuid4().hex

        oauth_params = {
            "oauth_consumer_key": api_key,
            "oauth_nonce": oauth_nonce,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": oauth_ts,
            "oauth_token": access_token,
            "oauth_version": "1.0",
        }

        signing_key = f"{urllib.parse.quote(api_secret, safe='')}&{urllib.parse.quote(access_secret, safe='')}"
        base_str_params = "&".join(
            f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(v, safe='')}"
            for k, v in sorted(oauth_params.items())
        )
        base_string = f"POST&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(base_str_params, safe='')}"
        sig = base64.b64encode(
            hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
        ).decode()

        oauth_params["oauth_signature"] = sig
        auth_header = "OAuth " + ", ".join(
            f'{k}="{urllib.parse.quote(v, safe="")}"' for k, v in sorted(oauth_params.items())
        )

        resp = httpx.post(
            url,
            headers={"Authorization": auth_header, "Content-Type": "application/json"},
            json={"text": content},
            timeout=15,
        )
        if resp.status_code >= 400:
            return ActionOutcome(success=False, data={}, error=f"Twitter error {resp.status_code}: {resp.text[:200]}")

        data = resp.json()
        return ActionOutcome(success=True, data={"tweet_id": data.get("data", {}).get("id"), "platform": "twitter"})

    def _post_buffer(self, httpx, content: str, platform: str) -> ActionOutcome:
        token = os.environ["BUFFER_TOKEN"]
        resp = httpx.post(
            "https://api.bufferapp.com/1/updates/create.json",
            data={"text": content, "profile_ids[]": platform},
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        if resp.status_code >= 400:
            return ActionOutcome(success=False, data={}, error=f"Buffer error {resp.status_code}")
        return ActionOutcome(success=True, data={"platform": platform, "status": "scheduled"})
