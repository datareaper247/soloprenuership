# Swarm — Sequential Multi-Role Analysis

## Auto-Trigger (No Slash Command Needed)
Fires automatically when founder says: "multiple perspectives on X", "challenge my thinking", "play devil's advocate", "what would X think"

---


**Usage**: `/swarm [type] "[task description]"`

**Examples**:
- `/swarm product-launch "Rankly — daily keyword rank tracker, $9/mo, targeting solo founders"`
- `/swarm weekly-ops` (reads from context files)
- `/swarm growth-sprint "Grow MRR from $4K to $8K in 90 days"`
- `/swarm market-research "B2B expense tracking tools for freelancers"`

Runs a structured sequential analysis where each role's perspective feeds the next.
**Not parallel agents** — one Claude session, multiple role perspectives with explicit handoffs.
Each role builds on the prior output. The synthesis is the deliverable.

---

## How It Actually Works

```
Step 1: Claude reads the task and identifies which roles should contribute
Step 2: Claude adopts Role 1 system prompt → produces Role 1 output
Step 3: Claude explicitly hands off: "Role 1 found X. Role 2, given that, analyze Y."
Step 4: Repeat for each role in sequence
Step 5: CEO/Operator synthesis: given all perspectives, what are the top 5 actions?
```

This is not parallel execution. It's one intelligent system with multiple specialized
lenses applied sequentially. The output quality comes from role-specific depth + handoffs.

**Typical session time**: 45-90 minutes
**Your review time**: 15-20 minutes

---

## Swarm Types

### `product-launch`

For launching a product. Requires: product name, description, price, target customer.

**Role sequence with handoffs**:

**CMO lens** (positioning + GTM):
- What's the positioning? Who is this for exactly? What's the competitive alternative?
- What GTM motion fits this ACV/complexity? (PLG / sales-assisted / enterprise)
- Output: 1-paragraph positioning statement + recommended GTM motion + rationale

**SEO Specialist lens** (using CMO output):
- Given the ICP identified, what keywords are they searching?
- What's the search demand for this problem? What does the competitive landscape look like?
- Output: Top 10 keywords with estimated monthly volume + content gap opportunity

**SDR lens** (using CMO + SEO output):
- Who is the specific person to cold-outreach? Where do they congregate?
- What's the pain hook? What trigger events create urgency?
- Output: ICP description + top 5 communities/channels + outreach angle + first email draft

**Content Marketer lens** (using all above):
- Given the positioning, keywords, and ICP — what's the launch content?
- Output: Launch blog post outline (H1, H2s, key arguments) + 3 email subject line tests

**CEO synthesis**:
- Given all four perspectives, what are the top 5 actions for launch week?
- What's the realistic 30-day goal?
- Output: Launch brief with ranked actions, owners (you), timelines

**Full output format**:
```
PRODUCT LAUNCH BRIEF: [Product]
Date: [date]
════════════════════════════════════════════════════

CMO PERSPECTIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Positioning: [1 paragraph — competitive alternative + unique attribute + value + ICP]
GTM motion: [PLG / Sales-assisted / Enterprise] — Rationale: [2 sentences]

SEO PERSPECTIVE (informed by CMO)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target keywords:
  1. [keyword] — [monthly volume] — [KD] — [page type]
  2. [keyword] — ...
  (top 10)
Content gap: [the specific thing competitors rank for but do poorly]

SDR PERSPECTIVE (informed by CMO + SEO)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ICP: [specific person description]
Where to find them: [top 3 specific channels]
Trigger events: [what creates urgency now]
First email draft:
  Subject: [subject]
  Body: [4-sentence draft]

CONTENT PERSPECTIVE (informed by all above)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Launch blog post: "[H1 title]"
  H2 sections: [list]
  Key argument: [what makes this worth reading]
Email subject tests:
  A: [subject]
  B: [subject]
  C: [subject]

════════════════════════════════════════════════════
CEO SYNTHESIS — TOP 5 LAUNCH ACTIONS
════════════════════════════════════════════════════
1. [Action] — Owner: You — Timeline: Launch day
2. [Action] — Owner: You — Timeline: Week 1
3. [Action] — Owner: You — Timeline: Week 1
4. [Action] — Owner: You — Timeline: Week 2
5. [Action] — Owner: You — Timeline: Week 2

30-day realistic goal: [specific metric]
90-day goal if executed: [specific metric]

The single highest-leverage thing: [1 action]
════════════════════════════════════════════════════
```

---

### `weekly-ops`

Monday morning brief. No input required — reads from context files.

**Role sequence**:

**Data Analyst lens** (reads experiment-log.md + business-context.md):
- What are the numbers? What moved? What's the trend?
- Output: 5-metric pulse, 2 anomalies, 1 pattern

