# Execution Engine

## The Agentic Swarm Patterns for Solo Founder Execution

Based on real-world implementations: TTal (356 PRs/33 days), Cook CLI (composable agent loops), Karpathy Autoresearch (910 experiments/8 hours).

---

## Core Execution Patterns

### Pattern 1: The Cook Composable Loop

The most transferable pattern from the coding world to all business execution:

```
Outcome + Quality Criteria + Parallelism = Autonomous Execution

Syntax:
  [Agent] "[Task description]" v[N] [quality-gate] "[selection criteria]"

Examples:
  # 3 parallel cold email drafts, pick highest conversion likelihood
  [CMO] "Write cold email for solo SaaS founders pain: time tracking" v3 review "highest conversion likelihood"

  # 5 parallel pricing model scenarios, pick best LTV:CAC
  [CFO] "Model pricing for $49/$149/$499 tiers given churn data" v5 "maximize LTV:CAC at <3% churn"

  # 10 parallel title options for SEO post
  [SEO] "Create title for keyword 'best pharmacy audit software'" v10 "most click-worthy with exact keyword match"

  # 4 landing page copy variants, test with real users
  [CMO] "Write landing page hero section for pharmacy audit SaaS" v4 "highest signup CVR signal"
```

**Why this works**: The human specifies the OUTCOME and CRITERIA, not the steps. Agents execute, quality gate filters, winner is surfaced for final human review or automatic promotion.

### Pattern 2: The Manager-Worker Hierarchy (TTal Architecture)

For complex, multi-step execution projects:

```
Manager Layer (Long-running, persistent):
  Researcher Agent: gathers context, maintains project understanding
  Planner Agent: breaks tasks into worker-ready subtasks

Worker Layer (Short-lived, disposable):
  Worker 1 → isolated context → completes task → outputs to shared store → terminates
  Worker 2 → isolated context → completes task → outputs to shared store → terminates
  Worker N → ...

Review Layer (Quality gate):
  Review Agent 1-6 → evaluates outputs before human review
  Only passing outputs surface to human

Human (Mobile):
  Receives: PR-ready outputs, summary of what was done
  Acts: Approve / Modify / Reject (5 min, not 5 hours)
```

**Key principle**: Workers are disposable. Context lives in the Manager layer and shared knowledge base. Each worker gets ONLY the context it needs for its specific task (reduces hallucination, reduces cost).

### Pattern 3: The Parallel Factorial Grid (Autoresearch Pattern)

For any problem where you have multiple dimensions to test:

```
Dimension A: [a1, a2, a3]
Dimension B: [b1, b2, b3]
Dimension C: [c1, c2]

Sequential approach: test a1b1c1 → best → test a1b1c2 → ... (linear search)
Parallel approach: test ALL 18 combinations simultaneously → pick global winner

Why parallelism finds better answers:
  Sequential: finds local optima (hill-climbing)
  Parallel: finds global optima (factorial search reveals interactions)

Applied to business:
  Email campaign: [subject lines x3] × [CTAs x3] × [target segments x3] = 27 variants
  Run all 27 with small send (500 each) → auto-promote winner to full list
```

### Pattern 4: The Outcome-Loop Closure

**What's missing in every current AI framework** (per March 2026 research): no system connects agent actions to business outcomes.

Every execution task must define:
```yaml
task: "Write 5 SEO blog posts targeting pharmacy audit"
quality_gate: "Published and indexed within 14 days"
outcome_metric: "Organic signups from these posts in 30 days"
outcome_target: "≥5 signups per post"
rollback_trigger: "0 signups after 30 days → remove from sitemap, repurpose"
attribution_window: "30 days"
```

The Execution Engine closes the loop:
1. Task assigned to agent swarm
2. Agent completes and passes quality gate
3. Output deployed/published
4. Outcome metric tracked for attribution_window
5. Result fed back to knowledge base ("SEO posts about pharmacy audit convert at X%")
6. Future tasks get this context automatically

---

## Execution Swarm Configurations

### Build Swarm (For Product Development)

```yaml
name: build-swarm
purpose: Ship product features at 10x speed

agents:
  product_manager:
    role: "Break feature into minimal implementation"
    model: claude-opus-4-6
    prompt: "You are a ruthless MVP product manager. Return MINIMUM viable implementation as task list."

  architect:
    role: "Define technical approach"
    model: claude-sonnet-4-6
    depends_on: product_manager

  code_generator:
    role: "Write production code"
    model: claude-opus-4-6
    parallel_count: 3  # 3 parallel implementations
    depends_on: architect

  review_agents:
    role: "Review each implementation"
    model: claude-sonnet-4-6
    count: 2  # Per code generator output
    checks: [security, correctness, performance, style]

  selector:
    role: "Pick best implementation"
    model: claude-opus-4-6
    depends_on: [code_generator, review_agents]
    selection_criteria: "cleanest, most secure, most maintainable"

  test_writer:
    role: "Write comprehensive tests"
    model: claude-sonnet-4-6
    depends_on: selector
    coverage_target: 0.80

output:
  files: [implementation, tests, documentation]
  human_review: final_implementation_only
  estimated_time: "30-90 minutes"
```

