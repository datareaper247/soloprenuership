---
last_updated: 2026-03-27
---

# Active Kill Signals

## FL-002 — GovProcure Validation
**Status**: 🟡 WARNING — 8 days remaining
**Due**: 2026-04-05
**Original signal**: "If fewer than 3 people respond positively from 20 DMs in 14 days"
**Updated signal (2026-03-27)**: Manual DMs replaced with automated sales pipeline. See `products/govprocure/validation-pipeline.md`

**New kill criteria** (any channel, 10 days):
- Email: <3% reply rate from 200 sends across 3 variants
- Landing page: <1% CTA click from 500 visitors
- Paid ads: >$50 spent, 0 signups
- Overall: <8 total positive signals across all channels

**Decision**: Build manual concierge version first before coding (original intent)
**Updated approach**: Automated pipeline validation — if pipeline signals confirm demand, skip concierge and build directly

---

## Past Kill Signals (Closed)

| ID | Decision | Kill Signal | Outcome |
|---|---|---|---|
| FL-001 | — | — | — |

---

# Idea Verdicts (Permanent)

| Idea | Score | Verdict | Date |
|---|---|---|---|
| GovProcure AI | 8/10 | BUILDING — validating | 2026-03-26 |
| TapTap (iOS seniors tutorial) | 7/10 | BUILDING — pre-launch | 2026-03 |
| SnoozeTales (AI bedtime stories) | 5.8→7/10 | PARKED — unit econ fix needed | 2026-03-10 |
| ScamAlert (scam detection) | 7/10 | PARKED — validated, bank path | 2026-03-17 |
| FSMA 204 compliance | 7.5/10 | PARKED — window Q2 2026–Q1 2027 | 2026-03-19 |
| Pharmacy PBM audit | 6.5/10 | PARKED — researched, not started | 2026-03-19 |
| Veterinary AI documentation | 6/10 | PARKED — competitive | 2026-03-19 |
| RFP Response/Proposal Gen | 3.5/10 | REJECTED — crowded, duopoly | 2026-03-19 |
| HS Code Classification | 2/10 | REJECTED — avoid | 2026-03-18 |
| AI Agents Digest (newsletter) | 2/10 | REJECTED — saturated, burnout | 2026-03-18 |

---

# Strategic Decisions Log

## Tech Stack — SnoozeTales
Frontend: Next.js 14 (App Router) + Tailwind + Zustand
Backend: Supabase (PostgreSQL, Auth, Storage)
AI: Claude 3.5 Sonnet + Flux (Replicate) + ElevenLabs
Hosting: Vercel
Pattern: Result<T,E> over exceptions, TDD, Zod-first

## Payment Provider — eenmanszaak products
Decision: LemonSqueezy (Merchant of Record, handles EU VAT)
Alternative: Stripe with Tax
Reason: Dutch eenmanszaak, App Store revenue B2B → reverse charge

## AI Development Stack (Jan 2026)
Minimum viable: Claude Code + memory-keeper MCP + Gemini CLI + SSH + tmux
Skip for now: Vector DBs, fancy terminals, multi-model routing
Full stack (when ready): Fly.io bastion + Tailscale + Zellij + tiered memory
