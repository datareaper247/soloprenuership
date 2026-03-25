# SoloOS V10 — Architecture Design
**Version:** 10.0
**Date:** 2026-03-26
**Status:** Design Phase — Pre-Implementation
**Author:** Deep research synthesis: Gemini Pro architectural analysis × brainstorm swarm × codebase audit

---

## 1. Executive Summary

SoloOS V10 is not an incremental version bump. It is a ground-up architectural rethinking of what a founder intelligence co-pilot should be.

**V9 state of the art:** 31 MCP tools, 5 modules, live Stripe/Mercury integration, 5-seat AI council, BM25 knowledge search, causal simulation engine, kill signal enforcement. ~9,748 lines of Python.

**V10 north star:** A *self-improving causal intelligence engine* — a system that not only answers questions about your business but traces the causal chains behind outcomes, simulates futures, queries its own past, and evolves its own toolset.

The architectural gap between V9 and what engineers at Anthropic, Google DeepMind, or Linear would ship comes down to **five systemic weaknesses:**

| Weakness | V9 Symptom | V10 Fix |
|----------|-----------|---------|
| Brittle data layer | Regex-parsed markdown, silent failures | Pydantic-validated YAML + SQLite |
| No retrieval intelligence | BM25 on 40 items, no semantic capability | Tag-indexed structured lookup + optional vector layer |
| Zero observability | No metrics, no timing, no error rates | structlog + Prometheus-lite instrumentation |
| API cost bleed | Raw Claude calls in council, raw HTTP in intel | Multi-layer disk cache with TTL |
| No test safety net | 0 tests, every refactor is risky | pytest suite with smoke + unit + integration tiers |

Fix these five, then the bold capabilities (Pre-mortem Oracle, Temporal Echo Chamber, Reflexive Metasystem) become buildable without chaos.

---

## 2. V10 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         MCP CLIENT                              │
│              (Claude Code, Claude Desktop, etc.)                │
└──────────────────────────┬──────────────────────────────────────┘
                           │  stdio transport (MCP protocol)
┌──────────────────────────▼──────────────────────────────────────┐
│                    FastMCP Server (server.py)                   │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │  Tool Layer │  │  Middleware  │  │  Observability         │ │
│  │  (31 tools) │  │  - Cache     │  │  - structlog           │ │
│  │  exposed    │  │  - Timing    │  │  - tool_call_log.jsonl │ │
│  │  via @mcp   │  │  - Retry     │  │  - cost_tracker        │ │
│  └──────┬──────┘  └──────────────┘  └────────────────────────┘ │
└─────────┼───────────────────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────────────────┐
│                      Intelligence Layer                         │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  tools/                                                    │ │
│  │  ├── memory.py      Kill signals, context files, log       │ │
│  │  ├── decisions.py   Causal chains, simulation, council     │ │
│  │  ├── financial.py   Stripe, Mercury, unit economics        │ │
│  │  ├── intelligence.py HN, Reddit, Jina, market signals      │ │
│  │  └── agents.py      Multi-seat AI council (cached)         │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────────────────┐
│                      Data Layer (V10 NEW)                       │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  Knowledge Base  │  │  Context Store   │  │  Cache Store │ │
│  │  YAML + Pydantic │  │  SQLite DB       │  │  diskcache   │ │
│  │  Validated load  │  │  Decisions/Exps  │  │  LLM + HTTP  │ │
│  │  Tag-indexed     │  │  Kill signals    │  │  TTL-aware   │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. The 10 Universal Principles (Applied to SoloOS)

Synthesized from architectural analysis of Notion AI, Linear, Cursor, GitHub Copilot, Perplexity, Superhuman, Vercel AI SDK, and Replit Ghostwriter:

### P1: Context is King, Actively Assembled
World-class tools craft prompts as artifacts, not strings. SoloOS must move from "stuff everything in" to structured context assembly: stage-aware relevance scoring, pattern tag matching, recency weighting.

**V10 implementation:** `context_assembler.py` — a dedicated module that, given a query + founder stage, returns ranked context chunks from KB + decision log + live signals.

### P2: Strong Data Model Precedes Intelligence
Linear's AI works because it sits on top of impeccably structured issue data. Notion AI works because blocks are queryable. SoloOS V9 sits on top of regex-parsed markdown — the AI's context is as reliable as the parser.

**V10 implementation:** Migrate all context files to YAML frontmatter + SQLite. Pydantic models enforce schemas at load time, not at query time.

### P3: Hybrid Retrieval > Single Strategy
Cursor combines vector search + grep. Perplexity combines web search + source ranking. For a 40-item KB: BM25 is overkill AND too weak. Replace with tag-indexed structured lookup (O(1), deterministic) + semantic boosting for fuzzy queries.

**V10 implementation:** `kb_v2.py` — tag-indexed dict lookup primary, BM25 as a fallback only if tag match returns <2 results.

### P4: Multi-Layer Caching is Non-Negotiable
SoloOS fires raw HTTP requests on every market signal query and raw Claude API calls on every council. Identical queries cost real money and real seconds.

