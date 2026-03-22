# Legal Intelligence Engine — The General Counsel Solo Founders Never Had

> **This is not legal advice. For any significant legal matter, consult a qualified attorney in your jurisdiction.**

## Auto-Trigger (No Slash Command Needed)

Fires automatically when:
- "what entity should I form" / "LLC vs C-Corp" / "should I incorporate" → entity selection protocol
- "I want to give equity to" / "co-founder equity" / "vesting schedule" → equity structure protocol
- "stock options" / "ESOP" / "hiring employees" → equity compensation guide
- "contractor vs employee" / "1099 vs W2" / "using freelancers" → classification guide
- "terms of service" / "terms and conditions" / "privacy policy" → compliance checklist
- "GDPR" / "EU users" / "data privacy" / "CCPA" → privacy compliance protocol
- "someone is using my code" / "protecting my IP" / "copied my product" → IP protection protocol
- "open source" / "MIT license" / "GPL" / "using a library" → open source license audit
- "partnership agreement" / "co-founder agreement" / "working with someone" → equity split and legal structure
- "do I need a lawyer" / "can I do this myself" → DIY vs hire decision tree
- "trademark" / "brand name" / "domain squatter" → IP and brand protection
- "83(b)" / "cap table" / "SAFE note" / "convertible note" → equity and financing instruments
- "platform ban" / "Stripe shut down" / "App Store removal" → platform dependency risk

---

## Why This Exists

Legal mistakes are the silent killer of profitable companies. They're quiet until they're catastrophic:

- **Open source time bomb**: Building on GPL or AGPL code without realizing it requires you to open-source your entire product. Discovered at acquisition — deal collapses.
- **Contractor misclassification**: Treating employees as contractors. The IRS or a state agency audits you. You owe 3 years of back payroll taxes, penalties, and benefits — easily $100K+ on a single worker.
- **Co-founder equity without vesting**: Co-founder leaves at month 3 with 50% of the company. You spend the next 3 years building their retirement fund.
- **No IP assignment**: Contractor built your core feature. They own it, not you. Discovered at Series A — term sheet pulled.
- **GDPR non-compliance**: You have 200 EU users. Someone files a complaint. Fine: 4% of global annual revenue. For a $200K ARR company, that's $8,000 minimum — plus legal costs.
- **Platform dependency without TOS compliance**: Stripe terminates your account for violating acceptable use policy. Revenue goes to zero overnight.

This engine gives you enough legal intelligence to avoid the 95% of common mistakes and to know precisely when you need a real attorney.

---

## THE ENTITY SELECTION PROTOCOL

### The Decision in Plain Language

Most solo founders spend more time choosing a font for their landing page than choosing their legal entity. Entity choice affects taxes, fundraising, liability, and exit. Get it wrong and changing it costs $5,000-$20,000 in legal and tax fees.

```
ENTITY SELECTION ENGINE (fires when entity type is questioned):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE THREE QUESTIONS:
1. Do you plan to raise venture capital? → C-Corp (Delaware)
2. Are you profitable or expect to be within 12 months? → S-Corp election on LLC
3. Are you bootstrapped with no VC plans? → LLC (your home state)

IF NONE OF THE ABOVE: Sole proprietorship only if revenue <$50K and liability is minimal.
Never build a real business as a sole proprietorship. One lawsuit = your personal assets.
```

### C-Corp (Delaware) — When to Choose It

**Use C-Corp if ANY of these are true**:
- You plan to raise VC funding (angels, seed rounds, Series A+)
- You want to issue stock options to employees (ISOs require a C-Corp)
- You're building something you intend to sell to a large strategic acquirer
- You have or plan to have international investors or co-founders

**Why Delaware specifically**:
- Delaware Chancery Court: specialized business court with 200 years of established precedent
- Investors expect it — trying to close a seed round with a Wyoming LLC creates friction
- Director-friendly laws that protect founders in governance disputes
- Easy to re-incorporate (most startups flip to Delaware C-Corp before first raise)

**The flip event**: If you start as an LLC and later want to raise VC, you will need to convert to a Delaware C-Corp. Services like Clerky (~$2,000) or a startup attorney ($5,000-$10,000) handle this. Budget for it.

**C-Corp tax reality**: C-Corps pay corporate tax (21% federal) then shareholders pay personal tax on dividends (double taxation). For a profitable bootstrapped company, this is costly. For a VC-backed growth company burning cash, it's irrelevant.

```
C-CORP CHECKLIST:
□ Delaware Secretary of State filing: ~$89 + $50/year franchise tax (minimum)
□ Registered agent: ~$50-$300/year (required if not physically in Delaware)
□ Bylaws and board resolutions (use Clerky or Stripe Atlas templates)
□ 83(b) election filed within 30 days of stock issuance (CRITICAL — see below)
□ IP assignment agreements with all founders signed at formation
□ IRS EIN application (free, takes 5 minutes at IRS.gov)
```

