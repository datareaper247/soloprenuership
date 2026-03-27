---
last_updated: 2026-03-27
status: Building — due by 2026-04-05
---

# GovProcure Validation Pipeline

## Strategy
Automated sales pipeline metrics replace manual DM validation.
Sales funnel conversion = market signal. No human responses required.

## Pipeline Architecture
```
[Awareness] → [Interest] → [Intent]
     ↓               ↓            ↓
   Ad CTR      Page→Signup    "Buy/Demo" click
   >2% = pain   >8% = real    >15% of signups = validated
   exists       problem       willingness to pay
```

## Channel 1: Cold Email (Instantly.ai)
- **Source**: Apollo.io free tier (50 exports/mo)
- **Sequence**: Day 0 → Day 3 follow-up → Day 7 break-up
- **Volume**: 200 contacts, 40/day send limit
- **3 variants running in parallel**: Pain-led (A), Price-shock (B), Social-proof (C)
- **Full copy**: See `agents/prompts/govprocure-validation.md`

## Channel 2: Landing Page (Carrd)
- **Headline**: "Stop missing RFPs. GovProcure watches SAM.gov 24/7."
- **CTA**: Fake door — "Start Free Trial" → waitlist capture
- **Domain**: govprocure.ai (to register)
- **Cost**: $19/mo

## Channel 3: Google Ads ($100 budget)
- **Keywords**: [government contract opportunities], [SAM.gov RFP search tool], [GovWin IQ alternative], etc.
- **Budget**: $15/day × 7 days = $105
- **Expected**: 400-600 impressions, 20-40 clicks

## Channel 4: LinkedIn (Organic)
- **Tactic**: Connect with Capture Managers + BD Directors
- **Message**: Variant C (personalized with real NAICS data)

## Kill Metrics (10 days from launch)
| Channel | Kill if | Continue if |
|---|---|---|
| Email open rate | <25% | >40% |
| Email reply rate | <3% from 60+ sends | >6% |
| Landing page CTA | <2% of visitors | >5% |
| Google Ads CTR | <2% | >4% |
| Total waitlist signups | <5 | >15 |

**Overall**: If email + ads both miss AND <5 signups → kill.
If 1 channel hits → message problem, not market problem.
If all channels hit → build.

## Stack
| Tool | Purpose | Cost |
|---|---|---|
| Apollo.io | Prospect sourcing | Free tier |
| Instantly.ai | Email sequences | $37/mo |
| Carrd | Landing page | $19/mo |
| Google Ads | Paid traffic | $100 budget |
| Airtable | Pipeline tracking | Free |
