# Legal Intelligence Engine — Solo Founder Legal OS

> **⚠️ DISCLAIMER**: This is not legal advice. For any significant legal matter, consult a qualified attorney in your jurisdiction. This skill helps you avoid the most common mistakes and know when to get professional help.

## Auto-Trigger (No Slash Command Needed)

Fires automatically when:
- "what entity should I form" / "LLC vs C-Corp" → entity selection protocol
- "I want to give equity to" / "stock options" → equity structure guide
- "contractor vs employee" / "1099 vs W2" → worker classification guide
- "terms of service" / "privacy policy" / "GDPR" → compliance checklist
- "someone is using my code" / "protecting my IP" → IP protection protocol
- "co-founder agreement" / "partnership agreement" → equity + legal structure
- "do I need a lawyer" → DIY vs hire decision tree

---

## Why This Exists

Legal mistakes are the silent killers of profitable companies:

- **Equity without vesting**: co-founder leaves at month 3 with 50% of the company permanently
- **Contractor misclassification**: IRS reclassifies as employees → $100K+ in back taxes and penalties
- **IP without assignment**: contractor owns the code they wrote for you (unless you have a work-for-hire agreement)
- **Open-source license trap**: your product is built on GPL code → you're legally required to open-source your entire product
- **GDPR violation**: handling EU user data without a privacy policy → 4% of global revenue fine
- **No vesting cliff**: co-founder is out at month 5, but the cliff was 12 months → you keep the equity. Without it, they keep it all.

The most dangerous assumption: "I'll deal with the legal stuff later."
Later = when you're exiting or raising, and the cost of fixing it is 10x higher.

**Chanakya on contracts**: "A treaty made with an enemy should be binding; one made with a friend may be relaxed. Know the difference between what can be undone and what cannot."
Modern translation: Get the structural agreements right at the beginning. Equity splits and IP ownership are nearly impossible to change after the fact.

---

## THE ENTITY SELECTION PROTOCOL

### LLC vs C-Corp vs S-Corp — The Decision Tree

```
ENTITY SELECTION DECISION TREE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUESTION 1: Do you plan to raise venture capital (traditional VC round)?
→ YES: Delaware C-Corp. Full stop. VCs will not invest in LLCs.
         Use Stripe Atlas ($500) or Clerky ($2,000) to form in Delaware.
→ NO: Continue to Question 2.

QUESTION 2: Are you profitable (or expect to be profitable soon)?
→ YES (bootstrapped, profitable): Choose between LLC and S-Corp
  → If profit <$50K/year: LLC with disregarded entity treatment (simplest)
  → If profit >$50K/year: S-Corp election saves 15.3% self-employment tax on
    distributions above reasonable salary (can save $5K-15K/year)
→ NO (pre-revenue or early stage): LLC (your home state) — cheapest, simplest.

QUESTION 3: Do you have a co-founder?
→ YES: LLC is fine, but your operating agreement MUST include:
  → Equity split + vesting schedule
  → Decision-making authority (who can sign contracts, who has veto power)
  → Buy-sell provisions (what happens if one founder wants out)
  → Intellectual property assignment clause
→ NO: Solo-founder LLC is the simplest and cheapest option.

C-CORP SPECIFICS (if you choose this path):
→ Delaware is standard because: investor-friendly laws, established case law,
  Chancery Court (no juries for business disputes = predictable outcomes)
→ Cost: $500-2,000 to form, $300/year Delaware franchise tax (minimum)
→ Employee stock options: ISOs (Incentive Stock Options) only available in C-Corps
→ 83(b) election: CRITICAL if receiving founder shares — see section below
→ Conversion from LLC to C-Corp: possible later but costs $3-10K and creates tax events

LLC SPECIFICS (if you choose this path):
→ Form in your HOME STATE unless you have investors pushing for Delaware
→ Cost: $50-500 depending on state, $800/year minimum in California
→ Pass-through taxation: profits flow to your personal return (simpler for sole founder)
→ Operating Agreement: Even as a solo founder — write one. It protects you from "disregarded entity" risk.
→ Members vs Managers: Single-member LLC = you're both. Multi-member: define roles in operating agreement.

S-CORP SPECIFICS:
→ S-Corp is a TAX election, not a separate entity type
→ You form an LLC or C-Corp FIRST, then elect S-Corp tax treatment
→ Benefit: Income above "reasonable salary" distributed as dividends (no SE tax = 15.3% savings)
→ Limitation: US citizens only, max 100 shareholders, no foreign shareholders
→ S-Corp election deadline: 75 days after incorporation (or by March 15 for next tax year)
→ Reasonable salary requirement: IRS requires you to pay yourself a market-rate salary first.
  Can't pay yourself $0 and take $200K in distributions.

THE "FLIP TO DELAWARE C-CORP" EVENT:
If you start as an LLC and later decide to raise VC:
→ Cost: $3,000-8,000 in lawyer fees + potential tax consequences
→ Timeline: 4-6 weeks
→ Trigger: Signed term sheet from institutional VC
→ Before flip: issue promissory notes or SAFEs (preferred over equity in an LLC for pre-flip investors)
```

