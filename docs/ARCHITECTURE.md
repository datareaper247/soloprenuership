# SoloOS Architecture

## System Overview

SoloOS is a layered framework. Each layer has a clear responsibility and interface.

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOLO OS FRAMEWORK                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Intelligence Layer (Decision Engine)           │  │
│  │  - Real-time decision scoring                            │  │
│  │  - Context synthesis + memory                            │  │
│  │  - 3-Agent Rule enforcement (BCG Research)               │  │
│  │  - Cross-agent coordination                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ▲                                      │
│         ┌─────────────────┼─────────────────┐                   │
│         │                 │                 │                   │
│    ┌────▼────┐      ┌─────▼─────┐      ┌───▼──────┐            │
│    │Research │      │ Strategy  │      │  Build   │            │
│    │ Engine  │      │ Engine    │      │  Engine  │            │
│    └─────────┘      └───────────┘      └──────────┘            │
│    ┌─────────┐      ┌───────────┐      ┌──────────┐            │
│    │ Growth  │      │    Ops    │      │Knowledge │            │
│    │ Engine  │      │  Engine   │      │   Base   │            │
│    └─────────┘      └───────────┘      └──────────┘            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │        Execution Layer (Workflow Engine + Agents)        │  │
│  │  - Parallel agent orchestration                          │  │
│  │  - Quality gate enforcement (3-gate protocol)            │  │
│  │  - Result aggregation + winner selection                 │  │
│  │  - Outcome-loop closure (actions → business metrics)     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │      Integration Layer (Tools & External Services)       │  │
│  │  - AI Models: Claude (opus/sonnet/haiku), Gemini         │  │
│  │  - Data: Reddit, HN, Ahrefs, Semrush, Jina               │  │
│  │  - Action: GitHub, Stripe, Vercel, Supabase              │  │
│  │  - Communication: Slack, email, Telegram                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Design Principles

### 1. Human-in-Command (Not Human-in-the-Loop)

**Problem**: Human-in-the-loop makes the founder the bottleneck and causes cognitive collapse (BCG 3-Agent research).

**Solution**: Human sets objectives + quality criteria → agents execute autonomously → interface surfaces only decisions requiring human judgment (max 3 at a time).

```
BAD (Human-in-the-Loop):
  Task → Agent → Human approves → Agent continues → Human approves → ...
  Result: Founder drowns in approval requests

GOOD (Human-in-Command):
  Founder: "Research pharmacy audit market, score opportunity, recommend go/no-go"
  System: [Runs research swarm autonomously, 45 min, 4 parallel agents]
  System: "Score: 6.8/10. Recommendation: VALIDATE. Here's why. Approve?"
  Founder: "Approved" (2 min)
```

### 2. Parallelism as Strategy (Autoresearch Pattern)

From Karpathy's SkyPilot experiment: parallel agents find global optima; sequential agents find local optima.

```
Sequential approach:
  test hypothesis A → if good, refine A
  Result: local optimum around A, never discovers B is better

Parallel approach:
  test hypotheses A, B, C, D, E simultaneously
  Result: global optimum discovered; interaction effects revealed
```

**Applied everywhere in SoloOS**: content generation (`v5`), pricing scenarios (`v3`), cold email variants (`v10`), product features (parallel implementations), market research (4 agents simultaneously).

### 3. Compound Learning

Every agent output feeds the knowledge base. Every decision is logged. Every outcome is measured.

The system gets smarter over time:
- Month 1: Generic agent outputs
- Month 6: Agents know your customers, your tone, your proven patterns
- Month 12: Agents are fine-tuned to your specific market, audience, and product

### 4. Cost-Aware Model Routing

| Task Type | Model | Cost |
|-----------|-------|------|
| Architecture decisions | Claude Opus 4.6 | $15/M tokens |
| Code generation, content | Claude Sonnet 4.6 | $3/M tokens |
| Formatting, validation, summaries | Claude Haiku | $0.25/M tokens |
| Large context (>50K tokens) | Gemini 2.5 Flash | ~Free |
| Real-time web search | Perplexity | Low cost |

Auto-routing based on task type reduces AI costs by 60-80% vs. using Opus for everything.

### 5. The 3-Gate Quality Protocol

