# Onboard — Context Setup in 10 Questions

## Auto-Trigger (No Slash Command Needed)
Fires automatically when founder says: New session with no context loaded, "starting fresh", "you don't know my business", no MRR mentioned after 3 messages.

---


**Usage**: `/onboard`

**When to run**: First time using SoloOS with a new project. Takes 10-15 minutes.
Populates all four context files with real data so every SoloOS skill works at full power.

Without context files: SoloOS gives generally good output.
With context files: SoloOS gives output calibrated to your specific stage, ICP, and history.

---

## What This Does

Asks you 10 questions. Writes your answers into:
- `context/business-context.md` — product, metrics, ICP, competition, OKRs
- `context/customer-voice.md` — real customer language for copy and messaging
- `context/experiment-log.md` — what you've already tried
- `context/decision-log.md` — key decisions already made

After `/onboard`, you never need to re-explain your business to Claude.

---

## The 10 Questions

Claude will ask these in sequence. Answer honestly — vague answers produce generic output.

```
QUESTION 1 — THE PRODUCT
"Describe your product in one sentence. Not what it does — what it helps
someone accomplish."
(Wrong: "Rankly is a keyword rank tracking tool."
Right: "Rankly lets solo founders know when their keywords drop without
paying Semrush prices.")

QUESTION 2 — THE STAGE
"What's your current MRR? (Or if pre-revenue: how many users / what's the
status?)"
[If they give a number, auto-classify: pre-PMF / early-PMF / growth]

QUESTION 3 — THE CUSTOMER
"Describe your best customer. Not a persona — a real person. What's their
job title, what size company, what were they doing before they found you?"

QUESTION 4 — THE PAIN (in their words)
"What's the exact phrase your best customers use when they describe the
problem you solve? Quote them directly if you can."
(This goes into customer-voice.md as the #1 pain quote.)

QUESTION 5 — THE COMPETITION
"What do your customers use instead of you? What's the #1 reason someone
would choose them over you?"

QUESTION 6 — THE NUMBERS
"Fill in what you know: conversion rate from trial to paid, D30 retention,
CAC, how long it takes to close a deal. Skip what you don't know."
(Unknown numbers are flagged as the highest-priority things to measure.)

QUESTION 7 — THIS QUARTER'S ONE THING
"What's the single most important outcome you need in the next 90 days?
Not a list — one thing."

QUESTION 8 — WHAT YOU'VE TRIED
"Name 2-3 things you've tested in the last 6 months that didn't work the
way you expected, and 1 thing that worked better than expected."
(Goes into experiment-log.md as baseline.)

QUESTION 9 — THE OPEN DECISION
"What's the decision you keep putting off that you know you need to make?
The one that's been on your list for more than 2 weeks."
(Goes into decision-log.md as a pending decision to be resolved.)

QUESTION 10 — THE BLOCKER
"What's the thing that would most accelerate your progress if it were
solved? The thing you don't have an answer to yet."
```

---

## QUESTION 11 — FL-001: YOUR FIRST KILL SIGNAL (v5 addition)

The most important output from onboarding is not the context files — it's your first kill signal.
A kill signal is the specific, measurable data that, if it appears within 30 days, tells you to stop,
pivot, or fundamentally change your current approach.

```
QUESTION 11 — FL-001: FIRST KILL SIGNAL
"Based on everything you just told me — what is the ONE outcome in the next 30 days
that would tell you this is working? And what's the opposite: the specific data
that would tell you to change course immediately?"

Format I'll use to capture it:
  Working signal: [what success looks like in 30 days — specific number]
  Kill signal: [what failure looks like — specific threshold that triggers a change]
  Review date: [30 days from today]
```

