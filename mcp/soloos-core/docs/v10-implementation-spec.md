# SoloOS V10 — Implementation Specification

**Status:** Approved for implementation
**Date:** 2026-03-26
**Scope:** Phases A, B, C, D, E, F, G, H, I
**Rule:** Zero breaking changes. All 19 existing tests must pass after every phase.

---

## Repository Layout

```
mcp/soloos-core/
├── src/soloos_core/
│   ├── server.py              # ← DO NOT MODIFY (entry point)
│   ├── log_manager.py         # ← Phase B adds SQLite adapter (keep all existing functions)
│   ├── kb_loader.py           # ← Phase KB adds YAML loader (keep existing as fallback)
│   ├── data/
│   │   ├── cache.py           # ← existing (do not modify)
│   │   ├── analytics_db.py    # ← Phase A: NEW
│   │   ├── context_db.py      # ← Phase B: NEW
│   │   └── connectors/        # ← Phase C/D/J: NEW directory
│   │       ├── __init__.py
│   │       ├── base.py        # connector protocol
│   │       ├── stripe_connector.py
│   │       ├── mercury_connector.py
│   │       └── posthog_connector.py
│   ├── core/
│   │   ├── observability.py   # ← existing (do not modify)
│   │   └── scheduler.py       # ← Phase F: NEW
│   ├── kb/
│   │   ├── __init__.py        # ← Phase KB: NEW
│   │   └── kb_v2.py           # ← Phase KB: NEW (tag-indexed loader)
│   └── tools/
│       └── ... (no modifications unless adding data-driven variants)
├── dashboard/
│   └── app.py                 # ← Phase I: NEW (Streamlit)
├── tests/
│   ├── smoke/                 # existing
│   ├── unit/
│   │   ├── test_cache.py      # existing
│   │   ├── test_observability.py  # existing
│   │   ├── test_analytics_db.py   # ← Phase A: NEW
│   │   ├── test_context_db.py     # ← Phase B: NEW
│   │   └── test_scheduler.py      # ← Phase F: NEW
│   └── integration/
│       └── test_connectors.py     # ← Phase C: NEW (skipped if no API keys)
└── pyproject.toml             # add deps per phase
```

---

## Phase A — DuckDB Analytics Store

**File:** `src/soloos_core/data/analytics_db.py`
**Dep:** `duckdb>=0.10.0` (add to pyproject.toml)
**Test:** `tests/unit/test_analytics_db.py`

### Schema

```sql
-- Revenue events (from Stripe connector)
CREATE TABLE IF NOT EXISTS revenue_events (
    id VARCHAR PRIMARY KEY,
    source VARCHAR NOT NULL,          -- 'stripe', 'paddle', etc.
    event_type VARCHAR NOT NULL,      -- 'charge.succeeded', 'subscription.deleted'
    customer_id VARCHAR,
    amount_cents INTEGER,
    currency VARCHAR DEFAULT 'usd',
    mrr_delta_cents INTEGER,          -- +N for new/expansion, -N for churn
    metadata JSON,
    occurred_at TIMESTAMP NOT NULL,
    synced_at TIMESTAMP DEFAULT current_timestamp
);

-- User/product events (from PostHog/Mixpanel)
CREATE TABLE IF NOT EXISTS user_events (
    id VARCHAR PRIMARY KEY,
    source VARCHAR NOT NULL,
    event_name VARCHAR NOT NULL,
    user_id VARCHAR,
    properties JSON,
    occurred_at TIMESTAMP NOT NULL,
    synced_at TIMESTAMP DEFAULT current_timestamp
);

-- Sync state (last successful sync per source)
CREATE TABLE IF NOT EXISTS sync_state (
    source VARCHAR PRIMARY KEY,
    last_synced_at TIMESTAMP,
    last_cursor VARCHAR,
    status VARCHAR DEFAULT 'ok'
);
```

### Key Views (compute KPIs)

