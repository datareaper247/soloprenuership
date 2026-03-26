# SoloOS — Autonomous AI Founder: Complete Vision & Architecture

**Version:** Vision 1.0
**Date:** 2026-03-26
**Status:** Design — Awaiting Phase Approval
**Goal:** An AI system that starts, operates, and scales companies without a human in the loop.

---

## 1. The Fundamental Shift

> Current SoloOS (V10): Human founder uses AI as co-pilot.
> Target: AI IS the founder. Human is the oversight board.

This is not an incremental improvement to a chatbot. It is a different category of system.

**The gap between "AI assistant" and "AI founder" is not intelligence — it's agency infrastructure.**

Claude already has the cognitive capability to run a company. What is missing:

| Missing | What it enables | Build or OSS |
|---------|----------------|-------------|
| Persistent execution environment | AI runs 24/7 without human at keyboard | Temporal.io or Prefect |
| External action capability | AI can DO things, not just recommend them | Per-category APIs |
| Permission framework | What AI can do without asking | Custom — SoloOS ActionRegistry |
| Event-driven triggers | AI acts on signals, not just prompts | Webhooks + APScheduler (partial) |
| Persistent world model | AI knows business state at any moment | DuckDB + SQLite (built) |
| Multi-agent specialization | Different experts for different functions | LangGraph + CrewAI |
| Graduated autonomy | Earn trust, expand permissions over time | Custom — SoloOS Trust Engine |

---

## 2. Graduated Autonomy: V1 → V10

The path from assistant to autonomous founder is not a single jump. It is a trust-building ladder.

```
V1  │ AI answers questions                        ← Current SoloOS V10
    │ Human does everything
    │
V2  │ AI proactively surfaces insights             ← APScheduler morning brief (built)
    │ Human still makes all decisions
    │
V3  │ AI handles read-only research autonomously   ← Market signals, competitor monitoring
    │ Drafts actions, human approves
    │
V4  │ AI autonomously handles COMMUNICATE tier      ← Support replies, social posts
    │ (within daily limits, human can override)
    │
V5  │ AI autonomously handles BUILD tier            ← Writes + deploys staging code
    │ Human approves production deploys
    │
V6  │ AI autonomously handles DEPLOY tier           ← Ships to production within risk limits
    │ Human approves spend + legal
    │
V7  │ AI runs defined business functions            ← Customer support, content marketing
    │ autonomously end-to-end
    │
V8  │ AI manages multi-agent team                   ← CEO/CMO/CTO/CFO agents delegating
    │ Human is board of directors
    │
V9  │ AI discovers + validates new opportunities    ← Identifies and tests new products
    │ Human approves major pivots
    │
V10 │ Full autonomous AI company operation          ← AI starts and runs companies solo
    │ Human receives dividends
```

**Honest current state:** We are between V2 and V3. V4-V10 require the Action Registry + external capabilities.

---

## 3. The Complete Action Surface

Every action a company needs to take, mapped to what the AI can call programmatically.

### Tier 0: READ (no approval, no cost)
| Action | OSS/API | Risk |
|--------|---------|------|
| Fetch own metrics | DuckDB (built) | None |
| Search web | SerpAPI, Jina | None |
| Monitor HN/Reddit | HN MCP, Reddit MCP (built) | None |
| Read competitor sites | Jina reader MCP (built) | None |
| Fetch stock prices | Yahoo Finance, Alpha Vantage | None |
| Check domain availability | GoDaddy MCP (available) | None |
| Analyze code repos | GitHub API | None |

### Tier 1: COMPUTE (no approval, logged)
| Action | OSS/API | Risk |
|--------|---------|------|
| Generate content drafts | Claude API | Low |
| Run financial models | DuckDB (built) | Low |
| Score opportunities | SoloOS tools (built) | Low |
| Generate code (staging) | Claude Code | Low |
| Create design assets | DALL-E API, Midjourney API | Low |
| Draft emails | Claude API | Low |

