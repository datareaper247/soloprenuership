# Validate — Paid Validation Gate

**Usage**: `/validate "[idea or feature description]"`

**Examples**:
- `/validate "AI-powered invoice reconciliation for small accounting firms"`
- `/validate "Add team collaboration features to my solo-user product"`
- `/validate "Pivot from B2C to B2B"`
- `/validate "Launch a new pricing tier at $299/month"`

The #1 killer of pre-PMF founders: building something that gets positive feedback but no money.
"I'd use that" ≠ "I'll pay for that." This skill forces the paid validation gate before a single line of code gets written.

---

## The Core Problem This Solves

Research from Arvid Kahl, Tyler Tringas, and Justin Jackson consistently shows:
- 70% of failed SaaS products had "lots of interest" during building
- The difference between interest and payment is the validation gate most founders skip
- **Building before 5 paid commitments = burning founder runway on speculation**

This skill won't let you pass without real demand signals.

---

## The Validation Framework

Every idea must pass through 4 gates in sequence. Fail any gate = don't build yet.

```
GATE 1: Problem Existence
Does a painful, urgent problem exist that your idea solves?

GATE 2: Market Signal
Are people currently spending money (time, cash) on inadequate solutions?

GATE 3: Minimum Viable Commitment
Can you get 5 people to give a real commitment BEFORE you build?

GATE 4: Unit Economics
Does the pricing make sense given the problem's perceived value?
```

If all 4 gates pass → BUILD
If any gate fails → The skill tells you exactly what to test first

---

## Full Validation Protocol

### Phase 1: Problem Decomposition

Break the idea into its core problem statement:

```
IDEA SUBMITTED: [your idea]

CORE PROBLEM STATEMENT:
"[Specific person] who [specific situation] struggles to [specific job-to-be-done]
because [specific root cause], which costs them [specific measurable consequence]."

Test this statement against: Is this specific enough that you could find 20 people
on LinkedIn who fit this description in 30 minutes?

If not → the problem is too vague. Narrow it.
```

### Phase 2: Competing Solutions Audit

The market tells you demand exists. Research what people pay for today:

```
COMPETING SOLUTIONS AUDIT:
Paid alternatives (what they pay now): [list]
Free workarounds (what they DIY): [list]
Status quo (doing nothing): [cost of inaction]

If no one pays for anything in this space → demand may not exist.
If people cobble together 3 free tools → demand exists, willingness to pay unclear.
If people pay $X/month for worse solutions → strong demand signal.

DEMAND SIGNAL STRENGTH: [Strong / Medium / Weak / Unknown]
Basis: [evidence]
```

### Phase 3: The 5 Commitments Test

The validation gate. Not signups. Not "interested." Real commitments.

**Commitment tiers** (ranked by strength):
```
Tier 1 (weakest): Email signup for waitlist
Tier 2: Verbal "yes I'd pay for that" in a call
Tier 3: Survey with email + stated willingness to pay
Tier 4: LOI / Letter of Intent (for B2B)
Tier 5 (strongest): Pre-payment / deposit / founding member purchase
```

**SoloOS validation standard: You need 5 Tier 4+ commitments before building.**

For founders who say "I can't get pre-payments before building" — you can:
- B2B: "We're building this. Would you sign a letter of intent to pay $X/month if it does Y?"
- B2C: "We're launching in 6 weeks. Founding member price is $X. 50 spots."
- Internal test: "I'll build you a manual version first. Will you pay $X/month for it?"

```
COMMITMENT PLAN:
Target: 5 Tier [4/5] commitments
Who to approach: [specific 10-15 people, companies, or channels]
Your ask: "[Exact script — one sentence pitch + one commitment request]"
Timeline: [how many days to gather 5 commitments]
```

### Phase 4: The Pricing Sanity Check

Founders systematically underprice because they're afraid. This gate prevents that.

```
PRICING ANALYSIS:
Problem severity: [1-10 — how urgent/painful is this?]
Cost of status quo: [what does NOT solving this cost them per month?]
Comparable solutions: [what do similar solutions charge?]
Your target price: $[X]

PRICE SANITY:
If your price < 10% of the cost of the problem → you're undercharging. Raise it.
If your price > 50% of the cost of what they pay for alternatives → justify the premium.

Price recommendation: $[X]
Floor (don't go below): $[X]
Ceiling (push test): $[X]
```

---

## Validation Output Format

