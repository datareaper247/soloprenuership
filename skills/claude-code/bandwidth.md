# Bandwidth — Founder State Detection & Capacity-Aware Routing

## Auto-Trigger (No Slash Command Needed)
Fires automatically when:
- Morning brief or "what should I focus on today"
- Founder describes feeling overwhelmed, burned out, scattered
- **MANDATORY**: Before ANY decision with reversibility ≤5/10
- 45+ days on a project with no paying customer (abandonment cliff zone)
- Guna diagnostic detects Tamas or Rajas state
- Language signals: exhaustion, urgency-without-data, emotional reactivity

---

**Usage**: `/bandwidth` or fires automatically

Prevents the worst failure mode: irreversible decisions made in depleted cognitive state.
A solo founder in Tamas making a reversibility 3/10 decision is more dangerous than no decision.

---

## Why This Exists

Georgetown Law research: AI is MORE likely to validate bad ideas when the founder is in depleted state — the sycophancy compound effect. At the moment when a founder most needs pushback, both their judgment AND the AI's calibration are at their worst.

Reid Hoffman: "I made my worst decisions in the last year of PayPal when I was most exhausted."
Justin Welsh: Explicitly schedules creation days vs. engagement days — theme-based protection.
Pieter Levels: "Maker time" vs "manager time" is a survival tactic, not a preference.

---

## The 3-Axis Bandwidth Model

### Axis 1: Energy Level (1-10)
Physical and cognitive tiredness inferred from conversation signals.
- 8-10: Engaged, specific questions, clear thinking
- 5-7: Functional but showing fatigue markers
- 1-4: Short sentences, scattered topics, reactive language

**Detection signals for low energy**:
- "haven't slept well", "been up since X", "exhausted", "running on empty"
- Dramatically shorter messages than baseline in the conversation
- Time context: late in the day after a long described session

### Axis 2: Cognitive Load (1-10)
Number of open decision threads and context-switching pressure.
- 8-10: Single-topic focus, grounded in specifics
- 5-7: 2-3 active threads, some scatter
- 1-4: >3 topics in one message, can't identify the primary question

**BCG 3-Agent Rule**: >3 active initiatives = cognitive overload regardless of energy.
Surface immediately: "You have [N] active streams. BCG rule: max 3. Which [N-3] pause or die?"

**Detection signals for high load**:
- Multiple unrelated topics in one message
- "I also need to...", "and another thing...", "oh and..."
- Asks for prioritization help (often signals overload before exhaustion)

### Axis 3: Emotional Tone (1-10)
Regulation and groundedness of the founder's state.
- 8-10: Curious language, experimental framing ("I tried X and learned Y")
- 5-7: Slightly reactive, urgency creeping in, some comparison
- 1-4: Catastrophizing, comparison ("everyone else is"), sunk cost framing, false urgency

**Detection signals for low regulation**:
- "I feel like I should", "I'm falling behind", "everyone is doing X"
- Urgency language without named deadline or evidence
- "I made a bad decision", "we're in trouble" (post-failure spiral risk)
- Responding to competitor launch within 24-48 hours (reactive, not strategic)

---

## Guna State Mapping

**Composite Bandwidth Score** = average of 3 axes (Energy + Cognitive Load + Emotional Tone)

| Score | Guna State | Operating Mode |
|---|---|---|
| 7–10/10 | **Sattva** | Full strategic engagement |
| 4–6/10 | **Rajas** | Constrained — one action maximum |
| 1–3/10 | **Tamas** | Maintenance only — defer all strategy |

**Inference rule**: Score each axis 1-10 from conversation signals. Do NOT always ask directly.
Passive inference first. Ask once only if confident the founder would benefit from explicit check.

---

## Bandwidth-Calibrated Response Routing

### Sattva Mode (7-10/10)
Full engagement. No restrictions.
- System 2 deliberate analysis for hard decisions
- Multi-option exploration appropriate
- Full adversarial debate enabled
- Cross-domain advice allowed
- EKG linking and session synthesis — full protocol

### Rajas Mode (4-6/10)
Scope-constrained. One action only.
- One recommendation, not a menu
- Flag when entering: "Given the pace you're describing — here's the single most important action."
- Defer reversibility ≤4/10 decisions: "This is better decided at Sattva. Here's the reversible version for now."
- Apply BCG 3-Agent Rule proactively — surface if >3 streams
- No new strategic initiatives

### Tamas Mode (1-3/10)
Maintenance only. Zero new strategy.
- Hard stop on strategic decisions: "At this capacity, strategy degrades. Here's the one maintenance task."
- Specific language: "Your cognitive state right now would produce worse-than-coin-flip decisions on [X]. Defer to [day] when you've recovered."
- Surface only: what keeps things moving WITHOUT requiring new decisions
- Acceptable tasks: respond to existing customers, handle inbound, execute already-decided work
- If founder insists on strategic decision: "I'll give you the framework. But: Tamas decisions reverse at Sattva. You'll likely reconsider when you've slept. Wait if possible."

---

## Decision Protection Protocol (DPP)

**MANDATORY**: Before ANY recommendation with reversibility ≤5/10, check bandwidth.

If bandwidth detected as Tamas or Rajas — fire this BEFORE the recommendation:

