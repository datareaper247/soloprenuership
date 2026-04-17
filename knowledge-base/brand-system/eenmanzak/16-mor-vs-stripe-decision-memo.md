# Decision Memo — Merchant of Record vs Stripe for Web Micro-SaaS

**Status:** Draft decision memo; professional tax/accounting review required before paid launch
**Last updated:** 2026-04-17
**Decision owner:** Founder + accountant/tax adviser
**Applies to:** Web micro-SaaS, paid web apps, digital products, templates, and non-app-store software sold internationally.


## Company mandate alignment

Interpret this document through `00-company-mandate-and-alignment.md`: the company is an AI-first founder-led software company using senior software engineering and ecommerce/logistics expertise to build B2B/B2C apps, SaaS/micro-SaaS, consulting, R&D, OSS/content authority, and multiple revenue streams. Dutch ZZP, TapTap, SpatialSense, and SoloOS are lanes, not the entire company identity.

> This memo does **not** apply to app-native digital goods consumed inside iOS/Android apps. For those, start with Apple In-App Purchase / Google Play Billing and RevenueCat unless a specific platform-permitted alternative path is reviewed.

## 1. Decision to make

Choose the first web-commerce path for paid digital products:

```text
Option A — Merchant of Record: Paddle or FastSpring
Option B — Direct merchant: Stripe Billing + Stripe Tax
Option C — Defer paid web checkout until the offer is validated manually
```

## 2. Recommendation

### Default recommendation

Use **Paddle as the default first web micro-SaaS Merchant of Record** if the first paid web offer is:

- software/digital product;
- sold to customers in multiple countries;
- low-touch or self-serve;
- not consulting/services;
- not app-native digital goods consumed inside iOS/Android apps;
- not a regulated legal/tax/accounting/medical/safety product.

### Use FastSpring instead if

- B2B quotes/localized invoices are central;
- sales motion is more enterprise/procurement-like;
- you need stronger quote/invoice workflow than simple self-serve checkout.

### Use Stripe Billing + Stripe Tax if

- direct merchant/customer relationship matters more than simplicity;
- you need custom checkout, custom usage billing, or tight product integration;
- you have accountant/tax support ready;
- you accept tax registration/reporting/filing responsibility;
- you want more control over disputes, invoices, refunds, and data flows.

### Defer paid checkout if

- no validated paid offer yet;
- privacy/terms/support pages are not live;
- pricing and buyer type are unclear;
- claims register has unresolved high-risk claims;
- no accounting workflow exists.

## 3. Why this matters

For international micro-SaaS, the payment provider is not just “checkout.” It affects:

- VAT/sales tax/GST collection;
- invoice/tax-document quality;
- refund/cancellation operations;
- consumer-rights expectations;
- support workload;
- merchant liability and platform dependence;
- accounting reconciliation;
- privacy/vendor processing register;
- pricing experiments;
- chargebacks/disputes;
- whether you can sell globally without opening tax registrations too early.

## 4. Option comparison

| Criterion | Paddle / FastSpring MoR | Stripe Billing + Stripe Tax | Manual invoice / defer |
|---|---|---|---|
| Global VAT/sales tax ops | Provider handles covered transaction tax/remittance | You own setup, registrations, reporting/filing decisions | Usually limited to B2B/manual scope |
| Checkout control | Lower | High | Low/medium |
| Speed for solo founder | High if approved | Medium; more setup decisions | High for early validation |
| B2C suitability | High for digital products | Possible but more compliance work | Poor at scale |
| B2B suitability | Paddle ok; FastSpring stronger for quotes | Strong | Strong for consulting/custom work |
| App-store app fit | Not for app-native digital goods unless platform-permitted | Not for app-native digital goods unless platform-permitted | N/A |
| Services/consulting fit | Usually not ideal; Lemon Squeezy often not suitable | Strong with invoicing | Strong |
| Accounting | payouts need reconciliation | direct transactions/invoices | invoices/bank transfers |
| Liability reduction | Tax/payment ops reduced for covered sales | More retained responsibility | Depends on contract/invoice |
| Lock-in | Medium | Medium/low | Low |

## 5. Decision criteria

Score each 1–5.

