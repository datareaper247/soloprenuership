# soloos-growth MCP Server

**Purpose**: Data-driven growth capabilities — experimentation, funnel analysis, retention, channel scoring, and viral mechanics.

## TypeScript Server Definition

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'soloos-growth',
  version: '1.0.0',
  description: 'Growth engineering for solo founders — experiments, funnels, retention, viral loops'
});

// ─── EXPERIMENTATION ──────────────────────────

server.tool('experiment_design', 'Design a rigorous A/B experiment with full statistical setup', {
  hypothesis: z.string().describe('If we change X, then Y will improve because Z'),
  metric: z.string().describe('Primary metric to measure (e.g. "signup conversion rate")'),
  baseline_rate: z.number().describe('Current metric value as decimal (e.g. 0.04 for 4%)'),
  minimum_detectable_effect: z.number().default(0.20).describe('Smallest relative improvement worth detecting'),
  traffic_per_day: z.number().describe('Daily visitors/users exposed to experiment'),
  confidence_level: z.number().default(0.95),
  power: z.number().default(0.80)
}, async (params) => {
  // Calculate: required sample size per variant
  // Estimate: days to reach significance given traffic
  // Define: guardrail metrics (what must not degrade)
  // Specify: segmentation strategy, exclusion criteria
  // Flag: common pitfalls (novelty effect, seasonal bias, multi-armed bandit trade-offs)
  // Return: complete experiment brief — hypothesis, metrics, sample size, timeline, guardrails
});

server.tool('ab_test_analyze', 'Analyze A/B test results with statistical rigor', {
  control_visitors: z.number(),
  control_conversions: z.number(),
  variant_visitors: z.number(),
  variant_conversions: z.number(),
  test_duration_days: z.number(),
  confidence_level: z.number().default(0.95),
  secondary_metrics: z.array(z.object({
    name: z.string(),
    control_value: z.number(),
    variant_value: z.number()
  })).optional()
}, async (params) => {
  // Calculate: conversion rates, relative uplift, absolute uplift
  // Statistical significance: chi-square or z-test, p-value, confidence interval
  // Business impact: annualized revenue impact at current scale
  // Segment breakdown if provided
  // Recommendation: ship / iterate / stop with rationale
  // Return: statistical summary + business impact + decision recommendation
});

server.tool('pricing_experiment', 'Design a pricing page experiment', {
  current_pricing: z.array(z.object({
    tier: z.string(),
    price: z.number(),
    billing: z.enum(['monthly', 'annual'])
  })),
  goal: z.enum(['increase_arpu', 'increase_conversion', 'reduce_churn', 'push_annual']),
  product: z.string(),
  avg_deal_size: z.number().optional()
}, async (params) => {
  // Generate 2-3 pricing experiment variants based on goal
  // Variant ideas: anchor pricing, feature repackaging, price increase test, freemium toggle
  // Define: success metrics, segment targeting, holdout strategy
  // Warn: pricing experiments require careful rollout (existing customer impact)
  // Return: variant designs + measurement plan + rollback criteria
});

// ─── FUNNEL ANALYSIS ──────────────────────────

server.tool('funnel_analyze', 'Analyze conversion funnel and identify drop-off points', {
  funnel_steps: z.array(z.object({
    step_name: z.string(),
    users: z.number(),
    step_type: z.enum(['awareness', 'acquisition', 'activation', 'retention', 'revenue', 'referral']).optional()
  })),
  timeframe_days: z.number().default(30),
  segment: z.string().optional().describe('e.g. "organic", "paid", "mobile users"')
}, async (params) => {
  // Calculate: step-by-step conversion rates and cumulative conversion
  // Identify: biggest absolute and relative drop-off points (Pareto analysis)
  // Benchmark against SaaS industry medians (Sequoia / OpenView / Lenny benchmarks)
  // Root cause hypotheses for top 3 drop-off points
  // Prioritized fix recommendations with estimated conversion impact
  // Return: funnel visualization data + drop-off analysis + improvement priorities
});

server.tool('cohort_analyze', 'Retention cohort analysis to understand user lifecycle', {
  cohort_data: z.array(z.object({
    cohort_month: z.string().describe('e.g. "2024-01"'),
    initial_users: z.number(),
    retained_by_month: z.array(z.number()).describe('Users retained at month 1, 2, 3... N')
  })),
  product_type: z.enum(['saas', 'consumer', 'marketplace', 'mobile_app']).default('saas'),
  revenue_per_user: z.number().optional()
}, async (params) => {
  // Build: standard retention cohort matrix (rows = cohorts, cols = months since signup)
  // Calculate: D1, D7, D30 retention rates; M1, M3, M6, M12 for SaaS
  // LTV projection: revenue-weighted cohort curves
  // Identify: cohort quality trends — is retention improving or degrading over time?
  // Flag: smile vs cliff vs plateau retention curve pattern with implications
  // Return: cohort matrix + trend analysis + LTV projections + improvement levers
});

