# soloos-engineering MCP Server

**Purpose**: Engineering excellence capabilities — architecture review, code review, security audits, incident management, API design, infrastructure cost estimation, and technical debt tracking.

## TypeScript Server Definition

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'soloos-engineering',
  version: '1.0.0',
  description: 'Senior engineering intelligence for solo founders — architecture, security, performance, and ops'
});

// ─── ARCHITECTURE ─────────────────────────────

server.tool('architecture_review', 'Review system architecture, flag risks and improvements', {
  architecture_description: z.string().describe('System description, tech stack, data flows, component diagram or ADR'),
  system_type: z.enum(['monolith', 'microservices', 'serverless', 'edge', 'hybrid']),
  scale_target: z.string().describe('Expected load: e.g. "10K MAU in 6 months, 100K in 18 months"'),
  current_pain_points: z.array(z.string()).optional(),
  non_negotiables: z.array(z.string()).optional().describe('Constraints: compliance, latency SLAs, budget'),
  tech_stack: z.array(z.string()).optional()
}, async (params) => {
  // Evaluate against: scalability, reliability, maintainability, security, cost efficiency
  // SPOF analysis: single points of failure in data path, auth, storage
  // Coupling analysis: tight coupling between services / modules that limits evolution
  // Data model review: normalization, indexing strategy, scaling bottlenecks
  // Cost efficiency: over-provisioned services, serverless cold start risks
  // Recommendations prioritized: P0 (fix now) / P1 (fix soon) / P2 (tech debt)
  // Return: risk scorecard + prioritized recommendations + suggested ADR changes
});

server.tool('api_design', 'Design REST or GraphQL APIs with full OpenAPI spec', {
  api_name: z.string(),
  api_type: z.enum(['rest', 'graphql', 'grpc', 'webhooks']),
  use_cases: z.array(z.string()).describe('What consumers of this API need to do'),
  resources: z.array(z.string()).describe('Core domain objects: e.g. ["User", "Order", "Product"]'),
  auth_strategy: z.enum(['api_key', 'jwt', 'oauth2', 'none']).default('jwt'),
  versioning_strategy: z.enum(['url_path', 'header', 'query_param']).default('url_path'),
  existing_patterns: z.string().optional().describe('Existing APIs to stay consistent with')
}, async (params) => {
  // Design resource hierarchy and URL structure
  // REST: endpoints (GET/POST/PUT/PATCH/DELETE), path params, query params, request/response bodies
  // GraphQL: schema definition, query/mutation/subscription types, resolver hints
  // For each endpoint: status codes, error response format, pagination strategy
  // Generate: OpenAPI 3.0 spec in YAML
  // Include: rate limiting headers, idempotency keys, webhook delivery guarantees
  // Return: full OpenAPI spec + design decision rationale + integration guide snippet
});

server.tool('migration_plan', 'Create database or system migration plans', {
  migration_type: z.enum(['database_schema', 'database_engine', 'monolith_to_microservices', 'cloud_provider', 'data_migration', 'auth_system']),
  current_state: z.string().describe('Current system/schema description'),
  target_state: z.string().describe('Target system/schema description'),
  data_volume: z.string().optional().describe('e.g. "10M rows, 500GB"'),
  downtime_tolerance: z.enum(['zero_downtime', 'maintenance_window', 'flexible']).default('zero_downtime'),
  rollback_required: z.boolean().default(true)
}, async (params) => {
  // Generate phased migration plan with zero-downtime strategy if required
  // Database: expand-contract pattern, dual-write strategy, backfill scripts
  // System: strangler fig pattern for monolith decomposition
  // Validation: data integrity checks at each phase
  // Rollback procedures: per-phase rollback runbook
  // Estimated timeline: effort per phase, parallelization opportunities
  // Return: phase-by-phase migration plan + SQL/code scaffolding + validation queries + rollback runbook
});

// ─── CODE QUALITY ─────────────────────────────

