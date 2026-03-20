# Solo Founder Playbooks — Validated Behavioral Patterns

5 documented approaches from the most successful indie makers. Not theory — observable behavior
patterns extracted from their writing, interviews, and documented build histories.

**How to use this file**: Each playbook is encoded as a set of concrete AI behaviors.
When these patterns are active (via CLAUDE.md), Claude applies them automatically —
no need to describe the approach every session.

---

## Playbook 1: The Arvid Kahl Pattern
**"Embedded Entrepreneur"** — Audience before product

### What Kahl Actually Did (Documented)
- Spent 6+ months inside teacher Facebook groups before building FeedbackPanda
- Never mentioned a product idea until he had the community's trust
- Listened for language — used teachers' own words in every landing page headline
- Built a first paying customer list of 20 teachers before writing code
- By launch: zero cold outreach needed, audience was warm

### The Core Behavioral Unlock
**The sequence matters more than the idea**.
Most founders: find idea → build → find audience.
Kahl's sequence: find audience → listen deeply → audience surfaces the idea.

The product was almost incidental. The community relationship was the defensible asset.

### Encoded as AI Behaviors

**Auto-trigger**: When a founder says "I have an idea for [X]", flag this:
```
⚠️ ORIGIN CHECK (Kahl Rule)
Did you hear this specific problem from 3+ community members in their own words?
If no: spend 2 hours in [relevant community] listening before validating this idea.
The Kahl pattern starts with the community, not the idea.
```

**The listening protocol**: Run `/listen` for 4 weeks before running `/validate`.
Collect 10+ pain quotes in their exact words. Use those words in your copy.

**The engagement ladder** (must complete before selling):
1. Comment helpfully (week 1-2)
2. Share a useful resource (week 3)
3. Ask for a 15-min interview (week 4)
4. Mention you're building something (week 5)
5. Test positioning (week 6)
6. Invite to founding beta (week 7+)

### Warning Signal (Flag These)
- Founder invented idea without community input → flag Kahl Rule
- Founder uses their own language in copy, not customer language → flag: "Use their words"
- Founder wants to market before 5 customer interviews → flag: "Kahl pattern: listen first"

---

## Playbook 2: The Marc Lou Pattern
**"Every launch is a content machine"** — Product + story of building product

### What Marc Lou Actually Does (Documented)
- Ships 2-3 products per month
- Each product generates: 1 HN post + 1 tweet thread + 1 PH launch + email to list
- Treats failure publicly: "I shut down [X] after [N] weeks because [honest reason]"
- Compounds: each launch grows the audience for the next launch
- Revenue from the portfolio, not from one product

### The Core Behavioral Unlock
**You're building two products simultaneously**: the thing itself, and the story of building it.
The audience compounds across launches. By launch 10, the audience does most of the distribution.

Marc Lou quote: "I don't market products. I market the act of building products."

### Encoded as AI Behaviors

**After every `/validate` → BUILD decision**, auto-trigger `/launch` planning:
```
You're about to build. Per the Marc Lou pattern:
Before writing code, generate your launch assets with /launch.
This ensures the story of building is captured from day 1.
```

**The content hooks to capture during build**:
- Day 1: "Started building [X] today because [honest personal reason]"
- Day 3: "Hit first wall: [specific technical or product challenge]"
- Day 7: "First ugly version: [screenshot]"
- Day 14: "What I cut to ship faster: [specific features dropped]"
- Launch: Full `/launch` output
- Day 2 post-launch: "48 hours in: [honest numbers]"
- Day 14 post-launch: "2 weeks in: [what I got wrong]"

**The failure value principle**:
A product that fails publicly is worth more to the audience than a product that never launched.
"I shut this down after [N] weeks" is content. "I'm still building" is not.

### Warning Signal (Flag These)
- Founder is building without a launch plan → flag: "Marc Lou pattern: generate launch assets now"
- Founder wants to wait until "it's ready" to share → flag: "Build in public from day 1"
- Founder treating failure as embarrassing → flag: "Failed launch is content — share the learnings"

---

## Playbook 3: The Pieter Levels Pattern
**"Constraints as competitive advantage"** — No code (or minimal code), max speed

### What Levels Actually Does (Documented)
- Launched 12 startups in 12 months (2014 — foundational "make" era experiment)
- Nomad List: started as a spreadsheet, then a public Google Sheet, then simple PHP
- No frameworks — single HTML file + vanilla JS at launch for many products
- Speed principle: "If I can't validate it in 2 weeks, I shouldn't build it"
- Revenue first: doesn't scale until $500/month sustained

### The Core Behavioral Unlock
**Constraints eliminate the premature optimization death spiral.**
With no fancy framework, no backend, no team — you're forced to validate first.
The constraint IS the strategy.

### Encoded as AI Behaviors

**The Levels MVP Test**: Before building any feature, apply this filter:
```
LEVELS TEST:
Can this be a spreadsheet? → Make it a spreadsheet first.
Can this be a form + email? → Start there.
Can this be done manually for the first 10 customers? → Do it manually.
Code is the optimization, not the starting point.
```

**Speed calibration** (auto-apply when scope creeps):
- MVP that ships in 2 weeks > MVP that ships in 8 weeks
- 80% product in 2 weeks beats 100% product in 8 weeks
- The question is never "is it ready?" — it's "is it good enough to learn from?"

**Revenue threshold** (flag premature scaling):
- Below $500 MRR: single product, single customer segment, no team
- $500-$2K MRR: now you can optimize
- $2K-$5K MRR: now you can scale marketing
- Above $5K MRR: now you can consider team

### Warning Signal (Flag These)
- Founder adding "nice to have" features before launch → flag: "Levels test: is this in the MVP?"
- Founder building instead of validating → flag: "Levels rule: validate in 2 weeks or kill it"
- Founder optimizing before $500 MRR → flag: "Too early — get to $500 MRR first"

