# Autonomous AI Founder — Implementation Specification

**Repo root:** `mcp/soloos-core/`
**Current tests:** 80 passed, 7 skipped
**Current MCP tools:** 43
**Rule:** Zero breaking changes. All existing tests pass after every phase.

---

## Directory Layout (New Additions)

```
src/soloos_core/
├── core/
│   ├── action_registry.py    ← NS-0: permission tiers, kill switch, audit
│   └── audit_log.py          ← NS-0: append-only action audit trail
├── actions/                  ← Next-1: executable action implementations
│   ├── __init__.py
│   ├── base_action.py        ← BaseAction protocol
│   ├── email_action.py       ← Resend email
│   ├── deploy_action.py      ← Vercel + Railway
│   ├── social_action.py      ← Twitter/Buffer
│   ├── support_action.py     ← Intercom/Crisp webhook reply
│   └── dns_action.py         ← Cloudflare
├── agent/                    ← Next-2: persistent execution runtime
│   ├── __init__.py
│   ├── task_queue.py         ← SQLite-backed task queue
│   ├── world_model.py        ← Persistent business state
│   ├── executor.py           ← LangGraph-based agent runner
│   └── founder_loop.py       ← Main autonomous loop
├── agents/                   ← Next-3/4/5/6: specialized agent implementations
│   ├── __init__.py
│   ├── customer_success_agent.py   ← Next-3
│   ├── marketing_agent.py          ← Next-4
│   ├── engineering_agent.py        ← Next-5
│   ├── founder_agent.py            ← Next-6: orchestrator
│   └── crew.py                     ← Next-6: CrewAI team
└── gateway/
    └── webhook_handler.py    ← Next-2: event triggers (Stripe, GitHub, Intercom)

tests/
├── unit/
│   ├── test_action_registry.py
│   ├── test_audit_log.py
│   ├── test_task_queue.py
│   ├── test_world_model.py
│   ├── test_actions.py
│   └── test_agents.py
└── integration/
    └── test_autonomous_flow.py     ← e2e: trigger → queue → execute → audit
```

---

## NS-0: ActionRegistry + Audit Log

### `core/action_registry.py`

```python
"""
ActionRegistry — permission gating for all autonomous AI actions.

CRITICAL SAFETY RULES (enforced in code, not config):
1. Tier.LEGAL always requires approval. Cannot be configured away.
2. Kill switch (SOLOOS_AUTONOMOUS=false or ~/.soloos/kill_switch) blocks Tier 2+.
3. Budget limits are hard-coded ceilings. Config can only reduce, not increase.
4. AI cannot modify its own permissions. ActionRegistry is read-only to agents.
5. Every execution is logged to AuditLog before AND after.
"""

from enum import IntEnum
from dataclasses import dataclass, field
from typing import Callable, Any
from pathlib import Path
import os

class Tier(IntEnum):
    READ = 0        # no approval, no log required
    COMPUTE = 1     # no approval, logged
    COMMUNICATE = 2 # soft approval (daily limits), logged
    BUILD = 3       # soft approval (risk params), logged
    DEPLOY = 4      # hard approval OR within safe params
    SPEND = 5       # hard approval + budget enforcement
    LEGAL = 6       # ALWAYS human approval (cannot be configured away)

@dataclass
class ActionDefinition:
    name: str
    tier: Tier
    description: str
    reversible: bool
    daily_limit: int | None = None       # None = no limit
    per_tx_limit_usd: float | None = None
    requires_approval: bool | None = None  # None = use tier default

@dataclass
class ActionRequest:
    action: str
    params: dict
    reasoning: str
    agent_id: str = "founder"
    request_id: str = field(default_factory=lambda: ...)

@dataclass
class ActionResult:
    request_id: str
    action: str
    status: str      # "executed" | "queued_for_approval" | "blocked" | "dry_run"
    result: Any = None
    error: str | None = None
    audit_id: str | None = None

class ActionRegistry:
    """
    Gate for all autonomous AI actions.

    Usage:
        registry = get_action_registry()
        result = registry.execute(ActionRequest(
            action="send_email",
            params={"to": "...", "subject": "...", "body": "..."},
            reasoning="Customer asked about pricing 3 days ago"
        ))
    """

    def execute(self, request: ActionRequest) -> ActionResult: ...
    def is_kill_switch_active(self) -> bool: ...
    def get_daily_usage(self, action: str) -> int: ...
    def get_pending_approvals(self) -> list[dict]: ...
    def approve(self, request_id: str) -> ActionResult: ...
    def reject(self, request_id: str, reason: str = "") -> None: ...
    def get_permissions_summary(self) -> dict: ...
    def register_action(self, action: ActionDefinition,
                        handler: Callable) -> None: ...

def get_action_registry() -> ActionRegistry: ...  # singleton
```

