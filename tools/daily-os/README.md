# Daily OS — Solo Founder Operating System

> Your AI-powered daily briefing, task prioritization, and decision-making system.

## Overview

The Daily OS is your morning ritual. In 15 minutes each morning, it synthesizes:
- Key metrics from yesterday
- Priority tasks for today (with AI prioritization)
- Decisions that need your attention
- Blockers to unblock
- Opportunities to act on

## Daily Ritual (15 minutes)

### 6:00 AM — The Brief (5 min)
```
Prompt to CEO Agent:
"Generate my morning brief for [date]:
- Metrics to check: [MRR, active users, churn signals, support tickets]
- Decisions pending: [paste any open decisions]
- Top goals this week: [your weekly goals]

Format: 5 bullets max, most important first."
```

### 6:05 AM — Priority Stack (5 min)
```
Prompt to COO Agent:
"Prioritize today's tasks using the Impact/Effort matrix:
[paste your task list]

Context:
- Stage: [discover/validate/build/scale]
- Biggest current goal: [X]
- Biggest current bottleneck: [Y]
- Time available: [X hours]

Output: Top 3 tasks in priority order with rationale."
```

### 6:10 AM — Agent Assignment (5 min)

Assign each priority task to the right agent swarm:
- Research task → Research Swarm
- Code task → Build Swarm
- Content task → Content Swarm
- Strategic decision → CEO Agent + Devil's Advocate

## Weekly Cadence

### Monday — Strategy Review (1 hour)
- Last week's metrics review (15 min)
- Goal alignment check (15 min)
- This week's priority setting (15 min)
- Agent tasking for the week (15 min)

### Wednesday — Momentum Check (30 min)
- Midweek metrics pulse
- Blockers removal
- Adjust priorities if needed

### Friday — Week Close (1 hour)
- Week in review (metrics, shipped, learned)
- Customer feedback synthesis
- Next week prep
- Memory update (save key learnings to knowledge base)

## Task Prioritization Framework

### RICE Score
```
RICE = (Reach × Impact × Confidence) / Effort

Reach: How many customers affected? (1-100)
Impact: How much value? (1=minimal, 10=massive)
Confidence: How sure are you? (0.5=uncertain, 1.0=confident)
Effort: Person-days required (1=small, 5=large)

Priority order: Highest RICE score first
```

### Eisenhower Matrix (Quick version)
```
Urgent + Important → DO NOW (you personally)
Important + Not Urgent → SCHEDULE (block time)
Urgent + Not Important → DELEGATE (to AI agent)
Neither → DELETE
```

## AI Agent Daily Task Queue

Structure your agent tasks like this:
```yaml
# daily-tasks-[date].yaml
date: 2026-03-20
priority_focus: [scale/build/validate]

tasks:
  - id: 1
    agent: content-swarm
    task: "Write SEO blog post targeting 'pharmacy audit software'"
    output: "content/blog/pharmacy-audit-post.md"
    deadline: EOD

  - id: 2
    agent: research-agent
    task: "Monitor competitor updates: [competitor list]"
    output: "intel/competitor-update-2026-03-20.md"

  - id: 3
    agent: cfo-agent
    task: "Analyze last month's churn cohort and identify top 3 risk segments"
    input: "data/march-churn-data.csv"
    output: "analysis/march-churn-analysis.md"
```

## Metrics Dashboard Template

Track these in Notion/Airtable, review daily:

```
🟢 REVENUE
  MRR: $___          (target: $___)
  MRR vs last week:  +/-___%
  Churned this week: $___ (X customers)
  New revenue:       $___

🟡 GROWTH
  New signups today: ___
  Trials active:     ___
  Trial → Paid CVR:  ___%
  Traffic (7d):      ___

🔴 RETENTION
  Active users (30d): ___
  Engagement rate:    ___%
  Support tickets:    ___
  NPS (last survey):  ___

⚡ PIPELINE
  Demos scheduled:   ___
  Outreach sent:     ___
  Content published: ___
  Experiments running: ___
```

## Weekly Review Template

```markdown
# Week [X] Review — [Date Range]

## Metrics
- MRR: $[X] ([+/-X%] from last week)
- Active users: [X]
- Churn: [X customers, $X MRR]
- New: [X customers, $X MRR]

## Shipped
- [Feature/fix 1]
- [Feature/fix 2]
- [Content published]

## Learned
- [Customer insight]
- [Market insight]
- [Product insight]

## Next Week Focus
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## Decisions Made
- [Decision 1: X because Y]
- [Decision 2: X because Y]

## Open Questions
- [Question needing answer]
```

## Knowledge Capture (End of Week)

Every Friday, save key insights to the knowledge base:
```
→ patterns/ : Patterns you've confirmed work
→ templates/ : New templates created this week
→ case-studies/ : Customer stories worth documenting
```
