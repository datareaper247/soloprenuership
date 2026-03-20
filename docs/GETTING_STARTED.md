# Getting Started with SoloOS

## What Is This?

SoloOS is not software you install. It's a framework you deploy — a system of playbooks, agent configurations, decision frameworks, and knowledge bases that, together, multiply what a single founder can do.

Think of it as hiring a team that never sleeps:
- **Researcher** — runs market analysis while you sleep
- **Strategist** — stress-tests your decisions before you make them
- **Builder** — generates code, content, and copy in parallel
- **Analyst** — tracks metrics and flags anomalies
- **Operator** — runs daily processes on autopilot

You are the CEO. Everything else can be augmented with AI.

---

## The 3 Ways to Use SoloOS

### Option A: Framework Only (Start Here)

Use the playbooks, agent system prompts, and templates directly in Claude, ChatGPT, or any AI interface. No setup required.

**Start with**:
1. Identify your current phase → `playbooks/[0-4]-[phase]/README.md`
2. Deploy the relevant agent system prompts → `agents/[role]/system-prompt.md`
3. Use the templates → `knowledge-base/templates/README.md`

### Option B: Claude Code Integration

With Claude Code, you can run agent swarms from your terminal. The `framework/swarms/` directory contains swarm configurations you can reference.

### Option C: Build Your Own SoloOS Dashboard

Use the architecture blueprint in `docs/ARCHITECTURE.md` as the spec for a custom TypeScript application. The full directory structure and TypeScript interfaces are documented.

---

## Day 1 Checklist

### Step 1: Know Your Phase (5 minutes)

Answer honestly:
- [ ] Do I have a validated idea? → No → Start at Phase 0 (Discover)
- [ ] Am I validating with real customers? → Phase 1 (Validate)
- [ ] Am I actively building? → Phase 2 (Build)
- [ ] Am I growing revenue? → Phase 3 (Scale)
- [ ] Am I preparing an exit? → Phase 4 (Exit)

### Step 2: Deploy Your First Agent (10 minutes)

Open the system prompt for your most-needed function:
- Need to research a market? → `agents/research/` (coming soon) or use `framework/research/README.md`
- Need a strategic decision? → `agents/ceo/system-prompt.md`
- Need a technical decision? → `agents/cto/system-prompt.md`
- Need a financial model? → `agents/cfo/system-prompt.md`
- Need content? → `agents/cmo/system-prompt.md`
- Need a process documented? → `agents/coo/system-prompt.md`

Copy the system prompt → paste into Claude → start with your question.

### Step 3: Set Up Your Daily OS (15 minutes)

Open `tools/daily-os/README.md` and implement the morning brief ritual. 15 minutes each morning, AI-powered.

### Step 4: Start Building Your Knowledge Base (Ongoing)

Every time an agent produces a useful output:
- Save it to the appropriate directory
- Tag it with: date, phase, type, confidence level

This is your compound advantage. Start on Day 1.

---

## Which Agent to Use for What

| Question | Agent | File |
|----------|-------|------|
| "What should I focus on this week?" | CEO Agent | `agents/ceo/system-prompt.md` |
| "Is this the right tech stack?" | CTO Agent | `agents/cto/system-prompt.md` |
| "How should I price this?" | CFO Agent | `agents/cfo/system-prompt.md` |
| "Write my launch email" | CMO Agent | `agents/cmo/system-prompt.md` |
| "Document this process" | COO Agent | `agents/coo/system-prompt.md` |
| "Research this market" | Research Engine | `framework/research/README.md` |
| "Score this opportunity" | Strategy Engine | `framework/strategy/README.md` |
| "Build this feature" | Build Swarm | `framework/execution/README.md` |
| "Grow my revenue" | Growth Swarm | `playbooks/3-scale/README.md` |

---

## The Daily Rhythm

**Morning (15 min)**:
1. Run CEO Agent morning brief (5 min)
2. Review and approve today's agent task queue (5 min)
3. Set priority decision for the day (5 min)

**During day (async)**:
- Agent swarms run on approved tasks
- Review outputs as they arrive (batched, not real-time)
- Max 3 decisions surfaced to you at any time (3-Agent Rule)

**Evening (30 min)**:
1. Review day's agent outputs — approve, modify, or reject (15 min)
2. Update knowledge base with key learnings (10 min)
3. Queue tomorrow's tasks for agents (5 min)

**Weekly (Friday, 1 hour)**:
1. Metrics review (15 min)
2. Strategy alignment (15 min)
3. Knowledge base update (15 min)
4. Next week planning (15 min)

---

## The 3-Agent Rule (Mandatory)

Based on BCG research (March 2026): managing more than 3 active AI agent streams simultaneously causes cognitive collapse.

**Always limit yourself to**: 3 active decisions pending your review at any time.

If you have more than 3 things needing your judgment:
1. Prioritize the 3 most impactful
2. Let agents hold the rest until you clear the queue
3. Trust quality gates to prevent bad outputs from queuing

This feels slow at first. It is faster in practice.

---

## Common Mistakes (Avoid These)

### ❌ Mistake 1: Human-in-the-Loop Thinking
**Don't**: Set up agents to ask permission at every step
**Do**: Define objectives + quality criteria once → review final output

### ❌ Mistake 2: Ignoring Quality Gates
**Don't**: Accept the first agent output without review
**Do**: Run the 3-gate protocol on every output (mechanical → quality → alignment)

### ❌ Mistake 3: Forgetting Compound Learning
**Don't**: Let agent insights evaporate after each session
**Do**: Save every insight, decision, and outcome to the knowledge base

### ❌ Mistake 4: Running Agents Sequentially on One Approach
**Don't**: Ask one agent for one answer
**Do**: Run 3-5 parallel agents, measure quality, select winner

### ❌ Mistake 5: Skipping the Morning Brief
**Don't**: Start work without knowing your 1 priority
**Do**: 15-minute morning brief → focused execution → compounding results

---

## What Success Looks Like

After 30 days:
- Daily OS running with 15-minute morning brief
- 1-3 agent swarms running regularly
- Knowledge base accumulating with real patterns
- Time to first draft of any content: < 30 min
- Time to market research brief: < 2 hours

After 90 days:
- Agents know your customers, your voice, your patterns
- Research cycles: 90 minutes (was: 1 week)
- Content production: 2 posts/week (was: 0.5)
- Strategic decisions: 30 min with full analysis (was: 3 hours with uncertainty)

After 12 months:
- Compound advantage visible: agents optimized for your specific business
- Knowledge base is a moat competitors can't easily replicate
- Operating at the functional equivalent of a 5-10 person team
- Founder time spent entirely on judgment calls, not execution

---

## Next Steps

1. **Identify your phase** → Read the relevant playbook
2. **Deploy one agent** → CEO or CFO if unsure where to start
3. **Set up Daily OS** → `tools/daily-os/README.md`
4. **Start your knowledge base** → Even one insight saved is the start of compounding

Welcome to the AI era of solo entrepreneurship.
