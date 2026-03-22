# PMF — Product-Market Fit Engine

## Auto-Trigger (No Slash Command Needed)

Fires automatically when founder says:

| Trigger Phrase | What Fires |
|---|---|
| "do I have PMF" / "is this working" / "have I found it" | PMF measurement protocol — all 5 systems |
| "should I scale" / "ready to grow" / "time to add channels" | PMF gate check before any growth recommendation |
| "retention is bad" / "churn is high" / "users aren't coming back" | Retention diagnosis → PMF root cause map |
| "users love it but won't pay" / "engagement is great but no revenue" | Engagement vs. monetization PMF gap diagnosis |
| "getting traction" / "this is working" / "seeing some growth" | Signal-vs-noise test: distinguish real PMF from lucky streak |
| "activation is low" / "users sign up but don't stick" | Activation diagnosis → Aha moment protocol |
| "should I add features" / "what should I build next" | PMF check first — building before PMF is solved wrong |

**Premature scaling detection fires automatically**: If founder mentions paid acquisition, SEO investment, hiring for growth, or fundraising — check PMF status first. Scaling before PMF is the most expensive mistake in startup building.

---

**Usage**: `/pmf` *(or just describe your retention/growth situation)*

**Examples**:
- `/pmf "we have 80 users, most open the app once then disappear"`
- `/pmf "NPS is 7 but no one refers anyone"`
- `/pmf "should I start running Facebook ads?"`
- `/pmf "retention seems stable but I don't know if that means anything"`

---

## Why This Exists

Most founders either scale too early or iterate too long — both are fatal.

**Scale too early**: Burning cash to acquire customers into a leaky bucket. Andreessen Horowitz found startups that scale prematurely are 2x more likely to fail than those who wait.

**Iterate too long**: Sitting on a product that actually has PMF but being too afraid to push the accelerator. Leaving revenue, market share, and eventually the whole window of opportunity on the table.

**The truth**: PMF is not a feeling. It is a set of measurable signals with documented thresholds from thousands of founders who measured them. This skill tells you which signals to measure, what the thresholds are, and what to do when you're below them.

---

## THE 5 PMF MEASUREMENT SYSTEMS

Run all 5 if you have the data. Weight them in the order listed. System 1 is the most actionable early signal. System 2 is the most important long-term signal.

---

### System 1: Sean Ellis Test — The Gold Standard

**What it is**: A single survey question asked to real users who have experienced your product.

**The exact question**:
```
"How would you feel if you could no longer use [Product]?"

Answer options (must use exactly these):
□ Very disappointed
□ Somewhat disappointed
□ Not disappointed (it really isn't that helpful)
□ N/A — I no longer use [Product]
```

**The threshold**: If >40% answer "Very Disappointed" → you have PMF for that segment.

**Real benchmarks**:
- Superhuman (email client): 58% — scaled aggressively
- Slack: 51% before Series B
- Notion: ~40% with a specific ICP (startups) before it hit mainstream
- Dropbox: 30% initially → improved onboarding → crossed 40% → then grew

**How to conduct it correctly**:
```
TIMING (critical): Ask after the 3rd meaningful usage event — NOT at signup.
Asking at signup = measuring intent. Asking after 3 uses = measuring value delivery.

Event triggers (customize per product):
- SaaS tools: After 3 separate sessions with a core action completed
- Content/media: After 5+ articles/videos consumed
- Marketplace: After first successful transaction completed
- B2B: After first export/share/workflow integration

DELIVERY:
- In-app modal: highest response rate (20-40%)
- Email (sent day after 3rd event): moderate response (5-15%)
- In-app + email follow-up: best quality responses
```

**Minimum sample for reliable signal**:
- 40 respondents = minimum to act on
- 100 respondents = reliable signal
- <40 respondents = directional only — don't make major decisions

**What to do with "Somewhat Disappointed" responses**:
```
SOMEWHAT DISAPPOINTED PROTOCOL:
These are your biggest growth lever — they're close but not converted.

For each "Somewhat Disappointed" response, ask follow-up:
1. "What is the primary benefit you get from [Product]?"
2. "What type of people do you think would benefit most from [Product]?"
3. "What would most improve [Product] for you?"

The "Somewhat Disappointed" group tells you what's missing.
The "Very Disappointed" group tells you who your real customer is.

Pattern you're looking for: "Very Disappointed" users cluster around a specific
use case, job title, company size, or workflow — that cluster IS your ICP.
```

**When you're below 40%**:
```
BELOW THRESHOLD ACTION PLAN:
Score 30-39%: You're close. Narrow ICP to the "Very Disappointed" cluster.
              Rerun the test in 30 days with that cluster only.

Score 20-29%: Deeper product problem. Identify the Aha Moment — do users
              reach it? How fast? Run the Activation Diagnosis below.

Score <20%:   Either wrong ICP or wrong problem. Go back to problem validation.
              Do not invest in growth until this score moves above 30%.
```

---

### System 2: Net Revenue Retention (NRR) — The Long-Term Signal

**What it is**: What percentage of your existing revenue stays and grows, independent of new customer acquisition.