```sql
-- MRR as of today
CREATE VIEW IF NOT EXISTS v_mrr AS
SELECT
    date_trunc('month', occurred_at) AS month,
    SUM(mrr_delta_cents) / 100.0 AS mrr_dollars
FROM revenue_events
GROUP BY 1 ORDER BY 1;

-- Monthly churn rate
CREATE VIEW IF NOT EXISTS v_churn AS
SELECT
    date_trunc('month', occurred_at) AS month,
    COUNT(CASE WHEN mrr_delta_cents < 0 AND event_type LIKE '%deleted%' THEN 1 END) AS churned,
    COUNT(DISTINCT customer_id) AS total_customers
FROM revenue_events
GROUP BY 1;
```

### Python API (what other modules use)

```python
class AnalyticsDB:
    def __init__(self, db_path: str = "~/.soloos/analytics.duckdb"): ...
    def insert_events(self, table: str, rows: list[dict]) -> int: ...
    def query(self, sql: str, params: list = None) -> list[dict]: ...
    def get_current_mrr(self) -> float: ...
    def get_mrr_trend(self, months: int = 6) -> list[dict]: ...
    def get_churn_rate(self) -> float: ...
    def get_sync_state(self, source: str) -> dict: ...
    def update_sync_state(self, source: str, cursor: str) -> None: ...

# Module-level singleton
_db: AnalyticsDB | None = None
def get_analytics_db() -> AnalyticsDB: ...
```

### Quality Gates
- [ ] DuckDB file created at `~/.soloos/analytics.duckdb` on first use
- [ ] Schema idempotent (can call `init()` multiple times safely)
- [ ] Fails open — if DuckDB not installed, returns empty results with warning
- [ ] `test_analytics_db.py`: 6+ tests covering schema init, insert, query, views

---

## Phase B — SQLite Operational Store

**File:** `src/soloos_core/data/context_db.py`
**Dep:** `sqlite3` (stdlib — zero new deps)
**Modified:** `log_manager.py` (adapter layer only — all existing function signatures UNCHANGED)
**Test:** `tests/unit/test_context_db.py`

### Schema

```sql
CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,              -- "FL-001" format preserved
    date TEXT NOT NULL,
    situation TEXT NOT NULL,
    decision TEXT NOT NULL,
    kill_signal TEXT,
    kill_signal_date TEXT,            -- ISO date
    outcome TEXT,                     -- filled later
    outcome_date TEXT,
    tags TEXT,                        -- comma-separated
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY,
    hypothesis TEXT NOT NULL,
    status TEXT DEFAULT 'running',    -- running, completed, abandoned
    started_at TEXT,
    completed_at TEXT,
    result TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    context_snapshot TEXT,            -- JSON
    tools_used TEXT                   -- JSON array
);

CREATE TABLE IF NOT EXISTS feedback (
    id TEXT PRIMARY KEY,
    call_id TEXT NOT NULL,            -- from observability log
    tool_name TEXT,
    rating INTEGER,                   -- 1-5
    reason TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
```

### Migration Strategy
- On first init, `context_db.py` reads existing markdown files via `log_manager.py`
- Imports all entries into SQLite
- Sets a `migration_done` flag in `sync_state` table
- After migration, `log_manager.py` adapts to write to SQLite AND markdown (dual-write for safety)
- All existing `log_manager.py` functions MUST keep identical signatures

### Quality Gates
- [ ] All 19 existing tests still pass
- [ ] Migration runs once and is idempotent
- [ ] `test_context_db.py`: 8+ tests covering CRUD, migration, kill signal check

---

## Phase C — Stripe + Mercury Connectors

**Files:** `src/soloos_core/data/connectors/base.py`, `stripe_connector.py`, `mercury_connector.py`
**Deps:** `stripe>=7.0.0`, `httpx>=0.27.0` (Mercury has no official SDK)
**Tests:** `tests/integration/test_connectors.py` (skipped unless `STRIPE_API_KEY` set)

### Connector Protocol (base.py)

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class SyncResult:
    source: str
    rows_synced: int
    cursor: str | None
    error: str | None = None

class BaseConnector(ABC):
    """All connectors implement this interface."""

    source_name: str  # e.g. "stripe"

    @abstractmethod
    def is_configured(self) -> bool:
        """Return True if required env vars are set."""

    @abstractmethod
    def sync(self, since_cursor: str | None = None) -> SyncResult:
        """
        Fetch new events since cursor, write to AnalyticsDB.
        Must be idempotent (safe to call multiple times).
        Must fail open — never raise, always return SyncResult with error.
        """
