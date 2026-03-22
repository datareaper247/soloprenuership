# HIRE — Talent Intelligence Engine
# Auto-triggers: "should I hire", "thinking about hiring", "need a [role]", "first employee", "contractor", "VA", "I'm the bottleneck"

> Drawing from: Paul Graham, Joel Spolsky, Stripe hiring philosophy, Patrick Campbell (ProfitWell),
> Gergely Orosz (The Pragmatic Engineer), Arthashastra Amatya theory, Patrick Lencioni (team dysfunctions).

---

## THE HIRE GATE

**This fires BEFORE any hiring conversation.** Three questions. If you can't answer all three, stop.

```
HIRE GATE:
1. Can you describe exactly what this person will do in Week 1? (not "help me scale")
2. Do you have a written document they can execute WITHOUT asking you questions?
3. Have you been doing this task yourself for >30 days? (If no → document first, hire later)

Fail any gate → Don't hire yet. Document first.
```

**The Arthashastra Amatya Principle** (minister selection):
Kautilya's first test for any minister: "Can this person act with full autonomy in one domain — without requiring your decisions?" A hire who requires your decisions hasn't solved your bottleneck. They've added a management job to it.

---

## STAGE-CALIBRATED HIRING RULES

| MRR Stage | Hire Rule | Who |
|---|---|---|
| $0-5K | **Do not hire anyone.** | Figure out the model yourself first |
| $5-20K | Contractor only. One at a time. | VA for support/ops. Never product. |
| $20-50K | First full-time hire possible. | If founder extraction test passes |
| $50K+ | Build the machine, not you | Hire to documented processes |
| $100K+ | Hire ahead of the need | Revenue → reinvest → compound |

⚠️ **HIRING BEFORE $5K MRR**: You don't know your model yet. Hiring before product-market fit means you're scaling uncertainty. The hire will inherit your confusion and amplify it.

---

## THE 5 SIGNALS IT'S TIME TO HIRE

Fire the hire gate when 3+ of these are true simultaneously:

1. **The Time Audit Test**: You spend >10 hrs/week on documented, repeatable tasks
2. **The Delegation Test**: The task has a written SOP someone else could follow
3. **The Revenue Test**: The hire's time saving = >2x their cost in released founder hours
4. **The Bottleneck Test**: This person unblocks a revenue-generating activity (not "nice to have")
5. **The Regret Test**: You look back in 6 months and this hire was the only thing standing between you and the next level

**Signal that does NOT count**: "I'm overwhelmed." Overwhelm is usually a prioritization problem, not a hiring problem. Run the 4-box automation triage from ops-auto.md first.

---

## THE FOUNDER EXTRACTION TEST

Before hiring anyone, ask: "If I disappear for 2 weeks, what breaks?"

```
EXTRACTION AUDIT:
[ ] Customer support → if you: write the 10 most common responses as templates
[ ] Onboarding → if you: record a Loom, write the checklist
[ ] Content / posting → if you: batch 4 weeks, use Buffer
[ ] Sales calls → if you: create a qualification form that filters for fits only
[ ] Financial reporting → if you: build a Notion/Airtable dashboard that updates itself
[ ] Infrastructure/bug fixes → if you: document the 5 most common issues + resolutions

Items that cannot be extracted → these require you. Protect them.
Items that CAN be extracted → document first, then delegate.
```

**The hiring rule**: You can only delegate what you've extracted. Hire to the document, not to the person.

---

## FIRST HIRE ARCHETYPES

The wrong first hire kills companies. The right one creates 10x leverage.

### Archetype 1: The Operator ($5K-20K MRR)
**Who**: Customer success, operations, executive assistant / VA
**When to hire**: Your sales/ops are working but consuming >15 hrs/week of your time
**What they do**: Handle the repeatable: support tickets, onboarding calls, invoicing, scheduling
**Cost benchmark**: $15-25/hr (VA offshore), $40-70K (US ops person)
**Equity**: 0% to 0.1% — they're not equity-earning, they're leverage-earning
**Risk**: They build technical debt in your processes. Review their work monthly.
**Arthashastra archetype**: The Amatya — a trusted administrator, not a strategist

### Archetype 2: The Builder ($20K-50K MRR)
**Who**: First engineer / developer
**When to hire**: Product velocity is the binding constraint on growth
**What they do**: Ship features you've validated but can't build fast enough
**What they are NOT**: A research partner. They execute your validated product direction.
**Cost benchmark**: $120-200K US, $40-90K remote senior, 0.25-1.0% equity (4-year vest, 1-year cliff)
**Risk**: They build the wrong thing. The solution: weekly alignment on what ships this week.
**The Joel Test**: Apply the Joel Test (12 questions about development environment). A great engineer will thank you for asking.
**Arthashastra archetype**: The Purohita — technical authority in a specific domain

