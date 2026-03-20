# soloos-ops MCP Server

**Purpose**: Business operations capabilities — SOPs, legal, finance, compliance, hiring, and process optimization for solo founders.

## TypeScript Server Definition

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'soloos-ops',
  version: '1.0.0',
  description: 'Operational intelligence for founders — legal, finance, compliance, hiring, process'
});

// ─── PROCESS & SOPs ───────────────────────────

server.tool('sop_create', 'Create a Standard Operating Procedure with step-by-step instructions', {
  process_name: z.string().describe('e.g. "Customer Onboarding", "Bug Triage", "Monthly Close"'),
  department: z.enum(['sales', 'engineering', 'support', 'marketing', 'finance', 'hr', 'operations']),
  trigger: z.string().describe('What event starts this process?'),
  inputs: z.array(z.string()).describe('Required inputs to begin the process'),
  outputs: z.array(z.string()).describe('Expected outputs / deliverables'),
  tools_used: z.array(z.string()).optional().describe('Software tools involved'),
  existing_notes: z.string().optional().describe('Rough notes to structure into SOP')
}, async (params) => {
  // Generate: purpose, scope, roles & responsibilities (RACI), prerequisites
  // Step-by-step instructions with decision branches
  // Error handling / escalation paths
  // Success metrics and review cadence
  // Output: structured markdown SOP + Notion-compatible format
});

server.tool('process_audit', 'Audit and optimize a business process for efficiency', {
  process_description: z.string().describe('Current process description or existing SOP'),
  pain_points: z.array(z.string()).optional(),
  volume_per_week: z.number().optional().describe('How many times this runs per week'),
  time_per_run_minutes: z.number().optional()
}, async (params) => {
  // Apply Lean / Six Sigma analysis: identify waste categories (TIMWOOD)
  // Calculate: automation potential score, bottleneck identification
  // Identify: manual steps that can be automated with tools
  // Benchmark: industry best practices for this process type
  // Return: current state analysis + optimized future state + tooling recommendations + ROI estimate
});

// ─── LEGAL & CONTRACTS ────────────────────────

server.tool('contract_review', 'Review contracts, flag risks, and suggest improvements', {
  contract_text: z.string().describe('Full contract text to review'),
  contract_type: z.enum(['nda', 'msa', 'saas_agreement', 'employment', 'contractor', 'vendor', 'partnership', 'other']),
  perspective: z.enum(['customer', 'vendor', 'employer', 'employee']).default('vendor'),
  critical_concerns: z.array(z.string()).optional().describe('Specific clauses you want flagged')
}, async ({ contract_text, contract_type, perspective, critical_concerns }) => {
  // Section-by-section risk analysis with severity: High/Medium/Low
  // Flag: unusual liability caps, IP assignment, non-compete, auto-renewal, indemnification
  // For SaaS: data processing, uptime SLAs, price change clauses, termination for convenience
  // Suggest specific redline language for each flagged clause
  // Note: not a substitute for legal counsel — always review with attorney for high-stakes contracts
  // Return: risk summary table + detailed clause-by-clause analysis + suggested redlines
});

server.tool('policy_generate', 'Generate company policies and legal documents', {
  policy_type: z.enum([
    'privacy_policy', 'terms_of_service', 'cookie_policy',
    'data_processing_agreement', 'acceptable_use_policy',
    'refund_policy', 'employee_handbook_section',
    'information_security_policy'
  ]),
  company_name: z.string(),
  product_description: z.string(),
  data_collected: z.array(z.string()).optional().describe('Types of user data collected'),
  jurisdictions: z.array(z.string()).default(['US']).describe('Applicable jurisdictions for compliance'),
  last_updated: z.string().optional()
}, async (params) => {
  // Generate jurisdiction-appropriate policy using legal templates
  // For privacy policy: GDPR, CCPA, PIPEDA compliance sections as applicable
  // For ToS: limitation of liability, IP ownership, dispute resolution, governing law
  // Include: placeholder sections for legal review
  // Return: complete policy document in markdown + HTML-ready format
});

// ─── FINANCE ──────────────────────────────────

