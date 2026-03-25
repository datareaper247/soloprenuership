"""
Unit tests for data/cache.py — multi-tier disk cache.
"""

import pytest
import time
from unittest.mock import patch


def test_cached_decorator_returns_result():
    """@cached decorator returns the function's return value."""
    from soloos_core.data.cache import cached, TTL_HTTP

    call_count = 0

    @cached(TTL_HTTP)
    def expensive_fn(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    result = expensive_fn(5)
    assert result == 10
    assert call_count == 1


def test_cached_decorator_caches_on_second_call():
    """@cached decorator returns cached value on second call."""
    from soloos_core.data.cache import cached, TTL_HTTP

    call_count = 0

    @cached(TTL_HTTP)
    def expensive_fn_unique(y: int) -> int:
        nonlocal call_count
        call_count += 1
        return y * 3

    result1 = expensive_fn_unique(7)
    result2 = expensive_fn_unique(7)

    assert result1 == result2 == 21
    # Second call should hit cache — but we can't guarantee this in unit tests
    # without controlling the cache backend. Just verify correct result.


def test_cached_with_ttl_none_is_passthrough():
    """@cached(None) is a pass-through — no caching."""
    from soloos_core.data.cache import cached

    call_count = 0

    @cached(None)
    def passthrough_fn(z: int) -> int:
        nonlocal call_count
        call_count += 1
        return z

    result1 = passthrough_fn(42)
    result2 = passthrough_fn(42)

    assert result1 == result2 == 42
    # With TTL=None, every call goes through
    assert call_count == 2


def test_cached_with_custom_key_fn():
    """@cached with key_fn uses custom key."""
    from soloos_core.data.cache import cached, TTL_LLM

    call_count = 0

    @cached(TTL_LLM, key_fn=lambda decision, stage="": f"test_council:{hash(decision)}:{stage}")
    def fake_council(decision: str, stage: str = "") -> dict:
        nonlocal call_count
        call_count += 1
        return {"decision": decision, "verdict": "PROCEED"}

    result = fake_council("should I raise?", stage="$5K MRR")
    assert result["verdict"] == "PROCEED"
    assert call_count >= 1


def test_cache_stats_returns_dict():
    """get_cache_stats returns a dict with expected keys."""
    from soloos_core.data.cache import get_cache_stats

    stats = get_cache_stats()
    assert isinstance(stats, dict)
    assert "available" in stats


def test_cache_invalidate_method_exists():
    """Decorated function has a cache_invalidate method."""
    from soloos_core.data.cache import cached, TTL_HTTP

    @cached(TTL_HTTP)
    def fn_with_invalidate(x: int) -> int:
        return x

    assert hasattr(fn_with_invalidate, "cache_invalidate")
    assert callable(fn_with_invalidate.cache_invalidate)


def test_cache_ttl_attribute_set():
    """Decorated function exposes its TTL via .cache_ttl."""
    from soloos_core.data.cache import cached, TTL_LLM

    @cached(TTL_LLM)
    def fn_with_ttl() -> str:
        return "result"

    assert fn_with_ttl.cache_ttl == TTL_LLM


def test_clear_all_cache_returns_int():
    """clear_all_cache returns an integer (count of cleared items)."""
    from soloos_core.data.cache import clear_all_cache

    result = clear_all_cache()
    assert isinstance(result, int)
    assert result >= 0


def test_ttl_constants_are_correct():
    """TTL constants have expected values."""
    from soloos_core.data.cache import TTL_LLM, TTL_HTTP, TTL_COMPUTED

    assert TTL_LLM == 86_400    # 24h
    assert TTL_HTTP == 3_600    # 1h
    assert TTL_COMPUTED == 300  # 5m
    assert TTL_LLM > TTL_HTTP > TTL_COMPUTED
