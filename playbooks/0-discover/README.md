# Phase 0: DISCOVER

> Find your billion-dollar problem before writing a single line of code.

## Goal

In 1-2 weeks, identify 3-5 validated market opportunities with:
- Clear problem statements (from real human pain)
- Market size estimates
- Competitive landscape snapshot
- Initial willingness-to-pay signal
- Opportunity scores

## The Discovery Protocol

### Step 1: Pain Mining (Day 1-3)

**Reddit Mining** (2-3 hours):
```
Search patterns:
- "I wish there was a way to [X]"
- "Why doesn't anyone build [X]"
- "I hate when [X]"
- "I spend hours every week doing [X] manually"
- "[Tool] is terrible for [use case]"

Target subreddits based on domain:
- Business: r/entrepreneur, r/smallbusiness, r/SaaS
- Tech: r/programming, r/webdev, r/devops
- Finance: r/personalfinance, r/financialindependence
- Healthcare: r/medicine, r/nursing, r/pharmacy
- Legal: r/legaladvice, r/law
- HR: r/humanresources, r/recruiting
```

**HackerNews Mining** (1 hour):
```
Search: site:news.ycombinator.com "Ask HN: Is anyone working on"
Search: "frustrated with" OR "can't believe there's no"
Monitor: Ask HN monthly "What are you working on?"
```

**Review Mining** (1-2 hours):
```
G2, Capterra, Trustpilot, App Store for existing tools in space
Filter: 1-3 star reviews → extract complaints
Pattern: "I switched because..." = opportunity signal
```

### Step 2: Opportunity Scoring (Day 3-4)

Score each idea on:

| Dimension | Weight | Questions |
|-----------|--------|-----------|
| Problem Severity | 30% | How painful? How often? |
| Market Size | 20% | TAM > $1B? SAM addressable solo? |
| Competition | 20% | Fragmented? No clear winner? |
| Willingness to Pay | 20% | Do people pay for workarounds? |
| Solo Buildability | 10% | Can 1 person + AI build this? |

**Minimum threshold**: Score ≥ 6.5/10 to proceed

### Step 3: Quick Competitive Map (Day 4-5)

For each opportunity scoring ≥ 6.5:
- Find all competitors (Google, ProductHunt, G2, App Store)
- Map their: pricing, target customer, key features, reviews
- Identify: gaps, underserved segments, pricing white space

### Step 4: Hypothesis Formation (Day 5-7)

Write your core hypothesis:
```
FOR [specific customer segment]
WHO struggle with [specific problem]
WE WILL BUILD [product type]
THAT [core value proposition]
UNLIKE [main competitor]
OURS WILL [key differentiator]
WE BELIEVE [25-40% of target customers] will pay [$X/month]
WE'LL KNOW WE'RE RIGHT WHEN [measurable signal]
```

## Agent Swarm: Discovery Mode

**Deploy**: `framework/swarms/discovery-swarm.yaml`

The discovery swarm runs:
1. **Pain Miner** → Scrapes Reddit, HN, reviews for problems
2. **Market Sizer** → Estimates TAM/SAM from available data
3. **Competitor Scout** → Maps existing solutions
4. **Opportunity Scorer** → Scores each idea on matrix
5. **Hypothesis Writer** → Drafts structured hypotheses

## Outputs

- [ ] `discovery/pain-points.md` — Raw pain points organized by theme
- [ ] `discovery/opportunity-scores.md` — Scored idea matrix
- [ ] `discovery/competitor-maps/` — One map per opportunity
- [ ] `discovery/hypotheses.md` — Top 3-5 structured hypotheses
- [ ] `discovery/recommended.md` — AI recommendation with rationale

## Go/No-Go Criteria

**GO** if:
- Score ≥ 6.5/10 on opportunity matrix
- Market size ≥ $500M TAM
- No single dominant competitor (>40% market share)
- Evidence of willingness to pay
- Buildable v1 in 4 weeks

**NO-GO** if:
- Score < 5/10
- Market too small (<$100M TAM)
- Big Tech likely to build in 12 months
- Requires regulatory approval to launch
- Unit economics impossible at realistic price points

## Next Phase

✅ Discovery complete → `playbooks/1-validate/`