server.tool('financial_model', 'Build a 12 or 24-month financial model', {
  model_type: z.enum(['saas', 'marketplace', 'agency', 'ecommerce', 'general']).default('saas'),
  period_months: z.enum([12, 24]).default(12),
  inputs: z.object({
    starting_mrr: z.number().default(0),
    monthly_new_customers: z.number(),
    avg_contract_value: z.number(),
    churn_rate_monthly: z.number().describe('As decimal, e.g. 0.05 for 5%'),
    cogs_percent: z.number().describe('Cost of goods sold as % of revenue'),
    headcount: z.number().default(1),
    avg_salary: z.number().default(0),
    other_opex_monthly: z.number().default(0),
    starting_cash: z.number().default(0)
  }),
  growth_assumptions: z.object({
    optimistic_growth_rate: z.number().default(0.15),
    base_growth_rate: z.number().default(0.10),
    conservative_growth_rate: z.number().default(0.05)
  }).optional()
}, async (params) => {
  // Build month-by-month P&L: revenue, COGS, gross margin, OPEX, EBITDA, net income
  // Cash flow statement: operating, investing, financing activities
  // Unit economics: CAC, LTV, LTV:CAC ratio, payback period, magic number
  // Three-scenario model: optimistic / base / conservative
  // Runway calculation: months until cash out per scenario
  // Return: complete financial model as structured data + summary table
});

// ─── COMPLIANCE ───────────────────────────────

server.tool('compliance_check', 'Check compliance status for key regulatory frameworks', {
  framework: z.enum(['gdpr', 'ccpa', 'hipaa', 'soc2', 'pci_dss', 'iso_27001', 'coppa']),
  product_type: z.string().describe('What your product does and what data it handles'),
  current_controls: z.array(z.string()).optional().describe('Security/privacy controls already in place'),
  customer_types: z.array(z.enum(['consumers', 'b2b', 'healthcare', 'financial', 'children'])).optional()
}, async ({ framework, product_type, current_controls, customer_types }) => {
  // Map requirements checklist for specified framework
  // Score current state: controls coverage percentage
  // Identify: mandatory vs recommended controls
  // Prioritize gaps by risk level (High/Medium/Low)
  // Estimate implementation effort per gap
  // Return: compliance scorecard + gap analysis + 90-day remediation roadmap
});

// ─── HIRING ───────────────────────────────────

server.tool('hiring_package', 'Create complete hiring package for a role', {
  role_title: z.string(),
  department: z.string(),
  level: z.enum(['ic1', 'ic2', 'ic3', 'senior', 'staff', 'manager', 'director', 'vp']),
  company_stage: z.enum(['pre-seed', 'seed', 'series-a', 'series-b', 'growth']),
  must_haves: z.array(z.string()).describe('Non-negotiable requirements'),
  nice_to_haves: z.array(z.string()).optional(),
  team_context: z.string().optional().describe('What team they join, reporting structure')
}, async (params) => {
  // Job description: hook, mission, responsibilities (5-7), requirements (6-8), benefits
  // Structured interview plan: 4-5 rounds with clear evaluation criteria per round
  // Interview questions (15-20): behavioral, technical, situational + sample strong answers
  // Evaluation rubric: scorecard with weighted dimensions
  // Compensation benchmark: market ranges by level/geography (referencing levels.fyi patterns)
  // Return: complete hiring kit — JD, interview guide, scorecard template
});

// ─── VENDOR MANAGEMENT ────────────────────────

