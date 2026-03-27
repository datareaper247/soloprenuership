"""
Deploy action via Vercel API or Railway API.
Config:
    VERCEL_TOKEN + VERCEL_PROJECT_ID for Vercel
    RAILWAY_TOKEN + RAILWAY_PROJECT_ID for Railway
Dep: httpx>=0.27.0 (lazy import)

Supports:
    deploy_staging: always soft-approved
    deploy_production: requires approval (Tier 4)

Usage:
    DeployAction().execute({
        "target": "staging",   # or "production"
        "provider": "vercel",  # or "railway"
        "git_ref": "main"
    })
"""

from __future__ import annotations

import logging
import os

from .base_action import BaseAction, ActionOutcome

logger = logging.getLogger(__name__)


class DeployAction(BaseAction):
    action_name = "deploy"

    def is_configured(self) -> bool:
        has_vercel = bool(os.environ.get("VERCEL_TOKEN") and os.environ.get("VERCEL_PROJECT_ID"))
        has_railway = bool(os.environ.get("RAILWAY_TOKEN") and os.environ.get("RAILWAY_PROJECT_ID"))
        return has_vercel or has_railway

    def validate_params(self, params: dict) -> str | None:
        if not params.get("target"):
            return "Missing required param: target (staging|production)"
        if params["target"] not in ("staging", "production"):
            return f"Invalid target: {params['target']}. Must be 'staging' or 'production'"
        return None

    def execute(self, params: dict) -> ActionOutcome:
        err = self.validate_params(params)
        if err:
            return ActionOutcome(success=False, data={}, error=err)

        if not self.is_configured():
            return ActionOutcome(
                success=False,
                data={},
                error="DeployAction not configured: VERCEL_TOKEN+VERCEL_PROJECT_ID or RAILWAY_TOKEN+RAILWAY_PROJECT_ID missing",
            )

        provider = params.get("provider", "vercel")
        target = params["target"]
        git_ref = params.get("git_ref", "main")

        try:
            import httpx  # type: ignore[import]
        except ImportError:
            return ActionOutcome(
                success=False,
                data={},
                error="httpx package not installed. Run: pip install httpx",
            )

        try:
            if provider == "vercel":
                return self._deploy_vercel(httpx, target, git_ref)
            elif provider == "railway":
                return self._deploy_railway(httpx, target, git_ref)
            else:
                return ActionOutcome(success=False, data={}, error=f"Unknown provider: {provider}")
        except Exception as exc:
            logger.warning("DeployAction failed: %s", exc)
            return ActionOutcome(success=False, data={}, error=str(exc))

    def _deploy_vercel(self, httpx, target: str, git_ref: str) -> ActionOutcome:
        token = os.environ["VERCEL_TOKEN"]
        project_id = os.environ["VERCEL_PROJECT_ID"]

        resp = httpx.post(
            "https://api.vercel.com/v13/deployments",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={
                "name": project_id,
                "gitSource": {"type": "github", "ref": git_ref},
                "target": target,
            },
            timeout=30,
        )
        if resp.status_code >= 400:
            return ActionOutcome(success=False, data={}, error=f"Vercel API error {resp.status_code}: {resp.text[:200]}")

        data = resp.json()
        return ActionOutcome(success=True, data={
            "deployment_id": data.get("id"),
            "url": data.get("url"),
            "target": target,
            "provider": "vercel",
        })

    def _deploy_railway(self, httpx, target: str, git_ref: str) -> ActionOutcome:
        token = os.environ["RAILWAY_TOKEN"]
        project_id = os.environ["RAILWAY_PROJECT_ID"]

        resp = httpx.post(
            "https://backboard.railway.app/graphql/v2",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={
                "query": """
                    mutation Deploy($projectId: String!, $environmentName: String!) {
                        serviceInstanceDeploy(input: {
                            projectId: $projectId,
                            environmentName: $environmentName
                        })
                    }
                """,
                "variables": {"projectId": project_id, "environmentName": target},
            },
            timeout=30,
        )
        if resp.status_code >= 400:
            return ActionOutcome(success=False, data={}, error=f"Railway API error {resp.status_code}")

        return ActionOutcome(success=True, data={"target": target, "provider": "railway", "ref": git_ref})
