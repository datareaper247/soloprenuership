# GrowthBook Self-Hosted Setup Guide

Time required: under 30 minutes
Result: A/B testing dashboard at http://localhost:3100 + SoloOS connected to it.

---

## Prerequisites

- Docker and Docker Compose installed
- SoloOS V10 installed (`soloos-mcp` command available)
- Optional: `pip install 'soloos-core[ab-testing]'` for the Python SDK

---

## Step 1 — Start GrowthBook with Docker Compose

From the SoloOS core directory:

```bash
cd /path/to/mcp/soloos-core

docker compose -f docker/growthbook-compose.yml up -d
```

This starts:
- MongoDB 6 (internal, not exposed to host)
- GrowthBook on port 3100

Wait about 15 seconds for GrowthBook to finish its startup checks:

```bash
docker compose -f docker/growthbook-compose.yml ps
# STATUS should show "healthy" for both services
```

---

## Step 2 — Create Your Account

1. Open http://localhost:3100 in your browser
2. Click "Create your account"
3. Fill in your name, email, and password
4. You are now the admin — no further users can sign up by default

---

## Step 3 — Create a Project and Get Your API Keys

1. In the GrowthBook UI, click **Settings** (gear icon, bottom left)
2. Click **API Keys** in the left sidebar
3. Click **Add API Key**
4. Select key type: **SDK Connection**
5. Give it a name: `soloos-core`
6. Click **Create**
7. Copy the **Client Key** — it looks like `sdk-abc123xyz`

You will use this in the next step.

---

## Step 4 — Configure SoloOS to Connect

Add these two environment variables wherever you run SoloOS MCP (shell profile, `.env` file, or Claude Code environment):

```bash
export GROWTHBOOK_API_HOST="http://localhost:3100"
export GROWTHBOOK_CLIENT_KEY="sdk-abc123xyz"   # ← replace with your key
```

For Claude Code / Cursor / Windsurf (add to your shell profile or MCP config):

```json
{
  "mcpServers": {
    "soloos-core": {
      "command": "soloos-mcp",
      "env": {
        "GROWTHBOOK_API_HOST": "http://localhost:3100",
        "GROWTHBOOK_CLIENT_KEY": "sdk-abc123xyz"
      }
    }
  }
}
```

---

## Step 5 — Verify the Connection

Run the verification command:

```bash
python -c "
from soloos_core.data.growthbook_client import get_growthbook_client
c = get_growthbook_client()
print('Configured:', c.is_configured())
exps = c.list_experiments()
print('Experiments:', len(exps))
"
```

Or use the MCP tool from Claude:

```
Use tool: list_experiments
```

---

## You Know It's Working When...

- `create_ab_experiment` returns an `experiment_id` and a `dashboard_url` pointing to `http://localhost:3100/experiments/...`
- `list_experiments` returns a JSON array (empty is fine — means no experiments yet)
- The GrowthBook dashboard at http://localhost:3100 shows the experiment you created

---

## Creating Your First Experiment

```
Use tool: create_ab_experiment
  name: "Pricing Page CTA Test"
  hypothesis: "Changing CTA from 'Start Trial' to 'Start Free' increases signups by 15%"
  metric: "signup_conversion"
  variants: ["control", "free_cta"]
```

The tool returns:
- `experiment_id` — save this for checking results
- `setup_instructions` — Python SDK snippet for your app
- `kill_signal_template` — pre-filled 30-day kill signal

---

## Checking Results

```
Use tool: get_experiment_results
  experiment_id: "exp_pricing_page_cta_test"
```

Returns statistical analysis: conversion rates per variant, p-value, and a plain-language recommendation (ship / run longer / inconclusive).

---

## Stop and Restart

```bash
# Stop (data preserved)
docker compose -f docker/growthbook-compose.yml down

# Start again
docker compose -f docker/growthbook-compose.yml up -d

# Wipe all data
docker compose -f docker/growthbook-compose.yml down -v
```

---

## Custom JWT Secret (Production)

Before using in production, set a strong secret:

```bash
export GROWTHBOOK_JWT_SECRET="your-long-random-secret-here"
docker compose -f docker/growthbook-compose.yml up -d
```

Or edit `docker/growthbook-compose.yml` directly — replace `soloos-dev-secret-change-in-prod` in the `JWT_SECRET` env var.

---

## Troubleshooting

**Port 3100 already in use**:
```bash
lsof -i :3100  # find what's using it
# Or change port in growthbook-compose.yml: "3101:3100"
```

**"Connection refused" from Python**:
```bash
curl http://localhost:3100/api/v1/healthcheck
# Should return {"status": "healthy"}
```

**MongoDB not ready (GrowthBook fails to start)**:
```bash
docker compose -f docker/growthbook-compose.yml logs mongo
# Wait for: "Waiting for connections" message
```
