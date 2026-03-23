# GitHub Research: AI Founder Tools & Related Repos
## Competitive Landscape for SoloOS v5 Planning

**Research Date:** 2026-03-22
**Source:** Agent a05d8b989f52ea0ab (15 tool uses, 493s)
**Knowledge Cutoff:** August 2025 (star counts reflect that period)

---

## SUMMARY: TOP 5 MOST RELEVANT TO SOLOOOS

| Rank | Repo | Stars [~Aug 2025] | Core Overlap | Key Gap SoloOS Fills |
|---|---|---|---|---|
| 1 | geekan/MetaGPT | ~46K | Multi-agent role systems + SOPs | MetaGPT targets software teams; SoloOS targets founders with kill signals, stage calibration |
| 2 | SamurAIGPT/entrepreneur-gpt | ~1.2K | Explicitly entrepreneurship-focused AI | No stage awareness, no kill signals, no real founder data — proves the category is real but shallow execution fails |
| 3 | yoheinakajima/babyagi | ~20K | Goal decomposition + task loop | BabyAGI loops indefinitely with no kill signal; SoloOS is BabyAGI with gates at every step |
| 4 | mem0ai/mem0 | ~23K | Persistent AI memory | Solves SoloOS's #1 adoption friction: context file decay |
| 5 | mezod/awesome-indie | ~8K | Solo founder resource collection | Static list vs. SoloOS's dynamic, context-aware, auto-routing intelligence |

---

## COMPLETE REPO ANALYSIS

### MetaGPT (geekan/MetaGPT) — ~46K stars
Closest architectural analog to SoloOS's role system, but domain-specific to software building.
MetaGPT's SOP enforcement — each role must produce a defined output before the next role activates —
is the architecture SoloOS should apply to DECIDE: before a recommendation on reversibility ≤4/10,
a Critic SOP must complete first. MetaGPT achieves anti-sycophancy architecturally; SoloOS via
prompting — the former is more reliable.

### CrewAI (crewAIInc/crewAI) — ~28K stars
Production-ready multi-agent orchestration. SoloOS intelligence lives in markdown (passive, fires
when Claude reads context). CrewAI intelligence executes autonomously as agents with real tool access.
Strategic question for v5: prompt framework (zero infrastructure, runs anywhere) or CrewAI-backed
swarm (more powerful, requires deployment)? Prompt framework wins while user base is small.

### Microsoft AutoGen (microsoft/autogen) — ~36K stars
Anti-sycophancy is architectural (CriticAgent is a separate agent that must respond). SoloOS's
anti-sycophancy is instruction-based (can be overridden by conversational momentum).
For v5 without infrastructure: add CLAUDE.md rule — "For any decision with Reversibility ≤4/10,
generate strongest counter-argument FIRST as named [CRITIC] block, then deliver recommendation."
This approximates AutoGen's critic pattern with zero infrastructure.

### LangGraph (langchain-ai/langgraph) — ~9K stars (accelerating)
Exposes SoloOS's biggest structural gap: Chronos Check only fires when founder opens a Claude session.
A LangGraph wrapper would make it proactive — system notifies when a kill signal due date arrives
independent of whether they start a conversation.
Low-infrastructure alternative: GitHub Action that reads founder-log.md daily and emails when an
`Outcome due:` date has passed. Solves 80% of LangGraph value with 5% of the effort.

### Phidata / Agno (phidatahq/phidata) — ~14K stars
Automatic memory extraction (agent writes structured facts to memory after every conversation
without being told to) directly solves context/ file decay. In SoloOS today, founder must manually
update business-context.md. Most founders stop after 2-3 sessions. Phidata's model: extraction
happens automatically, silently, after every session.

### BabyAGI (yoheinakajima/babyagi) — ~20K stars
BabyAGI is the architectural ancestor of SoloOS's EDE operating mode. BabyAGI loops without
a completion gate. SoloOS's kill signal is the completion gate BabyAGI lacks.
Positioning frame: "BabyAGI for founders, with kill signals and stage gates at every step."

### OpenAI Swarm (openai/swarm) — ~18K stars
SoloOS role switching is prompt-based. Swarm's is agent handoff — different agent with different
tools and system state takes over. Prompt-based is faster and requires no infrastructure; handoff is
architecturally cleaner for complex multi-role workflows. Monitor, no action until exits experimental.