**PMF threshold**: NRR >100% = customers naturally expand. This is the clearest financial PMF signal.

**The formula**:
```
NRR CALCULATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Start MRR (customers at beginning of period):      $A
Minus churned MRR (cancellations):                -$B
Minus contracted MRR (downgrades):                -$C
Plus expansion MRR (upgrades, seat adds, usage):  +$D

NRR = (A - B - C + D) / A × 100%

Example:
Start: $10,000 MRR from 50 customers
Churn: -$500 (5 customers cancelled, avg $100)
Contraction: -$200 (2 customers downgraded)
Expansion: +$800 (8 customers upgraded)

NRR = ($10,000 - $500 - $200 + $800) / $10,000 = 101%
```

**NRR benchmarks by segment**:
| Company | NRR | Context |
|---|---|---|
| Snowflake (IPO) | 158% | Usage-based enterprise |
| Twilio | 131% | Developer platform |
| Slack | 143% | Pre-acquisition |
| Notion | ~110% | Bottoms-up PLG |
| Median SaaS ($1-5M ARR) | 95-105% | SMB heavy |
| Healthy early-stage | >100% | The PMF signal |

**Why NRR beats churn rate as a PMF signal**:
```
THE LEAKY BUCKET TEST:
If NRR < 90%: Your bucket is leaking faster than you're filling it.
              No amount of acquisition spending fixes this.
              Every dollar spent on growth is partially wasted.

If NRR 90-100%: Retention is acceptable. You can grow, but slowly.
                Focus on reducing churn before scaling acquisition.

If NRR >100%: Bucket is self-filling. This is the PMF signal.
              Now acquisition spending compounds — every dollar goes further.

The compounding math:
$100K ARR at NRR 90% → after 3 years of zero new customers: $73K ARR
$100K ARR at NRR 110% → after 3 years of zero new customers: $133K ARR

PMF with NRR >100% means your existing customers are growing your revenue without you.
```

---

### System 3: Cohort Retention Curves — The Behavioral Signal

**What it is**: Tracking the % of users from a given signup week/month who are still active at each subsequent interval.

**The key insight**: The curve shape matters more than any individual data point. A flattening curve = retained segment.

**What a PMF retention curve looks like**:
```
RETENTION CURVE INTERPRETATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

No PMF (still declining at 90 days):
100% → 60% → 35% → 20% → 12% → 8% → 5% → 3%
[Curve keeps declining — no stable retained base]

Approaching PMF (flattening but below threshold):
100% → 55% → 35% → 25% → 22% → 21% → 20% → 20%
[Curve flattens at 20% — core segment exists but small]

PMF (flattens above threshold):
100% → 65% → 50% → 42% → 40% → 39% → 39% → 39%
[Curve flattens above benchmark — strong retained segment]
```

**Retention thresholds by product type**:
| Product Type | L7 Target | L30 Target | L90 Target | Example |
|---|---|---|---|---|
| Daily-use tools (habit products) | >40% | >25% | >20% | Slack, Notion, Superhuman |
| Weekly-use tools | >60% | >40% | >25% | Calendly, project mgmt |
| Monthly/workflow tools | N/A | >60% | >50% | Reporting tools, analytics |
| Transactional/on-demand | N/A | >30% repurchase | >50% quarterly | Marketplaces |

**Real company benchmarks**:
- Slack: L30 = 85%+ (daily messaging product)
- Dropbox: L30 = 60% at PMF crossing
- Airbnb: L90 = 30%+ (low-frequency use product, correct benchmark)
- World-class consumer app: L30 = 25%+ (strong PMF)

**Power user identification from cohort data**:
```
POWER USER PROTOCOL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1: Identify top 20% of users by usage frequency/depth
Step 2: Pull their profile data — job title, company size, signup source,
        onboarding path, first feature used, time-to-first-value
Step 3: Interview them: "What does [Product] replace for you?"
                        "What would you use if we disappeared tomorrow?"
                        "When do you use us most? What triggers the session?"
Step 4: The answer to Step 3 IS your ICP. Rebuild positioning for them.
Step 5: Measure if new users who match power user profile retain at power user rates.

Why this works: Your best users found the PMF signal you haven't articulated yet.
               They're living proof of the correct use case. Mine them.
```

---

### System 4: Organic Growth Rate — The Word-of-Mouth Signal

**What it is**: What % of new users arrive without any paid or direct effort from you.

**PMF threshold**: >20% of new users come from referral or organic word-of-mouth.

**Why this signal matters**: People refer products that create genuine value. Referral is embarrassment-resistant behavior — nobody sends a friend a tool they're not confident about. When 20%+ of your growth is organic, your users are doing your marketing for you, which only happens when value is real.

**How to track referral source accurately** (not just UTM):
```
REFERRAL TRACKING PROTOCOL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem with UTMs: Dark social (Slack DMs, email forwards, private channels)
                  shows up as "direct" traffic — massively underestimates referral.

Accurate tracking:
1. Signup form: "How did you hear about us?" (open text, not dropdown)
   → Read every answer manually for first 6 months
   → Look for: friend told me, saw someone's post, Slack/Discord/community

2. After activation (3 days in): "Did someone recommend [Product] to you?"
   → Captures delayed referrals from organic discovery

3. Attribution model: Credit any "direct" signup that arrives within 30 days of
   a referral touchpoint (shared link, forwarded email) to referral

Organic signal calculation:
(Referral signups + "direct" attributed to referral) / Total new signups
Target: >20% to confirm PMF word-of-mouth flywheel is starting
```

