# Validate — Paid Validation Gate

## Auto-Trigger (No Slash Command Needed)
Fires automatically when founder says: "thinking about building X", "I want to add X", "should I build X", "my idea is X", "I'm planning to X"
**Arvid Kahl Rule fires first**: "Did 3+ customers describe this pain in their own words? If not, listen before building."

---

**Usage**: `/validate "[idea or feature description]"` *(or just describe what you're thinking about building)*

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

Every idea must pass through a Pre-Gate and then 4 gates in sequence. Fail any gate = don't build yet.

### GATE 0: ChatGPT Substitution Test (NEW — Pre-Gate)

**The #1 undetected failure mode (25-30% of AI product failures): the free LLM absorbed your use case.**

Before ANY validation work, run this test in 5 minutes:

```
CHATGPT SUBSTITUTION TEST:
1. Open ChatGPT or Claude (free tier)
2. Describe your product's core value in one sentence
3. Ask it to perform that exact function for you — right now

Result A: It does it adequately → You're building against a free competitor with infinite marketing budget.
          Options: (a) Find narrower niche with compliance/integration moat, (b) Find workflow step
          where LLM alone fails (data connectivity, multi-step automation, domain-specific training)

Result B: It can't do it → You have a real gap. Continue to Gate 1.
Result C: It does it badly → Document the gap specifically. That gap is your product.
```

**Services-to-Software shortcut** (highest validation confidence): Before running the 4 gates, ask: "Am I this customer?" If yes — you have lived experience as your own validation. Skip Gates 1-2. Document your exact painful workflow, then jump to Gate 3 (will others pay?) and Gate 4 (unit economics).

```
SELF-AS-CUSTOMER CHECK:
- Do I personally experience this problem? [yes/no]
- Have I built/documented a manual solution for myself? [yes/no]
- If yes to both → document your workflow first, validate others will pay second
  (This is the Arjun Jain / Services-to-Software flywheel — highest conviction path)
```

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

If Gate 0 passes AND all 4 gates pass → BUILD
If Gate 0 fails → Narrow or reframe before continuing
If any of Gates 1-4 fail → The skill tells you exactly what to test first

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

Founders systematically underprice because they're afraid. This gate runs 4 pricing frameworks to find the right number before you commit.

> **The Marc Lou Insight**: "If your first 20 customers paid without negotiating, your price is almost certainly too low."

---

#### Framework 1: Anchored Value Calculation

Show the cost of the alternative before showing your price. The anchor sets the frame.

```
ANCHOR CALCULATION:
Problem: [what does this replace?]
Alternative cost: [hours × hourly rate] OR [service cost] OR [tool cost × time saved]

Format: "Replaces [X hours] of [activity] at $[rate]/hr = $[total] of value."
Your price: $[actual price]
Value ratio: [anchor ÷ your price] — must be >5x to feel compelling

ShipFast example: $4,000 anchor ($40/hr × 100 hours saved) → $299 felt cheap.
The anchor belongs above the fold on your landing page, not below it.

ANCHOR RECOMMENDATION:
Anchor: $[X] in value
Your price: $[X]
Value multiple: [X]x
```

---

#### Framework 2: Van Westendorp Price Sensitivity

Run this BEFORE committing to a price point. Requires 30+ respondents (use your waitlist, cold outreach targets, or ICP communities).

**The 4 questions**:
1. "At what price would [Product] be so cheap you'd question its quality?"
2. "At what price is [Product] starting to feel like a good deal?"
3. "At what price is [Product] starting to feel expensive but you'd still consider it?"
4. "At what price would [Product] be too expensive to consider?"

**Plot 4 curves**:
- "Too cheap" (Q1) — ascending
- "Good value" (Q2) — descending
- "Getting expensive" (Q3) — ascending
- "Too expensive" (Q4) — descending

**Acceptable price range**: Where "too cheap" crosses "getting expensive" → where "too expensive" crosses "good value"

**Optimal price point** (PMC): Where "too expensive" and "too cheap" intersect

```
VAN WESTENDORP SHORTCUT (for pre-survey situations):
Too cheap threshold: $[X] (below this, customers distrust quality)
Sweet spot: $[X]-$[Y] (acceptable range)
Ceiling: $[Z] (above this, majority won't consider)
Recommended launch price: Middle of acceptable range
```

**Practical shortcut without survey**: Map against 3 comparable tools in the category. Price at 70-100% of the mid-tier competitor (not the cheapest, not the most expensive). Adjust after 20 customers.

---

#### Framework 3: Three-Tier Decoy Pricing Structure

The decoy effect: a middle-tier option looks compelling when flanked by a cheap option (obviously limited) and an expensive option (obviously more than needed).

```
DECOY PRICING TEMPLATE:

Starter: $[X]/mo
  → Include: [2-3 features — deliberately limited to make next tier look right]
  → Cap: [sessions / documents / seats / API calls — specific limit]
  → Designed to: make Pro look like the obvious choice

Pro: $[2-3X]/mo  ← designed as the natural landing point
  → Include: [full core features — everything most customers need]
  → Cap: [generous or unlimited]
  → This is the tier you optimize conversion for

Business: $[4-5X]/mo
  → Include: [multi-seat, advanced features, priority support]
  → Anchor effect: makes Pro look like a deal by comparison

Recommended Pro:Starter price ratio: 2.5-3x
Recommended Business:Pro price ratio: 2x

Annual pricing: 20% discount on Pro tier (target 20-35% of new users choosing annual)
```

**Example calibration** (generic B2B SaaS tool):
- Starter: $29/mo (up to 10 documents/month)
- Pro: $79/mo (unlimited + integrations) ← designed as the landing point
- Business: $149/mo (multi-seat + API + priority) ← anchor for Pro

---

#### Framework 4: Price Increase Playbook (For Post-Launch)

When to raise: After 50 paying customers with stable conversion rate.

```
MARC LOU PRICE LADDER:
ShipFast actual history: $99 → $149 → $199 → $299

RAISE PROTOCOL:
1. Announce on Twitter/X with 7-day warning: "Raising price from $X to $Y on [date]"
2. Grandfather ALL existing customers at their current rate (non-negotiable — loyalty signal)
3. Monitor conversion rate for 2 weeks after increase
4. Kill signal: conversion drops >50% from prior level → found the price ceiling → return to prior price
5. Annual lock-in at increase announcement:
   Offer existing monthly customers: "Lock in annual at current rate before price increases"
   Expected conversion: 15-25% of monthly → annual
   Benefit: Cash flow + churn reduction simultaneously

Price increase frequency: Every 50 new customers OR every $5K MRR milestone
```

---

#### Unified Pricing Output

```
PRICING ANALYSIS: [Product Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ANCHOR VALUE:
Problem cost / alternative: $[X] per [period]
Your price: $[X]
Value multiple: [X]x → [compelling / marginal / weak]

PRICE RANGE (Van Westendorp estimate):
Too cheap: below $[X]
Acceptable range: $[X]-$[Y]
Ceiling: above $[Z]

RECOMMENDED LAUNCH PRICE: $[X]/[period]
Floor (don't go below): $[X]
Growth price (after 50 customers): $[X]

TIER STRUCTURE:
Starter: $[X]/mo — [key limitation]
Pro (main): $[X]/mo — [full value]
Business: $[X]/mo — [multi-seat / enterprise]

PRICING RED FLAGS:
→ Price < $[X]: Underpricing. Raise before launch.
→ First 20 customers paid without negotiating: ⚠️ TEST HIGHER.
→ Demo to paid conversion <10%: NOT a pricing problem — wrong buyer or objections.
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
Anchor value: $[X] ([problem cost or alternative cost])
Recommended price: $[X]/[mo|yr|one-time] (value multiple: [X]x)
Acceptable range: $[X]-$[Y] (Van Westendorp estimate)
Price floor: $[X] | Growth target price: $[X]
Tier structure: Starter $[X] / Pro $[X] / Business $[X]

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
