# SoloOS Professional Role Catalog

A complete AI agent org chart — 46 professional roles deployable as system prompts.
Every role a real company needs, engineered for autonomous AI execution.

---

## Summary Table

| Function | Role | Reports To | Key Output |
|---|---|---|---|
| **LEADERSHIP** | CEO | Board/Founder | Strategy, Vision |
| | CTO | CEO | Technical Architecture |
| | CMO | CEO | Marketing Strategy |
| | CFO | CEO | Financial Health |
| | COO | CEO | Operational Excellence |
| **ENGINEERING** | Frontend Engineer | CTO | UI/UX Implementation |
| | Backend Engineer | CTO | APIs, Services |
| | DevOps/Platform Engineer | CTO | Infrastructure |
| | Mobile Engineer | CTO | Mobile Apps |
| | ML/AI Engineer | CTO | AI Features |
| | Security Engineer | CTO | Security Posture |
| | QA/Test Engineer | CTO | Quality Gates |
| | Data Engineer | CTO | Data Pipelines |
| **PRODUCT** | Product Manager | CEO/CTO | Roadmap, PRDs |
| | Product Designer | PM | Design Systems |
| | UX Researcher | PM | User Insights |
| | Technical Writer | CTO/PM | Documentation |
| **MARKETING** | Content Marketer | CMO | Content Assets |
| | SEO Specialist | CMO | Search Rankings |
| | SEM/PPC Manager | CMO | Paid Acquisition |
| | Social Media Manager | CMO | Social Presence |
| | Email Marketing Manager | CMO | Email Campaigns |
| | Brand Designer | CMO | Brand Assets |
| | Video Producer | CMO | Video Content |
| | PR/Communications Manager | CMO | Press & Narrative |
| | Community Manager | CMO | Community Growth |
| | Growth Marketer | CMO/COO | Growth Loops |
| **SALES** | SDR | VP Sales | Qualified Pipeline |
| | Account Executive | VP Sales | Closed Revenue |
| | Sales Engineer | AE/CTO | Technical Wins |
| | Customer Success Manager | COO | Retention, NRR |
| | Revenue Operations | COO | Revenue Systems |
| | Sales Enablement Manager | VP Sales | Sales Productivity |
| **OPERATIONS** | HR Manager | COO | People Systems |
| | Finance Manager | CFO | Financial Operations |
| | Legal Counsel | CEO | Legal Protection |
| | Compliance Officer | COO | Regulatory Compliance |
| | Business Analyst | COO | Process Intelligence |
| **CUSTOMER** | Customer Support Specialist | COO | Issue Resolution |
| | Technical Support Engineer | CTO | Technical Resolution |
| | Onboarding Specialist | COO | Customer Activation |
| **ANALYTICS** | Data Analyst | COO | Insights & Reports |
| | Growth Hacker | CMO/COO | Growth Experiments |
| | CRO Specialist | CMO | Conversion Optimization |
| | Analytics Engineer | CTO | Data Infrastructure |
| **INTERNATIONAL** | Localization Manager | CMO | Localized Products |
| | International Market Manager | CMO | Market Expansion |
| | Translation Specialist | Loc. Manager | Translated Assets |
| **PARTNERSHIPS** | Business Development | CEO | Strategic Deals |
| | Partnership Manager | BizDev | Partner Success |
| | API/Integration Manager | CTO | Integration Ecosystem |

---

## Role Interaction Map

```
FOUNDER
  └── CEO
        ├── CTO
        │     ├── Frontend Engineer
        │     ├── Backend Engineer
        │     ├── DevOps/Platform Engineer
        │     ├── Mobile Engineer
        │     ├── ML/AI Engineer
        │     ├── Security Engineer
        │     ├── QA/Test Engineer
        │     ├── Data Engineer
        │     ├── Technical Writer
        │     └── API/Integration Manager
        ├── CMO
        │     ├── Content Marketer
        │     ├── SEO Specialist
        │     ├── SEM/PPC Manager
        │     ├── Social Media Manager
        │     ├── Email Marketing Manager
        │     ├── Brand Designer
        │     ├── Video Producer
        │     ├── PR/Communications Manager
        │     ├── Community Manager
        │     ├── Growth Marketer
        │     ├── Localization Manager
        │     │     └── Translation Specialist
        │     └── International Market Manager
        ├── CFO
        │     └── Finance Manager
        ├── COO
        │     ├── HR Manager
        │     ├── Legal Counsel
        │     ├── Compliance Officer
        │     ├── Business Analyst
        │     ├── Customer Support Specialist
        │     ├── Technical Support Engineer
        │     ├── Onboarding Specialist
        │     ├── Data Analyst
        │     ├── Growth Hacker
        │     ├── CRO Specialist
        │     ├── Revenue Operations
        │     └── Analytics Engineer
        ├── Product Manager (CEO/CTO)
        │     ├── Product Designer
        │     └── UX Researcher
        └── Business Development (CEO)
              └── Partnership Manager
```

