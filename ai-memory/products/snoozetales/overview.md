---
last_updated: 2026-03-27
stage: Parked — unit economics fix required before building
verdict: 5.8/10 → potential 7-8/10 with fixes
---

# SnoozeTales — AI Bedtime Stories

## What It Is
iOS/web app that generates personalized, AI-narrated bedtime stories for children.
Stories read themselves — parent taps once, app takes over.

## Market
- Apps for Kids: $2.1B (2025) → $22.34B (2035) at 26.71% CAGR
- TAM: ~45M children in English-speaking markets
- **Threat**: Google Gemini Storybook launched Aug 2025 — FREE, 45 languages

## Unit Economics Problem (CRITICAL — FIX BEFORE BUILDING)
**Current**: $6.99/mo pricing, $0.66-1.40/story cost at 20 stories/user = -99% margin
**Required fix**:
1. Price: $6.99 → $12.99/mo
2. Cost: Reduce to <$0.20/story (use Haiku, fewer images, pre-recorded audio)
3. Result: -99% margin → +68% margin

## Correct Pricing Model
```
FREE:      3 stories/mo, standard voices, no downloads
PREMIUM:   $12.99/mo (was $6.99) — unlimited, premium voices, downloads, custom chars
ANNUAL:    $89.99/yr (~$7.50/mo, 42% discount)
LIFETIME:  $99.99 one-time (was $79.99)
```

## Differentiation (vs Google Gemini Storybook)
1. Hands-free experience (tap once, auto-play)
2. Character continuity (stories build on prior ones)
3. Warm narration (not robotic)
4. 100% content safety guarantee
5. Deeper personalization

## Tech Stack
- Frontend: Next.js 14 (App Router) + Tailwind + Zustand
- Backend: Supabase (PostgreSQL, Auth, Storage)
- AI: Claude 3.5 Sonnet (story text) + Flux/Replicate (images) + ElevenLabs (voice)
- Hosting: Vercel
- Pattern: Result<T,E>, TDD, Zod schemas as source of truth

## Financial Projection (Post-Fix)
- Break-even: Month 4-5
- MVP cost: $9,500 (bootstrappable)
- Year 1 revenue (optimistic): $9.2M

## Regulatory Flags
- COPPA compliance deadline: April 22, 2026
- EU AI Act: Aug 2, 2026 — AI-generated content labeling required
- Biometric data (voiceprints) = personal info under COPPA

## Status
Parked. Unit economics analysis done. Do NOT build until pricing/cost fix is implemented.
