# PATTERN LIBRARY: 50 Decision Patterns from Real Founders

> These are not frameworks. They are encoded decisions that real founders made at specific moments,
> with the outcomes documented. Apply the matching pattern to your situation.
>
> Format: SITUATION → PATTERN → REAL EXAMPLE → KILL SIGNAL

---

## CATEGORY A: PRODUCT DECISIONS

### P01 — The Levels Test
**Situation**: About to build a software feature or product
**Pattern**: "Can this be a spreadsheet, form, or manual process first?"
**Why**: Pieter Levels' 12 startups experiment proved: validate demand before writing code. His first Nomad List was a spreadsheet that went viral before any code.
**Apply when**: Estimating >2 weeks of build time
**Kill signal**: If you can't get 5 people interested in the manual version, don't build the automated version
**Reversibility**: 10/10 (testing = no commitment)

### P02 — The Marc Lou Kill Test
**Situation**: Evaluating whether to build a new product
**Pattern**: 4 gates before writing line 1 of code:
1. Can it be built in <2 weeks?
2. Does my existing audience need it?
3. Can the value be explained in 1 tweet?
4. Will I kill it in 4 weeks if no signal?
**Real example**: ShipFast — built in 1 week, explained in 1 tweet ("Next.js boilerplate saves 40+ hours"), sold to developer audience he already had.
**Kill signal**: No paid signups within 2 weeks of launch
**Reversibility**: 10/10 pre-build; 6/10 post-launch (sunk cost)

### P03 — The Danny Postma Formula
**Situation**: AI product ideation
**Pattern**: [New AI capability] + [Existing expensive painful professional workflow] = product
**Real examples**:
- LoRA fine-tuning + professional photography = HeadshotPro ($300K MRR peak)
- LLM + website documentation = SiteGPT ($15-40K MRR)
**Apply when**: A new AI capability becomes accessible (new model, new API)
**Kill signal**: Category has 5+ direct competitors with reviews → look for narrower niche
**Reversibility**: 8/10 (ideas are cheap)

### P04 — The Viral Output Requirement
**Situation**: Building a B2C AI product
**Pattern**: The output must be shareable. If users can't show someone else what it made, word-of-mouth won't work.
**Real examples**: HeadshotPro (users share their headshots on LinkedIn), PhotoAI (users post AI photos), Xnapper (polished screenshots shared on Twitter)
**Kill signal**: No organic sharing in first 30 days → product output is not shareable enough
**Reversibility**: 5/10 (baked into product design, hard to retrofit)

### P05 — The One-Time vs Subscription Decision
**Situation**: Choosing pricing model for new product
**Pattern**:
- One-time payment → use for clear one-job products with discrete output (headshots, logo, template)
- Subscription → use for ongoing workflow integration (scheduling, analytics, automation)
**Numbers**: One-time conversion rate typically 3-8%; subscription 1-3% but 4-12 month LTV
**Real example**: Tony Dinh — DevUtils (one-time) + BlackMagic.so (subscription) = portfolio balance
**Kill signal**: Subscription with <40% 3-month retention = wrong model, product isn't sticky enough

### P06 — The Compliance Moat Pattern
**Situation**: Choosing between compliance-adjacent and general tools
**Pattern**: Regulatory urgency → structural retention. Non-use has consequences (fines, contract loss).
**Numbers**: Compliance tools 80-90% 6-month retention vs 30-50% for productivity tools
**Apply when**: Target customer faces legal/financial penalty for not using correct documentation
**Kill signal**: If target customers have a manual workaround that costs less than $20/hour to maintain, won't convert

### P07 — The Narrow ICP Rule (Tringas Pattern)
**Situation**: Founding stage, defining target customer
**Pattern**: One ICP until $5K MRR. "Healthcare SMBs in the Southeast" beats "SMBs".
**Arvid Kahl's data**: FeedbackPanda TAM was 50-100K teachers. VC would reject it. Hit exit in 14 months.
**Test**: Can you find 20 of your target customers on LinkedIn in 30 minutes?
**Kill signal**: If you need LinkedIn Sales Navigator to find 20 → niche is too narrow; if you can't describe them in 10 words → too broad

---

## CATEGORY B: DISTRIBUTION & ACQUISITION

