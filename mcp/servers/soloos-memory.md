# soloos-memory MCP Server

**Purpose**: Persistent business intelligence across all agent sessions — decisions, metrics, customer insights, competitor tracking, and brand context. Powered by Mem0 (semantic memory layer).

## TypeScript Server Definition

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'soloos-memory',
  version: '1.0.0',
  description: 'Persistent business brain — remember everything across agent sessions'
});

// ─── BUSINESS CONTEXT ─────────────────────────

server.tool('business_context_save', 'Save business context — decisions, metrics, strategy, meeting notes', {
  category: z.enum([
    'decision', 'metric', 'strategy', 'customer_insight',
    'competitor', 'experiment', 'milestone', 'note', 'risk'
  ]),
  key: z.string().describe('Unique identifier, e.g. "pricing-decision-2025-03"'),
  value: z.string().describe('The content to store'),
  metadata: z.object({
    source: z.string().optional().describe('Where this came from: call, email, analysis'),
    confidence: z.enum(['high', 'medium', 'low']).optional(),
    related_keys: z.array(z.string()).optional(),
    expires_at: z.string().optional().describe('ISO date if this context has an expiry')
  }).optional(),
  tags: z.array(z.string()).optional()
}, async (params) => {
  // Store in Mem0 with semantic embeddings for fuzzy retrieval
  // Auto-link to related existing memories via embedding similarity
  // Deduplication: if similar memory exists, merge or version it
  // Return: memory_id + confirmation + auto-linked related memories
});

server.tool('business_context_get', 'Retrieve relevant business context for the current task', {
  query: z.string().describe('Natural language query, e.g. "what did we decide about pricing?"'),
  category: z.enum([
    'decision', 'metric', 'strategy', 'customer_insight',
    'competitor', 'experiment', 'milestone', 'note', 'risk', 'all'
  ]).default('all'),
  limit: z.number().default(5),
  recency_weight: z.number().min(0).max(1).default(0.3).describe('How much to weight recent vs relevant (0=pure semantic, 1=pure recent)')
}, async ({ query, category, limit, recency_weight }) => {
  // Mem0 semantic search: embed query, cosine similarity against stored memories
  // Hybrid ranking: semantic relevance + recency weighting
  // Filter by category if specified
  // Return: ranked memories with relevance scores + related context links
});

// ─── CUSTOMER INTELLIGENCE ────────────────────

server.tool('customer_insight_add', 'Add customer feedback, interview insights, or support signal', {
  source_type: z.enum(['interview', 'support_ticket', 'nps_response', 'review', 'churn_reason', 'sales_call', 'survey']),
  customer_segment: z.string().optional().describe('e.g. "Series A startup", "enterprise", "SMB"'),
  sentiment: z.enum(['positive', 'neutral', 'negative', 'mixed']),
  insight: z.string().describe('The raw insight or quote'),
  themes: z.array(z.string()).optional().describe('e.g. ["onboarding", "pricing", "missing-feature"]'),
  customer_id: z.string().optional(),
  date: z.string().optional().describe('ISO date of the interaction')
}, async (params) => {
  // Store insight with semantic embeddings
  // Auto-extract: pain points, feature requests, competitor mentions, praise signals
  // Cluster with similar insights for pattern building
  // Update theme frequency counters
  // Return: insight_id + auto-detected themes + similar insights count
});

server.tool('customer_insight_search', 'Search customer insights for patterns and evidence', {
  query: z.string().describe('e.g. "why do customers churn?", "what do people love about us?"'),
  source_types: z.array(z.enum(['interview', 'support_ticket', 'nps_response', 'review', 'churn_reason', 'sales_call', 'survey'])).optional(),
  sentiment: z.enum(['positive', 'neutral', 'negative', 'mixed', 'all']).default('all'),
  date_from: z.string().optional().describe('ISO date'),
  date_to: z.string().optional()
}, async (params) => {
  // Semantic search across all stored customer insights
  // Cluster results by theme
  // Frequency analysis: which themes appear most? Which are trending?
  // Quote selection: return most representative quotes per theme
  // Return: theme clusters + frequency counts + top quotes + trend direction
});

// ─── METRICS TRACKING ─────────────────────────