**V10 implementation:** `diskcache` with TTL layers:
- LLM responses: 24h TTL (council answers don't change minute-to-minute)
- HTTP market signals: 1h TTL (HN/Reddit)
- KB search results: session TTL (in-memory, no disk needed)

### P5: Streaming for Perceived Performance
Council brief takes 15-30s. No feedback during that time = broken feel. Even if total time is identical, streaming first tokens in 2s feels 5× faster.

**V10 implementation:** `@mcp.tool()` functions that delegate to long LLM chains should yield partial results progressively. FastMCP supports streaming via generator tools.

### P6: Observability as Architecture, Not Afterthought
Linear monitors every sync operation. Cursor tracks index freshness. SoloOS has zero visibility into which tools are slow, which fail silently, or which cost the most.

**V10 implementation:** `observability.py` — `structlog`-based JSON logging to `~/.soloos/logs/tool_calls.jsonl`. Every tool call: name, duration_ms, cache_hit, cost_estimate. Queryable post-hoc.

### P7: Build for Trust Through Transparency
Perplexity's citations are the product. Cursor's `@` commands make the AI's brain visible. SoloOS recommendations feel like a black box.

**V10 implementation:** Every tool response that involves KB lookup includes a `sources` array: which pattern IDs were retrieved, which founder cases matched, which live signal was used. Traceable reasoning.

### P8: Feedback Loop as Flywheel
GitHub Copilot's telemetry loop is its moat. For a solo-founder tool, the equivalent is tracking which recommendations the founder acted on vs. ignored.

**V10 implementation:** `feedback.py` — simple `thumbs_up(tool_call_id)` / `thumbs_down(tool_call_id, reason)` tools. Log to SQLite. Over 3 months, this dataset identifies which patterns actually help vs. noise.

### P9: The Workflow Integration Principle
Copilot succeeded because it's in the editor, not a separate tab. SoloOS is already in Claude Code — but it needs to feel like a natural extension of founder thinking, not a tool you "invoke."

**V10 implementation:** Smart defaults, context-carry between tool calls, automatic morning brief on session start. The system should know what you last worked on and pick up where it left off.

### P10: Self-Improvement Loop
The most audacious principle: the system should be able to analyze its own usage patterns and propose improvements to itself.

**V10 implementation:** `reflexive.py` — a tool that reads `tool_calls.jsonl`, identifies the slowest tools, the most expensive patterns, the highest-miss-rate queries, and drafts improvement proposals.

---

## 4. V10 Module Architecture

### 4.1 New Modules

```
src/soloos_core/
├── server.py                 # Entry point — unchanged interface
├── tools/
│   ├── memory.py             # Existing + kill signal improvements
│   ├── decisions.py          # Existing + Pre-mortem Oracle
│   ├── financial.py          # Existing + Option-Value Matrix
│   ├── intelligence.py       # Existing + HTTP caching
│   └── agents.py             # Existing + LLM call caching
├── data/                     # NEW — Data Layer
│   ├── __init__.py
│   ├── kb_v2.py              # Tag-indexed KB (replaces kb_loader.py BM25)
│   ├── context_db.py         # SQLite-backed context store (replaces markdown files)
│   ├── cache.py              # diskcache wrapper with TTL tiers
│   └── schemas.py            # Pydantic models for all entities
├── core/                     # NEW — Cross-cutting concerns
│   ├── __init__.py
│   ├── observability.py      # structlog + tool call metrics
│   ├── context_assembler.py  # Smart context assembly for tools
│   └── reflexive.py          # Self-analysis and improvement proposals
├── kb_loader.py              # DEPRECATED — migration shim only
└── log_manager.py            # DEPRECATED — replaced by context_db.py
```

### 4.2 Dependencies (V10 additions to pyproject.toml)

```toml
dependencies = [
    "mcp[cli]>=1.0.0",
    "anthropic>=0.40.0",
    # V10 additions
    "diskcache>=5.6.0",          # Multi-tier disk caching
    "structlog>=24.0.0",         # Structured logging
    "python-frontmatter>=1.1.0", # YAML frontmatter parsing for KB migration
    "pydantic>=2.0.0",           # Schema validation (likely already transitive)
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-mock>=3.14.0",
    "pytest-asyncio>=0.23.0",
]
```

**What we do NOT add:**
- No ChromaDB — vector search for 40 items is over-engineering
- No Neo4j — graph DB for one founder is over-engineering
- No Redis — single-machine diskcache is sufficient
- No Celery — async background jobs are overkill for stdio MCP

**Why:** The key architectural insight from the Gemini audit is "apply the right tool for the scale." A solo-founder tool running on one machine should remain installable with `pip install soloos-core`. Every dependency is a deployment friction point.

---

## 5. Data Layer Design (V10 Core Upgrade)

### 5.1 KB V2 — Tag-Indexed Lookup

The current `kb_loader.py` uses BM25 scoring implemented in pure Python across 40 patterns. This is algorithmically correct but architecturally wrong for this scale. The insight from Cursor + Perplexity: **hybrid retrieval is better than single-strategy retrieval**.

For 40 items, tag-based structured lookup is faster, more deterministic, and easier to debug than BM25.

```python
# data/kb_v2.py

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Pattern:
    id: str                    # "P01"
    name: str
    category: str
    tags: list[str]            # ["pricing", "pmf", "b2b"] — NEW, explicit
    situation: str
    pattern: str
    real_example: str
    kill_signal: str
    reversibility: int         # 1-10 as int, not str — NEW
    mrr_stage: list[str]       # ["$0", "$1-5K", "$5-20K"] — NEW: stage gating

class KnowledgeBase:
    def __init__(self):
        self._by_id: dict[str, Pattern] = {}
        self._by_tag: dict[str, list[Pattern]] = {}
        self._by_stage: dict[str, list[Pattern]] = {}

    def lookup_by_id(self, pid: str) -> Optional[Pattern]:
        return self._by_id.get(pid)

    def search(self, query: str, stage: str = "", top_n: int = 5) -> list[Pattern]:
        """
        Hybrid retrieval:
        1. Tag match (O(1) dict lookup) — primary
        2. Stage filter — narrows results
        3. Keyword fallback only if tag match < 2 results
        Returns: ranked list with match_reason attached
        """
        # Step 1: Tag match
        query_lower = query.lower()
        tag_hits: set[str] = set()
        for tag in self._by_tag:
            if tag in query_lower:
                tag_hits.update(p.id for p in self._by_tag[tag])

        # Step 2: Stage filter
        candidates = [self._by_id[pid] for pid in tag_hits]
        if stage and candidates:
            stage_filtered = [p for p in candidates if not p.mrr_stage or stage in p.mrr_stage]
            candidates = stage_filtered if stage_filtered else candidates

        # Step 3: Keyword fallback for low-hit queries
        if len(candidates) < 2:
            keywords = [w for w in query_lower.split() if len(w) > 3]
            for p in self._by_id.values():
                if any(kw in p.situation.lower() or kw in p.pattern.lower() for kw in keywords):
                    if p not in candidates:
                        candidates.append(p)

        return candidates[:top_n]
```

**YAML knowledge base format** (replacing raw markdown headers):

```yaml
# knowledge-base/patterns/P01-levels-test.yaml
id: P01
name: The Levels Test
category: PRODUCT DECISIONS
tags: [scope, mvp, shipping, timeline]
mrr_stage: ["$0", "$1-5K"]
reversibility: 9
situation: MVP scope creeping beyond 2 weeks of solo work
pattern: |
  What's the version that ships Friday?
  If it can be a spreadsheet/form/manual process first — do that.
real_example: |
  Pieter Levels shipped Nomad List as a Google Sheet before writing a line of code.
  Marc Lou ships every ShipFast feature as a manual test first.
kill_signal: Feature shipped and used by 0 customers within 30 days of launch
```

**Migration path:** One-time script converts existing PATTERN_LIBRARY.md blocks into individual YAML files. `kb_loader.py` becomes a read-only migration shim.

### 5.2 Context DB — SQLite Replaces Markdown Files

The current `context/` directory has 6 markdown files parsed by regex at runtime. This is the system's weakest architectural point: unstructured data used as a structured database.

```python
# data/context_db.py

import sqlite3
from pathlib import Path
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Decision(BaseModel):
    id: str                    # FL-001
    date: str
    type: str                  # Decision / Experiment / Pivot / Insight
    summary: str
    context: str
    hypothesis: str
    kill_signal: str
    kill_signal_due: str
    outcome: str = "PENDING"
    outcome_due: str = ""
    outcome_status: str = "⏳ Pending"
    pattern_applied: str = ""
    reversibility: int = 5

class BusinessContext(BaseModel):
    mrr: int = 0               # Actual integer, not "$5K MRR" string
    mrr_updated_at: str = ""
    icp: str = ""
    stage: str = ""
    top_channel: str = ""
    biggest_challenge: str = ""
    open_decisions: list[str] = []

class Experiment(BaseModel):
    id: str
    name: str
    hypothesis: str
    started_at: str
    metric: str                # What we're measuring
    target: str                # Success threshold
    status: str = "active"    # active / completed / abandoned
    result: str = ""
    days_elapsed: int = 0

class ContextDB:
    """
    SQLite-backed context store. Replaces all markdown context files.
    Single file: ~/.soloos/context.db
    """
    def __init__(self, db_path: Path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS decisions (
            id TEXT PRIMARY KEY,
            date TEXT, type TEXT, summary TEXT, context TEXT,
            hypothesis TEXT, kill_signal TEXT, kill_signal_due TEXT,
            outcome TEXT DEFAULT 'PENDING',
            outcome_due TEXT, outcome_status TEXT DEFAULT '⏳ Pending',
            pattern_applied TEXT, reversibility INTEGER DEFAULT 5
        );
        CREATE TABLE IF NOT EXISTS experiments (
            id TEXT PRIMARY KEY,
            name TEXT, hypothesis TEXT, started_at TEXT,
            metric TEXT, target TEXT, status TEXT DEFAULT 'active',
            result TEXT DEFAULT '', days_elapsed INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS business_context (
            key TEXT PRIMARY KEY, value TEXT, updated_at TEXT
        );
        CREATE TABLE IF NOT EXISTS customer_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT, source TEXT, tags TEXT, created_at TEXT
        );
        CREATE TABLE IF NOT EXISTS tool_calls (
            id TEXT PRIMARY KEY,
            tool_name TEXT, called_at TEXT,
            duration_ms INTEGER, cache_hit INTEGER DEFAULT 0,
            cost_estimate_cents REAL DEFAULT 0,
            feedback INTEGER DEFAULT 0  -- -1 bad, 0 neutral, 1 good
        );
        """)
        self.conn.commit()

    def get_overdue_kill_signals(self) -> list[dict]:
        """Core enforcement query — replaces regex log parsing."""
        today = datetime.now().strftime("%Y-%m-%d")
        rows = self.conn.execute("""
            SELECT id, summary, kill_signal, kill_signal_due, outcome_status
            FROM decisions
            WHERE outcome_status = '⏳ Pending'
            AND kill_signal_due < ?
            AND kill_signal != ''
            ORDER BY kill_signal_due ASC
        """, (today,)).fetchall()
        return [
            {"id": r[0], "summary": r[1], "kill_signal": r[2],
             "due": r[3], "status": r[4]}
            for r in rows
        ]
```

**Migration:** One-time script reads all existing `context/*.md` and `founder-log.md` files, parses them with the existing regex logic, and inserts into the SQLite DB. After migration, markdown files become human-readable snapshots (generated on demand), not the source of truth.

---

## 6. Caching Architecture

### 6.1 Multi-Tier Cache Design

```python
# data/cache.py

import diskcache
from pathlib import Path
from functools import wraps
from typing import Any, Callable

CACHE_ROOT = Path.home() / ".soloos" / "cache"

# TTL tiers
TTL_LLM = 86400      # 24h — council answers, pattern analysis
TTL_HTTP = 3600      # 1h  — HN, Reddit, Jina market signals
TTL_COMPUTED = 300   # 5m  — financial calculations with live data
TTL_SESSION = None   # No expiry — KB search within a session

_cache = diskcache.Cache(CACHE_ROOT, size_limit=500_000_000)  # 500MB limit

def cached(ttl: int, key_fn: Callable = None):
    """
    Decorator for caching tool results.

    Usage:
        @cached(TTL_HTTP)
        def fetch_hn_top_stories(limit: int) -> list:
            ...

        @cached(TTL_LLM, key_fn=lambda *a, **kw: f"council:{kw.get('decision')}")
        def run_council(decision: str, stage_mrr: str) -> dict:
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if key_fn:
                key = key_fn(*args, **kwargs)
            else:
                key = f"{fn.__module__}.{fn.__name__}:{args}:{sorted(kwargs.items())}"

            cached_val = _cache.get(key)
            if cached_val is not None:
                return cached_val

            result = fn(*args, **kwargs)
            _cache.set(key, result, expire=ttl)
            return result

        wrapper.cache_invalidate = lambda *a, **kw: _cache.delete(
            key_fn(*a, **kw) if key_fn else f"{fn.__module__}.{fn.__name__}:{a}:{sorted(kw.items())}"
        )
        return wrapper
    return decorator
```

**Application:**
```python
# In intelligence.py
@cached(TTL_HTTP)
def fetch_hn_top_stories(limit: int = 10) -> list[dict]: ...

@cached(TTL_HTTP)
def search_reddit(query: str, subreddit: str = "") -> list[dict]: ...

# In agents.py
@cached(TTL_LLM, key_fn=lambda decision, stage, **_: f"council:{hash(decision)}:{stage}")
def run_council_seats(decision: str, stage: str, ...) -> list[dict]: ...
```

### 6.2 Cache Invalidation Rules

| Cache Type | TTL | Invalidated When |
|------------|-----|-----------------|
| LLM council responses | 24h | `decision` text changes |
| HN top stories | 1h | Never manually — let TTL expire |
| Reddit searches | 1h | Never manually |
| Jina URL content | 4h | URL changes |
| Financial calculations | 5min | Stripe webhook / manual refresh |
| KB search results | Session | KB reload triggered |

---

## 7. Observability Design

```python
# core/observability.py

import structlog
import time
import uuid
from functools import wraps
from pathlib import Path
from contextlib import contextmanager

LOG_DIR = Path.home() / ".soloos" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.WriteLoggerFactory(
        file=(LOG_DIR / "tool_calls.jsonl").open("a")
    ),
)

log = structlog.get_logger()

def instrument_tool(fn):
    """
    Decorator for MCP tools. Logs: call, duration, cache_hit, cost estimate.

    All tool calls end up in ~/.soloos/logs/tool_calls.jsonl as JSON lines.
    Queryable with: jq 'select(.tool_name == "council_brief")' ~/.soloos/logs/tool_calls.jsonl
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        call_id = str(uuid.uuid4())[:8]
        start = time.perf_counter()

        try:
            result = fn(*args, **kwargs)
            duration_ms = int((time.perf_counter() - start) * 1000)
            log.info(
                "tool_call",
                tool_name=fn.__name__,
                call_id=call_id,
                duration_ms=duration_ms,
                success=True,
                args_preview=str(args)[:100],
            )
            return result
        except Exception as e:
            duration_ms = int((time.perf_counter() - start) * 1000)
            log.error(
                "tool_call_failed",
                tool_name=fn.__name__,
                call_id=call_id,
                duration_ms=duration_ms,
                error=str(e),
            )
            raise

    return wrapper
```

**Reflexive analysis** — `reflexive.py` reads `tool_calls.jsonl` and surfaces:
- Slowest tool (avg duration > 5s)
- Most called tool (usage pattern)
- Highest error rate tool
- Cache hit rate by tool
- Estimated total LLM cost this month

---

## 8. V10 Signature Features (Bold Capabilities)

The following features are V10's differentiators — what makes it reference-quality:

### 8.1 Pre-mortem Oracle

**What it does:** Before any decision with reversibility ≤5, runs a structured pre-mortem: what are the 3 most probable failure pathways, and what's the earliest detectable signal of each?

**Why it's world-class:** Transforms the kill signal system from reactive (we log what went wrong) to proactive (we name what could go wrong before it does).

```python
@mcp.tool()
def premortem_oracle(
    decision: str,
    stage_mrr: str,
    timeframe_days: int = 90
) -> str:
    """
    Structured pre-mortem for any decision.
    Returns: top 3 failure pathways + earliest detectable signals for each.
    Uses pattern KB + founder cases + causal chains.
    """
    # 1. Retrieve relevant failure patterns from KB
    # 2. Map decision type to _CAUSAL_CHAINS failure modes
    # 3. Run council with devil's advocate framing
    # 4. Return structured failure pathway map
```

**Architectural implementation:** Reuses `council_brief` infrastructure with a modified prompt template. Adds `failure_mode_db.yaml` to KB: a catalog of 50 known startup failure patterns mapped to signals.

### 8.2 Temporal Echo Chamber

**What it does:** Reconstruct the system's state at any past date and answer queries from that perspective. "What would you have told me about this decision 3 months ago?"

**Why it's world-class:** First system in the founder co-pilot space to offer temporal rollback of intelligence. Combats recency bias systematically.

```python
@mcp.tool()
def query_past_self(
    query: str,
    as_of_date: str,          # "2025-12-01"
    compare_to_now: bool = True
) -> str:
    """
    Query historical business state.
    Returns: what the system knew/recommended at that date + delta vs. now.
    """
    # 1. Pull decisions/experiments active as_of_date from context_db
    # 2. Pull business_context snapshot for that date
    # 3. Identify which patterns were relevant given that state
    # 4. If compare_to_now: generate delta analysis
```

**Architectural requirement:** `context_db.py` must store all mutations with `created_at` timestamps — enabling point-in-time queries. This is a Git-like immutable audit log, not an update-in-place model.

### 8.3 Decision Path Unraveler

**What it does:** When a kill signal triggers, trace backward through the decision log to identify the causal chain that led to the outcome.

**Why it's world-class:** `git blame` for business strategy. Makes accountability systematic and learning automatic.

```python
@mcp.tool()
def unravel_decision_path(
    outcome: str,             # "churn spike", "missed MRR target"
    outcome_date: str,
    lookback_days: int = 90
) -> str:
    """
    Causal chain reconstruction for a negative outcome.
    Returns: decision timeline → causal edges → root cause candidates.
    """
```

**Architectural implementation:** Queries `context_db` for all decisions in the lookback window. Uses `_CAUSAL_CHAINS` from `decisions.py` to build a directed graph of causal edges. Asks the council to rank root cause probability.

### 8.4 Reflexive Metasystem

**What it does:** Analyze the system's own usage patterns, identify improvement opportunities, and draft implementation plans.

**Why it's world-class:** A system that improves itself. The ultimate expression of a co-pilot: not just helping build the business, but building itself.

```python
@mcp.tool()
def analyze_self(
    period_days: int = 30
) -> str:
    """
    Analyze SoloOS's own usage patterns.
    Returns: slowest tools, highest-cost patterns, low-hit queries,
             top 3 improvement proposals with implementation sketches.
    """
    # 1. Read tool_calls.jsonl for period_days
    # 2. Compute: avg duration per tool, cache hit rates, error rates
    # 3. Identify: what queries returned 0 KB matches (gaps in knowledge base)
    # 4. Draft: 3 specific improvements (new tool, new pattern, cache config)
```

### 8.5 Strategic Option-Value Matrix

**What it does:** Every significant technical/product decision is evaluated for its impact on the value of future strategic options (go enterprise, open-source, raise, sell).

**Why it's world-class:** Connects daily execution decisions to long-term strategic flexibility. Prevents the unintentional closing of future doors.

```python
@mcp.tool()
def option_value_impact(
    decision: str,
    options_to_evaluate: list[str] = None  # default: ["enterprise", "open_source", "raise", "sell"]
) -> str:
    """
    Evaluate a decision's impact on strategic option value.
    Each option scored: +2 (opens), +1 (neutral-positive), 0 (neutral),
                        -1 (constrains), -2 (closes).
    """
```

---

## 9. Test Architecture

SoloOS V10 ships with tests. Not 80% coverage (that's a product company metric). The pragmatic founder-tool equivalent: **smoke tests + critical path tests**.

```
tests/
├── smoke/
│   └── test_server_starts.py      # Server imports cleanly, all 31 tools register
├── unit/
│   ├── test_kb_v2.py              # Tag-indexed search returns expected patterns
│   ├── test_context_db.py         # SQLite CRUD + kill signal queries
│   ├── test_cache.py              # Cache hit/miss, TTL expiry
│   └── test_log_manager.py        # Existing log parsing (regression)
└── integration/
    └── test_tool_contracts.py     # Each tool returns valid JSON, no crashes
```

**Smoke test (highest value, lowest effort):**
```python
# tests/smoke/test_server_starts.py

def test_all_tools_register():
    """Server starts and all expected tools are present."""
    import asyncio
    from soloos_core.server import mcp

    async def _check():
        tools = await mcp.list_tools()
        tool_names = {t.name for t in tools}
        assert len(tool_names) >= 31, f"Expected 31+ tools, got {len(tool_names)}"
        # Critical tools must be present
        assert "check_kill_signals_tool" in tool_names
        assert "council_brief" in tool_names
        assert "simulate_business_change" in tool_names
        return tool_names

    asyncio.run(_check())
```

---

## 10. Dead Code Elimination

**server_legacy.py: 3,772 lines — DELETE.**

This file is the original monolithic server before the V7 modular refactor. It is not imported anywhere. It is not referenced anywhere. It is a liability:
- Confuses anyone reading the codebase
- Inflates line count by ~40%
- Contains outdated patterns that contradict V7 architecture

**Action:** `git rm mcp/soloos-core/src/soloos_core/server_legacy.py`

**kb_loader.py:** Keep but mark as `DEPRECATED`. In V10, `data/kb_v2.py` is the primary KB module. `kb_loader.py` is preserved as a migration shim until all callsites are migrated.

**log_manager.py:** Keep as a migration shim. In V10, `data/context_db.py` is the source of truth. `log_manager.py` functions are wrapped to write to both markdown (for human-readability) and SQLite (for querying).

---

## 11. V10 Implementation Plan

### Phase 1 — Foundation (Week 1, ~6 hours)
**Goal:** Safety net exists. Data layer is solid. No regressions.

| Task | File | Effort |
|------|------|--------|
| Delete server_legacy.py | `git rm` | 5min |
| Add pytest, diskcache, structlog, python-frontmatter to pyproject.toml | `pyproject.toml` | 5min |
| Write smoke test (all tools register) | `tests/smoke/` | 30min |
| Write unit tests for critical log_manager functions | `tests/unit/` | 1h |
| Implement `data/cache.py` (diskcache wrapper) | `data/cache.py` | 1h |
| Apply `@cached(TTL_HTTP)` to all intelligence.py HTTP functions | `intelligence.py` | 30min |
| Apply `@cached(TTL_LLM)` to agents.py council calls | `agents.py` | 30min |

**Kill signal:** Smoke test passes. Cache reduces council test call cost by >80%. No existing tool behavior changes.

### Phase 2 — Data Layer (Week 2, ~8 hours)
**Goal:** SQLite replaces markdown for all structured data. Pydantic schemas enforced.

| Task | File | Effort |
|------|------|--------|
| Design `data/schemas.py` Pydantic models | `schemas.py` | 1h |
| Implement `data/context_db.py` SQLite store | `context_db.py` | 2h |
| Write migration script (markdown → SQLite) | `scripts/migrate_context.py` | 1h |
| Update `check_kill_signals_tool` to use SQLite query | `memory.py` | 30min |
| Update `log_decision` to write to SQLite | `memory.py` | 30min |
| Write unit tests for context_db | `tests/unit/` | 1h |
| Convert PATTERN_LIBRARY.md top 10 patterns to YAML | `knowledge-base/patterns/` | 2h |

**Kill signal:** All kill signal queries work from SQLite. Migration script runs without errors on existing data. Zero regression in tool outputs.

### Phase 3 — Intelligence Upgrades (Week 3, ~6 hours)
**Goal:** KB search is deterministic. Observability is live. Sources are transparent.

| Task | File | Effort |
|------|------|--------|
| Implement `data/kb_v2.py` tag-indexed KB | `kb_v2.py` | 2h |
| Migrate PATTERN_LIBRARY.md → YAML (all 36 patterns) | `knowledge-base/patterns/` | 2h |
| Implement `core/observability.py` | `observability.py` | 1h |
| Add `@instrument_tool` to top 10 most-called tools | `server.py` + modules | 30min |
| Add `sources` array to `get_decision_intelligence_brief` output | `decisions.py` | 30min |

**Kill signal:** KB search returns results with `match_reason` field. Observability log writes to `~/.soloos/logs/tool_calls.jsonl`. Pattern ID tracking shows in tool output.

### Phase 4 — Bold Features (Week 4+, ~10 hours)
**Goal:** V10 signature capabilities that justify the version number.

| Task | File | Effort |
|------|------|--------|
| Implement `premortem_oracle` tool | `decisions.py` | 2h |
| Implement `analyze_self` reflexive tool | `core/reflexive.py` | 2h |
| Implement `query_past_self` temporal tool | `memory.py` | 3h |
| Implement `option_value_impact` tool | `financial.py` | 2h |
| Write integration tests for new tools | `tests/integration/` | 1h |

**Kill signal:** All 4 new tools return valid JSON without crashing. `analyze_self` surfaces at least 1 actionable improvement from tool call logs.

---

## 12. V10 vs. V9: The Gap

| Dimension | V9 | V10 |
|-----------|----|----|
| Data integrity | Regex-parsed markdown, silent failures | Pydantic-validated YAML + SQLite, errors are loud |
| Retrieval | BM25 (correct algorithm, wrong scale) | Tag-indexed O(1) + keyword fallback |
| Caching | None | 3-tier diskcache (LLM 24h, HTTP 1h, computed 5m) |
| Observability | Zero | structlog → JSONL, queryable tool call log |
| Test coverage | 0 tests | Smoke + unit + integration tiers |
| Transparency | Black box answers | Sources array in every KB-backed response |
| Self-awareness | Cannot analyze itself | `analyze_self` tool queries own usage patterns |
| Temporal reasoning | Cannot query past state | `query_past_self` point-in-time reconstruction |
| Pre-mortem | Reactive kill signals | `premortem_oracle` proactive failure pathway mapping |
| Dead code | 3,772 lines of server_legacy.py | Deleted |
| Lines of code (approx) | ~9,748 | ~8,000 (cleaner) |

---

## 13. Multi-Protocol Gateway — Universal AI Compatibility

> **Design goal:** The same 33 tools accessible from any AI system, without changing a single line of tool code.

### 13.1 Transport Compatibility Matrix

| Client | Protocol | Entry Point | Auth |
|--------|----------|-------------|------|
| Claude Code | MCP stdio | `soloos-mcp` | none (local) |
| Claude Desktop | MCP stdio | `soloos-mcp` | none (local) |
| Cursor / Windsurf | MCP stdio | `soloos-mcp` | none (local) |
| n8n / Zapier | MCP SSE | `GET /sse` | API key header |
| Claude Desktop (HTTP mode) | MCP Streamable HTTP | `GET /mcp` | API key header |
| ChatGPT / GPTs | OpenAPI Actions | `GET /openapi.json` | API key header |
| LangChain / LlamaIndex | REST + JSON Schema | `GET /tools?format=langchain` | API key header |
| OpenAI SDK | Function calling | `GET /tools?format=openai` | API key header |
| Anthropic SDK | Tool use | `GET /tools?format=anthropic` | API key header |
| Gemini SDK | Function declarations | `GET /tools?format=gemini` | API key header |
| Any HTTP client | REST | `POST /tools/{name}` | API key header |

### 13.2 Gateway Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     AI CLIENTS                                   │
│  Claude Code   ChatGPT   LangChain   n8n   OpenAI SDK   Gemini  │
└────┬────────────────┬──────────┬──────┬──────────┬───────┬──────┘
     │                │          │      │          │       │
     │ MCP stdio      │ OpenAPI  │ REST │ MCP SSE  │ REST  │ REST
     │                │          │      │          │       │
┌────▼────────────────▼──────────▼──────▼──────────▼───────▼──────┐
│                   SoloOS Gateway (http_bridge.py)                │
│                                                                  │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────────────┐ │
│  │  /mcp        │  │  /sse          │  │  REST Endpoints       │ │
│  │  Streamable  │  │  MCP SSE       │  │  GET  /tools          │ │
│  │  HTTP (MCP)  │  │  (legacy)      │  │  POST /tools/{name}   │ │
│  └──────┬───────┘  └───────┬────────┘  │  GET  /schemas        │ │
│         │                  │           │  GET  /.well-known/   │ │
│         └──────────────────┘           │       ai-plugin.json  │ │
│                  │                     │  GET  /connect        │ │
│                  ▼                     └──────────┬────────────┘ │
│         ┌────────────────┐                        │              │
│         │  FastMCP.call_tool()                    │              │
│         │  (one call, any transport)              │              │
│         └────────────────┘                        │              │
│                  │                     ┌──────────▼────────────┐ │
│                  │                     │  schema_gen.py        │ │
│                  │                     │  MCP → OpenAI/Ant/    │ │
│                  │                     │  Gemini/LangChain     │ │
│                  │                     └───────────────────────┘ │
└──────────────────┼───────────────────────────────────────────────┘
                   │
         ┌─────────▼──────────┐
         │  FastMCP (server.py)│  ← same 33 tools, unchanged
         │  + Cache + Observ. │
         └────────────────────┘
```

### 13.3 Schema Conversion

MCP `tool.inputSchema` is already JSON Schema. The difference between all major LLMs is only the **wrapper object**. `schema_gen.py` converts once from FastMCP's `Tool` objects:

```python
# One source schema (MCP Tool object)
tool.inputSchema = {"type": "object", "properties": {"decision": {"type": "string"}}}

# OpenAI / Groq / Mistral / Together / Ollama:
{"type": "function", "function": {"name": ..., "parameters": {...}}}

# Anthropic Claude API:
{"name": ..., "input_schema": {...}}

# Google Gemini:
{"name": ..., "parameters": {...}}

# LangChain / LlamaIndex:
{"name": ..., "description": ..., "parameters": {"title": ..., ...}}
```

### 13.4 ChatGPT Actions Setup

SoloOS exposes a ChatGPT Actions manifest at `/.well-known/ai-plugin.json`. To connect to ChatGPT:

1. Run `soloos-api --host 0.0.0.0 --port 8765`
2. Expose via ngrok: `ngrok http 8765`
3. In ChatGPT: Create GPT → Actions → Import from URL → `https://<ngrok-url>/openapi.json`
4. Set API key header: `X-SoloOS-API-Key: <your-key>`

### 13.5 Claude Desktop HTTP Mode

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "soloos-http": {
      "url": "http://localhost:8765/mcp"
    }
  }
}
```

### 13.6 Running the Gateway

```bash
# Install with HTTP extras
pip install "soloos-core[http]"