server.tool('code_review', 'Professional code review with security, performance, and maintainability scoring', {
  code: z.string().describe('Code to review (paste code or file path)'),
  language: z.string().describe('e.g. "TypeScript", "Python", "Go"'),
  context: z.string().optional().describe('What this code does and its role in the system'),
  review_focus: z.array(z.enum([
    'security', 'performance', 'maintainability', 'correctness',
    'error_handling', 'testing', 'api_design', 'data_handling'
  ])).default(['security', 'correctness', 'maintainability'])
}, async (params) => {
  // Score each dimension 1-10 with specific line references
  // Security: injection, auth bypass, secrets in code, input validation, OWASP Top 10
  // Performance: N+1 queries, missing indexes, memory leaks, blocking I/O
  // Maintainability: complexity, naming, single-responsibility, test coverage
  // Error handling: unhandled exceptions, silent failures, missing retries
  // Inline comments: specific line-by-line suggestions
  // Rewritten version: provide improved version for top 3 issues
  // Return: review report with scores + inline comments + suggested rewrites
});

server.tool('tech_debt_audit', 'Identify and quantify technical debt across a codebase', {
  codebase_description: z.string().describe('Stack, age, size, team history, known pain points'),
  files_or_modules: z.array(z.string()).optional().describe('Specific areas to focus on'),
  business_context: z.string().optional().describe('Growth stage, upcoming features that may be impacted'),
  time_horizon_months: z.number().default(12)
}, async (params) => {
  // Categorize debt: architectural, code quality, dependency, test, documentation, infrastructure
  // Quantify each item: estimated engineering days to fix
  // Impact analysis: which debt items will slow upcoming features?
  // Prioritization: cost of doing nothing vs cost of fixing per item
  // Create: tech debt register with effort/impact matrix
  // Quick wins: highest-ROI debt to clear first
  // Return: debt register + prioritized roadmap + effort estimates + business impact mapping
});

// ─── SECURITY ─────────────────────────────────

server.tool('security_audit', 'Security audit checklist for web application or API', {
  system_description: z.string(),
  tech_stack: z.array(z.string()),
  auth_mechanism: z.string().describe('How users authenticate'),
  data_sensitivity: z.enum(['public', 'internal', 'confidential', 'restricted']).default('confidential'),
  compliance_targets: z.array(z.enum(['soc2', 'gdpr', 'hipaa', 'pci_dss', 'iso27001'])).optional(),
  previous_incidents: z.array(z.string()).optional()
}, async (params) => {
  // OWASP Top 10 checklist: injection, broken auth, sensitive data exposure, XXE, broken access control, etc.
  // Auth security: JWT validation, token storage, session fixation, MFA
  // Data security: encryption at rest/transit, PII handling, data minimization
  // API security: rate limiting, input validation, CORS, API key management
  // Infrastructure: secrets management, dependency vulnerabilities, network segmentation
  // Dependency audit: known CVEs in current stack
  // Compliance gap: framework-specific requirements vs current state
  // Return: findings by severity (Critical/High/Medium/Low) + remediation steps + compliance checklist
});

server.tool('dependency_audit', 'Audit dependencies for security vulnerabilities and outdated versions', {
  package_file_content: z.string().describe('Contents of package.json, requirements.txt, go.mod, Gemfile, etc.'),
  package_manager: z.enum(['npm', 'yarn', 'pip', 'poetry', 'go', 'cargo', 'bundler', 'maven']),
  check_licenses: z.boolean().default(true),
  severity_threshold: z.enum(['critical', 'high', 'medium', 'low']).default('high')
}, async (params) => {
  // Parse dependency tree (direct + transitive)
  // Query vulnerability databases: OSV, NVD, Snyk DB (open)
  // Flag: CVEs above severity threshold with CVSS scores
  // Outdated packages: semver distance from latest stable
  // License compliance: flag GPL/AGPL in commercial products
  // Prioritized upgrade path: group upgrades to minimize breaking changes
  // Return: vulnerability report + upgrade priority list + license issues + estimated upgrade effort
});

// ─── INFRASTRUCTURE ───────────────────────────

