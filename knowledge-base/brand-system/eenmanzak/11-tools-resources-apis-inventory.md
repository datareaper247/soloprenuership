# Tools, Resources, APIs, and Official-Source Inventory

**Status:** Draft; operating inventory; not vendor/legal advice
**Last updated:** 2026-04-17
**Purpose:** Identify the tools, official docs, services, APIs, CLIs, OSS/public APIs, and internal resources that can accelerate the Eenmanszaak / Eenmanzak deep dive into apps, micro-SaaS, consulting, trust-building, commercial readiness, and liability reduction.

> Use this as a selection map. Do not connect tools or collect data until the relevant privacy, payment, tax, app-store, and claims-register gates are satisfied.

## 1. Operating model

```text
Founder judgment
└── Company trust spine
    ├── Official-source layer
    ├── Website + proof hub
    ├── Research + customer-language layer
    ├── Product/app delivery layer
    ├── Consulting/service delivery layer
    ├── Commerce/payment/tax layer
    └── Governance + liability-reduction layer
```

The right stack is not “all tools now.” It is:

1. **Now:** control, trust, research, proof, and risk registers.
2. **Next:** waitlist/newsletter, payments sandbox, app-store readiness, service contracts.
3. **Later:** advanced analytics, paid ads, CRM/helpdesk automation, product-specific communities.
4. **Watch:** laws/platform rules that can break assumptions.

## 2. Now / next / later / watch matrix

| Layer | Now | Next | Later | Watch |
|---|---|---|---|---|
| Official sources | KVK, Belastingdienst, AP, Business.gov.nl, RVO, IND, ACM, SRC, EU Commission | adviser-reviewed extracts/checklists | automated source freshness dashboard | AI Act, EAA, app-store payments, VAT/OSS, cookie guidance |
| Identity/trust | domain, business email, website, official account list | LinkedIn Page verification path, GitHub domain verification | press/media kit, verified platform badges | impersonation, name conflicts |
| Registers | account register, claims register, processing register, AI tools register, proof-permission log | vendor/DPA register, incident register, payment/tax register | automated access reviews | stale accounts, platform rule changes |
| Research | Reddit Pro/listening, LinkedIn comments, customer-language board | waitlist/interview form, source-coded insights | panel/community | privacy/consent drift |
| Analytics | UTMs, server logs, privacy-light aggregate analytics | Plausible/PostHog only after privacy review | event instrumentation, funnels, cohorts | cookie/ePrivacy rules |
| Commerce | no live paid stack until wedge is selected | Paddle/FastSpring/Stripe decision; RevenueCat for apps | dunning, annual plans, pricing tests | VAT/OSS, app billing rules, DSA trader data |
| App stores | App Store/Play readiness checklist | RevenueCat + StoreKit/Play Billing sandbox | paywall experimentation | Apple/Google payment changes, privacy labels |
| Consulting | scoped SOW templates, support/legal caveats | Stripe Invoicing + Moneybird | CRM/helpdesk, recurring retainers | professional liability, client sectors |
| Dev/ops | GitHub org, secret scanning, basic CI, Sentry later | App telemetry if app candidate | SOC2-lite controls for B2B | security incidents, dependency issues |

## 3. Official-source operating library

| Source | Use it for | Phase |
|---|---|---|
| KVK eenmanszaak | legal form, liability, trade names, activities | now |
| KVK business-name/trademark pages | naming, trade name vs brand/trademark, public Business Register implications | now |
| Business.gov.nl legal forms/liability | entity choice and personal liability comparison | now |
| Belastingdienst VAT / OSS / services | VAT entrepreneur status, VAT ID, EU B2C digital services, OSS | next before paid sales |
| RVO WBSO | technical R&D planning and future-work application timing | project-specific |
| IND HSM/self-employed/startup | founder work-rights and public-status caveats | before public immigration/work claims |
| Autoriteit Persoonsgegevens | GDPR, processing register, cookies, datalek, data subject rights | now before lead capture |
| ACM / Business.gov.nl consumer/e-commerce/email | online sales, reviews, email marketing, information duties | before B2C paid sale |
| Stichting Reclame Code | creator/influencer/affiliate disclosure | before partnerships |
| EU Commission AI Act | AI feature classification, AI disclosure, provider/deployer obligations | before AI productization |
| EAA / accessibility official sources | e-commerce/product accessibility obligations and claims | before consumer-facing paid launch |
| Apple Developer | App Review, IAP, app privacy, DSA trader info | before iOS launch |
| Google Play Developer | billing, payments policy, data safety, subscriptions API | before Android launch |