| Criterion | Weight | Paddle/FastSpring | Stripe | Defer/manual |
|---|---:|---:|---:|---:|
| International tax simplicity | 25% | 5 | 3 | 2 |
| Speed to first paid test | 20% | 4 | 3 | 5 |
| Checkout/control flexibility | 15% | 3 | 5 | 2 |
| Accounting simplicity | 15% | 4 | 4 | 4 |
| B2B invoice/quote needs | 10% | 4 FastSpring / 3 Paddle | 4 | 5 |
| Refund/dispute/support clarity | 10% | 4 | 4 | 3 |
| Vendor/product eligibility risk | 5% | 3 | 4 | 5 |

Use MoR when tax simplicity and speed dominate. Use Stripe when control and custom billing dominate.

## 6. Product fit table

| Offer type | Recommended path | Notes |
|---|---|---|
| Dutch ZZP checklist/template | Paddle or manual invoice test | Must not imply legal/tax advice. Use permission/terms/privacy. |
| Dutch ZZP SaaS subscription | Paddle first, Stripe later if custom control needed | Watch VAT/OSS and source-linked claims. |
| SoloOS-style web tool | Paddle first | Good for international digital product test. |
| Consulting sprint | Stripe Invoicing / bank transfer + Moneybird | Use SOW/MSA. Avoid MoR unless productized digital deliverable. |
| TapTap app subscription | Apple IAP / Google Play Billing + RevenueCat | Not Paddle/Stripe inside app for app-native digital content. |
| SpatialSense concept | No paid sale until safety/legal review | Avoid safety-critical claims. |

## 7. Readiness checklist before choosing MoR or Stripe

- [ ] First paid offer is defined.
- [ ] Buyer is B2B, B2C, or mixed.
- [ ] Product is not in prohibited/high-liability list.
- [ ] Terms/refund/cancellation language drafted.
- [ ] Privacy notice live.
- [ ] Cookie/analytics approach chosen.
- [ ] Support route live.
- [ ] Claims register checked.
- [ ] Accounting package selected or adviser consulted.
- [ ] Tax/VAT/OSS implications reviewed.
- [ ] Provider eligibility reviewed.
- [ ] Test-mode purchase/refund/cancellation flow documented.

## 8. Implementation path — Paddle/FastSpring

1. Confirm product is digital/software and provider-eligible.
2. Create vendor account with business/legal details.
3. Configure product, pricing, refund terms, customer emails.
4. Configure webhook endpoints only after security review.
5. Add checkout link on staging page only.
6. Test purchase, cancellation, invoice/receipt, refund, and support flow.
7. Record provider in vendor/processor register.
8. Reconcile test payout/accounting workflow.
9. Add source/caveat entry to claims register if public copy mentions MoR/tax handling.
10. Go live only after terms/privacy/support pages are live.

## 9. Implementation path — Stripe

1. Create Stripe account with correct business/legal details.
2. Choose Stripe Billing model: one-time, subscription, usage-based, or invoices.
3. Configure Stripe Tax only after identifying registrations/thresholds/adviser path.
4. Configure products/prices/test checkout.
5. Configure webhooks securely.
6. Configure customer portal if subscriptions.
7. Test purchase, invoice, receipt, cancellation, refund, failed payment, and tax behavior.
8. Record Stripe in vendor/processor register.
9. Set up accounting reconciliation.
10. Do not claim tax compliance; say tax handling is configured/reviewed as applicable.

## 10. Decision recommendation for first 90 days

Until the first paid web offer is clear:

```text
Do not choose final provider.
Prepare two sandbox paths:
- Paddle for self-serve digital product / micro-SaaS.
- Stripe Invoicing for consulting/services.
```

Once a specific paid offer is chosen:

- app-native subscription → RevenueCat + Apple/Google billing;
- web SaaS/digital product → Paddle first;
- consulting → Stripe Invoicing + Moneybird;
- complex B2B web sale → FastSpring or Stripe after adviser review.

## 11. Source anchors

- Paddle sales tax / MoR documentation.
- FastSpring Merchant of Record and VAT/sales-tax documentation.
- Stripe Billing and Stripe Tax documentation.
- Apple App Review Guidelines / In-App Purchase documentation.
- Google Play Payments policy / billing documentation.
- Existing `09-claims-compliance-register.md` and `12-commercial-readiness-playbooks.md`.
