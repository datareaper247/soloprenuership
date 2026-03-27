---
last_updated: 2026-03-27
version: V10
test_status: 168 passed, 7 skipped, 0 failed
---

# SoloOS V10 — Technical Architecture

## What It Is
Thin founder intelligence protocol. MCP server exposing 33 tools to Claude Code.
Runs locally. No persistent process required.

## Core Components

### MCP Server (`mcp/soloos-core/`)
- **Transport**: MCP stdio (default) + REST/SSE via `soloos-api` (HTTP bridge)
- **Tools**: 33 total (see CLAUDE.md tool routing table)
- **Language**: Python 3.11
- **Location**: `/Users/fsd/Projects/soloprenuership/mcp/soloos-core/`

### Agent Layer (`src/soloos_core/agent/`)
| Module | Purpose |
|---|---|
| `task_queue.py` | SQLite-backed task queue with priority + retry |
| `world_model.py` | Business metrics snapshot (MRR, customers, health) |
| `founder_loop.py` | Event routing → task enqueue → autonomous execution |
| `executor.py` | LangGraph/Anthropic SDK agent executor |
| `action_registry.py` | Kill switch, tier enforcement, daily limits, dry run |

### Gateway Layer (`src/soloos_core/gateway/`)
| Module | Purpose |
|---|---|
| `http_bridge.py` | FastAPI REST + SSE server |
| `webhook_handler.py` | Stripe/GitHub/Intercom/Crisp webhooks → TaskQueue |

### Data Layer
| Module | Purpose |
|---|---|
| `context_db.py` | SQLite: kill signals, experiments, sessions, feedback |
| `analytics_db.py` | DuckDB: MRR, cohort analysis, metrics |
| `audit_log.py` | Append-only audit trail |
| `cache.py` | TTL-based caching decorator |

### Observability
- `observability.py`: `@instrument_tool` decorator — latency, errors, stats
- `scheduler.py`: APScheduler-based scheduled tasks (morning brief, etc.)

## Multi-Transport Access
```bash
# Claude Code (default — MCP stdio)
soloos-mcp

# REST API + MCP gateway (any HTTP client)
pip install "soloos-core[http]"
soloos-api --port 8765 --api-key my-secret-key
```

## Key Design Decisions
- **Fail-open**: All data layer failures log + continue (never crash on DB error)
- **Kill switch**: Any action blocked if kill switch active
- **Webhook security**: Fail-closed — 403 if env var not set (no pass-through)
- **Module-level imports**: FastAPI types + get_task_queue/get_founder_loop at module level (required for monkeypatching in tests)

## Test Suite
- **Location**: `mcp/soloos-core/tests/`
- **Run**: `cd mcp/soloos-core && python -m pytest tests/ -q --tb=short`
- **Results**: 168 passed, 7 skipped (DuckDB optional), 0 failed
- **Coverage**: unit (130 tests) + integration/webhooks (13) + smoke (4)

## Recent Fixes (2026-03-27)
1. `webhook_handler.py`: Moved `get_task_queue`, `get_founder_loop`, `Request`, `HTTPException`, `JSONResponse` to module level — fixes monkeypatching + `from __future__ import annotations` type resolution
2. `executor.py`: Whitespace fix line 154 `-(  _MAX...)` → `-(_MAX...)`
