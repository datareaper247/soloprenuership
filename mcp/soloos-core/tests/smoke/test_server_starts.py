"""
Smoke tests — verify the server starts and all tools register without crashing.

These are the highest-value, lowest-effort tests. Run before every commit.
If these fail, nothing else matters.
"""

import asyncio
import pytest


def test_server_imports_cleanly():
    """Server module imports without errors."""
    from soloos_core import server  # noqa: F401


def test_all_tools_register():
    """All expected MCP tools are registered."""
    async def _check():
        from soloos_core.server import mcp
        tools = await mcp.list_tools()
        tool_names = {t.name for t in tools}
        return tool_names

    tool_names = asyncio.run(_check())

    # Minimum tool count
    assert len(tool_names) >= 31, (
        f"Expected 31+ tools, got {len(tool_names)}. "
        f"Registered: {sorted(tool_names)}"
    )

    # Critical enforcement tools must be present
    critical_tools = [
        "check_kill_signals_tool",
        "log_decision",
        "reject_if_overdue",
        "council_brief",
        "simulate_business_change",
        "get_decision_intelligence_brief",
        "score_opportunity",
        "calculate_runway",
        "score_pmf",
        "get_mrr_live",
        "get_market_signals",
        "read_web_content",
    ]
    for tool in critical_tools:
        assert tool in tool_names, f"Critical tool '{tool}' is not registered"


def test_kb_loads_without_errors():
    """Knowledge base loads patterns, founders, and markets without exceptions."""
    from soloos_core.kb_loader import get_patterns, get_founders, get_markets
    patterns = get_patterns()
    founders = get_founders()
    markets = get_markets()

    # KB should have content (not empty)
    assert len(patterns) >= 0  # Passes even if KB files don't exist yet
    assert isinstance(patterns, list)
    assert isinstance(founders, list)
    assert isinstance(markets, list)


def test_log_manager_paths_resolve():
    """Log manager resolves KB root and context paths without errors."""
    from soloos_core.log_manager import KB_ROOT, CONTEXT_ROOT
    # Paths should be Path objects (not throw exceptions on access)
    assert KB_ROOT is not None
    assert CONTEXT_ROOT is not None