### Archetype 3: The Revenue Hunter ($30K-80K MRR)
**Who**: First account executive / sales hire
**When to hire**: YOU have closed 10+ customers with a repeatable process and >$500 ACV
**What they do**: Execute your sales playbook, not create it
**What they are NOT**: Responsible for figuring out how to sell. That's yours.
**Cost benchmark**: $60-80K base + OTE 1.5-2x, 0.1-0.25% equity
**Risk**: They develop "happy ears" and fill pipeline with wrong-fit deals. Set ICP criteria in writing before they start.
**The Tringas Rule**: Only hire sales after you've sold it yourself 10+ times
**Arthashastra archetype**: The Duuta — the envoy who represents your interests at the frontier

### Archetype 4: The Operator / COO ($80K+ MRR)
**Who**: Chief of Staff, Head of Operations, or part-time fractional COO
**When to hire**: You are the bottleneck in operations and you hate operations
**What they do**: Own the "run the business" work so you can own the "build the business" work
**Cost benchmark**: $100-160K for a strong COO hire, 0.5-2.0% equity
**Risk**: Abdication masquerading as delegation. You still need weekly 1-1s and quarterly reviews.

---

## THE INTERVIEW PROTOCOL (Startup Edition)

Big tech interview processes screen for IQ. Startup interviews screen for judgment and execution in ambiguity.

### 3-Stage Protocol

**Stage 1: The Async Screening Challenge (60 min for candidate, 10 min for you)**
Before any call, send a paid work challenge ($50-100 gift card): a real problem you faced last month.
Not a trick question. A real task they would do in Week 1.
- For ops: "Here are 50 customer support tickets from last week. Write 5 template responses."
- For engineer: "Here's the bug report. Here's a read-only DB schema. Diagnose and describe your fix."
- For sales: "Here's our ICP definition and our pricing. Write the first 3 emails of a cold outreach sequence."

**What you're looking for**: Do they ask smart clarifying questions or do they just execute? Execution without questions = low judgment. Questions without execution = low bias-for-action. Smart execution + clarifying questions = hire.

**Stage 2: The Culture Call (30-45 minutes)**
Two questions carry 80% of the signal:

1. **"Tell me about the last time you identified a problem at work that no one asked you to fix, and what you did about it."**
   — Screen for: initiative, ownership, pattern recognition
   — Red flag: "I waited for my manager to tell me what to do"

2. **"Describe a time you disagreed with a decision your boss made. What did you do?"**
   — Screen for: constructive pushback vs sycophancy vs obstruction
   — Red flag: "I just did what I was told" (no agency) OR "I went around them" (no loyalty)

**Stage 3: The Day-in-the-Life Trial (Paid, 2-4 hours)**
Do one real work session together before any offer. Not a performance — actual work.
- Give them a real ticket to close
- Watch how they think out loud
- Watch how they handle being stuck

**The north star signal**: Do you feel 10x more capable when they're in the room? If the answer is not a clear yes, it's a no.

---

## COMPENSATION PHILOSOPHY

### Salary Benchmarks (USD, 2024)
| Role | Offshore | Remote (non-US) | US Remote | US Local |
|---|---|---|---|---|
| VA / Ops support | $800-2K/mo | $1.5-4K/mo | n/a | n/a |
| First engineer | $30-60K | $60-100K | $130-180K | $150-220K |
| Customer success | $20-40K | $40-70K | $60-90K | $70-110K |
| First AE (sales) | n/a | $50-80K | $70-100K base | $80-120K base |

**Rule**: Pay at the 50th percentile for the role and compensate the difference with equity and mission. Do not try to underpay great people — it creates resentment and they leave at the first offer.

### Equity Benchmarks (Standard vesting: 4-year, 1-year cliff)
| Role | Early (pre-$1M ARR) | Growth ($1M-5M ARR) |
|---|---|---|
| First engineer | 0.5-1.5% | 0.25-0.75% |
| Second engineer | 0.25-0.75% | 0.1-0.4% |
| First sales hire | 0.1-0.4% | 0.05-0.2% |
| First ops / CS | 0.05-0.2% | 0.025-0.1% |
| VP/Head of (any) | 0.5-2.0% | 0.25-1.0% |

**83(b) Election**: Any equity grant requires an 83(b) election filed within 30 days of grant. No exceptions. See legal.md.

**The Slicing Pie Rule**: If cash is constrained, use dynamic equity (Slicing Pie model) that converts contributions to equity at a fair rate. This prevents the "we'll figure out equity later" disaster.

---

## THE TRIAL HIRE PROTOCOL

Never hire full-time without a paid trial first.

```
TRIAL HIRE SEQUENCE:
Week 1-4: Paid project ($2-5K budget)
  → Real scope, real deadline, real work
  → No handholding — minimal context, see what they do with ambiguity
  → Check: Do they ask smart questions? Do they ship?

Week 5-8 (if week 1-4 went well): Part-time engagement (20 hrs/week)
  → Expand scope to include their future FT responsibilities
  → Check: Are they getting better? Do they ask for feedback?
  → Check: Does the relationship create leverage or create management overhead?

Week 9+: Full-time offer (if both parties want it)
  → The offer comes with context: "Based on our 8 weeks together, here's the role..."
```

**Trial cost**: $5-15K before any FT offer. This is cheap insurance against a $100K+ mistake.

