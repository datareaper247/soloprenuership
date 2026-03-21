# Ops — Business Operations Documents & Processes

## Auto-Trigger (No Slash Command Needed)
Fires automatically when founder says: "document this process", "SOP for X", "systematize X", "I keep doing X manually", "how to delegate X"

---


**Usage**: `/ops [command] "[context]"`

Produces professional-grade operational documents — SOPs, legal templates, financial models, process audits, and hiring documents — ready for immediate use.

---

## Solo Founder Ops Hierarchy

Not all ops work is created equal. Most founders use this skill too late (or too early).

| Stage | High value | Skip for now |
|-------|-----------|-------------|
| $0–$5K MRR | `financial-model` (unit economics sanity check), `sop` (your own repeatable processes) | `compliance`, `hiring`, `process-audit` |
| $5–$20K MRR | Add `legal` (contractor agreements, basic SaaS ToS) | `compliance` (GDPR/SOC2), complex `hiring` docs |
| $20–$50K MRR | Add `process-audit` (delegate before hiring), first hire `hiring` doc | `compliance` audits |
| $50K+ MRR | All commands relevant | — |

⚠️ If you're at <$20K MRR asking for `compliance` (GDPR, SOC 2): flag — **compliance frameworks are real but premature.** A 5-person team cannot pass SOC 2 audit, and GDPR basics (privacy policy, data processing) are covered by `legal` templates. Don't let compliance theater block shipping.

**For early-stage founders**: The highest-leverage ops move is writing your first SOP for a process you do 10+ times per month. Document once, delegate or automate later. Start there.

---


## Commands

### `sop` — Standard Operating Procedure
**Usage**: `/ops sop "[process name and context]"`

Creates a complete, executable SOP that any team member can follow without prior knowledge.

#### SOP Design Principles
- **Atomic steps**: Each step is one action, not two
- **Decision trees**: If X then Y, if not X then Z — cover the branches
- **Time estimates**: How long each step takes (sets expectations)
- **Ownership**: Who does what step
- **Checkpoints**: Quality gates embedded in the process
- **Escalation paths**: What to do when something goes wrong

#### Output Format
```
STANDARD OPERATING PROCEDURE
==============================
Process Name: [Name]
Version: 1.0
Owner: [Role responsible for this SOP]
Created: [date]
Last Updated: [date]
Next Review: [date, typically 6 months]

PURPOSE
[1-2 sentences: what this process accomplishes and why it matters]

SCOPE
Applies to: [Which teams/roles follow this]
Does NOT apply to: [Exclusions if any]
Frequency: [How often this runs — daily/weekly/per-event]

PREREQUISITES
- [Access/tool/permission needed before starting]
- [Data or context needed]
- [Prior process that must complete first]

ROLES
| Role | Responsibilities in this process |
|------|----------------------------------|
| [Role 1] | [What they do] |
| [Role 2] | [What they do] |

PROCESS STEPS

PHASE 1: [Phase Name]
Estimated time: X minutes

Step 1.1: [Action — verb first]
  Who: [Role]
  How: [Specific instructions — tool, where to click, what to enter]
  Expected output: [What should exist or be true after this step]
  Time: ~X minutes
  ⚠️ Common mistake: [What people often get wrong]

Step 1.2: [Action]
  Who: [Role]
  How: [Instructions]

  IF [condition A]:
    → [Sub-step A]
  IF [condition B]:
    → [Sub-step B]

Step 1.3: [Quality check]
  Who: [Role]
  Check: [What to verify]
  If check fails: [Escalation path]

PHASE 2: [Phase Name]
...

PHASE 3: [Phase Name]
...

COMPLETION CHECKLIST
[ ] [Deliverable 1 exists/is completed]
[ ] [Deliverable 2]
[ ] [Handoff to next step/person completed]
[ ] [Record updated in [system]]

ESCALATION PATH
Issue type 1: → Escalate to [Role] via [channel] within [timeframe]
Issue type 2: → See [linked runbook or resource]
After-hours emergency: → [on-call procedure]

RELATED DOCUMENTS
- [Link to related SOP]
- [Template referenced in this SOP]
- [Training material]

CHANGELOG
| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | [date] | Initial version | [name] |
```

