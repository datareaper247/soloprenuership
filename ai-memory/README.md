# AI Memory — Founder Intelligence Archive

**Last updated**: 2026-03-27
**Maintainer**: SoloOS V10 + Claude Code
**Purpose**: Single source of truth for all project context. Designed for seamless AI agent handover.

---

## Quick Navigation

### If you're a new AI agent → Start here
**[agents/QUICKSTART.md](agents/QUICKSTART.md)** — 5 steps to orient in <2 minutes

### If you're resuming a session
**[founder/current-focus.md](founder/current-focus.md)** — what's active right now
**[decisions/active-kill-signals.md](decisions/active-kill-signals.md)** — what has deadlines

---

## Folder Structure

```
ai-memory/
├── README.md                       ← You are here
├── AGENT_HANDOVER.md               ← Complete handover doc (one file)
│
├── founder/
│   ├── profile.md                  ← Who, where, financial situation
│   └── current-focus.md           ← Active projects + priorities
│
├── products/
│   ├── govprocure/                 ← ACTIVE — validation phase
│   │   ├── overview.md
│   │   ├── financial-model.md
│   │   ├── competitive-intel.md
│   │   └── validation-pipeline.md
│   ├── taptap/                     ← Pre-launch iOS app
│   │   └── overview.md
│   ├── snoozetales/                ← Parked — unit econ fix needed
│   │   └── overview.md
│   ├── scamalert/                  ← Parked — validated
│   │   └── overview.md
│   └── REJECTED/                   ← Do not revisit
│       ├── rfp-response-software.md
│       └── hs-code-classification.md
│
├── research/
│   ├── market-opportunities.md    ← B2B pain points + exit multiples
│   ├── fsma-204.md                ← 7.5/10 — window still open
│   └── pharmacy-pbm.md            ← 6.5/10 — researched, parked
│
├── technical/
│   ├── soloos-core/
│   │   └── architecture.md        ← V10 system design + test suite
│   └── environment.md             ← Tools, versions, project layout
│
├── decisions/
│   └── active-kill-signals.md     ← All kills signals + idea verdicts
│
└── agents/
    ├── QUICKSTART.md              ← 5-step orientation
    ├── session-protocol.md        ← SoloOS session checklist
    └── prompts/
        └── govprocure-validation.md ← Full cold email copy + pipeline
```

---

## Current State (2026-03-27)

| Dimension | Status |
|---|---|
| MRR | $0 (pre-revenue) |
| Active product | GovProcure AI |
| Kill signal | FL-002 due 2026-04-05 (8 days) |
| TapTap | Pre-launch, META P0s pending founder action |
| SnoozeTales | Parked — fix unit economics first |
| SoloOS | V10, 168 tests passing, 33 MCP tools |
| Eenmanszaak | Researched, not registered |

---

## Key Decisions Already Made — Don't Re-Litigate

1. **GovProcure validation**: Automated pipeline > manual DMs
2. **TapTap architecture**: Keep Supabase for now (pending simplification analysis)
3. **SnoozeTales pricing**: Must be $12.99/mo, not $6.99 (unit economics)
4. **ScamAlert form factor**: WhatsApp bot + web first, mobile app later
5. **Payment provider**: LemonSqueezy (MoR, EU VAT handled)
6. **RFP software**: Rejected — do not revisit (3.5/10)
7. **HS codes**: Rejected — do not revisit (2/10)
8. **AI newsletter**: Rejected — do not revisit (saturated)
9. **Crypto holdings**: ~€4-5K actual (NOT €50-200K as misreported earlier)
10. **Financial strategy**: Tax-Optimized Builder — clear plot loan Q1 2027, gift deed Q2 2027

---

## How to Keep This Updated

After significant sessions, run:
```
mcp__memory-keeper__context_save with category: "progress"
```

Then update the relevant file in `ai-memory/` manually or ask Claude to update it.

This folder is tracked in git (`soloprenuership` repo).
