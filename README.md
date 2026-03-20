# SoloOS: Universal Agent Company OS

> *Multiplex a single founder into a 50-person virtual company using agentic AI swarms.*
> *Drop into any agent CLI. Unlock professional-grade outputs in every business function.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Roles: 45](https://img.shields.io/badge/Roles-45-blue.svg)](#role-library)
[![MCP Servers: 10](https://img.shields.io/badge/MCP%20Servers-10-green.svg)](#mcp-servers)
[![Skills: 15](https://img.shields.io/badge/Skills-15-purple.svg)](#claude-code-skills)

---

## What Is SoloOS?

SoloOS is an open-source framework that gives any AI agent a complete professional company workforce.

**Without SoloOS**: Generic AI responses about marketing, sales, SEO.
**With SoloOS**: A CMO writes your GTM strategy. An SEO specialist delivers keyword research with volume/difficulty data. A CFO models your unit economics. An SDR writes personalized cold outreach sequences.

The gap is enormous. SoloOS achieves this through three layers:

```
┌────────────────────────────────────────────────────────────────────┐
│  LAYER 3: SWARM ORCHESTRATION                                      │
│  Multi-agent parallel execution. Product launch in 4 hours.        │
│  Weekly ops swarm runs autonomously every Monday 8am.              │
├────────────────────────────────────────────────────────────────────┤
│  LAYER 2: MCP TOOL SERVERS                                         │
│  10 MCP servers — real tool access for every business function.    │
│  Connects to 150+ tools via Composio (Salesforce, HubSpot, etc.)  │
├────────────────────────────────────────────────────────────────────┤
│  LAYER 1: ROLE LIBRARY (FREE)                                      │
│  44 professional role system prompts. Zero setup required.         │
│  Works with Claude Code, Cursor, Aider, AutoGen, CrewAI.           │
└────────────────────────────────────────────────────────────────────┘
```

---

## The Behavioral Unlock

This is what makes SoloOS different from a collection of prompts.

Drop `CLAUDE.md` into your project and every Claude session becomes founder-aware:
- 80/20 lens applied automatically to every recommendation
- Founder anti-patterns flagged (building before validation, optimizing too early)
- Decision framework: every recommendation includes assumption + kill signal + reversibility
- BCG 3-Agent Rule: max 3 decision streams, synthesis over completeness
- Context memory system: business DNA persists and compounds across sessions

**The daily driver loop**:
```
/morning          → 15-min brief: pulse + one thing + decision cleared
/decide           → Adversarial 3-voice debate on any pending decision
/prospect         → Research → pain hypothesis → 3 outreach variants → 6-touch sequence
/swarm weekly-ops → Monday brief across all business functions
```

**The pre-build validation loop**:
```
/listen "[market]"  → 4 weeks of community intelligence (Arvid Kahl pattern)
/validate "[idea]"  → 4 gates: problem → market signal → 5 commitments → unit economics
/launch "[product]" → All launch assets generated: HN + Twitter + PH + LinkedIn + DMs
```

**The compound memory effect**:
```
Week 1:  Claude gives advice based on your context
Month 3: Claude references past experiments when recommending new ones
Month 6: Claude spots patterns in your decision log you haven't noticed
Year 1:  Better context than any employee who joined last quarter
```

---

## Quick Start (60 seconds)

### Option A: Claude Code Skills (Recommended)
```bash
# Clone SoloOS
git clone https://github.com/datareaper247/soloprenuership.git ~/soloos

# Install as Claude Code commands
cp ~/soloos/skills/claude-code/*.md ~/.claude/commands/

# Add behavioral rules to your project (THE KEY STEP)
cp ~/soloos/CLAUDE.md ./CLAUDE.md

# Set up context memory system
mkdir -p ./context
cp ~/soloos/context/*.md ./context/
# Fill in context/business-context.md — takes 10 minutes, pays back forever

# Use immediately
/role seo-specialist
/swarm product-launch "Launch our DevOps tool next Tuesday"
/research competitor "FoodLogiQ"
```

### Option B: Any Agent via MCP
```bash
# Add MCP servers
claude mcp add soloos-swarm -- npx -y @soloos/mcp-swarm@latest
claude mcp add soloos-marketing -- npx -y @soloos/mcp-marketing@latest
claude mcp add soloos-research -- npx -y @soloos/mcp-research@latest

# Use in any conversation
"Use soloos-swarm to invoke the SEO specialist and research keywords for pharmacy audit software"
```

### Option C: CrewAI / AutoGen / LangGraph
```python
from soloos.roles import CMORole, SEORole, SDRRole
from crewai import Agent, Crew

cmo = Agent(role=CMORole.system_prompt, tools=CMORole.tools)
seo = Agent(role=SEORole.system_prompt, tools=SEORole.tools)
crew = Crew(agents=[cmo, seo], tasks=[launch_task])
crew.kickoff()
```

---

## Role Library (44 Roles)

Every role a real company needs, as AI agent system prompts.

### Leadership (5)
| Role | What They Do |
|------|-------------|
| CEO | Vision, strategy, fundraising, board management |
| CTO | Architecture, build vs buy, engineering culture |
| CMO | GTM strategy, positioning, demand generation |
| CFO | Unit economics, financial modeling, investor reporting |
| COO | Operations, process design, OKR tracking |

### Engineering (8)
| Role | What They Do |
|------|-------------|
| Frontend Engineer | React/Next.js, TypeScript, performance, a11y |
| Backend Engineer | APIs, databases, microservices, security |
| DevOps Engineer | CI/CD, Kubernetes, IaC, monitoring |
| Mobile Engineer | iOS/Android, React Native, Flutter |
| ML/AI Engineer | Model training, inference, MLOps |
| Security Engineer | Pen testing, SAST/DAST, compliance |
| QA Engineer | Test strategy, automation, quality gates |
| Data Engineer | Pipelines, warehouses, ETL, dbt |

### Product (4)
| Role | What They Do |
|------|-------------|
| Product Manager | Roadmap, PRDs, prioritization, metrics |
| Product Designer | UX/UI, design systems, usability testing |
| UX Researcher | User research, interviews, usability testing |
| Technical Writer | API docs, user guides, changelogs |

### Marketing (10)
| Role | What They Do |
|------|-------------|
| Content Marketer | Long-form SEO content, case studies, newsletters |
| SEO Specialist | Keyword research, content briefs, technical SEO |
| SEM/PPC Manager | Google Ads, LinkedIn Ads, paid acquisition |
| Social Media Manager | Twitter/X, LinkedIn, Instagram, community |
| Email Marketer | Sequences, lifecycle, deliverability |
| Brand Designer | Visual identity, positioning, messaging |
| Video Producer | Scripts, YouTube strategy, production briefs |
| PR Manager | Press releases, media pitches, thought leadership |
| Community Manager | Discord, Slack, Reddit, forums |
| Growth Marketer | Acquisition experiments, viral loops, retention |

### Sales (6)
| Role | What They Do |
|------|-------------|
| SDR | ICP prospecting, cold outreach, pipeline building |
| Account Executive | Discovery, demos, proposals, closing |
| Sales Engineer | Technical pre-sales, POCs, RFPs |
| Customer Success | Onboarding, QBRs, expansion, churn prevention |
| Revenue Operations | CRM, forecasting, process, comp plans |
| Sales Enablement | Playbooks, battlecards, training |

### Operations (5)
| Role | What They Do |
|------|-------------|
| HR Manager | Recruiting, comp, culture, performance |
| Finance Manager | Bookkeeping, projections, investor reporting |
| Legal Counsel | Contracts, IP, compliance (not legal advice) |
| Compliance Officer | GDPR, SOC2, regulatory, audits |
| Business Analyst | Data analysis, reporting, insights |

### Customer (3)
| Role | What They Do |
|------|-------------|
| Customer Support | Tickets, FAQ, empathy-driven resolution |
| Technical Support | Bug reports, debugging, escalation |
| Onboarding Specialist | Activation, training, time-to-value |

### Growth & Analytics (4)
| Role | What They Do |
|------|-------------|
| Data Analyst | SQL, dashboards, cohort analysis, insights |
| Growth Hacker | Viral loops, AARRR experiments, PLG |
| CRO Specialist | Conversion optimization, A/B testing |
| Analytics Engineer | dbt, data models, metrics layer |

### Geographic / International (3)
| Role | What They Do |
|------|-------------|
| Localization Manager | Translation, cultural adaptation, i18n |
| International Market Manager | Market entry, geo strategy |
| Translation Specialist | Professional translation, QA |

### Partnerships (3)
| Role | What They Do |
|------|-------------|
| Business Development | Strategic partnerships, deal structuring |
| Partnership Manager | Partner success, co-marketing |
| API/Integration Manager | Technical partnerships, marketplaces |

---

## MCP Servers (10)

Real tool integrations for every business function.

| Server | Tools | Integrations |
|--------|-------|-------------|
| `soloos-swarm` | swarm_launch, invoke_role, autopilot_configure, parallel_race | All SoloOS MCPs |
| `soloos-research` | market_scan, competitor_analyze, customer_pain_mine, opportunity_score | Jina, Perplexity, Reddit, HN |
| `soloos-marketing` | seo_research, content_brief, email_sequence, social_post, ad_copy | Ahrefs, Buffer, Mailchimp |
| `soloos-sales` | prospect_search, outreach_write, sequence_build, crm_update, deal_qualify | HubSpot, Apollo, LinkedIn |
| `soloos-product` | prd_create, feature_prioritize, roadmap_generate, ab_feature_plan | Linear, Jira, Productboard |
| `soloos-engineering` | architecture_review, code_review, security_audit, api_design | GitHub, SonarQube |
| `soloos-ops` | sop_create, contract_review, financial_model, compliance_check | QuickBooks, DocuSign |
| `soloos-growth` | experiment_design, funnel_analyze, viral_loop_design, growth_model | PostHog, Mixpanel, Amplitude |
| `soloos-geo` | market_entry_analyze, translate_localize, local_keyword_research | DeepL, Google Translate |
| `soloos-memory` | business_context_save, customer_insight_add, metric_track, decision_log | Mem0 (open source) |

### Install All MCP Servers
```bash
claude mcp add soloos-swarm     -- npx -y @soloos/mcp-swarm@latest
claude mcp add soloos-research  -- npx -y @soloos/mcp-research@latest
claude mcp add soloos-marketing -- npx -y @soloos/mcp-marketing@latest
claude mcp add soloos-sales     -- npx -y @soloos/mcp-sales@latest
claude mcp add soloos-product   -- npx -y @soloos/mcp-product@latest
claude mcp add soloos-engineering -- npx -y @soloos/mcp-engineering@latest
claude mcp add soloos-ops       -- npx -y @soloos/mcp-ops@latest
claude mcp add soloos-growth    -- npx -y @soloos/mcp-growth@latest
claude mcp add soloos-geo       -- npx -y @soloos/mcp-geo@latest
claude mcp add soloos-memory    -- npx -y @soloos/mcp-memory@latest
```

---

## Claude Code Skills (15)

Drop-in commands. Copy to `~/.claude/commands/` and use immediately.

| Command | What It Does |
|---------|-------------|
| `/role [name]` | Adopt any of 45 professional roles |
| `/morning` | Daily founder brief: pulse + one thing + decision cleared |
| `/decide "[decision]"` | Adversarial 3-voice debate framework (Operator / Devil's Advocate / Market Expert) |
| `/validate "[idea]"` | Paid validation gate — forces 4 sequential gates before building |
| `/prospect "[company role]"` | Full chain: research → pain hypothesis → outreach variants → sequence |
| `/launch "[product]"` | Build-in-public launch sequence: HN + Twitter + PH + LinkedIn + 50 DMs |
| `/listen "[market]"` | Community intelligence pipeline — pain signals → product opportunities |
| `/swarm [type] "[task]"` | Multi-role parallel execution (product-launch, growth-sprint, fundraise, crisis...) |
| `/research [type] [target]` | Professional market research |
| `/content [type] "[topic]"` | Content production (blog, email, social) |
| `/seo [command]` | Full SEO toolkit |
| `/sales [command]` | Sales tools (outreach, qualify, propose) |
| `/ops [command]` | Business operations (SOP, legal, finance) |
| `/growth [command]` | Growth hacking toolkit |
| `/geo [command]` | Geographic expansion toolkit |

---

## Swarm Examples

```bash
# Launch your product in parallel
/swarm product-launch "Launch PharmAudit — AI-powered pharmacy compliance software, targeting hospital pharmacy directors"

→ CMO creates GTM strategy (30 min)
→ SEO specialist researches 50 keywords (parallel)
→ Content marketer drafts 5 launch pieces (parallel)
→ SDR builds 200-prospect list + outreach (parallel)
→ PR manager writes press release + journalist list (parallel)
→ CEO synthesizes into launch plan (15 min review)

# Run weekly ops autonomously
/swarm weekly-ops

→ Data analyst pulls last week metrics, flags anomalies
→ SEO specialist checks rankings, surfaces opportunities
→ SDR sends follow-ups, updates CRM, surfaces warm leads
→ Customer success checks at-risk accounts
→ COO compiles weekly ops brief: wins, risks, actions
→ Your review: 15 minutes Monday morning

# 90-day growth sprint
/swarm growth-sprint "Grow MRR from $5K to $15K in 90 days"

→ Data analyst audits full funnel metrics
→ SEO specialist identifies quick-win keywords
→ Growth hacker designs 3 viral loop experiments
→ Content marketer builds SEO content calendar
→ SDR expands outbound to new segments
→ Synthesis: 90-day growth roadmap with weekly OKRs
```

---

## Open Source Stack

SoloOS is built on the best open source tools:

| Layer | Tools |
|-------|-------|
| Agent Orchestration | CrewAI (28K⭐), LangGraph (9K⭐), AutoGen (36K⭐) |
| Tool Integrations | Composio (12K⭐) — 150+ tool connectors |
| Workflow Automation | n8n (47K⭐) — self-hosted Zapier |
| Web Intelligence | Crawl4AI (25K⭐), Jina Reader (free), ScrapeGraph AI (16K⭐) |
| Memory | Mem0 (23K⭐), pgvector/Supabase |
| Analytics | PostHog (21K⭐), Metabase (37K⭐) |
| CRM | Twenty CRM (22K⭐) — open source Salesforce |
| Customer Support | Chatwoot (21K⭐) |
| Email | ListMonk (15K⭐) — self-hosted newsletters |
| Infrastructure | Trigger.dev (8K⭐), Infisical (14K⭐), E2B (7K⭐) |

**Full self-hosted stack cost**: ~$50-100/month
**Commercial SaaS equivalent**: $5,000-15,000/month

See [integrations/open-source/README.md](integrations/open-source/README.md) for full catalog.

---

## The Unlock

This is what SoloOS does that no other project does:

```
Standard AI agent + "write me a cold email" → Generic cold email

SoloOS agent (/role sdr) + "write me a cold email to VP Engineering at Series A startup" →
  - ICP analysis: what pain points does a Series A VP Eng have?
  - Personalization hook: recent funding = hiring mode = tooling needs
  - Email framework: PAS (Problem-Agitate-Solution)
  - Subject line: 3 A/B variants with CTR reasoning
  - Body: 4 sentences, specific pain reference, clear ask
  - Follow-up: 4-touch sequence with timing
  - CRM update: prospect record created
```

Role specialization + methodology + tools = professional output.

This is how OpenClaw extended Claude Code. SoloOS does the same for any agent working in a business context.

---

## Project Structure

```
soloprenuership/
├── CLAUDE.md                 # ← THE BEHAVIORAL UNLOCK. Drop this in your project.
├── context/                  # ← Memory system. Fill in once, compounds forever.
│   ├── business-context.md   # Current state: MRR, ICP, competition, OKRs
│   ├── customer-voice.md     # Exact customer quotes for copy and messaging
│   ├── experiment-log.md     # Growth experiments: hypothesis, results, learnings
│   └── decision-log.md       # Strategic decisions with rationale and kill signals
├── roles/                    # 45 professional role system prompts
│   ├── leadership/           # CEO, CTO, CMO, CFO, COO
│   ├── engineering/          # Frontend, Backend, DevOps, Mobile, ML, Security, QA, Data
│   ├── product/              # PM, Designer, UX Researcher, Technical Writer
│   ├── marketing/            # Content, SEO, SEM, Social, Email, Brand, Video, PR, Community, Growth
│   ├── sales/                # SDR, AE, SE, CS, RevOps, Enablement
│   ├── operations/           # HR, Finance, Legal, Compliance, Biz Analyst
│   ├── customer/             # Support, Technical, Onboarding
│   ├── growth/               # Data Analyst, Growth Hacker, CRO, Analytics Engineer
│   ├── geo/                  # Localization, International, Translation
│   └── partnerships/         # Biz Dev, Partnerships, API Integrations
├── mcp/                      # MCP server specifications
│   ├── README.md             # Installation guide
│   └── servers/              # 10 MCP server specs (TypeScript)
├── skills/                   # Claude Code custom commands
│   └── claude-code/          # 9 drop-in skill files
├── framework/                # Core frameworks
│   ├── strategy/             # Decision frameworks, BCG 3-agent rule
│   └── execution/            # Cook loop, manager-worker, parallel patterns
├── playbooks/                # Phase playbooks (discover → exit)
├── integrations/             # Open source + paid tool catalog
├── knowledge-base/           # Case studies, validated patterns
├── UNLOCK.md                 # The core "unlock" document
└── VISION.md                 # Solo billion-dollar company thesis
```

---

## Why This Exists

Three forces converging:

1. **AI capability** — Models now match senior professional output quality
2. **Agentic infrastructure** — MCP, CrewAI, LangGraph enable multi-agent coordination
3. **Open source tools** — Every business function has an open source backbone

The missing piece was the **system** — role definitions, methodology, tool wiring, swarm orchestration, quality standards. SoloOS is that system.

Every solo founder using SoloOS gets leverage that historically required a funded team.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). High-value contributions:
- New role system prompts (especially industry-specific)
- MCP server implementations
- Swarm templates for specific use cases
- Integrations with additional open source tools

---

## License

MIT — use commercially, modify freely, attribution appreciated.

---

*Built for the solo founder who refuses to hire when AI can staff the company.*
