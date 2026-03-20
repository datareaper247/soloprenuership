# soloos-sales MCP Server

**Purpose**: Full-cycle B2B sales capabilities — prospecting, enrichment, outreach, CRM, pipeline management, and forecasting.

## TypeScript Server Definition

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'soloos-sales',
  version: '1.0.0',
  description: 'End-to-end B2B sales tools for solo founders and small sales teams'
});

// ─── PROSPECTING ──────────────────────────────

server.tool('prospect_search', 'Find ideal customer profiles matching ICP criteria', {
  industry: z.string().describe('e.g. "SaaS", "FinTech", "Healthcare IT"'),
  company_size: z.enum(['1-10', '11-50', '51-200', '201-1000', '1000+']).optional(),
  role: z.string().describe('Job title or function, e.g. "Head of Engineering", "VP Sales"'),
  funding_stage: z.enum(['bootstrapped', 'pre-seed', 'seed', 'series-a', 'series-b', 'series-c+']).optional(),
  geography: z.array(z.string()).optional().describe('Countries or regions'),
  keywords: z.array(z.string()).optional().describe('Tech stack, tools used, intent signals'),
  limit: z.number().default(25)
}, async ({ industry, company_size, role, funding_stage, geography, keywords, limit }) => {
  // Query Apollo.io free tier (250 export credits/month)
  // Filter by ICP: industry SIC codes, headcount, title seniority
  // Layer Crunchbase/LinkedIn signals for funding context
  // Deduplicate against existing CRM records via Twenty CRM API
  // Return: company name, domain, LinkedIn URL, estimated revenue, tech stack, recent news
});

server.tool('contact_enrich', 'Enrich contact with email, LinkedIn, and company intelligence', {
  first_name: z.string().optional(),
  last_name: z.string().optional(),
  company_domain: z.string(),
  linkedin_url: z.string().optional()
}, async ({ first_name, last_name, company_domain, linkedin_url }) => {
  // Hunter.io free tier (25 searches/month) for email discovery
  // Apollo.io contact enrichment for direct phone, LinkedIn
  // Clearbit-equivalent OSS for company firmographics (revenue, headcount, tech)
  // Return: verified email, confidence score, direct phone, LinkedIn, company context
});

// ─── OUTREACH ─────────────────────────────────

server.tool('outreach_write', 'Generate personalized cold outreach copy', {
  channel: z.enum(['email', 'linkedin', 'call_script', 'twitter_dm']),
  prospect: z.object({
    name: z.string(),
    title: z.string(),
    company: z.string(),
    industry: z.string(),
    pain_point: z.string().optional(),
    recent_news: z.string().optional()
  }),
  product: z.string().describe('Brief description of your product/value prop'),
  icp_outcome: z.string().describe('Specific outcome this ICP cares about'),
  tone: z.enum(['professional', 'conversational', 'direct', 'challenger']).default('conversational'),
  variants: z.number().default(3)
}, async (params) => {
  // Generate N variants per channel
  // Email: subject line (3 options) + body (150 words max) + P.S. line
  // LinkedIn: connection request (300 chars) + follow-up message
  // Call script: opener, discovery questions, value statement, handle gatekeeper
  // Personalization hooks: reference company news, tech stack, mutual connections
  // Score each variant for personalization depth and clarity of value prop
});

server.tool('sequence_build', 'Build a multi-touch outreach sequence', {
  prospect_segment: z.string().describe('Who this sequence targets'),
  product: z.string(),
  touches: z.number().min(5).max(10).default(7),
  channels: z.array(z.enum(['email', 'linkedin', 'phone', 'twitter'])).default(['email', 'linkedin']),
  goal: z.enum(['demo_booked', 'trial_signup', 'intro_call', 'content_download']).default('demo_booked'),
  days_between: z.array(z.number()).optional().describe('Days between each touch — defaults to [1,2,3,5,7,10]')
}, async (params) => {
  // Map multi-channel sequence with channel-day matrix
  // Touch 1: warm email + LinkedIn view
  // Touch 2: LinkedIn connection request
  // Touch 3: Follow-up email referencing content
  // Touch 4: LinkedIn message
  // Touch 5: Phone call + voicemail script
  // Touch 6-7: Break-up emails
  // Return: complete sequence with copy for each touch, timing logic, exit conditions
});