### P08 — The Distribution-First Rule
**Situation**: Any stage, any product
**Pattern**: Distribution > Product. Every founder who succeeded had: pre-built audience, compounding channel, or product whose output markets itself.
**Evidence**: Of 300 AI products analyzed: 100% of $50K+ MRR had distribution first. <10% of products without distribution reached $5K MRR.
**Apply**: Before writing code, answer: what's our day-1 distribution path?
**Kill signal**: No distribution identified → run landing page + 20 outreach DMs before building

### P09 — The Marc Lou Audience Prerequisite
**Situation**: Launching a new product
**Pattern**: "Sell to the audience you already have." ShipFast worked because Marc had 30K+ developer Twitter followers who already trusted him.
**Anti-pattern**: Building for an audience you don't have yet = distribution from scratch
**Kill signal**: If you can't list 100 specific people who would want this product by name/username → build audience first

### P10 — The Pieter Levels Distribution Flywheel
**Situation**: Pre-launch product
**Pattern**: HN launch → Twitter build-in-public → Programmatic SEO → Email list → cycle repeats
**Real numbers**: Nomad List HN launch → 10K users day 1. PhotoAI reached $60K+ MRR largely through programmatic SEO (2,000+ indexed pages targeting "[profession] AI headshot").
**Timing**: HN launch on Monday 9am EST; ProductHunt on Tuesday midnight PST
**Kill signal**: If HN post doesn't reach front page within 2 hours, boost outreach before HN decay

### P11 — The Community Distribution Pattern (Arvid/FeedbackPanda)
**Situation**: Targeting a specific professional community
**Pattern**: Authentic community membership first. Market from inside, not from outside.
**Key**: Danielle was a real VIPKid teacher. Her recommendation read as peer, not marketer. CAC = ~$0.
**Apply when**: Target customer has an active community (subreddit, Facebook group, Slack, Discord)
**Kill signal**: If your first 5 community posts get flagged as spam → not authentic enough, need more genuine participation first

### P12 — The Direct Outreach Gate (<$5K MRR)
**Situation**: Pre-PMF, need first 10 customers
**Pattern**: Direct outreach > all other channels at this stage. Lists are buyable. Pain is confirmable.
**Numbers**: Cold email to identified pain-sufferers converts at 0.5-3% to demo; 10-30% of demos to paid
**Process**: Find 100 names → personalized 3-line email → ask for 15-min call → sell on call
**Kill signal**: <2% demo rate from 100 emails → ICP wrong or message wrong; A/B test one variable

### P13 — The SEO Timing Rule
**Situation**: Founder asks about SEO strategy
**Auto-trigger**: Check MRR first.
**Pattern**:
- $0-5K MRR → DO NOT DO SEO. Direct outreach. Every hour on SEO is wasted.
- $5-20K MRR → Bottom-of-funnel only: competitor comparison pages, "[product] alternative" keywords
- $20K+ MRR → Full content strategy viable
**Evidence**: Pieter didn't invest in SEO until PhotoAI had $20K+ MRR and a clear product
**Kill signal at $5-20K**: If your "alternative to X" page doesn't rank top 10 within 90 days → technical SEO issue; fix before creating more content

### P14 — The Paid Acquisition Gate
**Situation**: Considering paid ads
**Pattern**: Paid ads only work when: LTV:CAC > 2.5x + visual product + recurring subscription + B2B-adjacent use case
**Evidence**: Eric Smith (AutoShorts.ai) — $97K MRR in 7 months via Meta ads. LTV $407, CAC $120-150.
**Anti-pattern**: Paid acquisition before knowing LTV = burning money
**Kill signal**: 2 weeks of ads, CAC > 3x expected LTV → stop, fix retention first

---

## CATEGORY C: PRICING DECISIONS

### P15 — The Marc Lou Price Ladder
**Situation**: Setting initial pricing
**Pattern**: Start at uncomfortable-high price point. Increase in 4 stages. Announce each increase.
**ShipFast data**: $99 → $149 → $199 → $299. Each increase announced, each worked.
**Why**: "Save 40+ hours" at $299 vs $100/hr developer = obvious ROI. Price anchored to cost of alternative.
**Kill signal**: If conversion rate at new price drops >50% from prior level → price ceiling found; return to prior

