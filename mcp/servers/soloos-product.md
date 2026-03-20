# soloos-product MCP Server

**Purpose**: Full product management capabilities — PRDs, user stories, feature prioritization, roadmaps, OKRs, NPS analysis, and competitive feature mapping.

## TypeScript Server Definition

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'soloos-product',
  version: '1.0.0',
  description: 'Product management intelligence for solo founders — strategy, planning, and execution'
});

// ─── REQUIREMENTS ─────────────────────────────

server.tool('prd_create', 'Create a Product Requirements Document', {
  feature_name: z.string(),
  problem_statement: z.string().describe('The user problem being solved'),
  target_users: z.string().describe('Which user segment this is for'),
  success_metrics: z.array(z.string()).describe('How success will be measured, e.g. "activation rate +10%"'),
  constraints: z.array(z.string()).optional().describe('Technical, legal, or business constraints'),
  out_of_scope: z.array(z.string()).optional(),
  background_context: z.string().optional().describe('Customer research, support tickets, competitor info that drove this'),
  target_release: z.string().optional().describe('Target quarter or date')
}, async (params) => {
  // Generate full PRD structure:
  // 1. Overview: problem, opportunity, target user, success metrics
  // 2. Background: research summary, customer evidence, business case
  // 3. User stories: core user stories in job-to-be-done format
  // 4. Functional requirements: numbered requirements list with priority (must/should/could)
  // 5. Non-functional requirements: performance, security, accessibility
  // 6. UX considerations: key flows, edge cases, empty states
  // 7. Open questions: unresolved decisions needing input
  // 8. Out of scope: explicit exclusions
  // Return: complete PRD in structured markdown
});

server.tool('user_story_write', 'Write user stories with acceptance criteria', {
  feature: z.string(),
  user_types: z.array(z.string()).describe('e.g. ["admin", "end user", "guest"]'),
  job_to_be_done: z.string().describe('The underlying goal: "Help me do X so I can achieve Y"'),
  story_count: z.number().default(5),
  include_edge_cases: z.boolean().default(true)
}, async (params) => {
  // Generate user stories in format: "As a [user type], I want [action] so that [benefit]"
  // For each story: 3-5 acceptance criteria in Given/When/Then format
  // Include: happy path stories + error/edge case stories
  // Add: story point estimate (Fibonacci) and complexity notes
  // Flag: dependencies between stories, technical assumptions
  // Return: formatted user story card set ready for Linear/Jira import
});

// ─── PRIORITIZATION ───────────────────────────

server.tool('feature_prioritize', 'Score and prioritize features using structured frameworks', {
  framework: z.enum(['rice', 'ice', 'value_effort', 'kano', 'opportunity_scoring']).default('rice'),
  features: z.array(z.object({
    name: z.string(),
    description: z.string(),
    reach: z.number().optional().describe('RICE: users affected per quarter'),
    impact: z.number().min(1).max(3).optional().describe('RICE/ICE: 0.25/0.5/1/2/3x multiplier'),
    confidence: z.number().min(1).max(100).optional().describe('RICE/ICE: % confidence 1-100'),
    effort: z.number().optional().describe('RICE: person-weeks; Value/Effort: 1-10'),
    value: z.number().optional().describe('Value/Effort: 1-10 business value'),
    customer_evidence: z.number().optional().describe('Number of customers requesting this')
  })),
  strategic_goals: z.array(z.string()).optional().describe('Current quarter OKRs to weight against')
}, async (params) => {
  // Calculate RICE/ICE/etc. scores for each feature
  // Rank by score, then overlay strategic alignment to OKRs
  // Identify: quick wins (high score, low effort) vs strategic bets vs time sinks
  // Flag: features with low evidence count — need more validation before building
  // Return: prioritized list with scores + recommendation matrix + roadmap sequencing
});

server.tool('competitor_feature_map', 'Map feature coverage versus competitors', {
  product_name: z.string(),
  features: z.array(z.string()).describe('Your current and planned features'),
  competitors: z.array(z.object({
    name: z.string(),
    notes: z.string().optional()
  })),
  focus_area: z.string().optional().describe('e.g. "enterprise features", "collaboration"')
}, async (params) => {
  // Build competitive feature matrix: rows = features, cols = products
  // Scoring: Full (✓) / Partial (◑) / Missing (✗) per competitor per feature
  // Identify: features unique to you (differentiators) and parity gaps (table stakes missing)
  // Segment by impact: high-stakes gaps vs low-priority misses
  // Surface: features all competitors have but you don't (table stakes risk)
  // Return: feature matrix table + gap analysis + differentiation summary + build priority recommendations
});

// ─── RESEARCH & ANALYSIS ──────────────────────

