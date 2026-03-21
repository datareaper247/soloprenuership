# Decide — Adversarial Decision Framework

## Auto-Trigger (No Slash Command Needed)
Fires automatically when founder says: "should I X or Y", "I'm torn between", "I can't decide", "what would you do", "help me decide"

---


**Usage**: `/decide "[decision description]"`

Cut through decision fatigue with a structured adversarial debate. Three perspectives, one clear recommendation.

**Examples**:
- `/decide "Should I add a free tier to get more users?"`
- `/decide "Raise prices from $49 to $79/month?"`
- `/decide "Build the analytics dashboard or focus on outbound sales?"`
- `/decide "Hire a part-time VA or automate with n8n?"`

---

## Why This Exists

Decision fatigue is a top-3 killer of solo founder productivity. The average founder makes 35+ business decisions per day. The quality degrades over the day. Wrong strategic decisions cost weeks. Most founders avoid hard decisions by deferring them ("I'll think about it").

This skill forces clarity. Fast.

---

## The Adversarial Debate Protocol

Every `/decide` runs three voices in structured debate:

### Voice 1: The Operator (Pragmatist)
- Thinks in cash flow, time-to-result, and operational complexity
- Asks: "Does this actually work in the real world with limited resources?"
- Bias: Execution risk, hidden costs, founder bandwidth
- Challenge: Always wants "what's the simplest version that could work?"

### Voice 2: The Devil's Advocate (Contrarian)
- Steelmans the case AGAINST whatever the founder is leaning toward
- Asks: "What would have to be true for this to be catastrophically wrong?"
- Bias: Surfaces assumptions, challenges optimism, finds the hidden risk
- Challenge: "What if you're wrong about the core assumption here?"

### Voice 3: The Market Expert (Customer/Revenue Lens)
- Thinks only about: will this produce more revenue? Will customers pay for it?
- Asks: "What does the data say? What would a customer say?"
- Bias: PMF signals, conversion, retention, pricing psychology
- Challenge: "Is there actual demand for this or are you solving your own problem?"

---

## How the Debate Works