### P16 — The Annual Conversion Standard
**Situation**: Adding annual pricing option
**Pattern**: Offer annual at 20% discount from monthly × 12. Expect 20-35% of new paid users to choose annual.
**Numbers**: Annual users have 2-4x lower churn than monthly users.
**Kill signal**: If <10% choosing annual → annual discount not compelling; try 30-40% discount

### P17 — The B2B Price Floor
**Situation**: Pricing B2B SaaS targeting businesses
**Pattern**: Minimum $49/mo. Below $49/mo, support costs eat margin and buyers don't take you seriously.
**Evidence**: Every profitable B2B solo-founder product in research was ≥$49/mo.
**Kill signal**: If $49/mo gets consistent "too expensive" from actual target buyer → not B2B, actually consumer play

### P18 — The ACV-to-Sales-Motion Matrix
**Situation**: Designing sales process
**Pattern**:
| ACV | Sales Motion |
|-----|-------------|
| <$100/mo | Self-serve only; no calls |
| $100-500/mo | Founder-led async; email only |
| $500-2K/mo | Founder-led consultative; 30-min call |
| >$2K/mo | Enterprise; multi-stakeholder, contract |
**Kill signal**: If spending >1 hour per customer on deals <$500/mo → wrong sales motion, fix with self-serve

---

## CATEGORY D: VALIDATION

### P19 — The Pre-Sell Pattern (Gil Hildebrand)
**Situation**: About to build, want to validate first
**Pattern**:
1. Detailed landing page describing product
2. "Founding member" lifetime deal or deep discount
3. Threshold: "I'll build if I get X sign-ups by [date]"
4. Use revenue to fund development
**Evidence**: Subscribr ($30K MRR) — pre-sold 50 lifetime deals at $400 = $20K before writing code
**Kill signal**: <10 sign-ups in 14 days from targeted outreach to 100+ ideal prospects → don't build

### P20 — The 5-Commitment Rule
**Situation**: Validating an idea
**Pattern**: Get 5 people to commit to paying before building. Not "interested" — committed.
**Commitment tiers**:
1. "I'd be interested" — worthless
2. "I'd probably pay" — weak
3. "Add me to waitlist" — weak
4. "Here's my card, charge me when ready" — valid commitment
5. "I'm paying you now for early access" — strongest signal
**Kill signal**: Can't get 5 Tier-4 commitments in 4 weeks from targeted outreach → wrong ICP, wrong problem, or wrong price

### P21 — The Mom Test Application
**Situation**: Customer discovery calls
**Pattern**: Ask about past behavior, not future intent. "Tell me about the last time you [problem]" not "Would you pay for [solution]?"
**Key questions**:
1. How do you handle [problem] today?
2. How much time does it take?
3. Have you paid for any solution to this?
4. Why'd you stop using it?
**Kill signal**: If 7+ of 10 discovery calls describe a functional workaround they're happy with → problem not acute enough

---

## CATEGORY E: BUILDING THE MOAT

### P22 — The Three-Layer Moat Framework
**Situation**: Building any product
**Pattern**: Stack all three layers for defensibility:
- Layer 1 (Bottom): Recurring workflow retention mechanism
- Layer 2 (Middle): Proprietary element (data, training, integration)
- Layer 3 (Top): Day-1 distribution path
**Evidence**: Every $50K+ MRR product in research had all three. Products missing Layer 1 died to competition.
**Kill signal for Layer 1**: If D30 retention <40% → product not embedded in workflow → commoditized

### P23 — The Open Stats Flywheel (Pieter Levels)
**Situation**: Growth, need backlinks and press
**Pattern**: Publish revenue publicly. Journalists cover it. Other founders reference it. Trust builds.
**Evidence**: Nomad List open stats page (nomadlist.com/open) generated years of press + backlinks at $0 CAC
**Apply when**: Product has positive metrics worth showing. Don't do this in first 90 days.
**Kill signal**: If publishing metrics generates no inbound media/sharing in 30 days → metrics not interesting enough yet; need stronger numbers

### P24 — The Proprietary Data Moat
**Situation**: AI product in competitive category
**Pattern**: What proprietary data can you accumulate that competitors can't copy in 48 hours?
**Examples**:
- Subscribr: YouTube API data analysis → benchmarks not in native YouTube Studio
- FeedbackPanda: feedback templates that teachers actually used → better than competitors' generic templates
- Compliance tools: regulation parsing + form logic for specific state/federal schemas
**Build time**: 3-6 months to be genuinely hard to replicate
**Kill signal**: If a competitor replicates your proprietary data layer in <30 days → it wasn't actually proprietary

