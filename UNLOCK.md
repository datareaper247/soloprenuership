# The SoloOS Unlock

> How SoloOS does for company operations what OpenClaw/ClawdBot did for coding — unlocking new agentic behavior patterns in any AI model.

---

## What OpenClaw/ClawdBot Did

OpenClaw and ClawdBot extended Claude Code's core capabilities by:
1. **Persistent skills** — reusable prompt patterns any session can invoke
2. **Behavioral rules** — shaping how Claude approaches problems by default
3. **Meta-commands** — new capabilities beyond the base system
4. **Memory layer** — making Claude "remember" across sessions

The result: Claude Code became dramatically more powerful for coding workflows.

---

## What SoloOS Does

SoloOS applies the same principle at the **company operations** level.

When any agent CLI connects to SoloOS, it gains:

1. **40+ professional role skills** — any agent can now think and act as a CMO, CFO, SEO specialist, sales rep, legal counsel, etc.
2. **MCP servers for every business function** — real tools connecting to real services
3. **Multi-agent swarm protocols** — agents coordinate like a real company org chart
4. **Business memory** — agents share context, decisions, and knowledge across all sessions
5. **Open source integrations** — connected to 50+ tools through Composio, n8n, and direct APIs

The result: Any agent becomes a fully-staffed virtual company.

---

## The Architecture of the Unlock

```
WITHOUT SOLOOOS:
┌─────────────────────────────────────┐
│  Claude Code / Cursor / Any Agent   │
│  Capabilities: coding + reasoning   │
│  Context: this conversation only    │
│  Tools: basic filesystem + terminal │
└─────────────────────────────────────┘

WITH SOLOOOS:
┌─────────────────────────────────────────────────────────────────┐
│  ANY Agent CLI                                                  │
├─────────────────────────────────────────────────────────────────┤
│  SoloOS Skills Layer                                            │
│  /role cmo → CMO system prompt + marketing tools               │
│  /role seo → SEO specialist + keyword research tools           │
│  /role sales → SDR + CRM integrations + outreach tools         │
│  ... (40+ roles)                                               │
├─────────────────────────────────────────────────────────────────┤
│  SoloOS MCP Servers                                             │
│  soloos-research   → market intel, competitor analysis         │
│  soloos-marketing  → SEO, content, email, social               │
│  soloos-sales      → CRM, outreach, pipeline                   │
│  soloos-product    → PRDs, roadmaps, user research             │
│  soloos-engineering → code review, arch, security              │
│  soloos-ops        → finance, legal, HR, compliance            │
│  soloos-growth     → experiments, analytics, conversion        │
│  soloos-geo        → international markets, localization       │
│  soloos-swarm      → multi-agent orchestration                 │
│  soloos-memory     → persistent business context               │
├─────────────────────────────────────────────────────────────────┤
│  Tool Integration Layer (via Composio + n8n + direct APIs)     │
│  150+ business tools: Salesforce, HubSpot, Stripe, Ahrefs,    │
│  Google Analytics, LinkedIn, Mailchimp, Notion, Linear, ...    │
├─────────────────────────────────────────────────────────────────┤
│  Open Source Foundations                                        │
│  MetaGPT (role SOPs) + CrewAI (orchestration) +               │
│  Composio (integrations) + Mem0 (memory) + E2B (execution)    │
└─────────────────────────────────────────────────────────────────┘
```

---

## New Agentic Behaviors Unlocked

### Behavior 1: Instant Role Switching

```bash
# Any agent now has 40+ professional roles available
/role cmo "Create a 90-day content strategy targeting enterprise devs"
/role seo "Find 50 low-competition keywords for our DevOps tool"
/role sdr "Draft cold outreach sequence for VP Engineering prospects"
/role cfo "Model three pricing scenarios and recommend optimal tier structure"
/role legal "Review this SaaS agreement for red flags"
/role localization "Evaluate Japan market entry for B2B SaaS"
```

### Behavior 2: Multi-Agent Company Simulation

```bash
# Launch a full company team on any problem
/swarm product-launch "Launch our new API product next month"

# SoloOS orchestrates:
# → CMO Agent: develops launch strategy
# → SEO Agent: researches keywords, drafts blog posts
# → SDR Agent: builds prospect list, drafts outreach
# → DevRel Agent: drafts API docs, examples
# → Social Agent: creates content calendar
# → PR Agent: drafts press release
# Human reviews consolidated plan (30 min)
```

### Behavior 3: Real Business Tool Integration

```bash
# Agents now have hands — they can USE business tools
/task "Update CRM with notes from today's customer calls"
# → Reads call transcripts → updates HubSpot records → flags at-risk accounts

/task "Monitor competitors and alert on pricing changes"
# → Checks Ahrefs weekly → screenshots pricing pages → flags changes → notifies

/task "Publish this week's SEO content"
# → Optimizes post → schedules in Buffer → creates social snippets → emails list
```

