# Langfuse Self-Hosted Setup Guide

Time required: under 30 minutes
Result: LLM observability dashboard at http://localhost:3000 + SoloOS tool call traces visible there.

---

## What This Gives You

Once configured, every SoloOS tool call (council_brief, validate_idea_gates, etc.) is automatically
traced in Langfuse. You can:
- See latency, input, and output for every tool call
- Submit human feedback via `rate_recommendation` to track response quality over time
- Filter by tool name, date range, or score to find consistently bad recommendations

---

## Prerequisites

- Docker and Docker Compose installed
- SoloOS V10 installed
- Optional: `pip install 'soloos-core[observability]'` for the Langfuse Python SDK

---

## Step 1 — Start Langfuse with Docker Compose

From the SoloOS core directory:

```bash
cd /path/to/mcp/soloos-core

docker compose -f docker/langfuse-compose.yml up -d
```

This starts:
- PostgreSQL 15 (internal, not exposed to host)
- Langfuse server on port 3000

Wait about 20 seconds for migrations to complete:

```bash
docker compose -f docker/langfuse-compose.yml ps
# STATUS should show "healthy" for langfuse-server
```

---

## Step 2 — Create Your Account

1. Open http://localhost:3000 in your browser
2. Click **Sign up**
3. Fill in your email and password
4. You are now the admin

Note: After your first user, sign-up is disabled by default for security.
To invite teammates: Settings > Members > Invite.

---

## Step 3 — Create a Project and Get API Keys

1. On the Langfuse home screen, click **Create New Project**
2. Name it: `soloos-core`
3. Click **Create**
4. Go to **Settings** (gear icon in the sidebar)
5. Click **API Keys** in the left panel
6. Click **Create new API keys**
7. Copy both:
   - **Public Key** — looks like `pk-lf-abc123xyz`
   - **Secret Key** — looks like `sk-lf-abc123xyz`

Keep the secret key somewhere safe — it won't be shown again.

---

## Step 4 — Configure SoloOS to Connect

Add these environment variables to your shell profile or MCP server config:

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-abc123xyz"   # ← replace
export LANGFUSE_SECRET_KEY="sk-lf-abc123xyz"   # ← replace
export LANGFUSE_HOST="http://localhost:3000"
```

For Claude Code / Cursor / Windsurf MCP config:

```json
{
  "mcpServers": {
    "soloos-core": {
      "command": "soloos-mcp",
      "env": {
        "LANGFUSE_PUBLIC_KEY": "pk-lf-abc123xyz",
        "LANGFUSE_SECRET_KEY": "sk-lf-abc123xyz",
        "LANGFUSE_HOST": "http://localhost:3000"
      }
    }
  }
}
```

Restart your MCP client (Claude Code / Cursor) after updating env vars.

---

## Step 5 — Verify the Connection

Make one tool call in Claude (e.g. `run_morning_brief`), then:

1. Open http://localhost:3000
2. Click on your `soloos-core` project
3. Click **Traces** in the left sidebar

You should see a trace entry for the tool call you just made.

---

## You Know It's Working When...

- Traces appear in the Langfuse dashboard within a few seconds of a tool call
- Each trace shows: tool name, duration, success/failure status
- `rate_recommendation` returns `"stored": true` after you submit a rating

---

## Submitting Feedback

After any tool call you want to rate, use the `rate_recommendation` tool:

```
Use tool: rate_recommendation
  call_id: "a3f7bc12"    ← from the tool_calls.jsonl log or Langfuse trace ID
  score: 4
  reason: "Council was balanced but missed the distribution angle"
```

Scores: 1 = very unhelpful, 2 = poor, 3 = neutral, 4 = good, 5 = excellent

Finding the call_id:
```bash
tail -20 ~/.soloos/logs/tool_calls.jsonl | python3 -m json.tool
# Each line has a "call_id" field
```

---

## Viewing Quality Trends

In Langfuse:
1. Click **Scores** in the left sidebar
2. Filter by `human_feedback` score name
3. Sort by date to see quality trend over time

---

## Stop and Restart

```bash
# Stop (data preserved)
docker compose -f docker/langfuse-compose.yml down

# Start again
docker compose -f docker/langfuse-compose.yml up -d

# Wipe all data
docker compose -f docker/langfuse-compose.yml down -v
```

---

## Custom Secrets (Production)

Before using in production, set strong secrets:

```bash
export LANGFUSE_NEXTAUTH_SECRET="your-long-random-string-1"
export LANGFUSE_SALT="your-long-random-string-2"
docker compose -f docker/langfuse-compose.yml up -d
```

Or edit `docker/langfuse-compose.yml` and replace the `soloos-dev-*` placeholder values.

---

## Using Langfuse Cloud (Alternative)

If you prefer not to self-host, Langfuse offers a free cloud tier:
1. Sign up at https://cloud.langfuse.com
2. Create a project and copy your API keys
3. Set the same env vars — just omit `LANGFUSE_HOST` (it defaults to cloud)

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-abc123xyz"
export LANGFUSE_SECRET_KEY="sk-lf-abc123xyz"
# No LANGFUSE_HOST needed — defaults to https://cloud.langfuse.com
```

---

## Troubleshooting

**Port 3000 already in use** (common if you run other Node apps):
```bash
lsof -i :3000  # find what's using it
# Or change port in langfuse-compose.yml: "3001:3000"
# Then set: LANGFUSE_HOST=http://localhost:3001
```

**"Unauthorized" errors in traces**:
- Double-check that `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` match the project
- Keys are project-scoped — ensure you copied from the right project

**Traces not appearing**:
```bash
# Check if the langfuse package is installed
python -c "import langfuse; print(langfuse.__version__)"
# Install if missing:
pip install 'soloos-core[observability]'
```

**Database migration not complete**:
```bash
docker compose -f docker/langfuse-compose.yml logs langfuse-server | grep -i migrat
# Wait for: "Database migration complete"
```
