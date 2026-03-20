# SoloOS Role Interaction Map

Complete specification of how all 46 roles communicate, hand off work, and collaborate.

---

## Reporting Lines

```
FOUNDER / BOARD
    │
    └── CEO
          ├── CTO ──────────────────────────────────────────────────┐
          │     ├── Frontend Engineer                               │
          │     ├── Backend Engineer                                │
          │     ├── DevOps/Platform Engineer                        │
          │     ├── Mobile Engineer                                 │
          │     ├── ML/AI Engineer                                  │
          │     ├── Security Engineer                               │
          │     ├── QA/Test Engineer                                │
          │     ├── Data Engineer                                   │
          │     ├── Technical Writer (joint with PM)                │
          │     └── API/Integration Manager (joint with BizDev)     │
          │                                                         │
          ├── CMO                                                   │
          │     ├── Content Marketer                                │
          │     ├── SEO Specialist                                  │
          │     ├── SEM/PPC Manager                                 │
          │     ├── Social Media Manager                            │
          │     ├── Email Marketing Manager                         │
          │     ├── Brand Designer                                  │
          │     ├── Video Producer                                  │
          │     ├── PR/Communications Manager                       │
          │     ├── Community Manager                               │
          │     ├── Growth Marketer (joint with COO)                │
          │     ├── Localization Manager ──► Translation Specialists│
          │     └── International Market Manager                    │
          │                                                         │
          ├── CFO                                                   │
          │     └── Finance Manager                                 │
          │                                                         │
          ├── COO                                                   │
          │     ├── HR Manager                                      │
          │     ├── Legal Counsel (dotted line to CEO)              │
          │     ├── Compliance Officer                              │
          │     ├── Business Analyst                                │
          │     ├── Customer Support Specialist                     │
          │     ├── Technical Support Engineer (joint with CTO)     │
          │     ├── Onboarding Specialist                           │
          │     ├── Data Analyst                                    │
          │     ├── Growth Hacker                                   │
          │     ├── CRO Specialist                                  │
          │     ├── Revenue Operations                              │
          │     └── Analytics Engineer (joint with CTO)            │
          │                                                         │
          ├── Product Manager (CEO + CTO alignment)                 │
          │     ├── Product Designer                                │
          │     └── UX Researcher                                   │
          │                                                         │
          └── Business Development (direct to CEO)                  │
                ├── Partnership Manager                             │
                └── API/Integration Manager ◄─────────────────────┘
```

---

## Key Collaboration Flows

### Flow 1: Feature Development
```
UX Researcher → PM → Product Designer → PM → Engineering → QA → DevOps → Technical Writer → PM (accept) → CMO (launch)
```

**Handoff Details:**
| From | To | What | Format |
|---|---|---|---|
| UX Researcher | PM | Research synthesis | Notion report |
| PM | Product Designer | PRD | Notion doc |
| Product Designer | PM | Designs | Figma link |
| PM | Engineering | PRD + Figma | Linear ticket + links |
| Engineering | QA | PR | GitHub PR |
| QA | DevOps | Approved build | Deployment approval |
| Engineering | Technical Writer | Feature spec | Notion + PR description |
| PM | CMO | Launch brief | Notion doc |

---

### Flow 2: Sales Process
```
Marketing (MQL) → SDR (qualify) → AE (discovery + demo) → Sales Engineer (technical proof) → AE (proposal) → Legal (contract) → CS (onboard)
```

**Handoff Details:**
| From | To | What | Format |
|---|---|---|---|
| Marketing | SDR | MQL alert | CRM notification |
| SDR | AE | SQL opportunity | CRM opportunity + notes |
| AE | Sales Engineer | Technical requirements | CRM notes + pre-call brief |
| AE | Legal | Contract for review | PandaDoc draft |
| AE | CS | Signed customer | CRM deal + handoff doc |
| CS | Onboarding | New customer | Notion account plan |

---

### Flow 3: Customer Issue Resolution
```
Customer → Support Specialist → (if technical) Technical Support Engineer → (if bug) Engineering → (fix) Technical Support → Support Specialist → Customer
```

**Handoff Details:**
| From | To | What | SLA |
|---|---|---|---|
| Customer | Support Specialist | Ticket | < 4 hours first response |
| Support Specialist | Technical Support | Escalation | < 2 hours |
| Technical Support | Engineering | Bug report | Linear ticket, same day |
| Engineering | Technical Support | Fix notification | Per sprint cycle |
| Technical Support | Support Specialist | Resolution | Within 2 hours of fix |
| Support Specialist | Customer | Resolution | < 24 hours total |

---

