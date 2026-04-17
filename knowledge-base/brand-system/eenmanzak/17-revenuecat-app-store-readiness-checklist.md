# RevenueCat / App Store Readiness Checklist

**Status:** Draft operating checklist; App Store / Google Play / tax / privacy review required
**Last updated:** 2026-04-17
**Applies to:** TapTap and future paid iOS/Android app subscriptions or in-app purchases.

> Use this checklist before any paid app-store launch. It assumes digital content/features consumed inside the app use Apple In-App Purchase and/or Google Play Billing, with RevenueCat as the entitlement/subscription backend.

## 1. Decision rule

Use this path when:

- the product is a native mobile app;
- users buy digital content, subscriptions, or app features consumed inside the app;
- the product is distributed through App Store / Google Play;
- entitlement consistency across iOS/Android/web matters.

Do not use this path for:

- consulting services;
- external physical goods/services;
- web-only SaaS checkout;
- high-risk safety/medical/navigation claims without legal review.

## 2. Architecture

```text
Mobile app
├── Apple StoreKit / In-App Purchase
├── Google Play Billing
├── RevenueCat SDK + dashboard
├── Entitlements / Offerings / Products
├── App Store Connect / Play Console product setup
├── Privacy + support + terms URLs
├── Accounting reconciliation
└── Optional later: Superwall or Adapty for paywall experimentation
```

## 3. Pre-build readiness

- [ ] Product is outside the red/prohibited liability list.
- [ ] App claims are checked against `09-claims-compliance-register.md`.
- [ ] App privacy data inventory drafted.
- [ ] SDK list drafted, including RevenueCat and analytics/crash tools if any.
- [ ] Support email/page exists.
- [ ] Privacy page exists.
- [ ] Terms/subscription page exists.
- [ ] Refund/cancellation support expectations documented.
- [ ] App Store / Google Play account roles and MFA configured.
- [ ] Legal/trade name and trader/contact info verified.

## 4. App Store Connect checklist

- [ ] Apple Developer membership active.
- [ ] Agreements, tax, and banking complete.
- [ ] App record created.
- [ ] Bundle ID correct.
- [ ] App category selected.
- [ ] Age rating complete.
- [ ] Privacy URL entered.
- [ ] Support URL entered.
- [ ] Marketing URL / official site entered if applicable.
- [ ] App Privacy Details completed from actual data practices.
- [ ] In-App Purchase products/subscriptions created.
- [ ] Subscription group configured if using subscriptions.
- [ ] Localizations/prices reviewed for target countries.
- [ ] Review notes include test account/instructions if needed.
- [ ] Screenshots/previews match real app behavior.
- [ ] Claims avoid legal/tax/medical/safety/accessibility overstatement.

## 5. Google Play Console checklist

- [ ] Developer account active.
- [ ] Payments profile complete.
- [ ] App created.
- [ ] Package name correct.
- [ ] Store listing drafted.
- [ ] Privacy Policy URL entered.
- [ ] Data Safety section completed from actual SDK/data inventory.
- [ ] Subscription/in-app products created.
- [ ] License testers configured.
- [ ] Closed/internal testing track configured.
- [ ] Target countries reviewed.
- [ ] Support/contact details entered.
- [ ] Claims align with actual app behavior and claims register.

## 6. RevenueCat setup checklist

- [ ] RevenueCat project created.
- [ ] iOS app configured.
- [ ] Android app configured if relevant.
- [ ] App Store Connect integration configured.
- [ ] Google Play integration configured if relevant.
- [ ] Products imported or mapped.
- [ ] Entitlements defined.
- [ ] Offerings configured.
- [ ] SDK installed.
- [ ] Anonymous/user identity strategy documented.
- [ ] Purchase flow tested.
- [ ] Restore purchases tested.
- [ ] Expiration/revocation tested.
- [ ] Refund/cancellation behavior understood.
- [ ] Webhooks configured only if needed and secured.
- [ ] RevenueCat listed in vendor/processor register.
- [ ] Privacy/Data Safety labels updated for RevenueCat data use.

## 7. Test scenarios

### Purchase and entitlement

- [ ] New user sees paywall/offer correctly.
- [ ] Purchase succeeds.
- [ ] Entitlement unlocks immediately.
- [ ] App restart preserves entitlement.
- [ ] Offline state behaves safely.
- [ ] Backend/RevenueCat state matches app state.

### Restore and account state

- [ ] Restore purchases works.
- [ ] Existing subscriber on new device regains access.
- [ ] Signed-out/signed-in state does not leak entitlements across users.
- [ ] Deleting/reinstalling app does not break restore.

### Subscription lifecycle

- [ ] Trial start if used.
- [ ] Trial conversion.
- [ ] Renewal.
- [ ] Expiration.
- [ ] Cancellation.
- [ ] Refund/revocation.
- [ ] Billing retry/grace period if used.

### Store review

- [ ] Review account/instructions work.
- [ ] App does not mention unsupported external payment flows.
- [ ] Support/terms/privacy links are live.
- [ ] Subscription terms are visible and accurate.

## 8. Privacy and compliance checks

- [ ] App privacy labels match code and SDKs.
- [ ] Data Safety section matches code and SDKs.
- [ ] No unnecessary personal data collected.
- [ ] No sensitive data in analytics events.
- [ ] Crash/error monitoring redacts personal data.
- [ ] Consent/cookie/tracking requirements reviewed if web views or tracking SDKs are used.
- [ ] AI-generated content or AI features are disclosed where platform/law requires.
- [ ] Accessibility claims are supported by actual review/testing.

## 9. Product-specific caveats

### TapTap

Safe positioning:

> “Designed to support digital confidence for older adults.”

Avoid:

- guaranteed learning outcomes;
- medical/cognitive claims;
- “clinically proven”;
- real Apple UI/trademark/IP issues without review;
- misleading senior-vulnerability marketing.

### SpatialSense

Safe positioning:

> “Experimental assistive spatial-awareness concept.”

Avoid:

- “safe navigation”;
- “replaces cane/guide dog”;
- “prevents accidents”;
- medical device implication;
- selling before safety/product-liability review.

## 10. Launch readiness gate

Do not submit paid app release until all are true:

- [ ] Payment/IAP test scenarios pass.
- [ ] Restore/cancel/refund behavior understood.
- [ ] Privacy/support/terms URLs live.
- [ ] App privacy/data-safety declarations complete.
- [ ] Store listing avoids risky claims.
- [ ] Support inbox works.
- [ ] Revenue accounting path exists.
- [ ] Claims register checked.
- [ ] No red-tier liability claims.

## 11. Future optimization

Only after first real conversion/retention data:

- Superwall or Adapty paywall testing;
- pricing experiments;
- annual plan;
- localized pricing;
- win-back offers;
- lifecycle emails/push notifications;
- advanced product analytics.

Do not add growth tooling before the core entitlement/support/privacy system is stable.