**NPS + referral double-check**:
```
NPS BENCHMARK AGAINST REFERRAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NPS <20: Referral rare. Users politely tolerating the product.
NPS 20-40: Some referral, but not a growth engine.
NPS >50: Referral becoming meaningful. PMF signal.
NPS >70: Strong PMF. Word-of-mouth is a primary channel.

Warning: NPS is a lagging indicator. Measure it AND actual referral behavior.
High NPS with <10% referral = people say they'd recommend but haven't. Gap exists.
```

**Building referral tracking from day 1** (before you need it):
```
DAY 1 TRACKING SETUP (takes 2 hours, pays forever):
1. Add "How did you hear about us?" to signup form (text field, not dropdown)
2. Tag every source manually in your customer list for first 100 users
3. Create a simple tracking doc: [User ID] [Source] [Date] [Referred by user ID?]
4. Set a monthly calendar reminder: "Calculate organic % of new signups this month"

When you have <100 users you can track this manually.
When you have 100+ users you need this data to understand where PMF traction is.
```

---

### System 5: Bright Spot Analysis — The ICP Signal (Kathy Sierra Method)

**What it is**: Find the 10-20% of users who have transformational outcomes → understand what's different about them → build the product and positioning for THEM.

**The core insight**: Most products have PMF with a small segment long before they think they have PMF. Averaging across all users hides it. The bright spots ARE the product.

```
BRIGHT SPOT PROTOCOL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Define "transformational outcome" for your product.
        Not "uses the product frequently" — "achieves [specific result]."
        Examples:
        - Invoice tool: "Reduced time-to-payment by >50%"
        - Project management: "Launched a project that would have slipped without it"
        - Email tool: "Response rates increased measurably"
        - Analytics: "Made a decision that generated >$X based on this data"

Step 2: Identify users who achieved this outcome. Sort by:
        - Usage frequency AND depth (not just logins — actual core feature use)
        - NPS score (if collected)
        - Support ticket sentiment (zero complaints = possible bright spot)
        - Self-reported success (look for power user emails / tweets / reviews)

Step 3: Profile the bright spots. Pull:
        - Job title / role
        - Company size / type
        - Signup source / acquisition channel
        - Onboarding path: what was the first feature they used?
        - Time to first core action: how fast did they get to value?
        - What did they replace? What does this sit next to in their workflow?

Step 4: Interview 5-10 bright spot users. One question matters most:
        "Walk me through the last time [Product] helped you with something important."
        Let them talk. Don't pitch. Don't lead. Just listen.

Step 5: The pattern that emerges from those interviews = your real ICP + positioning.
        The bright spots found a use case you didn't design for — or confirmed
        one you weren't sure about. This is PMF hiding in plain sight.

Step 6: Rebuild your onboarding to get new users to the bright spot path faster.
        Kill friction between signup and the "Aha moment" the bright spots experienced.
        Measure: does new cohort retention improve for users who follow bright spot path?
```

**Why this matters for PMF acceleration**: The question isn't "do I have PMF?" It's "do I have PMF with who?" Bright spot analysis answers both simultaneously.

---

## THE PMF DIAGNOSTIC FRAMEWORK

When something feels off, run through this before making any build or marketing decision:

```
PMF DIAGNOSTIC TREE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYMPTOM 1 — "No one signs up"
→ NOT a PMF problem yet. This is a distribution problem.
→ Don't diagnose PMF when you can't measure it. Get 40 users first.
→ Action: Direct outreach to ICP. 20 DMs before any marketing spend.

SYMPTOM 2 — "People sign up but don't activate" (signup → no core action)
→ Onboarding problem. The Aha Moment isn't reached fast enough.
→ Aha Moment definition: The first moment a user receives the core value of the product.
→ Time-to-value targets:
   Consumer: <30 seconds to first "oh wow" moment
   SMB SaaS: <5 minutes to first meaningful output
   Enterprise: <1 week to first demo of value to the buyer
→ Action: Run 5 copilot sessions — sit with users and watch. The drop-off point IS the problem.

SYMPTOM 3 — "People activate but churn after 30 days"
→ Habit formation failure. No natural recurrence trigger.
→ Ask: Is there a real-world event that naturally prompts re-use?
         (weekly review, monthly billing, project kickoff, daily standup?)
→ Ask: Does using the product once make the next use more valuable? (network/data effects?)
→ Ask: What do users go back to instead? (status quo pull — measure this)
→ Action: Map the user's weekly workflow. Where does your product need to fit?
          If it requires behavior change with no forcing function → product problem.

SYMPTOM 4 — "People use it but won't pay"
→ Three possible causes:
   (a) Freemium trap: you gave too much free. Users have no reason to upgrade.
   (b) Wrong ICP: users are not the buyers. (Classic: individual users who can't expense it)
   (c) Value-price gap: benefit delivered < price asked. Product not differentiated enough.
→ Test: Offer it to 10 users at 2x your planned price. If none say yes → value gap.
        If 3+ say yes at 2x → pricing communication failure, not product failure.

SYMPTOM 5 — "People pay but tell no one"
→ The "politely useful" trap. Product is 10% better than the alternative, not 10x.
→ Referral requires users to stake their reputation on the product.
→ They'll only do that for a product that makes THEM look good / smart.
→ Ask: What outcome does using your product signal to their peers?
→ Ask: Does a user get credit for bringing this to their team? If not, build that in.
→ 10x better test: "What would a user have to give up to get this value without you?"
   If the answer is "not that much" → product problem, not marketing problem.

SYMPTOM 6 — "Early users love it, new users don't retain as well"
→ ICP drift. You've expanded beyond the segment with the acute problem.
→ Your positioning is attracting the wrong people now that you're growing.
→ Action: Segment retention by acquisition channel. Which channel delivers users who
          retain at your best-cohort rate? Double down on that channel only.
→ Classic cause: early users = founder's network (highly relevant), new users = generic outreach.
```

