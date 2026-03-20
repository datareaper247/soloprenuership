# Open Source Integrations

The SoloOS open source stack — the best tools to power each business function.

## Core Agent Frameworks (Foundation Layer)

### MetaGPT — Software Company Simulation
- **GitHub**: github.com/geekan/MetaGPT ⭐ 46K+
- **What it does**: Multi-agent framework with role-based SOPs for software companies
- **Why relevant**: Closest existing implementation to what SoloOS does for business
- **Integration**: Use MetaGPT's role system as inspiration for SoloOS role definitions
- **Key features**: Product Manager → Architect → Engineer → QA → DevOps roles with handoffs
- **License**: MIT

### CrewAI — Multi-Agent Orchestration
- **GitHub**: github.com/crewAIInc/crewAI ⭐ 28K+
- **What it does**: Framework for building and deploying multi-agent crews
- **Why relevant**: Best production-ready orchestration layer for SoloOS swarms
- **Integration**: Use CrewAI as the swarm runtime; SoloOS provides the roles + tools
- **Key features**: Sequential/parallel execution, role definitions, task assignment
- **License**: MIT
- **Code**:
```python
from crewai import Agent, Task, Crew
from soloos.roles import CMORole, SEORole, SDRRole

# SoloOS agents plugged into CrewAI
cmo = Agent(role=CMORole.system_prompt, tools=CMORole.tools)
seo = Agent(role=SEORole.system_prompt, tools=SEORole.tools)
sdr = Agent(role=SDRRole.system_prompt, tools=SDRRole.tools)

crew = Crew(agents=[cmo, seo, sdr], tasks=[launch_task])
crew.kickoff()
```

