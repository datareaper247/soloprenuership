# Getting Started with SoloOS

SoloOS is markdown files. No install. No servers. Copy files, start using.

This guide gets you from zero to your first useful output in 10 minutes.

---

## Step 1: Clone and set up (2 minutes)

```bash
git clone https://github.com/datareaper247/soloprenuership.git ~/soloos

# Add behavioral rules to your project — this is the core unlock
cp ~/soloos/CLAUDE.md ./CLAUDE.md

# Install all skills as Claude Code commands
cp ~/soloos/skills/claude-code/*.md ~/.claude/commands/

# Create context directory
mkdir -p ./context
cp ~/soloos/context/*.md ./context/
```

## Step 2: Populate your business context (10 minutes)

Open Claude Code in your project directory and run:

```
/onboard
```

Claude will ask you 10 questions and write your context files automatically.
This is the step most people skip. Don't skip it — it's what makes everything else calibrated.

## Step 3: Run your first skill

```bash
# Daily brief
/morning

# Validate a product idea before building
/validate "your idea here"

# Research a competitor
/research competitor "CompetitorName"

# Decide something you've been putting off
/decide "the decision you keep avoiding"
```

---

## What You Have Now

After setup:

```
Your project/
├── CLAUDE.md              ← Every Claude session is now founder-aware
└── context/
    ├── business-context.md  ← Populated by /onboard
    ├── customer-voice.md    ← Populated by /onboard
    ├── experiment-log.md    ← Populated by /onboard
    └── decision-log.md      ← Populated by /onboard

~/.claude/commands/
├── morning.md     ← /morning
├── decide.md      ← /decide
├── validate.md    ← /validate
├── listen.md      ← /listen
├── launch.md      ← /launch
├── prospect.md    ← /prospect
├── onboard.md     ← /onboard
├── swarm.md       ← /swarm
├── research.md    ← /research
├── seo.md         ← /seo
├── sales.md       ← /sales
├── role.md        ← /role
└── ...
```

---

## The Daily Workflow

**Every morning (10 minutes)**:
```
/morning    → What matters today. One thing. One decision.
```

**Before building anything**:
```
/listen "[market]"     → 4 weeks of community intelligence (skip if you've done this)
/validate "[idea]"     → 4-gate validation before writing code
```

**When launching**:
```
/launch "[product]"    → All 7 launch assets in one command
```

**When stuck on a decision**:
```
/decide "[decision]"   → Adversarial debate, recommendation, kill signal
```

**When prospecting**:
```
/prospect "[company + role]"   → Research → pain → outreach → sequence
```

---

## The 10 Core Roles

For any business function, activate the specialist:

```
/role ceo      → Strategy, OKRs, investor narrative
/role cmo      → GTM, positioning, demand gen
/role cfo      → Unit economics, pricing math
/role sdr      → Cold outreach, ICP research
/role seo      → Keyword research, content briefs
/role pm       → PRDs, roadmap, prioritization
/role cs       → Customer retention, churn prevention
/role growth   → AARRR experiments, viral loops
```

---

## Real Examples

See `examples/` for complete input → output walkthroughs:

- `examples/validate-saas-idea.md` — catching a fatal flaw before building
- `examples/decide-pricing.md` — adversarial debate on free tier
- `examples/morning-brief.md` — a real morning brief at $4K MRR
- `examples/launch-hacker-news.md` — full launch asset generation
- `examples/claude-md-before-after.md` — the CLAUDE.md difference

---

## Keeping Context Up to Date

**Weekly (5 minutes)**:
```
/onboard --metrics    → Update MRR and key numbers
/onboard --voice      → Add any customer quotes from the week
```

**After every decision**:
Update `context/decision-log.md` manually, or tell Claude:
"Add this decision to my decision log: [decision]"

---

## What Doesn't Work Yet

Honest limitations:
- **No MCP servers** — the integrations listed in some older docs don't exist yet
- **No parallel agents** — `/swarm` runs sequential role-switching, not true parallel
- **No Python package** — no `from soloos.roles import CMORole`

Everything that works, works today with stock Claude Code and these markdown files.