---

## Playbook 4: The Justin Jackson Pattern
**"Stair-stepping"** — Start small, self-sustaining, then step up

### What Jackson Documented (In His Own Writing)
- 2014: Started with small info products ($29-$99 ebooks, courses)
- Each small product built the audience for the next
- MegaMaker (community) funded from small product revenue
- Transistor FM (SaaS, now $1M+ ARR) built on top of an established audience
- Never raised funding — each step funded the next

### The Core Behavioral Unlock
**The stair-step model removes "must succeed immediately" pressure** which causes:
- Building before validating (no time to validate)
- Underpricing (afraid to lose customers)
- Adding features indiscriminately (afraid to lose anyone)
- Burning out (all-in on one bet)

Jackson's sequence: small product → audience → larger product → repeat.

### Encoded as AI Behaviors

**The stair-step revenue gate** (apply when founder discusses next move):
```
STAIR-STEP CHECK:
Current MRR: [X]
Target MRR: [Y]

Is this next step self-sustaining before moving to the step after it?
If no: the step is too big. Find the smaller version that validates first.
```

**The smallest viable bet** (auto-apply to feature/product proposals):
- Is there an info product version? (ebook, template, course)
- Is there a service version? (consulting, done-for-you, freelance)
- Is there a tool version? (simple utility, Chrome extension, script)
- Only after those: is there a SaaS version?

**Audience as compound asset**: Every customer is potentially:
1. A buyer of the next product
2. A source of future product ideas
3. A distributor (word of mouth)
4. A case study that attracts more customers

Never optimize for the transaction. Optimize for the relationship.

### Warning Signal (Flag These)
- Founder going straight to SaaS for first product → flag: "Stair-step: consider smaller first step"
- Founder ignoring existing small audience to chase bigger one → flag: "Jackson rule: your current audience is the asset"
- Founder spending revenue instead of reinvesting in next step → flag: "Stair-step: fund the next step first"

---

## Playbook 5: The Tyler Tringas Pattern
**"Micro-SaaS"** — Narrow focus, defensible niche, boring but profitable

### What Tringas Documented (Coined the Term)
- Coined "Micro-SaaS" in 2013 with Storemapper
- Built Storemapper as a single-feature tool: "show your stores on a map"
- Never tried to expand into a full commerce suite
- Profitable, maintainable alone, sold for multiple six figures
- The defensibility came from the narrow focus, not the product complexity

### The Core Behavioral Unlock
**Profitable narrow beats unprofitable broad.**
Most founders ask: "How do I get more customers?"
Tringas asks: "Which customers will I defend?"

The narrow focus creates natural moats:
- Deep integration with specific tools (Shopify, Salesforce, etc.)
- Community trust in the specific niche
- Vocabulary that matches exactly what the niche searches for
- Word of mouth within the niche (small worlds talk)

### Encoded as AI Behaviors

**The Micro-SaaS Validation Test** (apply to any product idea):
```
MICRO-SAAS TEST:
1. Can you describe the customer in one sentence? (specific, not a persona)
2. Can you name 10 specific people who need this today?
3. Is there an existing tool they pay for that does this badly?
4. Can this be built and maintained by one person?
5. Will narrow focus create defensibility in 12 months?

If yes to all 5: strong Micro-SaaS candidate.
If no to #1 or #2: too broad. Narrow it.
```

**The niche depth principle** (auto-apply to positioning):
- "For [specific software] users" beats "for businesses"
- "For [specific workflow] teams" beats "for teams"
- The narrower the positioning, the stronger the word-of-mouth in the niche

**Anti-expansion discipline** (flag premature broadening):
- Below $5K MRR: do not expand the ICP
- Below $10K MRR: do not add a second core use case
- The temptation to expand is the #1 killer of Micro-SaaS profitability

### Warning Signal (Flag These)
- Founder wants to serve multiple ICPs before PMF → flag: "Tringas rule: one ICP until $5K MRR"
- Founder building features for one-off requests vs. core ICP → flag: "Narrow focus protects defensibility"
- Founder under-pricing narrow solution → flag: "Narrow solutions command premium pricing"

---

## Pattern Cross-Reference: Which to Apply When

| Stage | Primary Pattern | Supporting Patterns |
|-------|----------------|-------------------|
| Pre-idea | Kahl (listen first) | — |
| Idea → Validate | Kahl + Tringas (narrow + community) | Jackson (start small) |
| Validate → Build | Levels (constraints + speed) | Tringas (narrow MVP) |
| Build → Launch | Marc Lou (build in public) | — |
| Launch → $500 MRR | Tringas (defend the niche) | Levels (no scaling yet) |
| $500 → $5K MRR | Jackson (stair-step planning) | Marc Lou (compound launches) |
| $5K MRR+ | All five apply in combination | — |

---

## The Meta-Pattern Across All Five

Different playbooks, same underlying principles:

1. **Validation before building** (Kahl, Levels, Tringas)
2. **Narrow focus creates compounding advantages** (Tringas, Kahl)
3. **Constraints force creativity and speed** (Levels, Jackson)
4. **Every action should build the next action** (Marc Lou, Jackson)
5. **Audience is worth more than the product** (Kahl, Marc Lou)

The divergence is strategic emphasis:
- **Kahl**: Audience as the unfair advantage
- **Marc Lou**: Consistency of shipping as the unfair advantage
- **Levels**: Speed and constraints as the unfair advantage
- **Jackson**: Small wins compounding as the unfair advantage
- **Tringas**: Niche depth as the unfair advantage

A founder doesn't need to pick one. The CLAUDE.md behavioral rules encode all five — Claude applies the right pattern based on what stage the founder is at and what decision they're facing.
