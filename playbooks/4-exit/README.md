# Phase 4: EXIT

> Build to last, or build to sell — both require the same foundation.

## Goal

Maximize the value of what you've built through:
- Acquisition (2-10x ARR for micro-SaaS, 5-15x ARR for growth SaaS)
- Recapitalization (PE minority investment, keep running)
- IPO/SPAC (rare for solo, but possible at scale)
- Lifestyle business (ongoing cash flow, no exit)

## Exit Readiness Checklist

### Financial Documentation (3-6 months pre-exit)
- [ ] Clean P&L (Stripe + accounting software)
- [ ] Revenue attribution by channel
- [ ] Cohort analysis (retention by signup month)
- [ ] CAC/LTV by acquisition channel
- [ ] MRR growth chart (12+ months)
- [ ] Churn analysis and explanation
- [ ] Operating expenses breakdown
- [ ] Owner salary adjusted (normalized EBITDA)

### Technical Documentation
- [ ] Architecture diagram (current state)
- [ ] Technology stack documentation
- [ ] Database schema + data dictionary
- [ ] API documentation
- [ ] Deployment runbook
- [ ] Security audit (or recent pen test)
- [ ] Dependencies audit (no critical vulnerabilities)
- [ ] Codebase README + onboarding guide

### Business Documentation
- [ ] Customer list (anonymized for initial discussions)
- [ ] Customer concentration analysis (<20% from single customer)
- [ ] Key contracts (customer agreements, vendor agreements)
- [ ] IP ownership (all contractors signed IP assignment)
- [ ] Domain and trademark ownership
- [ ] No pending legal issues

### Operational Documentation
- [ ] Processes documented (can run without you in 30 days)
- [ ] Customer support playbooks
- [ ] Onboarding and offboarding procedures
- [ ] Vendor relationships documented
- [ ] SLAs and their current performance

## Valuation Framework

### Multiple Expectations by Profile

| ARR | Churn | Growth | Multiple Range |
|-----|-------|--------|----------------|
| <$500K | >5%/mo | <20% YoY | 2-4x ARR |
| <$500K | <3%/mo | 20-50% YoY | 4-6x ARR |
| $500K-2M | <3%/mo | 50%+ YoY | 5-8x ARR |
| $2M-5M | <2%/mo | 50%+ YoY | 6-10x ARR |
| $5M+ | <2%/mo | 100%+ YoY | 8-15x ARR |

**Premium drivers** (+20-40% to base):
- Strong NRR (>110%) → Expansion revenue story
- Vertical SaaS (sticky, regulated markets)
- High gross margins (>80%)
- No key-person risk (processes documented)
- Strategic value to buyer

**Discount drivers** (-20-50%):
- Key-person dependency (YOU can't leave)
- High customer concentration (>30% single customer)
- High churn (>5% monthly)
- Undocumented code / processes
- Revenue declining

### Buyer Types

**PE Consolidators** (55% of micro-SaaS deals):
- Timeline: 45-90 days
- Multiple: 3-5x ARR (lower but faster)
- Operators: MicroAcquire, Acquire.com, FE International, Flippa
- What they want: Profitability, processes, low churn

**Strategic Buyers** (35% of deals):
- Timeline: 3-6 months
- Multiple: 5-10x ARR (higher but slower)
- Motivation: Distribution, technology, customer base
- What they want: Strategic fit, team/tech/customers

**Acquihires** (<10%):
- Timeline: 1-3 months
- Multiple: 1-2x ARR
- Motivation: Talent and technology
- Outcome: Often employment contract, not true exit

## The Exit Process

### 6 Months Before Exit

1. **Clean up finances**:
   - Move to professional bookkeeping (Pilot.com)
   - Separate personal/business expenses
   - Document all one-time expenses vs recurring

2. **Reduce key-person risk**:
   - Document every process
   - Set up automated customer support
   - Ensure product runs without active development

3. **Optimize the metrics that matter to buyers**:
   - Reduce churn (the #1 value driver)
   - Increase net revenue retention
   - Grow EBITDA margins

### 3 Months Before Exit

4. **Prepare your Confidential Information Memorandum (CIM)**:
   - Business overview and story
   - Market opportunity
   - Product and technology
   - Customer metrics
   - Financial summary (3 years historical)
   - Growth opportunities for buyer

5. **Create the data room**:
   ```
   /data-room/
   ├── financials/
   │   ├── p-and-l-3yr.xlsx
   │   ├── mrr-cohort-analysis.xlsx
   │   └── financial-model.xlsx
   ├── legal/
   │   ├── incorporation-docs/
   │   ├── customer-contracts/
   │   └── ip-assignments/
   ├── technical/
   │   ├── architecture-diagram.pdf
   │   └── tech-debt-assessment.md
   └── operations/
       ├── runbooks/
       └── vendor-agreements/
   ```

### Exit Execution

6. **List on marketplaces** (parallel outreach):
   - Acquire.com (PE buyers)
   - FE International (if >$100K ARR)
   - Quiet Light Brokerage (if >$500K SDE)
   - Empire Flippers (if strong metrics)

7. **Direct outreach** to strategic buyers:
   - Companies that compete in adjacent space
   - Potential acquirers in your customer's stack
   - PE firms focused on your vertical

8. **Negotiate**:
   - Always get 3+ competing offers
   - Structure: upfront vs earnout (prefer upfront)
   - Employment agreement terms (if required)
   - IP transfer and non-compete terms

## Exit Agent Swarm

**Deploy**: `framework/swarms/exit-swarm.yaml`

**Valuation Agent** → Models different scenarios and multiples
**Documentation Agent** → Helps write CIM and data room docs
**Buyer Research Agent** → Identifies and scores potential acquirers
**Negotiation Coach Agent** → Prep for buyer questions and counters

## Outputs

- [ ] `exit/valuation-model.xlsx` — Multi-scenario valuation
- [ ] `exit/cim-draft.md` — Confidential Information Memorandum
- [ ] `exit/data-room-checklist.md` — Document preparation tracker
- [ ] `exit/buyer-list.md` — Potential acquirer pipeline
- [ ] `exit/negotiation-prep.md` — Q&A preparation

## The Alternative: Don't Exit

If you're generating $50K+ MRR with low churn and high margins, consider:

**Keep and compound**:
- At $50K MRR (60% margins) = $360K/year profit
- At $150K MRR = $1M+/year profit
- Hire a part-time operator to run day-to-day
- Start building your second product

The best exit is often: don't exit.
