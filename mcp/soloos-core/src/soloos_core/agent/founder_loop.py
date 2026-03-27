"""
Main autonomous founder loop.
Called by APScheduler on schedule, and triggered by webhooks.

Loop:
1. Check kill switch → abort if active
2. Refresh World Model
3. Dequeue highest priority task (or generate from World Model state)
4. Run through AgentExecutor
5. Log to AuditLog
6. Update World Model with outcome
7. Deliver summary if configured
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from ..core.action_registry import is_kill_switch_active
from ..core.audit_log import get_audit_log
from .task_queue import get_task_queue
from .world_model import get_world_model
from .executor import get_executor

logger = logging.getLogger(__name__)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class FounderLoop:
    """Main autonomous execution loop."""

    def run_once(self) -> dict:
        """Process one task from the queue. Returns outcome dict."""
        if is_kill_switch_active():
            return {"status": "blocked", "reason": "Kill switch active"}

        world_model = get_world_model().refresh()
        queue = get_task_queue()
        executor = get_executor()
        audit = get_audit_log()

        task = queue.dequeue()
        if task is None:
            # Generate default task from world model state
            task = self._generate_default_task(world_model)
            if task is None:
                return {"status": "idle", "reason": "No pending tasks"}

        task_id = task.get("id", "generated")
        logger.info("FounderLoop: running task %s (%s)", task_id, task.get("task_type"))

        audit.log({
            "action": "founder_loop_start",
            "tier": 1,
            "agent_id": "founder",
            "reasoning": f"Processing task: {task.get('task_type')}",
            "status": "intent",
        })

        try:
            result = executor.run(
                task=task,
                world_model=world_model,
                available_tools=[],
            )

            if task_id != "generated":
                queue.complete(task_id, result)

            get_world_model().update_agent_state({
                "last_task": task.get("task_type"),
                "last_result": result.get("status"),
                "notes": [result.get("reasoning", "")[:200]],
            })

            audit.log({
                "action": "founder_loop_complete",
                "tier": 1,
                "agent_id": "founder",
                "status": "executed",
                "result": {"task": task.get("task_type"), "outcome": result.get("status")},
            })

            return {
                "status": "completed",
                "task_type": task.get("task_type"),
                "result": result,
            }

        except Exception as exc:
            logger.exception("FounderLoop task failed: %s", exc)
            if task_id != "generated":
                queue.fail(task_id, str(exc))
            return {"status": "error", "error": str(exc)}

    def run_morning_session(self) -> str:
        """Full morning brief + actions."""
        if is_kill_switch_active():
            return "Morning session blocked: kill switch active"

        queue = get_task_queue()
        world_model = get_world_model().refresh()

        # Enqueue morning brief tasks
        queue.enqueue("morning_brief", {"source": "scheduled"}, priority=1)
        queue.enqueue("check_experiments", {}, priority=3)
        queue.enqueue("scan_market_signals", {}, priority=5)

        results = []
        for _ in range(3):  # Process the 3 enqueued tasks
            outcome = self.run_once()
            results.append(f"- {outcome.get('task_type', 'unknown')}: {outcome.get('status', 'unknown')}")

        metrics = world_model.get("metrics", {})
        return (
            f"# Morning Session — {_now()[:10]}\n\n"
            f"**MRR**: ${metrics.get('mrr', 0):,.0f}\n"
            f"**Customers**: {metrics.get('active_customers', 0)}\n\n"
            f"**Tasks processed**:\n" + "\n".join(results)
        )

    def run_evening_review(self) -> str:
        """Reflect on day, plan tomorrow."""
        if is_kill_switch_active():
            return "Evening review blocked: kill switch active"

        audit = get_audit_log()
        stats = audit.get_stats(hours=24)
        world_model = get_world_model().get()
        queue = get_task_queue()

        pending = queue.list_pending()

        return (
            f"# Evening Review — {_now()[:10]}\n\n"
            f"**Actions today**: {stats.get('total', 0)}\n"
            f"**By status**: {json.dumps(stats.get('by_status', {}))}\n"
            f"**Pending tasks tomorrow**: {len(pending)}\n\n"
            f"*Review complete. World model updated.*"
        )

    def handle_event(self, event_type: str, payload: dict) -> dict:
        """Handle an incoming webhook event."""
        if is_kill_switch_active():
            return {"status": "blocked", "reason": "Kill switch active"}

        queue = get_task_queue()

        # Map event types to task types
        event_task_map = {
            "stripe.charge.succeeded": "welcome_new_customer",
            "stripe.customer.subscription.deleted": "churn_alert",
            "github.pull_request.opened": "review_pr",
            "github.issues.labeled": "diagnose_bug",
            "intercom.conversation.created": "respond_support",
            "crisp.message.updated": "respond_support",
        }

        task_type = event_task_map.get(event_type, "handle_generic_event")
        task_id = queue.enqueue(task_type, {"event_type": event_type, **payload}, priority=2)

        logger.info("FounderLoop.handle_event: queued %s as %s", event_type, task_type)
        return {"status": "queued", "task_id": task_id, "task_type": task_type}

    def _generate_default_task(self, world_model: dict) -> dict | None:
        """Generate a task from world model state when queue is empty."""
        # Check for churn risks
        metrics = world_model.get("metrics", {})
        churn = metrics.get("churn_rate", 0)
        if churn and churn > 0.05:  # >5% churn
            return {
                "id": "generated",
                "task_type": "analyze_churn",
                "payload": {"churn_rate": churn},
                "priority": 2,
                "agent_id": "founder",
            }
        return None


_loop: FounderLoop | None = None


def get_founder_loop() -> FounderLoop:
    global _loop
    if _loop is None:
        _loop = FounderLoop()
    return _loop