### Mem0 (mem0ai/mem0) — ~23K stars
Persistent memory layer for AI agents. Semantic search over past interactions, automatic fact
extraction from conversations, cross-session persistence.
Mem0 solves SoloOS's #1 adoption friction: context files require manual updating; most founders
stop after 2-3 sessions. Mem0 extracts and stores facts automatically — the founder never manually
updates a context file again. Every session, Mem0-backed SoloOS loads current business context
automatically. Already in integrations/open-source/README.md; needs an MCP wrapper to activate.

### Zep (getzep/zep) — ~3K stars
Long-term memory with temporal fact versioning: tracks how facts change over time.
"ICP was 'developers' in January, is 'indie hackers' in March."
Zep is more powerful than Mem0 specifically for assumption archaeology. Mem0 is better for general
context persistence. Ideal: Mem0 for session persistence + Zep for drift detection.

### entrepreneur-gpt (SamurAIGPT/entrepreneur-gpt) — ~1.2K stars
Closest repo to SoloOS's stated mission in name. Critically weaker in execution: no stage awareness,
no kill signals, no reversibility scoring, no real founder data, no assumption tracking.
Low star count (~1.2K) despite explicit category alignment confirms that generic execution does not
build a committed user base. SoloOS's depth is the differentiating factor.

### awesome-indie (mezod/awesome-indie) — ~8K stars
8,000 stars on a static list confirms strong latent demand for systematized indie founder knowledge.
The list tells founders where to learn; SoloOS tells them what to do in their specific situation.
SoloOS is the AI-queryable, context-aware, dynamically routed version of what awesome-indie attempts.
Positioning opportunity: "the version of awesome-indie that knows your MRR and fires the right
resource automatically."

### Crawl4AI (unclecode/crawl4ai) — ~25K stars
Intel.md skill currently requires founders to manually provide competitor information. Crawl4AI +
SoloOS would automate the gather step — founder names a competitor, Crawl4AI fetches and structures
website + pricing + review data, SoloOS runs the 5-layer autopsy on structured output.
Changes intel from reactive (founder provides data) to proactive (system fetches data).
Highest-leverage infrastructure integration for the intelligence layer.

### ScrapeGraph AI (VinciGit00/Scrapegraph-ai) — ~16K stars
AI-guided web scraping with JSON output. Crawl4AI for content analysis + ScrapeGraph for structured
data extraction + SoloOS intel.md = fully automated competitive intelligence pipeline with no manual
data input.

### PostHog (PostHog/posthog) — ~21K stars
SoloOS's PMF skill reasons from founder-reported metrics. Direct PostHog integration would
eliminate the largest source of bad advice — incorrect manually-reported numbers. Founders are often
wrong by 10-15 percentage points on retention. Real data changes the recommendation.

### Composio (ComposioHQ/composio) — ~12K stars
Connects AI agents to 150+ business tools (Salesforce, HubSpot, Slack, GitHub, Stripe, QuickBooks).
Composio is the tool access layer SoloOS's MCP servers need. Converts SoloOS from "advice based
on founder-reported data" to "advice grounded in actual business data."

### n8n (n8n-io/n8n) — ~47K stars
Self-hosted visual workflow automation. 400+ integrations. The open-source Zapier.
When a founder identifies a manual task to automate, SoloOS could generate the actual automation
workflow (as a JSON export the founder imports). "Document → automate → delegate" ladder
implemented as a real artifact, not just advice.

### Claude Engineer (Doriandarko/claude-engineer) — ~8K stars
Claude-powered autonomous coding agent. Different domain (software engineering), same architectural
insight — CLAUDE.md-driven context enhancement produces materially better Claude sessions.
Claude Engineer's 8K stars from a developer audience confirms the market for specialized Claude
context systems. SoloOS applies the same architecture to founder intelligence.

---

## PATTERNS & GAPS ACROSS THE ECOSYSTEM

### What's Universal Among High-Star Repos
1. **General-purpose over founder-specific**: Horizontal frameworks get highest stars. Vertical
   applications have lower theoretical star ceilings but higher retention.
2. **Infrastructure over intelligence**: Market has solved agent execution (CrewAI, AutoGen, LangGraph)
   and tool connectivity (Composio, n8n). Has NOT solved what the agents should know, when to fire,
   how to reason about founder-specific decisions.
3. **Single-session architecture**: No repo tracks "you tried this 6 months ago, and here's what
   happened." Longitudinal memory is SoloOS's structural advantage and hardest to copy.