// ─── GROWTH MECHANICS ─────────────────────────

server.tool('viral_loop_design', 'Design referral and viral growth mechanics', {
  product: z.string(),
  current_acquisition_channels: z.array(z.string()),
  product_type: z.enum(['b2b_saas', 'b2c_app', 'marketplace', 'developer_tool']),
  existing_user_base: z.number().optional(),
  viral_coefficient_target: z.number().default(0.3).describe('Target K-factor (> 1 = viral)')
}, async (params) => {
  // Select appropriate viral loop type: word-of-mouth, product-led, collaboration, referral program
  // For each mechanic: design the loop, trigger point, incentive structure, friction removal
  // Calculate: viral coefficient formula and target K-factor milestones
  // Prioritize by: implementation effort vs potential K-factor impact
  // Case studies from similar product types
  // Return: 3-5 viral mechanic concepts + implementation roadmap + K-factor model
});

server.tool('retention_campaign', 'Design retention and win-back campaigns', {
  campaign_type: z.enum(['onboarding', 'feature_adoption', 'at_risk', 'churned_winback', 'expansion']),
  segment: z.string().describe('Who this campaign targets'),
  product: z.string(),
  trigger_criteria: z.string().describe('What behavior/event triggers this campaign'),
  available_channels: z.array(z.enum(['email', 'in_app', 'push', 'sms', 'sales_touch'])).default(['email', 'in_app'])
}, async (params) => {
  // Design multi-touch campaign with: trigger, timing, message per touch, channel
  // Onboarding: activation milestone sequence
  // At-risk: usage drop detection + intervention sequence
  // Win-back: multi-wave outreach with increasing incentives
  // Include: subject lines, in-app copy, CTA hierarchy
  // Success metrics: reactivation rate, time-to-reactivate, incremental revenue
  // Return: campaign blueprint + copy for each touchpoint + measurement plan
});

// ─── CHANNEL & STRATEGY ───────────────────────

server.tool('channel_score', 'Score acquisition channels across CAC, conversion rate, and scalability', {
  channels: z.array(z.object({
    name: z.string(),
    monthly_spend: z.number().optional(),
    monthly_signups: z.number().optional(),
    monthly_customers: z.number().optional(),
    notes: z.string().optional()
  })),
  avg_contract_value: z.number(),
  ltv: z.number().optional()
}, async (params) => {
  // Calculate per channel: CAC, conversion rate (visitor to customer), LTV:CAC ratio
  // Score each on 5 dimensions: CAC efficiency, conversion quality, scalability, payback speed, brand fit
  // Identify: star channels (high ROI + scalable) vs dogs (high cost, low scale)
  // Portfolio recommendation: where to double down, test, or cut
  // Return: channel scorecard + portfolio allocation recommendation + next experiments
});

server.tool('growth_model', 'Project growth scenarios with compound model', {
  current_mrr: z.number(),
  current_customers: z.number(),
  months_to_project: z.number().default(12),
  assumptions: z.object({
    new_customers_per_month: z.number(),
    monthly_churn_rate: z.number().describe('As decimal'),
    expansion_revenue_rate: z.number().default(0.02).describe('Monthly expansion as % of MRR'),
    avg_contract_value: z.number()
  }),
  scenarios: z.array(z.enum(['conservative', 'base', 'optimistic'])).default(['conservative', 'base', 'optimistic'])
}, async (params) => {
  // Month-by-month model: new MRR, churn MRR, expansion MRR, net new MRR, cumulative MRR
  // For each scenario: growth multiplier applied to new customers assumption
  // Key milestones: when does $10K/$50K/$100K MRR get hit per scenario?
  // Sensitivity analysis: which lever (churn vs acquisition vs expansion) moves the needle most?
  // Return: monthly table per scenario + milestone dates + sensitivity table
});

