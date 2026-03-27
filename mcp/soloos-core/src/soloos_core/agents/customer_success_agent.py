"""
Autonomous customer success agent.

Triggers:
- Webhook: new support ticket (Intercom/Crisp)
- Schedule: daily NPS analysis
- Schedule: weekly churn risk scan

Capabilities (all routed through ActionRegistry):
- Read customer history from context_db
- Generate empathetic, helpful response using Claude
- Send reply via support_action (Tier 2 — soft approved, daily limit)
- Flag churn risks to Founder Agent (Tier 1 — compute only)
- Create follow-up tasks if issue complex

System prompt focus: empathy, resolution rate, retention
Tools available: read tools only + support_action (no spend/deploy)
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are a world-class customer success manager for a SaaS startup.
Your priorities in order:
1. Resolve the customer's immediate problem completely
2. Leave them feeling heard and valued
3. Identify and flag churn risks proactively

Rules:
- Never be defensive or dismissive
- Always acknowledge the problem first, then solve it
- If you can't fully resolve it, give a clear timeline
- Keep responses concise (3-5 sentences max for simple issues)
- Escalate to founder if: billing issue >$100, legal threat, multiple repeated failures
"""


class CustomerSuccessAgent:
    """Autonomous customer success agent."""

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

    def handle_ticket(self, ticket: dict) -> dict:
        """Process a support ticket and generate a reply."""
        from ..core.action_registry import get_action_registry, ActionRequest, is_kill_switch_active

        if is_kill_switch_active():
            return {"status": "blocked", "reason": "Kill switch active"}

        customer_id = ticket.get("customer_id", "unknown")
        message = ticket.get("message", "")
        conversation_id = ticket.get("conversation_id", "")

        history = self._load_customer_history(customer_id)
        reply = self.generate_reply(ticket, history)

        # Check for churn risk
        churn_risk = self._detect_churn_risk(ticket, history)
        if churn_risk:
            self._flag_churn_risk(customer_id, churn_risk)

        if conversation_id:
            registry = get_action_registry()
            result = registry.execute(ActionRequest(
                action="reply_support",
                params={
                    "conversation_id": conversation_id,
                    "message": reply,
                },
                reasoning=f"Customer ticket: {message[:100]}",
                agent_id="customer_success",
            ))
            return {
                "status": result.status,
                "reply": reply,
                "churn_risk": churn_risk,
                "customer_id": customer_id,
            }

        return {"status": "reply_generated", "reply": reply, "churn_risk": churn_risk}

    def generate_reply(self, ticket: dict, history: list) -> str:
        """Generate empathetic, helpful response using Claude."""
        client = self._get_client()
        if client is None:
            return f"Thank you for reaching out. We received your message and will respond shortly."

        try:
            context = ""
            if history:
                context = f"\nCustomer history ({len(history)} previous interactions):\n"
                for h in history[-3:]:
                    context += f"- {h.get('summary', '')}\n"

            response = client.messages.create(
                model=os.environ.get("SOLOOS_CS_MODEL", "claude-haiku-4-5-20251001"),
                max_tokens=500,
                system=_SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"Customer message: {ticket.get('message', '')}{context}\n\nWrite a reply:"
                }],
            )
            return response.content[0].text
        except Exception as exc:
            logger.warning("CustomerSuccessAgent.generate_reply failed: %s", exc)
            return "Thank you for contacting us. Our team will review your request and follow up shortly."

    def analyze_nps(self) -> dict:
        """Analyze NPS scores and identify patterns."""
        # Reads from analytics DB — stub for now
        return {
            "status": "analyzed",
            "avg_nps": None,
            "detractors": [],
            "promoters": [],
            "trends": [],
        }

    def scan_churn_risks(self) -> list[dict]:
        """Scan all customers for churn risk signals."""
        risks = []
        try:
            from ..agent.world_model import get_world_model
            metrics = get_world_model().get_section("metrics")
            churn_rate = metrics.get("churn_rate", 0)
            if churn_rate and churn_rate > 0.05:
                risks.append({
                    "type": "high_overall_churn",
                    "churn_rate": churn_rate,
                    "action": "review_recent_cancellations",
                })
        except Exception:
            pass
        return risks

    def _load_customer_history(self, customer_id: str) -> list:
        """Load customer interaction history from context DB."""
        try:
            from ..data.context_db import get_context_db
            db = get_context_db()
            # Simple query — expand as needed
            return db.search_context(f"customer:{customer_id}") if hasattr(db, 'search_context') else []
        except Exception:
            return []

    def _detect_churn_risk(self, ticket: dict, history: list) -> dict | None:
        """Detect churn risk signals from ticket content."""
        message = ticket.get("message", "").lower()
        churn_signals = ["cancel", "quit", "refund", "disappointed", "not working", "terrible"]
        escalation_signals = ["legal", "lawsuit", "fraud", "charge dispute"]

        if any(s in message for s in escalation_signals):
            return {"level": "critical", "reason": "Legal/billing escalation signal"}
        if any(s in message for s in churn_signals):
            return {"level": "high", "reason": "Churn language detected"}
        if len(history) > 5:
            return {"level": "medium", "reason": "High ticket volume — possible dissatisfaction"}
        return None

    def _flag_churn_risk(self, customer_id: str, risk: dict) -> None:
        """Enqueue a churn risk alert for the founder loop."""
        try:
            from ..agent.task_queue import get_task_queue
            get_task_queue().enqueue(
                "churn_risk_alert",
                {"customer_id": customer_id, "risk": risk},
                priority=2,
                agent_id="founder",
            )
        except Exception as exc:
            logger.warning("Failed to flag churn risk: %s", exc)
