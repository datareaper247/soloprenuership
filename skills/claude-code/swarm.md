# Swarm — Coordinated Multi-Agent Task Execution

**Usage**: `/swarm [type] "[task description]"`

Launches a coordinated swarm of role-specialized agents that decompose, execute in parallel phases, and synthesize outputs into an actionable brief.

---

## How It Works

1. **Parse** the swarm type and task description
2. **Decompose** the task into role-specific subtasks across execution phases
3. **Load** each agent's system prompt from `~/soloos/roles/[role].md`
4. **Execute** Phase 1 agents in parallel (independent tasks)
5. **Feed** Phase 1 outputs into Phase 2 agents as context
6. **Synthesize** all outputs into a prioritized action brief
7. **Deliver** the brief with top 10 priority actions, owners, and timelines

---

## Swarm Types

### `product-launch`
Full product launch orchestration.

**Phase 1 — Parallel Intelligence Gathering**
- `product-manager` → Feature/benefit matrix, launch criteria checklist, success metrics
- `seo-specialist` → Target keyword clusters, search volume, competitive gap analysis
- `pr-manager` → Media list, pitch angle, embargo strategy, press kit outline
- `competitive-analyst` → Competitor positioning map, differentiation matrix

**Phase 2 — Parallel Asset Creation** (uses Phase 1 outputs)
- `content-marketer` → Launch blog post, announcement copy, email announcement
- `brand-designer` → Visual brief for launch assets, naming/tagline review
- `social-media-manager` → Platform-specific launch posts (LinkedIn, Twitter/X, Reddit)
- `email-marketer` → Launch day sequence (announcement, follow-up, re-engagement)
- `cro-specialist` → Landing page conversion audit, CTA recommendations

**Phase 3 — Sequential Coordination**
- `cmo` → Synthesizes all Phase 2 assets into unified GTM narrative
- `growth-marketer` → Post-launch growth loops and distribution amplification plan

**Output Format**:
```
PRODUCT LAUNCH BRIEF
====================
Launch Readiness Score: X/10

PHASE 1 INSIGHTS
- Keyword opportunities: [top 5]
- Media targets: [top 10 journalists/outlets]
- Key differentiators vs competitors: [3 bullets]

PHASE 2 ASSETS
- Launch post: [draft or outline]
- Email sequence: [3-email outline]
- Social calendar: [7-day calendar]
- Landing page recommendations: [top 3 changes]

PHASE 3 GTM NARRATIVE
[Unified narrative paragraph]

PRIORITY ACTIONS (ranked by impact/effort)
1. [Action] — Owner: [Role] — Timeline: [X days]
...
```

---

### `market-research`
Deep market intelligence gathering.

**Phase 1 — Parallel Research**
- `market-researcher` → TAM/SAM/SOM sizing, market structure, growth vectors
- `ux-researcher` → Customer pain point mapping, JTBD framework, persona hypotheses
- `data-analyst` → Available market data synthesis, trend identification
- `competitive-analyst` → Competitor landscape, funding, positioning, weaknesses

**Phase 2 — Parallel Synthesis**
- `business-analyst` → Opportunity scoring matrix, risk assessment
- `growth-hacker` → Underserved channel/segment identification
- `ceo` → Strategic implications, go/no-go framework

**Output Format**:
```
MARKET INTELLIGENCE BRIEF
=========================
Market Attractiveness Score: X/10
Confidence Level: [High/Medium/Low]

MARKET OVERVIEW
- TAM: $Xb | SAM: $Xm | SOM: $Xm (Year 3 target)
- Growth rate: X% YoY
- Key dynamics: [3 bullets]

CUSTOMER INSIGHTS
- Primary pain: [1 sentence]
- JTBD: [functional, emotional, social jobs]
- Willingness to pay signal: [evidence]

COMPETITIVE LANDSCAPE
- Leaders: [names + one-line positioning]
- Gaps: [3 specific unaddressed needs]

OPPORTUNITY SCORECARD
| Dimension | Score | Evidence |
|-----------|-------|----------|
| Market size | X/5 | ... |
| Pain intensity | X/5 | ... |
| Competition | X/5 | ... |
| Timing | X/5 | ... |

PRIORITY ACTIONS
1. ...
```

---

### `growth-sprint`
2-week growth experiment design and execution planning.

**Phase 1 — Parallel Diagnostic**
- `data-analyst` → Current funnel metrics, cohort analysis, leaky bucket identification
- `growth-hacker` → Experiment backlog generation (min 20 ideas, ICE-scored)
- `cro-specialist` → Conversion audit of top 3 funnel steps
- `customer-success` → Churn reasons analysis, expansion opportunity mapping

**Phase 2 — Parallel Experiment Design**
- `growth-marketer` → Top 5 acquisition experiments with test designs
- `email-marketer` → Activation/retention email experiments
- `product-manager` → In-product growth loop experiments
- `seo-specialist` → SEO quick-win experiments (low competition, high volume)

**Phase 3 — Synthesis**
- `growth-hacker` → Unified sprint backlog, sprint calendar, metrics dashboard spec

