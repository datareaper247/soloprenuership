"""
LangGraph-based agent executor.
Dep: langgraph>=0.2.0, langchain-anthropic>=0.3.0 (optional — falls back to direct Anthropic SDK)

Pattern (LangGraph):
    StateGraph with nodes:
    - think: Claude decides what to do (tool_use)
    - act: executes tool/action via ActionRegistry
    - observe: processes result, updates world model
    - decide_next: continue loop or stop

The executor runs ONE task from the TaskQueue per invocation.
It is NOT a persistent process itself — APScheduler calls it on schedule.
"""

from __future__ import annotations

import json
import logging
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

_MAX_ITERATIONS = 10


class AgentState:
    """Agent execution state (TypedDict-compatible dict wrapper)."""
    task: dict
    world_model: dict
    messages: list
    actions_taken: list
    iteration: int
    done: bool


class _UnavailableExecutor:
    """Stub returned when langgraph/anthropic packages not installed."""

    def run(self, task: dict, world_model: dict, available_tools: list) -> dict:
        return {
            "result": f"AgentExecutor unavailable: install 'soloos-core[agent]' for full execution. Task: {task.get('task_type', 'unknown')}",
            "actions_taken": [],
            "reasoning": "Executor not configured",
            "status": "unavailable",
        }


class AgentExecutor:
    """
    Wraps a LangGraph StateGraph (or falls back to direct Anthropic SDK).
    Runs one task to completion.
    """

    def __init__(self) -> None:
        self._backend = self._build_backend()

    def _build_backend(self):
        """Try LangGraph first, then Anthropic SDK, then stub."""
        # Try LangGraph
        try:
            from langgraph.graph import StateGraph, END  # type: ignore[import]
            from langchain_anthropic import ChatAnthropic  # type: ignore[import]
            return "langgraph"
        except ImportError:
            pass

        # Try direct Anthropic SDK
        try:
            import anthropic  # type: ignore[import]
            if os.environ.get("ANTHROPIC_API_KEY"):
                return "anthropic"
        except ImportError:
            pass

        return "stub"

    def run(self, task: dict, world_model: dict, available_tools: list) -> dict:
        from ..core.action_registry import is_kill_switch_active

        if is_kill_switch_active():
            return {
                "result": "Execution blocked: kill switch active",
                "actions_taken": [],
                "reasoning": "Kill switch prevented execution",
                "status": "blocked",
            }

        if self._backend == "langgraph":
            return self._run_langgraph(task, world_model, available_tools)
        elif self._backend == "anthropic":
            return self._run_anthropic(task, world_model, available_tools)
        else:
            return _UnavailableExecutor().run(task, world_model, available_tools)

    def _run_anthropic(self, task: dict, world_model: dict, available_tools: list) -> dict:
        """Direct Anthropic SDK execution (simpler than LangGraph)."""
        import anthropic  # type: ignore[import]

        client = anthropic.Anthropic()
        model = os.environ.get("SOLOOS_AGENT_MODEL", "claude-sonnet-4-6")

        context = self._build_context(task, world_model)
        actions_taken = []

        messages = [{"role": "user", "content": context}]

        for iteration in range(_MAX_ITERATIONS):
            response = client.messages.create(
                model=model,
                max_tokens=2048,
                tools=available_tools,
                messages=messages,
            )

            # Collect text reasoning
            reasoning_parts = [
                block.text for block in response.content
                if hasattr(block, "text")
            ]

            if response.stop_reason == "end_turn":
                return {
                    "result": "\n".join(reasoning_parts),
                    "actions_taken": actions_taken,
                    "reasoning": "\n".join(reasoning_parts),
                    "status": "completed",
                    "iterations": iteration + 1,
                }

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_result = self._execute_tool(block.name, block.input, available_tools)
                        actions_taken.append({"tool": block.name, "input": block.input, "result": tool_result})
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(tool_result),
                        })

                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

        return {
            "result": "Max iterations reached",
            "actions_taken": actions_taken,
            "reasoning": "Stopped after max iterations",
            "status": "max_iterations",
        }

    def _run_langgraph(self, task: dict, world_model: dict, available_tools: list) -> dict:
        """LangGraph StateGraph execution."""
        try:
            from langgraph.graph import StateGraph, END  # type: ignore[import]
            from langchain_anthropic import ChatAnthropic  # type: ignore[import]
            from langchain_core.messages import HumanMessage  # type: ignore[import]
        except ImportError:
            return _UnavailableExecutor().run(task, world_model, available_tools)

        model = os.environ.get("SOLOOS_AGENT_MODEL", "claude-sonnet-4-6")
        llm = ChatAnthropic(model=model, max_tokens=2048)

        actions_taken: list = []
        context = self._build_context(task, world_model)

        # Simple single-pass for now (LangGraph full graph is for Next-6)
        messages = [HumanMessage(content=context)]
        response = llm.invoke(messages)

        return {
            "result": response.content if isinstance(response.content, str) else str(response.content),
            "actions_taken": actions_taken,
            "reasoning": str(response.content)[:500],
            "status": "completed",
        }

    def _build_context(self, task: dict, world_model: dict) -> str:
        task_type = task.get("task_type", "unknown")
        payload = task.get("payload", {})
        metrics = world_model.get("metrics", {})

        return f"""You are the SoloOS Founder AI. Execute this task:

TASK: {task_type}
PAYLOAD: {json.dumps(payload, indent=2)}

BUSINESS CONTEXT:
- MRR: ${metrics.get('mrr', 0):,.0f}
- Active customers: {metrics.get('active_customers', 0)}
- Runway: {metrics.get('runway_months', 'unknown')} months

Respond with your reasoning and the action to take.
If you need to call a tool, use the tool call format.
When done, summarize what was accomplished."""

    def _execute_tool(self, tool_name: str, tool_input: dict, available_tools: list) -> dict:
        """Execute a tool call — routes through ActionRegistry for action tools."""
        from ..core.action_registry import get_action_registry, ActionRequest

        registry = get_action_registry()
        if tool_name in registry._actions:
            result = registry.execute(ActionRequest(
                action=tool_name,
                params=tool_input,
                reasoning=f"Tool call from AgentExecutor",
                agent_id="agent_executor",
            ))
            return {"status": result.status, "result": result.result, "error": result.error}
        return {"error": f"Unknown tool: {tool_name}"}


_executor: AgentExecutor | None = None


def get_executor() -> AgentExecutor:
    global _executor
    if _executor is None:
        _executor = AgentExecutor()
    return _executor
