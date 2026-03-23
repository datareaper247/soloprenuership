# SoloOS v5 — Claude Code Setup Optimization
## Analysis & Implementation Report — March 2026

---

## Executive Summary

This document captures the holistic optimization of the SoloOS cognitive operating system for solo founders. The work was conducted via multi-agent analysis (4 parallel specialist agents + Gemini CLI deep analysis) and implemented across two sessions in March 2026.

**Core finding**: The system had a fundamental gap — skill files existed and were referenced but never actually read. Every auto-trigger said "See X.md" but Claude used general training instead of the specific frameworks. This undermined the entire 591-line validate.md, 467-line decide.md, and all other skill files.

---

## What Changed (v4 → v5)

### 1. SESSION START PROTOCOL (New)

**Problem**: Kill signal checks, context file loading, and mission alignment were aspirational — described in the KILL SIGNAL CHECK section at the bottom of CLAUDE.md, never enforced at session start.

**Fix**: Added mandatory 4-step protocol at the TOP of CLAUDE.md, before CORE IDENTITY:

```
Step 1 — Kill Signal Check: READ founder-log.md, surface ⏳ Pending entries past due date
Step 2 — Context File Check: READ business-context.md, detect template placeholders → prompt onboarding
Step 3 — Mission Alignment Check: READ mission.md, detect empty → ask once for exit goal
Step 4 — Assumption Drift Check: compare context file vs. today's conversation
```

**Why this matters**: Without enforcement at session start, none of these checks actually ran. Now they're the first thing Claude executes.

---

### 2. SKILL FILE READ ENFORCEMENT (Core Fix)

**Problem**: Every auto-trigger ended with "See `skills/claude-code/X.md`" — a passive reference Claude ignores entirely. The 33 skill files in `skills/claude-code/` were effectively dead weight.

**Fix**: Changed every trigger from:
```
→ Apply [framework]. See `skills/claude-code/X.md`.
```
To:
```
→ READ `skills/claude-code/X.md`. Apply [framework].
```

**Triggers updated** (24 total):
- VALIDATE → READ validate.md
- MORNING → READ morning.md
- DECIDE → READ decide.md
- LAUNCH → READ launch.md
- GROWTH → READ growth.md
- SEO → READ seo.md
- COMPETITOR/INTEL → READ intel.md
- FINANCE → READ finance.md
- PMF → READ pmf.md
- EXIT-PREP-EARLY → READ exit-prep-early.md
- EXIT → READ exit.md
- OPS → READ ops-auto.md
- PSYCHOLOGY → READ psychology.md
- HIRE → READ hire.md
- BRAND → READ brand.md
- CONTENT-FOUNDER → READ content-founder.md
- FUNDRAISING → READ fundraising.md
- TAX-STRUCTURE → READ legal-tax-structure.md
- PRODUCT-MOAT → READ product-moat.md
- POSITIONING → READ positioning.md
- NEGOTIATION → READ negotiation.md
- BANDWIDTH → READ bandwidth.md
- ACQUIHIRE → READ exit.md (acquihire is a subset of exit)
- NETWORK → READ network.md
- WISDOM → READ wisdom.md
- GUNA → READ psychology.md (Guna section)
- KAALA → READ wisdom.md (Kaala section)

---

### 3. MCP TOOL ENFORCEMENT (Critical Decisions)

**Problem**: MCP tools were suggested ("Use calculate_unit_economics") but Claude could pattern-match from training instead. For high-stakes decisions, this is dangerous.

**Fix**: Changed language to MUST for critical triggers:

| Trigger | MCP Tool Enforced |
|---------|-------------------|
| DECIDE | MUST call `search_founder_cases` + `match_pattern` BEFORE answering |
| FINANCE | MUST call `calculate_unit_economics` / `calculate_runway` / `calculate_valuation` / `calculate_ev` |
| PMF | MUST call `score_pmf` |
| EXIT | MUST call `calculate_valuation` |
| INTEL | MUST call `generate_competitor_brief` + `check_market` |
| VALIDATE | MUST call `validate_idea_gates` |
| MOMENTUM-TRAP | MUST call `calculate_unit_economics` before advising |

**Why this matters**: The MCP server contains real founder data and calibrated calculation logic. Using general AI pattern-matching for "what's my runway?" produces worse results than calling the actual tool.

---

### 4. GITHUB ACTION — Kill Signal Automation (Phase 2)

**Implementation**: `.github/workflows/kill-signal-check.yml`