server.tool('email_score', 'Score and improve cold email copy', {
  subject: z.string(),
  body: z.string(),
  cta: z.string()
}, async ({ subject, body, cta }) => {
  // Score across 6 dimensions (0-10 each):
  // 1. Personalization: Is it specific to this person/company?
  // 2. Clarity: Is the value prop immediately clear?
  // 3. Brevity: Under 150 words?
  // 4. CTA quality: Single, low-friction ask?
  // 5. Subject line: Curiosity + relevance?
  // 6. Social proof: Credibility signals without being braggy?
  // Return: scores + specific improvement suggestions + rewritten version
});

// ─── CRM & PIPELINE ───────────────────────────

server.tool('crm_update', 'Log activities and update deal records in CRM', {
  crm: z.enum(['twenty', 'hubspot', 'salesforce', 'pipedrive']).default('twenty'),
  action: z.enum(['log_email', 'log_call', 'log_meeting', 'create_contact', 'update_deal', 'add_note']),
  contact_email: z.string().optional(),
  company_domain: z.string().optional(),
  deal_id: z.string().optional(),
  data: z.record(z.string(), z.unknown()).describe('Fields to create or update')
}, async (params) => {
  // Twenty CRM: open-source HubSpot alternative (self-hosted or twenty.com)
  // HubSpot/Salesforce via Composio — handles OAuth + API abstractions
  // Auto-enrich contact record on creation (trigger contact_enrich)
  // Return: updated record URL, field change summary
});

server.tool('deal_qualify', 'Qualify a deal using structured frameworks', {
  framework: z.enum(['meddic', 'bant', 'spiced', 'custom']).default('meddic'),
  deal_notes: z.string().describe('Call notes, email history, discovery info'),
  deal_size: z.number().optional(),
  company: z.string().optional()
}, async ({ framework, deal_notes, deal_size, company }) => {
  // MEDDIC: Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion
  // BANT: Budget, Authority, Need, Timeline
  // SPICED: Situation, Pain, Impact, Critical Event, Decision
  // Score each dimension Green/Yellow/Red
  // Identify qualification gaps and next questions to ask
  // Return: qualification scorecard + recommended next actions
});

// ─── PROPOSALS & OBJECTIONS ───────────────────

server.tool('proposal_generate', 'Generate a professional sales proposal with ROI analysis', {
  company: z.string(),
  prospect_name: z.string(),
  deal_context: z.string().describe('Pain points, goals, timeline from discovery'),
  product: z.string(),
  pricing_options: z.array(z.object({
    tier: z.string(),
    price: z.number(),
    billing: z.enum(['monthly', 'annual'])
  })),
  roi_inputs: z.object({
    current_cost: z.number().optional(),
    time_saved_hours_per_week: z.number().optional(),
    revenue_impact: z.number().optional()
  }).optional()
}, async (params) => {
  // Generate: executive summary, problem statement, proposed solution,
  // implementation timeline, ROI calculation, pricing table, next steps
  // Include: 3-year ROI model, payback period, risk mitigation section
  // Output: structured markdown + metadata for PDF generation
});

server.tool('objection_handle', 'Generate objection handling scripts', {
  objection: z.string().describe('The specific objection raised by prospect'),
  context: z.string().optional().describe('Stage in sales cycle, prospect profile'),
  style: z.enum(['feel_felt_found', 'question_back', 'data_backed', 'story']).default('question_back')
}, async ({ objection, context, style }) => {
  // Identify objection category: price, timing, competitor, status-quo, authority
  // Generate: acknowledge + respond + advance response
  // Include 2-3 discovery questions to uncover root concern
  // Provide competitor-specific rebuttals if competitor mentioned
  // Return: primary response + alternative approaches + follow-up questions
});