```
Gate 1: Mechanical Correctness
  Code: tests pass, no linter errors
  Content: grammar correct, links work
  Research: sources cited, recent (< 12 months)

Gate 2: Quality Threshold
  Score must exceed configured minimum
  Failed gate → automatic revision loop (max 2)
  Still fails → escalate to human

Gate 3: Business Alignment
  Does this advance the stated objective?
  Misaligned → revision loop
  Still misaligned → human escalation
```

Human sees only outputs that passed all 3 gates.

---

## The 5 Engines

### Research Engine
**Purpose**: Market intelligence on demand
**Inputs**: Topic, competitor name, customer problem
**Outputs**: Opportunity scores, competitor maps, customer insight briefs
**Key agents**: Market Researcher, Competitor Analyst, Trend Spotter, Validation Researcher
**Latency target**: 30-90 minutes for full analysis

### Strategy Engine
**Purpose**: Business decision support
**Inputs**: Strategic question, context, constraints
**Outputs**: Ranked options with confidence scores, risk assessment, action plan
**Key agents**: CEO Agent, Devil's Advocate, Market Expert, Synthesis Agent
**Latency target**: 30-60 minutes for decision brief

### Build Engine
**Purpose**: Product and content creation
**Inputs**: Feature spec, content brief, design requirement
**Outputs**: Production-ready code, tested features, published content
**Key agents**: Product Manager, Architect, Code Generator, QA Engineer, Content Creator
**Latency target**: 30-90 minutes per feature/post

### Growth Engine
**Purpose**: Revenue growth through systematic experimentation
**Inputs**: Business metrics, growth hypothesis, budget
**Outputs**: Experiments running, content published, pipeline built
**Key agents**: SEO Specialist, Content Marketer, Growth Hacker, Sales Closer
**Latency target**: Weekly cadence, continuous operation

### Ops Engine
**Purpose**: Business operations without a team
**Inputs**: Process question, financial data, legal question
**Outputs**: SOPs, financial models, legal templates, compliance checks
**Key agents**: CFO Agent, COO Agent, Legal Advisor, Compliance Officer
**Latency target**: On-demand, 15-60 minutes

---

## Knowledge Base Architecture

```
knowledge-base/
├── patterns/         # Proven business patterns (versioned)
├── templates/        # Reusable frameworks and scripts
├── case-studies/     # Real-world examples with transferable lessons
│
└── [dynamic, agent-generated]
    ├── market-intel/    # Research engine outputs
    ├── customer-intel/  # Interview synthesis, NPS, feedback
    ├── competitor-intel/# Competitor updates
    ├── experiments/     # Growth experiment results
    └── decisions/       # Decision log with outcomes
```

**Retrieval**: Semantic search across all stored knowledge.
**Freshness**: Time-stamped, staleness alerts after 90 days.
**Deduplication**: New research checks for existing coverage before running.

---

## Agent Communication Protocol

```typescript
interface AgentMessage {
  from: AgentId;
  to: AgentId | 'broadcast';
  task: string;
  context: Record<string, any>;  // From knowledge base
  quality_criteria: string;      // What "good" looks like
  budget?: number;               // Max tokens/cost
  timeout?: number;              // Max seconds
}

interface AgentResponse {
  result: any;
  confidence: number;    // 0-1
  reasoning: string;     // Why this output
  gate_scores: GateScore[];  // Quality gate results
  cost: number;
  duration_ms: number;
}
```

---

## Implementation Stack

### Recommended for Building SoloOS Tools

```
Language:     TypeScript (type safety, ecosystem)
Runtime:      Node.js (Bun for performance)
Framework:    Next.js App Router (full-stack)
Database:     Supabase (Postgres + auth + realtime)
AI Primary:   Anthropic Claude API
AI Secondary: Gemini (large context), Perplexity (search)
Orchestration: Custom or LangChain
Vector DB:    pgvector (in Supabase) or Pinecone
Queue:        Supabase Queues or BullMQ
Deployment:   Vercel (frontend) + Railway (background jobs)
Monitoring:   Sentry + PostHog
```

### For Using SoloOS as a Framework

No installation required. Use the playbooks, agent system prompts, and templates directly with Claude Code or any AI interface.
