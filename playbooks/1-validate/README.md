# Phase 1: VALIDATE

> Get 5 strangers to pay you before building anything.

## Goal

In 1-2 weeks:
- Confirm the problem is real through primary research
- Validate willingness to pay at your target price
- Identify your beachhead customer segment
- Make the go/build/pivot decision

## The Validation Protocol

### Step 1: Landing Page Test (Day 1-2)

**Build in 4 hours** (not days):
- Headline: The outcome you deliver
- Sub-headline: How and for whom
- 3 bullet points: Key benefits
- Social proof: Even a quote from a Reddit post
- CTA: "Join Waitlist" (collect email + job title)

**Tools**: Carrd ($19/yr), Framer, or Webflow in 2 hours
**Drive traffic**: Post in relevant subreddits, LinkedIn, HN

**Signal**: >5% conversion = people want this. <1% = messaging problem.

### Step 2: Customer Interview Script (Day 2-7)

**Target**: 15-20 interviews in 2 weeks
**Find them**: Reddit DMs, LinkedIn, existing network, Slack communities

**The Mom Test Framework**:
```
1. Context setting (2 min)
   "Tell me about your day-to-day work..."
   "Walk me through the last time you had to deal with [problem area]..."

2. Problem exploration (10 min)
   "What's the hardest part of [X]?"
   "How do you currently handle that?"
   "How much time does that take?"
   "What have you tried to fix it?"

3. Solution probing (5 min)
   "What would the perfect solution look like?"
   "Would you pay for something that solved X?"
   [If yes] "What would you pay per month?"

4. Competitive awareness (3 min)
   "What tools do you currently use for this?"
   "Why haven't you switched?"

AVOID: "Would you use this?" (Hypotheticals lie)
ASK: "How are you solving this today?"
```

### Step 3: Concierge MVP (Day 5-14)

Before building software, manually deliver the value:
- Offer to do it for free for 3-5 target customers
- You do the work manually (with AI assistance)
- Observe: where is the friction? What do they value?
- This IS your product research

**Example**: If building a market research tool → manually produce a market research report for them using your AI workflow. Charge $0. Learn everything.

### Step 4: Pre-Sell (Day 10-14)

The ultimate validation: someone pays before you build.

**Pre-sale approaches**:
- "Early Access" at 50% discount: Annual paid upfront
- Pilot program: $500-2000 for 3-month beta
- Letter of intent: Signed commitment (for B2B)

**Target**: 3+ paying customers OR 10+ waitlist with credit card

## Validation Agent Swarm

**Deploy**: `framework/swarms/validation-swarm.yaml`

1. **Interview Synthesizer** → Process interview notes → patterns
2. **Hypothesis Tester** → Score original hypotheses against findings
3. **Segment Definer** → Identify highest-value ICP (Ideal Customer Profile)
4. **Pricing Researcher** → Competitive pricing analysis
5. **Decision Agent** → Build/pivot/kill recommendation

## The Validation Decision Matrix

| Signal | Build | Pivot | Kill |
|--------|-------|-------|------|
| Pre-sales | 3+ paying | 1-2 interested | 0 |
| Interview sentiment | 80%+ confirmed pain | 50% confirmed | <30% |
| Landing page CVR | >5% | 2-5% | <1% |
| Pricing acceptance | Accepted at target | Need to discount | Won't pay |
| Competitor gap | Clear gap found | Small gap | No gap |

## Outputs

- [ ] `validation/interview-notes/` — Raw interview notes
- [ ] `validation/synthesis.md` — Patterns and insights
- [ ] `validation/icp.md` — Ideal Customer Profile definition
- [ ] `validation/pricing.md` — Validated pricing range
- [ ] `validation/decision.md` — Build/pivot/kill with rationale
- [ ] `validation/pre-sales.md` — Tracking of pre-sales

## Go/No-Go Criteria

**BUILD** if:
- 3+ pre-sales OR strong LOI from B2B customers
- 12+ interviews confirm the problem
- Clear ICP defined
- Pricing validated (they'll pay your target price)
- Competitive gap confirmed

**PIVOT** if:
- Problem confirmed but solution rejected
- Wrong customer segment
- Price resistance (adjust tier, not abandonment)

**KILL** if:
- <30% of interviews confirm the problem
- No pre-sales after genuine attempts
- Market dominated by free tools they love

## Next Phase

✅ Validation complete → `playbooks/2-build/`