---

## CATEGORY F: OPERATIONAL PATTERNS

### P25 — The 30-Minute Support Rule
**Situation**: Scaling beyond $10K MRR
**Pattern**: <30 min/day on support at $10K MRR. Stack:
1. In-product tooltips (eliminates 30-40% of tickets)
2. Loom video library (eliminates 40-60%)
3. AI chat answering from docs (70-80% deflection)
4. Community where power users answer each other
5. Async email (48hr SLA)
**Kill signal**: If spending >2hrs/day on support at $10K MRR → self-service investment overdue

### P26 — The Weekly Operating Rhythm
**Situation**: $20K-$50K MRR solo operator
**Pattern** (from documented founder schedules):
- Monday: Support triage + product planning (2-3 hrs)
- Tue-Wed: Core development (6-8 hrs/day)
- Thursday: Marketing (3-4 hrs)
- Friday: Analytics + customer calls (2-3 hrs)
- Weekend: Off with 30-min async monitoring
**Total**: 30-35 hrs/week. Exceeding this = hiring time.
**Kill signal**: Consistently >40hrs/week for 3+ weeks → one area is consuming disproportionate time; identify and fix or hire

### P27 — The Multi-Product Portfolio Timing
**Situation**: When to add second product
**Pattern**: Tony Dinh's rule: 1 cash cow + 1 growth product + 1 experiment. Never all at once.
**Timing**: Add second product only when first product has documented support self-service + growth plateau
**Kill signal**: If first product requires >10hrs/week maintenance → not ready for second product

---

## CATEGORY G: STRATEGIC PIVOTS & EXITS

### P28 — The Exit Preparation Checklist
**Situation**: $50K+ ARR, considering exit
**Pattern** (Arvid Kahl — sold FeedbackPanda for est. $500K-$1M):
- Clean MRR metrics documented: revenue, churn, growth rate
- Low founder dependency: documented processes, not "tribal knowledge"
- Platform risk assessed: is customer base concentrated on one platform?
- Exit multiple expectation: 3-5x ARR for micro-SaaS <$1M ARR
**Platforms**: Acquire.com, MicroAcquire, Quiet Light, Flippa
**Kill signal**: If 70%+ of revenue from customers on one third-party platform → exit before platform regulatory risk

### P29 — The Pivot Signal Framework
**Situation**: Deciding whether to pivot or persist
**Pattern**: Pivot when 3+ of these are true:
1. 3+ months without PMF signal ($0 → $1K MRR)
2. Can't get 40% "very disappointed" on Sean Ellis survey
3. CAC > 3x LTV consistently
4. Monthly churn > 10% for 3+ consecutive months
5. D30 retention < 30%
**Don't pivot when**: Single metric is bad but others are strong

### P30 — The Platform Dependency Red Flag
**Situation**: Building on top of another platform's API
**Pattern**: If platform is core to your customer base existence, assess exit/survival risk quarterly.
**Evidence**: Arvid sold FeedbackPanda 14 months after launch; VIPKid collapsed 18 months later due to Chinese regulatory changes. Exit timing was fortunate but taught: concentration risk in platform-dependent businesses.
**Kill signal**: Platform changes ToS or faces regulatory action that could eliminate your customer base

---

## CATEGORY H: MINDSET & ANTI-PATTERNS

### P31 — The Build-in-Public Dual Product Rule (Marc Lou)
**Situation**: Shipping a new product
**Pattern**: "Before shipping, every ship is two products: the product itself and the launch content."
**Assets to generate before shipping**: HN post, tweet thread, Product Hunt copy, 50 warm DMs
**Kill signal**: If you have no Twitter/HN/community post planned before launch → you're missing 50-70% of launch distribution

### P32 — The Speed Test (Levels)
**Situation**: Starting any project
**Pattern**: "Can this version be done in a weekend?" If no → scope it down until yes.
**Evidence**: Pieter's best products (Nomad List, Remote OK, PhotoAI) all had working MVPs in <2 weeks
**Kill signal**: If MVP is >4 weeks of solo work → either scope down, use existing tools, or pre-validate before building