---

### `legal` — Legal Document Templates
**Usage**: `/ops legal "[document type] for [context]"`

Document types: nda, contractor-agreement, terms-of-service, privacy-policy, employment-offer, consulting-agreement, saas-agreement, data-processing-agreement

**Important disclaimer to include**: These are templates and starting points. All legal documents should be reviewed by qualified legal counsel before use. This is not legal advice.

#### NDA Template (Mutual)
```
MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is entered into as of [DATE]
("Effective Date") between [COMPANY A], a [state] [entity type] ("Party A"),
and [COMPANY B], a [state] [entity type] ("Party B").

1. DEFINITION OF CONFIDENTIAL INFORMATION
"Confidential Information" means any non-public information that one party
("Disclosing Party") discloses to the other party ("Receiving Party") in
connection with [PURPOSE], whether disclosed verbally, in writing, or by any
other means, and that is designated as confidential or that reasonably should
be understood to be confidential given the nature of the information and
circumstances of disclosure.

2. EXCLUSIONS
Confidential Information does not include information that:
(a) was or becomes publicly known through no breach of this Agreement;
(b) was rightfully known by Receiving Party before disclosure;
(c) is rightfully received from a third party without restriction;
(d) was independently developed by Receiving Party without use of Confidential Information;
(e) is required to be disclosed by law or court order (with prompt prior written notice).

3. OBLIGATIONS
Each party agrees to: (a) maintain the confidentiality of the other party's
Confidential Information; (b) not disclose Confidential Information to third
parties without prior written consent; (c) use Confidential Information solely
for evaluating [PURPOSE]; (d) apply at least the same standard of care used to
protect its own confidential information, but not less than reasonable care.

4. TERM
This Agreement shall remain in effect for [2 years] from the Effective Date.
Confidentiality obligations survive termination for [3 years].

5. RETURN OF INFORMATION
Upon request, each party shall promptly return or certify destruction of all
Confidential Information and copies thereof.

6. REMEDIES
Each party acknowledges that breach would cause irreparable harm and that
monetary damages would be inadequate. Either party may seek equitable relief
without posting bond or other security.

7. GENERAL
This Agreement: (a) constitutes the entire agreement regarding confidentiality;
(b) may only be amended in writing signed by both parties; (c) shall be governed
by the laws of [State]; (d) is not assignable without written consent.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

[COMPANY A]                          [COMPANY B]
By: ___________________________      By: ___________________________
Name: _________________________      Name: _________________________
Title: ________________________      Title: ________________________
Date: _________________________      Date: _________________________
```

#### SaaS Terms of Service Key Sections Outline
```
SAAS AGREEMENT STRUCTURE
=========================
[This outline should be filled in with your specifics]

1. DEFINITIONS
   - "Service" definition
   - "Customer Data" definition
   - "Users" definition

2. GRANT OF LICENSE
   - Subscription grant (non-exclusive, non-transferable)
   - User limits
   - Use restrictions (no reverse engineering, no competitive use)

3. CUSTOMER OBLIGATIONS
   - Acceptable use policy
   - Account security responsibility
   - Accurate information requirement

4. FEES AND PAYMENT
   - Payment terms
   - Auto-renewal terms
   - Price change notice period
   - Late payment consequences

5. INTELLECTUAL PROPERTY
   - Your IP ownership
   - Customer data ownership (they own their data)
   - Feedback license

6. CONFIDENTIALITY
   - Mutual obligations
   - Exceptions

7. DATA PRIVACY
   - Reference to Privacy Policy
   - DPA reference if applicable
   - Data retention and deletion

8. WARRANTIES AND DISCLAIMERS
   - Uptime SLA (if offered)
   - Warranty disclaimers

9. LIMITATION OF LIABILITY
   - Cap at amounts paid in last 12 months (standard)
   - Exclusion of consequential damages

10. INDEMNIFICATION
    - You indemnify customer for IP infringement
    - Customer indemnifies you for misuse

11. TERM AND TERMINATION
    - Subscription terms
    - Termination for cause
    - Effect of termination (data export period)

12. GENERAL
    - Governing law
    - Dispute resolution
    - Force majeure
    - Entire agreement

⚠️ Engage legal counsel to draft the full text.
```

