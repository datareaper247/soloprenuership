# SoloOS Core MCP Server

**Founder intelligence as callable tools. Not prompts — actual structured data.**

## What this is

A working Python MCP server that transforms the SoloOS knowledge base (PATTERN_LIBRARY.md,
FOUNDER_INTELLIGENCE.md, MARKET_INTELLIGENCE.md) into live tools Claude can call with real
structured responses.

## Install

```bash
pip install -e .
```

## Add to Claude Code

```bash
claude mcp add soloos-core -- python -m soloos_core.server
```

Or with the installed entrypoint:
```bash
claude mcp add soloos-core -- soloos-mcp
```

## Tools

| Tool | Description |
|------|-------------|
| `match_pattern` | Find matching decision patterns from PATTERN_LIBRARY |
| `search_founder_cases` | Find real founder evidence for recommendations |
| `check_market` | Market saturation and unit economics lookup |
| `calculate_ev` | Expected Value per hour calculator (optional Monte Carlo) |
| `log_decision` | Append to founder-log.md with kill signal tracking |
| `check_kill_signals_tool` | Check overdue outcomes — fires at session start |
| `get_stage_advice` | Stage-calibrated advice based on MRR |
| `session_synthesis` | Generate session wrap + auto-log decisions |
| `get_business_context` | Read business-context.md |
| `validate_idea_gates` | Run Gate 0-4 validation on an idea |
| `knowledge_base_stats` | Verify connection to knowledge base |
