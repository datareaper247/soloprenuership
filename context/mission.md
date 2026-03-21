# SoloOS Mission — Strategic Root

> This is the strategic root of your venture. SoloOS uses this file to evaluate every action against your ultimate goal via backwards induction. Keep it accurate. A wrong goal produces a wrong critical path.

---

## 1. THE EXIT: What are you actually building towards?

Choose one. Be specific with numbers and timeframes. Vague goals produce vague advice.

```
[ ] Acquisition: Sell for $[amount] in [X] months
[ ] Lifestyle Business: $[MRR] with [X] hrs/week max, no team
[ ] Fundable Startup: $[MRR] then raise Series A in [X] months
[ ] Portfolio: [X] products, each at $[MRR] — managed passively
```

**My exit:** `[fill this in]`

---

## 2. THE CRITICAL PATH MILESTONE

The single quantifiable milestone that must be hit for the exit to be possible. Not the exit itself — the necessary precondition.

Examples:
- "Achieve $10K MRR"
- "1,000 paying customers"
- "40% D30 retention with 3 customers as reference accounts"
- "$5K MRR in one ICP vertical before expanding"

**Our critical path milestone:** `[fill this in]`

**Deadline:** `[fill this in — be specific, e.g., 2026-09-01]`

---

## 3. THE BACKWARDS INDUCTION MODEL

Working back from exit → critical path → today:

```
Exit goal: [copy from section 1]
  ↑ requires
Critical path milestone: [copy from section 2]
  ↑ requires at 60% of timeline
[milestone @ 60%]
  ↑ requires at 30% of timeline
[milestone @ 30%]
  ↑ requires in next 30 days
[next 30-day target]
  ↑ requires this week
[this week's one action]
```

**This week's one action:** `[fill this in — Claude will help you derive this]`

---

## 4. THE CURRENT OBSTACLE

The one thing blocking progress toward the critical path milestone RIGHT NOW. Not all blockers — the most important one.

If solved, everything else gets easier. If not solved, everything else is noise.

**#1 obstacle:** `[fill this in]`

---

## 5. GOAL DRIFT LOG

When your exit goal changes, document it here. Don't erase — append. Knowing your past goals reveals whether you're pivoting based on data or emotion.

| Date | Previous Goal | New Goal | Reason |
|---|---|---|---|
| [date] | [what you wanted] | [what you want now] | [why it changed] |

---

## HOW SOLOS USES THIS FILE

Every strategic question gets evaluated against this mission. Claude will say:

> "This action [aligns with / diverges from] your critical path to [milestone] because [reason]. Based on backwards induction, at this stage you need to [X], not [Y]."

This is not permission-gating. You can still do whatever you decide. The mission file is a compass, not a lock.

**To update this file**: Edit directly and tell Claude "mission updated." Claude will re-derive the backwards induction model and update the recommended week's action.

**To start fresh**: Run `/onboard` — it will ask the goal questions and write this file for you.