### Kill Switch Detection

```python
def is_kill_switch_active() -> bool:
    """
    Kill switch is ON (actions blocked) if ANY of:
    1. env var SOLOOS_AUTONOMOUS is set to "false" or "0"
    2. file ~/.soloos/kill_switch exists
    3. env var SOLOOS_KILL_SWITCH is set to any value
    """
```

### Config (`~/.soloos/permissions.yaml`)

```yaml
autonomous_mode: true        # false = queue ALL Tier2+ for approval
dry_run: false               # true = log actions but don't execute

limits:
  communicate:
    email_per_day: 50
    social_posts_per_day: 3
    support_replies_per_day: 100
  spend:
    daily_usd: 50
    monthly_usd: 500
    per_transaction_usd: 100

approval_channel:
  slack_webhook: ""          # or SOLOOS_SLACK_WEBHOOK env var
  timeout_hours: 24          # auto-reject if no response
```

### `core/audit_log.py`

```python
"""
Append-only audit log for all autonomous actions.
Path: ~/.soloos/audit.jsonl
Format: one JSON object per line.

{
  "id": "uuid",
  "ts": "2026-03-26T07:00:00Z",
  "action": "send_email",
  "tier": 2,
  "agent_id": "founder",
  "params": {...},              # PII redacted for email/support actions
  "reasoning": "...",
  "status": "executed",
  "result": {...},
  "duration_ms": 340
}
"""

class AuditLog:
    def log(self, entry: dict) -> str: ...     # returns audit_id
    def query(self, filters: dict) -> list[dict]: ...
    def get_stats(self, hours: int = 24) -> dict: ...
    def export(self, path: Path) -> None: ...

def get_audit_log() -> AuditLog: ...
```

### New MCP Tools (add to server.py)

- `action_registry_status()` → permissions summary, kill switch state, daily usage
- `approve_action(request_id)` → human approves queued action
- `reject_action(request_id, reason)` → human rejects queued action
- `list_pending_approvals()` → all Tier 4+ actions awaiting approval
- `get_audit_log(hours=24)` → recent autonomous actions taken
- `set_autonomous_mode(enabled: bool)` → toggle kill switch

### Tests (`tests/unit/test_action_registry.py`, `test_audit_log.py`)

- Kill switch blocks Tier 2+ when env var set
- Kill switch does NOT block Tier 0-1 (read/compute)
- Daily limit enforced and reset
- Tier 6 (LEGAL) always returns "queued_for_approval" regardless of config
- Dry run mode logs but does not execute
- Audit log appends, never overwrites
- Approval timeout auto-rejects
- 10+ tests

---

## Next-1: Action Implementations

### `actions/base_action.py`

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ActionOutcome:
    success: bool
    data: dict
    error: str | None = None

class BaseAction(ABC):
    """All actions implement this interface."""
    action_name: str

    @abstractmethod
    def is_configured(self) -> bool:
        """True if required env vars/SDKs are present."""

    @abstractmethod
    def execute(self, params: dict) -> ActionOutcome:
        """Execute the action. MUST fail open — never raise."""

    def validate_params(self, params: dict) -> str | None:
        """Return error string or None if valid."""
        return None