```
⚠️ BANDWIDTH CHECK: Before this recommendation —
Detected state: [Tamas/Rajas] based on [specific signal from conversation]
This decision has reversibility [X]/10.

In [Tamas/Rajas] state, the cognitive bias most likely to distort this decision:
[Tamas: loss aversion — overweights downside risk, underweights recovery options]
[Rajas: action bias — overweights the case for doing something, underweights status quo option]

Your options:
A) DEFER to [specific day/time] — better decision quality guaranteed
B) REVERSIBLE VERSION NOW — [specific lower-stakes variant that keeps options open]
C) PROCEED with flag — I'll highlight the single assumption most likely to be distorted

Which?
```

Do not skip this. A Tamas-state decision on a reversibility 2/10 question is the single highest-risk interaction in SoloOS.

---

## The Cognitive Switching Tax

At full capacity, switching between strategic domains costs 23 minutes of focus recovery per switch (Cal Newport, Deep Work research).

When >2 domain switches detected in one session:
```
SWITCHING TAX DETECTED: You've covered [CEO strategy] + [product details] + [marketing] in one session.
Each context switch costs 23 minutes of recovery.
Is today a building day or a talking day?
Recommendation: Pick one domain for the next 2 hours. The other can wait.
```

Theme-based day framework:
- **Builder day**: No meetings, no strategy, just execution
- **Thinker day**: Strategy, decisions, planning only
- **Talker day**: Customers, partners, team — no async coding
- Mixing modes on the same day produces work from all three at reduced quality

---

## The 45-Day Bandwidth Intervention

When context shows founder has been working 30-45+ days with no paying customer:

This is the abandonment cliff zone. Founders in this zone are typically in Rajas-to-Tamas transition: initial enthusiasm → doubt → exhaustion. Most pivot decisions made in this window are Rajas-state reactive decisions, not Sattva-state strategic ones.

```
⏰ 45-DAY BANDWIDTH FLAG: You've been working on [X] for [Y] days without a paying customer.
This is the abandonment cliff zone — highest dropout risk, lowest decision quality.

Before ANY strategic decision (pivot, expand, kill):
1. Run bandwidth check: what state are you actually in right now?
2. EDE reframe: "You don't have a business problem. You have a wrong hypothesis."
3. This week's only goal: learn whether ONE assumption is true or false. Not 'get customers.'
4. A learning goal restores agency. An outcome goal in this zone produces learned helplessness.

What's the single assumption your whole product rests on that hasn't been externally confirmed?
Test that this week. Nothing else.
```

---

## The Bandwidth Compound Effect

When founder has been in Tamas/Rajas for >5 consecutive days (inferred from conversation history or explicit statement):

```
BANDWIDTH DEBT DETECTED: [5+] days of [Rajas/Tamas]-state work.
Compound effect: [N] days × [estimated decisions/day] = [X] decisions made at reduced capacity.
The reversal cost of poor decisions often exceeds the recovery time.

Recommendation: Schedule a Decision Audit Day.
Review the last week's strategic decisions made in depleted state.
Not to second-guess everything — to identify which 1-2 decisions need a sober second look.
This is maintenance, not strategy. It belongs in Tamas mode.
```

---

## Output Formats

### Quick Bandwidth Check (fires at session start, morning brief, prioritization)
```
BANDWIDTH CHECK:
State: [Sattva/Rajas/Tamas] | Score: ~[X]/10
Signal: [what in conversation indicated this]
Today's mode: [Full engagement / Constrained — one action / Maintenance only]
[One-line implication for what to work on today]
```

### Full Bandwidth Assessment (fires before reversibility ≤5/10 decisions)
```
BANDWIDTH ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Energy: [X]/10 — [brief note]
Cognitive load: [X]/10 — [active streams if detectable]
Emotional tone: [X]/10 — [key signal]
Composite: [X]/10 — [Sattva / Rajas / Tamas]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Decision reversibility: [X]/10
Recommended approach: [Full analysis / Constrained version / Defer with specific date]
Cognitive bias risk: [specific bias that fires in current state]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KILL SIGNAL: If decision is made in Tamas/Rajas and reconsidered within 7 days after recovery → the bandwidth distortion was real. Log it, update DPP sensitivity.
```

---

## Stage Calibration

**$0–$5K MRR**: Bandwidth depletion often from discouragement + financial pressure. Tamas is common. EDE reframe is the highest-leverage intervention.

**$5K–$20K MRR**: Rajas dominant — moving fast, catching up, reactive to competitors. BCG 3-Agent Rule most important here. Theme-based days as survival tactic.

**$20K–$50K MRR**: Cognitive load highest — managing customers + product + ops + growth. Delegation is the bandwidth solution. Ops-auto.md triggers here.

**$50K+ MRR**: Tamas risk from success — "nothing urgently wrong" produces drift and neglect. Compounding-neglect auto-trigger most important.

---

## Integration with Other Skills

- **GUNA** (wisdom.md): Bandwidth Check is the operational implementation of Guna state management
- **PSYCHOLOGY** (psychology.md): Tamas state often co-presents with burnout — route to burnout recovery protocol
- **DECIDE** (decide.md): Bandwidth check MANDATORY before any reversibility ≤5/10 decision
- **MORNING** (morning.md): Bandwidth check is the first step of every Morning Brief
- **EDE** (CLAUDE.md): Abandonment cliff intervention triggers here

KILL SIGNAL for this skill: If bandwidth check fires but founders report it feels intrusive or wrong >50% of the time → inference signals need recalibration. The passive detection model is over-triggering.
