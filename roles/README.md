# Professional Roles Library

Every role a real company needs, deployed as AI agent system prompts.

## Complete Role Catalog (44 Roles)

### Leadership (5)
| Role | File | Primary Function |
|------|------|----------------|
| CEO | `leadership/ceo/` | Vision, strategy, stakeholder management |
| CTO | `leadership/cto/` | Technical architecture, engineering decisions |
| CMO | `leadership/cmo/` | Marketing strategy, brand, growth |
| CFO | `leadership/cfo/` | Finance, unit economics, fundraising |
| COO | `leadership/coo/` | Operations, processes, execution |

### Engineering (8)
| Role | File | Primary Function |
|------|------|----------------|
| Frontend Engineer | `engineering/frontend/` | UI, React, TypeScript, performance |
| Backend Engineer | `engineering/backend/` | APIs, databases, microservices |
| DevOps Engineer | `engineering/devops/` | Infrastructure, CI/CD, reliability |
| Mobile Engineer | `engineering/mobile/` | iOS/Android, React Native, Flutter |
| ML/AI Engineer | `engineering/ml-ai/` | Models, training, inference, MLOps |
| Security Engineer | `engineering/security/` | Pen testing, SAST/DAST, compliance |
| QA Engineer | `engineering/qa/` | Test strategy, automation, quality |
| Data Engineer | `engineering/data/` | Pipelines, warehouses, ETL |

### Product (4)
| Role | File | Primary Function |
|------|------|----------------|
| Product Manager | `product/pm/` | Roadmap, prioritization, PRDs |
| Product Designer | `product/designer/` | UX/UI design, design systems |
| UX Researcher | `product/ux-researcher/` | User research, usability testing |
| Technical Writer | `product/technical-writer/` | Docs, APIs, user guides |

### Marketing (10)
| Role | File | Primary Function |
|------|------|----------------|
| Content Marketer | `marketing/content/` | Blog, case studies, long-form |
| SEO Specialist | `marketing/seo/` | Keyword research, on-page, technical SEO |
| SEM/PPC Manager | `marketing/sem/` | Google Ads, LinkedIn Ads, paid acquisition |
| Social Media Manager | `marketing/social/` | Twitter, LinkedIn, Instagram, community |
| Email Marketer | `marketing/email/` | Sequences, newsletters, automation |
| Brand Designer | `marketing/brand/` | Visual identity, messaging, positioning |
| Video Producer | `marketing/video/` | Scripts, production briefs, YouTube strategy |
| PR Manager | `marketing/pr/` | Press releases, media pitches, thought leadership |
| Community Manager | `marketing/community/` | Discord, Slack, Reddit, forums |
| Growth Marketer | `marketing/growth/` | Acquisition experiments, channel testing |

### Sales (6)
| Role | File | Primary Function |
|------|------|----------------|
| SDR | `sales/sdr/` | Prospecting, cold outreach, pipeline building |
| Account Executive | `sales/ae/` | Demos, proposals, closing |
| Sales Engineer | `sales/se/` | Technical pre-sales, POCs, RFPs |
| Customer Success | `sales/cs/` | Onboarding, retention, expansion |
| Revenue Operations | `sales/rev-ops/` | CRM, forecasting, process optimization |
| Sales Enablement | `sales/enablement/` | Training materials, playbooks, tools |

### Operations (5)
| Role | File | Primary Function |
|------|------|----------------|
| HR Manager | `operations/hr/` | Hiring, onboarding, culture, comp |
| Finance Manager | `operations/finance/` | Bookkeeping, projections, investor reporting |
| Legal Counsel | `operations/legal/` | Contracts, IP, compliance, entity |
| Compliance Officer | `operations/compliance/` | GDPR, SOC2, regulatory, audits |
| Business Analyst | `operations/biz-analyst/` | Data analysis, reporting, insights |

### Customer (3)
| Role | File | Primary Function |
|------|------|----------------|
| Customer Support | `customer/support/` | Tickets, FAQ, email support |
| Technical Support | `customer/technical/` | Bug reports, debugging, escalation |
| Onboarding Specialist | `customer/onboarding/` | Activation, training, time-to-value |

### Growth & Analytics (4)
| Role | File | Primary Function |
|------|------|----------------|
| Data Analyst | `growth/data-analyst/` | SQL, dashboards, business insights |
| Growth Hacker | `growth/growth-hacker/` | Viral loops, experiments, acquisition |
| CRO Specialist | `growth/cro/` | Conversion optimization, A/B testing |
| Analytics Engineer | `growth/analytics-engineer/` | dbt, data models, warehouse |

### Geographic / International (3)
| Role | File | Primary Function |
|------|------|----------------|
| Localization Manager | `geo/localization/` | Translation, cultural adaptation |
| International Market Manager | `geo/international/` | Market entry, geo strategy |
| Translation Specialist | `geo/translation/` | Professional translation, QA |

### Partnerships (3)
| Role | File | Primary Function |
|------|------|----------------|
| Business Development | `partnerships/biz-dev/` | Strategic partnerships, deals |
| Partnership Manager | `partnerships/partnerships/` | Partner success, co-marketing |
| API/Integration Manager | `partnerships/api-integrations/` | Technical partnerships, marketplaces |

---

## Role Interaction Map

```
                    CEO
                   / | \
                CTO  CMO  CFO
               / |    |    \
           Eng  QA  Mktg  Finance
                     |
              SEO  Content  Social  Email  Growth
                     |
                   Sales
              SDR → AE → CS → RevOps
                     |
                 Customer
              Support  Technical  Onboarding
```

## How to Use a Role

### Option 1: Direct System Prompt
Copy the system prompt from `[role]/system-prompt.md` and use as your AI's system context.

### Option 2: Claude Code Skill
```bash
/role seo-specialist
# → Agent adopts SEO Specialist role for current session
```

### Option 3: Via MCP
```
invoke_role("seo_specialist", task="Research keywords for pharmacy audit software")
```

### Option 4: CrewAI Integration
```python
from soloos.roles import SEOSpecialist, ContentMarketer

seo = SEOSpecialist.as_crewai_agent()
writer = ContentMarketer.as_crewai_agent()
```

---

## Role Design Principles

Each role is designed to:
1. **Produce professional-grade outputs** — not "AI responses" but actual deliverables
2. **Know their tools** — explicit about what tools/software they use
3. **Know when to escalate** — clear decision boundaries
4. **Have quality standards** — specific criteria for what "good" looks like
5. **Collaborate correctly** — defined handoff patterns with other roles

---

## Adding New Roles

Template for a new role:
```
roles/[function]/[role-name]/
├── system-prompt.md   # The AI system prompt
├── tools.md           # Tools and integrations
├── deliverables.md    # What this role produces
├── workflows.md       # Standard workflows
└── examples/          # Example outputs
```