server.tool('infra_cost_estimate', 'Estimate cloud infrastructure costs for a system design', {
  provider: z.enum(['aws', 'gcp', 'azure', 'vercel', 'railway', 'fly_io', 'multi_cloud']).default('aws'),
  components: z.array(z.object({
    type: z.enum(['compute', 'database', 'storage', 'cdn', 'queue', 'cache', 'ai_inference', 'email', 'monitoring']),
    spec: z.string().describe('e.g. "2 vCPU 4GB RAM app server", "100GB Postgres RDS", "1TB S3"'),
    scale: z.string().describe('e.g. "1 instance", "3 replicas", "auto-scale 1-10"')
  })),
  traffic_profile: z.string().describe('e.g. "10K MAU, 500 concurrent peak, 2TB/month egress'),
  optimization_goal: z.enum(['minimize_cost', 'balance', 'maximize_reliability']).default('balance')
}, async (params) => {
  // Price each component using provider pricing APIs / published rates
  // Total monthly cost at current scale + projected 3x and 10x scale
  // Cost breakdown: compute vs storage vs network vs managed services
  // Savings opportunities: reserved instances, spot instances, right-sizing
  // Alternative: compare equivalent setup on 2 alternative providers
  // Free tier / startup credits: AWS Activate, GCP credits, Vercel hobby limits
  // Return: cost estimate table + scaling curve + optimization recommendations + provider comparison
});

// ─── RELIABILITY ──────────────────────────────

server.tool('incident_runbook', 'Create incident response runbooks for common failure scenarios', {
  system_name: z.string(),
  incident_type: z.enum([
    'service_down', 'database_failure', 'high_latency', 'memory_leak',
    'data_corruption', 'security_breach', 'third_party_outage',
    'deploy_rollback', 'ddos', 'certificate_expiry'
  ]),
  tech_stack: z.array(z.string()),
  monitoring_tools: z.array(z.string()).optional().describe('e.g. ["Datadog", "PagerDuty", "Sentry"]'),
  on_call_team_size: z.number().default(1)
}, async (params) => {
  // Runbook structure: detection → triage → mitigation → resolution → postmortem
  // Detection: what alerts fire and what dashboards to check first
  // Triage: decision tree to narrow root cause in < 5 minutes
  // Mitigation steps: ordered actions with exact commands/links
  // Escalation: when and how to escalate, stakeholder notification templates
  // Postmortem template: timeline, root cause, action items, metrics impacted
  // Return: complete runbook + alert configuration recommendations + postmortem template
});

server.tool('performance_profile', 'Performance profiling recommendations for a system', {
  symptoms: z.array(z.string()).describe('Observed issues: e.g. "slow API responses", "high CPU at peak load"'),
  system_description: z.string(),
  tech_stack: z.array(z.string()),
  current_metrics: z.object({
    p50_latency_ms: z.number().optional(),
    p99_latency_ms: z.number().optional(),
    error_rate_percent: z.number().optional(),
    cpu_percent: z.number().optional(),
    memory_mb: z.number().optional()
  }).optional(),
  target_sla: z.string().optional().describe('e.g. "p99 < 200ms"')
}, async (params) => {
  // Diagnose: likely bottlenecks based on symptoms and stack
  // Instrumentation: what metrics and traces to add to identify root cause
  // Profiling approach: how to profile each layer (DB, app, network, frontend)
  // Quick wins: changes likely to yield 2x+ improvement (caching, indexing, query optimization)
  // Systematic approach: profiling → hypothesis → fix → measure loop
  // Tools: open source profiling tools for the specific stack
  // Return: bottleneck hypotheses + investigation steps + optimization playbook + tooling recommendations
});
```

## Open Source Tools Powering This Server

| Tool | Purpose | GitHub | License |
|------|---------|--------|---------|
| [Semgrep](https://github.com/semgrep/semgrep) | SAST security scanning, code quality rules | 10k+ stars | LGPL 2.1 |
| [OSV Scanner](https://github.com/google/osv-scanner) | Dependency vulnerability scanning (Google) | 6k+ stars | Apache 2.0 |
| [Trivy](https://github.com/aquasecurity/trivy) | Container and infra security scanning | 24k+ stars | Apache 2.0 |
| [Infracost](https://github.com/infracost/infracost) | Cloud cost estimation from IaC | 11k+ stars | Apache 2.0 |
| [Checkov](https://github.com/bridgecrewio/checkov) | IaC security and compliance scanning | 7k+ stars | Apache 2.0 |
| [Steampipe](https://github.com/turbot/steampipe) | SQL queries over cloud provider APIs | 7k+ stars | MPL 2.0 |

## Environment Variables

```env
# Security Scanning
SEMGREP_APP_TOKEN=...           # Semgrep Cloud for rule management (free tier available)
SNYK_TOKEN=...                  # Snyk vulnerability DB (free tier: 200 tests/month)