### P33 — The Founder Type Match
**Situation**: Choosing which archetype to model
**Pattern**: Match your constraint to the archetype:
- Have audience → Marc Lou or Arvid Kahl path (sell to existing followers)
- No audience, technical → Tony Dinh path (tool for developers/designers, build portfolio)
- No audience, designer/creative → Danny Postma path (AI + visual profession formula)
- Content-first preference → Arvid Kahl path (audience then product)
- Low tolerance for ambiguity → Tony Dinh path (solve your own pain, know the customer = yourself)

### P34 — The Jackson Stair-Step Rule
**Situation**: First product, no audience
**Pattern**: Don't start with recurring SaaS. Start with:
1. Info product ($29-99): teach what you know
2. Template/tool ($19-49): sell what you built
3. Community ($29-49/mo): aggregate audience
4. SaaS ($49-199/mo): sell to the audience you built
**Kill signal**: If jumping straight to SaaS with no audience → validate with step 1 or 2 first

### P35 — The 40% Test
**Situation**: Assessing product-market fit
**Pattern**: Survey active users: "How would you feel if you could no longer use [product]?"
- Very disappointed: target >40%
- Somewhat disappointed: note %
- Not disappointed: red flag if >30%
**Evidence**: Sean Ellis PMF threshold. Superhuman validated PMF this way.
**Kill signal**: <40% "very disappointed" after 3+ months of active users → not at PMF; don't scale acquisition yet

---

## CATEGORY I: AI-SPECIFIC PATTERNS

### P36 — The ChatGPT Substitution Test
**Situation**: Building any AI-powered feature
**Pattern**: "Can a user accomplish 80% of this with a free ChatGPT prompt?" If yes → you need workflow integration, not just AI.
**Evidence**: Top failure mode (25-30% of AI products): native LLM interfaces absorbed the use case
**Kill signal**: If your product's core value is "AI writes [content type]" without workflow embedding → test this by actually trying to do it in ChatGPT first

### P37 — The Compute Economics Check
**Situation**: Before pricing an AI product
**Pattern**: Cost out your compute per user at 3x average usage. If COGS > 30% of revenue at any tier → margin problem.
**Reference data**:
- Text (Claude Sonnet): $0.002-0.012/request
- Image (FLUX): $0.006-0.055/image
- Document processing: $0.01-0.05/doc
**Kill signal**: If 20% of users account for >60% of compute costs → need usage limits or tiered metering

### P38 — The Model Abstraction Requirement
**Situation**: Building on top of an AI API
**Pattern**: Abstract the underlying model. Your product is the workflow, not the model.
**Evidence**: Pieter Levels (PhotoAI) — used Replicate abstraction layer. Swapped models as better ones emerged. Products that hardcoded to one model got stuck when capabilities shifted.
**Kill signal**: If updating to a new base model requires >1 day of engineering work → abstraction layer needed

---

## QUICK REFERENCE: STAGE × PATTERN MAP

| Stage | Most Critical Patterns |
|-------|----------------------|
| $0 MRR | P01 P02 P08 P09 P18 P19 P20 P21 P33 P34 P36 P37 P38 |
| $1-5K MRR | P07 P10 P11 P12 P15 P22 P29 P35 P39 |
| $5-20K MRR | P13 P14 P16 P17 P23 P25 P27 P40 |
| $20-50K MRR | P24 P26 P28 P30 |
| $50K+ MRR | P28 P29 P30 P27 |

---

## CATEGORY F: VALIDATED-BY-SWARM PATTERNS (v3)

These patterns emerged from multi-model synthesis (Claude + Gemini parallel analysis) and gap analysis across 300+ founder cases. Research date: March 2026.