server.tool('metric_track', 'Record a business metric snapshot', {
  metric_name: z.string().describe('e.g. "mrr", "cac", "ltv", "churn_rate", "activation_rate"'),
  value: z.number(),
  unit: z.string().describe('e.g. "USD", "percent", "count", "days"'),
  period: z.string().describe('ISO date or period string, e.g. "2025-03" or "2025-03-15"'),
  dimension: z.string().optional().describe('Segment or dimension, e.g. "plan:pro", "channel:organic"'),
  notes: z.string().optional()
}, async (params) => {
  // Store metric point in time-series structure
  // Calculate: delta vs prior period
  // Flag: if metric crosses defined thresholds (set via business_context_save)
  // Maintain: rolling 7-day, 30-day, 90-day averages
  // Return: stored value + period delta + trend direction
});

server.tool('metric_get', 'Get latest metric values with trend analysis', {
  metric_names: z.array(z.string()).describe('List of metrics to retrieve'),
  periods_back: z.number().default(6).describe('How many periods of history to return'),
  include_trend: z.boolean().default(true),
  include_benchmark: z.boolean().default(true).describe('Include industry benchmark comparison')
}, async ({ metric_names, periods_back, include_trend, include_benchmark }) => {
  // Retrieve latest N periods for each metric
  // Trend analysis: MoM growth rate, acceleration/deceleration signal
  // Benchmark comparison: SaaS benchmarks (Lenny Rachitsky / OpenView data)
  // Anomaly detection: flag unusual spikes or drops
  // Return: metrics table + trend sparkline data + benchmark deltas + anomalies
});

// ─── DECISIONS ────────────────────────────────

server.tool('decision_log', 'Log an important business decision with full context', {
  decision: z.string().describe('What was decided'),
  rationale: z.string().describe('Why this decision was made'),
  alternatives_considered: z.array(z.string()).optional(),
  made_by: z.string().optional().describe('Who made the decision'),
  confidence: z.enum(['high', 'medium', 'low']).default('medium'),
  review_date: z.string().optional().describe('When to revisit this decision'),
  tags: z.array(z.string()).optional().describe('e.g. ["pricing", "product", "hiring"]')
}, async (params) => {
  // Store with full decision context
  // Auto-link to related decisions and context (similar topic embedding)
  // Create review reminder if review_date provided
  // Return: decision_id + related past decisions on same topic
});

server.tool('decision_search', 'Search past decisions by topic or context', {
  query: z.string().describe('e.g. "pricing decisions", "decisions about enterprise sales"'),
  date_from: z.string().optional(),
  tags: z.array(z.string()).optional(),
  include_rationale: z.boolean().default(true)
}, async (params) => {
  // Semantic search across all logged decisions
  // Return decisions with their rationale and context
  // Group related decisions chronologically
  // Flag: decisions pending review (past review_date)
  // Return: relevant decisions + rationale + timeline + pending reviews
});

// ─── COMPETITIVE INTELLIGENCE ─────────────────

server.tool('competitor_update', 'Update competitor intelligence profile', {
  competitor_name: z.string(),
  update_type: z.enum(['pricing_change', 'new_feature', 'funding', 'leadership', 'partnership', 'outage', 'review', 'general']),
  update: z.string().describe('What changed or was observed'),
  source: z.string().optional().describe('URL, source type'),
  significance: z.enum(['high', 'medium', 'low']).default('medium')
}, async (params) => {
  // Update competitor profile with timestamped change log
  // Flag high-significance changes for immediate attention
  // Auto-detect: pricing, feature, and positioning pattern shifts
  // Return: update_id + competitor profile summary + related past changes
});

server.tool('competitor_get', 'Get competitor profile and recent intelligence', {
  competitor_name: z.string().optional().describe('Specific competitor, or omit for all'),
  include_changes_days: z.number().default(30).describe('Include changes from last N days'),
  focus: z.enum(['pricing', 'features', 'positioning', 'company', 'all']).default('all')
}, async (params) => {
  // Return full competitor profile with timeline of changes
  // Highlight: recent significant changes
  // Compare: feature and pricing changes relative to your product
  // Return: competitor profiles + change log + strategic implications
});

// ─── BRAND CONTEXT ────────────────────────────