## 4. Commercial stack inventory

| Business model | Default stack | Why | Avoid |
|---|---|---|---|
| iOS/Android paid app or subscription | Apple IAP + Google Play Billing + RevenueCat + Moneybird | app-store policy fit, one entitlement layer, simpler store reconciliation | using Stripe/Paddle inside app for app-native digital goods unless explicitly allowed by jurisdiction/program |
| Web micro-SaaS / digital product | Paddle as default Merchant of Record; FastSpring if B2B quotes/localization matter | reduces global VAT/sales-tax operational burden | custom tax engine before PMF |
| Web SaaS needing full control | Stripe Billing + Stripe Tax + Moneybird/Exact | maximum control and ecosystem | assuming Stripe Tax equals MoR liability shift |
| Consulting / productized services | Stripe Invoicing or bank transfer + Moneybird; SOW/MSA templates | simple B2B invoicing and accounting | app-store billing; Lemon Squeezy for services |
| Content/templates | Paddle or Lemon Squeezy if digital-only and approved; otherwise Stripe | simple digital sale | presenting templates as legal/tax/accounting advice |

## 5. Public APIs and developer surfaces worth knowing

| API / CLI / surface | Use | Phase | Caveat |
|---|---|---|---|
| KVK APIs | Dutch company lookup, KVK-number validation, B2B onboarding prefill | later for Dutch ZZP/B2B tooling | API key/terms/cost; not needed for static site |
| EU VIES VAT validation | EU VAT number validation for B2B reverse-charge workflows | paid B2B EU SaaS | official VIES is SOAP/availability can vary; keep validation logs |
| VAT rate APIs | estimating VAT by country | paid commerce prototype | use official/tax-provider source for production; unofficial APIs are convenience, not authority |
| Stripe API / CLI | invoices, subscriptions, tax, webhooks, test mode | next if Stripe path | direct merchant responsibility remains |
| Paddle API | transactions, subscriptions, customers, webhooks, MoR commerce | next if MoR path | provider approval and product eligibility |
| FastSpring API | B2B quotes, invoices, subscriptions, localization | later if B2B/international checkout complexity | heavier vendor relationship |
| RevenueCat API | entitlements, offerings, web billing, app subscriptions | next for app subscriptions | still depends on Apple/Google/store setup |
| App Store Connect API | apps, subscriptions, IAP, reports | app lane | requires Apple program, roles, secrets, privacy labels |
| Google Play Developer API | purchases/subscriptions, orders, Play Billing operations | app lane | requires Play Console setup and policy compliance |
| GitHub API / CLI | org/repo automation, issues, releases, secret/security workflows | now/later | do not automate public issue replies without review |
| Google Search Console API | organic search performance for official site | later after site indexed | not a substitute for privacy-safe analytics |
| PostHog API / SDK | product analytics, feature flags, surveys | later | cookie/privacy and EU data processing review |
| Sentry SDK / API | crash/error monitoring | next for apps/SaaS | SDK privacy review; avoid collecting personal data unnecessarily |

## 5.1 Platform automation and distribution APIs

Use native platform APIs only when they are explicitly allowed and when the account has a human approval step. For early trust-building, automation should collect signals, prepare drafts, and update internal dashboards — not post, comment, DM, vote, or manipulate engagement automatically.

