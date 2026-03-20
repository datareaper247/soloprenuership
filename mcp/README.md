# SoloOS MCP Servers

10 Model Context Protocol servers covering every business function.

## One-Command Install (All Servers)

```bash
# Claude Code
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

# Cursor / Any MCP Client (mcp.json)
{
  "mcpServers": {
    "soloos-swarm":       { "command": "npx", "args": ["-y", "@soloos/mcp-swarm@latest"] },
    "soloos-research":    { "command": "npx", "args": ["-y", "@soloos/mcp-research@latest"] },
    "soloos-marketing":   { "command": "npx", "args": ["-y", "@soloos/mcp-marketing@latest"] },
    "soloos-sales":       { "command": "npx", "args": ["-y", "@soloos/mcp-sales@latest"] },
    "soloos-product":     { "command": "npx", "args": ["-y", "@soloos/mcp-product@latest"] },
    "soloos-engineering": { "command": "npx", "args": ["-y", "@soloos/mcp-engineering@latest"] },
    "soloos-ops":         { "command": "npx", "args": ["-y", "@soloos/mcp-ops@latest"] },
    "soloos-growth":      { "command": "npx", "args": ["-y", "@soloos/mcp-growth@latest"] },
    "soloos-geo":         { "command": "npx", "args": ["-y", "@soloos/mcp-geo@latest"] },
    "soloos-memory":      { "command": "npx", "args": ["-y", "@soloos/mcp-memory@latest"] }
  }
}
```

---

## Server Index

### `soloos-swarm` — The Orchestrator
**The unlock server. Turns your agent into a company.**

| Tool | Description |
|------|-------------|
| `swarm_launch` | Launch typed multi-agent swarms (product_launch, market_research, growth_sprint, weekly_ops) |
| `invoke_role` | Instantly adopt any of 44 professional roles with full methodology |
| `autopilot_configure` | Schedule recurring autonomous company operations |
| `parallel_race` | Run N agents on same task, return best output |
| `workflow_run` | Execute pre-built business workflows |

**Example:**
```
"Use soloos-swarm to launch a product_launch swarm for our DevOps monitoring tool targeting senior engineers"
```

---

### `soloos-research` — Market Intelligence
**Professional market research without a research team.**

| Tool | Description |
|------|-------------|
| `market_scan` | Full market opportunity analysis (TAM, competitors, trends) |
| `competitor_analyze` | Deep competitive profile (features, pricing, positioning, weaknesses) |
| `customer_pain_mine` | Extract validated pain points from Reddit, HN, reviews |
| `opportunity_score` | Score business ideas on 10 dimensions |
| `trend_detect` | Identify emerging trends before they peak |

---

### `soloos-marketing` — Full-Stack Marketing
**CMO + SEO + Content + Email + Social + PR in one server.**

| Tool | Description |
|------|-------------|
| `seo_research` | Keyword research: volume, difficulty, CPC, SERP features |
| `content_brief` | Full SEO content brief with H2/H3 structure |
| `seo_content_write` | Write complete SEO-optimized article |
| `email_sequence` | Create complete lifecycle email sequences |
| `social_post` | Platform-optimized posts (Twitter, LinkedIn, Instagram) |
| `ad_copy` | Ad copy for Google, LinkedIn, Meta with A/B variants |
| `landing_page_copy` | Full landing page copy optimized for conversion |
| `press_release` | Professional press release |
| `content_calendar` | 30-90 day content calendar |
| `geo_seo` | Multi-country SEO strategy with hreflang |

---

### `soloos-sales` — Revenue Engine
**SDR + AE + CS capabilities with CRM integration.**

| Tool | Description |
|------|-------------|
| `prospect_search` | Find ICPs matching your criteria |
| `outreach_write` | Personalized cold outreach (email/LinkedIn/call) |
| `sequence_build` | Multi-touch outreach sequences |
| `deal_qualify` | MEDDIC/BANT/SPICED qualification |
| `proposal_generate` | Professional proposals with ROI calculations |
| `crm_update` | Log activities to HubSpot/Salesforce/Twenty |
| `forecast_update` | Update pipeline forecasts |
| `objection_handle` | Objection handling scripts |

---

### `soloos-product` — Product Development
**PM + Designer capabilities for product decisions.**

| Tool | Description |
|------|-------------|
| `prd_create` | Product Requirements Documents |
| `feature_prioritize` | RICE/ICE scoring and prioritization |
| `roadmap_generate` | Product roadmap from priorities |
| `user_story_write` | User stories with acceptance criteria |
| `competitor_feature_map` | Feature coverage vs competitors |
| `nps_analyze` | NPS survey analysis |
| `okr_create` | OKRs aligned to company strategy |

---

