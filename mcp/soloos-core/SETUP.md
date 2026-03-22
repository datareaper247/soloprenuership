# SoloOS Core — Setup Guide

## One-Command Install

```bash
pip install -e /path/to/soloprenuership/mcp/soloos-core
claude mcp add soloos-core -- soloos-mcp
```

## What You Get

### MCP Server (Claude Code)

Claude can now call 18 tools instead of reading markdown:

| Tool | Example Claude usage |
|------|---------------------|
| `match_pattern` | "Find patterns for: should I add a free tier?" |
| `search_founder_cases` | "Find cases where founders raised prices" |
| `check_market` | "Is AI resume builder saturated?" |
| `calculate_ev` | "Which has higher EV: cold DMs or SEO content?" |
| `log_decision` | "Log: decided to build concierge version first" |
| `check_kill_signals_tool` | Session-start kill signal review |
| `get_stage_advice` | "What should I focus on at $3K MRR?" |
| `session_synthesis` | End-of-session decision logging |
| `get_business_context` | Read business-context.md |
| `validate_idea_gates` | "Validate: AI invoice reconciliation for accountants" |
| `knowledge_base_stats` | Verify connection |
| `calculate_unit_economics` | "My ARPU is $99, churn is 3%, CAC is $300 — what's my LTV:CAC?" |
| `calculate_valuation` | "My ARR is $120K, growing 80% YoY — what's the company worth?" |
| `score_pmf` | "Sean Ellis 45%, NRR 108%, D30 retention 38% — do I have PMF?" |
| `generate_competitor_brief` | "Generate autopsy template for Notion competitor" |
| `calculate_runway` | "I have $50K cash, $8K burn, $4K MRR — true runway?" |
| `monitor_competitor` | "Weekly intel brief on Linear with signal classification + MCP research commands" |
| `enrich_prospect` | "90-second prospect brief for Acme Corp + 3 outreach variants" |

### CLI Tool

```bash
# Pattern matching
soloos pattern "should I add a free tier"

# Expected Value calculator (interactive or args)
soloos ev

# Market intelligence
soloos market "AI resume builder"

# Stage advice
soloos stage '$3K' "how do I grow"

# Idea validation
soloos validate "AI invoice reconciliation for accountants" --heard 1

# Kill signal check
soloos signals

# KB stats
soloos stats

# Unit economics (ARPU, churn, optional CAC)
soloos uniteconomics 99 0.03 --cac 300 --gm 80

# Company valuation (ARR, YoY growth, optional NRR and SDE)
soloos valuation 120000 80 --nrr 105 --sde 40000

# PMF score (any combination of metrics)
soloos pmf --ellis 45 --nrr 108 --l30 38 --churn 2.1 --customers 55

# Runway projection (accounts for MRR growth + churn)
soloos runway 50000 8000 --mrr 4000 --new-mrr 1000

# Competitor autopsy template
soloos competitor "Notion" --pricing "freemium + $8/mo" --icp "teams"

# Weekly competitive intelligence brief with signal classification
soloos monitor "Linear" --url "https://linear.app" --mrr '$20K' --category "project management"

# 90-second prospect research brief + 3 outreach variants
soloos prospect "Acme Corp" --contact "Jane Smith" --role "Head of Ops" --mrr '$5K' --product "automates invoice reconciliation"
```

## What's Different

**Before SoloOS Core MCP**:
- Claude reads PATTERN_LIBRARY.md (static markdown)
- No structured search, just text reference
- Kill signals are text strings in a file, not tracked
- EV is a template, not live math

**After SoloOS Core MCP**:
- Claude calls `match_pattern("should I add a free tier")` → gets P05, P08, P20 with real evidence
- Kill signals are date-tracked objects with urgency ratings
- EV/hr is calculated with optional Monte Carlo simulation
- Market saturation is instantly queryable across 79 categories
- Session decisions are auto-logged to founder-log.md as FL-XXX entries