### LLC — When to Choose It

**Use LLC if ALL of these are true**:
- You are bootstrapped and intend to stay bootstrapped
- You are profitable or will be within 12 months
- You will not raise institutional venture capital
- You want pass-through taxation (profits taxed once at personal rate)

**Why LLCs are underrated for bootstrappers**:
- Pass-through taxation: profits appear on your personal return, no double taxation
- Flexibility: can be taxed as a sole proprietor, partnership, S-Corp, or C-Corp
- Less paperwork than a C-Corp (no required annual meetings, fewer formalities)
- Your home state LLC is fine — you don't need Delaware unless you're raising

**Multi-member LLC**: If you have a co-founder or partner, your LLC operating agreement IS your co-founder agreement. Get it right. Include: ownership percentages, decision-making authority, what happens when someone leaves, buyout provisions. DIY templates exist but this is one area where a $500 attorney review is worth it.

```
LLC FORMATION COST GUIDE:
→ DIY (Secretary of State website): $50-$500 depending on state
→ Stripe Atlas: $500 flat (Delaware LLC or C-Corp, EIN, bank account)
→ Firstbase.io: $400-$1,500 (state filings, registered agent, compliance calendar)
→ Northwest Registered Agent: $39 (formation) + $125/year (registered agent)
→ Attorney-formed: $500-$2,000 (worth it for multi-founder LLCs)
```

### S-Corp Election — The Tax Efficiency Layer

**What it is**: An LLC or C-Corp can elect S-Corp status with the IRS. S-Corps allow you to split income into "salary" and "distributions." You pay self-employment tax (15.3%) only on the salary portion, not the distributions.

**When it makes sense**: When you are paying yourself $60K+ per year in profit. The tax savings on a $150K profit year can be $10,000-$20,000.

**The math example**:
```
S-CORP TAX SAVINGS CALCULATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Without S-Corp (single-member LLC):
→ $150K profit = $150K subject to 15.3% SE tax + income tax
→ SE tax alone: $150K × 15.3% = $22,950

With S-Corp election:
→ Set "reasonable salary": $80K (IRS requires this to be market-rate)
→ $80K salary: subject to 15.3% SE tax = $12,240
→ $70K distribution: NOT subject to SE tax
→ SE tax savings: $22,950 - $12,240 = $10,710/year

Break-even: S-Corp adds ~$1,500-$2,500/year in accounting complexity.
Worthwhile at: $60K+ in annual profit.
```

**How to elect**: File IRS Form 2553 within 75 days of incorporation or by March 15 for current tax year. Miss the deadline and you wait until next year.

---

## IP PROTECTION PROTOCOL

### The Four IP Types and What They Protect

```
IP PROTECTION MAP (fires when IP protection is mentioned):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COPYRIGHT:
→ Protects: Code, written content, designs, UI elements, documentation
→ When created: Automatically at creation (no registration required)
→ Duration: Creator's lifetime + 70 years
→ Register? Optional, but registration ($65 at copyright.gov) required to sue for statutory damages
→ Startup action: Use copyright notices (© 2026 YourCompany) on all materials

TRADEMARK:
→ Protects: Brand name, logo, tagline — used in commerce
→ When created: Common law rights from first commercial use (weak)
→ Registered trademark: ~$250-$350 per class at USPTO.gov (strong, nationwide)
→ Duration: 10 years, renewable forever
→ Startup action: Search USPTO before naming your company. File when you have product-market fit.

TRADE SECRET:
→ Protects: Algorithms, customer lists, processes, formulas kept confidential
→ When created: Automatically, as long as reasonable secrecy maintained
→ Duration: Indefinitely, as long as secret
→ How to protect: NDAs with contractors and employees; access controls; documented secrecy practices
→ Startup action: Have every person who touches core IP sign an NDA before sharing

PATENT:
→ Protects: Novel, non-obvious inventions with a 20-year monopoly
→ Cost: $15,000-$50,000 for full utility patent (provisional: $1,500-$3,000 buys 12 months)
→ Time: 2-5 years to grant
→ Solo founder reality: Almost never worth it. Your speed and execution is your moat, not patents.
→ Exception: Biotech, hardware, deep tech with defensible novel mechanism
```

### Open Source License Audit (The Most Overlooked Legal Risk)

This fires whenever you use open-source libraries in a commercial product. Most founders have no idea what licenses their dependencies use.