server.tool('user_research_analyze', 'Analyze user research data and surface patterns', {
  research_data: z.string().describe('Raw interview notes, survey responses, usability study findings'),
  research_type: z.enum(['interviews', 'usability_test', 'survey', 'support_tickets', 'session_recordings', 'mixed']),
  research_question: z.string().describe('What question did this research aim to answer?'),
  participant_count: z.number().optional()
}, async (params) => {
  // Affinity mapping: cluster insights into themes
  // Jobs-to-be-done extraction: functional, social, emotional jobs
  // Pain point inventory: prioritized by frequency and severity
  // Opportunity statements: convert pains to "How Might We" statements
  // Confidence level: how strongly does evidence support each finding?
  // Return: thematic analysis + JTBD map + prioritized opportunities + evidence strength
});

server.tool('nps_analyze', 'Analyze NPS survey results and extract actionable insights', {
  responses: z.array(z.object({
    score: z.number().min(0).max(10),
    comment: z.string().optional(),
    segment: z.string().optional().describe('e.g. customer plan, signup date range')
  })),
  compare_to_previous_nps: z.number().optional().describe('Previous period NPS score')
}, async (params) => {
  // Calculate NPS score: % Promoters (9-10) minus % Detractors (0-6)
  // Sentiment analysis on open-text comments
  // Theme clustering: what promoters love, what detractors hate, passives' unmet needs
  // Segment analysis: NPS by plan, cohort, feature usage
  // Driver analysis: what most differentiates promoters from detractors?
  // Action items: specific product changes mapped to detractor themes
  // Return: NPS score + benchmark comparison + theme breakdown + top 5 action items
});

// ─── PLANNING ─────────────────────────────────

server.tool('roadmap_generate', 'Generate a product roadmap from prioritized features', {
  features: z.array(z.object({
    name: z.string(),
    priority_score: z.number(),
    effort_weeks: z.number(),
    dependencies: z.array(z.string()).optional()
  })),
  team_size: z.number().default(1).describe('Number of engineers'),
  quarters_to_plan: z.number().default(2),
  strategic_themes: z.array(z.string()).optional().describe('e.g. ["Enterprise Readiness", "Core UX Polish"]'),
  now_next_later: z.boolean().default(true).describe('Use Now/Next/Later format instead of quarterly')
}, async (params) => {
  // Schedule features into quarters/weeks respecting dependency order
  // Balance: quick wins vs strategic investments per quarter
  // Flag: capacity conflicts, dependency bottlenecks, critical path
  // Output formats: Now/Next/Later swim lanes OR quarterly Gantt
  // Include: theme headers for each bucket to communicate strategy
  // Return: roadmap structure + capacity utilization + dependency graph + communication summary
});

server.tool('okr_create', 'Create OKRs aligned to company strategy', {
  company_mission: z.string(),
  timeframe: z.enum(['quarterly', 'annual']).default('quarterly'),
  focus_areas: z.array(z.string()).describe('Top 2-4 strategic priorities for the period'),
  current_metrics: z.record(z.string(), z.number()).optional().describe('Baseline metrics: {mrr: 10000, nps: 32}'),
  team_size: z.number().default(1)
}, async (params) => {
  // Generate 3-5 Objectives with 2-4 Key Results each
  // Key Results: measurable, time-bound, ambitious but achievable
  // Cascade: company OKRs → product OKRs → engineering OKRs
  // Include: initiative suggestions under each KR
  // Flag: anti-patterns — output-based KRs, too many objectives, vague metrics
  // Return: OKR tree + scoring rubric + weekly check-in cadence template
});

// ─── COMMUNICATION ────────────────────────────

server.tool('changelog_write', 'Write user-facing product changelog entries', {
  changes: z.array(z.object({
    type: z.enum(['new', 'improved', 'fixed', 'removed', 'security']),
    technical_description: z.string().describe('Engineering description of the change'),
    affected_users: z.string().optional()
  })),
  tone: z.enum(['formal', 'friendly', 'developer']).default('friendly'),
  include_header: z.boolean().default(true),
  date: z.string().optional()
}, async (params) => {
  // Transform technical changelog into user-benefit language
  // Group by: New Features / Improvements / Bug Fixes / Security
  // Headline each item with the user benefit, not the implementation
  // Add emoji icons for visual scanning (optional based on tone)
  // Include: upgrade note if breaking changes present
  // Return: formatted changelog entry for website/email/ProductHunt

});