---

## THE PREMATURE SCALING DETECTION SYSTEM

**Fires as an anti-pattern check whenever growth/acquisition/hiring is discussed.**

If any of these conditions are true, scaling will accelerate failure, not success:

| Warning Signal | What It Means | Action Required |
|---|---|---|
| Monthly churn >5% AND considering paid ads | Spending to fill a leaky bucket | Fix churn first. Every ad dollar partially wasted. |
| NRR <90% AND hiring marketing | Marketing can't fix a retention problem | Fix NRR to 100%+ before marketing hire |
| L30 retention <30% AND investing in SEO | Compounding content into a non-sticky product | SEO traffic won't convert to retained users |
| Sean Ellis score <30% AND raising Series A | Building a house on a cracked foundation | Investors who understand this will see it |
| NPS <20 AND running referral program | Asking unsatisfied users to spread the word | No referral program survives a weak NPS |
| Monthly churn >8% AND positive about growth | Growth is masking a retention crisis | Calculate net growth rate: new - churned |
| Gross margin <50% AND scaling acquisition | Unit economics deteriorate with scale | Fix margins first — must reach 60%+ |

**The premature scaling cost model**:
```
SCENARIO: $5K MRR with 8% monthly churn

If you spend $5K/mo on ads to acquire 20 new customers at $250/mo:
  New MRR from ads: +$5,000
  Churned this month (8% × $5K): -$400
  Net new MRR: +$4,600
  CAC spent: $5,000

After 6 months of this:
  You've spent $30,000 on ads
  Net MRR growth: ~$27,600 total added (not accounting for compounding churn)
  Reality: Monthly churn is accelerating as base grows
  Effective LTV at 8% churn: $250 ÷ 0.08 = $3,125
  CAC: $250 per customer
  LTV:CAC = 12.5x (looks great on paper)

BUT: at 8% churn, average customer lasts 12.5 months
     LTV:CAC only looks good because you're measuring wrong.
     Fix churn to 3% → LTV = $8,333 → now you can actually scale.
```

---

## THE PMF ACCELERATION PROTOCOL

Once you have >40 real users — how to reach PMF faster. These are ordered by leverage, not by difficulty.

### 1. Weekly Customer Calls (Non-Negotiable Until PMF)

```
CUSTOMER CALL PROTOCOL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Frequency: 3-5 calls per week until Sean Ellis >40%
Duration: 30 minutes
Who: Mix of active users, activated-but-churned users, and churned users

The 5 questions that matter (in order):
1. "What were you trying to do when you signed up?"
   → Tests whether your positioning attracted the right person

2. "Walk me through the last time you used [Product]. What were you doing?"
   → Reveals actual use case vs. intended use case

3. "What happened before you opened [Product]? What triggered the session?"
   → Identifies the real-world trigger that creates usage (the habit loop)

4. "If [Product] disappeared tomorrow, what would you do instead?"
   → Defines your real competition (often not who you think)

5. "Who else do you know who has this problem?"
   → Validates ICP specificity AND generates referrals simultaneously

DO NOT: Ask about features. Ask about problems and workflows.
DO NOT: Pitch or defend. Only listen and clarify.
DO: Take verbatim quotes. These become your positioning copy.
```

### 2. The "Most Important Email" Ritual

Email every new user personally within 24 hours of signup. Not automated. Not from a noreply address.

```
TEMPLATE (adapt for your product):
Subject: Quick question about [Product]

Hi [Name],

I'm [Your Name], the founder of [Product]. I saw you signed up yesterday — thanks.

Quick question before you dive in: what were you hoping [Product] would help you with?

No pitch, no demo — just want to make sure you get to the right thing fast.

[Your name]
P.S. If you run into anything, reply directly — I'm the one answering.
```

This email does four things: (1) confirms they're real and engaged, (2) gives you real intent data, (3) opens a 1:1 channel for onboarding help, (4) signals you're a founder who cares, which builds loyalty. Response rates: 15-40% for this type of email from a real founder.

