# soloos-swarm MCP Server

**Purpose**: The orchestrator — runs multi-agent company simulations using all other SoloOS MCPs.

This is the "unlock" server. It turns your agent CLI into a company.

## TypeScript Server Definition

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'soloos-swarm',
  version: '1.0.0',
  description: 'Multi-agent company orchestration — runs your AI workforce'
});

// ─── SWARM LAUNCH ─────────────────────────────

server.tool(
  'swarm_launch',
  'Launch a multi-agent swarm to complete a company-level task',
  {
    task: z.string().describe('High-level task for the swarm to complete'),
    swarm_type: z.enum([
      'product_launch',      // CMO + SEO + Content + Sales + DevRel
      'market_research',     // Market + Competitor + Validation + Strategy
      'growth_sprint',       // SEO + Content + Growth + Sales + Analytics
      'go_to_market',        // CMO + Sales + Marketing + Content
      'due_diligence',       // Research + Finance + Legal + Strategy
      'weekly_ops',          // All ops agents for weekly tasks
      'custom'               // Define your own agent combination
    ]),
    agents: z.array(z.string()).optional().describe('For custom swarm: list of agent roles'),
    output_format: z.enum(['brief', 'detailed', 'actionable']).default('actionable'),
    parallel: z.boolean().default(true).describe('Run agents in parallel where possible')
  },
  async ({ task, swarm_type, agents, output_format, parallel }) => {
    const swarmConfig = SWARM_CONFIGS[swarm_type] || buildCustomSwarm(agents);

    // Phase 1: Parallel research/analysis
    // Phase 2: Synthesis
    // Phase 3: Actionable output

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          task,
          swarm_type,
          agents_used: swarmConfig.agents,
          outputs: {}, // Per-agent outputs
          synthesis: '', // Combined insight
          actions: [], // Prioritized next steps
          timeline: '' // Suggested execution timeline
        })
      }]
    };
  }
);

// Pre-defined swarm configurations
const SWARM_CONFIGS = {
  product_launch: {
    agents: ['cmo', 'seo_specialist', 'content_marketer', 'sdr', 'developer_relations'],
    phases: [
      {
        name: 'Strategy',
        parallel: ['cmo'],
        output: 'launch_strategy'
      },
      {
        name: 'Execution Prep',
        parallel: ['seo_specialist', 'content_marketer', 'sdr'],
        depends_on: 'launch_strategy',
        output: ['keyword_list', 'content_pieces', 'prospect_list']
      },
      {
        name: 'Go-Live',
        sequential: ['publisher', 'outreach_sender'],
        depends_on: ['content_pieces', 'prospect_list'],
        output: 'launch_report'
      }
    ]
  },

  market_research: {
    agents: ['market_researcher', 'competitor_analyst', 'validation_researcher', 'ceo'],
    phases: [
      {
        name: 'Data Gathering',
        parallel: ['market_researcher', 'competitor_analyst', 'validation_researcher'],
        output: ['market_data', 'competitor_data', 'validation_data']
      },
      {
        name: 'Synthesis',
        sequential: ['ceo'],
        depends_on: ['market_data', 'competitor_data', 'validation_data'],
        output: 'opportunity_brief'
      }
    ]
  },

  growth_sprint: {
    agents: ['seo_specialist', 'content_marketer', 'growth_hacker', 'sdr', 'data_analyst'],
    phases: [
      {
        name: 'Analysis',
        parallel: ['data_analyst', 'seo_specialist'],
        output: ['metrics_brief', 'keyword_opportunities']
      },
      {
        name: 'Execution',
        parallel: ['content_marketer', 'growth_hacker', 'sdr'],
        depends_on: ['metrics_brief', 'keyword_opportunities'],
        output: ['content_pieces', 'experiments', 'outreach']
      }
    ]
  }
};

// ─── COMPANY AUTOPILOT ────────────────────────

server.tool(
  'autopilot_configure',
  'Set up recurring autonomous company operations',
  {
    operation: z.enum([
      'weekly_content',        // Publish 2 SEO posts/week
      'competitor_monitor',    // Weekly competitor brief
      'lead_nurture',          // Automated follow-up sequences
      'retention_monitor',     // Flag at-risk customers
      'growth_experiments',    // Weekly A/B experiment cycle
      'financial_review',      // Monthly financial brief
      'custom'
    ]),
    schedule: z.string().describe('Cron expression: "0 9 * * 1" = Monday 9am'),
    config: z.record(z.any()).optional()
  },
  async ({ operation, schedule, config }) => {
    // Register recurring task in scheduler
    // Returns: confirmation + next run time
  }
);