server.tool('north_star_define', 'Define the north star metric and driver tree', {
  product: z.string(),
  product_type: z.enum(['b2b_saas', 'b2c_app', 'marketplace', 'developer_tool', 'media']),
  business_model: z.enum(['subscription', 'usage_based', 'transactional', 'advertising', 'freemium']),
  current_focus: z.enum(['growth', 'retention', 'monetization', 'acquisition']).default('growth'),
  existing_metrics: z.array(z.string()).optional()
}, async (params) => {
  // Propose 2-3 north star metric candidates with trade-off analysis
  // For chosen NSM: build L1/L2/L3 driver tree
  // L1: NSM directly (e.g. weekly active paying accounts)
  // L2: drivers that move L1 (activation rate, retention rate, expansion rate)
  // L3: levers that move each L2 (onboarding completion, feature adoption, seat adds)
  // Map which team owns each lever
  // Return: NSM recommendation + driver tree diagram data + ownership matrix
});
```

## Open Source Tools Powering This Server

| Tool | Purpose | GitHub | License |
|------|---------|--------|---------|
| [PostHog](https://github.com/PostHog/posthog) | Self-hosted product analytics, funnels, cohorts, A/B tests | 25k+ stars | MIT/Enterprise |
| [GrowthBook](https://github.com/growthbook/growthbook) | Open-source feature flags and A/B testing | 6k+ stars | MIT |
| [Metabase](https://github.com/metabase/metabase) | Self-hosted BI for cohort and funnel queries | 38k+ stars | AGPL 3.0 |
| [OpenStats](https://github.com/opensearch-project/OpenSearch) | Analytics aggregation layer | — | Apache 2.0 |
| [Scipy / Statsmodels](https://github.com/statsmodels/statsmodels) | Statistical significance calculations | 10k+ stars | BSD |

## Environment Variables

```env
# Product Analytics
POSTHOG_API_KEY=...              # PostHog project API key
POSTHOG_HOST=...                 # Self-hosted: https://your-posthog.com

# Experimentation
GROWTHBOOK_API_KEY=...           # GrowthBook for feature flags + A/B tests
GROWTHBOOK_CLIENT_KEY=...        # Frontend SDK key

# BI / Data
METABASE_URL=...                 # Self-hosted Metabase URL
METABASE_API_KEY=...

# AI
ANTHROPIC_API_KEY=...            # For experiment design and recommendation generation

# Optional — direct data sources
POSTGRES_CONNECTION_STRING=...   # Direct DB access for funnel queries
STRIPE_SECRET_KEY=...            # Revenue data for cohort analysis
```

## Example Usage

```typescript
// Design an A/B test on the signup page
await client.callTool('experiment_design', {
  hypothesis: 'If we replace the generic CTA with a personalized one based on job role, signup conversion will improve because relevance increases motivation',
  metric: 'signup_conversion_rate',
  baseline_rate: 0.04,
  minimum_detectable_effect: 0.25,
  traffic_per_day: 500,
  confidence_level: 0.95
});

// Analyze a completed A/B test
await client.callTool('ab_test_analyze', {
  control_visitors: 4500,
  control_conversions: 180,
  variant_visitors: 4500,
  variant_conversions: 234,
  test_duration_days: 14,
  confidence_level: 0.95
});

// Analyze a leaky signup funnel
await client.callTool('funnel_analyze', {
  funnel_steps: [
    { step_name: 'Landing page visit', users: 10000 },
    { step_name: 'Signup page', users: 1200 },
    { step_name: 'Account created', users: 400 },
    { step_name: 'Onboarding complete', users: 140 },
    { step_name: 'First value action', users: 55 },
    { step_name: 'Paid conversion', users: 18 }
  ],
  timeframe_days: 30
});

// Project 12-month growth scenarios
await client.callTool('growth_model', {
  current_mrr: 8500,
  current_customers: 42,
  months_to_project: 12,
  assumptions: {
    new_customers_per_month: 8,
    monthly_churn_rate: 0.025,
    expansion_revenue_rate: 0.015,
    avg_contract_value: 199
  }
});
```

## Integration Notes

- **soloos-memory**: Experiment results saved via `business_context_save` with category "experiments"; track metric trends with `metric_track` (MRR, churn, activation rate)
- **soloos-marketing**: `channel_score` inputs come from marketing channel spend tracked in soloos-marketing; `retention_campaign` copy generated using marketing email tools
- **soloos-ops**: `growth_model` projections feed `financial_model` in soloos-ops for board-level reporting
- **soloos-product**: `funnel_analyze` drop-off points become input for `feature_prioritize`; `cohort_analyze` LTV curves inform pricing strategy
- **soloos-sales**: `north_star_define` driver tree syncs with sales pipeline targets; `channel_score` informs sales vs PLG investment split
