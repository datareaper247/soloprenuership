# SoloOS v5 — Strategic Direction Document
## Research Council Synthesis — March 22, 2026

> **Council composition**: Research agents covering GitHub landscape (2× parallel), HN/Reddit signals,
> Gemini Flash competitive analysis, internal SoloOS audit. Synthesized by Claude Sonnet 4.6.

---

## EXECUTIVE SUMMARY

The Claude Code ecosystem has exploded. In 90 days (Jan-Mar 2026):
- Superpowers: 0 → ~100K stars
- everything-claude-code: 0 → 84K stars
- gstack: 0 → 20K stars
- kipi-system: launched as direct SoloOS competitor

**SoloOS's position**: Deeper strategic intelligence than any competitor. Zero distribution.
The gap between value and visibility is the entire v5 problem to solve.

**v5 Thesis**: Transform SoloOS from a brilliant private system into the definitive
open-source operating system for solo founders — with the same viral potential as OpenClaw,
the strategic depth of a seasoned advisor, and the memory of a chief of staff.

---

## CURRENT STATE AUDIT (v4 Capabilities)

### What SoloOS Has That Nobody Else Does
- Kill signal system (falsifiable recommendations, measurable, time-bounded)
- Stage-calibrated advice ($0 / $1-5K / $5-20K / $20-50K / $50K+ MRR)
- Anti-sycophancy protocol (challenge before affirm)
- Assumption archaeology (cross-session ICP/stage/value-prop drift detection)
- Founder intelligence pattern library (P01-P55, real case evidence)
- Temporal intelligence layer (Day 30/45 intervention, abandonment cliff detection)
- EKG (Emergent Knowledge Graph) wiki-link syntax: [[FL-XXX]] [[P-XX]]
- PMF archetype detection (Hair on Fire / Hard Fact / Future Vision)
- Kaala timing assessment (position strength × market window)
- Ancient wisdom routing (Bhagavad Gita, Sun Tzu, Chanakya, Stoic)
- 10 auto-trigger domains (VALIDATE, MORNING, DECIDE, LAUNCH, GROWTH, FINANCE, INTEL, PMF, EXIT, OPS, + 10 more)
- 55 named patterns across 5 knowledge-base files
- 3 customer-facing skill files (positioning, negotiation, customer-success)
- BSHR reasoning loop (Buffer → Search → Hypothesize → Refine)
- Dual-process routing (System 1 pattern match / System 2 adversarial)

