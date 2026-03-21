# SoloOS v3: The Cognitive OS for Solo Founders

> *A goal-oriented reasoning engine that connects your decisions, actions, and outcomes into an emergent knowledge graph — turning your daily work into a personal playbook.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills: 17](https://img.shields.io/badge/Auto--Trigger%20Skills-17-purple.svg)](#skills)
[![Roles: 10](https://img.shields.io/badge/Core%20Roles-10-blue.svg)](#roles)
[![Works with: Claude Code](https://img.shields.io/badge/Works%20with-Claude%20Code-orange.svg)](#quick-start)
[![Cross-platform](https://img.shields.io/badge/Also%20works-Claude.ai%20%7C%20API%20%7C%20Any%20LLM-green.svg)](integrations/claude-ai-system-prompt.md)

---

## What SoloOS v3 Actually Does

**v1**: Required slash commands. You had to know `/validate` existed.
**v2**: Auto-triggers. Claude detects intent and fires the right framework.
**v3**: Learns from you. Every decision logged. Goals drive every answer. Knowledge compounds.

---

## What SoloOS v2 Actually Does

SoloOS is a **prompt framework** — markdown files that transform Claude into a founder-aware co-pilot.

**v1** required you to remember slash commands. `/validate`, `/decide`, `/morning` — you had to know the command existed and type it.

**v2** removes that entirely. Claude detects what you need and applies the right framework automatically.

```
You: "I'm thinking about building an AI resume tool for nurses"

Claude: ⚠️ VALIDATE FIRST: Did 3+ nurses describe this pain in their own words?
Reading this as $0 MRR — pre-revenue stage. Continuing...

4-gate validation:
Gate 1 — Problem clarity: "Nurses struggling with resume formatting" vs "nurses can't get callbacks" — which?
Gate 2 — Market signal check: [checks MARKET_INTELLIGENCE.md] AI resume tools are Heavily Saturated.
  Viable with niche focus: nursing-specific certifications, ATS formatting for hospital HR systems.
Gate 3 — 5 Tier-4+ commitments needed before building. Here's the exact DM to send...
Gate 4 — Unit economics: at $29 one-time, 92% gross margin. Compliance angle available?

KILL SIGNAL: If you can't get 5 nurses to say "charge my card" in 4 weeks from 100 direct DMs → wrong ICP or wrong problem.
```

No command typed. That's v2.

---

## What's Genuinely New in v2

| Feature | v1 | v2 |
|---|---|---|
| Framework activation | Slash command required | **Auto-detects from conversation** |
| Stage awareness | Founder must declare MRR | **Inferred from conversation clues** |
| Role switching | `/role cmo` command | **Automatic from topic** |
| Anti-pattern flags | Fires on explicit triggers | **Fires on implicit signals** |
| Kill signals | Optional | **Mandatory on every recommendation** |
| Reversibility scoring | Not included | **Every significant decision scored** |
| Assumption tracking | Not included | **Contradictions flagged across session** |
| Market claims | Generic | **Referenced from real founder data** |
| Knowledge base | Patterns + playbooks only | **+ FOUNDER_INTELLIGENCE + MARKET_INTELLIGENCE** |

---

## Quick Start (2 minutes)

```bash
# 1. Clone SoloOS
git clone https://github.com/datareaper247/soloprenuership.git ~/soloos

# 2. Add the cognitive OS to your project
cp ~/soloos/CLAUDE.md ./CLAUDE.md

# 3. Install skills as Claude Code commands (optional — auto-triggers work without this)
cp ~/soloos/skills/claude-code/*.md ~/.claude/commands/

# 4. Set up context memory
mkdir -p ./context
cp ~/soloos/context/*.md ./context/
# /onboard will fill these in through a 10-question conversation

# 5. Open Claude Code. Start talking. No commands needed.
```

From session 1, Claude auto-detects your stage and applies the right framework.

---

## The Auto-Trigger System

17 skills. All fire without slash commands. Mapped in `skills/AUTO_TRIGGERS.md`.

| When you say... | What fires automatically |
|---|---|
| "thinking about building X" | 4-gate validation + Kahl Rule |
| "good morning" / "what to focus on" | Morning brief: pulse → action → decision |
| "should I X or Y" / "I can't decide" | Adversarial decision: Rec → Why → Risks → Reversibility → Kill Signal |
| "about to launch" / "going live" | Marc Lou Rule + 7-asset launch generation |
| "how do I grow" / "stuck at $X MRR" | Retention check first, then acquisition |
| "SEO strategy" / "blog posts" | Stage gate: $0-5K → "Not yet, here's why" |
| "[competitor] launched" | 5-layer competitor autopsy |
| "new customer session" + no context | 10-question onboarding flow |
| "should I hire" | Reversibility score (3/10) + process-first flag |
| Pricing question | Marc Lou price ladder + conversion benchmarks |

**Slash commands still work** as power-user shortcuts for explicit invocation.

---

## The Knowledge Base (New in v2)

Real founder data encoded as reference intelligence. Claude consults these before making market claims.

### `knowledge-base/FOUNDER_INTELLIGENCE.md`
300+ founder journeys distilled to:
- **7 Master Patterns** with evidence citations (Pieter Levels, Marc Lou, Arvid Kahl, Tony Dinh, Danny Postma...)
- **Stage-specific decision trees** ($0 / $1-5K / $5-20K / $20-50K / $50K+ MRR)
- **6 Founder Archetypes** with exact strategies, real numbers, and "best for / not for"
- **Kill Signal Database** — specific data that proves each decision type wrong within 30 days
- **Assumption Debt Patterns** — the 4 most common conflicting assumptions founders hold
- **Honest failure data**: 45-50% of AI products launched 2023-2024 generated $0 MRR

### `knowledge-base/MARKET_INTELLIGENCE.md`
- **Category Saturation Map**: Dead / Saturated / Viable-with-niche / Open / Emerging
- **Unit economics database**: Gross margins, LTV:CAC, churn rates by category
- **Pricing conversion benchmarks**: Real conversion rates at each price point
- **AI API cost structure**: $/request for every major model
- **Moat strength matrix**: How long each moat type takes to build, clone resistance rating

### `knowledge-base/PATTERN_LIBRARY.md`
38 decision patterns from real founders:
- P01 The Levels Test → P07 The Narrow ICP Rule → P14 The Paid Acquisition Gate → P35 The 40% Test...
- Each has: situation → pattern → real example → kill signal → reversibility score

---

## The 17 Skills

All auto-trigger. All still available as slash commands for explicit use.

### Pre-Build Intelligence
| Skill | Auto-fires when | Framework |
|---|---|---|
| `validate` | "thinking about building X" | 4-gate paid validation — Kahl + Tringas |
| `listen` | "what do customers want" / "community research" | Arvid Kahl community intelligence pipeline |
| `research` | Market/competitor/ICP questions | 5-layer autopsy, bottom-up sizing, Signal Classifier |
| `onboard` | New session with no context | 10-question flow → writes all 4 context files |

### Daily Operations
| Skill | Auto-fires when | Framework |
|---|---|---|
| `morning` | "good morning" / "prioritize today" | Chief of Staff daily brief |
| `decide` | "should I X or Y" / "I can't decide" | Adversarial 3-voice: Operator / Devil's Advocate / Expert |
| `prospect` | "cold outreach to [X]" / "find leads at [Y]" | Research → trigger events → 3 outreach variants → 6-touch sequence |

### Launch + Growth
| Skill | Auto-fires when | Framework |
|---|---|---|
| `launch` | "about to launch" / "going live" | Marc Lou build-in-public: 7 assets before shipping |
| `growth` | "stuck at $X MRR" / "how do I grow" | Retention check → acquisition calibrated to stage |
| `seo` | SEO/content/keywords question | Stage-gated: $0-5K (no), $5-20K (bottom-funnel), $20K+ (full funnel) |
| `sales` | Pipeline/outreach/demos | ACV-gated: <$100 (self-serve), $100-500 (email), $500+ (calls) |
| `content` | "I need to write X" / "what to post" | Stage-matched content + distribution ladder |

### Specialist Tools
| Skill | Auto-fires when | Framework |
|---|---|---|
| `swarm` | "multiple perspectives" / "challenge my thinking" | Sequential role analysis with explicit handoffs |
| `ops` | "document this process" / "SOP for X" | Document → automate → delegate |
| `geo` | International expansion questions | Stage gate ($50K+ only) + market entry framework |

---

## Auto-Triggers: The New Behaviors

Beyond skills, CLAUDE.md v2 adds 4 behaviors that fire on every strategic conversation:

### 1. Stage Inference
Claude reads conversation for stage signals. "You're asking about hiring → Reading this as $20K+ MRR."
Stated in one line. Never blocks the answer.

### 2. Reversibility Scoring
Every significant decision gets: `Reversibility: 3/10 — Hard to reverse. Need 3 data points before committing.`
Hiring = 3/10. Cold email test = 9/10. Different analysis warranted for each.

### 3. Kill Signal (Mandatory)
Every strategic recommendation ends with: `KILL SIGNAL: [specific data that proves this wrong in 30 days]`
No exceptions. Unmeasurable recommendations get refined until they have one.

### 4. Assumption Debt Tracking
When "ICP = SMBs" in session 1 conflicts with "our best customer is an enterprise" in session 4:
`⚠️ ASSUMPTION CONFLICT: Earlier you said X, now implying Y. Which is true?`

---

## The 10 Core Roles

Auto-activate by topic. No `/role` command needed.

| Role | Auto-activates on | Full command |
|---|---|---|
| **CEO** | Strategy, OKRs, investors, pivots | `/role ceo` |
| **CMO** | Marketing, GTM, channels, brand | `/role cmo` |
| **SDR** | Cold outreach, ICP research, pipeline | `/role sdr` |
| **Account Executive** | Discovery, demos, close | `/role ae` |
| **SEO Specialist** | Keyword research, content briefs, audit | `/role seo` |
| **Content Marketer** | Long-form SEO, newsletters, case studies | `/role content` |
| **Product Manager** | PRDs, prioritization, user stories | `/role pm` |
| **Customer Success** | Onboarding, retention, churn prevention | `/role cs` |
| **Growth Hacker** | AARRR experiments, viral loops, PLG | `/role growth` |
| **CFO** | Unit economics, pricing math, financial modeling | `/role cfo` |

---

## Context Memory System

Four files. Fill once. Every skill gets dramatically more accurate.

```
context/
├── business-context.md   # MRR, ICP, competition, OKRs, open decisions
├── customer-voice.md     # Exact customer quotes — the words that convert
├── experiment-log.md     # What you tried, what worked, what didn't
└── decision-log.md       # Strategic decisions, rationale, kill signals
```

Run `/onboard` to populate all four through a 10-question conversation.

**Compounding effect**: Claude detects conflicts between what context says and what you're describing today. Keeps your model of your own business honest.

---

## Real Examples

Complete input → output walkthroughs:

- [`examples/validate-saas-idea.md`](examples/validate-saas-idea.md) — validate catching a fatal flaw before writing code
- [`examples/launch-hacker-news.md`](examples/launch-hacker-news.md) — launch generating Show HN + full tweet thread + 50 DMs
- [`examples/decide-pricing.md`](examples/decide-pricing.md) — decide running adversarial debate on "free tier?"
- [`examples/morning-brief.md`](examples/morning-brief.md) — morning output for a $4K MRR B2B SaaS founder
- [`examples/claude-md-before-after.md`](examples/claude-md-before-after.md) — same question, with and without CLAUDE.md

---

## Project Structure

```
soloprenuership/
├── CLAUDE.md                      ← THE COGNITIVE OS. Drop in any project.
├── context/                       ← Fill once. Compounds forever.
│   ├── business-context.md
│   ├── customer-voice.md
│   ├── experiment-log.md
│   └── decision-log.md
├── skills/
│   ├── AUTO_TRIGGERS.md           ← Master routing table (how skills auto-fire)
│   └── claude-code/               ← 17 skill files (auto-trigger + slash command)
│       ├── validate.md
│       ├── morning.md
│       ├── decide.md
│       └── ... (14 more)
├── agents/roles/                  ← 10 core + 34 extended role system prompts
├── knowledge-base/
│   ├── FOUNDER_INTELLIGENCE.md    ← 300+ founder journeys → decision patterns
│   ├── MARKET_INTELLIGENCE.md     ← Category maps, unit economics, pricing benchmarks
│   ├── PATTERN_LIBRARY.md         ← 38 decision patterns with kill signals
│   └── patterns/
│       └── SOLO_FOUNDER_PLAYBOOKS.md
├── docs/
│   ├── GETTING_STARTED.md
│   └── CONTRIBUTING.md
└── examples/                      ← Real input → output walkthroughs
```

---

## Why This vs. Generic Prompts

A generic "act as a startup advisor" prompt gives you advice for one message.

SoloOS CLAUDE.md gives you a co-pilot that:
- **Knows your stage** without being told (infers from what you're asking)
- **Remembers your experiments** (context files prevent recommending what already failed)
- **Grounds advice in real data** (FOUNDER_INTELLIGENCE.md: "Danny Postma did X at $300K MRR peak")
- **Forces kill signals** before you waste weeks on wrong assumptions
- **Flags stage mismatches** ("you're asking about paid ads but you're $0 MRR — here's why that's wrong")
- **Scores reversibility** so you know when to go fast vs. when to go careful

Generic prompts give you a thinking partner. SoloOS gives you a co-founder who's seen 300 similar situations.

---

## What's New in v3

Three architectural breakthroughs. All zero-infrastructure. All built on top of v2.

### 1. Personal Pattern Accrual
Every decision you make gets logged to `knowledge-base/personal/founder-log.md` via **Session Synthesis** — an auto-trigger that fires at the end of sessions containing key decisions, experiments, or pivots. After 6 months, Claude reasons from 200+ of your own decisions with outcomes, not just generic founder data.

### 2. Emergent Knowledge Graph (EKG)
`[[type:id]]` wiki-link syntax across all context files creates a traversable knowledge graph with zero infrastructure. `[[D-017]]` links to `[[E-004]]` links to `[[P-06]]`. Your company's entire decision history becomes traversable. Claude follows the links to reason about causality, not just current state.

### 3. Goal-Oriented Backwards Induction
`context/mission.md` is the new strategic root. Declare your exit goal once. Claude derives the backwards induction model — what must be true at 60%, 30%, and 10% of your timeline — and evaluates every strategic question against that model. You stop optimizing for the wrong things at the wrong stage.

**New auto-triggers**:
- **KILL SIGNAL CHECK**: At session start, Claude checks `founder-log.md` for overdue outcome reviews and surfaces them before anything else.
- **MISSION CHECK**: Every strategic answer evaluated against your declared critical path milestone.
- **SESSION SYNTHESIS**: At session end, key decisions auto-logged with hypothesis + kill signal.

Everything that works, works today with stock Claude Code.

---

## What's Still Planned (Not Built Yet)

Honest roadmap:

- **MCP servers** connecting to real APIs (Reddit research, HN monitoring, competitor intelligence)
- **Python package** for CrewAI / LangGraph integration
- **True parallel swarm execution** via Claude sub-agent API
- **Auto-context updates** from integrated business tools (Stripe, PostHog, etc.)

---

## Contributing

See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

Highest-value contributions:
- New examples with real input/output from your actual founder use
- Sharper role system prompts (closer to how a senior hire actually thinks)
- Additional patterns for PATTERN_LIBRARY.md with real kill signals
- Auto-trigger rules for edge cases not covered in AUTO_TRIGGERS.md

---

## License

MIT — use commercially, modify freely.