---

## Handoff Protocols

### Engineering Handoffs
- **PM → Frontend/Backend**: PRD with acceptance criteria, wireframes, API contract
- **Backend → Frontend**: OpenAPI spec, endpoint documentation, mock data
- **Engineering → QA**: PR with test plan, environment URL, edge cases documented
- **QA → DevOps**: Approved build artifact, deployment checklist

### Marketing Handoffs
- **Brand Designer → Content/Social**: Brand kit, asset library, tone guide
- **SEO → Content**: Keyword clusters, content briefs, internal link map
- **Content → Social**: Published URL, social copy variants, asset sizes
- **PR → Social/Content**: Press release, approved quotes, embargo dates

### Sales Handoffs
- **SDR → AE**: Qualified opportunity with BANT, discovery notes, stakeholder map
- **AE → CS**: Signed contract, success criteria, implementation scope
- **CS → Support**: Account health score, escalation history, technical context
- **Sales Engineer → Backend**: Integration requirements, security questionnaire

### Product Handoffs
- **UX Research → PM**: Research synthesis, validated personas, opportunity sizing
- **PM → Design**: Problem statement, user stories, success metrics
- **Design → Engineering**: Figma specs, component inventory, interaction notes
- **Engineering → Technical Writer**: Feature spec, API changes, changelog entry

---

## Information Flow Standards

### Upward (status, blockers, decisions needed)
- Weekly status updates every Monday 09:00
- Blocker escalation within 4 hours
- Decision requests with options + recommendation

### Downward (direction, context, priorities)
- Priority changes communicated within 1 hour
- Strategic context updated monthly
- Resources unlocked proactively

### Lateral (collaboration, handoffs)
- Handoffs documented in shared system
- SLA: acknowledge within 2 hours, complete within agreed timeline
- Async-first communication

---

## File Structure

```
agents/roles/
├── CATALOG.md (this file)
├── INTERACTION_MAP.md
├── leadership/
│   ├── ceo/system-prompt.md
│   ├── cto/system-prompt.md
│   ├── cmo/system-prompt.md
│   ├── cfo/system-prompt.md
│   └── coo/system-prompt.md
├── engineering/
│   ├── frontend-engineer/system-prompt.md
│   ├── backend-engineer/system-prompt.md
│   ├── devops-engineer/system-prompt.md
│   ├── mobile-engineer/system-prompt.md
│   ├── ml-ai-engineer/system-prompt.md
│   ├── security-engineer/system-prompt.md
│   ├── qa-engineer/system-prompt.md
│   └── data-engineer/system-prompt.md
├── product/
│   ├── product-manager/system-prompt.md
│   ├── product-designer/system-prompt.md
│   ├── ux-researcher/system-prompt.md
│   └── technical-writer/system-prompt.md
├── marketing/
│   ├── content-marketer/system-prompt.md
│   ├── seo-specialist/system-prompt.md
│   ├── sem-ppc-manager/system-prompt.md
│   ├── social-media-manager/system-prompt.md
│   ├── email-marketing-manager/system-prompt.md
│   ├── brand-designer/system-prompt.md
│   ├── video-producer/system-prompt.md
│   ├── pr-communications/system-prompt.md
│   ├── community-manager/system-prompt.md
│   └── growth-marketer/system-prompt.md
├── sales/
│   ├── sdr/system-prompt.md
│   ├── account-executive/system-prompt.md
│   ├── sales-engineer/system-prompt.md
│   ├── customer-success/system-prompt.md
│   ├── revenue-operations/system-prompt.md
│   └── sales-enablement/system-prompt.md
├── operations/
│   ├── hr-manager/system-prompt.md
│   ├── finance-manager/system-prompt.md
│   ├── legal-counsel/system-prompt.md
│   ├── compliance-officer/system-prompt.md
│   └── business-analyst/system-prompt.md
├── customer/
│   ├── support-specialist/system-prompt.md
│   ├── technical-support/system-prompt.md
│   └── onboarding-specialist/system-prompt.md
├── analytics/
│   ├── data-analyst/system-prompt.md
│   ├── growth-hacker/system-prompt.md
│   ├── cro-specialist/system-prompt.md
│   └── analytics-engineer/system-prompt.md
├── international/
│   ├── localization-manager/system-prompt.md
│   ├── international-market-manager/system-prompt.md
│   └── translation-specialist/system-prompt.md
└── partnerships/
    ├── business-development/system-prompt.md
    ├── partnership-manager/system-prompt.md
    └── api-integration-manager/system-prompt.md
```
