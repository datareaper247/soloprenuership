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

## Pre-Debate Data Check (NEW — Fires Before Every Debate)

Many decisions are data-collection problems disguised as decision problems. Running an adversarial debate on zero data produces confident-sounding wrong answers.

Before entering the debate, check:

```
DATA READINESS CHECK:
Decision type: [pricing / product / channel / hiring / pivot / other]
Data available: [what we actually know vs. what we're assuming]
Missing data: [what would make the right answer obvious]
Collection time: [how long to gather the missing data]

If missing data collectible in <14 days AND reversibility is ≤5/10:
→ "Recommend gathering data first. Here's the 14-day experiment..."
→ Debate runs anyway with explicit uncertainty flagging

If missing data not collectible (real deadline, irreversible) OR reversibility ≥7/10:
→ Proceed to debate with explicit assumptions labeled
```

## How the Debate Works

**Dual-Process Routing** (new in v3):
- **System 1 (Fast)**: Reversibility ≥7/10 and strong pattern match → Skip full debate, return pattern + recommendation in under 60 seconds
- **System 2 (Deliberate)**: Reversibility ≤5/10 OR no pattern match → Full adversarial debate below

For System 1 fast-path, show the matched pattern explicitly:
```
PATTERN MATCH: P-[XX] — [Pattern name]
Evidence: [Real founder who faced this exact situation + outcome]
Recommendation: [1 sentence]
Kill signal: [what proves this wrong in 30 days]
(Use /decide --deep to force full System 2 debate)
```

For System 2 full debate, run voices in this order:
1. Each states their position (1 sentence)
2. The two strongest objections get surfaced
3. The debate resolves to a recommendation
4. A reversibility score is assigned
5. A kill signal is defined (how to know within 30 days if you're wrong)

**BSHR Evidence Display** (mandatory in System 2): The BSHR loop must SHOW its evidence, not apply it silently.

**CRITICAL**: Before starting the debate, Claude MUST explicitly call `search_founder_cases` with the decision topic AND `match_pattern` with relevant keywords. Do not skip this. Do not apply patterns silently. Show the evidence.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANALOGOUS CASE (from founder knowledge base)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Call search_founder_cases("decision topic") and match_pattern("keywords") BEFORE this section]

Case: [Founder name or type] faced "[exactly this decision]" at [$X MRR in Y market].
They chose: [the option]
Outcome at 90 days: [specific result — number, not vague]
What made it work: [1 specific factor]
What almost killed it: [1 specific risk]

Your situation differs in: [what's different — do NOT pretend it's identical]
Pattern match confidence: [HIGH — >3 similar cases / MEDIUM — 1-2 cases / LOW — extrapolation only]
Pattern ID: [[P-XX]] (link to pattern for full detail)

If no case found: "No direct match in knowledge base. Proceeding with first-principles analysis."
```

---

## Anti-Advisor Protocol (Mandatory for Reversibility ≤5/10)

The Devil's Advocate voice is not enough. For hard-to-reverse decisions, a dedicated **Anti-Advisor** runs before the recommendation is finalized.

The Anti-Advisor's mandate: *Find the scenario where this decision is catastrophically wrong.* Not "here are some risks" — the strongest possible case for why this fails.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANTI-ADVISOR REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Deliberately pessimistic. This is the Red Team report.]

Failure scenario: [The most likely way this goes badly wrong — be specific]
Underlying assumption that breaks it: [The ONE assumption, if wrong, kills this]
Evidence this assumption is fragile: [Why we can't be confident it's true]
Pre-mortem (6 months from now, this failed): [What specifically happened]

Anti-advisor verdict: [STRONG RISK / MODERATE RISK / ACCEPTABLE RISK]
What would change this verdict: [Specific data that would lower the risk]
```

The recommendation is only considered final after the Anti-Advisor report is shown to the founder. They can override — but they saw the strongest case against.

## Expected Value Framing (for time-allocation decisions)

When the decision involves allocating founder time between two activities, add EV framing:

```
EV ANALYSIS: [Activity A] vs [Activity B]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Activity A]:
  Time required: [X hours]
  Estimated probability of positive outcome: [Y%]
  If outcome positive: $[Z] revenue impact
  EV: Y% × $Z ÷ X hours = $[EV/hr]

[Activity B]:
  Time required: [X hours]
  Estimated probability: [Y%]
  Revenue impact if success: $[Z]
  EV: Y% × $Z ÷ X hours = $[EV/hr]

Highest EV activity: [A or B] at $[EV/hr]
Caveat: [What this analysis misses — asymmetric bets, compounding, etc.]
```

*Note: These are rough estimates, not precision math. The point is to surface order-of-magnitude differences, not false precision.*

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
ANALOGOUS CASE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Result of search_founder_cases + match_pattern call]
Founder/case: [Name or type] at [$X MRR in Y category]
They chose: [option] → 90-day outcome: [specific result]
Confidence: [HIGH / MEDIUM / LOW] | Pattern: [[P-XX]]
Differs from yours in: [what's NOT the same]

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
PRE-MORTEM (only for reversibility ≤ 5/10)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Apply Gary Klein's pre-mortem technique for hard-to-reverse decisions]

Imagine it's 90 days from now. You made [this decision]. It failed badly.
What happened?

Most likely failure scenario: [specific cause]
Core assumption that turned out wrong: [what had to be true but wasn't]
Second most likely failure scenario: [different failure path]

What would prevent failure scenario 1: [specific action]
What would prevent failure scenario 2: [specific action]

Pre-mortem confidence: If you can name specific, credible failure scenarios, the decision is well-understood.
If you cannot name how this fails, you don't yet understand the decision well enough to make it.

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