# Start REST/MCP gateway (all protocols on one port)
soloos-api --port 8765 --api-key my-secret-key

# Or: only stdio MCP (Claude Code, Cursor, Windsurf)
soloos-mcp

# Or: SSE transport (n8n)
soloos-mcp --transport sse

# Check connection guide for your AI client
curl http://localhost:8765/connect
```

### 13.7 LangChain Integration Example

```python
import httpx

# Fetch tools in LangChain format
resp = httpx.get("http://localhost:8765/tools?format=langchain",
                 headers={"X-SoloOS-API-Key": "my-key"})
tools_schema = resp.json()["tools"]

# Call a tool
result = httpx.post("http://localhost:8765/tools/council_brief",
                    json={"decision": "Should I raise prices?", "stage_mrr": "$8K MRR"},
                    headers={"X-SoloOS-API-Key": "my-key"})
print(result.json()["result"])
```

### 13.8 Design Principles

1. **One codebase, zero duplication.** All tool logic lives in `tools/*.py`. The gateway is a thin transport adapter.
2. **Schema generation is stateless.** `schema_gen.py` is a pure function — input MCP Tool, output dict. No side effects.
3. **MCP-first, REST-secondary.** stdio MCP is the primary interface. REST exists for clients that can't speak MCP.
4. **Fail-open auth.** If `SOLOOS_API_KEY` is unset, all requests are allowed (local dev). Set it when exposed publicly.
5. **ChatGPT Actions are first-class.** The `/.well-known/ai-plugin.json` manifest is always present, even without ChatGPT configuration.

---

## 14. What We Are NOT Building (and Why)

**Vector search (ChromaDB, FAISS):** For 40-150 patterns, vector search adds ~200ms latency and a deployment dependency for marginal quality gain over tag-indexed lookup. Revisit at 500+ KB items.

**Graph database (Neo4j, Memgraph):** Single-user, single-machine tool. The `_CAUSAL_CHAINS` dict + SQLite joins provide equivalent capability at zero ops overhead.

**Redis:** `diskcache` is Redis-lite for single-machine use. Same API, zero ops.

**Streaming responses:** FastMCP's stdio transport doesn't support streaming in the same way HTTP servers do. The right V10 investment is caching (reduces latency) not streaming architecture.

**Multi-tenancy:** SoloOS is a personal intelligence system. Multi-tenancy is a V20 problem if SoloOS ever becomes a product. Building it now is premature.

**Fine-tuning:** The knowledge base is <100 items. RAG is the right architecture. Fine-tuning requires thousands of examples and a training loop. Not warranted.

---

## 14. Definition of "Done" for V10

V10 is done when:

1. `pytest` runs without errors (smoke + unit + integration)
2. `server_legacy.py` is deleted from the repository
3. At least one council call shows cache hit in observability log (cost savings confirmed)
4. `check_kill_signals_tool` queries SQLite (not markdown regex)
5. `analyze_self` returns a valid response with ≥1 improvement proposal
6. `premortem_oracle` returns a valid 3-pathway failure analysis
7. CLAUDE.md references V10 tools in routing table
8. All 31 existing tools continue to pass smoke tests

---

*This document is the single source of truth for SoloOS V10 design. Implementation follows Phase 1 → 4 in order. Each phase has a kill signal. If a phase's kill signal is not met within its window, it is redesigned before Phase N+1 begins.*

*Generated: 2026-03-26 via parallel Gemini Pro research swarms × codebase audit × lateral brainstorm synthesis.*