### Tier 2: COMMUNICATE (soft approval, daily limits)
| Action | OSS/API | Reversible | Risk |
|--------|---------|-----------|------|
| Send customer email | Resend, Postmark | No | Medium |
| Respond to support ticket | Intercom API, Crisp API | Partial | Low |
| Post to social media | Twitter API v2, Buffer API | Yes (delete) | Medium |
| Send Slack message | Slack Webhooks | No | Low |
| Create calendar invite | Cal.com API | Yes | Low |
| Post job listing | LinkedIn API | Yes | Low |
| Respond to review | Trustpilot API, Google | No | Medium |

### Tier 3: BUILD (soft approval, within risk limits)
| Action | OSS/API | Reversible | Risk |
|--------|---------|-----------|------|
| Deploy to staging | Vercel API, Railway API | Yes | Low |
| Create landing page | Vercel API + template | Yes | Low |
| Update documentation | GitHub API | Yes (git) | Low |
| Create Notion page | Notion API | Yes | Low |
| Set up email sequence | ConvertKit API | Yes | Low |
| Create Linear ticket | Linear API | Yes | Low |
| Register subdomain | Cloudflare API | Yes | Low |

### Tier 4: DEPLOY (hard approval OR within defined safe params)
| Action | OSS/API | Reversible | Risk |
|--------|---------|-----------|------|
| Deploy to production | Vercel API, Railway API | Partial | High |
| Update pricing page | Stripe API + deploy | No | High |
| Launch paid ad campaign | Google Ads API, Meta API | Yes (pause) | High |
| Send mass email | Resend, Mailchimp API | No | High |
| Change feature flags | GrowthBook API (built) | Yes | Medium |
| Create new Stripe product | Stripe API | Yes | Medium |
| Register domain | GoDaddy API, Namecheap API | Partial | Low |

### Tier 5: SPEND (hard approval + budget enforcement)
| Action | OSS/API | Reversible | Risk |
|--------|---------|-----------|------|
| Buy domain | GoDaddy API | No | Low ($15) |
| Pay infrastructure bill | Vercel, Railway, AWS | No | Medium |
| Run ads (within budget) | Google Ads API | Yes (pause) | High |
| Pay contractor | Wise API, Deel API | No | High |
| Purchase SaaS tool | Stripe card | No | Medium |
| AWS/GCP spend | Cloud billing API | No | High |

### Tier 6: LEGAL (always human approval)
| Action | Notes |
|--------|-------|
| Sign contract | DocuSign — never autonomous |
| Update TOS/Privacy Policy | Legal review required |
| Register entity | Always human |
| IP decisions | Always human |
| Hiring (permanent) | Always human |
| Fundraising | Always human |

---

## 4. Permission Architecture (ActionRegistry)

Every autonomous action goes through the ActionRegistry before execution.

```
┌─────────────────────────────────────────────────────────┐
│                    ACTION REQUEST                        │
│  action: "send_email"                                   │
│  params: {to: customer@..., subject: "...", body: "..."}│
│  reasoning: "Customer asked about pricing 3 days ago"   │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│                   ACTION REGISTRY                        │
│                                                         │
│  1. Classify tier (COMMUNICATE = Tier 2)                │
│  2. Check daily limit (emails sent today: 3 of 20)      │
│  3. Check budget limit (N/A for email)                  │
│  4. Check reversibility (No — email can't be unsent)    │
│  5. Check kill switch status (active? abort)            │
│  6. Check human override queue (any blocks? abort)      │
│                                                         │
│  Decision: PROCEED / QUEUE_FOR_APPROVAL / BLOCKED       │
└──────────────────────────┬──────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
     PROCEED          QUEUE FOR         BLOCKED
          │           APPROVAL               │
          ▼                │            Log + stop
    Execute action         ▼
    Log to audit     Slack/email
    Update state     to human →
                     await approval
                     (timeout = abort)
```

### ActionRegistry Configuration (YAML)