### Content Swarm (For Content Marketing)

```yaml
name: content-swarm
purpose: Produce SEO content at 10x speed

weekly_output_from_2_hours_human_input:
  - 2 long-form blog posts (2000+ words, SEO optimized)
  - 5 social posts (LinkedIn/Twitter)
  - 1 email newsletter
  - 2 short-form repurposing pieces
  - 3 community answer drafts

agents:
  keyword_researcher:
    role: "Find target keyword + 5 semantic variants"
    tools: [semrush, ahrefs, google_trends]

  outline_writer:
    role: "Create SEO-optimized structure"
    model: claude-sonnet-4-6
    depends_on: keyword_researcher

  content_writers:
    role: "Write each section"
    count: 3  # Parallel section writers
    model: claude-sonnet-4-6
    depends_on: outline_writer

  editor:
    role: "Edit for voice, flow, accuracy"
    model: claude-opus-4-6
    depends_on: content_writers

  seo_optimizer:
    role: "Optimize title, meta, internal links, keyword density"
    model: claude-sonnet-4-6
    depends_on: editor

  repurposer:
    role: "Create social variants from final post"
    model: claude-haiku-4-5
    depends_on: seo_optimizer

human_checkpoints:
  - Approve keyword + title (5 min)
  - Final review before publish (15 min)
```

### Research Swarm (For Market Intelligence)

```yaml
name: research-swarm
purpose: Complete market intelligence in hours, not weeks

agents:
  reddit_miner:
    role: "Extract pain points from relevant subreddits"
    tools: [reddit_api]
    output: "top 20 pain points with upvotes and quotes"

  hn_analyst:
    role: "Extract signals from HackerNews"
    tools: [hn_api]
    output: "Ask HN threads, Show HN launches, notable comments"

  competitor_mapper:
    role: "Map competitive landscape"
    tools: [web_search, jina]
    output: "competitor matrix with pricing + features"

  market_sizer:
    role: "Estimate TAM/SAM/SOM"
    tools: [perplexity, web_search]
    output: "market size estimates with sources"

  synthesizer:
    role: "Combine all research into opportunity score"
    model: claude-opus-4-6
    depends_on: [reddit_miner, hn_analyst, competitor_mapper, market_sizer]
    output: "opportunity score + recommendation + next steps"

parallelism:
  phase_1: [reddit_miner, hn_analyst, competitor_mapper, market_sizer]
  phase_2: [synthesizer]
  total_time: "30-90 minutes"
```

### Growth Swarm (For Revenue Growth)

```yaml
name: growth-swarm
purpose: Systematic, data-driven revenue growth

weekly_cadence:
  monday:
    agents: [analytics_agent]
    task: "Review last week metrics, flag anomalies, propose 3 experiments"
    output: "Weekly metrics brief + experiment proposals"

  tuesday:
    agents: [content_agent, community_agent]
    tasks:
      - "Publish 1 SEO blog post"
      - "Prepare 3 community answers"
    output: "Published content"

  wednesday:
    agents: [outreach_agent]
    task: "Send 10 personalized cold outreaches from last week's research"
    output: "10 sent outreaches"

  thursday:
    agents: [experiment_agent]
    task: "Launch this week's approved growth experiment"
    output: "Running experiment with tracking"

  friday:
    agents: [retention_agent, analytics_agent]
    tasks:
      - "Review churn signals, flag at-risk accounts"
      - "Week in review summary"
    output: "At-risk list + week summary for human review"

human_time_required: "45 minutes per week"
```

---

## The Verification Protocol

Addresses the "AI coding is gambling" problem documented in HN research.

Every agent output passes through 3 gates before human review:

### Gate 1: Mechanical Correctness
```
Code: tests pass, types check, no linter errors
Content: grammar, links work, word count met
Research: sources cited, no hallucinated statistics
Financial: formulas verified, no circular references
```

### Gate 2: Quality Threshold
```
Code: review agent scores ≥ 7/10 on security + correctness
Content: reading level appropriate, keyword density 1-2%, CTA present
Research: confidence score ≥ 0.7, sources from last 12 months
Financial: numbers reconcile, assumptions stated
```

### Gate 3: Business Alignment
```
"Does this output advance the stated business objective?"
Objective defined at task creation
Misalignment triggers automatic revision loop (max 2 iterations)
Then escalates to human if still misaligned
```

**If all 3 gates pass**: Human gets polished, ready-to-use output (5-15 min review)
**If any gate fails**: Automatic revision loop, not human interruption

---

## Execution Metrics

Track per swarm, per week:

```
Build Swarm:
  - Features shipped: ___
  - Test coverage: ___%
  - Bugs in production: ___
  - Avg feature time: ___ hours

Content Swarm:
  - Posts published: ___
  - Avg keyword ranking: ___
  - Organic sessions from content: ___
  - Content → Trial CVR: ___%

Research Swarm:
  - Opportunities scored: ___
  - Validated hypotheses: ___
  - Competitive updates: ___

Growth Swarm:
  - Experiments run: ___
  - Win rate: ___%
  - MRR attributed to growth work: $___
  - CAC this week: $___
```
