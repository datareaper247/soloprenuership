# Research Engine

## Purpose

Systematic market intelligence gathering using AI agent swarms. Replace a 10-person research team with a coordinated set of AI agents that run continuously.

## Research Types

### 1. Market Discovery Research
**When**: Phase 0 (Discover)
**Purpose**: Find new opportunities
**Sources**: Reddit, HN, Product Hunt, G2, App Store reviews
**Output**: Pain point catalog + opportunity scores

### 2. Competitive Intelligence
**When**: Continuous (weekly monitoring)
**Purpose**: Track competitors, find gaps
**Sources**: Competitor websites, pricing pages, job postings, PR, reviews
**Output**: Competitor brief + positioning gaps

### 3. Customer Research Synthesis
**When**: Phase 1 (Validate) and continuous
**Purpose**: Extract patterns from customer interviews
**Sources**: Interview notes, support tickets, NPS surveys
**Output**: Customer insight brief + product implications

### 4. Technology Research
**When**: Phase 2 (Build) and continuous
**Purpose**: Keep up with AI/tech landscape
**Sources**: HN, GitHub trending, research papers, benchmarks
**Output**: Technology assessment + adoption recommendations

## Research Swarm Configuration

```yaml
# research-swarm.yaml
name: market-discovery-swarm
version: 1.0

input:
  type: topic
  value: "[TARGET MARKET OR PROBLEM SPACE]"

agents:
  reddit-miner:
    role: "Mine Reddit for pain points and discussions"
    tools: [reddit_search, reddit_get_subreddit_posts]
    prompt: |
      Search Reddit for discussions about [TOPIC].
      Find: complaints, workarounds, "I wish there was...", frustrations.
      Return: top 20 pain points with subreddit, upvotes, and quote.

  hn-analyst:
    role: "Analyze HackerNews for signals"
    tools: [hn_search, hn_get_stories]
    prompt: |
      Search HackerNews for [TOPIC].
      Find: Ask HN complaints, Show HN launches in this space, comments showing frustration.
      Return: key threads, notable comments, launch sentiment.

  competitor-mapper:
    role: "Map the competitive landscape"
    tools: [web_search, jina_reader]
    prompt: |
      Find all software products that solve [PROBLEM].
      For each: product name, pricing, key features, target customer, funding status.
      Format: competitive matrix table.

  opportunity-scorer:
    role: "Score and rank opportunities"
    depends_on: [reddit-miner, hn-analyst, competitor-mapper]
    model: claude-opus-4-6
    prompt: |
      Based on the research from all agents, score the opportunity on:
      - Problem severity (1-10)
      - Market size (1-10)
      - Competition gap (1-10)
      - Willingness to pay (1-10)
      - Solo buildability (1-10)
      Return: scores + rationale + top recommendation.

orchestration:
  phase1_parallel: [reddit-miner, hn-analyst, competitor-mapper]
  phase2_sequential: [opportunity-scorer]
  output: research/[topic]-opportunity-analysis.md
```

## Research Templates

### Pain Point Template
```markdown
## Pain Point: [Title]

**Source**: Reddit r/[subreddit] | [upvotes] upvotes
**Quote**: "[Direct quote from the source]"
**Problem**: [Synthesized problem statement]
**Current solution**: [What they currently do]
**Frustration level**: High/Medium/Low
**Frequency**: Daily/Weekly/Monthly

**Market signal**: [Why this is interesting]
```

### Competitor Profile Template
```markdown
## [Competitor Name]

**Website**: [URL]
**Founded**: [Year]
**Funding**: [Amount/Stage or Bootstrapped]
**Target customer**: [ICP description]

**Pricing**:
- [Tier 1]: $[X]/month — [what's included]
- [Tier 2]: $[X]/month — [what's included]
- [Tier 3]: Custom

**Key features**:
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Strengths**: [What they do well]
**Weaknesses**: [What they do poorly]
**Customer complaints** (from reviews):
- "[Quote from negative review]"
- "[Quote from negative review]"

**Positioning gap**: [Where they leave customers underserved]
```

### Opportunity Analysis Template
```markdown
# [Market/Problem] Opportunity Analysis
**Date**: [Date]
**Analyst**: Research Swarm v1.0

## TL;DR
[2-sentence summary: Is this worth pursuing?]

## Opportunity Score: [X.X/10]

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Problem Severity | [X]/10 | [Why] |
| Market Size | [X]/10 | [Why] |
| Competition Gap | [X]/10 | [Why] |
| Willingness to Pay | [X]/10 | [Why] |
| Solo Buildability | [X]/10 | [Why] |

## Pain Points Found
[Top 5-10 pain points from research]

## Competitive Landscape
[Competitor matrix table]

## Target Customer Profile
[ICP based on research]

## Pricing Opportunity
[Pricing gap analysis]

## Recommended Next Step
[Go/No-Go with specific action]
```

## Running Research

### Quick market scan (30 minutes)
```bash
# Deploy research swarm for a topic
# Outputs to: research/[slug]-analysis.md
```

### Deep dive (2-4 hours)
```bash
# Add customer interview synthesis
# Add financial market sizing
# Add regulatory landscape review
```

### Continuous monitoring (automated)
```bash
# Weekly competitor tracking
# Daily pain point monitoring in target subreddits
# Monthly market landscape refresh
```