### `soloos-engineering` — Engineering Excellence
**CTO + Senior Engineer capabilities.**

| Tool | Description |
|------|-------------|
| `architecture_review` | System architecture review with risk analysis |
| `code_review` | Security + performance + maintainability scoring |
| `api_design` | REST/GraphQL API design with OpenAPI spec |
| `security_audit` | OWASP security checklist |
| `tech_debt_audit` | Technical debt identification and quantification |
| `infra_cost_estimate` | Cloud infrastructure cost estimation |
| `migration_plan` | Database/system migration plans |

---

### `soloos-ops` — Business Operations
**COO + HR + Legal + Finance capabilities.**

| Tool | Description |
|------|-------------|
| `sop_create` | Standard Operating Procedures |
| `contract_review` | Contract risk analysis and redlines |
| `financial_model` | 12/24-month financial models (P&L, cash flow) |
| `compliance_check` | GDPR/SOC2/HIPAA compliance status |
| `hiring_package` | Job descriptions, interview questions, rubrics |
| `policy_generate` | Privacy policy, ToS, data processing agreements |

---

### `soloos-growth` — Growth Engine
**Growth hacker + CRO + analytics capabilities.**

| Tool | Description |
|------|-------------|
| `experiment_design` | A/B experiment design with sample size |
| `funnel_analyze` | Conversion funnel analysis |
| `viral_loop_design` | Referral and viral growth mechanics |
| `cohort_analyze` | Retention cohort analysis |
| `growth_model` | Growth projections (3 scenarios) |
| `north_star_define` | North star metric and driver tree |
| `channel_score` | Acquisition channel scoring (CAC, scalability) |

---

### `soloos-geo` — Geographic Expansion
**Full international expansion capabilities.**

| Tool | Description |
|------|-------------|
| `market_entry_analyze` | Country market entry analysis |
| `translate_localize` | Translation + cultural adaptation |
| `local_keyword_research` | Keyword research per locale |
| `hreflang_generate` | hreflang tags for multi-language SEO |
| `regulatory_check` | Country-specific regulatory requirements |
| `cultural_fit_score` | Product/messaging cultural fit scoring |

---

### `soloos-memory` — Business Memory
**Persistent context across all agent sessions.**

| Tool | Description |
|------|-------------|
| `business_context_save` | Save decisions, strategy, insights |
| `business_context_get` | Retrieve context relevant to current task |
| `customer_insight_add` | Add customer feedback and interview insights |
| `metric_track` | Track business metrics (MRR, CAC, LTV, churn) |
| `decision_log` | Log business decisions with rationale |
| `brand_context_get` | Get brand voice, positioning, ICP for agents |

**Powered by [Mem0](https://github.com/mem0ai/mem0) (23K⭐ — open source)**

---

## Environment Variables

```env
# Core (required)
ANTHROPIC_API_KEY=...

# Research
PERPLEXITY_API_KEY=...          # Deep research
JINA_API_KEY=...                # Optional (free tier works without)

# Marketing
AHREFS_API_KEY=...              # Keyword data (or SEMRUSH_API_KEY)
GOOGLE_SEARCH_CONSOLE=...       # Rank tracking

# Sales
APOLLO_API_KEY=...              # Prospecting (free tier available)
COMPOSIO_API_KEY=...            # CRM integrations (HubSpot, Salesforce)

# Email/Social
MAILCHIMP_API_KEY=...           # Email (or use ListMonk self-hosted)
BUFFER_ACCESS_TOKEN=...         # Social scheduling

# Localization
DEEPL_API_KEY=...               # Translation quality

# Analytics
POSTHOG_API_KEY=...             # Product analytics (free tier)

# Memory
MEM0_API_KEY=...                # Agent memory (or self-host)
```

---

## Architecture

All servers follow the same pattern:

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'soloos-[function]',
  version: '1.0.0'
});

server.tool('tool_name', 'description', {
  param: z.string().describe('Parameter description'),
}, async (params) => {
  // implementation
  return { content: [{ type: 'text', text: result }] };
});
```

See individual server specs in `mcp/servers/` for full TypeScript definitions.

---

## Integration with CrewAI / AutoGen / LangGraph

```python
# CrewAI
from crewai import Agent, Task, Crew
# Load SoloOS role system prompts
from soloos.roles import get_role_prompt, get_tools

seo_agent = Agent(
    role="SEO Specialist",
    backstory=get_role_prompt("seo_specialist"),
    tools=get_tools("marketing", ["seo_research", "content_brief"])
)

# AutoGen
import autogen
seo_config = {
    "name": "SEO_Specialist",
    "system_message": get_role_prompt("seo_specialist")
}

# LangGraph
from langgraph.graph import StateGraph
# Each SoloOS role becomes a node in the graph
```