```

### `actions/email_action.py` — Resend

```python
"""
Email action via Resend (https://resend.com).
Config: RESEND_API_KEY env var
Dep: resend>=2.0.0 (lazy import)

Usage:
    EmailAction().execute({
        "to": "customer@example.com",
        "from": "ai@yourcompany.com",
        "subject": "Re: your question",
        "body": "Hi ...",
        "reply_to": "support@yourcompany.com"
    })
"""
```

### `actions/deploy_action.py` — Vercel + Railway

```python
"""
Deploy action via Vercel API or Railway API.
Config:
    VERCEL_TOKEN + VERCEL_PROJECT_ID for Vercel
    RAILWAY_TOKEN + RAILWAY_PROJECT_ID for Railway
Dep: httpx>=0.27.0 (lazy import)

Supports:
    deploy_staging: always soft-approved
    deploy_production: requires approval (Tier 4)

Usage:
    DeployAction().execute({
        "target": "staging",   # or "production"
        "provider": "vercel",  # or "railway"
        "git_ref": "main"
    })
"""
```

### `actions/social_action.py` — Twitter/Buffer

```python
"""
Social media posting action.
Config:
    TWITTER_BEARER_TOKEN + TWITTER_API_KEY + TWITTER_API_SECRET
    BUFFER_TOKEN (alternative — schedules posts)
Dep: httpx (lazy)
Daily limit: 3 posts per platform (enforced by ActionRegistry)
"""
```

### `actions/support_action.py` — Intercom/Crisp

```python
"""
Customer support reply action.
Config:
    INTERCOM_TOKEN for Intercom
    CRISP_WEBSITE_ID + CRISP_TOKEN for Crisp
Dep: httpx (lazy)
Daily limit: 100 replies (enforced by ActionRegistry)
"""
```

### `actions/dns_action.py` — Cloudflare

```python
"""
DNS management via Cloudflare API.
Config: CLOUDFLARE_TOKEN + CLOUDFLARE_ZONE_ID
Dep: httpx (lazy)
Creates: A records, CNAME records, TXT records
"""
```

### New MCP Tools

- `take_action(action_type, params, reasoning)` → routes through ActionRegistry
- `list_available_actions()` → all registered actions + configuration status
- `test_action(action_type)` → dry-run test with mock params

### Dependencies (pyproject.toml — add to optional[actions])

```toml
actions = [
    "resend>=2.0.0",
]
# httpx already in connectors optional group
```

### Tests (`tests/unit/test_actions.py`)

- All actions return ActionOutcome when SDK missing (fail-open)
- All actions return ActionOutcome when unconfigured (is_configured=False)
- EmailAction validates required params (to, subject, body)
- DeployAction staging → soft-approved tier, production → hard-approved tier
- 8+ tests

---

## Next-2a: Task Queue + World Model

### `agent/task_queue.py`

```python
"""
SQLite-backed task queue for autonomous agent operations.
DB: reuses ~/.soloos/context.db (adds 'agent_tasks' table)

Schema:
    CREATE TABLE agent_tasks (
        id TEXT PRIMARY KEY,
        task_type TEXT NOT NULL,      -- 'morning_brief', 'respond_support', etc.
        priority INTEGER DEFAULT 5,   -- 1=critical, 10=low
        payload TEXT,                 -- JSON
        status TEXT DEFAULT 'pending', -- pending|running|done|failed|cancelled
        created_at TEXT,
        started_at TEXT,
        completed_at TEXT,
        result TEXT,                  -- JSON
        error TEXT,
        retry_count INTEGER DEFAULT 0,
        max_retries INTEGER DEFAULT 3,
        agent_id TEXT DEFAULT 'founder'
    );
"""

class TaskQueue:
    def enqueue(self, task_type: str, payload: dict,
                priority: int = 5, agent_id: str = "founder") -> str: ...
    def dequeue(self, agent_id: str = None) -> dict | None: ...
    def complete(self, task_id: str, result: dict) -> None: ...
    def fail(self, task_id: str, error: str) -> None: ...
    def list_pending(self) -> list[dict]: ...
    def list_recent(self, hours: int = 24) -> list[dict]: ...
    def cancel(self, task_id: str) -> None: ...
    def stats(self) -> dict: ...