**Output Format**:
```
GROWTH SPRINT BRIEF
===================
Current North Star Metric: [metric] = [value]
Sprint Goal: Increase [metric] by X% in 14 days

TOP LEVERAGE POINTS (from diagnostic)
1. [Funnel step] converting at X% vs benchmark Y%
2. [Cohort] churning at X% within [timeframe]
3. [Channel] showing X% better CAC

SPRINT BACKLOG (ICE scored)
| Experiment | Impact | Confidence | Ease | ICE | Phase |
|------------|--------|------------|------|-----|-------|
| ... | | | | | |

SPRINT CALENDAR
Week 1: [experiments running]
Week 2: [experiments running + read results]

SUCCESS METRICS
- Primary: [metric, target, measurement method]
- Secondary: [metric, target]

PRIORITY ACTIONS
1. ...
```

---

### `go-to-market`
Full GTM strategy for a new product or market segment.

**Phase 1 — Parallel Strategy**
- `cmo` → Positioning, ICP definition, messaging hierarchy
- `seo-specialist` → Organic acquisition strategy, content pillars
- `sem-manager` → Paid acquisition strategy, channel mix, budget allocation
- `sales-enablement` → Sales process design, qualification criteria

**Phase 2 — Parallel Execution Planning**
- `content-marketer` → 90-day content calendar, SEO content plan
- `email-marketer` → Lead nurture sequences, trial-to-paid flows
- `account-executive` → Sales playbook, discovery framework, demo structure
- `customer-success` → Onboarding flow, activation milestones, health scoring

**Phase 3 — Unified Plan**
- `ceo` → Resource requirements, hiring plan, 90-day milestones, board narrative

**Output Format**:
```
GO-TO-MARKET STRATEGY
=====================

ICP DEFINITION
- Company: [firmographics]
- Buyer: [title, responsibilities, pain]
- Champion: [title, motivations]
- Disqualifiers: [3 things that make bad fit]

POSITIONING
- Category: [what we are]
- Differentiation: [why us vs status quo]
- Value prop: [one sentence]
- Proof points: [3 evidence-based claims]

MESSAGING HIERARCHY
1. Primary: [hero message]
2. Supporting: [3 key messages]
3. Proof: [evidence for each]

CHANNEL STRATEGY (90 days)
| Channel | Goal | Budget | Tactic | Owner |
|---------|------|--------|--------|-------|
| Organic SEO | ... | | | |
| Paid Search | ... | | | |
| Outbound | ... | | | |
| Content | ... | | | |

SALES PROCESS
Stage 1 → Stage 2 → ... → Closed

90-DAY MILESTONES
Month 1: [milestone]
Month 2: [milestone]
Month 3: [milestone]

PRIORITY ACTIONS
1. ...
```

---

### `due-diligence`
Business due diligence for investment, acquisition, or partnership.

**Phase 1 — Parallel Assessment**
- `cfo` → Financial analysis, unit economics, burn rate, projections integrity
- `cto` → Technical architecture review, technical debt, scalability, security posture
- `legal-counsel` → Contract review, IP ownership, regulatory exposure, litigation risk
- `hr-manager` → Team assessment, key person risk, culture, comp structure
- `competitive-analyst` → Market position, competitive moat, defensibility

**Phase 2 — Synthesis**
- `ceo` → Investment thesis, key risks, negotiation leverage points

**Output Format**:
```
DUE DILIGENCE REPORT
====================
Overall Assessment: [Green/Yellow/Red]
Recommendation: [Proceed/Negotiate/Pass]

FINANCIAL SUMMARY
- Revenue: $X (LTM) | Growth: X% YoY
- Gross Margin: X% | Net Margin: X%
- Burn Rate: $Xk/mo | Runway: X months
- Unit Economics: LTV $X | CAC $X | LTV:CAC X:1
- RED FLAGS: [if any]

TECHNICAL ASSESSMENT
- Architecture: [summary]
- Technical Debt: [Low/Medium/High] — [details]
- Scalability: [assessment]
- Security: [gaps identified]
- RED FLAGS: [if any]

LEGAL/COMPLIANCE
- IP Status: [owned/licensed/unclear]
- Key Contracts: [summary]
- Regulatory Exposure: [summary]
- RED FLAGS: [if any]

TEAM ASSESSMENT
- Key person risk: [names, roles, retention]
- Org gaps: [missing capabilities]
- Culture: [assessment]

COMPETITIVE POSITION
- Moat: [assessment]
- Key risks: [3 bullets]

NEGOTIATION CONSIDERATIONS
1. [Leverage point]
...

PRIORITY ACTIONS
1. ...
```

---

### `weekly-ops`
Weekly business operations review and planning.

**Phase 1 — Parallel Review**
- `data-analyst` → Metrics review vs targets, anomaly flagging
- `product-manager` → Sprint review, roadmap health, blockers
- `customer-success` → Customer health dashboard, at-risk accounts, wins
- `revenue-ops` → Pipeline review, forecast accuracy, CRM hygiene