```

### Stripe Connector
- Reads: `STRIPE_API_KEY` env var
- Fetches: charges, subscriptions, customer events
- Computes: `mrr_delta_cents` per event
- Writes to: `revenue_events` table in DuckDB
- Pagination: uses Stripe's `starting_after` cursor

### Mercury Connector
- Reads: `MERCURY_API_KEY` env var
- Fetches: account balances, transactions
- Writes to: new `banking_events` table in DuckDB
- Updates: `sync_state` table

### Quality Gates
- [ ] Both connectors implement `BaseConnector` protocol
- [ ] `is_configured()` returns False gracefully if no API key — never crash
- [ ] Integration tests skipped unless API key env var present
- [ ] `sync()` is idempotent — duplicate events ignored via PRIMARY KEY conflict

---

## Phase D — PostHog Connector

**File:** `src/soloos_core/data/connectors/posthog_connector.py`
**Dep:** `posthog>=3.0.0`
**Config:** `POSTHOG_API_KEY`, `POSTHOG_HOST` (default: app.posthog.com)

- Fetches: events, person properties, cohorts
- Computes: DAU, WAU, retention day-1/day-7/day-30
- Writes to: `user_events` table in DuckDB

---

## Phase E — Data-Driven Tools

**Modified:** `src/soloos_core/tools/financial.py`, `tools/decisions.py`
**No new files** — just update existing tool functions to check DuckDB first

### Pattern for every tool upgrade:

```python
def calculate_unit_economics(arpu=None, churn_rate_monthly_pct=None, ...):
    # Try live data first
    if arpu is None or churn_rate_monthly_pct is None:
        db = get_analytics_db()
        if db.has_data():
            arpu = arpu or db.get_current_arpu()
            churn_rate_monthly_pct = churn_rate_monthly_pct or db.get_churn_rate() * 100

    # Fall back to manual input (existing logic unchanged)
    if arpu is None:
        return json.dumps({"error": "No Stripe data connected and no manual input provided"})

    # ... existing calculation logic unchanged
```

### Tools to upgrade (Phase E):
- `calculate_unit_economics` → reads ARPU, churn from DuckDB if available
- `calculate_runway` → reads cash from Mercury, MRR from Stripe if available
- `score_pmf` → reads retention cohorts from PostHog if available
- `get_mrr_live` → now reads from DuckDB cache (not raw Stripe API every call)
- `get_runway_live` → now reads from DuckDB cache

---

## Phase F — APScheduler Automation

**File:** `src/soloos_core/core/scheduler.py`
**Dep:** `apscheduler>=3.10.0`
**Config:** `~/.soloos/scheduler-config.yaml`
**Test:** `tests/unit/test_scheduler.py`

### scheduler-config.yaml schema

```yaml
enabled: true
timezone: "America/New_York"

delivery:
  slack_webhook_url: ""       # SOLOOS_SLACK_WEBHOOK env var or explicit
  ntfy_topic: ""              # e.g. "my-soloos-alerts"
  email_to: ""
  email_smtp_host: ""
  email_smtp_port: 587

jobs:
  morning_brief:
    enabled: true
    cron: "0 7 * * *"         # 07:00 daily
  kill_signal_check:
    enabled: true
    cron: "0 9 * * *"         # 09:00 daily
  data_sync:
    enabled: true
    cron: "0 * * * *"         # every hour
  weekly_review:
    enabled: true
    cron: "0 9 * * 1"         # Monday 09:00
  monthly_investor_draft:
    enabled: false
    cron: "0 8 1 * *"         # 1st of month 08:00
```

### Scheduler class

```python
class SoloOSScheduler:
    def start(self) -> None: ...           # non-blocking, background thread
    def stop(self) -> None: ...
    def run_now(self, job_name: str) -> str: ...   # manual trigger
    def list_jobs(self) -> list[dict]: ...
    def next_run(self, job_name: str) -> str: ...

def get_scheduler() -> SoloOSScheduler: ...  # module-level singleton
```

### Delivery functions

```python
def deliver_slack(message: str, webhook_url: str) -> bool: ...
def deliver_ntfy(message: str, topic: str) -> bool: ...
def deliver_email(subject: str, body: str, config: dict) -> bool: ...