After capturing the founder's answer, call `mcp__soloos-core__log_decision` with:
- `decision_type`: "Experiment"
- `summary`: "Onboarding complete — first kill signal set"
- `hypothesis`: [the founder's working signal — what success looks like in 30 days]
- `kill_signal`: [the founder's failure signal — specific threshold that triggers a change]
- `context`: "FL-001 created via /onboard"

This writes `[[FL-001]]` to `knowledge-base/personal/founder-log.md`.
It is the first entry in your personal knowledge graph — your company's decision history starts here.
The GitHub Action now has something to check. The kill signal system is active.

---

## Output After All 11 Questions

Claude writes four context files + creates FL-001, then confirms:

```
ONBOARDING COMPLETE
════════════════════════════════════════════════════

Files written:
  ✅ context/business-context.md — [product name, MRR, ICP, competition, OKR]
  ✅ context/customer-voice.md — [N customer quotes captured]
  ✅ context/experiment-log.md — [N experiments logged]
  ✅ context/decision-log.md — [N decisions logged, 1 open]
  ✅ knowledge-base/personal/founder-log.md — [[FL-001]] kill signal created

WHAT YOU TOLD ME (confirm this is right):
  Product: [one-sentence description]
  Stage: [pre-PMF / early-PMF / growth]
  Best customer: [description]
  This quarter's goal: [OKR]
  Open decision: [decision]
  Biggest blocker: [blocker]
  Kill signal: [FL-001 summary — what data in 30 days means change course]

WHAT I'LL DO DIFFERENTLY NOW:
  Every response will be calibrated to [stage].
  I won't recommend [things wrong for your stage] until [condition].
  When you describe [blocker], I'll prioritize solving that.
  At session start, I'll check FL-001 if [review date] has passed.

FIRST RECOMMENDED ACTION:
  Given what you told me, the highest-leverage thing right now is:
  [Specific action based on their answers]

TO UPDATE CONTEXT: Run /onboard again anytime, or edit the context files directly.
════════════════════════════════════════════════════
```

---

## What Gets Written to Each File

### `context/business-context.md`
Populated from Questions 1-7:
```markdown
# Business Context

## Product
[One-sentence description from Q1]

## Stage
[MRR / status from Q2]
Classification: [pre-PMF / early-PMF / growth / scale]

## Best Customer (ICP)
[Description from Q3]

## Their Pain (In Their Words)
"[Quote from Q4]"

## Competition
Primary alternative: [from Q5]
Our advantage: [from Q5]

## Key Metrics
[Filled from Q6 — unknown metrics flagged]

## This Quarter's OKR
[From Q7]

## Open Questions
[Unknown metrics from Q6 that need to be measured]
```

### `context/customer-voice.md`
Populated from Questions 3, 4, and any quotes shared:
```markdown
# Customer Voice

## Pain Descriptions (Their Exact Words)
"[Quote from Q4]"
Source: [customer type] | Date added: [date]

## ICP Profile
[From Q3 — who your best customer actually is]
```

### `context/experiment-log.md`
Populated from Question 8:
```markdown
# Experiment Log

## What Didn't Work
[Experiment 1 from Q8] — Result: didn't work — Learning: [implication]
[Experiment 2 from Q8] — Result: didn't work — Learning: [implication]

## What Worked Better Than Expected
[Success from Q8] — Result: worked — Learning: [what to double down on]
```

### `context/decision-log.md`
Populated from Question 9:
```markdown
# Decision Log

## Pending Decisions
[Decision from Q9]
Status: Open — In queue for: [how long] — Suggested: Run /decide on this

## Decided
[Any decisions mentioned during onboarding]
```

---

## Re-running /onboard

Run `/onboard` again anytime to update context. Options:

```
/onboard --update     Updates existing files with new information
/onboard --metrics    Updates numbers only (fast — 2 questions)
/onboard --decisions  Updates decision log only
/onboard --voice      Adds new customer quotes to customer-voice.md
```

**Friday ritual** (5 minutes):
```
/onboard --metrics    → Update MRR, key metrics
/onboard --voice      → Add any customer quotes from the week
```

This 5-minute habit builds context that makes every other SoloOS skill more accurate.

---

## Why This Matters

Context files are the multiplier on everything else:

| Without context | With context |
|----------------|-------------|
| `/morning` asks "what are your metrics?" | `/morning` reads them automatically |
| `/decide` gives generic framework | `/decide` calibrates to your stage and past decisions |
| `/validate` checks generic gates | `/validate` flags if idea contradicts known customer voice |
| `/swarm` produces general output | `/swarm` references your ICP and avoids experiments you've already run |
| `/prospect` writes generic outreach | `/prospect` uses your actual customer pain language |

The context investment compounds. A 15-minute `/onboard` pays back in every session after.
