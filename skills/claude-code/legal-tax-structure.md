# Legal & Tax Structure — Entity Optimization for Solo Founders

## Auto-Trigger (No Slash Command Needed)
Fires automatically when:
- "what entity should I form", "LLC vs S-Corp", "should I incorporate"
- "self-employment tax", "quarterly taxes", "SE tax"
- "should I set up an S-Corp", "S corporation election"
- "how much should I pay myself", "salary vs distributions"
- "EIN", "business bank account" (early operational setup)
- "Dutch BV", "Estonian OÜ", "international structure", "digital nomad" + business context
- Founder at $50K+ ARR mentioned WITHOUT entity structure confirmed
- TAX-STRUCTURE auto-trigger from CLAUDE.md

---

**Usage**: `/tax-structure` or fires automatically

At $50K+ ARR as a sole proprietor, the entity structure decision is costing $5,000–$15,000/year in avoidable taxes. That's more than all founder tool subscriptions combined.

---

## MANDATORY DISCLAIMER

```
⚠️ TAX & LEGAL DISCLAIMER
This is educational information, not legal or tax advice.
Tax law varies by jurisdiction, changes annually, and depends entirely on your specific facts.
The numbers here are US-based estimates for illustration purposes.
Before any entity formation or tax strategy decision:
consult a licensed CPA and business attorney in your jurisdiction.
This file helps you ask better questions — your advisors provide the answers.
```

This disclaimer must appear at the start of every output from this skill. No exceptions.

---

## The Core Insight: The SE Tax Leak

As a sole proprietor, ALL net profit is subject to self-employment tax (15.3% on the first ~$168,600, 2.9% above that). There is no separation between earned income and investment return from your business.

The S-Corp structure creates that separation:
- **Salary portion**: subject to payroll taxes (SE equivalent)
- **Distribution portion**: NOT subject to SE tax
- **Annual savings**: the SE tax on the distribution portion — typically $3,000–$15,000+/year

This is not a loophole. It is Congress-intended tax treatment for legitimate business owners.

---

## Tax Optimization Ladder — 4 Stages

### STAGE 1: $0–$35,999 Net Profit (Sole Proprietor)
**Default status — no entity action required yet.**

What you should do now:
- Open a dedicated business checking account (separate personal/business now)
- Apply for a free EIN from IRS.gov (takes 5 minutes online)
- Track ALL business expenses from day 1: software, hardware, home office, phone, professional development
- Set aside 25-30% of each payment received for taxes
- Set up quarterly estimated tax payments to avoid underpayment penalties

Quarterly estimated tax calendar (US):
- Q1 income (Jan-Mar) → due April 15
- Q2 income (Apr-May) → due June 17
- Q3 income (Jun-Aug) → due September 16
- Q4 income (Sep-Dec) → due January 15

**Safe harbor rule (memorize this)**: Pay 100% of your prior year tax (or 110% if prior year income exceeded $150K). You will owe no underpayment penalty regardless of this year's actual income. This is the most important quarterly tax concept for growing founders.

**Kill signal to stay at Stage 1**: Net profit stays below $36K consistently. S-Corp administrative costs ($1,500–$4,000/year) exceed tax savings.

---

### STAGE 2: $36,000–$99,999 Net Profit (S-Corp Election Zone)

**This is the decision point. Run the calculator before deciding.**

**S-Corp Decision Calculator**:
```
ANNUAL NET PROFIT: $[X]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AS SOLE PROPRIETOR:
SE tax (15.3% on net profit): $[X × 0.153]
Total SE tax: $[result]

AS S-CORP:
Reasonable salary (typically 40-60% of profit): $[Y]
SE tax on salary only: $[Y × 0.153]
Distribution (profit minus salary): $[X - Y]
SE tax on distribution: $0
Annual SE tax as S-Corp: $[Y × 0.153]

ANNUAL TAX SAVINGS: $[(X-Y) × 0.153]
S-Corp setup cost (one-time): ~$800–$2,000
Annual accounting increase: ~$1,500–$3,500/yr
NET ANNUAL SAVINGS: $[savings - ongoing costs]
BREAK-EVEN: $[setup cost ÷ net annual savings] months
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERDICT: Worth it if NET ANNUAL SAVINGS > $2,000
```

