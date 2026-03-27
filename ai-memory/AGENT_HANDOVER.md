# Complete Agent Handover Document
**Generated**: 2026-03-27
**Project**: Solo founder — building SaaS products
**Primary tool**: SoloOS V10 (MCP server, 33 tools)

---

## The Founder

Dutch resident (Indian national), Highly Skilled Migrant visa, solo founder alongside full-time job.
Has a young child. 30% tax ruling expires Sep 2027. Financial strategy locked: clear India plot loan Q1 2027, gift deed Q2 2027.

Full profile: `founder/profile.md`

---

## Active Work (Do This First)

### 1. GovProcure AI — URGENT (Kill signal in 8 days)
**What**: B2B SaaS for government contractors to find RFPs faster. Beats GovWin IQ ($40K/yr) at $299/mo.
**Status**: $0 MRR, validation phase. Automated sales pipeline being set up.
**Kill signal**: Due 2026-04-05. New criteria: <8 total signals from email+landing+ads in 10 days = kill.
**Next action**: Launch Apollo → Instantly sequence (200 contacts) + Carrd landing page + Google Ads ($100)
**Full details**: `products/govprocure/`

### 2. TapTap iOS App — Pre-Launch
**What**: iOS tutorial app for seniors learning iPhones.
**Status**: Code done (25 tutorials, 697 tests, P0/P1 fixes committed). Blocked on META P0s (founder must fill EAS.json, fix privacy policy).
**Next action**: Founder fills META-P0-1 through META-P0-4
**Full details**: `products/taptap/overview.md`

---

## Products at a Glance

| Product | Stage | Score | Next Action |
|---|---|---|---|
| GovProcure AI | Validating | 8/10 | Launch pipeline TODAY |
| TapTap | Pre-launch | 7/10 | Founder fills META P0s |
| SnoozeTales | Parked | 5.8→7/10 | Fix pricing ($12.99) then build |
| ScamAlert | Parked | 7/10 | Bank pitch deck when ready |
| FSMA 204 | Parked | 7.5/10 | Entry window Q2 2026–Q1 2027 |
| Pharmacy PBM | Parked | 6.5/10 | Research complete, not started |
| RFP Response | ❌ Rejected | 3.5/10 | Do not revisit |
| HS Codes | ❌ Rejected | 2/10 | Do not revisit |
| AI Newsletter | ❌ Rejected | 2/10 | Do not revisit |

---

## Technical Stack

### SoloOS V10 (Infrastructure)
- MCP server: 33 tools, Python 3.11, `mcp/soloos-core/`
- Test suite: 168 passing, 0 failing (`python -m pytest tests/ -q`)
- Recent fix: webhook_handler module-level imports (FastAPI type resolution bug)

### TapTap (iOS App)
- Expo/React Native, 697 tests, 25 tutorials, all videos at 30fps/700x1520
- Location: `/Users/fsd/Projects/taptap/`

### SnoozeTales (Web/iOS)
- Next.js 14, Supabase, Claude + ElevenLabs + Flux
- Architecture: Result<T,E>, TDD, Zod schemas as source of truth

---

## Tools & Infrastructure

### MCP Servers (Active)
```bash
mcp__soloos-core__check_kill_signals_tool   # ALWAYS run at session start
mcp__soloos-core__get_business_context      # Load MRR, ICP, stage
mcp__soloos-core__run_morning_brief         # Daily priorities
mcp__soloos-core__council_brief             # Hard decisions (reversibility ≤5/10)
mcp__soloos-core__score_opportunity         # Rate new ideas
mcp__soloos-core__enrich_prospect           # Research prospects
mcp__memory-keeper__context_get             # Load prior context
mcp__jina__jina_reader                      # Scrape any URL (free)
mcp__hackernews__getTopStories              # HN research
```

### Projects Layout
```
~/Projects/
├── soloprenuership/    # SoloOS + GovProcure (ACTIVE)
├── taptap/             # iOS tutorial app
├── ideas-project/      # All idea research (GitHub: datareaper247/ideas-project)
├── personal-finance/   # Financial docs
└── openclaw/           # AI agent setup (partial)
```

---

## Session Protocol (Follow Every Session)

1. `mcp__soloos-core__check_kill_signals_tool` — check overdue signals
2. `mcp__soloos-core__get_business_context` — load stage/MRR
3. If kill signal overdue: surface IMMEDIATELY before answering

**Every recommendation must end with**:
```
KILL SIGNAL: If [specific measurable outcome] does not happen within [30 days], stop.
```

---

## Anti-Patterns (What NOT to Do)

- ❌ Manual DMs for validation — use automated pipeline instead
- ❌ SEO/content/brand at $0 MRR — too early
- ❌ Multiple ICPs at once — pick one
- ❌ Building SnoozeTales at $6.99/mo pricing — unit economics broken
- ❌ Recommending VC fundraising — bootstrap path preferred
- ❌ Re-opening rejected ideas (RFP software, HS codes, AI newsletter)
- ❌ Treating crypto as material asset — ~€4-5K actual value

---

## Open Decisions (Not Yet Made)

1. TapTap: Should Supabase be removed for MVP? (simplification analysis pending)
2. GovProcure: Which channel wins in pipeline test? (results in 10 days)
3. Eenmanszaak: KOR threshold — €20K or €30K? (verify at belastingdienst.nl)
4. FSMA 204: Build or pass? (decide by Q4 2026)
5. SnoozeTales: Implement $12.99 pricing fix then build, or park indefinitely?