### P36 — The ChatGPT Substitution Test
**Situation**: About to build an AI-powered product
**Pattern**: Before ANY validation work, spend 5 minutes testing if ChatGPT/Claude free tier already solves the core problem.
**Why**: 25-30% of AI products launched 2023-2025 failed because native LLM interfaces absorbed their use case. This is now the #1 single-category failure mode for AI-first solo founders.
**Apply when**: Any AI product idea — before writing code or running full validation
**Pass criteria**: LLM cannot adequately solve the problem, or can only solve part of it (the gap = your product)
**Fail criteria**: LLM does it adequately → find a narrower niche or integration moat
**Kill signal**: If you can demonstrate the task to a customer using ChatGPT and they say "oh, that works" → you don't have a product
**Reversibility**: 10/10 (it's a 5-minute test)

### P37 — The Experiment-Driven Identity Shift
**Situation**: Founder experiencing discouragement, stagnation, or "it's not working"
**Pattern**: Reframe identity from "entrepreneur who needs customers" to "scientist who needs data." Failing experiments become successful invalidations.
**Why (psychological)**: The 45-day abandonment cliff is driven by learned helplessness — the founder loses belief that their actions affect outcomes. The "scientist" identity breaks this by making any outcome (including failure) a valid result.
**Apply when**: >30 days since project start with no paying customer; founder expressing discouragement
**The intervention**: Shift from launch goal ("get a customer") to learning goal ("determine whether assumption X is true")
**Evidence**: Scientific framing has been shown in behavioral research to improve persistence through failure because failure is reframed as information, not judgment
**Kill signal**: If the founder cannot articulate a specific hypothesis being tested (not a general goal), the experiment frame isn't working
**Reversibility**: 10/10 (mental model only)

### P38 — The Services-to-Software Flywheel
**Situation**: Looking for the highest-probability validation path, especially when you're the target customer
**Pattern**: (1) Solve your own problem manually → (2) Document the manual process → (3) Build tooling to automate → (4) Sell to others with the same problem.
**Why**: Eliminates market research. Pricing is validated (you paid in time). Product roadmap is your own pain points. Distribution starts with communities you're already in.
**Evidence**: Arjun Jain ($500K ARR), multiple Indie Hackers success stories 2025-2026. Pattern identified in >40% of successful solo founder cases where founder was target customer.
**Critical difference from typical advice**: Do NOT start by asking "what do others need?" Start by asking "what do *I* need, that I'm solving manually right now?"
**Apply when**: You're solving a problem you personally experience
**Kill signal**: If you can't document the manual process (step-by-step workflow) in under 2 hours, you don't understand the problem well enough yet
**Reversibility**: 10/10 (document first, software decision comes later)

### P39 — The Parallel Experiment Design
**Situation**: About to test one approach sequentially (A then B then C)
**Pattern**: Run N variants simultaneously. Sequential search finds local optima. Parallel search finds global optima.
**Evidence**: Karpathy/SkyPilot Autoresearch (March 2026) — 16 parallel experiments found a 2.87% better solution than sequential hill-climbing, at 9x the speed. The optimal strategy (screen on H100s → validate on H200s) was never in the instructions — it emerged from parallel interaction data.
**Business application**:
- Pricing: Test 3-5 price points with different segments simultaneously (not sequentially)
- Cold outreach: Test 5+ subject lines × 3 CTAs in parallel (not "let me try A first")
- Content: Publish 5 angles, measure, concentrate on winners
**Kill signal**: If testing one approach at a time and it "doesn't work," you've reached a local optimum. Pause, design parallel experiment.
**Reversibility**: 8/10

### P40 — Reference Class Forecasting (Anti-Planning Fallacy)
**Situation**: Making a time estimate for building, validating, or growing to a target
**Pattern**: Before committing to any timeline, find the reference class (similar projects/founders) and use their median outcome, not your optimistic estimate.
**Why**: The solo founder planning fallacy is amplified by: (1) no team to dampen optimism, (2) identity fusion with the plan (conservative estimates feel like inadequacy), (3) error compounding (one delay steals time from all other areas).
**Apply when**: Any commitment to a timeline, any resource allocation plan
**Execution**: "How long do you think this takes?" → Founder answers → "What do similar founders report for this exact task?" → Apply 2x multiplier to founder's estimate as starting point
**Kill signal**: If actual time exceeds estimate by >50%, apply 3x multiplier to all remaining estimates in the plan
**Reversibility**: 10/10 (mental model only)

---

*Sources: 300+ documented founder journeys from Indie Hackers, Twitter/X, podcast interviews, and public revenue disclosures (2021-2026). Additional patterns P36-P40 from multi-model synthesis (Claude + Gemini parallel research), BCG/HBR studies (2026), and Karpathy/SkyPilot experimental data (March 2026).*