def deliver(message: str, subject: str = "") -> list[str]:
    """Deliver to all configured channels. Returns list of channels used."""
```

### Quality Gates
- [ ] Scheduler starts without error when no delivery channels configured
- [ ] All jobs fail open (error is logged, never crashes scheduler)
- [ ] `test_scheduler.py`: 6+ tests (config load, job listing, delivery mock)

---

## Phase G — GrowthBook A/B Testing Integration

**File:** `src/soloos_core/data/growthbook_client.py`
**Dep:** `growthbook>=1.0.0`
**External:** GrowthBook self-hosted (Docker — documented, not automated)

### Setup doc (not code):
```
# One-time GrowthBook setup:
docker run -d -p 3100:3100 growthbook/growthbook
# Open http://localhost:3100, create account
# Set GROWTHBOOK_API_HOST=http://localhost:3100
# Set GROWTHBOOK_CLIENT_KEY=<from dashboard>
```

### Python API
```python
class GrowthBookClient:
    def create_experiment(self, name: str, hypothesis: str,
                          metric: str, variants: list) -> str: ...
    def get_experiment_results(self, experiment_id: str) -> dict: ...
    def track_conversion(self, experiment_id: str, variant: str, value: float): ...
    def list_experiments(self) -> list[dict]: ...
```

### New MCP tools (added to server.py):
- `create_ab_experiment(hypothesis, metric, variants)` — creates experiment
- `get_experiment_results(experiment_id)` — returns stats + recommendation
- `list_experiments()` — shows all running/completed experiments

---

## Phase H — Langfuse Observability

**File:** `src/soloos_core/core/observability.py` (EXTEND, not replace)
**Dep:** `langfuse>=2.0.0`
**External:** Langfuse self-hosted (Docker — documented)

### Setup doc:
```
docker-compose -f docker/langfuse-compose.yml up -d
# Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY
# Set LANGFUSE_HOST=http://localhost:3000
```

### Integration:
- Extend existing `@instrument_tool` decorator to also send to Langfuse if configured
- Fail open — if Langfuse not configured, existing JSONL logging continues unchanged
- New `rate_recommendation(call_id, score, reason)` MCP tool logs to Langfuse + SQLite

---

## Phase I — Streamlit Dashboard

**File:** `dashboard/app.py`
**Dep:** `streamlit>=1.35.0`, `plotly>=5.0.0`
**Run:** `cd mcp/soloos-core && streamlit run dashboard/app.py`

### Pages
1. **Morning Brief** — kill signals, experiments running, MRR chart, today's focus
2. **Decision History** — searchable table of all decisions + outcomes
3. **KPI Dashboard** — MRR, churn, runway, CAC/LTV charts (from DuckDB)
4. **Experiments** — A/B tests running + results (from GrowthBook)

### Quality Gates
- [ ] Dashboard renders without error when DuckDB has no data (empty state)
- [ ] Dashboard renders correctly with mock data
- [ ] All charts have `st.empty()` fallback for missing data sources

---

## Global Quality Gates (Every Phase)

- [ ] `cd mcp/soloos-core && python -m pytest tests/ -q` — all tests green
- [ ] No new import errors in `server.py`
- [ ] `soloos-mcp` (stdio MCP) still starts cleanly
- [ ] Each new module has `if __name__ == "__main__"` smoke test or dedicated test
- [ ] All env var dependencies documented in module docstring
- [ ] No hardcoded paths — all use `Path.home() / ".soloos" / ...`

---

## Dependency Additions (pyproject.toml)

```toml
[project.dependencies]  # add to existing list
"duckdb>=0.10.0",       # Phase A
"apscheduler>=3.10.0",  # Phase F

[project.optional-dependencies]
connectors = [
    "stripe>=7.0.0",        # Phase C
    "httpx>=0.27.0",        # Phase C Mercury
    "posthog>=3.0.0",       # Phase D
]
ab-testing = [
    "growthbook>=1.0.0",    # Phase G
]
observability = [
    "langfuse>=2.0.0",      # Phase H
]
dashboard = [
    "streamlit>=1.35.0",    # Phase I
    "plotly>=5.0.0",        # Phase I
]
http = [                    # existing
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
]
```
