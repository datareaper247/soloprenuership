# Strategy Engine

## The Intelligence Layer for Solo Founder Decision-Making

Based on research from BCG, HBR, Indie Hackers, and HackerNews (March 2026), this strategy engine is designed around one core principle:

**The human sets objectives and quality criteria. Agents execute. The interface surfaces only decisions that genuinely require human judgment.**

---

## The 3-Agent Rule (BCG Research, 2026)

**Finding**: Managing more than 3 active AI agents simultaneously causes cognitive collapse, not plateau.

**Implementation for SoloOS**:
- Never present more than 3 pending decisions to the founder at once
- Agents auto-resolve everything below a configured quality threshold
- The daily OS surfaces: Top 3 Decisions + Agent Status + Metrics
- Founder = Commander, not Approver

---

## Core Frameworks

### 1. Opportunity Scoring Matrix

Score each opportunity on 5 dimensions (1-10 each):

| Dimension | Weight | Key Question |
|-----------|--------|-------------|
| Problem Severity | 30% | How painful is this, how often does it occur? |
| Market Size | 20% | Is TAM > $500M, SAM > $50M? |
| Competitive Gap | 20% | Is there a clear gap in existing solutions? |
| Willingness to Pay | 20% | Are people currently paying for workarounds? |
| Solo Buildability | 10% | Can 1 person + AI build v1 in 4 weeks? |

**Threshold**: Score ≥ 6.5/10 to proceed to validation.

### 2. The Parallelism Strategy (Autoresearch Pattern)

**Key insight from Karpathy's SkyPilot experiment (2026)**:
Sequential agents find local optima. Parallel agents find global optima.

Apply to every strategic question:
```
Instead of: "What should our pricing be?"
Do: Run 5 pricing models in parallel, test with 5 customer segments
Output: The pricing that maximizes LTV:CAC across ALL segments

Instead of: "What's our positioning?"
Do: Run 6 positioning hypotheses against real customer language
Output: The positioning with highest resonance signal
```

**Rule**: Any decision affecting >$10K annual revenue warrants parallel agent analysis before human decides.

### 3. Competitive Moat Scoring

Score each moat type (0-3):

| Moat Type | Weight | Score | Total |
|-----------|--------|-------|-------|
| Product (IP, network effects, switching costs) | 40% | /3 | |
| Market (brand, distribution, cost) | 30% | /3 | |
| Team (unfair advantages) | 20% | /3 | |
| Financial (runway, capital efficiency) | 10% | /3 | |

**Thresholds**:
- 2.5-3.0: Strong moat → proceed with conviction
- 1.5-2.5: Moderate moat → strengthen before scaling
- <1.5: Weak moat → reconsider or reposition

### 4. Decision Framework (Human-in-Command)

For any major decision, route through this process:
```
1. CEO Agent drafts decision brief (context, options, tradeoffs)
2. Devil's Advocate Agent challenges each option
3. Market Expert Agent adds external context
4. CFO Agent models financial implications
5. Synthesizer Agent produces ranked recommendation + confidence score
6. Human reviews synthesis → approves/modifies/rejects
```

Human input required only at Step 6. Steps 1-5 run in parallel.

**Decision latency target**: < 2 hours from question to human review.

### 5. Phase Transition Gates

Before moving to the next phase, all gate conditions must be met:

**DISCOVER → VALIDATE**
- ≥1 opportunity scored ≥6.5/10
- TAM > $500M validated
- Clear competitive gap identified

**VALIDATE → BUILD**
- 3+ pre-sales OR 15+ confirmed problem interviews
- WTP confirmed at target price point
- ICP defined (specific job title + industry + company size)

**BUILD → SCALE**
- Product shipped to production
- Activation rate > 50%
- Week-2 retention > 30%
- NPS > 30

**SCALE → EXIT**
- MRR > $50K
- Monthly churn < 3%
- NRR > 100%
- Processes documented (can run without founder 30 days)

---

## The Human-in-Command Interface

Based on TTal's Telegram pattern (the most advanced real-world implementation as of March 2026):

**What founder sees (max 3 items at a time)**:
1. Decisions requiring human judgment
2. Agents completing major milestones
3. Business metrics crossing thresholds (positive or negative)

**What agents handle autonomously**:
- Research tasks (output reviewed, not every step)
- Content drafting (review final output, not each iteration)
- Competitive monitoring (weekly digest, not daily reports)
- Code review and QA passes (review pass/fail, not line-by-line)
- Financial modeling iterations (review final model, not each run)

**Mobile command interface design**:
```
Morning Brief (< 5 min):
  → 3 priority decisions requiring judgment
  → Yesterday's key agent completions
  → MRR / active users / churn alerts

Async review:
  → Agent outputs queued for human approval
  → Accept / Modify / Reject with voice note
  → Agent continues with approved direction

Evening summary:
  → Day's completions
  → Metrics delta
  → Queue for tomorrow
```

---

## Strategy Agent Swarm

### Composition
1. **Strategic Advisor** (CEO Agent) — Vision and market positioning
2. **Opportunity Scorer** — Multi-dimensional analysis
3. **Devil's Advocate** — Challenges every assumption
4. **Market Expert** — External context and signals
5. **Synthesis Agent** (Claude Opus) — Aggregates, ranks, recommends

### Interaction Protocol
```
Input: Business decision or strategic question

Phase 1 (Parallel, 15-30 min):
  - Strategic Advisor: initial assessment
  - Devil's Advocate: challenges and risks
  - Market Expert: competitive context

Phase 2 (Sequential, 10-15 min):
  - Synthesis Agent: reads all 3 outputs
  - Produces: ranked options + confidence + reasoning

Phase 3 (Human, 5-10 min):
  - Reviews synthesis
  - Approves, modifies, or rejects
  - Agent logs decision for future learning

Total time: 30-55 minutes from question to decision
Human time: 5-10 minutes
```

### When to Escalate to Human Immediately
- Any irreversible decision (pivot, kill, launch)
- Spending > $1,000 in any form
- Customer-facing commitments
- Legal or compliance exposure
- Decisions contradicting prior human guidance

---

## Gap Analysis: What Business Intelligence Agents Don't Exist Yet (March 2026)

Research confirms these are **unmanned layers** in the current ecosystem:

| Business Function | Current State | Gap |
|------------------|---------------|-----|
| Market sizing | Manual research | Automated TAM/SAM analysis agent |
| ICP research | Manual interview synthesis | AI-powered customer signal aggregation |
| Pricing strategy | Manual competitive research | Parallel pricing scenario testing agent |
| Growth experiments | Manual A/B test design | Automated experiment design + measurement |
| Churn prediction | Manual cohort analysis | Predictive churn signal agent |
| Competitor monitoring | Manual web searches | Real-time competitive intelligence feed |
| Customer feedback synthesis | Manual reading | Pattern extraction from all feedback sources |

**SoloOS fills every one of these gaps.**
