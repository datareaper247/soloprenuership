# Commercial Readiness Playbooks for Apps, Micro-SaaS, and Consulting

**Status:** Draft; operating guide; professional review required before paid launch
**Last updated:** 2026-04-17
**Purpose:** Define concrete commercial-readiness paths for paid mobile apps, web micro-SaaS, and consulting/services sold internationally, with rich Western markets as the first commercial target.


## Company mandate alignment

Interpret this document through `00-company-mandate-and-alignment.md`: the company is an AI-first founder-led software company using senior software engineering and ecommerce/logistics expertise to build B2B/B2C apps, SaaS/micro-SaaS, consulting, R&D, OSS/content authority, and multiple revenue streams. Dutch ZZP, TapTap, SpatialSense, and SoloOS are lanes, not the entire company identity.

> This guide is for planning. It is not tax, legal, accounting, app-store, consumer-law, or payment-provider advice.

## 1. Market sequencing

### First paid markets to design for

| Market group | Why attractive | Readiness burden |
|---|---|---|
| Netherlands / EU | founder location, KVK/Belastingdienst context, local trust | VAT/OSS, GDPR, cookies, DSA trader info, EAA if covered |
| US | large app/SaaS market, high willingness to pay | sales tax/provider coverage, product liability, stronger need for entity/insurance/terms |
| UK | high software spend, English market | VAT, consumer terms, support expectations |
| Canada / Australia / New Zealand | English, rich markets, app/SaaS-friendly | GST/HST/VAT-style obligations often handled better through MoR |
| Switzerland / Norway | high purchasing power | non-EU tax/localization complexity; use MoR or reviewed tax setup |

### Commercial principle

For the first paid experiments, prefer channels where **payment/tax/customer-support complexity is outsourced or standardized**:

- app stores for app-native digital goods;
- Merchant of Record for web SaaS/digital products;
- direct invoicing for scoped consulting.

## 2. Playbook A — paid mobile app / subscription app

### Recommended stack

```text
iOS/Android app
├── Apple In-App Purchase / Google Play Billing
├── RevenueCat entitlement/subscription backend
├── Moneybird accounting for payouts/revenue records
├── App Store / Play Console privacy and data-safety declarations
├── Support inbox + privacy/support pages
└── Crash/error monitoring after SDK privacy review
```

### Required before launch

- Apple Developer Program / Google Play Console account ready.
- App Store Connect / Play Console tax, banking, agreement, and trader/contact requirements completed.
- App privacy labels / Google Data safety entries drafted from actual SDK/data inventory.
- In-app purchase/subscription products configured and reviewable.
- Support URL, privacy URL, terms URL, and cancellation/help flow live.
- RevenueCat project configured if using app subscriptions.
- Test purchases, restores, cancellations, entitlement revocation.
- Claims register checked for learning, accessibility, safety, and AI claims.
- Product support path tested.

### Use this path for

- TapTap paid app/subscription;
- future mobile education/accessibility/productivity apps;
- app-native digital content/features.

### Avoid

- directing app users to external payment in ways Apple/Google do not allow;
- using Stripe/Paddle inside native app for app-native digital goods unless a specific entitlement/regional program permits it;
- making accessibility/medical/safety claims without audit/review;
- shipping analytics/crash SDKs without privacy/data-safety updates.

### Rich-market launch order

1. Netherlands/EU if trader/contact/privacy pages are ready.
2. US/Canada/UK/Australia if support capacity and app-store compliance are ready.
3. Other regions after localization/support/refund expectations are understood.

## 3. Playbook B — web micro-SaaS / paid web app

### Recommended default stack

```text
Web SaaS / digital product
├── Paddle as default Merchant of Record
├── FastSpring if B2B quotes/localized invoicing matter more
├── Stripe Billing + Stripe Tax only if direct merchant control is worth compliance load
├── Moneybird accounting for payouts and business records
├── Privacy-light analytics first
├── Support inbox / help page
└── Terms, privacy, refund/cancellation, DPA if B2B data processing
```

### Merchant of Record decision

Use MoR first if:

- selling globally to consumers or small businesses;
- VAT/sales-tax complexity is not your differentiator;
- you want a cleaner solo-founder launch;
- the product is digital/software and accepted by the provider.

Use Stripe/direct merchant if:

- you need full checkout/custom billing control;
- you have accountant/tax support;
- you want direct customer merchant relationship;
- you accept registration/filing/reporting burden.

### Required before launch

- clear product category: B2B vs B2C;
- privacy notice and cookie/analytics decision;
- terms, refund/cancellation, support expectations;
- DPA/security posture if processing customer business data;
- payment-provider eligibility approved;
- tax/VAT approach documented;
- price display and invoice expectations checked;
- claims register checked;
- support and deletion/access request routes ready.

### Use this path for

- Dutch ZZP operating tool;
- SoloOS-style web product;
- paid templates/checklists if sold digitally;
- productized tools not consumed inside app-store apps.

