"""
SoloOS V10 — Multi-Tier Disk Cache

Three TTL tiers:
  TTL_LLM     24h  — council answers, pattern analysis (expensive, deterministic)
  TTL_HTTP     1h  — HN, Reddit, Jina market signals (fresh-enough)
  TTL_COMPUTED 5m  — financial calculations with live data (fast-changing)

Usage:
    from soloos_core.data.cache import cached, TTL_HTTP, TTL_LLM

    @cached(TTL_HTTP)
    def fetch_hn_stories(limit: int = 10) -> list:
        ...  # HTTP call cached for 1h

    @cached(TTL_LLM, key_fn=lambda dec, stage, **_: f"council:{hash(dec)}:{stage}")
    def run_council(decision: str, stage: str) -> dict:
        ...  # LLM call cached for 24h

Cache is stored at ~/.soloos/cache/ — survives server restarts.
"""

import os
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional

# ─────────────────────────────────────────────────────────────
# TTL constants (seconds)
# ─────────────────────────────────────────────────────────────

TTL_LLM = 86_400       # 24h — LLM council answers
TTL_HTTP = 3_600       # 1h  — HN, Reddit, Jina
TTL_COMPUTED = 300     # 5m  — financial calculations
TTL_SESSION = None     # No expiry — in-memory only (not for disk cache)

# ─────────────────────────────────────────────────────────────
# Cache initialization (lazy, fail-open)
# ─────────────────────────────────────────────────────────────

_cache = None
_cache_available = False


def _get_cache():
    global _cache, _cache_available
    if _cache is not None:
        return _cache, _cache_available

    try:
        import diskcache
        cache_dir = Path.home() / ".soloos" / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        _cache = diskcache.Cache(str(cache_dir), size_limit=500_000_000)  # 500MB
        _cache_available = True
    except ImportError:
        # diskcache not installed — cache is a no-op
        _cache = {}
        _cache_available = False
    except Exception:
        # Disk error — fail open
        _cache = {}
        _cache_available = False

    return _cache, _cache_available


# ─────────────────────────────────────────────────────────────
# Cache decorator
# ─────────────────────────────────────────────────────────────

def cached(ttl: Optional[int], key_fn: Optional[Callable] = None):
    """
    Decorator that caches function return values to disk.

    Args:
        ttl: TTL in seconds. None = no caching (pass-through).
        key_fn: Optional function to compute cache key from args/kwargs.
                Default: uses function module + name + all args as string.

    The decorated function gains a `.cache_invalidate(*args, **kwargs)` method
    to manually bust the cache for specific arguments.

    Fail-open: if diskcache is unavailable or errors, function runs normally.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if ttl is None:
                return fn(*args, **kwargs)

            cache, available = _get_cache()
            if not available:
                return fn(*args, **kwargs)

            # Compute cache key
            if key_fn:
                key = key_fn(*args, **kwargs)
            else:
                key = f"{fn.__module__}.{fn.__qualname__}:{args}:{sorted(kwargs.items())}"

            try:
                cached_val = cache.get(key)
                if cached_val is not None:
                    return cached_val
            except Exception:
                pass  # Cache read failure → fall through to real call

            result = fn(*args, **kwargs)

            try:
                cache.set(key, result, expire=ttl)
            except Exception:
                pass  # Cache write failure → return result anyway

            return result

        def cache_invalidate(*args, **kwargs):
            """Manually invalidate cache for these specific args."""
            cache, available = _get_cache()
            if not available:
                return
            if key_fn:
                key = key_fn(*args, **kwargs)
            else:
                key = f"{fn.__module__}.{fn.__qualname__}:{args}:{sorted(kwargs.items())}"
            try:
                cache.delete(key)
            except Exception:
                pass

        wrapper.cache_invalidate = cache_invalidate
        wrapper.cache_ttl = ttl
        return wrapper

    return decorator


# ─────────────────────────────────────────────────────────────
# Cache management utilities
# ─────────────────────────────────────────────────────────────

def get_cache_stats() -> dict:
    """Return cache statistics for observability."""
    cache, available = _get_cache()
    if not available:
        return {"available": False, "reason": "diskcache not installed or disk error"}

    try:
        return {
            "available": True,
            "size_bytes": cache.volume(),
            "item_count": len(cache),
            "cache_dir": str(Path.home() / ".soloos" / "cache"),
        }
    except Exception as e:
        return {"available": True, "error": str(e)}


def clear_cache_by_prefix(prefix: str) -> int:
    """Clear all cache entries whose key starts with prefix. Returns count deleted."""
    cache, available = _get_cache()
    if not available:
        return 0
    count = 0
    try:
        for key in list(cache.iterkeys()):
            if isinstance(key, str) and key.startswith(prefix):
                cache.delete(key)
                count += 1
    except Exception:
        pass
    return count


def clear_all_cache() -> int:
    """Nuke entire cache. Returns item count cleared."""
    cache, available = _get_cache()
    if not available:
        return 0
    try:
        count = len(cache)
        cache.clear()
        return count
    except Exception:
        return 0
