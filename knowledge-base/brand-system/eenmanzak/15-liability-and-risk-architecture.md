# Liability and Risk Architecture

**Status:** Draft; risk-control architecture; legal review required
**Last updated:** 2026-04-17
**Purpose:** Define how the business should avoid high-liability work, reduce exposure lawfully, and protect personal wealth as much as feasible.


## Company mandate alignment

Interpret this document through `00-company-mandate-and-alignment.md`: the company is an AI-first founder-led software company using senior software engineering and ecommerce/logistics expertise to build B2B/B2C apps, SaaS/micro-SaaS, consulting, R&D, OSS/content authority, and multiple revenue streams. Dutch ZZP, TapTap, SpatialSense, and SoloOS are lanes, not the entire company identity.

> Hard truth: an **eenmanszaak does not create a liability shield**. Under official Dutch guidance, the owner is personally liable and creditors can reach private assets. There is no lawful “liability-free” product or service. The correct strategy is: avoid high-risk work, use limited-liability entities when justified, insure, contract carefully, minimize data/safety exposure, and keep claims conservative.

## 1. Non-negotiable principle

Do not search for “loopholes.” Use lawful risk allocation:

- choose lower-risk products;
- avoid regulated advice/products;
- use a BV when risk/revenue justifies it;
- use insurance;
- use reviewed contracts and terms;
- use MoR/platform rails where helpful;
- minimize data and safety exposure;
- maintain proof, testing, source, and incident records;
- never personally guarantee business obligations unless explicitly chosen after review.

## 2. Liability reality by structure

| Structure | Personal-wealth protection | Notes |
|---|---|---|
| Eenmanszaak | weak / none for business debts and claims | owner and business are not separate legal persons; private assets can be exposed |
| BV | stronger, but not absolute | legal entity usually liable, but director can still be personally liable for mismanagement, unlawful acts, tax/UWV reporting failures, guarantees, or improper registration/actions |
| Separate BV per high-risk product | stronger compartmentalization | useful later for products with different risk profiles; more admin/accounting/legal cost |
| Contract only | limited protection | helpful, but cannot erase statutory duties, fraud, gross negligence, consumer rights, privacy duties, or all third-party claims |
| Insurance only | risk transfer, not immunity | coverage exclusions and limits matter; must match product/service risk |

## 3. Entity conversion triggers

Strongly consider BV / legal-structure review before any of these:

- meaningful recurring paid revenue where claims could exceed cash reserves;
- US market exposure with B2C or high complaint risk;
- enterprise/B2B contracts with indemnities, SLAs, or consequential damages;
- products involving safety, health, navigation, finance, legal, tax, children, accessibility-critical use, or regulated domains;
- hiring employees/contractors for delivery;
- taking on client data that could cause breach damages;
- signing any personal guarantee, loan, lease, or large vendor commitment;
- product liability or professional negligence risk exceeds what insurance/contract can comfortably absorb.

## 4. Risk-tier map

| Tier | Example | Default decision |
|---|---|---|
| Low | static templates, source-linked checklists, non-regulated productivity tools, internal ops docs | OK under eenmanszaak with caveats and privacy hygiene |
| Medium | paid web SaaS processing business/customer data; app subscriptions; consulting prototypes | require terms, privacy, support process, insurance review, payment/tax architecture |
| High | tax/legal/accounting advice, cybersecurity guarantees, health/medical/safety outcomes, navigation assistance, children/minors, financial decisions | avoid under eenmanszaak unless professionally reviewed, insured, and possibly moved to BV |
| Red / prohibited now | “guaranteed compliance,” “safe navigation,” “medical/financial/legal replacement,” emergency response guarantees, handling highly sensitive data at scale | do not offer |

## 5. Product-specific risk posture

### TapTap

Primary risks:

- privacy/app-store data declarations;
- senior/vulnerable-user trust;
- accessibility claims;
- content accuracy;
- refunds/subscriptions/support;
- Apple UI/IP/trademark issues if using real iOS interfaces.

Risk posture:

- OK as app/product proof if claims remain educational and non-medical;
- require App Store privacy/support/terms readiness;
- avoid “guaranteed learning,” “clinically proven,” or dependency/health claims.

### SpatialSense

Primary risks:

- safety/navigation reliance;
- visually impaired user expectations;
- potential medical/assistive-device implications;
- product liability;
- accessibility/safety testing;
- sensor/AI accuracy.

Risk posture:

- keep experimental until legal/product-safety review;
- do not sell/market as safety-critical navigation under eenmanszaak;
- avoid “replaces cane/guide dog,” “safe navigation,” “prevents accidents,” or medical-device language.

### Dutch ZZP / admin product

Primary risks:

- legal/tax/accounting advice boundaries;
- VAT/KOR/WBSO misunderstandings;
- data privacy;
- customer reliance on deadlines/recommendations.

Risk posture:

- frame as workflow support and source-linked general information;
- route legal/tax/accounting decisions to qualified professionals;
- avoid “compliant,” “no accountant needed,” “guaranteed tax savings.”

### Consulting/services

Primary risks:

- professional negligence;
- scope creep;
- IP disputes;
- client data/security;
- missed deadlines;
- consequential damages.

Risk posture:

- only take scoped projects with written SOW;
- cap liability in contract;
- avoid regulated advice and safety-critical systems;
- get professional liability insurance before material client work.

## 6. Lawful liability reduction mechanisms

| Mechanism | What it reduces | What it cannot do |
|---|---|---|
| BV | personal exposure for ordinary business debts/claims | protect against director mismanagement, unlawful acts, guarantees, fraud/gross negligence |
| Professional liability insurance | negligence/errors in professional services | excluded risks, intentional acts, uncovered product liability |
| Business liability insurance | third-party property/personal injury claims | pure professional advice errors unless covered |
| Cyber insurance | breach response, incident costs | bad security practices, excluded incidents |
| Contract/SOW | scope creep, expectations, some damages | consumer statutory rights, privacy duties, fraud/gross negligence |
| Terms of service | user expectations, usage boundaries, support/refund rules | all legal duties or all third-party claims |
| Disclaimers | reliance and misunderstanding | substitute for safe product design or truthful claims |
| Merchant of Record | sales tax/VAT/payment operations for covered transactions | product liability, local income tax, privacy, support, account disputes |
| App stores | payment rails and distribution rules | app privacy, support, product claims, refunds/support obligations entirely |
| Data minimization | breach impact | security obligations entirely |
| Human review gates | AI/content/support claim risk | all errors; still need source/professional review |

## 7. Contract/SOW clauses to require professional drafting

For consulting and B2B SaaS, get legal review for:

- parties and legal/trade names;
- scope and exclusions;
- deliverables and acceptance criteria;
- timeline and dependencies;
- client responsibilities;
- fees, VAT, expenses, late payment;
- IP ownership and license;
- confidentiality;
- data processing / DPA;
- security responsibilities;
- warranty disclaimer;
- limitation of liability;
- exclusion of consequential damages where allowed;
- indemnity boundaries;
- support/SLA boundaries;
- termination;
- governing law/forum;
- force majeure;
- non-solicit only if needed;
- permission process for case studies/testimonials.

## 8. Insurance review checklist

Discuss with a Dutch insurance broker/adviser:

- bedrijfsaansprakelijkheidsverzekering (business liability);
- beroepsaansprakelijkheidsverzekering (professional liability/errors and omissions);
- cyber insurance;
- legal assistance insurance;
- directors’ liability if/when BV;
- product liability if selling consumer-facing products;
- worldwide/US/Canada coverage exclusions;
- subcontractor/contractor coverage;
- coverage for software, advice, data incidents, and AI-related services;
- exclusions for regulated advice, safety-critical, medical, finance, and security services.

## 9. Personal-wealth protection checklist

Before any paid launch or client contract:

- [ ] Is the product/service outside the red/prohibited risk list?
- [ ] Is the legal structure adequate for the risk?
- [ ] Are you signing any personal guarantee?
- [ ] Is insurance appropriate and active?
- [ ] Are terms/SOW reviewed?
- [ ] Is liability capped where legally possible?
- [ ] Are regulated claims avoided?
- [ ] Are consumer rights/refunds/cancellations addressed?
- [ ] Is privacy/cookie/support workflow ready?
- [ ] Is data minimized?
- [ ] Are app-store/platform rules followed?
- [ ] Are public claims in the claims register?
- [ ] Is there an incident response path?

## 10. Default prohibited project list while still eenmanszaak

Do not accept or launch these without lawyer + insurance + entity review:

- legal, tax, accounting, immigration, investment, medical, or insurance advice as a product;
- emergency, safety, or navigation guarantees;
- products for minors requiring sensitive data;
- client cybersecurity guarantees;
- mission-critical enterprise infrastructure with uncapped liability;
- handling high-volume sensitive/special-category data;
- products making automated decisions with legal/financial/health consequences;
- products requiring formal certification/attestation;
- contracts requiring personal guarantees or uncapped indemnities.

## 11. Recommended risk roadmap

### Now

- Keep all public offers low-risk and informational/workflow-oriented.
- Create prohibited-project list.
- Build SOW/terms/privacy/support drafts.
- Start insurance adviser conversations.
- Keep claims register mandatory.

### Before first paid product

- Decide app store vs MoR vs Stripe/direct merchant.
- Review terms/refunds/cancellation.
- Verify VAT/tax route.
- Verify insurance coverage.
- Decide whether eenmanszaak is still acceptable.

### Before high-risk or meaningful revenue

- Get BV/entity conversion advice.
- Separate high-risk product lines if needed.
- Add professional liability/cyber coverage.
- Formalize DPA/security posture.
- Refuse contracts with uncapped liability.

### Ongoing

- Quarterly legal/compliance/source review.
- Monthly access/privacy/claims review.
- Incident drills after launch.
- Keep personal and business finances/accounts cleanly separated.

## 12. Key source anchors

- Business.gov.nl: sole proprietorship means no separation between private and business assets; creditors can claim personal assets.
- Business.gov.nl: legal forms with legal personality generally shift liability to the legal entity, with exceptions.
- Business.gov.nl: changing to BV can make the company liable instead of the sole proprietor for company obligations, but director liability remains possible.
- KVK: insurance guidance distinguishes business liability and professional liability needs.
- Existing claims register: no public compliance/tax/legal/safety claims without source and review.