### Microsoft AutoGen — Conversational Multi-Agent
- **GitHub**: github.com/microsoft/autogen ⭐ 36K+
- **What it does**: Multi-agent conversation framework, agents debate + collaborate
- **Why relevant**: Perfect for SoloOS "adversarial" patterns (devil's advocate, strategy debate)
- **Integration**: Use AutoGen for strategic decision sessions (CEO + Devil's Advocate + Market Expert)
- **License**: MIT

### LangGraph — Stateful Agent Workflows
- **GitHub**: github.com/langchain-ai/langgraph ⭐ 9K+
- **What it does**: Stateful, cyclical agent workflows (loops, branches, checkpoints)
- **Why relevant**: Production-grade workflow engine for SoloOS swarms
- **Integration**: Implement SoloOS workflow templates as LangGraph graphs
- **License**: MIT

### Phidata — Agent with Tools + Memory
- **GitHub**: github.com/phidatahq/phidata ⭐ 14K+
- **What it does**: AI agent framework with built-in web search, memory, and tool use
- **Why relevant**: Quick way to deploy SoloOS roles with web search capability
- **License**: MPL 2.0

---

## Tool Integration Platforms

### Composio — 150+ Business Tool Integrations
- **GitHub**: github.com/ComposioHQ/composio ⭐ 12K+
- **What it does**: Connects AI agents to 150+ tools (Salesforce, HubSpot, Slack, GitHub, etc.)
- **Why relevant**: THE integration layer for SoloOS — gives all business function MCPs real tool access
- **Integration**: Every SoloOS MCP uses Composio for tool connections
- **Key integrations**: Salesforce, HubSpot, Pipedrive, Notion, Linear, Jira, Slack, Gmail, GitHub, Stripe, QuickBooks
- **License**: Elastic + open core
- **Code**:
```python
from composio_langchain import ComposioToolSet, Action

toolset = ComposioToolSet()
# CRM tools for Sales MCP
crm_tools = toolset.get_tools(actions=[
    Action.HUBSPOT_CREATE_CONTACT,
    Action.HUBSPOT_UPDATE_DEAL,
    Action.HUBSPOT_SEARCH_CONTACTS
])
```

### n8n — Self-Hosted Workflow Automation
- **GitHub**: github.com/n8n-io/n8n ⭐ 47K+
- **What it does**: Visual workflow automation (like Zapier, but open source and self-hostable)
- **Why relevant**: SoloOS autopilot workflows live here — schedule and automate agent tasks
- **Integration**: SoloOS weekly ops swarms run as n8n workflows
- **License**: Source Available (SSPL for self-host is free)
- **SoloOS Workflows**:
  - Weekly SEO rank monitoring + report
  - Competitor pricing page screenshot comparison
  - New customer onboarding sequence trigger
  - Churn risk detection + alert

### Apify — Web Scraping Platform
- **GitHub**: github.com/apify/crawlee ⭐ 14K+
- **What it does**: Web scraping and browser automation at scale
- **Why relevant**: Powers SoloOS research agents (competitor scraping, G2 reviews, SERP analysis)
- **License**: Apache 2.0

### Browserbase / Stagehand — AI Browser Automation
- **GitHub**: github.com/browserbase/stagehand ⭐ 7K+
- **What it does**: Browser automation that works with AI agents
- **Why relevant**: SoloOS agents can browse competitor sites, fill forms, research live data
- **License**: MIT

### E2B — Code Execution Sandboxes
- **GitHub**: github.com/e2b-dev/e2b ⭐ 7K+
- **What it does**: Isolated sandboxes for running AI-generated code
- **Why relevant**: SoloOS Build Engine uses E2B for safe code testing
- **License**: Apache 2.0

---

## Memory & Context

### Mem0 — Agent Memory Layer
- **GitHub**: github.com/mem0ai/mem0 ⭐ 23K+
- **What it does**: Persistent memory for AI agents (semantic search over past interactions)
- **Why relevant**: Powers `soloos-memory` MCP — agents remember business context across sessions
- **Integration**: Every SoloOS agent reads/writes to Mem0 for business context
- **License**: Apache 2.0
- **Code**:
```python
from mem0 import Memory

memory = Memory()
# Save customer insight
memory.add("Customers hate the 3-minute onboarding flow", user_id="business-context")
# Retrieve for agent
insights = memory.search("customer onboarding pain points")
```

### Zep — Memory for LLMs
- **GitHub**: github.com/getzep/zep ⭐ 3K+
- **What it does**: Fast, scalable long-term memory for LLM applications
- **Why relevant**: Alternative to Mem0 with better structured data support
- **License**: Apache 2.0

---

## Research & Web Intelligence

### Jina Reader — Free Web Scraping
- **API**: r.jina.ai/{url} — no API key needed
- **What it does**: Clean markdown extraction from any URL
- **Why relevant**: SoloOS research agents use this for competitor research (free)
- **GitHub**: github.com/jina-ai/reader

### ScrapeGraph AI — AI-Powered Web Scraping
- **GitHub**: github.com/VinciGit00/Scrapegraph-ai ⭐ 16K+
- **What it does**: Uses AI to understand web page structure, extracts structured data
- **Why relevant**: Competitors' pricing pages → structured data without brittle scrapers
- **License**: MIT

### Crawl4AI — Web Crawling for LLMs
- **GitHub**: github.com/unclecode/crawl4ai ⭐ 25K+
- **What it does**: LLM-optimized web crawler that outputs clean markdown
- **Why relevant**: Research engine web crawling
- **License**: Apache 2.0

---

## Analytics & Monitoring

### PostHog — Open Source Product Analytics
- **GitHub**: github.com/PostHog/posthog ⭐ 21K+
- **What it does**: Product analytics, feature flags, A/B testing, session recording
- **Why relevant**: SoloOS growth engine integrates directly; Growth Hacker agent reads PostHog data
- **License**: MIT / SSPL

### Plausible — Privacy-Friendly Web Analytics
- **GitHub**: github.com/plausible/analytics ⭐ 20K+
- **What it does**: Simple, privacy-friendly web analytics
- **Why relevant**: SoloOS SEO agent reads traffic data for content performance
- **License**: AGPL

### Metabase — Open Source Business Intelligence
- **GitHub**: github.com/metabase/metabase ⭐ 37K+
- **What it does**: BI dashboards for any database
- **Why relevant**: SoloOS financial and growth dashboards
- **License**: AGPL + commercial

---

## CRM & Customer Tools

### Twenty CRM — Open Source CRM
- **GitHub**: github.com/twentyhq/twenty ⭐ 22K+
- **What it does**: Open source alternative to Salesforce
- **Why relevant**: SoloOS sales agents use this as the CRM backend
- **License**: AGPL

### Chatwoot — Open Source Customer Support
- **GitHub**: github.com/chatwoot/chatwoot ⭐ 21K+
- **What it does**: Customer messaging platform (live chat, email, social)
- **Why relevant**: SoloOS customer support agent integrates here
- **License**: MIT

### Cal.com — Open Source Scheduling
- **GitHub**: github.com/calcom/cal.com ⭐ 32K+
- **What it does**: Scheduling infrastructure
- **Why relevant**: Sales agent uses this for demo scheduling automation
- **License**: AGPL

---

## Email & Marketing

### ListMonk — Self-Hosted Email Newsletters
- **GitHub**: github.com/knadh/listmonk ⭐ 15K+
- **What it does**: High-performance newsletter and mailing list manager
- **Why relevant**: SoloOS email marketing agent uses this for newsletters (no per-email cost)
- **License**: AGPL

### Formbricks — Open Source Survey Platform
- **GitHub**: github.com/formbricks/formbricks ⭐ 9K+
- **What it does**: Open source survey and feedback collection
- **Why relevant**: SoloOS uses this for customer discovery surveys, NPS collection
- **License**: AGPL

---

## DevOps & Infrastructure

### Infisical — Open Source Secrets Management
- **GitHub**: github.com/Infisical/infisical ⭐ 14K+
- **What it does**: Open source alternative to Vault for secrets management
- **Why relevant**: SoloOS stores all API keys and credentials securely
- **License**: MIT

### Trigger.dev — Background Jobs
- **GitHub**: github.com/triggerdotdev/trigger.dev ⭐ 8K+
- **What it does**: Open source background job framework
- **Why relevant**: SoloOS swarm jobs and scheduled tasks run on Trigger.dev
- **License**: Apache 2.0

---

## The SoloOS Open Source Stack

```
┌─────────────────────────────────────────────┐
│  AGENT ORCHESTRATION                        │
│  CrewAI + LangGraph + AutoGen               │
├─────────────────────────────────────────────┤
│  TOOL INTEGRATIONS                          │
│  Composio (150+ tools) + n8n (automation)   │
├─────────────────────────────────────────────┤
│  WEB INTELLIGENCE                           │
│  Jina Reader + Crawl4AI + ScrapeGraph AI    │
├─────────────────────────────────────────────┤
│  MEMORY & CONTEXT                           │
│  Mem0 + pgvector (Supabase)                 │
├─────────────────────────────────────────────┤
│  ANALYTICS                                  │
│  PostHog + Plausible + Metabase             │
├─────────────────────────────────────────────┤
│  CRM & SALES                                │
│  Twenty CRM + Apollo (for prospecting)      │
├─────────────────────────────────────────────┤
│  CUSTOMER OPS                               │
│  Chatwoot + Cal.com + Formbricks            │
├─────────────────────────────────────────────┤
│  EMAIL                                      │
│  ListMonk (newsletters) + Resend (transact) │
├─────────────────────────────────────────────┤
│  INFRASTRUCTURE                             │
│  Trigger.dev + Infisical + E2B              │
└─────────────────────────────────────────────┘
```

**Total cost for fully self-hosted**: ~$50-100/month in hosting
**Commercial equivalent**: $5,000-15,000/month in SaaS tools