### Behavior 4: Cross-Session Business Memory

```bash
# Agents remember your business across ALL sessions
/recall customers
# → Returns: ICP, top 10 customers, common pain points, language they use

/recall experiments
# → Returns: all A/B tests run, what worked, what didn't, current running

/recall decisions
# → Returns: strategic decisions log with rationale and outcomes
```

### Behavior 5: Agentic Company Autopilot

```bash
# Set weekly autonomous operations
/autopilot research "Monitor top 5 competitors, send weekly brief"
/autopilot growth "Run 1 growth experiment per week, report results"
/autopilot content "Publish 2 SEO posts/week from approved calendar"
/autopilot retention "Flag churning customers, draft win-back outreach"
```

---

## Why This Is Different From Existing Tools

| Tool | What It Does | SoloOS Advantage |
|------|-------------|-----------------|
| MetaGPT | Software company roles (coding-focused) | ALL business functions, not just coding |
| CrewAI | Multi-agent orchestration framework | Business-ready roles + tool integrations |
| AutoGPT | Autonomous task execution | Business context memory + professional SOPs |
| LangChain | Agent + tool framework | Ready-to-deploy, no-code skills for existing CLIs |
| Composio | Tool integrations (150+) | Integrated into role-specific workflows |
| Dify | LLMOps platform | Skills format for any existing CLI agent |

**The SoloOS difference**: It's not a new agent framework. It's a **skills/MCP layer** that makes your EXISTING agent CLI (whatever you're already using) capable of operating as a full company.

You don't switch tools. You extend your current tool.

---

## Integration Guide by Agent CLI

### Claude Code
```bash
# Add all SoloOS MCPs to your Claude Code config
claude mcp add soloos-research -- npx -y @soloos/mcp-research@latest
claude mcp add soloos-marketing -- npx -y @soloos/mcp-marketing@latest
claude mcp add soloos-sales -- npx -y @soloos/mcp-sales@latest
claude mcp add soloos-ops -- npx -y @soloos/mcp-ops@latest
claude mcp add soloos-growth -- npx -y @soloos/mcp-growth@latest
claude mcp add soloos-swarm -- npx -y @soloos/mcp-swarm@latest
claude mcp add soloos-memory -- npx -y @soloos/mcp-memory@latest

# Add SoloOS skills
cp -r soloprenuership/skills/claude-code/* ~/.claude/commands/
```

### Cursor
```json
// .cursor/mcp.json
{
  "mcpServers": {
    "soloos-marketing": { "command": "npx", "args": ["-y", "@soloos/mcp-marketing"] },
    "soloos-research": { "command": "npx", "args": ["-y", "@soloos/mcp-research"] },
    "soloos-sales": { "command": "npx", "args": ["-y", "@soloos/mcp-sales"] }
  }
}
```

### Any MCP-Compatible Agent
```json
// Standard MCP configuration
{
  "mcpServers": {
    "soloos": {
      "command": "npx",
      "args": ["-y", "@soloos/mcp-all"],
      "env": {
        "SOLOOS_API_KEY": "your-key",
        "COMPOSIO_API_KEY": "optional-for-integrations"
      }
    }
  }
}
```

### Skills Format (Any Agent)
```markdown
<!-- Copy any role system prompt into your agent's system/context -->
<!-- From: soloprenuership/roles/[function]/[role]/system-prompt.md -->
<!-- Immediately gives your agent that professional role's capabilities -->
```

---

## The Compound Moat

Each week SoloOS is running, your competitive advantage grows:

- **Week 1**: Generic agent outputs with professional framing
- **Month 1**: Agents know your industry, customers, competitors
- **Month 3**: Agents know YOUR voice, proven patterns, what works for your ICP
- **Month 6**: Agents have context competitors can't replicate — accumulated decisions, experiments, customer language
- **Month 12**: You have a proprietary AI company OS, fine-tuned to your business

No competitor can fast-follow this. The moat is the accumulated memory.

---

## What Gets Unlocked at Each Stage

```
Stage 1 (Skills Only):
✓ 40+ professional roles available instantly
✓ Any agent becomes multi-functional
✓ No setup, no API keys, just system prompts
Cost: Free

Stage 2 (+ MCP Servers):
✓ Real tool integrations (Ahrefs, HubSpot, Stripe, etc.)
✓ Agents can READ from and WRITE to business tools
✓ Cross-session memory
Cost: Tool API costs only

Stage 3 (+ Swarm Orchestration):
✓ Multi-agent coordination
✓ Parallel execution of company-wide tasks
✓ Automated weekly operations
Cost: API costs + hosting for orchestration server

Stage 4 (+ Business Autopilot):
✓ Autonomous weekly company operations
✓ Competitive monitoring, content publishing, growth experiments
✓ Human reviews outcomes, not steps
Cost: ~$200-500/month in API costs for full operation
```
