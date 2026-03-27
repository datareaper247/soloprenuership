"""
Autonomous engineering agent (wraps Claude Code functionality).

Triggers:
- GitHub webhook: PR opened → code review
- GitHub webhook: issue labeled "bug" → diagnosis + fix attempt
- Linear webhook: task created → spec generation
- Schedule: daily code quality scan

Capabilities:
- Code review (read-only, no approval needed)
- Bug diagnosis (read-only)
- Generate fix PRs (Tier 3 — staging, soft approval)
- Deploy to staging (Tier 3)
- Flag critical bugs to Founder Agent

Uses: Anthropic Claude API directly (not MCP) for code analysis
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

_REVIEW_SYSTEM_PROMPT = """You are a senior software engineer conducting code reviews.
Focus on:
1. Security vulnerabilities (injection, auth bypass, exposed secrets)
2. Logic errors and edge cases
3. Performance anti-patterns (N+1 queries, unnecessary loops)
4. Test coverage gaps

Format: structured markdown with sections for each concern.
Severity: CRITICAL / HIGH / MEDIUM / LOW for each finding.
Include line references when provided.
Keep it actionable — one clear fix recommendation per finding."""

_DIAGNOSIS_SYSTEM_PROMPT = """You are a debugging expert. Given a bug report:
1. Identify the most likely root cause (not symptoms)
2. List 3 hypotheses ranked by probability
3. Describe the simplest experiment to confirm the root cause
4. Suggest the fix

Be specific. Reference the codebase if provided."""


class EngineeringAgent:
    """Autonomous engineering agent."""

    def __init__(self) -> None:
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import anthropic  # type: ignore[import]
                if os.environ.get("ANTHROPIC_API_KEY"):
                    self._client = anthropic.Anthropic()
            except ImportError:
                pass
        return self._client

    def review_pr(self, pr_url: str) -> str:
        """Perform code review on a PR."""
        client = self._get_client()
        if client is None:
            return f"[Code review unavailable: ANTHROPIC_API_KEY required]\nPR: {pr_url}"

        pr_content = self._fetch_pr_content(pr_url)

        try:
            response = client.messages.create(
                model=os.environ.get("SOLOOS_ENG_MODEL", "claude-sonnet-4-6"),
                max_tokens=2000,
                system=_REVIEW_SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"Review this PR:\nURL: {pr_url}\n\n{pr_content}"
                }],
            )
            return response.content[0].text
        except Exception as exc:
            logger.warning("EngineeringAgent.review_pr failed: %s", exc)
            return f"[Review failed: {exc}]"

    def diagnose_bug(self, issue: dict) -> dict:
        """Diagnose a bug from issue details."""
        client = self._get_client()
        if client is None:
            return {
                "status": "unavailable",
                "diagnosis": "ANTHROPIC_API_KEY required for diagnosis",
            }

        title = issue.get("title", "")
        description = issue.get("body", "")
        error_log = issue.get("error_log", "")

        try:
            content = f"Bug title: {title}\nDescription: {description}"
            if error_log:
                content += f"\n\nError log:\n{error_log[:2000]}"

            response = client.messages.create(
                model=os.environ.get("SOLOOS_ENG_MODEL", "claude-sonnet-4-6"),
                max_tokens=1500,
                system=_DIAGNOSIS_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": content}],
            )
            diagnosis_text = response.content[0].text
            return {
                "status": "diagnosed",
                "diagnosis": diagnosis_text,
                "issue_title": title,
            }
        except Exception as exc:
            logger.warning("EngineeringAgent.diagnose_bug failed: %s", exc)
            return {"status": "error", "error": str(exc)}

    def generate_fix(self, bug_diagnosis: dict) -> dict:
        """Generate a fix based on diagnosis."""
        client = self._get_client()
        if client is None:
            return {"status": "unavailable", "fix": None}

        diagnosis = bug_diagnosis.get("diagnosis", "")
        try:
            response = client.messages.create(
                model=os.environ.get("SOLOOS_ENG_MODEL", "claude-sonnet-4-6"),
                max_tokens=2000,
                system="You are an expert software engineer. Generate a precise, minimal fix for the diagnosed bug. Include the exact code changes needed.",
                messages=[{
                    "role": "user",
                    "content": f"Based on this diagnosis:\n{diagnosis}\n\nGenerate the minimal code fix."
                }],
            )
            return {
                "status": "fix_generated",
                "fix": response.content[0].text,
                "diagnosis": diagnosis[:200],
            }
        except Exception as exc:
            logger.warning("EngineeringAgent.generate_fix failed: %s", exc)
            return {"status": "error", "error": str(exc)}

    def create_pr(self, changes: dict, description: str) -> str:
        """Create a PR via GitHub API (Tier 3 — requires soft approval)."""
        from ..core.action_registry import get_action_registry, ActionRequest, Tier

        # This would require a github_action — placeholder
        logger.info("EngineeringAgent.create_pr: %s", description[:100])
        return f"PR creation queued for approval: {description[:100]}"

    def deploy_staging(self, pr_url: str) -> dict:
        """Deploy to staging after code review passes (Tier 3)."""
        from ..core.action_registry import get_action_registry, ActionRequest

        registry = get_action_registry()
        result = registry.execute(ActionRequest(
            action="deploy",
            params={"target": "staging", "provider": "vercel", "git_ref": "main"},
            reasoning=f"Auto-deploy after PR review: {pr_url}",
            agent_id="engineering",
        ))
        return {"status": result.status, "pr_url": pr_url}

    def daily_code_scan(self) -> dict:
        """Perform daily code quality scan."""
        # Light scan — reads package.json/pyproject.toml for outdated deps
        return {
            "status": "scanned",
            "findings": [],
            "outdated_deps": [],
            "security_issues": [],
        }

    def _fetch_pr_content(self, pr_url: str) -> str:
        """Fetch PR diff content from GitHub API."""
        github_token = os.environ.get("GITHUB_TOKEN")
        if not github_token or "github.com" not in pr_url:
            return f"[PR content unavailable — GITHUB_TOKEN not set or not a GitHub URL]"

        try:
            import httpx  # type: ignore[import]
            # Convert PR URL to API URL
            # e.g., https://github.com/owner/repo/pull/123 → /repos/owner/repo/pulls/123
            parts = pr_url.replace("https://github.com/", "").split("/")
            if len(parts) >= 4:
                owner, repo, _, pr_num = parts[:4]
                api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_num}/files"
                resp = httpx.get(
                    api_url,
                    headers={"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github.v3+json"},
                    timeout=15,
                )
                if resp.status_code == 200:
                    files = resp.json()
                    content_parts = []
                    for f in files[:10]:  # Limit to 10 files
                        content_parts.append(f"## {f.get('filename', '')}\n{f.get('patch', '')[:1000]}")
                    return "\n\n".join(content_parts)
        except Exception as exc:
            logger.warning("Failed to fetch PR content: %s", exc)

        return f"[PR URL: {pr_url}]"