### 3. Feature Kill Protocol

The counter-intuitive PMF move: kill features until activation improves.

```
FEATURE KILL PROTOCOL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Every week until PMF: identify one feature to remove, hide, or deprioritize.

Criteria for killing:
- Used by <10% of active users AND not on the path to Aha Moment
- Adds complexity to the signup/activation flow
- Exists because you thought users would want it, not because they asked

Effect: Simplification almost always improves activation.
        Every feature is friction for users who don't need it.

Slack's early kill: removed 8 of 12 early features before finding PMF in gaming teams.
Notion's early kill: removed the "database" view from default onboarding — activation improved 40%.

Track: Activation rate (signup → first core action) before and after each kill.
       If activation improves: feature was hurting you.
       If flat: kill it anyway — maintenance cost isn't worth it.
```

### 4. The Boring Middle Navigation

Map exactly what users do between entering the product and getting the first value. This is where PMF is lost.

```
BORING MIDDLE AUDIT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Define your Aha Moment precisely. One specific action.
        "The moment the user [specific action] for the first time."
        Examples:
        - "Sent their first invoice and it arrived in their client's inbox"
        - "Connected their first data source and saw a chart appear"
        - "Completed their first project task and marked it done"

Step 2: Map every step between signup and that Aha Moment.
        Use session recordings (Hotjar, FullStory, Posthog).
        Count clicks. Count decisions. Count confusing moments.

Step 3: Calculate time-to-Aha for your last 20 activated users.
        What's the median? What's the range?

Step 4: Identify the biggest friction point in the path.
        Where do users most often stop before reaching the Aha?

Step 5: Remove that friction. Measure if time-to-Aha decreases.
        Repeat weekly.

PMF acceleration happens when: Time-to-Aha decreases → Activation rate increases
                               → More users reach value → More retention → Sean Ellis improves.
```

### 5. Copilot Mode (5 Sessions Changes Everything)

Watch a user use your product live — say nothing, just observe. This is the highest ROI research activity in pre-PMF.

```
COPILOT SESSION PROTOCOL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Setup: "Would you mind sharing your screen and trying [Product] while I watch?
        I won't explain anything — I just want to see what's intuitive and what isn't.
        If you get confused, that's the most valuable thing for me."

What to track (take notes, don't react):
□ Where do they pause and look confused?
□ Where do they click and nothing happens (or something unexpected happens)?
□ What do they read? What do they skip?
□ What do they say out loud ("huh", "why is this...", "oh wait...")?
□ What do they give up on?
□ When do they light up? (That moment IS the Aha Moment you're building toward)

After 5 sessions: The same 3-5 friction points will appear across all of them.
                  Fix those 3-5 things before anything else.
                  Repeat until you don't see confusion anymore.
```

---

## VERTICAL PMF vs. HORIZONTAL PMF

Understanding which you have determines your GTM strategy.

```
VERTICAL PMF:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Definition: Solve one problem for one industry perfectly.
Signal: Sean Ellis >40% within that industry. Referral flows within the vertical.
Advantage: Easier to find, faster to confirm, higher word-of-mouth density.
GTM: Dominate one vertical before expanding. Own the category for [industry].
Examples: Veeva (pharma CRM), Toast (restaurant POS), Procore (construction mgmt)

HORIZONTAL PMF:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Definition: Solve one problem across multiple industries.
Challenge: Averaging across industries masks where PMF actually lives.
           Aggregated retention of 30% can hide: 60% in one vertical, 15% in another.
Warning: DO NOT conclude you have horizontal PMF until you have confirmed VERTICAL PMF
         independently in 2+ segments with similar user profiles.
GTM: Find the verticals with >40% Sean Ellis first. Expand from those.
Examples: Slack (started gaming teams → tech companies → everything), Notion (founders → students)

THE HORIZONTAL PMF TRAP:
"Our users come from lots of different industries" sounds like horizontal traction.
It's actually: unclear ICP + unclear positioning + unclear why anyone stays.
Segment your retention data FIRST. If retention varies wildly by industry — you have
vertical PMF hiding in averaged noise. Find it.
```

---

## THE CHASM CROSSING SIGNAL

After PMF with early adopters — how to know you're ready for the mainstream.

Geoffrey Moore's chasm: early adopters tolerate rough edges for new capability. Early majority requires proven solutions, peer references, and ecosystem fit.

```
CHASM CROSSING CHECKLIST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Signals you're crossing the chasm (need 4 of 5):
□ >30% of new users arrive from referrals from early users to their non-tech colleagues
□ You're fielding questions about integrations you don't have yet
  (early majority needs [Product] to fit their existing stack)
□ Procurement / IT is getting involved in purchase decisions (not just the champion)
□ Users start asking "who else in [industry] uses this?" before committing
□ Case studies and third-party validation are requested before trials

What to prepare before crossing:
1. 3 case studies with quantified outcomes (not quotes — numbers)
2. Integrations with the 3 tools your ICP uses daily
3. SOC 2 or security documentation (early majority IT departments require this)
4. Clear onboarding for "I've never heard of this category" users
   (early adopters figured it out; early majority need to be shown)
5. Pricing that reflects value clearly (early majority is price-sensitive to ambiguity,
   not necessarily to amount)

The crossing the chasm failure mode: Trying to serve early majority before early adopters
are done referring. Result: too many support tickets, diluted referral quality, confused positioning.
```

