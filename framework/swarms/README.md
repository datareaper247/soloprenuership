# Agent Swarm Orchestration

## What is an Agent Swarm?

An agent swarm is a coordinated network of AI agents, each with specialized roles, working in parallel or sequence to accomplish complex business tasks that would take a human team days or weeks.

## Swarm Architectures

### 1. Sequential Pipeline
```
Input → Research Agent → Strategy Agent → Execution Agent → Output
```
Best for: Deep work requiring progressive refinement (market analysis → strategy → plan)

### 2. Parallel Fan-Out
```
         ┌→ Research Agent 1 (Market) ─┐
Input →  ├→ Research Agent 2 (Competitors) ─┤ → Synthesis Agent → Output
         └→ Research Agent 3 (Trends) ──┘
```
Best for: Multi-dimensional research tasks

### 3. Hierarchical (Manager + Workers)
```
CEO Agent
├── CTO Agent → Build Workers
├── CMO Agent → Content Workers
└── CFO Agent → Analysis Workers
```
Best for: Full business function coordination

### 4. Debate/Adversarial
```
Proposal Agent → Critic Agent → Defender Agent → Arbiter Agent → Decision
```
Best for: Strategic decisions, architecture choices, pricing

## Core Swarms

### Research Swarm
**Purpose**: Complete market intelligence in hours, not weeks
**Agents**: Market Scanner + Competitor Analyst + Trend Spotter + Customer Synthesizer
**Output**: Market Brief, Opportunity Score, Competitor Map

### Strategy Swarm
**Purpose**: Generate and stress-test business strategies
**Agents**: CEO Agent + Devil's Advocate + Market Expert + Financial Modeler
**Output**: Strategy Document, Risk Assessment, Decision Matrix

### Build Swarm
**Purpose**: Ship product features at 10x speed
**Agents**: Product Manager + Architect + Developer + QA + Documenter
**Output**: Shipped features, tests, documentation

### Content Swarm
**Purpose**: Content marketing machine
**Agents**: Strategy Agent + Writer + Editor + SEO Optimizer + Publisher
**Output**: Blog posts, social content, email sequences, documentation

### Growth Swarm
**Purpose**: Systematic revenue growth
**Agents**: Acquisition Agent + Activation Optimizer + Retention Analyst + Revenue Modeler
**Output**: Growth experiments, A/B tests, funnel analysis

## Swarm Configuration Format

```yaml
# swarm-config.yaml
name: market-research-swarm
version: 1.0

agents:
  - id: market-scanner
    role: "Market opportunity discovery"
    model: claude-opus-4-6
    tools: [web_search, reddit, hackernews]

  - id: competitor-analyst
    role: "Competitive intelligence"
    model: claude-sonnet-4-6
    tools: [web_search, jina]

  - id: synthesizer
    role: "Insight synthesis and scoring"
    model: claude-opus-4-6
    depends_on: [market-scanner, competitor-analyst]

orchestration:
  type: parallel_then_sequential
  timeout: 3600
  output_format: markdown
```

## Running a Swarm

```bash
# Run market research swarm
claude --swarm framework/swarms/market-research-swarm.yaml \
  --input "Target market: pharmacy PBM audit software" \
  --output research/pharmacy-pbm-2026.md

# Run strategy swarm
claude --swarm framework/swarms/strategy-swarm.yaml \
  --input research/pharmacy-pbm-2026.md \
  --output strategy/pharmacy-pbm-strategy.md
```
