# MCP Servers for SoloOS

> Install existing, production-ready MCP servers that give your SoloOS roles real tool access.
> Don't reinvent — wrap. These servers work today.

---

## Quick Install: Essential Stack

The minimum MCP set to power all SoloOS roles:

```bash
# Research & Web Intelligence
claude mcp add jina -- npx -y @jina-ai/mcp-server-jina
claude mcp add firecrawl -- npx -y firecrawl-mcp
claude mcp add brave-search -- npx -y @modelcontextprotocol/server-brave-search
claude mcp add exa -- npx -y exa-mcp-server

# Productivity & Project Management
claude mcp add notion -- npx -y @notionhq/mcp
claude mcp add linear -- npx -y linear-mcp-server
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Communication
claude mcp add slack -- npx -y @modelcontextprotocol/server-slack
claude mcp add gmail -- npx -y @modelcontextprotocol/server-gmail

# Sales & CRM
claude mcp add hubspot -- npx -y @hubspot/mcp-server

# Analytics
claude mcp add posthog -- npx -y posthog-mcp-server

# Universal connector (8,000+ actions)
claude mcp add zapier -- npx -y zapier-mcp
```

---

## By Business Function

### Research & Intelligence

| MCP Server | Install | What It Powers |
|------------|---------|----------------|
| **Jina Reader** | `npx -y @jina-ai/mcp-server-jina` | Free URL-to-markdown extraction. No API key. Competitor pages, blog posts, docs |
| **Firecrawl** | `npx -y firecrawl-mcp` | Deep web scraping + structured data extraction. Pricing pages → JSON |
| **Exa Search** | `npx -y exa-mcp-server` | Neural web search built for AI agents. Semantic similarity over recency |
| **Brave Search** | `npx -y @modelcontextprotocol/server-brave-search` | Privacy-respecting web search. Good for market research |
| **Perplexity** | `npx -y @modelcontextprotocol/server-perplexity` | Real-time web + AI synthesis. Best for "what's happening now" queries |
| **Reddit** | Already in your setup | Pain point mining, competitor discussions, ICP research |
| **HackerNews** | Already in your setup | Tech trend signals, B2B buyer mindset, Show HN competitor launches |
| **Fetch** | `npx -y @modelcontextprotocol/server-fetch` | General HTTP requests to any URL or API |

**Roles powered**: Market Researcher, Competitive Analyst, UX Researcher, Growth Hacker

```bash
# Example: Research Agent using these MCPs
claude mcp add jina -- npx -y @jina-ai/mcp-server-jina
claude mcp add exa -- npx -y exa-mcp-server
claude mcp add firecrawl -- npx -y firecrawl-mcp
```

---

### SEO & Content Marketing

| MCP Server | Install | What It Powers |
|------------|---------|----------------|
| **Ahrefs** | `npx -y ahrefs-mcp-server` | Keyword research, backlink analysis, site audit |
| **Semrush** | Contact Semrush for MCP access | Keyword/competitor research, position tracking |
| **Google Search Console** | Via Zapier MCP or direct API | Organic performance data, indexing status |
| **Jina Reader** | `npx -y @jina-ai/mcp-server-jina` | SERP analysis, competitor content extraction |

**Roles powered**: SEO Specialist, Content Marketer, SEM Manager

**Alternative (free)**: Use Jina + Brave Search + Firecrawl for zero-cost SEO research

---

### Sales & CRM

| MCP Server | Install | What It Powers |
|------------|---------|----------------|
| **HubSpot Official** | `npx -y @hubspot/mcp-server` | Contact management, deal pipeline, email sequences, company data |
| **Apollo.io** | `npx -y apollo-mcp-server` | 34+ tools: prospect search, contact enrichment, email sequences |
| **Salesforce** | Via Composio MCP | Full CRM operations, opportunity management, forecasting |
| **LinkedIn** | Via Composio MCP | Profile research, connection requests, InMail (use carefully) |
| **Clay** | Via Zapier MCP | AI-powered prospect enrichment and personalization |
| **Pipedrive** | `npx -y pipedrive-mcp` | Pipeline management, deal tracking, activity logging |

**Roles powered**: SDR, Account Executive, Revenue Ops, Customer Success

```bash
# Sales stack
claude mcp add hubspot -- npx -y @hubspot/mcp-server
claude mcp add apollo -- npx -y apollo-mcp-server
```

---

### Productivity & Project Management

| MCP Server | Install | What It Powers |
|------------|---------|----------------|
| **Notion** | `npx -y @notionhq/mcp` | Docs, databases, wikis, meeting notes, knowledge base |
| **Linear** | `npx -y linear-mcp-server` | Issue tracking, roadmap management, sprint planning |
| **Jira** | Via Composio or `npx -y jira-mcp` | Enterprise project tracking, agile boards |
| **GitHub** | `npx -y @modelcontextprotocol/server-github` | Repo management, issues, PRs, code review |
| **Asana** | Via Zapier MCP | Task management, project tracking, team workload |