def get_task_queue() -> TaskQueue: ...
```

### `agent/world_model.py`

```python
"""
Persistent World Model — the AI's understanding of the business at any moment.

Reads from: DuckDB (analytics), SQLite (decisions, experiments)
Writes to: SQLite (world_model_state table)
Refreshes: on demand or triggered by significant events

World model JSON structure (see autonomous-ai-founder-vision.md section 7)
"""

class WorldModel:
    def refresh(self) -> dict: ...          # recompute from all sources
    def get(self) -> dict: ...              # current snapshot
    def get_section(self, key: str) -> dict: ...  # "metrics", "goals", "experiments"
    def update_goals(self, goals: dict) -> None: ...
    def update_agent_state(self, state: dict) -> None: ...
    def get_context_for_agent(self, agent_role: str) -> str: ...
        # Returns formatted context string for LLM prompt

def get_world_model() -> WorldModel: ...
```

### Tests (8+ covering queue CRUD, priority order, world model refresh)

---

## Next-2b: LangGraph Executor + Founder Loop

### `agent/executor.py`

```python
"""
LangGraph-based agent executor.
Dep: langgraph>=0.2.0, langchain-anthropic>=0.3.0

Pattern:
    StateGraph with nodes:
    - think: Claude decides what to do (tool_use)
    - act: executes tool/action via ActionRegistry
    - observe: processes result, updates world model
    - decide_next: continue loop or stop

The executor runs ONE task from the TaskQueue per invocation.
It is NOT a persistent process itself — APScheduler calls it on schedule.
"""

from typing import TypedDict

class AgentState(TypedDict):
    task: dict
    world_model: dict
    messages: list
    actions_taken: list
    iteration: int
    done: bool

class AgentExecutor:
    """
    Wraps a LangGraph StateGraph. Runs one task to completion.
    Falls back to direct Anthropic SDK if langgraph not installed.
    """
    def run(self, task: dict, world_model: dict,
            available_tools: list) -> dict: ...
        # Returns: {"result": ..., "actions_taken": [...], "reasoning": "..."}

def get_executor() -> AgentExecutor: ...
```

### `agent/founder_loop.py`

```python
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

class FounderLoop:
    def run_once(self) -> dict: ...   # process one task, return outcome
    def run_morning_session(self) -> str: ...  # full morning brief + actions
    def run_evening_review(self) -> str: ...   # reflect on day, plan tomorrow
    def handle_event(self, event_type: str, payload: dict) -> dict: ...

def get_founder_loop() -> FounderLoop: ...
```

### Dependencies (add to pyproject.toml)

```toml
agent = [
    "langgraph>=0.2.0",
    "langchain-anthropic>=0.3.0",
]
```

---

## Next-2c: Webhook Handler

### `gateway/webhook_handler.py`

```python
"""
Webhook receiver — turns external events into TaskQueue entries.

Endpoints (added to existing FastAPI app in http_bridge.py):
    POST /webhooks/stripe      — charge.succeeded → send welcome email task
    POST /webhooks/github      — push/PR → engineering review task
    POST /webhooks/intercom    — new ticket → customer success task
    POST /webhooks/crisp       — new message → customer success task
    POST /webhooks/generic     — generic event → any task type

Each webhook:
1. Validates signature (or logs warning if no secret configured)
2. Parses event type
3. Enqueues appropriate task in TaskQueue
4. Returns 200 immediately (async processing)
"""

def register_webhooks(app: FastAPI) -> None: ...
    # Called from http_bridge.build_app() to add webhook routes
```

---

## Next-3: Customer Success Agent

### `agents/customer_success_agent.py`

```python
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

class CustomerSuccessAgent:
    def handle_ticket(self, ticket: dict) -> dict: ...
    def analyze_nps(self) -> dict: ...
    def scan_churn_risks(self) -> list[dict]: ...
    def generate_reply(self, ticket: dict, history: list) -> str: ...
```

---

## Next-4: Marketing Agent

### `agents/marketing_agent.py`

```python
"""
Autonomous marketing agent.

Capabilities:
- Generate SEO blog post from HN/Reddit pain point signals
- Schedule social posts (Tier 2 — soft approved)
- Draft email newsletter (Tier 1 — compute, human sends)
- Monitor competitor moves and generate response content
- Track content performance via analytics_db

Schedule:
- Monday: generate content plan for week
- Daily: post social (within limit)
- Wednesday: draft newsletter (for human review)
- Friday: content performance review
"""