# Cloud Pricing
INFRACOST_API_KEY=...           # Infracost for Terraform cost estimation

# Static Analysis
SONARQUBE_TOKEN=...             # SonarQube/SonarCloud (free for open source)

# AI
ANTHROPIC_API_KEY=...           # Architecture review and code review generation

# Optional
GITHUB_TOKEN=...                # For dependency audit via GitHub Dependency Graph
DATADOG_API_KEY=...             # Pull performance metrics for profiling analysis
```

## Example Usage

```typescript
// Architecture review before scaling
await client.callTool('architecture_review', {
  architecture_description: 'Next.js + Vercel frontend, Node.js API on Railway, Postgres + Redis on Railway, Stripe for payments, Resend for email, S3 for file uploads',
  system_type: 'monolith',
  scale_target: '50K MAU in 12 months, 500 concurrent users peak',
  current_pain_points: ['Database queries slowing on reports page', 'Railway has cold starts'],
  tech_stack: ['Next.js', 'Node.js', 'PostgreSQL', 'Redis', 'Railway', 'Vercel']
});

// Review a critical auth module
await client.callTool('code_review', {
  code: `
    async function login(email, password) {
      const user = await db.query('SELECT * FROM users WHERE email = ' + email);
      if (user && user.password === password) {
        return jwt.sign({ userId: user.id }, process.env.SECRET);
      }
    }
  `,
  language: 'JavaScript',
  context: 'User authentication endpoint',
  review_focus: ['security', 'correctness', 'error_handling']
});

// Audit npm dependencies
await client.callTool('dependency_audit', {
  package_file_content: '{"dependencies":{"express":"4.18.0","jsonwebtoken":"8.5.1","lodash":"4.17.20"}}',
  package_manager: 'npm',
  check_licenses: true,
  severity_threshold: 'high'
});

// Estimate AWS costs before shipping
await client.callTool('infra_cost_estimate', {
  provider: 'aws',
  components: [
    { type: 'compute', spec: '2 vCPU 4GB RAM ECS Fargate container', scale: '2 tasks, auto-scale to 8' },
    { type: 'database', spec: 'db.t3.medium RDS Postgres Multi-AZ', scale: '1 instance + read replica' },
    { type: 'cache', spec: 'cache.t3.micro ElastiCache Redis', scale: '1 node' },
    { type: 'storage', spec: 'S3 standard', scale: '500GB + 1TB egress' }
  ],
  traffic_profile: '25K MAU, 200 concurrent peak, 1TB/month egress',
  optimization_goal: 'balance'
});

// Create database outage runbook
await client.callTool('incident_runbook', {
  system_name: 'Acme SaaS API',
  incident_type: 'database_failure',
  tech_stack: ['Node.js', 'PostgreSQL', 'AWS RDS'],
  monitoring_tools: ['Datadog', 'PagerDuty'],
  on_call_team_size: 1
});
```

## Integration Notes

- **soloos-memory**: Architecture decisions saved via `decision_log` with tags ["engineering", "architecture"]; tech debt register → `business_context_save` category "risk"; security findings → `business_context_save` category "risk"
- **soloos-ops**: `security_audit` findings feed `compliance_check`; `infra_cost_estimate` feeds `financial_model` for accurate COGS modeling; `api_design` output feeds `contract_review` for API terms
- **soloos-product**: `prd_create` from soloos-product is the input to `architecture_review` and `api_design`; `tech_debt_audit` feeds feature prioritization decisions
- **soloos-growth**: `performance_profile` improvements directly impact funnel conversion (page load speed → signup rate); `infra_cost_estimate` informs CAC through infrastructure COGS
- **soloos-sales**: `security_audit` results become sales collateral for enterprise security reviews (SOC2, GDPR questionnaires); `api_design` docs shared with technical evaluators