**Roles powered**: Product Manager, COO, DevOps Engineer, Backend Engineer

---

### Communication & Email

| MCP Server | Install | What It Powers |
|------------|---------|----------------|
| **Slack** | `npx -y @modelcontextprotocol/server-slack` | Send messages, read channels, post updates to team |
| **Gmail** | `npx -y @modelcontextprotocol/server-gmail` | Read/send emails, manage labels, draft responses |
| **Google Calendar** | `npx -y @modelcontextprotocol/server-google-calendar` | Schedule meetings, check availability, create events |
| **SendGrid** | Via Composio or Zapier | Transactional email, marketing campaigns |
| **Mailchimp** | Via Zapier MCP | Email list management, campaign creation |

**Roles powered**: SDR, Email Marketer, Customer Success, PR Manager

---

### Analytics & Business Intelligence

| MCP Server | Install | What It Powers |
|------------|---------|----------------|
| **PostHog** | `npx -y posthog-mcp-server` | Product analytics, feature flags, user events, funnel data |
| **Stripe** | `npx -y stripe-mcp` | Payment data, subscription metrics, MRR/ARR, churn |
| **Mixpanel** | Via Composio or Zapier | User behavior analytics, cohort analysis |
| **Amplitude** | Via Zapier MCP | Product analytics, user journeys, retention data |
| **Google Analytics** | Via Zapier or `npx -y ga4-mcp-server` | Web traffic, acquisition, conversion data |

**Roles powered**: Data Analyst, Growth Hacker, CRO Specialist, CFO

```bash
# Analytics stack
claude mcp add posthog -- npx -y posthog-mcp-server
claude mcp add stripe -- npx -y stripe-mcp
```

---

### Finance & Operations

| MCP Server | Install | What It Powers |
|------------|---------|----------------|
| **Stripe** | `npx -y stripe-mcp` | Payment processing, subscription management, revenue data |
| **QuickBooks** | Via Zapier MCP | Bookkeeping, invoicing, expense tracking, financial reports |
| **Xero** | Via Zapier MCP | Accounting, bank reconciliation, payroll |
| **Docuseal** | Self-hosted + API | Document signing, contract execution |

**Roles powered**: CFO, Finance Manager, Legal Counsel, Compliance Officer

---

### Customer Support

| MCP Server | Install | What It Powers |
|------------|---------|----------------|
| **Intercom** | Via Composio or Zapier | Customer conversations, support tickets, user data |
| **Zendesk** | Via Zapier MCP | Ticket management, SLA tracking, help center |
| **Chatwoot** | Self-hosted + API | Open source alternative to Intercom, full API |
| **Cal.com** | Self-hosted + API | Meeting scheduling, availability management |

**Roles powered**: Customer Support, Technical Support, Onboarding Specialist

---

### Developer Tools

| MCP Server | Install | What It Powers |
|------------|---------|----------------|
| **GitHub** | `npx -y @modelcontextprotocol/server-github` | Code, issues, PRs, releases, org management |
| **GitLab** | `npx -y @modelcontextprotocol/server-gitlab` | GitLab repos, CI/CD, merge requests |
| **Docker** | `npx -y docker-mcp-server` | Container management, image builds, registry |
| **Vercel** | `npx -y vercel-mcp-server` | Deployment management, domain config, logs |
| **Supabase** | `npx -y @supabase/mcp-server-supabase` | Database, auth, edge functions, storage |
| **Sentry** | `npx -y sentry-mcp` | Error tracking, performance monitoring, issue management |
| **PostgreSQL** | `npx -y @modelcontextprotocol/server-postgres` | Direct database access, queries, schema inspection |
| **SQLite** | `npx -y @modelcontextprotocol/server-sqlite` | Local database operations |
| **Filesystem** | `npx -y @modelcontextprotocol/server-filesystem` | File read/write operations |
| **Memory** | `npx -y @modelcontextprotocol/server-memory` | Persistent key-value memory across sessions |

**Roles powered**: CTO, Backend Engineer, DevOps Engineer, Data Engineer

---

### Social Media & Community

| MCP Server | Install | What It Powers |
|------------|---------|----------------|
| **Reddit** | Already in your setup | Research + community engagement |
| **Twitter/X** | Via Composio or Zapier | Post tweets, read timeline, DMs (use with care) |
| **Buffer** | Via Zapier MCP | Schedule social posts across platforms |
| **LinkedIn** | Via Composio | Company page posts, personal updates |

**Roles powered**: Social Media Manager, Community Manager, PR Manager

---

## Universal Connectors (Cover Everything Else)