---

## SURVEY TEMPLATES AND SCRIPTS

### Sean Ellis Survey (Full)

```
SEAN ELLIS SURVEY — COMPLETE TEMPLATE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Subject line: "Quick question — takes 2 minutes"

Body:
Hi [Name],

I'm [Founder] from [Product]. You've been using [Product] for [X weeks] and
I'd love your honest feedback — it directly shapes what we build.

Three quick questions:

1. How would you feel if you could no longer use [Product]?
   □ Very disappointed
   □ Somewhat disappointed
   □ Not disappointed (it's not that helpful)

2. (If "Somewhat disappointed"):
   What is the main benefit you get from [Product]?
   [open text]

3. What type of person do you think would benefit most from [Product]?
   [open text]

4. How could we improve [Product] for you?
   [open text]

That's it. Honest answers — even brutal ones — are the most helpful.

[Founder name]
```

### Exit Interview Script (Churned Users)

```
EXIT INTERVIEW SCRIPT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Subject: "Honest question — why did you cancel?"

Body:
Hi [Name],

I saw you cancelled [Product] — I'm not going to pitch you to come back.

I'm genuinely trying to understand what went wrong so we can fix it for others.
Would you be willing to answer one question?

"What were you hoping [Product] would do for you that it didn't?"

That's it. No sales call. Just one answer in reply to this email.

[Founder name]

---
LIVE INTERVIEW VERSION (for users who agree to a call):

Question 1: "What were you originally trying to accomplish when you signed up?"
Question 2: "Was there a moment when you decided to cancel? What happened?"
Question 3: "What did you go back to instead? Or what are you doing instead now?"
Question 4: "What would have needed to be true about [Product] for you to stay?"
Question 5: "Is there anything I could tell you about [Product] that would make you reconsider?"
            (Note: This is research, not a save attempt. Listen to the answer, don't argue.)
```

### Activation Aha Moment Survey (Active Users)

```
AHA MOMENT SURVEY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Trigger: Send 7 days after signup to users who completed a core action

"Quick question: Was there a specific moment when [Product] clicked for you?
 When you thought: 'Oh — THIS is what this is for'?"

□ Yes — [open text: "Describe that moment in 1-2 sentences"]
□ Not yet — still figuring it out
□ Honestly, I'm not sure it's clicked yet

If they answer "Yes": the description they give = your marketing copy.
If they answer "Not yet": trigger an onboarding nudge within 24 hours.
If they answer "Not sure yet": flag for founder outreach — personal touch within 48 hours.
```

---

## PMF OUTPUT FORMAT

When running a full PMF assessment:

```
PMF ASSESSMENT: [Product Name]
Date: [date]   |   Stage: [inferred MRR]
════════════════════════════════════════════════════════

OVERALL PMF STATUS: [🟢 PMF CONFIRMED / 🟡 PMF APPROACHING / 🔴 PRE-PMF]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYSTEM 1: SEAN ELLIS SCORE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score: [X]% "Very Disappointed"   |   Sample: [N] respondents
Threshold: 40%
Status: [✅ Above / ⚠️ Close / ❌ Below]
"Very Disappointed" ICP cluster: [what profile they share, if visible]
Action: [what to do based on score]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYSTEM 2: NET REVENUE RETENTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NRR: [X]%
Threshold: 100%
Status: [✅ Above / ⚠️ Close / ❌ Below]
Monthly churn: [X]%   |   Expansion MRR: $[X]/mo
Leaky bucket diagnosis: [specific bottleneck]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYSTEM 3: COHORT RETENTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
L7: [X]%   L30: [X]%   L90: [X]%
Curve status: [Declining / Flattening / Flat]
Benchmark for [product type]: [targets]
Status: [✅ Above / ⚠️ Close / ❌ Below]
Power user profile: [early pattern, if visible]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYSTEM 4: ORGANIC GROWTH RATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Referral/organic %: [X]% of new signups
Threshold: 20%
Status: [✅ Above / ⚠️ Close / ❌ Below]
Primary referral source: [channel where word-of-mouth is flowing]
NPS: [X]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYSTEM 5: BRIGHT SPOT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bright spot profile: [job title, use case, retention rate]
% of users who are bright spots: [X]%
What they have in common: [pattern]
Aha Moment they experienced: [description]
Status: [Identified / Partial / Not yet run]

════════════════════════════════════════════════════════
PMF VERDICT
════════════════════════════════════════════════════════
[🟢 CONFIRMED]: [X] of 5 systems above threshold. Safe to scale acquisition.
[🟡 APPROACHING]: Strong on [systems]. Weak on [systems]. Narrow ICP first.
[🔴 PRE-PMF]: Below threshold across systems. Do not scale. Run protocol below.

HIGHEST LEVERAGE ACTION:
[The single thing that will most move PMF in the next 30 days]

KILL SIGNAL: [specific measurable data that proves current approach wrong within 30 days]
```