**The Hire Rule**: If you feel uncertain at Week 4, extend the trial. If you feel uncertain at Week 8, do not hire. Uncertainty at the offer stage amplifies in the job.

---

## THE LET GO PROTOCOL

The most common founder mistake: keeping underperformers too long.

**The 3-Month Regret Rule** (from Andy Grove, "High Output Management"):
"If the person left tomorrow, would you be relieved or sad?"
If relieved → you already know the answer. The question is when, not if.

### Performance Warning Protocol
1. **Month 1 signal**: Something is off. Document it. One direct conversation: "Here's what I'm observing. Here's what I expected. What's your read?"
2. **Month 2 signal**: Pattern repeating. Put it in writing. A performance memo to yourself AND shared with the employee: "These are the 3 specific outcomes I need to see in 30 days."
3. **Month 3**: If no improvement, begin offboarding. The business cannot afford a 4th month.

**The Direct Conversation**: "This isn't working. I don't think this role is the right fit for you, and I should have said this sooner. I'm going to help with [reference, severance, reasonable transition period]. The decision is made."

**Legal requirements**: Consult an employment attorney before any termination. Requirements vary by state/country. Two-week severance minimum for any good-faith exit. This is not legal advice.

---

## REMOTE VS LOCAL MATRIX

| Factor | Remote-first | Local required |
|---|---|---|
| Async-compatible work | ✅ Remote wins | — |
| High-collaboration product work | ✅ Remote works with timezone overlap | — |
| Sales (enterprise) | — | ✅ Relationship-dependent markets |
| Culture-critical first hires | ✅ Video culture is buildable | ✅ If you're bad at async |
| Your collaboration style | Async-comfortable → remote | Prefer sync → local |

**The timezone rule**: If you need synchronous collaboration, hire within 3 hours of your timezone. Beyond 3 hours = async by necessity.

---

## THE CHANAKYA MITRA HIRING PRINCIPLE

From the Arthashastra, Book 1, Chapter 9 — On the Testing of Ministers:

Kautilya identifies 4 qualities of a reliable minister (Amatya):
1. **Svadharma** — They have internalized the mission as their own, not as employment
2. **Pragyna** — Practical wisdom: they make the right call in the absence of instructions
3. **Utsaha** — Self-motivated initiative: they start without being asked
4. **Dakshatva** — Competence: they ship what they commit to, on time

**Application**: Score each candidate 1-5 on each dimension. Total >15 = hire. <12 = pass. 12-15 = trial hire.

Kautilya adds one more: **Sattvic character** — they tell you bad news immediately, before it gets worse. A "yes" person is not a minister; they are a liability.

---

## HIRING ANTI-PATTERNS

| Anti-Pattern | What It Looks Like | Real Risk |
|---|---|---|
| Comfort hire | Hiring a friend/colleague who's "safe" | Skills misaligned to actual need |
| Resume hire | Impressive background, no startup experience | Corporate patterns don't transfer |
| Passion hire | "So enthusiastic" but no evidence of execution | Enthusiasm ≠ ability |
| Savior hire | Expecting one hire to fix a broken model | They inherit your problems |
| Premature hire | Hiring before you've done the job yourself | Can't manage what you don't understand |
| Clone hire | Hiring someone exactly like you | You both have the same blind spots |

---

## KILL SIGNALS FOR HIRING DECISIONS

```
KILL SIGNAL — Should I hire?
If after 30 days the hire hasn't shipped one meaningful thing you couldn't have done alone → wrong hire or wrong time.

KILL SIGNAL — Correct hire archetype?
If after 60 days the bottleneck you hired to solve still exists → wrong role definition, not wrong person.

KILL SIGNAL — Right compensation?
If 2+ strong candidates reject offers citing comp → you're underpaying for the market. Revisit benchmarks.

KILL SIGNAL — Right stage?
If hiring increased your management burden by >5 hrs/week without equivalent output → process wasn't documented enough to delegate. Go back to ops-auto.md.
```

---

## QUICK REFERENCE: WHO TO HIRE WHEN

```
$0-5K MRR:     No one. You're the company.
$5-15K MRR:    VA / ops contractor (10 hrs/week, offshore, $15-25/hr)
$15-30K MRR:   Part-time contractor in your biggest bottleneck role
$30-70K MRR:   First full-time hire (operator OR builder — not both simultaneously)
$70-150K MRR:  Second hire. Now you have a team.
$150K+ MRR:    Hire ahead of the need. Revenue runway allows it.
```

**The hiring mantra** (from Patrick Campbell, ProfitWell):
"Hire to your strengths, not your weaknesses. Your job isn't to become average — it's to become exceptional at the one thing that moves the needle."

> WISDOM: Arthashastra 6.1 — "A king who employs an incompetent minister ruins himself. A king who employs a competent one wins the world." The quality of your first hire determines whether you are building a company or a job.

---

*ALWAYS INCLUDE: This is not legal or employment advice. Employment law varies by jurisdiction. Consult qualified employment counsel before any hiring, equity grants, or terminations.*
