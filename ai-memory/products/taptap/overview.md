---
last_updated: 2026-03-27
stage: Pre-launch (App Store submission prep)
---

# TapTap — iOS Tutorial App for Seniors

## What It Is
iOS app that teaches seniors how to use iPhones/iOS apps through interactive tutorials with video walkthroughs. Targets adults 50+ who struggle with digital devices.

## Target Market
- Primary: Seniors 50+ (especially 65+) learning to use smartphones
- Secondary: Adult children buying/gifting for parents
- Platform: Facebook (primary), YouTube, Pinterest

## Brand
- **Voice**: Patient, Warm, Empowering, Never Condescending
- **Tagline**: "Digital Confidence, Built Together"
- **North Star**: Someone's parent saying "I did it myself"

## Current Status
- **Tutorials**: 25 complete
- **Tests**: 697 (all passing)
- **Interactions**: 81 calibrated
- **Videos**: All rescaled to 700x1520, re-encoded to 30fps
- **Branch**: main (19 commits ahead of origin at last check)

## App Store Submission Blockers
### CODE DONE (committed 2026-03-20, commit 34d14ba):
- UX-P0-2: First-launch overlay
- UX-P0-3: Settings sign-out clears state
- NET-P0-1: Paywall timeout + offline UI
- NET-P0-2: Network reconnect sync
- SEC-H2/H3: Security fixes (localhost removed, SecureStore)
- SUB-001/002/003: Subscription UX fixes
- A11Y fixes, ErrorBoundary, video rescaling

### REQUIRES FOUNDER ACTION (META P0s):
- META-P0-1: Fill EAS.json (Apple ID, team ID, project ID)
- META-P0-2: Rewrite privacy policy (Supabase collects email — must be disclosed)
- META-P0-3: Fix ToS jurisdiction placeholder "[Your Jurisdiction]"
- META-P0-4: Deploy live URLs for privacy + ToS at taptap.app

## Architecture Decision (Pending)
Open question: Can we drop Supabase entirely for MVP?
→ Use RevenueCat + StoreKit only (reduces complexity + review risk)
→ Analysis not yet done

## Marketing (Complete — 48K words across 5 docs)
Located at `/Users/fsd/Projects/taptap/docs/marketing/channels/`
- Content strategy (12-month editorial calendar, 156 posts)
- Social media playbook (FB primary, YouTube, Pinterest)
- Email marketing system (5 complete sequences)
- Community + PR strategy (AARP partnership angle)
- 90-day calendar

## Commands
```bash
cd /Users/fsd/Projects/taptap
npx expo start         # Dev
npx expo run:ios       # Native build
npm test               # Run 697 tests
```

## Legal / IP
- Analysis: `/Users/fsd/Projects/taptap/docs/TAPTAP_LEGAL_IP_ANALYSIS_2026.md`
- Recommendation: Approach 4 (Hybrid) — formal Apple permission request + styled practice zones
- Risk: Showing real iOS UI in tutorials has IP risk; stylized mockups reduce but don't eliminate it