**Growth Hacker lens** (using data output):
- Given these metrics, what's the constraint? What's the highest-leverage experiment?
- Output: 1 experiment to run this week with hypothesis + success metric

**SDR lens** (reads business-context.md for pipeline):
- What's the pipeline status? What follow-ups are due?
- Output: 3 follow-up actions + 1 new prospecting action

**CEO synthesis**:
- Given data + growth + pipeline: what's the one thing this week?
- What decision has been open too long and needs resolution today?
- Output: Weekly brief with 1 priority + 1 decision + 1 experiment

```
WEEKLY OPS BRIEF — [date]
════════════════════════════════════════════════════
PULSE (5 metrics, 30 seconds)
  MRR: $[X] ([+/-X%] WoW) | Target: $[X] | Gap: $[X]
  New MRR this week: $[X] | Churned: $[X]
  Active users: [N] | Signups: [N] | Conversion: [X%]

ANOMALY FLAGS
  ⚠️ [Metric] is [X% above/below] normal range — possible cause: [hypothesis]

EXPERIMENT THIS WEEK
  Hypothesis: If [action], then [outcome], because [reasoning]
  Measure: [metric] after [N] days
  Effort: [hours]

PIPELINE
  Hot (follow up today): [N leads + names]
  Warm (follow up this week): [N leads]
  One outbound action: [specific target + approach]

════════════════════════════════════════════════════
THIS WEEK'S ONE THING
  [Single most important action]
  Why: [reason it outranks everything else]

DECISION TO CLEAR
  [Decision that's been open > 7 days]
  Recommended: [clear recommendation]
  Kill signal: [how to know if wrong]
════════════════════════════════════════════════════
```

---

### `growth-sprint`

For a defined growth push over 30-90 days with a specific target.

**Role sequence**:

**Data Analyst lens**: Audit the full funnel. Where is the biggest conversion drop?

**Growth Hacker lens** (using data): What's the constraint? Top/middle/bottom funnel?
Design 3 experiments targeting the weakest stage.

**Content Marketer lens** (using growth output): What content supports the growth motion?
Prioritize by: drives immediate traffic to conversion page.

**SDR lens** (using all above): What's the outbound motion that complements the experiments?

**CEO synthesis**: 90-day plan with weekly milestones, experiment cadence, kill signals.

---

### `market-research`

For sizing a market or validating a space before building.

**Role sequence**:

**CMO lens**: Who buys in this space? What triggers the purchase? How do they evaluate?

**SDR lens** (using CMO): Who specifically? What's their title, company size, buying process?

**Content Marketer lens**: What are they searching for? What content exists? What's missing?

**CEO synthesis**: Market size estimate + opportunity assessment + entry angle recommendation.

---

### `fundraise`

For founder preparing to raise. Requires: stage, amount, what the money is for.

**Role sequence**:

**CFO lens**: Financial model — current metrics, projection assumptions, use of funds math.

**CEO lens** (using CFO): Investor narrative — why now, why us, what we need to be true.

**CMO lens** (using CEO): Pitch positioning — how to frame the company vs. the competitive landscape.

**CEO synthesis**: Pitch deck outline (11 slides), top 5 investor objections + responses, data room checklist.

---

### `customer-crisis`

For when a key customer threatens to churn or a critical bug/incident occurs.

**Role sequence**:

**Customer Success lens**: Immediate response — what does this customer need to hear right now?

**CEO lens**: What's the root cause? What's the strategic response vs. tactical fix?

**SDR lens** (recovery angle): If they churn, what's the re-engagement path? What would win them back?

**CEO synthesis**: Response plan — what to say now, what to fix in 48h, what to change in 30 days.

---

## BCG 3-Agent Rule (Applied to Swarms)

Max 3 active decision streams presented to you at synthesis time.

A swarm with 5 roles still produces a synthesis with ≤3 priority actions.
The synthesis is not a list of everything that came up. It's the top 3 that matter.

If a swarm outputs 10 equal priority actions, the synthesis failed.

---

## Context File Integration

Swarms use context files automatically if present:

| File | Swarm Uses It For |
|------|------------------|
| `context/business-context.md` | All swarms — calibrates recommendations to your stage |
| `context/customer-voice.md` | `product-launch`, `market-research` — uses exact ICP language |
| `context/experiment-log.md` | `weekly-ops`, `growth-sprint` — avoids re-running failed experiments |
| `context/decision-log.md` | All swarms — prevents contradicting past strategic decisions |

Without context files: the swarm gives generally good output for the task.
With context files: the swarm gives output calibrated to your specific business.

---

## After the Swarm

1. Log the top decisions in `context/decision-log.md`
2. Log the top experiment in `context/experiment-log.md`
3. Add any customer language discovered to `context/customer-voice.md`
4. Run `/morning` next day to track which swarm actions you executed