The three voices debate in this order:
1. Each states their position (1 sentence)
2. The two strongest objections get surfaced
3. The debate resolves to a recommendation
4. A reversibility score is assigned
5. A kill signal is defined (how to know within 30 days if you're wrong)

---

## Full Decision Framework Output

```
DECISION ANALYSIS: [decision as stated]
Date: [date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTEXT READ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What I understand about your situation:
- Business stage: [inference from context]
- Key constraint: [most limiting factor]
- What's driving this decision: [the underlying pressure]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE DEBATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE OPERATOR says:
[Pragmatic position on the decision — execution feasibility, real-world constraints, founder bandwidth cost]

THE DEVIL'S ADVOCATE says:
[Strongest case AGAINST the most likely direction — the scenario where this goes wrong]
Core assumption being challenged: [the thing that has to be true for the "yes" case to work]

THE MARKET EXPERT says:
[Revenue and customer lens — what the demand signal says, pricing psychology, PMF implications]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPTION A: [Action / Yes case]
  What it requires: [resources, time, money]
  Best case: [what success looks like in 90 days]
  Worst case: [what failure looks like]
  Key assumption: [what has to be true]

OPTION B: [No action / Alternative]
  What it requires: [resources, time, money]
  Best case: [what success looks like in 90 days]
  Worst case: [what failure looks like]
  Key assumption: [what has to be true]

[OPTION C if relevant — hybrid or creative alternative]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Decision: [OPTION A / B / C]
Confidence: [Low / Medium / High] — [why]

Why this wins:
- [Primary reason]
- [Secondary reason]

The condition: [This recommendation only holds if X. If X is not true, reconsider.]

Reversibility: [🟢 Easily reversible / 🟡 Reversible with cost / 🔴 Hard to reverse]
Speed required: [DECIDE NOW / GATHER DATA FIRST / LOW URGENCY]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FIRST ACTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Specific thing to do in the next 24 hours to act on this decision]

KILL SIGNAL
[If [this specific thing] happens within [X days], reverse the decision]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOG THIS DECISION?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Save to context/decision-log.md: [y/n]
```

---

## Special Modes

### `/decide --fast "[decision]"`
When you're 80% sure and need just the push:
```
FAST DECIDE:
My read: [Option A/B]
The one risk to watch: [single biggest downside]
Do it: [yes/no] — [1 sentence]
```

### `/decide --matrix "[decision with multiple options]"`
When there are more than 2 options (pick the tool, pick the market, pick the hire):

Adds a comparison matrix:
```
DECISION MATRIX: [decision]

Criteria weights (auto-generated based on business stage):
- Revenue impact (30%)
- Implementation speed (25%)
- Risk level (20%)
- Reversibility (15%)
- Founder energy cost (10%)

| Option | Revenue | Speed | Risk | Reversibility | Energy | TOTAL |
|--------|---------|-------|------|---------------|--------|-------|
| [A]    | 8/10    | 6/10  | 5/10 | 9/10         | 8/10   | 7.3   |
| [B]    | 6/10    | 9/10  | 8/10 | 7/10         | 9/10   | 7.7   |

Winner: [highest total score]
Caveat: [what the matrix misses that matters here]
```

### `/decide --reversibility "[decision]"`
Optimized for irreversible decisions (pricing changes, co-founder agreements, pivots):

Adds expanded Devil's Advocate section with 3 failure scenarios:
- **Best case wrong**: The plan works but the assumption doesn't hold
- **Execution wrong**: Right strategy, wrong implementation
- **Catastrophic wrong**: This decision breaks something critical

---

## Decision Categories and Default Approach

| Decision Type | Speed | Depth | Note |
|---------------|-------|-------|------|
| Pricing changes | FAST | Medium | Highly reversible for new customers |
| Hiring/firing | SLOW | Deep | High reversibility cost |
| Product pivot | SLOW | Deep | Validate with customers first |
| Feature priority | FAST | Low | Bias to shipping |
| Marketing channel | MEDIUM | Medium | Test cheap before scaling |
| Tool/tech choice | FAST | Low | Almost all reversible |
| Positioning/brand | SLOW | Deep | Hard to reverse, compounds |
| Partnership/deal | MEDIUM | Deep | Model the economics explicitly |

---

## Anti-Patterns This Skill Prevents

### The Analysis Paralysis Loop
- Pattern: Thinking about a decision for weeks without a framework
- Fix: Time-box to 15 minutes. Anything not resolved in 15 minutes needs more data — not more thinking.

### The Optimism Bias
- Pattern: The founder's plan always succeeds in their head
- Fix: Devil's Advocate voice steelmans the case against every default "yes"

### The Sunk Cost Trap
- Pattern: "We already built it, we have to use it"
- Fix: Operator and Market Expert evaluate forward-looking value only

### The HiPPO Effect
- Pattern: The loudest voice wins (Highest Paid Person's Opinion)
- Fix: Three independent voices, each with equal weight in the debate

### The Deferred Decision
- Pattern: "I'll think about this tomorrow" — indefinitely
- Fix: Every `/decide` produces a FIRST ACTION within 24 hours. No exceptions.

---

## Example: Full Decision Run

**Input**: `/decide "Should I add a free tier to get more users?"`

**Context**: $3,800 MRR, B2B SaaS, 22 paying customers, conversion from trial is 8%

**Output**:

```
DECISION ANALYSIS: Add a free tier to increase user acquisition
Date: March 2026

CONTEXT READ
Business stage: Pre-PMF (strong traction signals, still optimizing activation)
Key constraint: Founder bandwidth + infrastructure cost of serving free users
What's driving this: Trial-to-paid conversion at 8% feels low. Hypothesis: freemium gets more users.

THE DEBATE

THE OPERATOR says:
Free tiers create massive support overhead for zero immediate revenue. At $3,800 MRR,
you don't have capacity to support free users. Every hour spent on free users is an
hour not spent converting your 8% to something better.

THE DEVIL'S ADVOCATE says:
You're assuming the conversion problem is a volume problem. It's more likely an
activation problem. Adding 10x more free users doesn't fix an activation problem —
it just creates 10x more unactivated users. Core assumption challenged: that
"more users in = more conversions out" without fixing the funnel first.

THE MARKET EXPERT says:
At $22B2B customers, you don't yet know what makes customers convert. A free tier
muddies the signal — you can't tell if new users convert because of the product or
because of pricing. Your 8% is actually 8%+ with motivated buyers. Free users are
less motivated. Conversion likely drops to 2-4%.

OPTIONS

OPTION A: Add free tier now
  Requires: Infrastructure changes, support bandwidth, clear upgrade triggers
  Best case: 3x signup volume, conversion stays at 6%, reach $8K MRR in 6 months
  Worst case: Conversion drops to 3%, $0 extra revenue, massive support burden
  Key assumption: More trial volume will improve conversion math

OPTION B: Fix activation first, then consider free tier
  Requires: Customer interviews (5 churned + 5 successful), activation funnel audit
  Best case: Conversion improves to 20%, reach $6K MRR with existing volume
  Worst case: No activation improvements found, same conversion rate

RECOMMENDATION

Decision: OPTION B — Fix activation before adding free tier
Confidence: High

Why this wins:
- 8% conversion means 92% of your trial users are leaving without understanding value.
  That's the problem to fix. Free tier amplifies this problem, doesn't solve it.
- 5 customer interviews to understand the activation gap costs 3 hours. The potential
  payoff (doubling conversion) outweighs 6 months of freemium experimentation.

The condition: This holds if your product has a clear "aha moment" that can be accelerated.
If customers tell you "I get the value but can't justify the cost," then free tier makes sense.

Reversibility: 🟢 Easily reversible (revisit in 60 days after activation work)
Speed required: DECIDE NOW (every week without this decision is conversion rate leak)

FIRST ACTION
Schedule 3 customer calls with recent churned trials this week.
Ask specifically: "What would have made you stay?"

KILL SIGNAL
If activation interviews reveal "pricing is the primary objection" (not "didn't see value"),
reverse to Option A. Check at 30 days.
```

---

## Integration

Before `/decide`, use these to get better context:
- `/research customer-profile "[your market]"` — understand customer constraints
- `/research competitor "[competitor]"` — see how competitors made this decision

After `/decide`, log to:
- `context/decision-log.md` — for compound learning across sessions
- Review in `/morning` — the decision shows up in pulse