**Phase 2 — Planning**
- `coo` → Priorities for the week, resource conflicts, escalations needed
- `ceo` → Weekly narrative for team, focus areas

**Output Format**:
```
WEEKLY OPS BRIEF — Week of [DATE]
==================================

METRICS SUMMARY
| KPI | Target | Actual | Trend | Status |
|-----|--------|--------|-------|--------|
| ... | | | | 🟢/🟡/🔴 |

WINS THIS WEEK
1. ...

BLOCKERS / ESCALATIONS NEEDED
1. [Blocker] — Owner: [name] — Action needed: [action]

PRODUCT
- Shipped: [features/fixes]
- In progress: [items]
- Blocked: [items + blockers]

CUSTOMER
- At-risk accounts: [names + actions]
- Expansion opportunities: [names + stage]
- NPS/CSAT: [score + trend]

PIPELINE
- New pipeline: $X
- Forecast (30 day): $X
- Deals at risk: [list]

THIS WEEK'S PRIORITIES
1. [Priority] — Owner: [name] — Due: [day]
...
```

---

### `competitive-intelligence`
Deep competitive intelligence on a specific competitor.

**Phase 1 — Parallel Research**
- `competitive-analyst` → Positioning, pricing, features, recent changes
- `seo-specialist` → Competitor keyword strategy, content gaps, domain authority
- `growth-marketer` → Competitor acquisition channels, estimated spend, tactics
- `customer-success` → Win/loss analysis, why customers choose them or leave them
- `pr-manager` → Recent press, executive messaging, brand narrative

**Phase 2 — Synthesis**
- `sales-enablement` → Battle card creation
- `cmo` → Strategic response recommendations

**Output Format**:
```
COMPETITIVE INTELLIGENCE: [COMPETITOR NAME]
===========================================
Threat Level: [Critical/High/Medium/Low]

COMPANY OVERVIEW
- Funding: $X (last round: Series X, $Xm, [date])
- Team size: ~X employees
- Revenue estimate: $X ARR (if known)
- Customers: [notable logos]

POSITIONING
- How they describe themselves: "[quote]"
- Target customer: [ICP]
- Core differentiators: [3 bullets]

PRODUCT COMPARISON
| Feature | Them | Us | Advantage |
|---------|------|----|-----------|
| ... | | | |

PRICING
[Their pricing structure]
[Our advantage/gap]

SEO PROFILE
- Domain Authority: X
- Ranking keywords: X (organic traffic est: Xk/mo)
- Top content: [titles]
- Keywords we could take: [list]

ACQUISITION CHANNELS
- Primary: [channels with evidence]
- Estimated spend: $Xk/mo on paid

BATTLE CARD
WHEN THEY SAY: "[objection]"
YOU SAY: "[response]"

OUR WIN CONDITIONS
[When we beat them and why]

STRATEGIC RECOMMENDATIONS
1. ...
```

---

### `content-machine`
Full content production system setup.

**Phase 1 — Strategy**
- `seo-specialist` → Keyword universe, content pillars, competitive content gaps
- `content-marketer` → Editorial strategy, content calendar, distribution plan
- `cmo` → Audience definition, tone of voice, success metrics

**Phase 2 — Production Templates**
- `technical-writer` → Documentation content templates
- `email-marketer` → Email newsletter template and cadence
- `social-media-manager` → Platform-specific content templates
- `video-producer` → Video content strategy and script templates

**Phase 3 — Distribution**
- `growth-marketer` → Content distribution playbook, amplification tactics

**Output**: Full content system — pillars, calendar, templates, distribution playbook, metrics.

---

### `sales-outreach`
Targeted sales outreach campaign design.

**Phase 1 — Research**
- `sdr` → ICP definition, prospect research methodology, list building criteria
- `competitive-analyst` → Competitive context for messaging
- `customer-success` → Customer success stories for social proof

**Phase 2 — Creation**
- `sales-enablement` → Email sequences, call scripts, LinkedIn templates
- `account-executive` → Discovery framework, demo narrative
- `content-marketer` → Supporting content assets (one-pagers, case studies)

**Output**: Complete outreach campaign — sequences, scripts, assets, tracking setup.

---

### `custom`
**Usage**: `/swarm custom "[task]"`

For custom tasks, automatically:
1. Analyze the task to identify the 3-6 most relevant roles
2. Design a 2-3 phase execution plan with clear inputs/outputs per phase
3. Execute and synthesize

State the inferred swarm design before executing so the user can approve or adjust.

---

## Execution Standards

### Parallel Execution
- All agents within a phase run simultaneously
- Each agent receives: (1) the original task, (2) relevant outputs from prior phases, (3) its specific subtask brief

### Output Quality Gates
- Each agent output must be specific, actionable, and professional-grade
- No generic advice — every recommendation tied to the specific task
- Every claim backed by reasoning or data

### Synthesis Principles
- Prioritize actions by impact, not completeness
- Surface conflicts between agent recommendations explicitly
- End every swarm with "Top 10 Priority Actions" ranked by expected impact