---

## SEQUOIA ARC PMF ARCHETYPE SYSTEM

**Critical insight**: PMF looks completely different depending on which archetype your product is. Applying uniform PMF advice across archetypes produces wrong recommendations. This section routes your PMF work to the correct framework.

### Archetype Detection (Run at start of any PMF assessment)

```
PMF ARCHETYPE DETECTOR:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Question 1: "How do your best customers describe their situation before finding you?"

□ "I was desperate / couldn't believe how painful this was / it was killing us"
  → HAIR ON FIRE archetype

□ "I knew this was a problem but assumed it was just how things work / I'd given up on it being solved"
  → HARD FACT archetype

□ "I didn't realize this was even a problem until [product] showed me a different way"
  → FUTURE VISION archetype

Question 2 (if still unclear): "What was your customer's life like the week BEFORE they found you?"
- Acute daily pain that was costing them time/money/customers → Hair on Fire
- Chronic background problem they'd normalized → Hard Fact
- No conscious problem — a new possibility was revealed → Future Vision
```

---

### Archetype 1: HAIR ON FIRE 🔥

**Definition**: Customers have an acute, urgent problem causing immediate pain. They're already looking for a solution. The market "gets it" immediately.

**Recognition signals**:
- First-touch conversion is high (people understand immediately what you do)
- Customers can articulate the pain in vivid, emotional terms
- Short sales cycle — they buy before fully testing
- Referrals flow easily because the problem is universally recognized

**Examples**: Stripe (accepting payments was broken), PagerDuty (on-call alerting was hell), Zendesk (customer support tickets in an inbox)

**PMF measurement adjustments for Hair on Fire**:
```
HAIR ON FIRE PMF THRESHOLDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sean Ellis: Standard 40% applies. But expect to hit it faster (60-90 days vs. 6-18 months).
            If you're NOT hitting 40% quickly: you've misidentified the archetype OR
            your solution isn't actually better than the current workaround.

NRR: Target >110%. Hair on Fire products have high switching costs — if NRR is <100%,
     your solution isn't actually better enough. The bar is high because users ALREADY
     KNEW THEY HAD THIS PROBLEM — they won't tolerate a weak solution.

Referral: Expect >30% organic. Pain is universally recognized — if they love you,
          they tell everyone with the same pain.

Time to PMF signal: 3-6 months with first 100 users. If you need >6 months: wrong archetype.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**PMF obstacles specific to Hair on Fire**:
1. **Competitive Noise**: Many solutions exist for acute pain. PMF = being clearly 10x better, not just better.
2. **Urgency-Price Trap**: Early users pay because desperate. Later users price-compare. True PMF requires value beyond urgency.
3. **First-Mover Erosion**: Competitors copy fast once the pain is confirmed. Build switching costs BEFORE scaling.

**PMF acceleration for Hair on Fire**:
- Focus on "time to relief" — how fast can the customer feel the pain go away?
- Build the product around the MOMENT OF PAIN, not general utility
- Referrals are your engine — make sharing the product part of the relief experience

---

### Archetype 2: HARD FACT 📊

**Definition**: Customers have a real problem they've accepted as inevitable. They weren't actively looking for a solution. "That's just how it works" is the mindset you're breaking.

**Recognition signals**:
- Education is required before conversion — customers need to understand there's a better way
- Longer sales cycle — trust must be built before they believe the problem is solvable
- Early adopters are visionaries (not the majority)
- Referrals are slower — "you have to experience it to believe it"

**Examples**: Salesforce (CRM in spreadsheets was "normal"), Dropbox (file sharing via email was "normal"), Calendly (back-and-forth scheduling was "just how it works")

**PMF measurement adjustments for Hard Fact**:
```
HARD FACT PMF THRESHOLDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sean Ellis: 40% threshold still applies but expect <40% for 6-18 months. This is NOT failure.
            "Somewhat Disappointed" responses are CRITICAL here — they're your converts-in-waiting.
            Hard Fact PMF success = the Somewhat Disappointed cohort converts to Very Disappointed
            as they use the product longer. Measure this transition, not just the current score.

NRR: Target >100%. Expansion comes from users who finally "get it" and expand usage.
     Watch for slow initial adoption then sharp expansion — this is the Hard Fact pattern.
     If NRR is declining: you haven't solved the "normal" belief. Education is failing.

Time to PMF signal: 6-18 months with first 100 users. Be patient. The breakthrough is a
                    threshold effect — once users "get it," they become evangelists.

Activation metric: TIME TO "AHA MOMENT" is the most important metric.
                   The moment they go from "I guess this works" to "oh my god why didn't I do this sooner"
                   is the PMF signal for Hard Fact. Track this moment explicitly.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**PMF obstacles specific to Hard Fact**:
1. **The Patience Trap**: Slow traction gets misread as lack of demand → premature pivot
2. **Wrong Segment Sequencing**: Leading with the wrong ICP (skeptics vs. visionaries) kills early traction
3. **Education Overload**: Spending all energy convincing vs. serving the people already convinced