---

## THE 83(B) ELECTION — THE MOST IMPORTANT PIECE OF PAPER YOU'LL SIGN

```
83(b) ELECTION GUIDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT IT IS: A one-page IRS form that lets you pay taxes on your founder equity NOW
(at near-zero value) rather than when it vests (potentially millions).

WHEN IT APPLIES: When you receive restricted stock (stock subject to vesting) in a corporation.
Does NOT apply to LLC membership interests (different tax treatment).

THE MATH:
WITHOUT 83(b): You pay ordinary income tax as each share vests.
  → At month 12 (cliff): 25% of your shares vest at market value of $1/share = $250,000 taxable
  → You owe $70,000-100,000 in taxes on income you haven't received as cash.

WITH 83(b): You pay on the TOTAL grant at grant date, when value is near zero.
  → At incorporation, your 1,000,000 shares are worth $0.001/share = $1,000 taxable
  → You owe maybe $350 in taxes. Then all future appreciation is capital gains.

DEADLINE: 30 DAYS from the date of stock grant. Missing this is irreversible.

HOW TO FILE:
1. Download the 83(b) election form (IRS Form 83(b) election statement)
2. Fill it out (takes 20 minutes — templates available from Stripe Atlas, Clerky)
3. Send via CERTIFIED MAIL to the IRS within 30 days of grant
4. File a copy with your next tax return
5. Keep a copy forever

COST: $0 if you do it yourself.

HIRE A LAWYER FOR THIS?: No. It's a template. Do it yourself. Just don't miss the deadline.
```

---

## IP PROTECTION PROTOCOL

### Protecting What You Build

```
IP AUDIT (fire when IP protection question detected):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. CODE OWNERSHIP — Work-For-Hire Agreement
RISK: Without a written agreement, the contractor owns the code they wrote for you.
"Independent contractor" status does NOT automatically transfer IP to you.

REQUIREMENT: Every contractor, every engagement must sign:
→ "Contractor assigns all work product, including source code, to [Company Name]"
→ Include: moral rights waiver, work-for-hire designation
→ Template: Bonsai.io, HelloSign templates, or Clerky's contractor agreement ($0)
→ Must be signed BEFORE work starts. Retroactive assignments are hard to enforce.

For employees: IP assignment is typically in the employment agreement.
Make sure every employment agreement includes an IP assignment clause.

2. OPEN-SOURCE LICENSE AUDIT
BEFORE using any open-source library, check the license:

GREEN (commercial use allowed, modifications stay private):
→ MIT License: Use freely, keep private, no restrictions. (React, Node.js, Express)
→ Apache 2.0: Similar to MIT + explicit patent grant. (Kubernetes, TensorFlow)
→ BSD 2/3-Clause: Very permissive, similar to MIT. (FreeBSD, some Python packages)
→ ISC: Functionally equivalent to MIT.

YELLOW (check before using):
→ LGPL (Lesser GPL): Can use as library without open-sourcing your code.
  CANNOT modify the library and keep those modifications private.
→ Creative Commons CC BY: Can use with attribution. Check specific variant (NC, SA, ND)

RED (requires open-sourcing your code — avoid in commercial products):
→ GPL 2.0/3.0: If your product includes GPL code, your ENTIRE product must be open-sourced.
  The GPL is viral — it infects everything it touches.
→ AGPL: Even worse — web applications that run AGPL code must open-source their code.
  This catches AI companies who use AGPL-licensed models.
→ SSPL (Server Side Public License — MongoDB): Similar to AGPL, intended to prevent
  cloud providers from wrapping open-source software.

TOOL: https://choosealicense.com/ | https://tldrlegal.com/ for quick lookups.

3. TRADEMARK BASICS
WHAT IT PROTECTS: Your brand name and logo in commerce.
WHY IT MATTERS: Without a registered trademark, someone can use your brand name in a different state.

WHEN TO REGISTER: When you're generating consistent revenue and the brand has value (typically $10K+ MRR).
HOW: File with USPTO.gov yourself. Cost: $250/class. Takes 8-12 months.
PRIORITY: File before you get big enough to attract competitors copying your brand.

TRADEMARK SEARCH: Before naming your product, search USPTO.gov TESS database.
A trademark conflict discovered after 2 years of building = rebrand + customer confusion + lost SEO.

4. COPYRIGHT
WHAT IT IS: Automatic protection the moment you create it. No registration needed.
COVERS: Code, text, images, video — any creative expression.
DOES NOT COVER: Ideas, processes, functional elements.
REGISTRATION: Not required for protection, but required to sue for statutory damages.
Cost: $65 online at copyright.gov. Worth it for your core product IP.

5. PATENTS
WHAT THEY COVER: Novel, non-obvious inventions and processes.
COST: $10,000-30,000+ (with a patent attorney). Takes 2-3 years.
SOLO FOUNDER VERDICT: Almost never worth it at early stage.
→ By the time you get the patent, the market has moved.
→ Enforcing a patent costs $1M+.
→ Exceptions: Novel AI model architecture, novel hardware, life sciences.

6. TRADE SECRETS
WHAT THEY ARE: Confidential business information that gives competitive advantage.
HOW TO PROTECT: Access controls, NDAs, confidentiality agreements.
EXAMPLES: Customer lists, pricing algorithms, proprietary data, manufacturing processes.
REQUIREMENT: You MUST take active steps to protect them (NDAs + access controls).
If you don't protect them, you lose the right to enforce them.
```

