# Example: /validate catching a fatal flaw before code was written

**Command used**: `/validate "AI meeting summary tool that auto-creates Notion docs"`

**Context**: Founder has been using a painful manual process — copying Zoom transcripts into Notion and summarizing them — and wants to automate it. They've been building for 2 weeks when they run /validate.

---

## Input

```
/validate "AI meeting summary tool that auto-creates Notion docs from Zoom calls"
```

---

## Output

```
VALIDATION ASSESSMENT: AI Meeting Summary → Notion
Date: 2026-03-20
════════════════════════════════════════════════════

PROBLEM STATEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Professionals who run 5+ meetings per week and use Notion as their
knowledge base struggle to transfer meeting insights into structured
docs because manual transcription and formatting takes 15-20 min per
meeting — 75-100 min/week of pure administrative overhead.

Specificity score: Medium — "professionals who use Notion" is broad.
Narrowing test: Can you find 20 of these people on LinkedIn in 30 min?
Answer: Not reliably. "Notion power user + frequent meetings" is not a
searchable LinkedIn filter. The ICP needs to be narrower.

⚠️ ORIGIN CHECK (Kahl Rule)
This idea appears to originate from personal pain, not community listening.
Before running full validation, answer: did you hear this problem from 3+
potential customers in their own words?
If no: spend 2 hours in r/Notion or Notion's Slack community listening before
validating an idea you invented.

────────────────────────────────────────────────────

GATE 1: PROBLEM EXISTS? ⚠️ UNCLEAR
Evidence: You personally have this pain. That's 1 data point.
Gap: No community validation. Need to confirm 5+ people describe this
exact friction unprompted — not responding "yes" to a leading question.

────────────────────────────────────────────────────

GATE 2: MARKET SIGNAL? ❌ FAIL
Current spend on alternatives:
  - Otter.ai: $17/mo (transcription only)
  - Fireflies.ai: $18/mo (transcription + basic summaries)
  - Notion AI: $10/mo add-on (already inside Notion)
  - tl;dv: $25/mo (meeting recording + summaries)
  - Fathom: FREE (AI meeting notes, no cost)

CRITICAL FINDING: Fathom does exactly this for free. 100,000+ users.
Your target customer is already using a free solution.

Demand signal: WEAK — market exists but is captured by free tools.
The question is not "will people want this?" but "will they pay for it
when they can get it free?"

Gap: You need to find the specific thing Fathom/tl;dv does badly for
your exact ICP. "AI meeting summaries → Notion" is solved. "AI meeting
summaries → [specific workflow/format/integration] for [specific team
type]" might have a gap.

────────────────────────────────────────────────────

GATE 3: COMMITMENTS POSSIBLE? ❌ FAIL
If Gate 2 failed, Gate 3 cannot pass.

The commitment ask would be:
"I'm building a meeting summary tool that pushes structured notes to
Notion. Would you pay $15/mo for it?"

Predicted response: "I already use Fathom, it's free."

No realistic path to 5 Tier 4+ commitments at any price > $0 until
you've identified what Fathom doesn't do for your specific ICP.

────────────────────────────────────────────────────

GATE 4: UNIT ECONOMICS? ❌ FAIL
Recommended price based on alternatives: $0-$15/mo
Problem cost (time): ~$50-100/mo in saved labor
Comparable free solutions exist at $0.

At $15/mo vs. $0 (Fathom): Every prospect asks "why pay?"
Without a clear answer, conversion will be < 2%.

Price floor: Can't go lower than $0. Hard to compete with free.
Price ceiling: $29/mo if you find a specific ICP with a workflow gap.

════════════════════════════════════════════════════
OVERALL VERDICT: 🔴 DO NOT BUILD — Gates 2, 3, 4 all fail.
════════════════════════════════════════════════════

Core problem: You're building into a market captured by free alternatives.
Fathom has 100K+ users and is free. Unless you have a specific workflow
gap they don't serve, you're asking people to pay for what they get free.

WHAT TO DO NEXT:
────────────────
Option A — Find the gap inside the free tools (most likely path):
  1. Join the Fathom + tl;dv communities and find top complaints
  2. Look for: "I wish Fathom did X" or "Fathom doesn't work for Y"
  3. If you find a workflow pattern 20+ people complain about, validate that
     specific gap — not the generic "meeting → Notion" problem

Option B — Find a specific ICP that pays for premium (harder):
  Segments that might pay for premium meeting tools:
  - Revenue teams tracking action items and CRM updates (Salesforce integration)
  - Agencies billing clients (time + project tracking from meetings)
  - Product teams extracting feature requests into Jira/Linear from user calls
  None of these are "meeting → Notion." They're specific workflow integrations.

Option C — Kill this idea (honest answer if A and B look bleak):
  This is a crowded, free-tier dominated space. Your time has higher ROI
  elsewhere unless you find a very specific enterprise workflow gap.

TIME TO VALIDATE: 2 weeks listening in communities, 0 hours coding.

════════════════════════════════════════════════════
```

---

## What Happened After

The founder ran this before completing their MVP (2 weeks in). They:
1. Joined the Fathom user community and spent 3 days reading complaints
2. Found a consistent pattern: "Fathom summaries are great but they don't capture action items in a format our PM tool understands"
3. Pivoted to: "meeting action items → Linear tickets, auto-assigned, with due dates" for engineering teams
4. Found that pattern in 8+ separate complaints — different people, same workflow gap
5. Got 6 pre-commitments at $29/mo in 10 days without writing a line of new code

**The /validate output saved ~6 weeks of building into a saturated free-tier market.**

---

## What This Example Demonstrates

1. **Gate 2 is where most ideas die** — not because the problem isn't real, but because free alternatives already exist
2. **The Kahl Rule fires correctly** — founder-invented idea without community listening gets flagged before analysis
3. **The output tells you what to do, not just what's wrong** — Option A/B/C gives a concrete path
4. **Specificity unlocks willingness to pay** — "meeting → Notion" = $0, "meeting action items → Linear" = $29/mo