**PMF acceleration for Hard Fact**:
- Find the visionaries (people who already BELIEVE the status quo is broken) — they're your early majority
- "Before/after" case studies are your highest-leverage marketing asset
- Free trial or freemium almost always required — users must experience the product to believe in it
- The KEY insight: stop trying to convince skeptics. Find the believers and serve them until they evangelize.

---

### Archetype 3: FUTURE VISION 🔭

**Definition**: Customers don't know they have the problem until you show them a new possibility. You're creating a category, not entering one. The hardest PMF to find — but most defensible when found.

**Recognition signals**:
- Customer can't articulate the problem before experiencing the product
- "Demo-to-aha" ratio is high — live demos convert much better than messaging
- First reaction often: "I didn't know I needed this"
- Long time to PMF — often 18-36 months before signal is clear

**Examples**: iPhone (people didn't know they wanted a touchscreen computer in their pocket), Notion (people didn't know they wanted documents + databases combined), Figma (designers didn't know they wanted collaborative browser-based design)

**PMF measurement adjustments for Future Vision**:
```
FUTURE VISION PMF THRESHOLDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sean Ellis: Standard 40% threshold still applies but SEGMENT before measuring.
            Future Vision PMF is almost always NARROW before it's broad.
            Measure Sean Ellis on your earliest, most engaged cohort only.
            If >40% in your first 20-50 users: you have Future Vision PMF with visionaries.
            Scale from there.

Do NOT: Average Sean Ellis across all users including those who "tried it and left."
        Future Vision products have a bimodal distribution: people who "get it" (love) and
        people who don't (leave). Averaging = 20% = false negative.

Organic growth: Word of mouth is SLOW until a breakthrough moment. Track NPS trajectory
                instead: if NPS is increasing each month (even slowly), you're building.

Time to PMF signal: 12-36 months. Do not interpret slow traction as product failure.
                    Monitor: "Are the users who DO get it passionate (>70 NPS)?" If yes, continue.

Key question: "If we showed 1,000 of the right person this product, how many would 'get it' immediately?"
              If <5%: positioning/discovery problem. If 30%+: you have niche Future Vision PMF.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**PMF obstacles specific to Future Vision**:
1. **Category Education Cost**: You're spending to educate the market while competitors watch and copy
2. **CAC Explosion**: Without a recognized category, inbound CAC is impossible — outbound is required, which is expensive
3. **Premature Scaling**: Raising $10M to "educate the market" before PMF = the most expensive startup mistake

**PMF acceleration for Future Vision**:
- Find the "naturals" — people for whom the new vision is instantly obvious (often specific job title/industry)
- Build a community of naturals before building for the mainstream — they become your content/referral engine
- Demo-first GTM: get people to experience the product before buying it (webinars, free tools, viral features)
- The KEY insight: you're not convincing — you're finding people who already think like your vision. Map the archetype of the believer PRECISELY.

---

### Archetype-Informed PMF Assessment Output

When running a PMF assessment, add one line at the top of the output:

```
ARCHETYPE DETECTED: [Hair on Fire / Hard Fact / Future Vision]
ARCHETYPE EVIDENCE: [1 sentence — what customer words/behavior supports this classification]
ARCHETYPE-ADJUSTED TIMELINE: [Expected time to PMF signal for this archetype]
ARCHETYPE-ADJUSTED THRESHOLD: [Any modifications to standard thresholds explained above]
```

**The most common archetype misclassification**: Founders with Future Vision products who apply Hair on Fire timelines → quit too early because "traction is slow." The product needed 18 months. They gave it 6.

**The most expensive archetype error**: Assuming you have a Future Vision product (market education excuse) when you actually have a Hair on Fire product that's just not 10x better than alternatives → years spent "educating the market" for a problem people have other solutions for.

```
ARCHETYPE VALIDATION CHECK:
If founder says "the market doesn't understand yet" → verify archetype.
Ask: "Do customers with this pain KNOW they have it and actively look for solutions?"
→ YES: Hair on Fire (and your product isn't differentiated enough)
→ NOT EXACTLY: Hard Fact (and education is your primary GTM lever)
→ NO: Future Vision (and finding naturals is your PMF path)
```

---

## INTEGRATION

**PMF connects to everything — it is the gate between phases.**

| Skill | Relationship |
|---|---|
| `validate.md` | Pre-PMF gates: confirm problem exists before measuring PMF |
| `growth.md` | PMF must be confirmed before any growth skill runs |
| `finance.md` | Unit economics only become meaningful post-PMF (CAC/LTV math changes as churn stabilizes) |
| `morning.md` | PMF metrics (Sean Ellis, NRR, L30 retention) belong in weekly pulse — not just quarterly |
| `sales.md` | Bright spot interviews and exit interviews are sales conversations with research intent |
| `decide.md` | "Should I scale?" runs through PMF gate before the decision framework |
| `content.md` | "Very Disappointed" users' exact words → your positioning copy and content topics |

**The ordering rule**:
1. `validate.md` — Confirmed people will pay for this
2. `pmf.md` — Confirmed retained users are staying and referring
3. `growth.md` — Now scale the acquisition channels

Skipping step 2 is the most expensive mistake in early-stage company building. The PMF Engine exists to make that skip impossible.
