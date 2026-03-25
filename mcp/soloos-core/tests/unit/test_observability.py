"""
Unit tests for core/observability.py — structlog-based tool call instrumentation.
"""

import pytest


def test_instrument_tool_returns_correct_result():
    """@instrument_tool preserves function return value."""
    from soloos_core.core.observability import instrument_tool

    @instrument_tool
    def my_tool(x: int) -> str:
        return f"result:{x}"

    assert my_tool(42) == "result:42"


def test_instrument_tool_propagates_exceptions():
    """@instrument_tool re-raises exceptions from the wrapped function."""
    from soloos_core.core.observability import instrument_tool

    @instrument_tool
    def failing_tool() -> str:
        raise ValueError("something went wrong")

    with pytest.raises(ValueError, match="something went wrong"):
        failing_tool()


def test_instrument_tool_preserves_function_name():
    """@instrument_tool preserves __name__ and __doc__."""
    from soloos_core.core.observability import instrument_tool

    @instrument_tool
    def specifically_named_function() -> None:
        """My docstring."""
        pass

    assert specifically_named_function.__name__ == "specifically_named_function"
    assert specifically_named_function.__doc__ == "My docstring."


def test_log_event_does_not_raise():
    """log_event() is fail-open — never raises even with bad structlog config."""
    from soloos_core.core.observability import log_event

    # Should not raise regardless of structlog state
    log_event("test_event", key="value", number=42)


def test_get_log_stats_returns_dict():
    """get_log_stats returns a dict (even if log file doesn't exist)."""
    from soloos_core.core.observability import get_log_stats

    stats = get_log_stats(period_hours=1)
    assert isinstance(stats, dict)
    # Either has data or explains why there's no data
    assert "total_calls" in stats or "status" in stats or "entries" in stats


def test_instrument_tool_handles_no_args():
    """@instrument_tool works for zero-argument functions."""
    from soloos_core.core.observability import instrument_tool

    @instrument_tool
    def zero_arg_tool() -> dict:
        return {"status": "ok"}

    result = zero_arg_tool()
    assert result == {"status": "ok"}