server.tool('brand_context_get', 'Get brand voice, positioning, and ICP context for content agents', {
  context_for: z.enum(['email', 'social', 'ads', 'website', 'sales_outreach', 'product_copy', 'all']).default('all'),
  include_icp: z.boolean().default(true),
  include_competitors: z.boolean().default(false)
}, async ({ context_for, include_icp, include_competitors }) => {
  // Retrieve: brand voice guidelines, tone, vocabulary dos/don'ts
  // Positioning: category, differentiation, key messages
  // ICP: ideal customer profile attributes, pain points, goals, language they use
  // Value proposition: primary + secondary
  // Competitors: positioning map and differentiation angles (if requested)
  // This is the context package injected into content agents at session start
  // Return: structured brand context object all agents can consume
});
```

## Open Source Tools Powering This Server

| Tool | Purpose | GitHub | License |
|------|---------|--------|---------|
| [Mem0](https://github.com/mem0ai/mem0) | Semantic memory layer with hybrid storage | 23k+ stars | Apache 2.0 |
| [Qdrant](https://github.com/qdrant/qdrant) | High-performance vector store for embeddings | 22k+ stars | Apache 2.0 |
| [PostgreSQL](https://github.com/postgres/postgres) | Structured storage for metrics, decisions | — | PostgreSQL |
| [Redis](https://github.com/redis/redis) | Caching, counters, leaderboards | 68k+ stars | BSD |
| [LlamaIndex](https://github.com/run-llama/llama_index) | Knowledge graph linking for related context | 40k+ stars | MIT |

## Environment Variables

```env
# Mem0 (open source — self-hosted or managed)
MEM0_API_KEY=...                # Mem0 managed cloud API key (or self-hosted)
MEM0_ORG_ID=...                 # Organization ID in Mem0

# Vector Store (if self-hosting Mem0)
QDRANT_URL=...                  # Qdrant server URL (default: http://localhost:6333)
QDRANT_API_KEY=...              # Qdrant API key (optional for local)
QDRANT_COLLECTION=soloos_memory # Collection name

# Relational DB — metrics time series + decision log
DATABASE_URL=...                # PostgreSQL connection string

# Cache
REDIS_URL=...                   # Redis connection string (default: redis://localhost:6379)

# AI
ANTHROPIC_API_KEY=...           # For theme extraction and insight summarization
OPENAI_API_KEY=...              # Mem0's embedding model (text-embedding-3-small)
```

## Example Usage

```typescript
// Save a pricing decision with full context
await client.callTool('decision_log', {
  decision: 'Move to usage-based pricing in Q2 2025',
  rationale: 'Enterprise customers on flat-rate plan outgrowing seats — 3 churned citing pricing inflexibility. Competitors Vercel and Linear already usage-based.',
  alternatives_considered: [
    'Add enterprise tier at $2K/month flat',
    'Keep seat-based, increase seat limit'
  ],
  confidence: 'medium',
  review_date: '2025-06-01',
  tags: ['pricing', 'monetization', 'enterprise']
});

// Add insight from a customer churn interview
await client.callTool('customer_insight_add', {
  source_type: 'churn_reason',
  customer_segment: 'Series A startup',
  sentiment: 'negative',
  insight: 'We loved the product but when we scaled to 25 engineers the per-seat pricing got too expensive. We switched to Linear which charges per active user.',
  themes: ['pricing', 'scalability', 'competitor-linear'],
  date: '2025-03-10'
});

// Track MRR at month end
await client.callTool('metric_track', {
  metric_name: 'mrr',
  value: 18500,
  unit: 'USD',
  period: '2025-03',
  notes: 'Added 6 new customers, lost 2 (pricing and sunset)'
});

// Get brand context before writing any marketing copy
await client.callTool('brand_context_get', {
  context_for: 'email',
  include_icp: true,
  include_competitors: true
});

// Surface all customer evidence for pricing pain
await client.callTool('customer_insight_search', {
  query: 'customers complaining about pricing or saying its too expensive',
  sentiment: 'negative'
});
```

## Integration Notes

- **All SoloOS Agents**: Call `business_context_get` at session start with query matching the agent's domain (e.g. "brand positioning and ICP" for marketing agents). Call `business_context_save` with category "note" before session ends.
- **soloos-sales**: Deal qualification insights → `customer_insight_add` with source_type "sales_call"; competitor mentions in calls → `competitor_update`
- **soloos-growth**: Experiment results → `business_context_save` category "experiment"; metric snapshots → `metric_track` after every analytics pull
- **soloos-marketing**: All content agents call `brand_context_get` first to ensure consistent voice and positioning
- **soloos-ops**: Financial model outputs → `metric_track` for projected vs actual tracking; compliance decisions → `decision_log`
- **soloos-product**: NPS insights → `customer_insight_add`; roadmap decisions → `decision_log` with tags ["product", "roadmap"]
- **soloos-geo**: Market entry decisions → `decision_log`; local competitor intel → `competitor_update` with country tag
