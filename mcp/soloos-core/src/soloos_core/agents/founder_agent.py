"""
Founder Agent — the orchestrating intelligence.

Responsibilities:
- Weekly strategy session (reads World Model → sets objectives)
- Routes incoming events to right specialist agent
- Makes cross-domain decisions (pricing, pivots, partnerships)
- Maintains company goals in World Model
- Generates human-facing reports

The FounderAgent is the only agent with access to Tier 4+ actions.
All other agents are Tier 0-3 only.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are the Founder AI for an early-stage SaaS startup.
You make strategic decisions based on data, not vibes.

Your principles:
1. PMF before growth — never scale what isn't working
2. Cash is oxygen — track runway weekly
3. Kill signals save time — enforce them ruthlessly
4. Every action has a kill signal — if it doesn't, it's not specific enough

Anti-patterns you actively prevent:
- Building features without customer validation
- Adding growth channels before 40% "very disappointed"
- Hiring before documented processes
- Pivoting before exhausting current hypothesis

Output format for strategic questions:
RECOMMENDATION: [1 sentence]
WHY: [2-3 bullets with evidence]
RISKS: [1-2 key risks]
KILL SIGNAL: [measurable, 30-day window]
"""


class FounderAgent:
    """Orchestrating founder intelligence agent."""

    def __init__(self) -> None:
        self._client = None
        self._cs_agent = None
        self._mkt_agent = None
        self._eng_agent = None

    def _get_client(self):
        if self._client is None:
            try:
                import anthropic  # type: ignore[import]
                if os.environ.get("ANTHROPIC_API_KEY"):
                    self._client = anthropic.Anthropic()
            except ImportError:
                pass
        return self._client

    def run_weekly_strategy(self) -> dict:
        """Weekly strategy session — reads World Model, sets objectives."""
        from ..agent.world_model import get_world_model

        world_model = get_world_model().refresh()
        context = get_world_model().get_context_for_agent("FounderAgent")

        client = self._get_client()
        if client is None:
            return {
                "status": "unavailable",
                "objectives": [],
                "reasoning": "ANTHROPIC_API_KEY required",
            }

        try:
            response = client.messages.create(
                model=os.environ.get("SOLOOS_FOUNDER_MODEL", "claude-sonnet-4-6"),
                max_tokens=2000,
                system=_SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"{context}\n\nSet 3 weekly objectives for each domain: Customer Success, Marketing, Engineering. Each objective must have a kill signal.",
                }],
            )
            objectives_text = response.content[0].text

            # Save objectives to world model
            get_world_model().update_goals({
                "weekly_objectives": objectives_text,
                "week_start": _now()[:10],
            })

            return {
                "status": "completed",
                "objectives": objectives_text,
                "world_model_updated": True,
            }
        except Exception as exc:
            logger.warning("FounderAgent.run_weekly_strategy failed: %s", exc)
            return {"status": "error", "error": str(exc)}

    def route_event(self, event_type: str, payload: dict) -> dict:
        """Route incoming event to the appropriate specialist agent."""
        routing_map = {
            "new_support_ticket": "customer_success",
            "churn_alert": "customer_success",
            "pr_opened": "engineering",
            "bug_labeled": "engineering",
            "content_scheduled": "marketing",
            "competitor_move": "marketing",
        }

        domain = routing_map.get(event_type, "founder")

        if domain == "customer_success":
            from .customer_success_agent import CustomerSuccessAgent
            agent = CustomerSuccessAgent()
            return agent.handle_ticket(payload)

        elif domain == "engineering":
            from .engineering_agent import EngineeringAgent
            agent = EngineeringAgent()
            if event_type == "pr_opened":
                review = agent.review_pr(payload.get("pr_url", ""))
                return {"status": "reviewed", "review": review}
            elif event_type == "bug_labeled":
                return agent.diagnose_bug(payload)

        elif domain == "marketing":
            from .marketing_agent import MarketingAgent
            agent = MarketingAgent()
            return agent.generate_content_plan()

        # Founder handles it directly
        return self._handle_strategic_question(event_type, payload)

    def make_decision(self, question: str, context: dict | None = None) -> dict:
        """Make a cross-domain strategic decision."""
        client = self._get_client()
        if client is None:
            return {"status": "unavailable", "decision": None}

        from ..agent.world_model import get_world_model
        biz_context = get_world_model().get_context_for_agent("FounderAgent")

        additional = f"\n\nAdditional context: {json.dumps(context)}" if context else ""

        try:
            response = client.messages.create(
                model=os.environ.get("SOLOOS_FOUNDER_MODEL", "claude-sonnet-4-6"),
                max_tokens=1000,
                system=_SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"{biz_context}{additional}\n\nDecision needed: {question}"
                }],
            )
            decision_text = response.content[0].text
            return {
                "status": "decided",
                "question": question,
                "decision": decision_text,
                "timestamp": _now(),
            }
        except Exception as exc:
            logger.warning("FounderAgent.make_decision failed: %s", exc)
            return {"status": "error", "error": str(exc)}

    def generate_weekly_report(self) -> str:
        """Generate human-facing weekly report."""
        from ..agent.world_model import get_world_model
        from ..core.audit_log import get_audit_log

        world_model = get_world_model().get()
        metrics = world_model.get("metrics", {})
        experiments = world_model.get("experiments", [])
        audit_stats = get_audit_log().get_stats(hours=168)  # 7 days

        lines = [
            f"# Weekly Founder Report — {_now()[:10]}",
            "",
            "## Key Metrics",
            f"- MRR: ${metrics.get('mrr', 0):,.0f}",
            f"- Active customers: {metrics.get('active_customers', 0)}",
            f"- Churn rate: {metrics.get('churn_rate', 'unknown')}",
            f"- Runway: {metrics.get('runway_months', 'unknown')} months",
            "",
            "## AI Activity (Last 7 Days)",
            f"- Total actions: {audit_stats.get('total', 0)}",
            f"- By type: {json.dumps(audit_stats.get('by_action', {}))}",
            "",
            "## Running Experiments",
        ]

        for exp in experiments[:5]:
            lines.append(f"- {exp.get('hypothesis', 'Unknown')} [{exp.get('status', '')}]")

        if not experiments:
            lines.append("- No running experiments")

        return "\n".join(lines)

    def _handle_strategic_question(self, event_type: str, payload: dict) -> dict:
        """Handle events that don't fit a specific domain."""
        return self.make_decision(
            question=f"How should I respond to: {event_type}?",
            context=payload,
        )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