| Platform/API | Safe early use | Keep manual | Policy notes |
|---|---|---|---|
| LinkedIn Marketing APIs | reporting, organic-post metadata, company-page analytics, controlled publishing only after access approval | founder posts, sensitive announcements, relationship comments/DMs | API access is permissioned; Verified/Page badges are trust signals, not endorsements; do not scrape or automate human relationship-building. |
| GitHub REST/GraphQL/CLI | org/repo automation, issues/releases, scheduled workflows, documentation publishing, secret/security checks | security-sensitive approvals and public incident statements | GitHub CLI and Actions are strong internal automation surfaces; keep least privilege and avoid leaking tokens. |
| YouTube Data API | playlist/caption/video metadata workflows, analytics exports where authorized | final upload/title/claims/disclosures for important videos | OAuth consent is required; quota applies; developer policies restrict storage/aggregation and destructive actions without explicit user consent. |
| Product Hunt API | research and page/status lookup where supported | posting, commenting, launch-day engagement, voting | Launching is personal-account/community-driven; coordinated voting/incentives are prohibited. |
| Reddit Pro / Reddit tooling | trends, keyword monitoring, drafting/scheduling where provided | community participation, replies, product links | Treat Reddit as listening first; do not scrape/reuse user content without permission. |
| Pinterest API | pin scheduling/content workflows, analytics ingestion, conversion data after consent review | brand positioning and claims-heavy pins | Developer guidelines restrict unnecessary storage/sharing; commercial/branded content must be disclosed. |
| TikTok Content Posting API / Share Kit | draft upload and approved publishing workflows once app is audited | native creative direction, disclosures, comment/DM engagement | Direct Post restrictions apply until audit; shared content should avoid watermarks/promotional overlays; AI/commercial labels may be needed. |
| Meta / Instagram APIs | Business Suite scheduling/insights when eligible; branded-content tooling | founder/community replies, DMs, sensitive posts | Automated access/collection without express permission is restricted; branded content and AI/manipulated media labels must be handled in-platform. |
| Google Analytics / Search Console | aggregate acquisition and SEO reporting | user-level tracking without consent basis | Prefer privacy-light analytics first; add GA4/ads pixels only after cookie/privacy review. |

Automation rule: if it can create public speech, user contact, paid targeting, or account-level side effects, keep a human approval checkpoint.

## 6. Local internal accelerators already in the repo

| Local resource | Use | Suggested next action |
|---|---|---|
| `docs/api-intelligence-map.md` | existing tool/API matrix including PostHog, Stripe, Lemon Squeezy, Paddle, Vercel, Supabase | adapt into a current, NL/EU-specific commercial-readiness matrix |
| `integrations/mcps/README.md` | MCP server map: Stripe, PostHog, GitHub, Google Sheets, Zapier/Composio options | use once real accounts/API keys exist; do not connect before privacy/vendor register |
| `tools/daily-os/` | daily operating-system patterns | adapt into founder weekly/monthly trust cadence |
| `tools/content-factory/` | content production system | use after positioning is approved |
| `tools/market-scanner/` | market research workflows | use for ICP/customer-language capture |
| `tools/revenue-modeler/` | revenue modeling | use when first product/payment path chosen |
| `skills/claude-code/brand.md` | audience-first and platform-selection guidance | keep as brand/content operating reference |
| `skills/claude-code/launch.md` | launch asset generator | use when first product is launch-ready |
| `skills/claude-code/legal-tax-structure.md` | tax/entity-stage thinking, but US-centric | use only as pattern inspiration; replace with Dutch adviser/source review |
| `personal-finance/ai-context/compliance/rules_checklist.md` | Dutch WBSO/tax/eenmanszaak red lines from prior work | reference carefully; re-verify current rules before action |
| `paperclip_setup/tasks/atomic-task-generator.sh` | generates atomic tasks for build/research/GTM | useful once product/site implementation begins |

## 7. Recommended stack decisions by timing

### Choose now

- canonical website/CMS/hosting approach;
- business email provider and aliases;
- password manager and backup owner process;
- account/security/claims/processing/AI tools registers;
- privacy-light analytics approach;
- research board format;
- proof library structure.

### Choose after first CTA

- waitlist/newsletter provider;
- CRM/helpdesk or just inbox;
- MoR vs Stripe for paid web products;
- RevenueCat if app subscriptions are next;
- accounting package after accountant review.

### Choose after revenue/support signal

- product analytics depth;
- paid ad/pixel stack;
- helpdesk/SLA/status page;
- contract automation;
- DPA/security posture for B2B.

## 8. “Do not add yet” list

- full CRM before repeated inbound;
- retargeting pixels before cookie/privacy review;
- multiple paywall tools at once;
- three payment providers before product-market fit;
- separate product/social accounts before cadence/support exists;
- AI automation that posts, replies, supports, or advises publicly without human approval;
- high-risk products requiring legal/tax/medical/safety advice without entity/insurance/legal review.

## 9. Recommended next concrete actions

1. Build the official company site trust spine.
2. Decide the first wedge and CTA.
3. Create register templates as operational files/sheets from `appendix/register-templates.md`.
4. Choose privacy-light analytics.
5. Pick accounting tool with Dutch accountant input.
6. If app lane leads: create App Store / Google Play / RevenueCat readiness checklist.
7. If micro-SaaS lane leads: run Paddle vs Stripe vs FastSpring decision memo.
8. If consulting lane leads: create low-liability consulting SOW template and prohibited-project list.