```yaml
# ~/.soloos/permissions.yaml

global:
  kill_switch: false              # set to true to halt ALL autonomous actions
  autonomous_mode: true           # false = queue everything for approval
  audit_log: ~/.soloos/audit.jsonl

tiers:
  communicate:
    require_approval: false
    daily_limits:
      send_email: 50              # per recipient, per day
      post_social: 3             # per platform, per day
      support_replies: 100       # per day total
    human_review_sample_rate: 0.1  # review 10% of actions randomly

  deploy:
    require_approval: true        # all deploys require approval
    exceptions:
      - action: deploy_staging    # staging is soft-approved
        require_approval: false

  spend:
    require_approval: true
    budget_limits:
      daily_usd: 50
      monthly_usd: 500
      per_transaction_usd: 100

  legal:
    require_approval: always      # cannot be overridden
```

---

## 5. Persistent Execution Architecture

**The hardest problem:** MCP is request-response. An autonomous founder needs to run 24/7, react to events, and maintain state across restarts.

### Two-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 PERSISTENT AGENT RUNTIME                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              TRIGGER LAYER                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │   │
│  │  │ Cron     │  │ Webhooks │  │ Event Stream     │  │   │
│  │  │ APSched. │  │ FastAPI  │  │ (Stripe, GitHub) │  │   │
│  │  └────┬─────┘  └────┬─────┘  └────────┬─────────┘  │   │
│  │       └─────────────┴──────────────────┘            │   │
│  │                      │                              │   │
│  │              ┌────────▼────────┐                    │   │
│  │              │  TASK QUEUE     │                    │   │
│  │              │  (SQLite-backed)│                    │   │
│  │              └────────┬────────┘                    │   │
│  └───────────────────────┼──────────────────────────── ┘   │
│                          │                                  │
│  ┌───────────────────────▼─────────────────────────────┐   │
│  │              AGENT EXECUTOR                         │   │
│  │                                                     │   │
│  │  Dequeues task → builds context from World Model   │   │
│  │  → invokes Claude API with tools → executes plan   │   │
│  │  → logs outcome → updates World Model              │   │
│  │                                                     │   │
│  │  OSS: LangGraph (stateful graphs)                  │   │
│  │  or: direct Anthropic SDK with tool_use            │   │
│  └─────────────────────────────────────────────────── ┘   │
│                          │                                  │
│  ┌───────────────────────▼─────────────────────────────┐   │
│  │              WORLD MODEL                            │   │
│  │                                                     │   │
│  │  DuckDB: metrics, events, trends (built)           │   │
│  │  SQLite: decisions, experiments, state (built)     │   │
│  │  Goals: JSON — what the AI is trying to achieve    │   │
│  │  Memory: vector store — episodic memory (optional) │   │
│  └─────────────────────────────────────────────────── ┘   │
└─────────────────────────────────────────────────────────────┘
```

### Persistent Runtime Options (OSS)

| Option | Stars | Self-host | Complexity | Best For |
|--------|-------|-----------|------------|---------|
| **APScheduler** (already built) | 5k | Zero (embedded) | Low | Scheduled tasks |
| **Prefect** | 16k | Docker | Medium | Data workflow pipelines |
| **Temporal.io** | 12k | Docker | High | Durable long-running workflows |
| **LangGraph** | 8k | Embedded | Low-Medium | Stateful agent graphs |
| **Custom (FastAPI + APScheduler)** | N/A | Zero | Low | Our current approach |

**Recommendation for V next:** Extend current APScheduler + add LangGraph for stateful agent execution. Temporal when revenue >$10k MRR (operational complexity justified).

---

## 6. Multi-Agent Team Architecture

A single AI trying to do everything performs worse than specialized agents. The company needs a team.

```
┌─────────────────────────────────────────────────────────────────┐
│                      FOUNDER AGENT (Orchestrator)               │
│                                                                 │
│  Mission: profitable, growing company                          │
│  Tools: all SoloOS tools, delegate to specialists               │
│  Decisions: strategy, pivots, hires, major spend                │
│  Runs: daily strategy loop (morning + evening)                  │
└─────────────────────────────────────────────────────────────────┘
          │              │              │              │
          ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  PRODUCT     │ │  ENGINEERING │ │  MARKETING   │ │  FINANCE     │