```
OPEN SOURCE LICENSE RISK MATRIX:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GREEN — Commercial use permitted, no redistribution requirements:
→ MIT License: Use freely, just keep the copyright notice
→ Apache 2.0: Use freely, document changes, patent grant included
→ BSD (2-clause, 3-clause): Use freely, keep attribution
→ ISC: MIT-equivalent

YELLOW — Use with caution, read the specific terms:
→ Mozilla Public License (MPL): Copyleft applies per FILE. Modified MPL files must be open-sourced; your proprietary code around them is fine.
→ Creative Commons (various): CC-BY and CC-BY-SA are common. CC-NC prohibits commercial use — AVOID.
→ LGPL: Library LGPL — you can link to LGPL library without open-sourcing your code, but modifications to the library itself must be released.

RED — Do not use in commercial closed-source products without legal review:
→ GPL v2/v3: If you distribute software using GPL code, your ENTIRE product must be open-sourced.
→ AGPL: GPL + network distribution. Using AGPL in a SaaS means you must open-source your entire codebase. This is the "anti-SaaS" license. MongoDB, Redis used this to force AWS to pay.
→ SSPL: Server-Side Public License (MongoDB's custom license). Designed to prevent cloud providers from using the software. Even MORE aggressive than AGPL.
→ Commercial-only licenses: Some libraries require a paid license for commercial use.

HOW TO AUDIT YOUR DEPENDENCIES:
→ npm: npx license-checker --production
→ Python: pip-licenses
→ Ruby: license_finder
→ Manual: Check each package's LICENSE file on GitHub

ACTION: Run this audit before your first enterprise deal or acquisition conversation.
Investors and acquirers will ask. Surprises here kill deals.
```

### IP Ownership — The Contractor Trap

This is where solo founders get burned most often. When a contractor builds something for you, they own the copyright by default unless you have a written work-for-hire agreement.

```
IP ASSIGNMENT CHECKLIST (fires whenever a contractor is mentioned):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For EVERY person who contributes to your codebase or product:
□ Signed IP Assignment Agreement BEFORE work begins
□ IP Assignment states: all work created under this contract is "work for hire" and owned by [Company]
□ Contractor assigns to Company any work that doesn't qualify as "work for hire"
□ Assignment covers inventions, code, designs, documentation, and derivatives
□ Include a "moral rights" waiver for international contractors

Where to get these agreements:
→ Clerky.com: $50 — best for U.S.-based contractors
→ Bonsai (hellobonsai.com): Built into contractor agreement templates
→ Docracy.com: Free templates (review with an attorney if IP is core to your product)
→ Your own attorney: $300-$500 one-time for a template you reuse

INTERNATIONAL CONTRACTORS:
→ U.S. work-for-hire doctrine doesn't apply in most other countries
→ UK, Germany, India: Contractor retains "moral rights" even with assignment
→ Use explicit IP assignment language plus moral rights waiver
→ Do NOT use Upwork or Fiverr for core IP without their individual NDA/assignment (Upwork has a default IP agreement but read it carefully)

THE ACQUISITION MOMENT: Every acquirer's due diligence will request:
→ Signed IP assignments from all contributors
→ Evidence contractors didn't bring in 3rd party IP
→ List of all open-source dependencies and their licenses
Missing any of these = delayed or failed close.
```

### Trademark Registration — Practical Guide

```
TRADEMARK REGISTRATION PROTOCOL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEFORE registering, search for conflicts:
→ USPTO TESS database (tess.uspto.gov): Free, search exact name + similar names
→ Google: "your brand name" + competitor industry
→ State trademark databases (important — state TM can block federal)

WHEN to register (not before):
→ You have a product in market (or imminent launch — Intent to Use filing)
→ You have revenue or clear PMF signal
→ The name is core to your brand (not a generic descriptive term)
→ You're in a competitive market where brand confusion is possible

HOW to file (DIY):
→ USPTO TEAS Plus: $250/class at www.uspto.gov
→ Filing is straightforward if your mark is distinctive
→ Examine: USPTO examiner reviews ~3 months after filing
→ Publication: 30-day opposition window
→ Registration: Certificate issued ~8-12 months total

Classes that matter for SaaS founders:
→ Class 42: Software as a Service, computer services, tech consulting
→ Class 35: Business services, advertising, marketing services
→ Class 9: Software products (if you sell downloadable software)

ONE-TIME cost: $250-$350 per class
Ongoing cost: $225 maintenance fee at 5-6 year mark; $325 at 9-10 year mark

Chanakya principle: "A king who does not protect his territory will lose it." Your brand name is territory. If you don't register it, a competitor can register a confusingly similar name and force you to rebrand.
```

---

## CONTRACTOR VS EMPLOYEE CLASSIFICATION GUIDE

### Why This Matters More Than Almost Any Other Legal Issue

Misclassifying employees as contractors is the #1 IRS enforcement priority for small businesses. The penalties are retroactive — going back 3 years — and include:

- Back payroll taxes (employer portion): ~7.65% of wages
- Back income tax withholding
- Interest and penalties: 20-100% of unpaid taxes
- State-level penalties (often more severe than federal)
- Potential personal liability for founders (you can't discharge this in bankruptcy)

```
CLASSIFICATION TEST — THE IRS 3-FACTOR FRAMEWORK:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEHAVIORAL CONTROL (most important):
→ Do you control HOW they do the work? → Employee signal
→ Do they set their own hours? → Contractor signal
→ Do they use your equipment and tools? → Employee signal
→ Do you provide training? → Employee signal

FINANCIAL CONTROL:
→ Are they paid a regular salary or hourly rate? → Employee signal
→ Are they paid per project? → Contractor signal
→ Do they have significant investment in their own tools/equipment? → Contractor signal
→ Can they work for other clients simultaneously? → Contractor signal
→ Are they at risk for profit and loss? → Contractor signal

TYPE OF RELATIONSHIP:
→ Is this work integral to your business? (core product) → Employee signal
→ Is this a one-time or project-based engagement? → Contractor signal
→ Is there an indefinite ongoing relationship? → Employee signal
→ Do they receive benefits (health, PTO)? → Employee signal

SAFE CONTRACTOR PROFILE:
□ Has their own business entity (LLC or Corp)
□ Works for multiple clients concurrently
□ Uses their own tools and equipment
□ Sets their own hours
□ Delivers project-based output, not hours
□ Has signed a services agreement with defined scope
□ Sends invoices (not timesheets)
```

### The California ABC Test — If You Have ANY California-Based Workers

California uses the strictest test in the U.S. A worker is an EMPLOYEE unless ALL THREE of these are true:

```
CALIFORNIA ABC TEST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A: The worker is FREE from control and direction in performing the work.
   (Same as IRS behavioral control test above)

B: The work performed is OUTSIDE the usual course of the hiring entity's business.
   → If you're a SaaS company and you hire a developer: likely employee (software IS your business)
   → If you're a SaaS company and you hire a plumber to fix your office: clearly contractor
   → This test is the hardest for tech companies to pass for technical workers

C: The worker is CUSTOMARILY ENGAGED in an independently established trade.
   → They have their own business, other clients, hold themselves out as a contractor

CALIFORNIA REALITY FOR SOLO FOUNDERS:
→ If you're a solo founder in California and you hire technical workers on an ongoing basis → likely employees
→ Enforce at the state level, not just IRS. California EDD is aggressive.
→ AB5 (Gig Economy Law) strengthened these rules in 2020
→ If working with California-based contractors on ongoing technical work: get legal advice before assuming contractor status is safe
```

### When to Convert a Contractor to an Employee

The trigger point:

```
EMPLOYEE CONVERSION SIGNAL:
→ Same person, >20 hours/week, for >3 consecutive months
→ Work is core product development (not peripheral)
→ You are directing HOW they work, not just WHAT to deliver
→ The relationship is open-ended with no defined project end date

CONVERSION COST (budget for this):
→ Payroll setup: Gusto ($40/mo + $6/person) or Rippling ($8-$16/person/mo)
→ Employer payroll taxes: ~7.65% of gross wages (FICA match)
→ Workers' compensation insurance: varies by state ($500-$5,000/year)
→ State unemployment insurance: 1-6% of wages, varies by state
→ Onboarding legal: $500-$1,000 for offer letter + employment agreement templates (one-time)

INTERNATIONAL CONTRACTORS — WHAT'S DIFFERENT:
→ No W-9 required (use W-8BEN instead)
→ No 1099 required if payment is for services performed outside the U.S.
→ BUT: Their country may have worker classification laws stricter than the U.S.
→ UK, Germany, Netherlands, Australia: all have employee-vs-contractor rules that can trigger if work is ongoing and directed
→ Use Deel, Remote.com, or Oyster HR for international contractors if the relationship is ongoing — they handle compliance in the worker's country
```

---

## EQUITY STRUCTURE GUIDE

### Co-Founder Vesting — Non-Negotiable

If you have a co-founder and no vesting schedule, you have a loaded gun pointed at your company.

```
STANDARD VESTING SCHEDULE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INDUSTRY STANDARD: 4-year vest, 1-year cliff
→ Year 1 (cliff): 25% vests as a lump sum on the 1-year anniversary
→ Years 2-4: Remaining 75% vests monthly (1/48th per month)
→ Cliff purpose: Prevents a co-founder who leaves at month 6 from keeping any equity

EXAMPLE: Two co-founders, 50% each, 4-year vest, 1-year cliff
→ Month 6: Co-founder B quits. They get 0% equity (not yet past cliff).
  Company is protected. Remaining equity goes back to option pool or is cancelled.
→ Month 14: Co-founder B quits. They keep 25% + 2/48 × 75% ≈ 28% of their 50% = 14% of company.
  Remaining ~36% is cancelled or reallocated.

WITHOUT VESTING: Co-founder B quits month 6 with 50% of company.
You build for 4 years. They own half at exit. This happens every day.

ACCELERATION CLAUSES (add these):
→ Single trigger: Full vesting accelerates if company is acquired
→ Double trigger: Full vesting accelerates if (1) acquisition AND (2) founder is terminated
  Double trigger is standard — single trigger can be problematic for acquirers
```

### The 83(b) Election — The Most Time-Sensitive Legal Action in Startups

```
83(B) ELECTION — CRITICAL 30-DAY WINDOW:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT IT IS: An IRS election that says "I want to be taxed NOW on my stock at current value,
not later when it vests (and is worth much more)."

WHY IT MATTERS:
→ Without 83(b): As your shares vest, you pay income tax on the fair market value AT VESTING.
  If stock goes from $0.001 to $10/share over 4 years, you pay income tax on $10/share value
  as each share vests. On 1M shares, that's potentially millions in ordinary income tax.

→ With 83(b): You pay income tax today on $0.001/share × 1M shares = $1,000 total.
  Future gains (from $0.001 to $10) are taxed as long-term capital gains (15-20%), not ordinary income (37%).

WHEN IT APPLIES: Only for stock subject to a vesting schedule (restricted stock).
Does NOT apply to stock options (different rules apply at exercise).

THE 30-DAY RULE: You have exactly 30 days from the date of stock issuance to file.
Miss this window and the election is gone forever. No extensions. No exceptions.

HOW TO FILE (DIY — this is one you can do yourself):
1. Write a letter to the IRS (template available at clerky.com and online for free)
2. Include: your name, SSN, description of property, date of transfer, FMV at transfer, price paid
3. Send to the IRS Service Center where you file your tax return
4. CERTIFIED MAIL with return receipt (you need proof of timely filing)
5. Send a copy to your company and attach a copy to your personal tax return for that year

COST: $0 (DIY) or $100-$300 (attorney-assisted)
RISK OF MISSING: Potentially hundreds of thousands of dollars in excess taxes at exit.
```

### Advisor Equity — Standard Ranges

```
ADVISOR EQUITY GUIDE (Carta/FAST Agreement Standard):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ADVISOR TIERS (pre-Series A):
→ Strategic Advisor (1-2 hours/month of intros and advice):
  Equity: 0.1% - 0.25%
  Vesting: 2-year vest, 6-month cliff

→ Domain Expert Advisor (4+ hours/month, deep involvement):
  Equity: 0.25% - 0.5%
  Vesting: 2-year vest, 6-month cliff

→ Operating Advisor (hands-on, weekly calls, executes tasks):
  Equity: 0.5% - 1.0%
  Vesting: 2-year vest, 6-month cliff

USE THE FAST AGREEMENT: Founder Advisor Standard Template (available at
techcrunch.com/FAST or Clerky). Free, widely accepted, founder-friendly.

WHAT TO WATCH OUT FOR:
→ Advisors who ask for >1% pre-Series A without ongoing operational commitment
→ "Advisory boards" assembled for optics with no actual engagement
→ Advisors who want cash AND equity before you have PMF
→ No cliff — if an advisor ghosts you at month 4, you should get their equity back

Chanakya's MITRA test: "An ally who is inactive is not an ally." Apply the same test to advisors.
Before granting equity, ask: "What specific doors does this person open in the next 90 days?"
```

### SAFE Notes and Convertible Instruments — When Raising

```
FUNDING INSTRUMENTS GUIDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SAFE NOTE (Simple Agreement for Future Equity):
→ Invented by YC, now the standard pre-seed instrument
→ Not a loan — no interest, no maturity date (usually)
→ Converts to equity at the NEXT priced round
→ Investor gets equity at a discount to the priced round price (typically 15-20%)
→ Valuation cap: maximum valuation at which the SAFE converts (protects investors)
→ Cost to prepare: $500-$2,000 (or use YC's free standard SAFE template at ycombinator.com)
→ Use when: Raising $50K-$1M from angels before Series A

CONVERTIBLE NOTE:
→ A LOAN that converts to equity (has interest rate + maturity date)
→ More complex than SAFE — requires repayment if company doesn't raise a priced round
→ Typically: 5-8% interest rate, 18-24 month maturity, 15-25% discount
→ Use when: Investor insists (more common in non-YC ecosystem)
→ Risk: Maturity date creates pressure to raise or face repayment

PRICED ROUND (Series Seed, Series A):
→ Investor buys shares at a set price per share (defined valuation)
→ Requires: Term sheet, stock purchase agreement, investor rights agreement, legal fees
→ Cost: $25,000-$75,000 in legal fees (attorney required — do not DIY)
→ Use when: Raising $1M+ with institutional VCs

CAP TABLE HYGIENE (check before every fundraise):
□ Every share/option/SAFE documented in a cap table
□ Carta or Pulley for cap table management ($0-$500/year at early stage)
□ All option grants have board approval and documentation
□ IP assignments signed by all contributors
□ No undocumented oral equity promises to anyone
```

---

## THE GDPR / PRIVACY COMPLIANCE PROTOCOL

### What Triggers GDPR

You do not have to be European. You do not have to be incorporated in Europe. You do not have to have European employees.

**GDPR applies if you process personal data of people located in the EU — regardless of where your company is.**

"Processing" includes: collecting, storing, using, sharing, or even just displaying personal data.
"Personal data" includes: name, email, IP address, device ID, cookie values, usage behavior.

If you have a public website with analytics: you are processing personal data of EU users. GDPR applies.

```
GDPR COMPLIANCE CHECKLIST (minimal viable compliance for solo founders):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRIVACY POLICY (required):
□ What personal data you collect
□ Why you collect it (legal basis: consent, legitimate interest, contract, legal obligation)
□ Who you share it with (analytics providers, payment processors, email tools)
□ How long you keep it
□ User rights: access, deletion, correction, portability, objection
□ Contact method for privacy requests
□ If you use cookies: cookie policy must be separate or integrated

COOKIE CONSENT BANNER:
□ Functional/necessary cookies: no consent needed
□ Analytics cookies (Google Analytics, Mixpanel): consent required
□ Marketing/advertising cookies: consent required
□ "Accept All" and "Reject All" options must be equally prominent (no dark patterns)

DATA PROCESSING AGREEMENTS (DPAs):
□ Sign DPAs with every data processor: Stripe, Mailchimp, Intercom, AWS, Google Analytics
□ Most major vendors have DPAs available in their settings or on request
□ Failing to have DPAs = GDPR violation independent of other compliance

DATA SUBJECT REQUESTS:
□ Process for responding to: access requests (what data you have), deletion requests, correction requests
□ Legally required response time: 30 days
□ Simple: dedicated email address (privacy@yourcompany.com) that you monitor

THE PRAGMATIC SOLO FOUNDER APPROACH:
→ Termly.io: $10/month — generates GDPR-compliant privacy policy, cookie banner, cookie consent management
→ iubenda.com: $27-$129/year — privacy policy + cookie consent + DPA archive
→ Osano.com: Free tier for basic cookie consent
→ Total cost to achieve reasonable GDPR compliance: $10-$30/month

Better approach: Handle this at launch. Retrofitting GDPR compliance to 50,000 users is 10x harder and more expensive than building it in from the start.
```

### CCPA — California Consumer Privacy Act

Simpler than GDPR but applies to businesses with California users. Applies to your business if you meet ANY of:
- Annual gross revenue >$25 million (unlikely at early stage)
- Annually buy, sell, or share personal data of 100,000+ California consumers
- Derive 50%+ of annual revenue from selling personal data

**For most solo founders**: CCPA is less urgent than GDPR at early stage, but:
- Add a "Do Not Sell My Personal Information" link in your footer (this is cheap and satisfies the core CCPA requirement)
- Your privacy policy should mention California rights (Termly/iubenda handle this automatically)

---

## TERMS OF SERVICE AND STANDARD AGREEMENTS

### Terms of Service — What Must Be In Them

```
TERMS OF SERVICE MINIMUM REQUIREMENTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL CLAUSES (missing these creates serious risk):
□ Limitation of liability: Cap your total liability to the amount the user paid in the last 12 months
□ Disclaimer of warranties: "Product is provided as-is" — without this, implied warranties apply
□ Acceptable use policy: Define prohibited uses (illegal activity, abuse, spam)
□ Intellectual property ownership: You own your software; users own their data
□ Termination rights: When you can terminate accounts (TOS violation, non-payment, at will)
□ Governing law and jurisdiction: Your state, not theirs (e.g., "Laws of Delaware, exclusive jurisdiction: Delaware")
□ Dispute resolution: Arbitration clause + class action waiver (reduces litigation risk dramatically)
□ Data rights: What you can do with user data (especially important for B2B)

IMPORTANT FOR B2B SaaS:
□ Data processing agreement (or DPA provisions incorporated into TOS)
□ SLA definition if you promise uptime
□ Security obligations
□ Notification obligations for data breaches

WHERE TO GET A TEMPLATE:
→ Termly.io: $10-$30/month, auto-generates and keeps updated
→ Bonterms.com: Free, open-source SaaS TOS template (high quality, attorney-reviewed)
→ CommonPaper.com: Free standardized commercial agreements
→ Attorney-drafted: $1,500-$5,000 (worth it for B2B SaaS with enterprise customers)

TOS ARE NOT OPTIONAL: Many founders skip this until they have traction. A single dispute without a TOS limiting your liability can cost more than your first year of revenue.
```

---

## THE PLATFORM DEPENDENCY LEGAL RISK

### The Risk Nobody Talks About Until It Happens

Your business may be built on platforms that have the unilateral right to end your revenue overnight. This is a legal and operational risk that belongs in your risk register.

```
PLATFORM DEPENDENCY RISK MATRIX:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PAYMENT PROCESSORS (Stripe, PayPal):
→ Risk: TOS violation → account termination, funds held for 90-180 days
→ Common triggers: high chargeback rate (>1%), prohibited businesses, complaints
→ Prohibited categories include: adult content, CBD, gambling, firearms, certain financial services
→ Mitigation: Read Stripe's restricted businesses list before building. Maintain chargeback rate <0.5%.
  Keep a Braintree or Adyen account as backup payment processor.

APP STORES (Apple App Store, Google Play):
→ Risk: App removed with 30 days notice (or less for policy violations)
→ Common triggers: privacy violations, competing with Apple/Google, in-app payment bypass
→ Mitigation: Comply strictly with review guidelines. Never route around in-app payment for digital goods.
  Build a web app alternative that works without the app store.

AI API PROVIDERS (OpenAI, Anthropic, Cohere):
→ Risk: Usage policy violation → API key revocation
→ Common triggers: generating prohibited content, reselling API access, exceeding rate limits without notification
→ Mitigation: Read and comply with usage policies. Build with multi-provider support where possible.
  Cache responses where legally allowed to reduce API dependency.

CLOUD PROVIDERS (AWS, GCP, Azure):
→ Risk: Account suspension for TOS violation or fraud detection
→ Common triggers: cryptocurrency mining, automated abuse, billing disputes
→ Mitigation: Set billing alerts. Use multiple cloud providers for critical services.

DOMAIN REGISTRARS:
→ Risk: Domain suspended for UDRP disputes, ICANN violations, or non-payment
→ Mitigation: Set auto-renew. Register domain in your company name, not personal name.
  Own your domain for at least 5 years ahead. Register similar domains defensively.

THE RULE: Build to minimize dependency on any single platform. Own the customer relationship directly.
Get customer email addresses before they become app store subscribers. Have a backup payment processor. Maintain a web app alongside mobile apps.
```

---

## WHEN TO DIY VS HIRE A LAWYER

### The Decision Framework

Most early-stage legal work can be done yourself with templates. A small category requires an attorney.

```
LEGAL DIY GUIDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SAFELY DIY (good templates exist, low variance):
□ Entity formation: Stripe Atlas ($500), Clerky ($400), Firstbase ($400), or DIY on Secretary of State website ($50-$500)
□ EIN application: IRS.gov, free, 5 minutes
□ Privacy policy + TOS: Termly ($10-$30/mo), iubenda, or Bonterms (free)
□ Standard contractor agreement: Bonsai, Docracy free templates
□ IP assignment for contractors: Clerky template or Docracy free
□ 83(b) election: YC SAFE docs or online template, file yourself
□ Advisor agreements: FAST Agreement (free from YC)
□ SAFE notes: YC's standard SAFE template (free, widely accepted)
□ Trademark application: USPTO TEAS Plus ($250/class), DIY if name is distinctive
□ GDPR compliance: Termly or iubenda

HIRE A LAWYER FOR (high stakes, high variance):
□ Fundraising term sheets (Series A+): $20,000-$75,000 in legal fees — do not negotiate without counsel
□ Acquisition letter of intent or term sheet: This is the most expensive mistake you can make alone
□ IP dispute or cease-and-desist letter received: $5,000-$50,000+ depending on complexity
□ Employee termination with severance: Risk of wrongful termination claim is too high to DIY
□ GDPR enforcement action or data breach: Regulatory proceedings require specialized counsel
□ Multi-founder disputes or co-founder buyout: $5,000-$30,000 but far cheaper than litigation
□ Complex revenue-sharing or partnership agreements with material financial terms

WHERE TO FIND AFFORDABLE STARTUP LAWYERS:
→ Clerky.com: Online legal platform for startups, transparent fixed fees
→ Stripe Atlas: Includes legal guidance for entity formation
→ UpCounsel.com: Marketplace for startup attorneys, competitive rates
→ Lawtrades.com: Freelance attorneys for startups
→ SCORE (score.org): Free mentoring, includes legal advice via volunteer attorneys
→ Law school clinics: Many top law schools have startup clinics with supervised free legal work
→ Y Combinator's YC Deal: YC alum law firms offer discounted rates for YC companies (and sometimes non-YC)

BUDGET GUIDANCE:
→ Formation + basic docs package: $500-$2,000 (DIY) or $2,000-$5,000 (attorney)
→ First fundraise (SAFE round <$500K): $2,000-$5,000 (attorney review of docs)
→ Series A: $20,000-$50,000 (full legal counsel — non-negotiable)
→ Acquisition: $50,000-$200,000+ (full legal counsel — non-negotiable)
```

---

## THE CHANAKYA LEGAL INTELLIGENCE LAYER

Chanakya's Arthashastra dedicates entire chapters to contracts, allies, and the structure of agreements. His principles map directly to modern legal hygiene.

```
CHANAKYA ON CONTRACTS AND ALLIES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINCIPLE 1 (Arthashastra 2.10): "A king should execute transactions in writing,
witnessed and sealed. Oral transactions are void against power."

Modern translation: If it's not in writing, it doesn't exist in a dispute.
→ Co-founder equity agreement? In writing.
→ Contractor deliverables and IP ownership? In writing.
→ Advisor equity grant? In writing.
→ Partnership revenue share? In writing.
→ Payment terms with any supplier? In writing.

PRINCIPLE 2 (Arthashastra 7.1): "Before concluding a treaty, examine the character of the ally."
→ Before signing any partnership, revenue-sharing, or co-founder agreement: check their track record.
→ Google the person. Talk to their former partners. Look at their LinkedIn.
→ A bad actor with a contract is still a bad actor.

PRINCIPLE 3 (Arthashastra 3.1): "A contract made under compulsion is not binding."
→ Never sign legal documents under time pressure without reading them.
→ "The offer expires in 24 hours" is a negotiating tactic, not a legal reality (usually).
→ A legitimate acquirer, investor, or partner will give you time to have a lawyer review.

PRINCIPLE 4 (Arthashastra 2.7): "The treasury is the foundation of all enterprises."
→ Legal protection of IP and revenue streams IS treasury protection.
→ Every hour spent on legal hygiene at formation is worth 100 hours at crisis time.

PRINCIPLE 5: "Allies are created, not found."
→ Your attorney, your accountant, and your trusted advisors are created allies.
→ Invest in these relationships before you need them in a crisis.
→ The founder who calls their attorney for the first time when receiving a cease-and-desist
  is in a worse position than the founder who has a 2-year relationship with their counsel.
```

---

## THE 5 LEGAL MISTAKES THAT KILL PROFITABLE COMPANIES

1. **No co-founder vesting schedule**: The most common and most devastating. One co-founder leaves; they keep their equity. You build their exit check for them. Add vesting at formation — it's a 1-hour task that costs $0 to $500.

2. **Open source time bomb**: Building on AGPL or GPL code and not realizing it. The liability surfaces at acquisition or enterprise due diligence. Audit your dependencies before they audit you.

3. **Contractor IP not assigned**: Three years in, a contractor who built your core algorithm can claim ownership because you forgot a piece of paper. Get IP assignments signed before work begins, every time.

4. **Misclassified workers**: The IRS audit arrives 3 years later. Back taxes plus penalties plus interest across 5 "contractors" who were working full-time for you = $200K bill you can't pay. The classification test is not about what you want — it's about the economic reality of the relationship.

5. **No written agreements with co-founders or partners**: You build together for 18 months. The vision diverges. Without a written agreement, a dispute over who owns what, who can make decisions, and what happens when someone leaves becomes a $50,000-$200,000 legal battle that often kills both parties.

---

## LEGAL HEALTH DASHBOARD

Run this quarterly.

```
LEGAL HEALTH AUDIT (quarterly):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ENTITY AND STRUCTURE:
□ Annual report filed (due dates vary by state)
□ Franchise tax paid (Delaware: due June 1 — minimum $400, can be higher)
□ Registered agent current and receiving state mail
□ Operating agreement / bylaws up to date with current ownership

IP:
□ All contractors have signed IP assignment agreements
□ Open source license audit completed (run license-checker)
□ Core brand names registered or application filed
□ Domain auto-renew enabled

PEOPLE:
□ All employees have signed employment agreements with IP assignment and confidentiality
□ Worker classification reviewed for anyone >20 hrs/week
□ New hires in last 90 days have Form I-9 completed

DATA / PRIVACY:
□ Privacy policy updated within last 12 months
□ Cookie consent working and not pre-checked
□ DPAs signed with all major vendors
□ Data deletion requests handled within 30 days

AGREEMENTS:
□ All co-founders and advisors have signed equity agreements
□ All contractor agreements are in writing with defined scope
□ Customer-facing TOS updated within last 12 months
□ No verbal-only commitments outstanding

TAXES:
□ Quarterly estimated taxes paid (federal: Jan 15, April 15, June 17, Sept 15)
□ 1099s issued to contractors paid >$600 (due Jan 31)
□ Sales tax nexus reviewed if selling in multiple states
```

---

## Integration

Legal Engine connects to:
- `finance.md` → cap table hygiene, SAFE notes, fundraising checklist
- `ops-auto.md` → contractor agreements, IP assignment in contractor workflow
- `exit.md` → data room legal docs, IP audit, acquisition due diligence
- `network.md` → co-founder agreements, advisor equity, partnership structures
- `validate.md` → license check before building on third-party IP

Log legal decisions and agreements to `context/legal-log.md`.

> **This is not legal advice. For any significant legal matter, consult a qualified attorney in your jurisdiction.**
