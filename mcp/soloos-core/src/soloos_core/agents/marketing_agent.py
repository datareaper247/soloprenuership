"""
Autonomous marketing agent.

Capabilities:
- Generate SEO blog post from HN/Reddit pain point signals
- Schedule social posts (Tier 2 — soft approved)
- Draft email newsletter (Tier 1 — compute, human sends)
- Monitor competitor moves and generate response content
- Track content performance via analytics_db

Schedule:
- Monday: generate content plan for week
- Daily: post social (within limit)
- Wednesday: draft newsletter (for human review)
- Friday: content performance review
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are a growth-focused content marketer for a B2B SaaS startup.
Your goal: generate high-value content that attracts ideal customers and builds authority.

Rules:
- Always target a specific search intent (informational, commercial, transactional)
- Every piece of content should address a real pain point
- Lead with data, specifics, and examples — not vague generalities
- SEO: target long-tail keywords, not broad terms
- Social: one strong insight per post, not a list of 10 tips
"""


class MarketingAgent:
    """Autonomous marketing agent."""

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

    def generate_content_plan(self) -> dict:
        """Generate content plan for the week."""
        client = self._get_client()
        if client is None:
            return {
                "status": "unavailable",
                "plan": [],
                "reason": "ANTHROPIC_API_KEY not configured",
            }

        try:
            from ..agent.world_model import get_world_model
            context = get_world_model().get_context_for_agent("MarketingAgent")
        except Exception:
            context = "No business context available"

        try:
            response = client.messages.create(
                model=os.environ.get("SOLOOS_MARKETING_MODEL", "claude-sonnet-4-6"),
                max_tokens=1000,
                system=_SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"{context}\n\nCreate a 5-piece content plan for this week. Include: title, target keyword, format (blog/tweet/newsletter), and publish day."
                }],
            )
            plan_text = response.content[0].text
            return {"status": "generated", "plan": plan_text, "week": _current_week()}
        except Exception as exc:
            logger.warning("MarketingAgent.generate_content_plan failed: %s", exc)
            return {"status": "error", "error": str(exc), "plan": []}

    def write_blog_post(self, topic: str, target_keywords: list) -> str:
        """Generate SEO-optimized blog post."""
        client = self._get_client()
        if client is None:
            return f"# {topic}\n\n[Blog post draft — ANTHROPIC_API_KEY required for generation]"

        try:
            keywords_str = ", ".join(target_keywords[:5])
            response = client.messages.create(
                model=os.environ.get("SOLOOS_MARKETING_MODEL", "claude-sonnet-4-6"),
                max_tokens=2000,
                system=_SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"Write a 1200-word SEO blog post on: '{topic}'\nTarget keywords: {keywords_str}\nFormat: H2 subheadings, practical examples, actionable takeaways."
                }],
            )
            return response.content[0].text
        except Exception as exc:
            logger.warning("MarketingAgent.write_blog_post failed: %s", exc)
            return f"# {topic}\n\n[Generation failed: {exc}]"

    def schedule_social_post(self, content: str, platforms: list) -> dict:
        """Schedule social posts via ActionRegistry."""
        from ..core.action_registry import get_action_registry, ActionRequest, is_kill_switch_active

        if is_kill_switch_active():
            return {"status": "blocked", "reason": "Kill switch active"}

        registry = get_action_registry()
        results = {}
        for platform in platforms:
            result = registry.execute(ActionRequest(
                action="post_social",
                params={"content": content, "platform": platform},
                reasoning="Scheduled marketing post",
                agent_id="marketing",
            ))
            results[platform] = result.status

        return {"status": "processed", "results": results}

    def draft_newsletter(self) -> str:
        """Draft email newsletter for human review."""
        client = self._get_client()
        if client is None:
            return "[Newsletter draft — ANTHROPIC_API_KEY required]"

        try:
            from ..agent.world_model import get_world_model
            wm = get_world_model().get()
            metrics = wm.get("metrics", {})
            experiments = wm.get("experiments", [])
        except Exception:
            metrics, experiments = {}, []

        try:
            exp_summary = "\n".join(f"- {e.get('hypothesis', '')}" for e in experiments[:3]) or "No running experiments"
            response = client.messages.create(
                model=os.environ.get("SOLOOS_MARKETING_MODEL", "claude-sonnet-4-6"),
                max_tokens=800,
                system=_SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"Draft a weekly newsletter for our SaaS customers.\nMRR: ${metrics.get('mrr', 0):,.0f}\nRunning experiments:\n{exp_summary}\n\nInclude: 1 product update, 1 tip/insight, 1 ask."
                }],
            )
            return response.content[0].text
        except Exception as exc:
            logger.warning("MarketingAgent.draft_newsletter failed: %s", exc)
            return f"[Newsletter draft failed: {exc}]"

    def analyze_content_performance(self) -> dict:
        """Analyze content performance from analytics DB."""
        # Reads from analytics DB — basic stub
        return {
            "status": "analyzed",
            "top_posts": [],
            "top_social": [],
            "email_open_rate": None,
            "period": "last_7_days",
        }


def _current_week() -> str:
    return datetime.now(timezone.utc).strftime("%Y-W%V")