### Avoid

- custom tax logic before PMF;
- “GDPR compliant,” “AI Act compliant,” “tax compliant,” or “no accountant needed” claims;
- selling legal/tax/accounting advice as software output;
- payment before privacy/terms/support pages exist.

## 4. Playbook C — consulting / productized services

### Recommended stack

```text
Consulting services
├── Founder LinkedIn + company proof page
├── Business email and scoped intake form
├── SOW / proposal / MSA template
├── Stripe Invoicing or bank transfer
├── Moneybird / Exact / SnelStart accounting
├── Proof-permission log
└── Professional liability + contract review before higher-risk work
```

### Required before first client

- service boundaries and prohibited-project list;
- written SOW with deliverables, assumptions, acceptance, timeline;
- limitation-of-liability clause reviewed by a lawyer;
- IP ownership/license terms;
- confidentiality clause;
- data-processing terms if client data is handled;
- no regulated advice unless qualified;
- invoice details and VAT treatment verified;
- case-study permission process.

### Low-risk service offers to consider

- product/brand trust-shell setup;
- AI-assisted workflow audit with no legal/tax conclusions;
- automation prototype sprint with clear acceptance criteria;
- app/store-launch readiness checklist support;
- documentation/ops system setup;
- technical due diligence on non-safety-critical software.

### Avoid as an eenmanszaak unless professionally reviewed and insured

- legal/tax/accounting advice;
- medical/health/safety-critical software;
- financial/investment/credit decisions;
- emergency response/navigation guarantees;
- cybersecurity guarantees for third parties;
- enterprise SLAs with large consequential-damage exposure;
- work requiring personal guarantees;
- regulated compliance certification.

## 5. Accounting and invoicing decision

| Tool | Fit | Use when | Caveat |
|---|---|---|---|
| Moneybird | best default Dutch SMB/eensmanszaak accounting | simple invoices, bank matching, VAT, Peppol, accountant collaboration | verify plan/features with accountant |
| Exact | heavier B2B/accountant/e-invoicing | more complex finance, Peppol, scaling admin | likely overkill at day one |
| SnelStart | Dutch accountant-friendly | if accountant prefers it | validate API/workflow fit |
| Acumulus | low-cost bookkeeping | budget-sensitive early stage | verify Peppol/e-invoicing features before relying on it |

## 6. Required public pages by paid path

| Page | App | Web SaaS | Consulting |
|---|---:|---:|---:|
| Home | yes | yes | yes |
| About / operator | yes | yes | yes |
| Product/service description | yes | yes | yes |
| Pricing | if paid | yes | optional/proposal |
| Privacy | yes | yes | yes if forms/data |
| Terms | yes | yes | SOW/MSA instead or public terms |
| Support | yes | yes | yes |
| Refund/cancellation | subscription-dependent | yes | contract-dependent |
| Official accounts | yes | yes | yes |
| Trust / claims caveats | yes | yes | yes |
| Accessibility statement | if claiming/accessibility-sensitive | if covered/claimed | if relevant |
| DPA/security page | if B2B/user data | if B2B/user data | if client data handled |

## 7. Revenue instrumentation path

### Before revenue

- UTM source tracking;
- research board;
- email/waitlist consent records;
- proof library;
- manual spreadsheet of conversations.

### First revenue

- payment provider dashboard;
- Moneybird/accounting reconciliation;
- simple MRR/ARR/churn spreadsheet;
- support/refund log;
- claims/support incident log.

### After repeat revenue

- RevenueCat/Paddle/Stripe API pulls;
- product analytics;
- dunning/failure recovery;
- cohort/retention tracking;
- dashboard in Google Sheets/Metabase/PostHog as appropriate.

## 8. Rich Western-market launch checklist

Before selling in a rich Western market:

- [ ] Is this B2B, B2C, or both?
- [ ] Is the buyer in app store, web checkout, or invoice flow?
- [ ] Who is the Merchant of Record?
- [ ] Who calculates/remits VAT/sales tax/GST?
- [ ] Are customer terms/refunds/cancellation clear?
- [ ] Are support expectations realistic?
- [ ] Is personal/business contact information displayed where law/platform requires it?
- [ ] Are privacy, cookies, analytics, SDKs, and DPA reviewed?
- [ ] Are accessibility and AI claims checked?
- [ ] Are screenshots/testimonials/logos permissioned?
- [ ] Is entity/insurance/contract risk acceptable?
- [ ] Is the product outside the prohibited/high-liability list?

## 9. Recommended next decision memos

1. **MoR vs Stripe memo** for first web micro-SaaS.
2. **RevenueCat/App Store readiness memo** for TapTap.
3. **Consulting SOW/liability template memo** before first paid service.
4. **Moneybird vs Exact/SnelStart memo** with accountant input.
5. **Entity conversion memo: eenmanszaak to BV** before high-risk or meaningful revenue.