### Flow 4: Marketing Campaign
```
CMO (strategy) → SEO (keyword research) → Content Marketer (write) → Brand Designer (assets) → Email Manager (email) → Social Manager (social) → Analytics (measure) → CMO (optimize)
```

---

### Flow 5: Security Incident Response
```
Security Engineer (detect) → CTO + CEO (notify) → Engineering (patch) → DevOps (deploy fix) → Legal (assess disclosure requirements) → PR + CEO (customer communication)
```

**SLA:**
- Detection to notification: < 15 minutes
- Notification to patch deployment: < 24 hours (P0)
- Disclosure decision: Legal + CEO within 72 hours

---

### Flow 6: Partnership Deal
```
BizDev (identify) → CEO (approve pursue) → BizDev (negotiate) → Legal (contract review) → BizDev (sign) → Partnership Manager (onboard) → API Integration Manager (technical) → CMO (co-marketing)
```

---

### Flow 7: Data Product → Business Decision
```
Data Engineer (pipelines) → Analytics Engineer (models) → Data Analyst (analysis) → COO/CEO (decision)
```

---

### Flow 8: International Expansion
```
International Market Manager (research) → CEO (approve market) → Localization Manager (coordinate) → Translation Specialists (translate) → Engineering (i18n) → CMO (launch) → International Market Manager (grow)
```

---

## Communication Protocols

### Async-First Principles
1. Default to written communication with clear subject/context
2. Use synchronous meetings only for: decisions requiring real-time debate, relationship building, crisis management
3. Every meeting has an agenda and produces written outputs
4. Response SLAs are role-specific and documented per role

### Standard Response SLAs
| Urgency | Response Time |
|---|---|
| P0 (outage, breach, revenue-critical) | 15 minutes |
| P1 (urgent business need) | 2 hours |
| P2 (normal business request) | 24 hours |
| P3 (low priority) | 72 hours |

### Escalation Protocol
1. **Try to resolve at current level first** (one attempt)
2. **Clearly state what you tried and why it didn't work**
3. **Bring a recommendation, not just the problem**
4. **Escalate to the right level** — don't skip levels except in P0 situations

---

## Information Flow Architecture

### Upward (Status & Escalation)
| Frequency | From | To | Content |
|---|---|---|---|
| Real-time | Any | Manager | P0 alerts, blockers |
| Weekly | All functions | COO/CEO | Status, metrics, flags |
| Monthly | All departments | CEO | Performance vs. targets |
| Quarterly | CEO | Board | OKRs, financials, strategy |

### Downward (Direction & Context)
| Frequency | From | To | Content |
|---|---|---|---|
| Real-time | CEO | C-suite | Urgent direction changes |
| Weekly | C-suite | Teams | Priorities, context |
| Monthly | CEO | All | Company update, strategy |
| Quarterly | CEO | All | OKR review, next quarter priorities |

### Lateral (Collaboration & Handoffs)
| Protocol | Standard |
|---|---|
| Handoff format | Written summary with context, completed work, open questions, next step |
| Cross-functional requests | Routed through function head with timeline + priority |
| Information sharing | Default: accessible to all; escalate to restrict |
| Decision logging | Decisions documented with rationale in Notion |

---

## Shared Metrics & Accountability

### Company North Star
- Primary metric owned by CEO, measured weekly

### Function-Level Metrics
| Function | Primary KPI | Owner |
|---|---|---|
| Engineering | Deployment frequency, incident rate | CTO |
| Product | Feature adoption, NPS | PM |
| Marketing | MQL volume, CAC | CMO |
| Sales | ARR, quota attainment | VP Sales |
| Customer Success | NRR, churn rate | COO |
| Operations | Process efficiency, cost per unit | COO |
| Finance | Runway, gross margin | CFO |
| Analytics | Dashboard adoption, data quality | COO |

---

## Decision Rights Matrix (RACI)

### Key Decisions

| Decision | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Product roadmap | PM | CEO | CTO, Sales, CS | All |
| Hire/fire | HR | CEO/Manager | Legal | Finance |
| Marketing budget | CMO | CEO | Finance | Marketing team |
| Technical architecture | CTO | CEO | Engineers | PM |
| Pricing changes | PM + CMO | CEO | Sales, CS, Finance | All customer-facing |
| Partnership deals | BizDev | CEO | Legal, CTO | CMO, Sales |
| Security incident response | CTO + Security | CEO | Legal | Board |
| International expansion | Int'l Manager | CMO + CEO | Legal, Finance | All |
| Data privacy policy | Legal + Compliance | CEO | CTO, Engineering | All |
| Sales process changes | RevOps + VP Sales | COO | AEs, SDRs | All Sales |