server.tool('vendor_evaluate', 'Evaluate and compare vendors against requirements', {
  vendor_category: z.string().describe('e.g. "CRM software", "cloud hosting", "payroll provider"'),
  requirements: z.array(z.string()).describe('Must-have and nice-to-have requirements'),
  vendors: z.array(z.object({
    name: z.string(),
    pricing: z.string().optional(),
    notes: z.string().optional()
  })).min(2),
  decision_criteria: z.object({
    price_weight: z.number().default(30),
    features_weight: z.number().default(35),
    support_weight: z.number().default(15),
    scalability_weight: z.number().default(20)
  }).optional()
}, async (params) => {
  // Weighted scoring matrix for each vendor across criteria
  // Feature coverage analysis against requirements (met / partial / missing)
  // TCO analysis: license cost + implementation + training + maintenance
  // Risk assessment: vendor lock-in, data portability, contract flexibility
  // Integration compatibility with existing stack
  // Return: comparison matrix + recommendation with rationale + contract negotiation tips
});
```

## Open Source Tools Powering This Server

| Tool | Purpose | GitHub | License |
|------|---------|--------|---------|
| [Twenty CRM](https://github.com/twentyhq/twenty) | Process tracking, vendor management records | 25k+ stars | MIT |
| [Docassemble](https://github.com/jhpyle/docassemble) | Legal document generation from templates | 700+ stars | MIT |
| [Plane](https://github.com/makeplane/plane) | Process/SOP tracking, project management | 30k+ stars | AGPL 3.0 |
| [Lago](https://github.com/getlago/lago) | Usage-based billing and financial modeling | 7k+ stars | AGPL 3.0 |
| [InvoiceNinja](https://github.com/invoiceninja/invoiceninja) | Invoicing and financial tracking | 8k+ stars | Elastic |
| [Langchain](https://github.com/langchain-ai/langchain) | LLM chains for document generation | 95k+ stars | MIT |

## Environment Variables

```env
# AI Generation
ANTHROPIC_API_KEY=...           # Contract review and document generation

# CRM / Process Tracking
TWENTY_API_URL=...              # Self-hosted Twenty CRM
TWENTY_API_KEY=...

# Finance
STRIPE_SECRET_KEY=...           # Revenue data for financial models
QUICKBOOKS_ACCESS_TOKEN=...     # For pulling actuals into financial model (optional)

# Document Storage
AWS_S3_BUCKET=...               # Store generated contracts, SOPs, policies
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...

# Optional
NOTION_API_KEY=...              # Push SOPs directly to Notion workspace
GOOGLE_DRIVE_API_KEY=...        # Alternative doc storage
```

## Example Usage

```typescript
// Create a customer onboarding SOP
await client.callTool('sop_create', {
  process_name: 'Customer Onboarding',
  department: 'operations',
  trigger: 'New customer signs contract and payment clears',
  inputs: ['Signed contract', 'Customer email', 'Billing confirmed'],
  outputs: ['Customer account active', 'Admin invited', 'First value achieved'],
  tools_used: ['Stripe', 'Twenty CRM', 'Slack', 'Linear'],
  existing_notes: 'Customer gets welcome email, then we set up their account...'
});

// Review an MSA before signing
await client.callTool('contract_review', {
  contract_text: '...full MSA text...',
  contract_type: 'msa',
  perspective: 'vendor',
  critical_concerns: ['IP ownership', 'limitation of liability', 'auto-renewal']
});

// Build a 12-month financial model
await client.callTool('financial_model', {
  model_type: 'saas',
  period_months: 12,
  inputs: {
    starting_mrr: 5000,
    monthly_new_customers: 8,
    avg_contract_value: 299,
    churn_rate_monthly: 0.03,
    cogs_percent: 0.20,
    headcount: 2,
    avg_salary: 80000,
    other_opex_monthly: 2000,
    starting_cash: 150000
  }
});

// Check GDPR compliance status
await client.callTool('compliance_check', {
  framework: 'gdpr',
  product_type: 'B2B SaaS — we store EU customer data including names, emails, and usage analytics',
  current_controls: ['Data encryption at rest', 'SSL/TLS', 'Access logging'],
  customer_types: ['b2b']
});
```

## Integration Notes

- **soloos-memory**: All business decisions (vendor selections, policy versions, compliance status) auto-saved via `decision_log` and `business_context_save`
- **soloos-sales**: `proposal_generate` in soloos-sales references financial models built here; `contract_review` validates sales contracts
- **soloos-product**: `hiring_package` feeds product team headcount planning; `sop_create` documents product processes
- **soloos-engineering**: `compliance_check` results flow into `security_audit`; `financial_model` feeds `infra_cost_estimate` to size infrastructure spend
- **soloos-growth**: `financial_model` outputs (CAC, LTV, unit economics) feed `growth_model` projections