```
VALIDATION ASSESSMENT: [Idea Title]
Date: [date]
════════════════════════════════════════════════════

PROBLEM STATEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Refined 1-2 sentence problem statement with specific person + situation]
Specificity score: [High/Medium/Low] — [how easy to find these people]

GATE 1: PROBLEM EXISTS? [✅ PASS / ⚠️ UNCLEAR / ❌ FAIL]
Evidence: [what we know]
Gap: [what needs to be confirmed]

GATE 2: MARKET SIGNAL? [✅ PASS / ⚠️ UNCLEAR / ❌ FAIL]
Current spend: [what people pay for alternatives]
Demand signal: [Strong/Medium/Weak]
Gap: [what would strengthen this]

GATE 3: COMMITMENTS POSSIBLE? [✅ PASS / ⚠️ UNCLEAR / ❌ FAIL]
Commitment plan:
  Target people: [who + where to find them]
  Your ask: "[exact script]"
  Commitment type: Tier [X] — [description]
  Timeline: [days]

GATE 4: UNIT ECONOMICS? [✅ PASS / ⚠️ UNCLEAR / ❌ FAIL]
Recommended price: $[X]/[mo|yr|one-time]
Problem cost: $[X]/mo (basis: [how calculated])
Price floor: $[X] | Price ceiling: $[X]

════════════════════════════════════════════════════
OVERALL VERDICT
════════════════════════════════════════════════════
[🟢 BUILD — All gates pass]
[🟡 VALIDATE FIRST — [X] gates unclear. Do these tests first:]
[🔴 DO NOT BUILD — Gates [X,Y] fail. Here's what's wrong:]

WHAT TO DO NEXT:
[If Build]: First 3 steps to execute in 48 hours
[If Validate First]: Cheapest experiment to clear the gate(s)
[If Don't Build]: What variant might work / what to try instead

TIME ESTIMATE TO VALIDATE: [X days with X hours/day]
MINIMUM VIABLE FIRST VERSION: [description — if validated]
```

---

## Special Modes

### `/validate --fast "[idea]"`
30-second gut check. Returns:
```
QUICK VALIDATION:
Biggest assumption: [the single thing that has to be true]
Cheapest test: [how to validate in under a week]
Red flag: [the thing most likely to kill this]
Verdict: [Proceed to full validation / Stop here]
```

### `/validate --feature "[existing product + feature]"`
For adding features to an existing product. Uses customer voice data if available.
Asks: "Is this a customer request or a founder assumption?"
Tests against: churn data, support tickets, and existing customer interviews.

### `/validate --pivot "[current business + pivot direction]"`
For major strategic pivots. Adds:
- Sunk cost analysis (what you're giving up)
- Transition path (how to validate without shutting down the current business)
- Bridge revenue (how to fund validation without killing current cash flow)

---

## The Arvid Kahl Rule (Built Into This Skill)

From "The Embedded Entrepreneur": **Idea comes AFTER audience, not before.**

If you're running `/validate` on an idea you came up with yourself without talking to customers:

**Automatic flag**:
"⚠️ ORIGIN CHECK: This idea originated from you, not from your audience.
Before running full validation, answer: Did you hear this problem from 3+ potential customers in their own words?
If no → spend 2 hours in [relevant community] listening before validating an idea you invented."

This flag doesn't block — it surfaces. You decide. But you saw it.

---

## Anti-Patterns This Prevents

| Pattern | What Founders Do | What This Forces |
|---------|-----------------|-----------------|
| Survey validation | "I sent a survey, 80% said they'd use it" | Surveys ≠ payment intent. Show me a Tier 4+ commitment |
| Friends' opinions | "5 founder friends said it's a great idea" | Founders aren't customers. Find actual potential buyers |
| Building for 6 months | "I just need to finish it before I can show it" | The manual/concierge version can be shown today. Do that first |
| Price fear | "I'll start at $9/month and raise later" | Price math doesn't work. Start at the right price or you'll never raise it |
| Generic market size | "This is a $10B market" | TAM doesn't validate demand. Your 5 commitments do |

---

## After Validation

Once 5 Tier 4+ commitments are collected:
1. Log the validation in `context/experiment-log.md` as Experiment #[N]
2. Use `/decide "How to build the minimum viable version"` for build decision
3. Use `/swarm product-launch "[validated product]"` when ready to launch
4. Use `/morning` to track validation metrics daily