---

### `compliance` — Compliance Documentation
**Usage**: `/ops compliance "[standard: gdpr/ccpa/soc2/hipaa] for [product context]"`

#### GDPR Compliance Checklist
```
GDPR COMPLIANCE AUDIT
======================
Product/Company: [name]
Date: [date]
Auditor: [name/role]

LAWFUL BASIS FOR PROCESSING
[ ] Identified lawful basis for each data processing activity
[ ] Consent mechanisms collected properly (freely given, specific, informed, unambiguous)
[ ] Consent records maintained
[ ] Legitimate interest assessment documented where applicable

DATA INVENTORY (Record of Processing Activities - Article 30)
[ ] Data inventory completed and documented
[ ] For each data type: purpose, legal basis, retention period, recipients identified
[ ] Third-party processors documented
[ ] Data flows mapped (especially cross-border)

PRIVACY NOTICE / POLICY
[ ] Privacy policy is accessible, plain-language, comprehensive
[ ] Includes: identity of controller, purposes, legal basis, retention, rights, contact
[ ] Updated within last 12 months
[ ] Version history maintained

DATA SUBJECT RIGHTS
[ ] Right to access: process documented, respond within 30 days
[ ] Right to rectification: process in place
[ ] Right to erasure: process in place, downstream deletion considered
[ ] Right to portability: export mechanism exists
[ ] Right to object: opt-out mechanism exists
[ ] Rights request intake process: [email or web form]

DATA PROTECTION BY DESIGN
[ ] Privacy impact assessments (DPIA) conducted for high-risk processing
[ ] Data minimization practices in place
[ ] Access controls implemented (least privilege)
[ ] Encryption at rest and in transit
[ ] Pseudonymization where appropriate

VENDOR MANAGEMENT
[ ] Data Processing Agreements (DPAs) signed with all processors
[ ] Third-party processors on EU standard contractual clauses or equivalent
[ ] Vendor list maintained and audited annually

SECURITY
[ ] Security measures documented and proportionate to risk
[ ] Incident response plan in place
[ ] Breach notification process: to supervisory authority within 72 hours, to data subjects if high risk
[ ] Security testing conducted

RECORDS AND ACCOUNTABILITY
[ ] DPO appointed (if required)
[ ] Staff training completed and documented
[ ] Internal policies documented
[ ] Compliance evidence archived

GAPS IDENTIFIED
| Gap | Risk Level | Owner | Remediation Date |
|-----|-----------|-------|------------------|
| ... | High/Med/Low | | |
```

#### SOC 2 Readiness Checklist
```
SOC 2 TYPE II READINESS
========================
Trust Service Criteria: [Security / Availability / Confidentiality / Processing Integrity / Privacy]
Target audit period: [Start - End]

CC6: LOGICAL AND PHYSICAL ACCESS CONTROLS
[ ] Access provisioning process documented
[ ] Access reviews conducted quarterly
[ ] MFA enforced for all users
[ ] Privileged access controls in place
[ ] Vendor access controls in place
[ ] Physical access controls (if applicable)

CC7: SYSTEM OPERATIONS
[ ] Monitoring and alerting configured
[ ] Incident response procedures documented
[ ] Business continuity plan documented
[ ] Disaster recovery plan tested
[ ] Capacity management process in place

CC8: CHANGE MANAGEMENT
[ ] SDLC policy documented
[ ] Code review process enforced
[ ] Deployment process with approvals
[ ] Change log maintained

CC9: RISK MITIGATION
[ ] Risk assessment conducted annually
[ ] Vendor management process documented
[ ] Business associate agreements in place

EVIDENCE COLLECTION READINESS
[ ] Audit logging enabled across systems
[ ] Log retention: 12+ months
[ ] Evidence repository established
[ ] Evidence owner assigned per control

AUDIT PREPARATION TIMELINE
T-3 months: [Gap remediation]
T-2 months: [Evidence collection begins]
T-1 month: [Readiness review, pre-audit]
T: Audit period begins
```