---

## CONTRACTOR VS EMPLOYEE CLASSIFICATION

### The Most Expensive Mistake in HR

```
WORKER CLASSIFICATION GUIDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE RISK: Misclassifying an employee as a contractor:
→ Back payroll taxes (FICA: 7.65% employer share + 7.65% employee share you should have withheld)
→ Back income tax withholding
→ Penalties and interest (can total 30-50% of the misclassified wages)
→ Benefits owed: health insurance, unemployment, workers comp

THE IRS 3-FACTOR COMMON-LAW TEST (federal standard):

BEHAVIORAL CONTROL (do you control HOW they work?):
→ Contractor indicators: They work their own hours, use their own tools, work remotely
→ Employee indicators: You dictate their hours, they must use your equipment/systems,
  they work alongside your team

FINANCIAL CONTROL (do you control the economic aspects?):
→ Contractor indicators: They can make profit or loss, work for multiple clients, are not
  economically dependent on you alone
→ Employee indicators: Set hourly/weekly rate, single client, you provide all their tools,
  they can't realistically work for others

TYPE OF RELATIONSHIP:
→ Contractor indicators: Project-based with clear end, no benefits, no ongoing expectation
→ Employee indicators: Indefinite term, permanent role, integral to core business

CALIFORNIA AB5 (strictest in the US — applies if you have CA contractors):
The ABC test requires ALL three to be true for contractor status:
A. Free from your control in performing work
B. Performs work outside the usual course of the hiring entity's business
C. Is customarily engaged in an independently established trade or business

PRACTICAL SAFE CONTRACTOR PRACTICES:
□ Documented project scope with deliverables (not "work on our product full-time")
□ Written independent contractor agreement (every time, not just once)
□ They have at least 2 other clients
□ They use their own equipment and software where possible
□ They set their own hours within project deadlines
□ They invoice you (not you setting their hourly schedule)
□ 1099-NEC issued at end of year for >$600 paid

WHEN TO SWITCH TO W2:
→ >20 hours/week of core business work for >6 months
→ You're directing their daily tasks and schedule
→ They have no other clients and you're their primary income
→ They're doing work that is central to your product (not peripheral services)

INTERNATIONAL CONTRACTORS:
→ No W-9 required (US form)
→ Need W-8BEN from them (or W-8BEN-E for foreign entity)
→ No 1099 issued for foreign nationals
→ BUT: beware local employment laws in their country
  → Philippines, India: worker-friendly local laws that can conflict with your contractor classification
  → UK, EU: local laws often override contractor agreements
→ Use: Deel, Rippling, or Remote.com for international contractor payments and compliance
```

---

## EQUITY STRUCTURE GUIDE

### Getting Cap Table Right Before It Gets Complicated