**Example at $60K net profit**:
- Sole prop SE tax: $9,180
- S-Corp with $36K salary: SE tax = $5,508; distribution = $24K; SE tax on distribution = $0
- Annual savings = $3,672
- Ongoing accounting increase = ~$1,500
- Net annual savings = ~$2,172
- Break-even on setup = ~9 months
✅ S-Corp election makes sense.

**The "Reasonable Compensation" Rule (most audited S-Corp issue)**:
The IRS requires S-Corp owners to pay themselves a salary that reflects market rate for their role.
- Too low → IRS reclassification risk (back taxes + penalties + interest)
- How to document: LinkedIn salary data, BLS Occupational Employment Statistics, industry surveys
- Rule of thumb: 40-60% of S-Corp profit as salary is generally defensible
- WRITE IT DOWN: document the reasoning, comparable market data, board minutes (even as a solo "board")

**S-Corp election mechanics**:
1. Form an LLC (or corporation) in your state
2. Elect S-Corp tax treatment via IRS Form 2553
3. Set up payroll (Gusto is the standard for solo S-Corps: ~$50/month)
4. Run actual paychecks with proper withholding
5. File separate S-Corp tax return (Form 1120-S) in addition to personal return

**Kill signal for S-Corp at Stage 2**: If your CPA quotes >$4,000/year in additional accounting fees AND your net savings are <$4,000 → delay until Stage 3. The math must work.

---

### STAGE 3: $100,000–$499,999 Net Profit (Full Optimization)

**S-Corp is running. Now maximize it.**

**Retirement Account Maximization** (most underpowered tool for solo founders):

Solo 401(k) — the best option for most solo founders at this stage:
- Employee contribution: $23,000/year (2024); $30,500 if age 50+
- Employer contribution (as S-Corp): up to 25% of W-2 salary
- Combined maximum: $69,000/year (2024)
- Example: $80K salary, max employee $23K, employer 25% = $20K → total $43K/year sheltered
- Contributions are pre-tax (traditional) or post-tax (Roth option available)
- Setup: Fidelity, Vanguard, or Schwab — free to establish

SEP-IRA — simpler but less powerful:
- 25% of compensation, max $69,000/year (2024)
- No catch-up contributions
- Cannot contribute as employee (only employer contributions)
- Easier to set up and maintain than Solo 401(k)

**Health Insurance Deduction** (100% for S-Corp owners):
- Health insurance premiums paid by S-Corp for owner: add to W-2 wages, then deduct on personal return
- Net effect: 100% deductible vs. itemized deduction with AGI floor for individuals
- Family coverage included

**Home Office Deduction**:
- Dedicated space requirement: the room/area must be used REGULARLY and EXCLUSIVELY for business
- Calculation: business sq ft ÷ total home sq ft × home expenses (rent, utilities, insurance, repairs)
- Simplified method: $5/sq ft up to 300 sq ft ($1,500 max)
- Own your home: also captures mortgage interest, property tax, depreciation — use actual expense method

**Vehicle**:
- Standard mileage: 67 cents/mile (2024) — simpler, no depreciation tracking needed
- Actual expense: track all car expenses × business-use percentage — better if high business use
- Log business miles: date, destination, purpose (IRS requires contemporaneous records)

**Commonly missed deductions**:
- Business books, courses, conferences: 100%
- Software subscriptions: 100%
- Phone business-use percentage: typically 50-80% for founder phones
- Business meals: 50% (must document: date, attendees, business purpose)
- Startup costs: up to $5,000 deductible Year 1, remainder amortized over 15 years

**Kill signal for Stage 3 optimization**: If effective tax rate (total tax ÷ total income) is NOT declining year-over-year as income grows → the optimization strategy has a leak. CPA review needed.

---

### STAGE 4: $500,000+ Net Profit (Advanced — Requires Specialist Counsel)

**This stage requires a tax attorney AND a CPA. Not just a CPA.**