server.tool(
  'parallel_race',
  'Run N agents on same task, return best result',
  {
    task: z.string(),
    agents: z.array(z.string()).describe('Agents to race'),
    selection_criteria: z.string().describe('How to pick the winner'),
    return_all: z.boolean().default(false)
  },
  async ({ task, agents, selection_criteria, return_all }) => {
    // Run all agents in parallel
    // Score each output against selection criteria
    // Return winner (or all if return_all)
  }
);

// ─── ROLE INVOKER ─────────────────────────────

server.tool(
  'invoke_role',
  'Instantly adopt a professional role for the current task',
  {
    role: z.enum([
      // Leadership
      'ceo', 'cto', 'cmo', 'cfo', 'coo',
      // Engineering
      'frontend_engineer', 'backend_engineer', 'devops_engineer',
      'mobile_engineer', 'ml_engineer', 'security_engineer',
      'qa_engineer', 'data_engineer',
      // Product
      'product_manager', 'product_designer', 'ux_researcher',
      'technical_writer',
      // Marketing
      'content_marketer', 'seo_specialist', 'sem_manager',
      'social_media_manager', 'email_marketer', 'community_manager',
      'pr_manager', 'growth_marketer', 'video_producer',
      // Sales
      'sdr', 'account_executive', 'sales_engineer',
      'customer_success', 'revenue_ops',
      // Operations
      'hr_manager', 'finance_manager', 'legal_counsel',
      'compliance_officer', 'business_analyst',
      // Customer
      'customer_support', 'technical_support', 'onboarding_specialist',
      // Growth/Analytics
      'data_analyst', 'growth_hacker', 'cro_specialist',
      // Geo
      'localization_manager', 'international_market_manager',
      // Partnerships
      'business_development', 'partnership_manager'
    ]),
    task: z.string().describe('What you need this role to do'),
    context: z.string().optional()
  },
  async ({ role, task, context }) => {
    // Load role system prompt from SoloOS roles library
    // Apply role context to task
    // Return: role-framed response with professional methodology
  }
);

// ─── WORKFLOW ENGINE ──────────────────────────

server.tool(
  'workflow_run',
  'Execute a pre-built or custom business workflow',
  {
    workflow: z.string().describe('Workflow name from library or custom YAML'),
    inputs: z.record(z.any()).describe('Workflow input parameters'),
    dry_run: z.boolean().default(false)
  },
  async ({ workflow, inputs, dry_run }) => {
    // Load workflow definition
    // Validate inputs
    // Execute step by step (or dry run to show plan)
    // Return: workflow output + execution summary
  }
);
```

## Pre-Built Swarm Templates

### Product Launch Swarm
```yaml
# templates/swarms/product-launch.yaml
name: product-launch
description: "Full product launch in parallel"
estimated_time: "2-4 hours human review"

agents:
  strategy_phase:
    - role: cmo
      task: "Create go-to-market strategy for {product}"

  execution_phase:
    parallel: true
    - role: seo_specialist
      task: "Research 50 target keywords for {product}"
      depends_on: strategy_phase

    - role: content_marketer
      task: "Create 5 launch content pieces"
      depends_on: strategy_phase

    - role: sdr
      task: "Build prospect list of 200 {target_customer} and draft outreach"
      depends_on: strategy_phase

    - role: pr_manager
      task: "Write press release and identify 20 journalists to pitch"
      depends_on: strategy_phase

  review:
    role: ceo
    task: "Review all outputs, flag inconsistencies, produce launch plan"
    depends_on: execution_phase
```

### Weekly Operations Swarm
```yaml
# templates/swarms/weekly-ops.yaml
name: weekly-ops
description: "Monday morning company briefing and week setup"
schedule: "0 8 * * 1"

agents:
  parallel:
    - role: data_analyst
      task: "Pull last week metrics, flag anomalies"

    - role: content_marketer
      task: "Publish this week's scheduled content, report last week's performance"

    - role: sdr
      task: "Send follow-ups, update CRM, surface warm leads"

    - role: seo_specialist
      task: "Weekly rank check, flag movements, suggest actions"

    - role: customer_success
      task: "Check at-risk accounts, draft win-back for churned"

  synthesis:
    role: coo
    task: "Compile weekly ops brief: wins, risks, actions required"
    format: "5 bullets, human review 15 min"
```

## Why This Is the Unlock

The `invoke_role` tool is the single most powerful feature in SoloOS:

```bash
# In Claude Code or any agent:
"Use soloos-swarm to invoke the SEO specialist role and research keywords for pharmacy audit software"

→ Agent immediately has:
  - SEO specialist system prompt
  - Keyword research methodology
  - Access to soloos-marketing SEO tools
  - Quality standards for SEO output
  - Professional deliverable format

# Without SoloOS: Generic AI response about SEO
# With SoloOS: Professional SEO brief with keyword data, difficulty scores, content opportunities
```

The gap is enormous. Role specialization + tools + methodology = professional output.