│  AGENT       │ │  AGENT       │ │  AGENT       │ │  AGENT       │
│              │ │              │ │              │ │              │
│ - User       │ │ - Write code │ │ - Content    │ │ - Track MRR  │
│   research   │ │ - Review PRs │ │   creation   │ │ - Runway     │
│ - Feature    │ │ - Deploy     │ │ - SEO        │ │ - Unit econ  │
│   prioritize │ │ - Bugs       │ │ - Social     │ │ - Invoicing  │
│ - Roadmap    │ │ - Infra      │ │ - Email      │ │ - Expenses   │
│              │ │              │ │ campaigns    │ │              │
│ OSS:         │ │ OSS:         │ │              │ │ OSS:         │
│ LangGraph    │ │ Claude Code  │ │ OSS:         │ │ LangGraph    │
│ + SoloOS KB  │ │ (already     │ │ LangGraph    │ │ + Stripe SDK │
│              │ │ exists!)     │ │ + Resend SDK │ │              │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
          │
          ▼
┌──────────────┐
│  CUSTOMER    │
│  SUCCESS     │
│  AGENT       │
│              │
│ - Support    │
│   tickets    │
│ - Onboarding │
│ - NPS        │
│ - Churn prev.│
│              │
│ OSS:         │
│ Intercom API │
│ + LangGraph  │
└──────────────┘
```

### Agent Implementation Pattern

Each agent is:
- A LangGraph `StateGraph` with defined nodes + edges
- A set of permitted tools (subset of SoloOS ActionRegistry)
- A system prompt defining role + values + constraints
- A memory interface (reads World Model, writes decisions back)
- A reporting interface (reports to Founder Agent)

**Key insight:** Claude Code IS the Engineering Agent. It already exists. We need to make it callable as part of the autonomous system.

---

## 7. World Model Design

The AI's persistent understanding of the business. This is what makes continuity possible across sessions.

```json
{
  "company": {
    "name": "string",
    "stage": "$1-5K MRR",
    "founded": "2026-01-01",
    "mission": "string"
  },
  "metrics": {
    "mrr": 2500.00,
    "mrr_growth_mom": 0.15,
    "churn_monthly": 0.04,
    "runway_months": 18,
    "customers": 52,
    "nps": 42
  },
  "goals": {
    "this_week": ["ship pricing page", "close 3 new customers"],
    "this_month": ["reach $5K MRR", "launch referral program"],
    "this_quarter": ["hit PMF (40% very disappointed)", "expand to EU"],
    "north_star": "reach $10K MRR by 2026-09-30"
  },
  "product": {
    "current_version": "1.2.0",
    "top_requested_features": ["..."],
    "known_bugs": ["..."],
    "next_deploy_ready": true
  },
  "market": {
    "icp": "solo founders using Claude Code",
    "top_competitors": ["..."],
    "differentiators": ["..."],
    "last_competitive_analysis": "2026-03-20"
  },
  "experiments": {
    "running": ["pricing-test-79-vs-49"],
    "completed_last_30_days": ["..."]
  },
  "agent_state": {
    "last_morning_brief": "2026-03-26T07:00:00",
    "pending_approvals": [],
    "last_customer_contact": "2026-03-25",
    "in_progress_tasks": ["write SEO article on founder tools"]
  }
}
```

World Model lives in SQLite. Updated after every significant action. Read at start of every agent execution. This is the "brain stem" of the autonomous company.

---

## 8. The Opportunity Discovery Engine

For truly autonomous operation, the AI must find its own opportunities — not just execute on human-defined ones.

```
DISCOVERY LOOP (runs weekly):
1. Mine HN + Reddit for pain points in target domain
2. Score each pain point: frequency × severity × underserved
3. Cross-reference with own customer feedback
4. Generate 3-5 opportunity hypotheses
5. Auto-validate each: search for existing solutions, size market
6. Present top 3 to human for go/no-go
7. If approved: generate spec + start building
```

**OSS:** HN MCP + Reddit MCP (built) + validate_idea_gates + score_opportunity (built)

The missing piece: connecting discovery → validation → building autonomously.

---

## 9. Complete OSS Stack for Autonomous Operation

### Core Intelligence
| Component | OSS | Notes |
|-----------|-----|-------|
| AI brain | Anthropic Claude API | Already in use |
| Agent graphs | **LangGraph** (MIT, 8k stars) | Stateful multi-step reasoning |
| Multi-agent | **CrewAI** (MIT, 25k stars) | Role-based agent teams |
| Persistent workflows | **Prefect** (Apache 2, 16k stars) | Data workflows + scheduling |

### Action Layer (new — not yet built)
| Action Type | OSS/API | Auth |
|-------------|---------|------|
| Email send | **Resend** (MIT SDK, 4k stars) | API key |
| Code deploy | **Vercel SDK** (MIT) | API token |
| Infrastructure | **Railway SDK** | API token |
| Social post | **Twitter API v2** (httpx) | OAuth2 |
| Support | **Intercom API** (httpx) | API key |
| Email marketing | **ConvertKit API** (httpx) | API key |
| Domains | **Cloudflare API** (cloudflare SDK) | API token |
| Job posts | **LinkedIn API** (httpx) | OAuth2 |
| Content CMS | **Ghost API** (httpx) | API key |
| Contractors | **Upwork API** (httpx) | OAuth2 |
| Ads | **Google Ads API** (google-ads SDK) | OAuth2 |

### Safety + Governance (new — not yet built)
| Component | OSS | Notes |
|-----------|-----|-------|
| Action registry + permissions | **Custom** (50 lines) | ActionRegistry class |
| Audit log | **SQLite** (built) | append-only log |
| Kill switch | **Custom** (5 lines) | env var + file flag |
| Approval queue | **Slack webhooks** (built) | human-in-loop |
| Budget enforcement | **Custom** (built into ActionRegistry) | hard limits in code |

### Persistent Execution (new — partial)
| Component | OSS | Status |
|-----------|-----|--------|
| Scheduled tasks | APScheduler (built) | ✅ Done |
| Webhook receiver | FastAPI (built in gateway) | ✅ Done |
| Task queue | SQLite-backed (needs build) | 🔲 Next |
| World model | SQLite + DuckDB (built) | ✅ Done |
| Agent executor | LangGraph (needs build) | 🔲 Next |

---

## 10. Phased Roadmap to Autonomous AI Founder

### Phase Next-1: Action Layer (V3 capability)
**Goal:** AI can take real-world actions within defined limits. Human approves nothing unless high-risk.
- ActionRegistry with permission tiers + audit log
- Resend email action
- Vercel/Railway deploy action
- Cloudflare DNS action
- Twitter post action
- Slack notification (already partial)
**Kill signal:** AI successfully deploys a staging environment without human prompting.

### Phase Next-2: Persistent Agent (V4 capability)
**Goal:** AI runs continuously, reacts to events, maintains state.
- Task queue (SQLite-backed)
- Webhook receiver for Stripe + GitHub events
- LangGraph agent executor (replaces direct tool calls)
- World Model sync (updated on every significant event)
**Kill signal:** AI detects a new Stripe charge and sends a welcome email autonomously within 5 minutes.

### Phase Next-3: Customer Function (V5 capability)
**Goal:** Customer success runs fully autonomously.
- Intercom/Crisp webhook → AI reads ticket → generates reply → sends (Tier 2 auto)
- NPS survey → AI analyzes → flags churn risks → proposes retention action
- Onboarding sequence → AI personalizes based on user behavior
**Kill signal:** Zero support tickets unanswered >1h for 30 consecutive days.

### Phase Next-4: Marketing Function (V6 capability)
**Goal:** Content + email + social runs autonomously.
- Weekly SEO article (Claude writes → stages → deploys on approval)
- Daily social post (within limit, human can disable)
- Monthly email newsletter (drafted → human approves → sends)
- HN/Reddit signal → blog post opportunity → drafted → queued
**Kill signal:** Organic traffic grows 10%+ MoM for 3 consecutive months.

### Phase Next-5: Engineering Function (V7 capability)
**Goal:** AI can ship features end-to-end with human approval gates.
- GitHub webhook: PR opened → AI reviews → comments
- Linear ticket created → AI generates spec → human approves → AI codes → PRs → stages
- Bug reported → AI diagnoses → generates fix → PRs → human reviews → ships
**Kill signal:** AI ships a customer-reported bug fix to production within 24h of report.

### Phase Next-6: Multi-Agent Team (V8-V10 capability)
**Goal:** Specialized agents collaborate. Founder Agent orchestrates.
- CrewAI team: Founder + Product + Engineering + Marketing + Finance agents
- Inter-agent communication via shared World Model
- Founder Agent holds weekly strategy session (runs Monday morning, reports Thursday)
- Human receives weekly digest + approval queue only
**Kill signal:** Company operates for 30 days with <2h/week human time input.

---

## 11. What We Are NOT Building

| Idea | Why Not |
|------|---------|
| Custom LLM or fine-tuning | Claude API is the right LLM. Prompt engineering > fine-tuning at this scale. |
| Custom vector database | SQLite FTS5 handles KB. LlamaIndex RAG if KB >500 items. |
| Custom workflow engine | Prefect/LangGraph exists and is battle-tested. |
| Blockchain/smart contracts | No legitimate use case for a founder OS. |
| ML model for opportunity scoring | Rule-based scoring (built) is more explainable and debuggable. |
| Legal AI | Always human. Never automate legal decisions. |
| Financial AI trading | Out of scope. SoloOS manages company finances, not investments. |
| Physical world actions | No robotics, no hardware. Software companies only. |

---

## 12. Safety Non-Negotiables

These are not optional. They ship before any autonomous capability:

1. **Kill switch:** Single env var `SOLOOS_AUTONOMOUS=false` halts all Tier 2+ actions. Checked before every action execution.

2. **Audit log:** Every action logged to `~/.soloos/audit.jsonl` with timestamp, tier, action, params, reasoning, outcome. Append-only. Never deleted.

3. **Approval queue timeout:** If a Tier 4+ action is queued and no human approves within 24h, it is auto-rejected. Never auto-approved.

4. **Budget hard limits:** Enforced in ActionRegistry code, not config. Cannot be overridden by AI. Only changeable by editing Python source.

5. **No legal actions:** Tier 6 is not configurable. LEGAL tier always requires human. Hard-coded.

6. **Human can always override:** The approval queue, kill switch, and per-action override are always available via the Streamlit dashboard (built).

7. **Scope creep detection:** AI cannot modify its own permissions. The ActionRegistry is read-only to the AI. Permissions changes require human.

---

## 13. Definition of Done — Autonomous AI Founder

The system has achieved its goal when:

1. A new product opportunity is discovered by the AI, validated, built, and launched without human initiation
2. The product acquires its first paying customer without human involvement
3. Customer support runs for 30 days with zero human intervention
4. Monthly financial report is generated, reviewed by human, and all numbers are accurate
5. A production bug is detected, diagnosed, fixed, and deployed within 24h of user report
6. The AI correctly escalates (does NOT act) on a Tier 6 legal decision

---

*This document defines the north star for SoloOS. Current V10 represents V2 on the autonomy ladder.*
*Each phase above requires explicit approval before implementation.*
*Safety architecture (Phase NS-0) ships before any autonomous capability phase.*