```
EQUITY STRUCTURE FUNDAMENTALS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CO-FOUNDER VESTING (industry standard — non-negotiable):
4-year vest, 1-year cliff is the universal standard. Here's why:

→ 4-year vest: aligned with typical startup build-to-exit timeline
→ 1-year cliff: protects against co-founder who leaves in month 3 with 50% equity
→ What "cliff" means: zero shares vest until the 1-year mark. Then 25% vests at once.
→ After cliff: typically monthly vesting (1/48th per month for remaining 36 months)
→ Acceleration: "double trigger" is standard — sale of company AND termination required for full vest

EXAMPLE: 50/50 co-founders, 1M shares each, 4-year vest, 1-year cliff
→ Co-founder leaves at month 6: receives 0 shares (before cliff)
→ Co-founder leaves at month 13: receives 25% (cliff hit + 1 month) = 25% × 1M = 250,000 shares
→ Both founders stay 4 years: both keep full 1M shares

CO-FOUNDER EQUITY SPLIT APPROACHES:
→ 50/50: cleanest for equal co-founders; requires tie-breaking mechanism in operating agreement
→ 60/40 or 55/45: appropriate when roles are clearly asymmetric (technical/business split)
→ Slicing Pie model: Dynamic equity split based on contributions (complex, but fair)
→ Rule of thumb: Never let equity be the first conversation. Establish the working relationship first.

ADVISOR EQUITY (standard ranges):
→ Domain Expert (gives you 2hrs/month of domain knowledge): 0.1-0.25% / 2-year vest / 6-month cliff
→ Distribution Connector (opens doors to customers or channels): 0.25-0.5% / 2-year vest / 6-month cliff
→ Credibility Signal (name brand that helps raise or recruit): 0.1-0.25% / 2-year vest / 6-month cliff
→ True active advisor (weekly engagement, real deliverables): up to 0.5% / standard vesting

EMPLOYEE OPTIONS (if you hire employees):
→ ESOP pool: typically 10-15% pre-Series A (reserved for future employees)
→ ISOs (Incentive Stock Options): preferred (better tax treatment, only for employees)
→ NSOs (Non-Qualified Stock Options): for contractors, advisors, and board members
→ Strike price: must be FMV at time of grant (409A valuation required for C-Corps)
→ 409A valuation: required annually (or after material events), costs $1,500-5,000 from a 409A firm

SIMPLE EQUITY TOOLS:
→ Carta (carta.com): Cap table management, equity plan, 409A valuations. Free up to 25 stakeholders.
→ Pulley (pulley.com): Simpler and cheaper than Carta. Good for early-stage.
→ SAFE agreements (Y Combinator model): Simple Agreement for Future Equity — convertible into equity at funding. Free template at ycombinator.com/documents.
```

---

## PRIVACY & COMPLIANCE CHECKLIST

### The Minimum You Need to Not Get Fined

```
PRIVACY COMPLIANCE CHECKLIST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GDPR TRIGGER: ANY user from the European Union (citizenship doesn't matter — location does).
If your product is accessible to EU users, you need GDPR compliance.

GDPR MINIMUM REQUIREMENTS:
□ Privacy policy: Must include what data you collect, why, how long you keep it, who you share with
□ Cookie consent: Pop-up for non-essential cookies (analytics, marketing)
□ Data processing agreement: With any vendor that processes your users' data (Stripe, SendGrid, etc.)
□ Right to deletion: Users can request their data deleted. You must comply within 30 days.
□ Right to access: Users can request a copy of their data.
□ Data breach notification: Notify authorities within 72 hours of discovering a breach.

CCPA (California Consumer Privacy Act):
□ "Do Not Sell My Personal Information" link if you sell/share data with third parties
□ Privacy policy disclosure of data categories collected and purposes
□ Opt-out mechanism for data sharing

PRAGMATIC SOLO FOUNDER SOLUTION:
→ Termly (termly.io): $10-20/mo auto-generates GDPR + CCPA compliant policies, cookie consent
→ iubenda (iubenda.com): Similar to Termly, widely used in Europe
→ Cookiebot (cookiebot.com): Cookie consent specifically. Integrates with any CMS.

WHAT NOT TO DO:
→ Copy another company's privacy policy (it's copyright infringement AND won't match your actual practices)
→ Have no privacy policy at all (blocks Apple App Store approval + exposes you to GDPR fines)
→ Have a privacy policy that says you don't collect data when you clearly do (worse than no policy)

TERMS OF SERVICE (ToS):
→ Purpose: Defines the rules of use, limits your liability, governs disputes
→ Key clauses: Acceptable use policy, limitation of liability, dispute resolution (arbitration vs court)
→ Template sources: Orrick's startup documents, Docracy, or a service like Termly
→ When to hire a lawyer for ToS: SaaS with enterprise customers (they'll negotiate), HIPAA-regulated data,
  financial services, anything where custom ToS terms are material to customer negotiations
```

---

## THE PLATFORM DEPENDENCY LEGAL RISK

### What You Build On Can Take What You Built