- Runs daily at 9am UTC
- Python parser reads `knowledge-base/personal/founder-log.md`
- Finds entries where `Outcome status: ⏳ Pending` AND `Outcome due:` date is past
- Creates GitHub Issues with deduplication (won't re-open closed issues)
- Labels: `kill-signal`, `founder-log`, `overdue`

**Why this matters**: Kill signals have no value if they're never reviewed. This closes the accountability loop — overdue signals become actionable GitHub Issues even if the founder doesn't start a Claude session.

---

### 5. VERSION FOOTER UPDATE

Updated the trailing description from "SoloOS v3" to v5 with explicit capability declaration:
```
Skills READ their files. MCP tools are enforced. Session start is mandatory. Kill signals are tracked.
```

---

## Architecture Audit Findings

### What Was Already Working Well

1. **Auto-trigger routing**: The pattern-matching system in CLAUDE.md is comprehensive and well-designed. 35+ triggers covering the full founder journey.

2. **Anti-sycophancy protocol**: Structural (not tonal). ANTI-ADVISOR block + ADVERSARY entity for reversibility ≤5/10 is a genuinely superior design to most AI systems.

3. **Kill signal discipline**: The `[[FL-XXX]]` EKG linking + mandatory kill signal on every recommendation is the core value proposition. No other AI system enforces this.

4. **MCP server**: `soloos-core` FastMCP server is fully functional with 10 tools covering unit economics, founder cases, PMF scoring, competitor intel, and idea validation.

5. **Stage calibration**: The inference table (conversation clues → stage detection) is well-calibrated. Prevents giving $50K MRR advice to a $0 MRR founder.

### What Was Broken

1. **Dead skill file references**: "See X.md" never triggered a file read. Fixed.

2. **Session start enforcement**: Kill signal checks ran only if the founder knew to ask. Fixed.

3. **MCP tool optionality**: "Use X tool" is ignored by default. Changed to MUST for critical decisions. Fixed.

4. **Version inconsistency**: Header said v5, footer said v3. Fixed.

### What Remains (v5.1 Roadmap)

1. **Memory OS hooks**: Auto-capture session decisions → founder-log.md without requiring Claude to remember. Needs Mem0 MCP or hook-based capture.

2. **Context file population**: `context/business-context.md` and `context/mission.md` are empty templates. The SESSION START PROTOCOL now prompts for this, but the onboarding UX could be smoother.

3. **Viral distribution**: Install script, demo video, README polish for public release.

4. **Pattern library enrichment**: `knowledge-base/PATTERN_LIBRARY.md` and `knowledge-base/FOUNDER_INTELLIGENCE.md` would benefit from more real founder case data to power the MCP tools.

---

## Multi-Agent Research Council Findings

Four parallel agents (strategy, technical, systems, product) analyzed the codebase and converged on these unanimous findings:

### Finding 1: Memory is the Moat
The EKG system (`[[FL-XXX]]` linking across files) compounds over time. A founder who uses SoloOS for 6 months has a personal decision graph that makes every future recommendation more accurate. This is the headline value prop — not the anti-sycophancy.

### Finding 2: Skill File Gap Was the #1 Failure Mode
Every sophisticated framework in the 33 skill files was invisible. Fixing this alone (READ instructions) likely doubles the quality of triggered responses.

### Finding 3: MCP Enforcement Changes Risk Profile
Changing "use X tool" to "MUST call X tool" for financial calculations, PMF scoring, and decision analysis moves from "suggestion" to "enforcement." This is critical for high-reversibility decisions where hallucinated data causes real harm.

### Finding 4: Session Start Protocol is the Missing Activation Layer
The system was designed to be proactive (kill signals, context drift) but had no mechanism to actually trigger those checks. The 4-step SESSION START PROTOCOL adds the activation layer.

---

## Files Modified

| File | Change |
|------|--------|
| `CLAUDE.md` | SESSION START PROTOCOL added; 24 triggers updated with READ instructions; MCP enforcement on 7 critical triggers; version footer updated to v5 |
| `.github/workflows/kill-signal-check.yml` | New — daily kill signal GitHub Issue creator |
| `skills/claude-code/validate.md` | Gate 0 (ChatGPT Substitution Test) + Terrain Map Protocol added |
| `skills/claude-code/decide.md` | ANALOGOUS CASES section with explicit MCP calls; ANTI-ADVISOR REPORT; Pre-Debate Data Check |
| `docs/soloOS-v5-direction.md` | Full v5 strategy document (5 pillars, week-by-week plan) |
| `docs/v5-implementation-plan.md` | 16 tasks across 4 phases |

---

## Validation

All changes are additive to existing CLAUDE.md — no existing triggers removed, no frameworks deleted. The system degrades gracefully if skill files are missing (READ will fail silently and Claude falls back to general knowledge).

The GitHub Action uses a try/except structure with conservative deduplication — it will not spam issues on repeated runs.

---

*Generated: 2026-03-23*
*Session: SoloOS v5 optimization*