server.tool('forecast_update', 'Update pipeline forecast and deal probability', {
  pipeline: z.array(z.object({
    deal_name: z.string(),
    stage: z.string(),
    amount: z.number(),
    close_date: z.string(),
    last_activity_days: z.number(),
    qualification_score: z.number().min(0).max(10).optional()
  })),
  forecast_period: z.enum(['current_month', 'current_quarter', 'next_quarter']).default('current_quarter')
}, async ({ pipeline, forecast_period }) => {
  // Apply stage-based probability weights
  // Flag at-risk deals: no activity >14 days, pushed close dates, low qualification
  // Generate commit / best case / pipeline totals
  // Identify deals to accelerate vs cull
  // Return: forecast summary table + risk flags + recommended actions per deal
});
```

## Open Source Tools Powering This Server

| Tool | Purpose | GitHub | License |
|------|---------|--------|---------|
| [Apollo.io](https://apollo.io) | Prospect search, contact enrichment (250 free exports/mo) | SaaS free tier | Commercial |
| [Hunter.io](https://hunter.io) | Email discovery (25 free searches/mo) | SaaS free tier | Commercial |
| [Twenty CRM](https://github.com/twentyhq/twenty) | Open-source HubSpot alternative, full CRM backend | 25k+ stars | MIT |
| [Composio](https://github.com/ComposioHQ/composio) | CRM integrations (HubSpot, Salesforce, Pipedrive) | 18k+ stars | Apache 2.0 |
| [Langchain](https://github.com/langchain-ai/langchain) | LLM chains for copy generation | 95k+ stars | MIT |

## Environment Variables

```env
# Prospecting & Enrichment
APOLLO_API_KEY=...              # Apollo.io (free tier: 250 export credits/month)
HUNTER_API_KEY=...              # Hunter.io email finder (free: 25/month)

# CRM
TWENTY_API_URL=...              # Self-hosted Twenty CRM API URL (default: http://localhost:3000)
TWENTY_API_KEY=...              # Twenty CRM API key
COMPOSIO_API_KEY=...            # Composio for HubSpot/Salesforce/Pipedrive sync

# AI
ANTHROPIC_API_KEY=...           # For outreach copy generation

# Optional
HUBSPOT_ACCESS_TOKEN=...        # Direct HubSpot (if not using Composio)
SALESFORCE_ACCESS_TOKEN=...     # Direct Salesforce (if not using Composio)
```

## Example Usage

```typescript
// Find 25 VP Engineering prospects at Series A SaaS companies
await client.callTool('prospect_search', {
  industry: 'SaaS',
  role: 'VP of Engineering',
  funding_stage: 'series-a',
  company_size: '51-200',
  geography: ['United States'],
  limit: 25
});

// Write 3 variants of a personalized cold email
await client.callTool('outreach_write', {
  channel: 'email',
  prospect: {
    name: 'Sarah Chen',
    title: 'VP of Engineering',
    company: 'Acme Corp',
    industry: 'SaaS',
    recent_news: 'Just raised $8M Series A, hiring 20 engineers'
  },
  product: 'AI code review tool that reduces PR review time by 60%',
  icp_outcome: 'Ship faster without sacrificing code quality during hypergrowth',
  variants: 3
});

// Qualify a deal with MEDDIC
await client.callTool('deal_qualify', {
  framework: 'meddic',
  deal_notes: 'Discovery call 3/15: engineering team is 45 people, shipping 4x/week, CEO wants to 2x velocity...',
  deal_size: 24000
});
```

## Integration Notes

- **soloos-memory**: All prospect interactions and deal notes auto-saved via `business_context_save`; call `customer_insight_add` after every discovery call
- **soloos-marketing**: `outreach_write` pulls brand voice and ICP context from `brand_context_get`; use `email_sequence` for marketing nurtures vs this server's `sequence_build` for direct sales
- **soloos-product**: `deal_qualify` insights feed `user_research_analyze` for product-market fit signals
- **soloos-ops**: `proposal_generate` references financial models from `financial_model`; contracts go through `contract_review`