---

### `financial-model` — Financial Model Framework
**Usage**: `/ops financial-model "[business type and context]"`

#### SaaS Financial Model Structure
```
SAAS FINANCIAL MODEL
=====================
Company: [name]
Model date: [date]
Projection period: [3 years]
Base currency: USD

ASSUMPTIONS TAB

PRICING
- Plan A: $X/month (target customer: [ICP])
- Plan B: $X/month
- Annual discount: X%
- Average Contract Value (ACV): $X

GROWTH INPUTS
- Starting MRR: $X
- Month 1 new customers: X
- Monthly growth rate: X% (ramp: X% → Y% → Z%)
- Churn rate: X% monthly (target: <Y%)
- Expansion revenue: X% of base MRR monthly

CAC AND PAYBACK
- Blended CAC: $X per customer
- Payback period: X months
- LTV:CAC ratio target: X:1

HEADCOUNT PLAN
- Month 1 headcount: X
- New hires by month: [schedule]
- Average fully-loaded cost: $Xk/year
- Benefits/payroll tax load: X%

COST STRUCTURE
- COGS (hosting, support): X% of revenue
- Gross margin target: X%
- S&M: $X/month + X% of revenue
- R&D: $X/month
- G&A: $X/month

REVENUE MODEL

| Month | Beginning MRR | New MRR | Churn | Expansion | Ending MRR | Customers |
|-------|--------------|---------|-------|-----------|------------|-----------|
| 1 | | | | | | |
...

UNIT ECONOMICS

| Metric | Current | Month 12 | Month 24 | Month 36 |
|--------|---------|----------|----------|----------|
| MRR | | | | |
| ARR | | | | |
| Gross Margin % | | | | |
| CAC | | | | |
| LTV | | | | |
| LTV:CAC | | | | |
| Payback Period | | | | |
| Churn Rate | | | | |
| Net Revenue Retention | | | | |

P&L SUMMARY

| | Month 1 | Month 6 | Month 12 | Month 24 | Month 36 |
|--|---------|---------|----------|----------|----------|
| Revenue | | | | | |
| COGS | | | | | |
| Gross Profit | | | | | |
| S&M | | | | | |
| R&D | | | | | |
| G&A | | | | | |
| EBITDA | | | | | |
| Burn Rate | | | | | |

CASH FLOW
- Starting cash: $X
- Monthly burn (Month 1): $X
- Cash out date (current funding): Month X
- Funding needed to reach break-even: $X

KEY MILESTONES
- $10k MRR: Month X
- $100k MRR: Month X
- Break-even: Month X
- $1M ARR: Month X

SENSITIVITY ANALYSIS
| Scenario | Growth Rate | Churn | Break-Even |
|----------|------------|-------|------------|
| Bear | X% | X% | Month X |
| Base | X% | X% | Month X |
| Bull | X% | X% | Month X |
```

---

### `process-audit` — Business Process Audit
**Usage**: `/ops process-audit "[process or department]"`

