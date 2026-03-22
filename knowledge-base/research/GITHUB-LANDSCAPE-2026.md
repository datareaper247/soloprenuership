# GitHub AI Founder / Personal OS Landscape — March 2026
## Intelligence Compiled for SoloOS v5 Direction

**Research Date**: March 22, 2026
**Method**: Parallel web search + Gemini Flash analysis + agentic council synthesis
**Purpose**: Map the competitive and adjacent landscape before defining SoloOS v5

---

## THE MEGA-TREND: Claude Code + CLAUDE.md = New Platform

Claude Code (released May 2025) overtook GitHub Copilot and Cursor within 8 months to become
the most-used AI coding tool in 2026. The CLAUDE.md pattern — instruction files that shape agent
behavior — became the dominant "personal OS" substrate, spawning an entire ecosystem of repos.

**Key stat**: Gartner reported a 1,445% surge in multi-agent system inquiries Q1 2024 → Q2 2025.

**Solo founder signal**: 36.3% of all new companies are solo-founded (2026), powered by AI tools
costing under $1,000/month. Maor Shlomo built Base44 alone → sold to Wix for $80M in 6 months.
Dario Amodei publicly stated first solo unicorn arrives in 2026.

---

## TIER 1: VIRAL BREAKOUTS (100K+ Stars)

### OpenClaw (openclaw/openclaw)
- **Stars**: 250K+ (March 2026) — surpassed React to become most-starred software project on GitHub
- **Virality**: 60,000 stars in 72 hours (Jan 2026). One of fastest star accumulations in GitHub history.
- **Creator**: Peter Steinberger (PSPDFKit founder)
- **What it is**: Personal AI assistant running on your own hardware. Answers on channels you already use.
- **Channels**: WhatsApp, Telegram, Slack, Discord, Signal, iMessage, BlueBubbles, IRC, Teams, Matrix, LINE, Mattermost, Nostr, Twitch, Zalo, WebChat + 5 more
- **Key feature**: True personal AI agent — runs locally, remembers context across conversations, can do things on your machine
- **NOT founder-specific**: General personal assistant, not business/founder strategy
- **Distribution**: Creator joined OpenAI Feb 14, 2026. Project moved to open-source foundation.
- **Why it won**: Messaging channel integration (where users already live), zero friction, "lobster" branding

### Superpowers (obra/superpowers)
- **Stars**: ~94-100K (March 2026), gaining ~2,000/day
- **Creator**: Jesse Vincent (obra) + Prime Radiant team
- **In Anthropic official marketplace**: Yes (January 2026)
- **What it is**: Agentic skills framework + software development methodology
- **Methodology**: Socratic brainstorming → detailed planning → TDD → parallel sub-agents → code review
- **Skills**: 20+ battle-tested skills (TDD, debugging, collaboration)
- **NOT founder-specific**: Pure software development workflow
- **Monthly star gain**: Highest of any trending repo in March 2026 (+37,809/month)

### everything-claude-code (affaan-m/everything-claude-code)
- **Stars**: 84K+ (March 2026)
- **Creator**: Affaan Mustafa (built at Anthropic x Cerebral Valley Hackathon Feb 2026, won $15K)
- **What it is**: Agent harness performance optimization system
- **Launched**: January 17, 2026 with 9 agents, 14 commands, 11 skills
- **Quality**: 1,282 tests, 98% coverage, 102 static analysis rules
- **Notable**: Cross-platform (Claude Code, Codex, Opencode, Cursor)
- **NOT founder-specific**: General agent harness for developers

---

## TIER 2: STRONG TRACTION (10K-100K Stars)