### SoloOS's Current Gaps (vs. Ecosystem)
1. **No persistent memory layer** — FL-log exists but no auto-capture, no cross-session recall
2. **No proactive OS behavior** — purely reactive (responds, doesn't initiate)
3. **No channel integration** — WhatsApp/Telegram (OpenClaw has 20+ channels)
4. **No setup wizard** — kipi-system onboards in 20 min with interactive wizard
5. **No viral README or demo** — zero distribution machinery
6. **No install command** — friction kills adoption
7. **Knowledge base not queryable as infrastructure** — FOUNDER_INTELLIGENCE.md is static markdown
8. **No multi-agent swarm** — strategic questions answered by single agent, not a council
9. **No live market monitoring** — MCPs available but not wired to proactive alerts

---

## THE COMPETITIVE LANDSCAPE (Summary)

### Direct Competitors to Watch
| System | Differentiator | Our Counter |
|---|---|---|
| kipi-system | Morning workflow, AUDHD mode, investor pipeline, 25 agents | Deeper strategy, kill signals, stage calibration |
| PAI (danielmiessler) | Goal-based (not task-based), continuous learning | Founder-specific + our pattern library |
| AI-company | Chairman/CEO framing, self-driving company | Bring this framing to non-technical founders |

### Who's Winning Distribution
| Repo | Stars | Why |
|---|---|---|
| OpenClaw | 250K | Channels + famous creator + "runs locally" privacy angle |
| Superpowers | ~100K | TDD narrative + Anthropic marketplace + build-in-public |
| everything-CC | 84K | Hackathon win → press + extreme quality |
| gstack | 20K | YC president + productivity claim + TechCrunch controversy |

**Pattern**: Stars = credibility signal × productivity claim × easy setup.

---

## v5 ARCHITECTURE — WHAT TO BUILD

### The v5 Framework: Five Pillars

```
SoloOS v5 = v4 intelligence
           + MEMORY OS (persistent cross-session)
           + SWARM COUNCIL (multi-agent strategic decisions)
           + PROACTIVE LAYER (morning brief, experiment pings, kill signal checks)
           + MCP INTELLIGENCE SERVER (knowledge base as queryable infrastructure)
           + DISTRIBUTION ENGINE (viral README, one-command install, demo video)
```

---

### PILLAR 1: MEMORY OS
**What**: Cross-session persistent memory that auto-captures decisions, experiments, customer insights.

**Why now**: HAL-OS and PAI have proven this works. Without it, SoloOS restarts every session. The FL-log (founder-log.md) is the seed — needs auto-population.

**Implementation spec**:

```
memory/
├── founder-log.md        # FL-XXX entries (already exists, needs auto-capture hook)
├── decisions.md          # D-XXX entries — strategic decisions
├── experiments.md        # E-XXX entries — running experiments + outcomes
├── customers.md          # CU-XXX entries — customer quotes, insights
├── assumptions.md        # Current ICP, stage, value prop (auto-updated)
└── weekly-pulse.md       # Auto-generated weekly summary (Sunday night hook)
```

**Hook architecture**:
- `PostToolUse` hook: When any context/ file is updated, check for new FL candidates
- `Stop` hook: Session synthesis trigger (currently documented, needs automation)
- `SessionStart` hook: Kill signal check + assumption drift detection

**Memory protocol**: After every session with a decision/experiment/insight, auto-append to founder-log.md using the FL-XXX format. No manual intervention.

**The "memory.py" pattern** (from HAL-OS): SQLite + vector similarity + BM25 keyword search
→ v5.1 feature, not v5.0. v5.0 uses plain markdown + grep.

**KPI**: Zero sessions where a kill signal due date passes unnoticed.

---

### PILLAR 2: SWARM COUNCIL (Multi-Agent Strategic Decisions)

**What**: When reversibility ≤ 5/10 decision detected, spin up 4 agents in parallel, synthesize.

**Why now**: gstack proved the "virtual team" framing is viral and valuable. kipi-system runs 25 agents. Single-agent advice has bias. Founders need a council, not an oracle.

**Council composition**:
```
/council [question]
→ Spawns 4 parallel sub-agents:
  1. CEO Advocate    — makes the strongest case FOR the action
  2. Devil's Advocate — makes the strongest case AGAINST
  3. CFO Lens        — unit economics and runway implications
  4. Customer Voice  — "what does your best customer actually need?"
→ Each returns: Position + Evidence + Kill Signal
→ Master agent synthesizes: Consensus or Dissent + Recommendation
```

**Auto-trigger**: Fires when `reversibility ≤ 5/10` detected in any decision question.
**Slash command**: `/council [question]` for explicit invocation.

**Output format**:
```
COUNCIL VERDICT: [Proceed / Hold / Modified approach]
CONSENSUS: [X/4 agents agree]
KEY DISSENT: [What the devil's advocate said that matters most]
RECOMMENDATION: [1 sentence]
KILL SIGNAL: [measurable within 30 days]
```

**v5.0 scope**: 4-agent council for major decisions. v5.1: persistent council with named advisors.

---

### PILLAR 3: PROACTIVE LAYER (OS Behavior, Not Just Chat Behavior)

**What**: SoloOS initiates — doesn't just respond. Daily brief, experiment pings, kill signal alerts.

**Why now**: kipi-system's morning brief (/q-morning) is its most-used feature. PAI's continuous learning loop. claude-os's habit tracking. Proactivity = the OS experience vs. the chatbot experience.

**Components**:

#### 3a. Morning Brief (already in AUTO_TRIGGERS, needs formalization)
```
/morning →
  1. Kill Signal Check (any overdue experiments from founder-log.md)
  2. Active Experiment Status (days running, signal received?)
  3. Today's Highest-Leverage Action (one specific thing, based on stage)
  4. Open Decision Queue (any reversibility ≤5/10 decisions pending)
  5. Bandwidth Check (1-10 scale → calibrate day)
```
**Format**: 5 bullet points max. Total output < 200 words. Starts the day, doesn't delay it.

#### 3b. Experiment Ping (via hook or manual)
```
/ping-experiments →
  For each active experiment in experiments.md:
    - Days running
    - Target signal
    - Current status (received? partial? none?)
    - Intervention level (📊 normal / ⚠️ flag / 🚨 intervention)
```

#### 3c. Session Synthesis (already exists, needs auto-trigger)
```
After any session with: decision + experiment + pivot + insight
→ Auto-append to founder-log.md
→ Ask: "One sentence — what's the most important thing we decided today?"
→ Log outcome with [[FL-XXX]] + kill signal + due date
```

#### 3d. Weekly Pulse (Sunday night / Monday morning)
```
/weekly-pulse →
  1. Experiments started this week: [list]
  2. Kill signals due this week: [list]
  3. Decisions made this week: [list]
  4. Stage update: [any change?]
  5. Next week's single most important experiment
```

---

### PILLAR 4: FOUNDER INTELLIGENCE MCP SERVER

**What**: Package FOUNDER_INTELLIGENCE.md + PATTERN_LIBRARY.md + MARKET_INTELLIGENCE.md
as a local MCP server with semantic search + structured queries.

**Why this is genuinely novel**: Nobody has done this. Every other system is reactive.
SoloOS v5 would be the first "founder intelligence database" queryable as infrastructure.

**What it enables**:
```
# Instead of:
Claude reads 5,000-line FOUNDER_INTELLIGENCE.md and pattern-matches in context

# With MCP server:
mcp__soloos-core__search_founder_cases query: "what happens when founders build before validation"
→ Returns: P-09 (Kahl Rule), FL-042 (specific founder who lost 6 months), 3 relevant kill signals

mcp__soloos-core__match_pattern stage: "$5K MRR" situation: "considering hiring"
→ Returns: HIRE GATE protocol, P-18 (Operator Archetype), stage calibration for $5K

mcp__soloos-core__get_kill_signals decision_type: "hiring" stage: "$5K MRR"
→ Returns: specific measurable kill signals for this exact scenario
```

**Already exists**: `mcp__soloos-core` MCP is live. Tools: calculate_ev, calculate_runway,
calculate_unit_economics, calculate_valuation, check_kill_signals_tool, check_market,
score_pmf, validate_idea_gates, search_founder_cases, match_pattern, get_stage_advice.

**v5.0 task**: Wire existing MCP tools into CLAUDE.md auto-triggers.
When VALIDATE fires → call `validate_idea_gates`. When FINANCE fires → call `calculate_ev`.
When PMF fires → call `score_pmf`. Stop pattern-matching in-context, query the MCP.

---

### PILLAR 5: DISTRIBUTION ENGINE

**What**: Make SoloOS installable, demonstrable, and shareable in < 5 minutes.

**Why this is the entire game**: Superpowers at 100K stars has less strategic depth than SoloOS.
The tool that REACHES founders wins, not the tool that's best.

#### 5a. Install Command
```bash
# One-command install:
curl -sL https://raw.githubusercontent.com/[username]/soloOS/main/install.sh | bash

# Or via Claude plugin:
/plugin install soloOS
```

**Install flow**:
1. Copy CLAUDE.md + skills/ to target project
2. Initialize context/ directory with templates
3. Run onboarding wizard (see 5c)
4. Print "SoloOS installed. Run /morning to start."

#### 5b. Viral README Structure
```markdown
# SoloOS — The Cognitive Operating System for Solo Founders

> One person, doing what traditionally requires 10-50 people.
> **Every recommendation ends with a kill signal.**

## What happens when you install SoloOS

[GIF: morning brief running in Claude Code]

In 60 seconds, Claude:
- Checks your overdue experiments
- Tells you the single highest-leverage action for today
- Detects if you're about to make a Stage Mismatch error

## The 3 things no other AI advisor does

1. **Kill signals**: Every recommendation ends with "here's exactly what would prove me wrong within 30 days"
2. **Stage calibration**: Advice for $0 MRR is completely different from $20K MRR. We detect your stage automatically.
3. **Anti-sycophancy**: We challenge your ideas before agreeing with them. Your co-founder should too.

## Used by founders at [stage badges]
```

#### 5c. Onboarding Wizard (/onboard — 20 minutes)

```
Phase 1 — Context (5 min):
  "What are you building? (product in 1 sentence)"
  "What's your current MRR? (0 is fine)"
  "Who is your ideal customer? (describe one person)"
  "What's your biggest uncertainty right now?"

Phase 2 — History (5 min):
  "Any experiments already running? (what are you testing?)"
  "Any decisions made in the last 30 days that felt hard?"
  "What have you tried that hasn't worked?"

Phase 3 — Configuration (5 min):
  "Preferred interaction style? [Direct / Exploratory / Challenge-me]"
  "How often do you want proactive pings? [Daily / Weekly / Never]"
  "What does success look like in 90 days?"

Phase 4 — First Kill Signal (5 min):
  → Surfaces founder's biggest assumption
  → Proposes a 30-day experiment to test it
  → Writes it to founder-log.md as FL-001
  → "You now have your first kill signal. This is how SoloOS works."

Output: Populated context/business-context.md, context/experiment-log.md, FL-001
```

#### 5d. Demo Video
- 3-minute screen recording showing:
  1. `/morning` — kill signal check fires, experiment status surfaced (30s)
  2. Founder asks "should I pivot?" — Stage detected, DECIDE triggers, council runs (90s)
  3. Anti-sycophancy fires on a bad idea — founder pushes back, system holds position (60s)

#### 5e. Build-in-Public Strategy
- Creator (you) uses SoloOS publicly for own startup decisions
- Tweet: "I asked my AI advisor if I should raise. It said no, and named exactly what would change its mind."
- Thread: "The 3 anti-patterns that kill solo founders in month 3. My AI caught me doing #2."
- HN Show HN: "SoloOS — An AI operating system for solo founders that challenges your ideas instead of validating them"
- Hook: The anti-sycophancy angle is counternarrative in a world of AI sycophancy. That's the press story.

---

## v5 ROADMAP

### v5.0 — Core (Target: 4 weeks)
- [ ] **Memory OS**: Auto-capture hooks wired to founder-log.md
- [ ] **Morning Brief** (/morning command, formalized protocol)
- [ ] **Onboarding Wizard** (/onboard, 20-min setup → populates context/)
- [ ] **MCP Wire-up**: CLAUDE.md auto-triggers → mcp__soloos-core__ tool calls
- [ ] **Install script**: one command → SoloOS in any project
- [ ] **Viral README**: The counternarrative pitch (anti-sycophancy, kill signals, stage calibration)
- [ ] **Demo GIF/video**: 3 minutes, the 3 core moments

### v5.1 — Swarm Intelligence (Target: 6 weeks post-v5.0)
- [ ] **Council (/council command)**: 4-agent parallel strategic advice
- [ ] **Weekly Pulse**: Auto-generated weekly synthesis
- [ ] **Memory search**: grep-based search across all context/ files
- [ ] **Experiment tracker**: experiments.md with auto-ping on day 30/45

### v5.2 — Distribution + Ecosystem (Target: 6 weeks post-v5.1)
- [ ] **Claude plugin packaging**: official Anthropic marketplace submission
- [ ] **WhatsApp/Telegram integration**: morning brief on mobile (via CoWork-OS architecture inspiration)
- [ ] **Community layer**: GitHub Discussions for pattern contributions
- [ ] **Pattern contribution protocol**: how external founders add FL entries

---

## v5 POSITIONING

### The One-Liner
"The AI advisor that tells you when you're wrong — not when you want to hear you're right."

### The Counternarrative (the actual press hook)
Every AI assistant validates. SoloOS challenges.
In a world where AI sycophancy kills startups, SoloOS is the co-founder who pushes back.

### Target Repo Name for GitHub
`soloOS` or `soloos` — lowercase, intentional.
Tagline: *"Claude Code as your co-founder. One with a spine."*

### What We Win On
- **Depth vs. breadth**: kipi-system covers more surface. SoloOS goes deeper on what actually kills companies.
- **Intelligence vs. task management**: AI-company automates. SoloOS thinks.
- **Anti-sycophancy vs. validation**: Every other system tells you what you want to hear. We don't.

### What We Intentionally Don't Compete On
- Channel integration (WhatsApp/Telegram) — defer to v5.2
- Software engineering roles — gstack owns this, we don't need it
- General personal assistant — OpenClaw owns this

---

## RISKS AND KILL SIGNALS

| Bet | Risk | Kill Signal (30 days) |
|---|---|---|
| Anti-sycophancy as viral hook | Founders want validation, reject challenge | <5% of README visitors click install after reading anti-sycophancy pitch |
| Depth > features | kipi-system adds kill signals first | kipi-system ships kill signal feature within 60 days of our launch |
| Stage calibration as differentiator | Founders don't self-identify by MRR | <20% of onboarded users complete the MRR question in setup wizard |
| Open source distribution | Creator using it publicly generates attention | <100 GitHub stars in 30 days post-launch |

---

## FIRST ACTION (Start Here)

**The v5.0 launch sequence**:

1. **Today**: Write the viral README (Pillar 5b). This forces clarity on positioning.
2. **This week**: Build /onboard wizard (Pillar 5c). This forces clarity on onboarding.
3. **Week 2**: Wire MCP auto-triggers (Pillar 4). Makes every auto-trigger call real data.
4. **Week 3**: Memory OS hooks (Pillar 1). Makes FL-log auto-populate.
5. **Week 4**: Install script + demo video. Distribution machinery.
6. **Launch**: HN Show HN + tweet thread + build-in-public announcement.

The README goes first. If the README doesn't convince you the positioning is right,
nothing else matters.

---

## APPENDIX: THE COUNCIL'S DISSENT

*What the Devil's Advocate would say about this direction:*

> "The ecosystem is moving fast. Superpowers hit 100K stars in 3 months. By the time SoloOS launches,
> kipi-system will have added strategy features, gstack will have pivoted to founders, and two new
> repos will have copied our positioning. Distribution speed matters more than depth.
> Forget the MCP server and swarm council — ship the README, install script, and demo video in ONE WEEK,
> then grow from community feedback. The council is telling you to build. The right answer is to ship."

*Counter-counter*: The Devil's Advocate is right about timing. Wrong about what to ship. The README
IS shipping. The demo IS shipping. Week 1 is all distribution. The technical pillars are weeks 2-4.
The anti-sycophancy bet is: if you have nothing worth distributing, distribution doesn't matter.
The 4 weeks build something genuinely different. Then we distribute hard.

**KILL SIGNAL on this entire v5 direction**: If the viral README (anti-sycophancy angle) doesn't
generate >100 GitHub stars within 30 days of launch, the positioning is wrong. Pivot to the
"morning brief" hook (kipi-system's most viral feature) and relaunch within 2 weeks.

---

*Document synthesized by research council on March 22, 2026*
*Next review: At v5.0 launch — compare actual vs. predicted reception*