```
PLATFORM RISK ASSESSMENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APP STORE DEPENDENCY:
→ Apple can remove your app with 30-day notice (or immediately for policy violations)
→ Apple takes 30% (15% for subscriptions after year 1, small business program)
→ GDPR compliance is the app developer's responsibility, not Apple's
→ Review process: unpredictable, appeals process slow
→ Mitigation: also have a web app. Don't build iOS-only.

PAYMENT PROCESSOR DEPENDENCY (Stripe, PayPal, etc.):
→ Stripe's ToS prohibits: adult content, pharmaceutical sales, certain firearms, cannabis
→ Account termination: can happen with 30-60 days notice (funds held for 90-180 days)
→ Reserve requirements: Stripe may hold 10-25% of revenue for 90 days if high churn
→ Mitigation: Have a backup processor. Braintree (PayPal), Paddle, or Lemon Squeezy.

AI MODEL DEPENDENCY (OpenAI, Anthropic, etc.):
→ Model API usage policies can change: content that was allowed today might not be tomorrow
→ Rate limiting: without enterprise tier, your product can be degraded by usage spikes
→ AGPL license risk: some open-source models require open-sourcing your application code
→ Data retention: understand what the model provider does with your API call data
→ Mitigation: Build model-agnostic where possible. Use abstract interfaces that let you swap models.

CLOUD PROVIDER DEPENDENCY:
→ AWS, Vercel, Railway — all have ToS that can suspend accounts
→ Most common trigger: abuse or fraud detection (false positives do happen)
→ Mitigation: keep code portable (Docker containers), maintain regular data backups off-platform

SOCIAL PLATFORM DEPENDENCY (Twitter/X, LinkedIn, Reddit):
→ API access can be withdrawn (Twitter's 2023 API changes devastated many products)
→ Community-based growth can be disrupted by algorithm changes
→ Mitigation: Build email list ownership. Your platform, your list.
```

---

## WHEN TO DIY vs HIRE A LAWYER

```
LEGAL DIY vs HIRE DECISION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIY SAFELY (use templates + platforms, no lawyer needed):
→ Entity formation: Stripe Atlas ($500), Clerky ($2,000), Firstbase ($399)
→ Privacy policy + ToS: Termly, iubenda (auto-generated, legally sufficient for most cases)
→ Standard contractor agreement: Bonsai, HelloSign templates, or Clerky's free forms
→ SAFE note (pre-seed investment): Y Combinator's open-source SAFE template
→ 83(b) election: Template + certified mail. No lawyer needed. Just don't miss the 30 days.
→ Basic NDA: Many free templates. Most simple NDAs are fine DIY.

ALWAYS HIRE A LAWYER FOR:
→ Term sheet review (Series A or later): 1st-time founders don't know what to negotiate
→ Acquisition LOI / term sheet: Every material term has legal implications
→ IP dispute (someone copied your product): Cease and desist, potential litigation
→ Employment termination (with cause): mishandled terminations create lawsuits
→ GDPR enforcement action or FTC complaint: requires specialist counsel
→ Significant co-founder disputes: when relationships break down, get representation

WHERE TO FIND AFFORDABLE STARTUP LAWYERS:
→ UpCounsel: marketplace of startup-experienced lawyers, fixed-fee projects
→ Lawtrades: similar model, flat-fee or hourly startup lawyers
→ Clerky: document automation + lawyer network for startups
→ Your local SCORE chapter: free mentoring from retired executives (some are former lawyers)
→ YC-affiliated lawyers: if you're going through YC or using their docs, many firms work on YC terms
→ Law school clinics: free or reduced-cost help from supervised law students

BUDGET EXPECTATIONS:
→ Entity formation: $0 DIY, $500-2,000 with service, $1,500-3,000 with lawyer
→ Term sheet review: $2,000-5,000 (worth it — lawyers find things that save 10x their fee)
→ Acquisition review: $5,000-15,000 (non-negotiable for any significant deal)
→ IP dispute: $10,000-100,000+ (avoid by getting IP protection right upfront)
```

---

## Integration

Legal Intelligence connects to:
- `network.md` → co-founder agreements, advisor equity, investor term sheets
- `exit.md` → data room legal checklist, reps & warranties, deal structure
- `finance.md` → cap table, equity modeling, ESOP pool planning
- `ops-auto.md` → contractor agreements (every hire needs one)
- `onboard.md` → entity and IP questions are part of the business context setup

⚠️ **Reminder**: This skill reduces risk from common mistakes. It is not a substitute for qualified legal counsel on significant matters. The cost of prevention is always lower than the cost of litigation.