### gstack (garrytan/gstack)
- **Stars**: ~20K (March 2026), 2,200 forks — 10K in first 48 hours
- **Creator**: Garry Tan (Y Combinator President)
- **What it is**: Virtual engineering team roles via slash commands
- **Roles**: CEO, Designer, Eng Manager, Release Manager, Doc Engineer, QA Lead (18 specialists total)
- **Languages**: TypeScript (79.6%), Go (18.3%)
- **Productivity claim**: 10K LOC/day, 100 PRs/week over 50-day stretch
- **Setup**: `cp -Rf ~/.claude/skills/gstack .claude/skills/gstack`
- **TechCrunch coverage**: "Love and hate" — generated controversy AND viral adoption
- **NOT founder-specific**: Software factory for engineers. CEO role is a coding meta-role, not strategic advice.
- **Key insight**: The ROLE framing (CEO, Designer, QA) is highly viral and approachable

### Personal_AI_Infrastructure (danielmiessler/Personal_AI_Infrastructure)
- **Stars**: Unknown (active, well-documented)
- **Creator**: Daniel Miessler (security researcher, Unsupervised Learning newsletter)
- **What it is**: Agentic AI infrastructure for magnifying human capabilities
- **Philosophy**: Goal-based (NOT task-based) — most agentic systems are task-based; PAI is the opposite
- **Architecture**: 7 components — Memory System v7.0, Algorithm v0.2.23, Hook System, continuous learning
- **Key differentiator**: Continuously learns from every interaction; captures signals about outputs, changes, results, preferences
- **Built natively on Claude Code**
- **Versioning**: PAI v2.4 as of Jan 2026
- **Closest competitor in philosophy** to SoloOS's goal-based orientation

---

## TIER 3: DIRECT FOUNDER OS COMPETITORS

### kipi-system (assafkip/kipi-system) ⭐ PRIMARY COMPETITOR
- **Creator**: Assaf Kipnis (KTLYST Labs)
- **What it is**: Portable founder operating system for Claude Code
- **Tagline**: "The part of your brain that remembers everything, connects everything, and turns everything into the next action"
- **Architecture**: 25 agents across 9 phases → produces a single HTML file with copy-paste actions sorted by friction
- **Features**:
  - Interactive setup wizard (~20 min setup)
  - Morning briefings (/q-morning)
  - Conversation debriefs
  - Social engagement
  - Relationship tracking
  - Content pipeline
  - Lead sourcing
  - Investor pipeline management
  - AUDHD executive function mode
- **Technical stack**: Sub-agents, bash execution, hooks, MCP servers, CLAUDE.md, skills
- **Output format**: Single HTML file, every action pre-written, every follow-up drafted, every open thread tracked
- **Gaps vs SoloOS**: No kill signals, no stage calibration, no anti-sycophancy, no PMF framework, no pattern library, no assumption archaeology

### HAL-OS (thebrownproject/hal-os)
- **What it is**: Personal AI operating system for Claude Code
- **Memory**: Two-layer (daily session logs + curated long-term MEMORY.md that survives context resets)
- **Search**: hybrid — SQLite + sqlite-vec (vector similarity) + FTS5 (BM25 keyword)
- **Commands**: /boot, /shutdown, /status, /calendar, /second-brain, /networking, /work, /chat
- **Auto-memory hook**: Forces a persist pass after every response — nothing slips through
- **Second Brain**: Collaborative note capture (HAL asks questions, drafts notes before you confirm)
- **Work PA**: Configurable via system/storage/work/CLAUDE.md
- **Not founder-specific**: Personal OS (work, networking, note-taking)

### claude-os (knnymrls/claude-os)
- **What it is**: Personal OS built on Claude Code
- **Features**: Persistent memory across sessions, daily briefings, habit tracking, brain dumps
- **Key pattern**: /night routine tracks habits defined in memory/habits.md
- **Not founder-specific**: Life assistant focus

### carls-product-os (carlvellotti/carls-product-os)
- **What it is**: Personal operating system for Claude Code — how a PM organizes workspace
- **Not founder-specific**: Product manager focus