Overview of options (educational only — not a recommendation):

**C-Corp consideration**:
- Qualified Small Business Stock (QSBS) exclusion: up to 100% exclusion on capital gains from C-Corp stock held >5 years, up to $10M or 10x basis (Section 1202)
- Relevant IF: you're on a venture-backed path and expect a significant exit
- NOT relevant for: lifestyle/bootstrapped businesses, S-Corps (QSBS requires C-Corp)
- Corporate tax rate: 21% flat vs. individual rates up to 37%

**International structure options** (location-independent founders only):
- **Estonian e-Residency / OÜ**: 0% corporate tax on retained/reinvested profits; 20% flat tax on distributions. Attractive for founders reinvesting heavily. Requires genuine business management connection to Estonia. Annual costs: ~€200-400. NOT a tax avoidance tool — you still owe US taxes as a US person on worldwide income (FBAR, FATCA).
- **Dutch BV**: More EU enterprise credibility. Higher setup (~€1,500+). 15% corporate tax rate on first €200K (2024), 25.8% above. Better for SaaS with EU enterprise customers.
- **UK Ltd**: 25% corporation tax on profits >£250K; 19% below £50K (marginal relief between). Post-Brexit complicates EU sales but still commonly used.
- **CAUTION — US person abroad**: Controlled Foreign Corporation (CFC) rules, GILTI tax, Subpart F income — a US citizen/resident with a foreign corporation can end up paying MORE total tax, not less, without expert planning. The penalty structure is severe. This is not a DIY project.

**Family employment**:
- Legitimate wages to family members (spouse, children) for actual work performed
- Children's wages: up to Standard Deduction ($14,600 in 2024) potentially tax-free
- Must be reasonable compensation for actual work, documented properly
- Shifts income from high-bracket parent to lower/zero-bracket family member

---

## The Quarterly Tax System: Make It Automatic

The single biggest cause of founder tax stress: not paying quarterly estimates.
The fix is a one-time 20-minute setup:

1. Open a dedicated "Tax Reserve" savings account (separate from operating account)
2. Every time revenue hits the operating account, transfer 25-30% to Tax Reserve
3. On quarterly due dates, pay from Tax Reserve to IRS and state
4. Year-end: any excess in Tax Reserve = refund or next year's Q1 payment

This converts a painful annual event into a painless automated system.

---

## Stage-Calibrated Output

```
TAX-STRUCTURE ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ DISCLAIMER: Educational only. Consult CPA + attorney before deciding.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current stage: [Stage 1/2/3/4] based on [estimated ARR/net profit]
Primary recommendation: [specific action]
Tax savings estimate: [calculation or range]
Setup cost: [one-time + ongoing]
Net savings after costs: [range]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT ACTION: [specific, doable in next 7 days]
KILL SIGNAL: [specific data that means this recommendation is wrong]
```

**At $0–35K**: "Not yet. Set up business account + EIN + quarterly estimates. Ready when you hit $36K."
**At $36K–100K**: "Run the S-Corp calculator. If net savings >$2K, file Form 2553. Here's what to tell your CPA."
**At $100K–500K**: "S-Corp running? Now maximize: Solo 401(k) + health insurance deduction. These are the two highest-leverage moves."
**At $500K+**: "You need both a CPA and a tax attorney. Here's what questions to bring them."

---

## Questions to Bring to Your CPA

At Stage 2+, go into your CPA conversation with these specific questions:
1. "Given my projected net profit of $[X], what's the S-Corp election worth to me net of your fees?"
2. "What do you think is a defensible 'reasonable compensation' for someone in my role?"
3. "Can you set up a Solo 401(k) for me and maximize my contribution?"
4. "Am I capturing the home office deduction correctly?"
5. "What am I missing that founders at my revenue level typically miss?"

A good CPA answers all five without blinking. A CPA who hedges on every question without doing the math for you is not the right CPA for this stage.

KILL SIGNAL for this skill: If founder at $50K+ ARR implements S-Corp and net savings is less than projected by >50% → the "reasonable compensation" was set too high, or accounting costs were undercounted. Revisit with CPA.