#### Output Format
```
PROCESS AUDIT REPORT
=====================
Process: [Name]
Department: [Name]
Audit date: [date]
Auditor: [name/role]

PROCESS OVERVIEW
- Purpose: [what this process is supposed to achieve]
- Frequency: [how often it runs]
- Stakeholders: [who is involved]
- Systems: [tools and systems used]

CURRENT STATE MAPPING

Step 1: [Action]
  Owner: [role]
  Input: [what triggers/feeds this step]
  Output: [what this step produces]
  Time: [actual time taken]
  Issues found: [problems, inconsistencies, gaps]

[Repeat for all steps]

TOTAL PROCESS TIME: X hours/minutes
WAIT TIME (non-value-add): X hours/minutes (Y% of total)
VALUE-ADD TIME: X hours/minutes (Z% of total)

FINDINGS

CRITICAL ISSUES (causing business risk or significant inefficiency)
1. [Issue]: [description, impact, evidence]
   Root cause: [why this happens]
   Recommendation: [specific fix]
   Effort: [S/M/L]
   Impact: [High/Med/Low]

HIGH IMPACT IMPROVEMENTS
1. [Opportunity]: [description]
   Recommendation: [what to do]
   Expected outcome: [time saved, risk reduced, quality improved]

AUTOMATION OPPORTUNITIES
| Step | Current approach | Automation option | Est. time saved |
|------|-----------------|------------------|-----------------|
| ... | Manual | [tool/approach] | X hrs/week |

BENCHMARKS
| Metric | Current | Industry benchmark | Gap |
|--------|---------|-------------------|-----|
| Cycle time | X days | Y days | Z days |
| Error rate | X% | Y% | |
| Cost per transaction | $X | $Y | |

RECOMMENDED IMPROVEMENTS (Priority-ordered)
1. [Quick win — < 1 week effort]
2. [Medium effort — 1-4 weeks]
3. [Major redesign — 1-3 months]

30-DAY ACTION PLAN
Week 1: [Specific actions]
Week 2: [Specific actions]
Week 3: [Specific actions]
Week 4: [Review and measure]

SUCCESS METRICS
- Cycle time: from X to Y days
- Error rate: from X% to Y%
- Team time freed: X hours/week
```

---

### `hiring` — Hiring Process & Job Description
**Usage**: `/ops hiring "[role title and context]"`

#### Job Description Template
```
JOB DESCRIPTION: [ROLE TITLE]
==============================
Team: [Department]
Location: [Remote / Hybrid / On-site + location]
Compensation: $[X] - $[Y] + [equity range] + benefits
Reports to: [Title]
Hiring manager: [Name, Title]

ABOUT THE ROLE (2-3 sentences — sell the opportunity)
[What is exciting about this role, what they'll own, what impact they'll have]

WHAT YOU'LL DO
[Responsibilities — action-verb led, specific, not generic]
- [Key responsibility 1 — measurable]
- [Key responsibility 2]
- [Key responsibility 3]
- Within 30 days: [what first 30 days look like]
- Within 90 days: [early milestones]

WHAT WE'RE LOOKING FOR
Must-haves (dealbreakers if absent):
- [Requirement 1 — be specific, not generic]
- [Requirement 2]
- [Requirement 3]

Nice-to-haves (bonus, not required):
- [Bonus skill 1]
- [Bonus skill 2]

NOT required (things that often appear in JDs for this role but we don't need):
- [Common thing that's actually unnecessary]

WHAT WE OFFER
- Compensation: $X - $Y base + equity ([X]% - [Y]% range, [vesting schedule])
- Benefits: [specific list — health, 401k, PTO, etc.]
- Working style: [remote-first / async-first / specific hours policy]
- Growth: [what career progression looks like]

ABOUT [COMPANY]
[3-4 sentences: who we are, what we do, stage, why it's exciting]

HOW TO APPLY
[Application instructions — what to include, any specific screening questions]

---
HIRING MANAGER TOOLKIT

INTERVIEW SCORECARD: [ROLE TITLE]
===================================
Interviewer: [name]
Candidate: [name]
Round: [Screening / Technical / Culture / Executive]

Scoring: 1=Strong No, 2=No, 3=Maybe, 4=Yes, 5=Strong Yes

| Competency | Score | Evidence | Notes |
|------------|-------|----------|-------|
| [Competency 1] | | | |
| [Competency 2] | | | |
| [Competency 3] | | | |
| Culture fit | | | |
| Communication | | | |

STRUCTURED INTERVIEW QUESTIONS

Competency: [Name]
Q: "Tell me about a time when [situation relevant to competency]"
Follow-ups: "What was the hardest part?" / "What would you do differently?"
Look for: [Green flags] / [Red flags]

[Repeat for each competency]

Recommendation: [Strong Hire / Hire / No Hire / Strong No Hire]
Rationale: [2-3 sentences]

ONBOARDING CHECKLIST (first 30 days)
Week 1: [Orientation, tooling, team intros, culture]
Week 2: [Domain context, key meetings, first deliverable]
Week 3-4: [First independent project, 1:1s established]
30-day check-in: [Review against defined milestones]
```