### CoWork-OS (CoWork-OS/CoWork-OS)
- **What it is**: OS for personal AI agents, security-first
- **Channels**: WhatsApp, Telegram, Discord, Slack, iMessage (multi-channel like OpenClaw)
- **Providers**: 30+ LLMs (Claude, GPT, Gemini, Ollama, more)
- **Skills**: 139 skills across documents, code review, web search, image generation, financial analysis, etc.
- **Architecture**: Kanban task board, real-time activity feed, agent heartbeat monitoring, standup reports, performance reviews
- **Security**: No data to CoWork servers, API keys stored locally encrypted
- **Not founder-specific**: General team/personal AI OS

### AI-company (CronusL-1141/AI-company)
- **What it is**: AI Team OS — Multi-Agent Team Operating System for Claude Code
- **Framing**: YOU are the Chairman. AI is the CEO. Set vision → system executes, learns, evolves autonomously.
- **Architecture**: 40+ MCP tools, 22 agent templates, task wall, meeting system, dashboard
- **R&D agents**: Autonomously scan competitor frameworks, organize brainstorming meetings
- **Not founder-specific**: Software company builder, not founder strategy advisor

---

## TIER 4: ADJACENT / ECOSYSTEM

### awesome-claude-code-toolkit (rohitg00/awesome-claude-code-toolkit)
- 135 agents, 35 curated skills (+400,000 via SkillKit), 42 commands, 150+ plugins, 19 hooks, 15 rules, 7 templates, 8 MCP configs
- The "everything in one place" aggregator approach

### awesome-agent-skills (VoltAgent/awesome-agent-skills)
- Claude Code Skills + 500+ agent skills, cross-platform (Codex, Antigravity, Gemini CLI, Cursor)

### awesome-claude-skills (travisvn/awesome-claude-skills)
- Curated list of Claude Skills, resources, tools

### claude-mem (thedotmack/claude-mem)
- Automatically captures everything Claude does during coding sessions
- Compresses with AI (Claude agent-sdk), injects relevant context into future sessions

### awesome-ai-agents-2026 (caramaschiHG/awesome-ai-agents-2026)
- 300+ resources, 20+ categories, updated monthly

---

## COMPETITIVE POSITIONING MATRIX

| Repo | Stars | Founder-Specific | Strategy Depth | Memory | Channels | Kill Signals | Stage Calibration |
|---|---|---|---|---|---|---|---|
| **SoloOS** (us) | <100 | ✅ HIGH | ✅ DEEP | ⚠️ Partial (FL-log) | ❌ | ✅ YES | ✅ YES |
| OpenClaw | 250K | ❌ | ❌ | ✅ | ✅ 20+ | ❌ | ❌ |
| Superpowers | ~100K | ❌ Dev only | ❌ | ❌ | ❌ | ❌ | ❌ |
| everything-CC | 84K | ❌ Dev only | ❌ | ⚠️ | ❌ | ❌ | ❌ |
| gstack | 20K | ❌ Eng only | ❌ | ❌ | ❌ | ❌ | ❌ |
| kipi-system | ? | ✅ MEDIUM | ⚠️ Tactical | ⚠️ | ❌ | ❌ | ❌ |
| PAI | ? | ❌ | ⚠️ Goal-based | ✅ | ❌ | ❌ | ❌ |
| HAL-OS | ? | ❌ Personal | ❌ | ✅ | ❌ | ❌ | ❌ |
| CoWork-OS | ? | ❌ | ❌ | ⚠️ | ✅ | ❌ | ❌ |
| AI-company | ? | ⚠️ Tech-founder | ⚠️ | ⚠️ | ❌ | ❌ | ❌ |

**SoloOS's moat is unique**: No other system has kill signals, stage calibration, anti-sycophancy protocol, assumption archaeology, or a founder intelligence pattern library.

**SoloOS's gaps**: Memory persistence, channels, setup wizard, virality/distribution.

---

## KEY VIRAL MECHANICS OBSERVED

### What made repos go viral in 2026:

1. **OpenClaw (250K)**: Messaging channel integration (where users live) + "runs on your machine" privacy + catchy branding + famous creator (PSPDFKit founder) + 72-hour launch sprint

2. **Superpowers (~100K)**: "Senior developer" narrative + TDD methodology + Anthropic marketplace + `obra` credibility + consistent build-in-public tweets

3. **everything-claude-code (84K)**: Hackathon win = press + rapid iteration (9→84K stars in 6 weeks) + cross-platform positioning + extreme quality (1,282 tests)

4. **gstack (20K)**: Famous founder (Garry Tan, YC president) + TechCrunch controversy = debate traffic + "600K lines in 60 days" productivity claim + easy installation

### Common viral ingredients:
- Celebrity/credibility signal (PSPDFKit founder, YC president, hackathon winner)
- Dramatic productivity claim (10K LOC/day, 250K stars)
- Easy setup (one command)
- Clear role/identity narrative ("your personal engineering team", "personal AI OS")
- Build-in-public documentation of the creator actually using it

---

## WHAT NOBODY HAS BUILT (SoloOS's True Differentiation)

These features exist nowhere in the ecosystem:

1. **Kill Signal System** — Every recommendation ends with a specific falsifiable prediction within 30 days
2. **Stage-Calibrated Advice Engine** — Advice changes fundamentally at $0 / $1-5K / $5-20K / $20-50K / $50K+ MRR
3. **Anti-Sycophancy Protocol** — Explicit rules to challenge, not validate, the founder's ideas
4. **Assumption Archaeology** — Cross-session tracking of ICP, stage, value prop drift
5. **Founder Intelligence Pattern Library** — 55 named patterns with real founder case evidence (P01-P55)
6. **Temporal Intelligence Layer** — Day 30/45 intervention, experiment timeline tracking
7. **EKG (Emergent Knowledge Graph)** — [[FL-XXX]] [[P-XX]] wiki-link syntax
8. **PMF Archetype Detection** — Hair on Fire / Hard Fact / Future Vision routing
9. **Kaala Timing Assessment** — Position strength × market window before aggressive actions
10. **Ancient Wisdom Routing** — Bhagavad Gita, Sun Tzu, Chanakya, Stoic for founder psychology

---

## SIGNALS FOR v5 DIRECTION

### From the landscape:
- Memory persistence is table stakes (everyone has it or is building it)
- Multi-agent parallel execution is now expected
- Channel integration (WhatsApp/Telegram) is the next frontier for personal AI
- The "Chairman/CEO" framing (founder stays strategic, AI operates) is resonating
- Skills ecosystem growing explosively — a "plugin marketplace" play could matter
- Virality requires: famous user + dramatic claim + easy setup + build-in-public

### From competitive gaps:
- kipi-system (closest competitor) is purely tactical — no strategic depth
- Nobody has founder economics intelligence (kill signals, stage calibration)
- Memory + strategy = untapped combination
- "Founder intelligence as MCP server" = genuinely novel infrastructure

### From the macro:
- Solo founder economics improving dramatically (Base44: $80M exit, 6 months, one person)
- The market is validating: people WANT founder-specific AI tools
- Distribution is the hard part — the tool must be viral-worthy, not just valuable

---

## REPOS TO MONITOR

| Repo | Why |
|---|---|
| assafkip/kipi-system | Direct competitor — watch for strategy depth additions |
| garrytan/gstack | Watch for pivot toward non-technical founder use |
| danielmiessler/Personal_AI_Infrastructure | Closest philosophy, cross-pollinate |
| openclaw/openclaw | Distribution model to emulate |
| obra/superpowers | Skills ecosystem growth |
| CronusL-1141/AI-company | Chairman/CEO framing evolution |
| CoWork-OS/CoWork-OS | Channel integration architecture |
| thedotmack/claude-mem | Memory architecture patterns |

---

*Research compiled: March 22, 2026*
*Next update: When SoloOS v5 ships — compare positioning*