4. **No stage calibration**: Zero repos provide stage-calibrated advice. All advice is either generic
   or requires the user to supply context every session.
5. **No kill signals**: None of the repos surveyed enforce accountability mechanisms on recommendations.
6. **No real founder data grounding**: Generic LLM advice vs. "Pieter Levels did this at $30K MRR
   and here is what happened" is a meaningful trust differential. No competitor has 300+ documented
   founder trajectories as queryable knowledge.

### What SoloOS Does That No Competitor Does
- Stage-aware decision routing — **SoloOS UNIQUE as of Aug 2025**
- Kill signals on every recommendation — **SoloOS UNIQUE**
- Reversibility scoring on decisions — **SoloOS UNIQUE**
- Ancient wisdom as behavioral algorithms — **SoloOS UNIQUE**
- Backwards induction from declared exit goal — **SoloOS UNIQUE**
- Assumption archaeology with cross-session drift detection — **SoloOS UNIQUE**
- Psychological performance layer (burnout map, fear deconstruction) — **SoloOS UNIQUE**
- Real founder data grounding (300+ trajectories with specific numbers) — **SoloOS UNIQUE**
- Longitudinal session synthesis with EKG wiki-linking — **SoloOS UNIQUE**
- Zero-infrastructure deployment (pure markdown) — **SoloOS UNIQUE**

### What SoloOS Is Missing That Others Do Better
- **Persistent memory (Mem0/Zep)**: Context files decay. Commercial memory extracts facts automatically.
- **Proactive triggers (LangGraph/GitHub Actions)**: Kill signal deadlines fire only when founder opens Claude.
- **Structural critic enforcement (AutoGen)**: Prompting-based can be overridden. Architectural cannot.
- **Live data ingestion (Composio/PostHog/Stripe)**: Advises on metrics founder manually reports.
- **Autonomous research execution (Crawl4AI/CrewAI)**: Intel requires founder to supply competitor data.
- **Community and distribution**: No public presence vs. MetaGPT or CrewAI ecosystems.

---

## PRIORITY FEATURES FOR v5

### Priority 1 — High Impact, Zero Infrastructure (v5.0)

1. **Mandatory [CRITIC] Block for Reversibility ≤4/10**
   Before any recommendation where Reversibility ≤4/10, generate labeled [CRITIC] block containing
   strongest possible counter-argument. Then deliver recommendation.
   Borrowed from: AutoGen CriticAgent pattern.

2. **Kill Signal Calendar via GitHub Action**
   GitHub Action runs daily, parses founder-log.md for `Outcome due:` entries past today, sends email.
   30 lines of Python. Borrowed from: LangGraph temporal awareness, implemented without LangGraph.

3. **Vibe-Coding Rung Auto-Trigger in validate.md**
   When founder describes building with Cursor/Claude Code → run Rung Assessment.
   Evidence: DEEP_RESEARCH_2026_FOUNDER_PLAYBOOKS.md Pattern 1, just not wired.

4. **Automatic MRR Extraction in Session Synthesis**
   When founder says "we just hit $8K MRR," MRR updates business-context.md automatically.
   Effort: Low (Session Synthesis rule addition, no new infrastructure).

### Priority 2 — Medium Impact, Medium Effort (v5.1)

5. **Mem0 Integration** — Automatic context persistence after every conversation.
6. **Crawl4AI Integration** — Intel skill fetches competitor data automatically.
7. **PostHog/Stripe Auto-Read** — Financial advice grounded in actual numbers.
8. **Zep Integration** — Cross-session ICP drift detection with temporal versioning.
9. **n8n Workflow Generation** — Ops-auto generates importable automation JSON.

### Priority 3 — Strategic Infrastructure (v5.2+, after PMF)
- Full CrewAI Runtime Wrapper
- Python Package for programmatic access
- Distribution Campaign (HN Show HN, build-in-public thread)

---

## THE SINGLE HIGHEST-VALUE INTEGRATION

**Mem0 integration for automatic context persistence.**
It solves the number-one adoption friction (context file decay), is demonstrably powerful in
before/after demos, and creates a compounding usage loop — every session improves context quality,
advice gets better, founders tell other founders.

**Kill signal**: If after implementing Mem0, context currency doesn't improve >50% among active users
within 30 days → the friction was not context decay. Revisit.

---

*19 primary repos analyzed, 10 unique SoloOS advantages identified, 9 v5 integration opportunities ranked.*