class MarketingAgent:
    def generate_content_plan(self) -> dict: ...
    def write_blog_post(self, topic: str, target_keywords: list) -> str: ...
    def schedule_social_post(self, content: str, platforms: list) -> dict: ...
    def draft_newsletter(self) -> str: ...
    def analyze_content_performance(self) -> dict: ...
```

---

## Next-5: Engineering Agent

### `agents/engineering_agent.py`

```python
"""
Autonomous engineering agent (wraps Claude Code functionality).

Triggers:
- GitHub webhook: PR opened → code review
- GitHub webhook: issue labeled "bug" → diagnosis + fix attempt
- Linear webhook: task created → spec generation
- Schedule: daily code quality scan

Capabilities:
- Code review (read-only, no approval needed)
- Bug diagnosis (read-only)
- Generate fix PRs (Tier 3 — staging, soft approval)
- Deploy to staging (Tier 3)
- Flag critical bugs to Founder Agent

Uses: Anthropic Claude API directly (not MCP) for code analysis
"""

class EngineeringAgent:
    def review_pr(self, pr_url: str) -> str: ...
    def diagnose_bug(self, issue: dict) -> dict: ...
    def generate_fix(self, bug_diagnosis: dict) -> dict: ...
    def create_pr(self, changes: dict, description: str) -> str: ...
    def deploy_staging(self, pr_url: str) -> dict: ...
    def daily_code_scan(self) -> dict: ...
```

---

## Next-6: Multi-Agent Team (CrewAI)

### `agents/crew.py`

```python
"""
CrewAI multi-agent team configuration.
Dep: crewai>=0.11.0

The crew:
- FounderAgent (orchestrator)
- ProductAgent (roadmap, features, user research)
- EngineeringAgent (code, deploy, bugs)
- MarketingAgent (content, social, email)
- FinanceAgent (MRR, runway, unit economics)
- CustomerSuccessAgent (support, NPS, retention)

Each agent:
- Has a specific role + goal + backstory
- Has access to a defined subset of SoloOS tools
- Reports to FounderAgent
- Operates within ActionRegistry permission limits

Weekly crew run (Monday 09:00):
1. FounderAgent reads World Model
2. Assigns weekly objectives to each agent
3. Agents execute autonomously within their domains
4. FounderAgent synthesizes outcomes → human weekly report
"""
```

### `agents/founder_agent.py`

```python
"""
Founder Agent — the orchestrating intelligence.

Responsibilities:
- Weekly strategy session (reads World Model → sets objectives)
- Routes incoming events to right specialist agent
- Makes cross-domain decisions (pricing, pivots, partnerships)
- Maintains company goals in World Model
- Generates human-facing reports

The FounderAgent is the only agent with access to Tier 4+ actions.
All other agents are Tier 0-3 only.
"""
```

### Dependencies (add to pyproject.toml)

```toml
autonomous = [
    "langgraph>=0.2.0",
    "langchain-anthropic>=0.3.0",
    "crewai>=0.11.0",
    "resend>=2.0.0",
]
```

---

## pyproject.toml Final Additions

```toml
[project.optional-dependencies]
# ... existing groups ...
actions = [
    "resend>=2.0.0",
]
agent = [
    "langgraph>=0.2.0",
    "langchain-anthropic>=0.3.0",
]
autonomous = [
    "langgraph>=0.2.0",
    "langchain-anthropic>=0.3.0",
    "crewai>=0.11.0",
    "resend>=2.0.0",
]
```

---

## Global Quality Gates

- All existing 80 tests (7 skipped) must pass after every phase
- Every new module has `if TYPE_CHECKING` guards for optional deps
- Every class has a `_Unavailable*` stub returned when optional dep missing
- Kill switch checked in EVERY agent execute path
- Audit log written BEFORE execution (intent) and AFTER (outcome)
- No hardcoded credentials anywhere
- Fail-open everywhere — MCP server never crashes due to any agent failure
