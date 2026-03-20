# SoloOS Skills for Claude Code

Drop-in custom commands for Claude Code that instantly give you a 40+ person virtual company.

## Installation

```bash
# Clone SoloOS
git clone https://github.com/datareaper247/soloprenuership.git ~/soloos

# Install Claude Code skills
cp ~/soloos/skills/claude-code/*.md ~/.claude/commands/

# Verify installation
ls ~/.claude/commands/ | grep soloos
```

## Available Skills

### `/role` — Instant Role Adoption
```bash
/role cmo
/role seo-specialist
/role cfo
/role sdr
/role legal-counsel
# ... all 40+ roles
```

### `/swarm` — Launch Multi-Agent Teams
```bash
/swarm product-launch "Launch our DevOps tool next Tuesday"
/swarm market-research "Research pharmacy audit software market"
/swarm growth-sprint "Grow MRR from $5K to $15K in 90 days"
/swarm weekly-ops    # Run weekly company operations
```

### `/research` — Market Intelligence
```bash
/research market "pharmacy audit software"
/research competitor "FoodLogiQ"
/research opportunity "AI-powered legal document review"
/research pain-mine r/SaaS "project management"
```

### `/content` — Content Production
```bash
/content blog "best pharmacy audit software 2026" --seo
/content email-sequence onboarding 7-emails
/content social "new feature launch" --all-platforms
/content landing-page "DevOps monitoring tool"
```

### `/seo` — SEO Tools
```bash
/seo research "pharmacy audit"
/seo brief "best project management tools for startups"
/seo audit domain.com
/seo gaps vs competitor.com
```

### `/sales` — Sales Tools
```bash
/sales outreach "VP Engineering at Series A startup"
/sales sequence "cold email 5-touch"
/sales qualify company-data.json
/sales crm-update "call notes from today"
```

### `/ops` — Business Operations
```bash
/ops sop "customer onboarding process"
/ops legal "review this SaaS agreement"
/ops compliance "GDPR checklist for our product"
/ops financial-model 12-months
```

### `/growth` — Growth Hacking
```bash
/growth experiment "increase trial to paid conversion"
/growth funnel-analyze "analyze our signup funnel"
/growth viral-loop "design referral mechanism"
/growth retention "identify churn signals"
```

### `/geo` — Geographic Expansion
```bash
/geo analyze japan b2b-saas
/geo localize content.md ja-JP
/geo seo "pharmacy audit" --countries JP,DE,UK
```

## Skill Files

Each skill is a `.md` file in `~/.claude/commands/`:

### `role.md`
```markdown
# Role Adoption

Load a professional role system prompt and adopt that role for the current conversation.

Available roles: ceo, cto, cmo, cfo, coo, frontend-engineer, backend-engineer,
devops-engineer, mobile-engineer, ml-engineer, security-engineer, qa-engineer,
data-engineer, product-manager, product-designer, ux-researcher, technical-writer,
content-marketer, seo-specialist, sem-manager, social-media-manager, email-marketer,
community-manager, pr-manager, growth-marketer, video-producer, sdr, account-executive,
sales-engineer, customer-success, revenue-ops, hr-manager, finance-manager,
legal-counsel, compliance-officer, business-analyst, customer-support,
technical-support, onboarding-specialist, data-analyst, growth-hacker,
cro-specialist, localization-manager, international-market-manager,
business-development, partnership-manager

Usage: /role [role-name]

When invoked:
1. Load the system prompt from ~/soloos/roles/[function]/[role]/system-prompt.md
2. Apply the role's methodology, quality standards, and tool preferences
3. Respond to the next request as that professional role
4. Maintain role context for the conversation
```

### `swarm.md`
```markdown
# Agent Swarm Launcher

Launch a coordinated multi-agent swarm to complete company-level tasks.

Usage: /swarm [type] "[task description]"

Swarm types:
- product-launch: CMO + SEO + Content + Sales + PR working in parallel
- market-research: Market + Competitor + Validation + CEO synthesis
- growth-sprint: SEO + Content + Growth + Analytics in parallel
- go-to-market: Full GTM preparation
- weekly-ops: Monday morning operations (auto-scheduled)
- custom [agent1,agent2,...]: Define your own combination

When invoked:
1. Decompose task into role-specific subtasks
2. For each role: load system prompt + relevant tools
3. Run parallel phases where possible
4. Synthesize outputs into actionable brief
5. Present: team outputs + synthesis + priority actions
6. Human review time: 15-30 minutes

Quality standard: Each agent output should be professional-grade,
not just "AI response". The SEO agent produces real keyword data,
not generic advice.
```

### `research.md`
```markdown
# Market Research

Conduct professional-grade market research using the Research Swarm.

Usage: /research [type] [target]

Types:
- market [topic]: Full market opportunity analysis
- competitor [company]: Deep competitive profile
- opportunity [idea]: Score a business idea
- pain-mine [source] [topic]: Extract validated pain points

When invoked with soloos-research MCP:
1. Use market_scan, competitor_analyze, customer_pain_mine tools
2. Synthesize findings into structured output
3. Score opportunity if requested
4. Return: brief + scores + recommendation + next steps

Without MCP (fallback):
1. Use available web search and reasoning
2. Structure output as opportunity scorecard
3. Note confidence level for each data point
```