### Zapier MCP — 8,000+ Apps
```bash
claude mcp add zapier -- npx -y zapier-mcp
```
Covers: Any tool with a Zapier integration. 30,000+ pre-built actions.
Use when: The specific MCP doesn't exist but the tool has Zapier support.

### Composio MCP — 150+ Business Tools
```bash
pip install composio-claude
composio add hubspot salesforce github slack
```
Covers: Salesforce, HubSpot, GitHub, Slack, Notion, Linear, Jira, Gmail, Google Calendar, Twitter, LinkedIn, Stripe, Shopify, and 130+ more.
Use when: You need multiple tool connections under one SDK.

**Composio quick start**:
```python
from composio_claude import ComposioToolSet, Action

toolset = ComposioToolSet()

# Get tools for sales agent
sales_tools = toolset.get_tools(actions=[
    Action.HUBSPOT_CREATE_CONTACT,
    Action.HUBSPOT_CREATE_DEAL,
    Action.APOLLO_SEARCH_PEOPLE,
    Action.GMAIL_SEND_EMAIL,
])

# Get tools for growth agent
growth_tools = toolset.get_tools(actions=[
    Action.POSTHOG_GET_EVENTS,
    Action.STRIPE_GET_CUSTOMERS,
    Action.GOOGLESHEETS_CREATE_SPREADSHEET,
])
```

---

## MCP Server Reliability Tiers

| Tier | Servers | Reliability | Use For |
|------|---------|-------------|---------|
| **Tier 1: Official** | GitHub (Anthropic), HubSpot, Notion, Supabase, Stripe | Highest | Production use |
| **Tier 2: Well-maintained** | Jina, Exa, Brave Search, PostHog, Apollo | High | Daily workflows |
| **Tier 3: Community** | Most others on mcp.so / GitHub | Variable | Evaluate before using |
| **Universal fallback** | Zapier MCP, Composio | High (wrapper) | Anything not in Tier 1-2 |

---

## MCP Discovery Resources

- **Anthropic official servers**: github.com/modelcontextprotocol/servers
- **Community registry**: mcp.so (7,000+ servers)
- **Awesome MCP list**: github.com/punkpeye/awesome-mcp-servers
- **MCP Hub**: mcphub.io

---

## Recommended Stack by SoloOS Stage

### Stage 1: Just starting (free/low cost)
```bash
claude mcp add jina -- npx -y @jina-ai/mcp-server-jina
claude mcp add brave-search -- npx -y @modelcontextprotocol/server-brave-search
claude mcp add github -- npx -y @modelcontextprotocol/server-github
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem
claude mcp add memory -- npx -y @modelcontextprotocol/server-memory
# + Reddit and HackerNews already configured
```

### Stage 2: GTM-ready ($50-200/mo in tools)
```bash
# + Sales stack
claude mcp add hubspot -- npx -y @hubspot/mcp-server
claude mcp add apollo -- npx -y apollo-mcp-server
# + Productivity
claude mcp add notion -- npx -y @notionhq/mcp
claude mcp add linear -- npx -y linear-mcp-server
# + Analytics
claude mcp add posthog -- npx -y posthog-mcp-server
claude mcp add stripe -- npx -y stripe-mcp
```

### Stage 3: Full company OS ($200-500/mo in tools)
```bash
# Add all above PLUS
claude mcp add zapier -- npx -y zapier-mcp  # Universal coverage
claude mcp add slack -- npx -y @modelcontextprotocol/server-slack
claude mcp add gmail -- npx -y @modelcontextprotocol/server-gmail
claude mcp add supabase -- npx -y @supabase/mcp-server-supabase
# + Composio for any remaining gaps
pip install composio-claude
```

---

## Role → MCP Mapping

| SoloOS Role | Primary MCPs |
|-------------|-------------|
| `/role seo-specialist` | Jina, Brave Search, Exa, Ahrefs |
| `/role sdr` | HubSpot, Apollo, Gmail, LinkedIn (Composio) |
| `/role account-executive` | HubSpot, Notion, Cal.com, Stripe |
| `/role content-marketer` | Notion, Jina, Exa, Buffer (Zapier) |
| `/role data-analyst` | PostHog, Stripe, PostgreSQL, Google Sheets (Zapier) |
| `/role growth-hacker` | PostHog, Stripe, Exa, A/B tools (Zapier) |
| `/role cmo` | Jina, HubSpot, PostHog, Google Analytics (Zapier) |
| `/role cto` | GitHub, Supabase, Sentry, Docker |
| `/role cfo` | Stripe, QuickBooks (Zapier), PostgreSQL |
| `/role customer-success` | HubSpot, Intercom (Zapier), Cal.com |
| `/role product-manager` | Linear, GitHub, Notion, PostHog |
| `/role pr-manager` | Exa, Brave Search, Gmail, Twitter (Composio) |