server.tool('ab_feature_plan', 'Plan a feature A/B test (staged rollout + measurement)', {
  feature_name: z.string(),
  hypothesis: z.string(),
  target_metric: z.string(),
  baseline_metric_value: z.number(),
  rollout_strategy: z.enum(['percentage', 'segment', 'opt_in', 'shadow']).default('percentage'),
  feature_flag_tool: z.enum(['growthbook', 'posthog', 'launchdarkly', 'custom']).default('growthbook')
}, async (params) => {
  // Design: rollout phases (5% → 25% → 50% → 100%)
  // Define: per-phase success criteria and exit conditions
  // Specify: feature flag configuration for chosen tool
  // Guardrails: what metrics trigger rollback?
  // Monitoring: dashboards and alerts to set up
  // Return: rollout plan + feature flag config + monitoring checklist + rollback runbook
});
```

## Open Source Tools Powering This Server

| Tool | Purpose | GitHub | License |
|------|---------|--------|---------|
| [Linear](https://linear.app) | Issue tracking, roadmap (API for story import) | SaaS | Commercial |
| [Plane](https://github.com/makeplane/plane) | Open-source Linear alternative for roadmaps | 30k+ stars | AGPL 3.0 |
| [GrowthBook](https://github.com/growthbook/growthbook) | Feature flags for staged rollout | 6k+ stars | MIT |
| [PostHog](https://github.com/PostHog/posthog) | NPS surveys, product analytics, session recordings | 25k+ stars | MIT/Enterprise |
| [Typeform API](https://developer.typeform.com) | Pull NPS/survey responses programmatically | — | Commercial free tier |
| [Langchain](https://github.com/langchain-ai/langchain) | LLM chains for research analysis and doc generation | 95k+ stars | MIT |

## Environment Variables

```env
# Issue Tracking
LINEAR_API_KEY=...              # Linear API for creating issues from user stories
PLANE_API_KEY=...               # Plane (OSS alternative) API key

# Feature Flags
GROWTHBOOK_API_KEY=...          # GrowthBook for feature flags + A/B testing
GROWTHBOOK_CLIENT_KEY=...       # Frontend SDK key

# Analytics & Research
POSTHOG_API_KEY=...             # PostHog for NPS data and product analytics
POSTHOG_HOST=...                # Self-hosted PostHog URL
TYPEFORM_API_KEY=...            # Pull NPS/survey responses from Typeform

# AI
ANTHROPIC_API_KEY=...           # PRD generation, research analysis

# Optional
NOTION_API_KEY=...              # Sync PRDs to Notion
CONFLUENCE_API_KEY=...          # Alternative doc sync
FIGMA_ACCESS_TOKEN=...          # Pull design links into PRDs
```

## Example Usage

```typescript
// Create a PRD for a new feature
await client.callTool('prd_create', {
  feature_name: 'Magic Link Authentication',
  problem_statement: '40% of users drop off on the password reset flow. Password fatigue causing failed logins and churn.',
  target_users: 'All users, especially occasional users who forget passwords',
  success_metrics: [
    'Login success rate +15%',
    'Password reset support tickets -50%',
    'Time-to-login -30%'
  ],
  constraints: ['Must support existing session management', 'Email deliverability < 5 second SLA'],
  target_release: 'Q2 2025'
});

// Prioritize 6 features using RICE
await client.callTool('feature_prioritize', {
  framework: 'rice',
  features: [
    { name: 'Magic Link Auth', description: 'Passwordless login via email', reach: 500, impact: 2, confidence: 80, effort: 2 },
    { name: 'CSV Export', description: 'Export data to CSV', reach: 200, impact: 1, confidence: 90, effort: 1 },
    { name: 'Slack Integration', description: 'Send notifications to Slack', reach: 400, impact: 1, confidence: 70, effort: 3 }
  ],
  strategic_goals: ['Reduce churn by improving activation', 'Expand enterprise features']
});

// Create Q2 OKRs
await client.callTool('okr_create', {
  company_mission: 'Make engineering teams ship faster without sacrificing quality',
  timeframe: 'quarterly',
  focus_areas: ['Activation', 'Enterprise readiness', 'Retention'],
  current_metrics: { mrr: 18500, activation_rate: 0.38, nps: 28 }
});

// Analyze 50 NPS responses
await client.callTool('nps_analyze', {
  responses: [
    { score: 9, comment: 'Love the speed, transformed our code review process', segment: 'pro' },
    { score: 3, comment: 'Too expensive for our small team', segment: 'starter' },
    // ...more responses
  ],
  compare_to_previous_nps: 22
});
```

## Integration Notes

- **soloos-memory**: PRDs saved via `business_context_save` category "strategy"; user research insights → `customer_insight_add`; OKRs → `decision_log` with tags ["product", "okr"]
- **soloos-growth**: `feature_prioritize` feeds `experiment_design` for feature A/B tests; NPS analysis feeds `cohort_analyze` segmentation
- **soloos-engineering**: `prd_create` output is the input to `api_design` and `architecture_review`; `user_story_write` stories map directly to engineering tickets
- **soloos-sales**: `competitor_feature_map` gaps feed `objection_handle` scripts; feature announcements from `changelog_write` used in sales outreach
- **soloos-ops**: `okr_create` informs `hiring_package` for headcount planning against OKR capacity needs
