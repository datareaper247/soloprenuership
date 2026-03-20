# Proven Patterns Library

Recurring patterns that work for solo founders building with AI. Each pattern is validated by real outcomes.

---

## Business Model Patterns

### Pattern: Vertical SaaS Wedge
**What**: Enter a horizontal market through a specific vertical niche
**Why it works**: Less competition, clearer ICP, higher willingness to pay, sticky compliance/workflow lock-in
**Example**: Don't build "AI documentation tool" → build "AI documentation for veterinary practices"
**When to use**: When horizontal market is crowded but verticals are underserved
**Exit multiple**: 7-9.5x ARR (vs 4-6x for horizontal)

### Pattern: Workflow Automation Tax
**What**: Charge a percentage of the time/money saved (value-based pricing)
**Why it works**: Aligns your revenue with customer success, makes ROI obvious
**Example**: "We charge $X/month. Our users save 10 hours/week. If your time is worth $50/hr, that's $2,000/month saved."
**When to use**: When your product has measurable, quantifiable value

### Pattern: Services → Software
**What**: Start with manual services delivery, systematize, then productize
**Why it works**: Deep customer understanding before building, immediate revenue, no technical risk
**Steps**: 1) Do it manually with AI 2) Document the process 3) Build tools to automate your manual work 4) Sell the tool
**When to use**: When you're unsure if people will pay, or what they need

### Pattern: API + Dashboard Combo
**What**: Sell the API to technical users and the dashboard to non-technical users
**Why it works**: 2x addressable market from single codebase, technical users become advocates
**When to use**: When your core value is data processing or AI

---

## Growth Patterns

### Pattern: SEO Compound Machine
**What**: Publish 2+ SEO articles per week consistently for 12+ months
**Why it works**: Content compounds (a post from month 3 still gets traffic in month 36), very low CAC long-term
**Requirements**: Patience (6 month lag), consistent execution, high-quality content
**Result**: At 100+ posts, organic can drive 30-50% of signups for minimal marginal cost

### Pattern: Competitor Review Mining
**What**: Monitor competitor 1-3 star reviews on G2/Capterra for product gaps
**Why it works**: Customers tell you exactly what they want, but tell your competitor
**Tool**: Set up alerts for new reviews on top 3 competitors
**Action**: The most common complaints = your product differentiation

### Pattern: Community-Led Growth
**What**: Become a genuinely helpful member of communities where your customers gather
**Why it works**: Trust-based distribution is highest-quality (low churn, high NPS)
**Phases**:
  - Month 1-2: Lurk + learn
  - Month 2-4: Answer questions (no promotion)
  - Month 4+: Mention product only when perfectly relevant
**Mistakes to avoid**: Spamming, self-promotion too early, inconsistency

### Pattern: Integration Partnership Flywheel
**What**: Build integrations into tools your customers already use, get listed in their marketplace
**Why it works**: Warm distribution, borrowed trust, no acquisition cost
**Best integrations**: Zapier, Slack, Chrome Extension, Gmail, CRMs

---

## Product Patterns

### Pattern: One Core Loop
**What**: Design your entire product around ONE core value action
**Why it works**: Reduces complexity, makes onboarding simple, focuses engineering
**Test**: If a user can do ONE thing and get value, what is that thing?
**Anti-pattern**: Feature sprawl trying to serve all use cases

### Pattern: Progressive Disclosure
**What**: Show only what's needed for the current step; hide advanced features
**Why it works**: Reduces cognitive load, improves activation, reduces support tickets
**Implementation**: Default to simple. Advanced settings behind toggle. Power features behind upgrade.

### Pattern: Time-to-Value Speedrun
**What**: Obsessively optimize time from signup to first value experience
**Target**: <5 minutes to "aha moment"
**Measure**: Track each step in onboarding funnel with PostHog
**Priority**: The fastest and most common drop-off point is always your #1 fix

---

## AI Agent Patterns

### Pattern: Swarm then Synthesize
**What**: Run multiple specialized agents in parallel, then use a synthesis agent to combine outputs
**Why it works**: Each specialist agent goes deeper; synthesis removes contradictions and extracts key insights
**Use when**: Complex research requiring multiple dimensions

### Pattern: Critic Agent
**What**: After any output from a generative agent, route through a critic agent before using the output
**Why it works**: Reduces hallucinations, improves quality, catches errors
**Implementation**: Critic prompt: "You are a rigorous critic. Find flaws, errors, missing considerations, and overconfident claims in this output."

### Pattern: Human in the Loop for High Stakes
**What**: For any irreversible or high-stakes decision, always require human review before execution
**Why it works**: AI agents excel at generating options; humans excel at choosing between them in context
**Irreversible actions**: Send email, post publicly, commit code, delete data, make payment

### Pattern: Memory-Augmented Agents
**What**: Every agent reads from and writes to a shared knowledge base
**Why it works**: Agents compound knowledge over time; avoid repeating the same research
**Implementation**: Before researching X, check if X is already in knowledge base. After completing task, save key learnings.

---

## Solo Founder Operations Patterns

### Pattern: Monday Clarity Ritual
**What**: Every Monday morning, write 3 things: #1 priority, biggest bottleneck, this week's learning goal
**Why it works**: Prevents reactive work; ensures strategic progress even in hectic weeks
**Time required**: 15 minutes

### Pattern: No Decision Before Data
**What**: Before making any product decision, gather at least 3 customer data points
**Why it works**: Gut feel is wrong 60% of the time; 3 data points prevent costly mistakes
**Data sources**: Support tickets, user interviews, session recordings, NPS comments

### Pattern: Kill Meetings
**What**: Replace all meetings with async updates (Loom, written briefs, Notion)
**Why it works**: Meetings are expensive for solo founders; async is faster for all parties
**Exception**: Customer calls (keep these — they're research, not meetings)
