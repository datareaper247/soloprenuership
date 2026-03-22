# SoloOS Core — Setup Guide

## One-Command Install

```bash
pip install -e /path/to/soloprenuership/mcp/soloos-core
claude mcp add soloos-core -- soloos-mcp
```

## What You Get

### MCP Server (Claude Code)

Claude can now call 11 tools instead of reading markdown:

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
