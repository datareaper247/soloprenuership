# Role Catalog

## Core Roles (Solo Founder Daily Use)

These 10 roles are what a solo founder actually invokes. Deep system prompts with
identity, frameworks, escalation logic, and output formats.

| Role | Path | When to Use |
|------|------|------------|
| **CEO** | `leadership/ceo/` | Strategy, OKRs, investor narrative, pivot decisions |
| **CMO** | `leadership/cmo/` | GTM strategy, positioning canvas, demand gen planning |
| **CFO** | `leadership/cfo/` | Unit economics, pricing math, financial modeling |
| **SDR** | `sales/sdr/` | ICP research, cold outreach, pipeline building |
| **Account Executive** | `sales/account-executive/` | Discovery, demos, close strategies |
| **Customer Success** | `sales/customer-success/` | Retention, churn prevention, expansion |
| **SEO Specialist** | `marketing/seo-specialist/` | Keyword research, content briefs, technical audit |
| **Content Marketer** | `marketing/content-marketer/` | Long-form SEO, case studies, newsletters |
| **Growth Hacker** | `analytics/growth-hacker/` | AARRR experiments, viral loops, PLG |
| **Product Manager** | `product/product-manager/` | PRDs, roadmap, prioritization, metrics |

**Activate any core role**: `/role [name]` (e.g., `/role cmo`, `/role sdr`)

---

## Also Available (Core Adjacent)

Useful enough to keep prominent, not daily-driver territory:

| Role | Path | When to Use |
|------|------|------------|
| CTO | `leadership/cto/` | Architecture decisions, build vs buy, tech debt |
| COO | `leadership/coo/` | Process design, OKR tracking, ops |
| Frontend Engineer | `engineering/frontend-engineer/` | React/Next.js work, performance |
| Backend Engineer | `engineering/backend-engineer/` | API design, database, security |
| Data Analyst | `analytics/data-analyst/` | Cohort analysis, SQL, dashboards |
| CRO Specialist | `analytics/cro-specialist/` | Conversion optimization, A/B testing |
| Finance Manager | `operations/finance-manager/` | Bookkeeping, cash flow, reporting |
| Customer Support | `customer/support-specialist/` | Support playbooks, ticket handling |
| Growth Marketer | `marketing/growth-marketer/` | Acquisition experiments, retention |

---

## Extended Roles (See `extended/`)

30+ additional roles for when you have a team, enterprise motion, or specific
function to fill. All in `agents/roles/extended/`. See `extended/README.md`.

---

## How to Use Roles

**In Claude Code**:
```bash
/role cmo
```
Claude adopts the CMO system prompt for the conversation.

**In any Claude conversation**:
Copy the contents of the role's system-prompt.md into the system prompt or
the first user message with "You are the [role]:" prefix.

**In CrewAI / AutoGen** (manual setup, no package yet):
```python
with open('agents/roles/leadership/cmo/system-prompt.md') as f:
    cmo_prompt = f.read()
agent = Agent(role="CMO", backstory=cmo_prompt)
```
