# SoloOS: The Operating System for Solo Founders

> *Give Claude persistent business intelligence, professional-grade role cognition, and
> validated founder playbooks — all through markdown files that work today.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills: 16](https://img.shields.io/badge/Skills-16-purple.svg)](#claude-code-skills)
[![Roles: 10](https://img.shields.io/badge/Core%20Roles-10-blue.svg)](#role-library)
[![Works with: Claude Code](https://img.shields.io/badge/Works%20with-Claude%20Code-orange.svg)](#quick-start)

---

## What SoloOS Actually Is

SoloOS is a **prompt framework** — markdown files you drop into your project that transform
Claude from a generic AI assistant into a founder-aware business copilot.

No install. No servers. No API keys. Copy files, start using.

**What it gives you**:
1. **CLAUDE.md** — behavioral rules that make every Claude session founder-aware
2. **15 skills** — slash commands encoding validated founder frameworks (validation gate, launch sequence, community listening, etc.)
3. **10 core roles** — deep system prompts for the roles solo founders actually use
4. **Context templates** — persistent business memory that compounds across sessions
5. **Validated playbooks** — 5 proven founder patterns encoded as AI behaviors

**What it does NOT include (yet)**:
- MCP servers (planned, not built)
- Python packages
- Parallel multi-agent orchestration

Everything that works, works today with stock Claude Code and the files in this repo.

---

## The Core Unlock: CLAUDE.md

Drop `CLAUDE.md` into any project directory. Every Claude session in that directory becomes founder-aware.

```bash
cp ~/soloos/CLAUDE.md ./CLAUDE.md
```

From that point forward, without any prompting from you, Claude will:

- Apply 80/20 thinking to every recommendation — surfaces the top 20% that drives 80% of value
- Flag founder anti-patterns as they appear — building before validation, scaling before PMF, optimizing at <$10K MRR
- Frame every decision with: recommendation + key assumption + kill signal + reversibility
- Apply the BCG 3-Agent cognitive rule — max 3 active decision streams, prevents collapse
- Auto-trigger the right founder playbook based on stage (Kahl pre-idea, Levels MVP, Tringas post-PMF)

**Before CLAUDE.md**: "Here's a marketing strategy..."
**After CLAUDE.md**: "⚠️ VALIDATE FIRST — you haven't confirmed 5 people will pay for this.
Before any marketing, here are the 3 cheapest experiments to confirm demand."

See [examples/claude-md-before-after.md](examples/claude-md-before-after.md) for a full side-by-side.

---

## Quick Start (2 minutes)

```bash
# 1. Clone SoloOS
git clone https://github.com/datareaper247/soloprenuership.git ~/soloos

# 2. Add behavioral rules to your project
cp ~/soloos/CLAUDE.md ./CLAUDE.md

# 3. Install skills as Claude Code commands
cp ~/soloos/skills/claude-code/*.md ~/.claude/commands/

# 4. Set up context memory
mkdir -p ./context
cp ~/soloos/context/*.md ./context/
# Fill in context/business-context.md — 10 minutes, compounds forever

# 5. Run the onboarding skill to auto-populate context
/onboard
```

That's it. Open Claude Code and start using the skills.

---

## The 16 Skills

Drop-in commands for Claude Code. Encoding validated founder frameworks, not generic prompts.

### The Pre-Build Loop (do these in order before writing code)

| Skill | What It Does | Framework Source |
|-------|-------------|-----------------|
| `/listen "[market]"` | Community intelligence — maps pain signals, classifies build vs. content vs. validate | Arvid Kahl's Embedded Entrepreneur |
| `/validate "[idea]"` | 4-gate validation: problem → market signal → 5 paid commitments → unit economics | Kahl + Tringas paid validation gate |
| `/onboard` | 10-question flow that auto-populates all context templates | Original |

### The Daily Driver Loop

| Skill | What It Does | Framework Source |
|-------|-------------|-----------------|
| `/morning` | 15-min brief: revenue pulse + today's one thing + one decision cleared | Original |
| `/decide "[decision]"` | Adversarial 3-voice debate: Operator vs. Devil's Advocate vs. Market Expert | BCG decision quality research |
| `/prospect "[company + role]"` | Research → trigger events → pain hypothesis → 3 outreach variants → 6-touch sequence | SDR playbook synthesis |

### The Launch Loop

| Skill | What It Does | Framework Source |
|-------|-------------|-----------------|
| `/launch "[product]"` | Generates 7 launch assets: HN post + tweet thread + PH + LinkedIn + email + 50 DMs + Reddit | Marc Lou build-in-public pattern |
| `/swarm [type] "[task]"` | Sequential multi-role analysis: each role's output feeds the next | Original |

### The Specialist Toolkit

| Skill | What It Does |
|-------|-------------|
| `/role [name]` | Activate any of the 10 core role system prompts |
| `/research [type] "[topic]"` | Market sizing, competitor analysis, customer pain mining |
| `/content [type] "[topic]"` | Blog posts, email sequences, social content with SEO intent |
| `/seo [command]` | Keyword research, content briefs, technical audit checklist |
| `/sales [command]` | Cold outreach, deal qualification, proposal frameworks |
| `/ops [command]` | SOP creation, financial modeling, legal review templates |
| `/growth [command]` | Experiment design, funnel analysis, retention frameworks |

---

## Real Examples

See `examples/` for complete input → output walkthroughs:

- [`examples/validate-saas-idea.md`](examples/validate-saas-idea.md) — `/validate` catching a fatal flaw in a SaaS idea before a line of code was written
- [`examples/launch-hacker-news.md`](examples/launch-hacker-news.md) — `/launch` generating a Show HN post + full thread + 50 DMs
- [`examples/decide-pricing.md`](examples/decide-pricing.md) — `/decide` running the adversarial debate on "should I add a free tier?"
- [`examples/morning-brief.md`](examples/morning-brief.md) — `/morning` output for a $4K MRR B2B SaaS founder
- [`examples/claude-md-before-after.md`](examples/claude-md-before-after.md) — same question, with and without CLAUDE.md

---

## The 10 Core Roles

Roles a solo founder actually uses. Deep system prompts with identity, frameworks, tools, and escalation logic.

| Role | When to Use | Activates With |
|------|------------|---------------|
| **CEO** | Strategy, OKRs, investor narrative, pivot decisions | `/role ceo` |
| **CMO** | GTM strategy, positioning canvas, demand gen | `/role cmo` |
| **SDR** | Cold outreach, ICP research, pipeline building | `/role sdr` |
| **Account Executive** | Discovery, demos, close strategies | `/role ae` |
| **SEO Specialist** | Keyword research, content briefs, technical audit | `/role seo` |
| **Content Marketer** | Long-form SEO, case studies, newsletters | `/role content` |
| **Product Manager** | PRDs, prioritization, user stories, metrics | `/role pm` |
| **Customer Success** | Onboarding, retention, churn prevention | `/role cs` |
| **Growth Hacker** | AARRR experiments, viral loops, PLG | `/role growth` |
| **CFO** | Unit economics, pricing math, financial modeling | `/role cfo` |

> All 44 roles from the original role library are available in `agents/roles/` — the 10 above
> are the ones with the deepest prompts and highest solo-founder utility.

---

## Context Memory System

Four files. Fill them once. Every SoloOS skill gets dramatically better.

```
context/
├── business-context.md   # MRR, ICP, competition, current OKRs, open decisions
├── customer-voice.md     # Exact customer quotes — the words that convert
├── experiment-log.md     # What you tried, what worked, what didn't
└── decision-log.md       # Strategic decisions, rationale, kill signals
```

**The compound effect**:
```
Week 1:  Claude advises based on your context
Month 3: Claude cross-references experiments when you propose new ones
Month 6: Claude spots patterns in your decision log you've missed
Year 1:  More institutional memory than any hire you made in the last quarter
```

Run `/onboard` to populate all four files through a 10-minute conversation instead of staring at blank templates.

---

## Validated Founder Playbooks

Five documented founder patterns encoded as automatic Claude behaviors.
See [`knowledge-base/patterns/SOLO_FOUNDER_PLAYBOOKS.md`](knowledge-base/patterns/SOLO_FOUNDER_PLAYBOOKS.md).

| Playbook | Pattern | Auto-Triggers When |
|----------|---------|-------------------|
| **Kahl** | Audience before product | Founder proposes an idea without community validation |
| **Marc Lou** | Every launch is content | Founder is about to build without launch assets |
| **Levels** | Constraints as advantage | Scope creep detected, MVP growing beyond 2-week ship |
| **Jackson** | Stair-step to SaaS | Founder jumps straight to SaaS for first product |
| **Tringas** | Narrow focus wins | Founder tries to serve multiple ICPs before PMF |

These patterns are wired into `CLAUDE.md` — they activate automatically, not only when you invoke them.

---

## The /swarm Command (What It Actually Does)

`/swarm` runs sequential role-switching analysis — each role's perspective feeds the next.
It does **not** run parallel agents (that requires infrastructure not yet built).

What it actually produces in a single Claude session:

```bash
/swarm product-launch "Rankly — daily SEO rank tracker with Slack alerts"

Phase 1: CMO analyzes positioning and GTM motion
Phase 2: SEO Specialist identifies keyword opportunities from Phase 1
Phase 3: SDR builds ICP profile and outreach angle from Phase 1+2
Phase 4: Content Marketer writes launch blog intro from all above
Synthesis: CEO-level brief with top 5 actions, owners, timelines
```

Each role has access to the prior role's output. The synthesis is the deliverable.
Total session: 45-90 minutes. Review time: 15 minutes.

Available swarm types: `product-launch`, `weekly-ops`, `growth-sprint`, `fundraise`, `customer-crisis`, `market-research`

---

## Project Structure

```
soloprenuership/
├── CLAUDE.md                 ← THE BEHAVIORAL UNLOCK. Drop this in any project.
├── context/                  ← Fill once. Compounds forever.
│   ├── business-context.md
│   ├── customer-voice.md
│   ├── experiment-log.md
│   └── decision-log.md
├── skills/claude-code/       ← 15 slash commands for Claude Code
│   ├── morning.md            ← Daily brief
│   ├── decide.md             ← Adversarial decision framework
│   ├── validate.md           ← Paid validation gate
│   ├── listen.md             ← Community intelligence pipeline
│   ├── launch.md             ← Build-in-public launch sequence
│   ├── prospect.md           ← Full outreach chain
│   ├── onboard.md            ← Context setup flow
│   ├── swarm.md              ← Sequential multi-role analysis
│   └── ...
├── agents/roles/             ← 44 role system prompts (10 core, 34 extended)
├── knowledge-base/
│   └── patterns/
│       ├── AI_ERA_PATTERNS.md        ← Research-validated AI behavior patterns
│       └── SOLO_FOUNDER_PLAYBOOKS.md ← 5 founder playbooks as AI behaviors
└── examples/                 ← Real input → output walkthroughs
```

---

## What's Planned (Not Built Yet)

Honest roadmap. None of this exists today:

- **MCP Servers** — `soloos-research`, `soloos-marketing` etc. connecting to real APIs
- **Python package** — `from soloos.roles import CMORole` for CrewAI / LangGraph
- **Parallel swarm execution** — true multi-agent orchestration via Claude's sub-agent API
- **Auto-context population** — automatic business-context.md updates from integrated tools

If you want to contribute any of these, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Why Not Just Use ChatGPT or Generic Prompts?

The difference is **behavioral programming vs. one-off prompting**.

A generic "act as a CMO" prompt gets you a CMO for one message.

SoloOS CLAUDE.md + `/role cmo` gets you a CMO that:
- Knows your current MRR and growth rate (from context files)
- Has already read your last 3 experiments and won't recommend what already failed
- Applies April Dunford's positioning canvas without you asking
- Flags when your GTM motion is wrong for your ACV before building a plan around it
- Refuses to recommend brand investment before PMF (built into the behavioral rules)

The depth compounds. Generic prompts don't.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

Highest-value contributions:
- Sharper role system prompts (the closer to how a senior hire actually thinks, the better)
- New examples with real input/output
- `/onboard` improvements — reducing friction to context setup
- MCP server implementations (if you build one, it goes here)

---

## License

MIT — use commercially, modify freely.

---

*For the founder who refuses to hire when AI can staff the company — but only if it actually works.*
