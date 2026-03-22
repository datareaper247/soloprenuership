# PMF Engine — The Product-Market Fit Measurement System

## Auto-Trigger (No Slash Command Needed)

Fires automatically when:
- "do I have PMF" / "is this working" → PMF measurement protocol
- "should I scale" / "ready to grow" → PMF gate check FIRST before any growth advice
- "retention is bad" / "churn is high" → retention analysis + PMF diagnosis
- "users love it but don't pay" → engagement vs monetization PMF gap
- "getting traction" → distinguish signal from noise protocol
- "activation is low" / "people sign up but don't use it" → activation diagnosis

**THE SCALE GATE RULE**: No growth advice without PMF check first.
If PMF score <60%: retention is the problem. Acquisition budget makes it worse.

---

## Why This Exists

Premature scaling is the #2 cause of startup death (Startup Genome Project, 2019).
It killed companies with 10x more funding than you have.

The brutal truth:
- **At PMF**: Each new customer acquired adds compounding value.
- **Without PMF**: Each new customer acquired accelerates the burn rate and adds churn data.

The diagnostic: If you're losing money acquiring customers who don't stay, you're not growing — you're learning an expensive lesson.

**Sean Ellis's discovery**: He surveyed 100+ startups and found one question predicted PMF with 95% accuracy. The companies above 40% went on to scale. The companies below failed or pivoted.

**The retention curve revelation** (Brian Balfour): A product without PMF has a retention curve that hits zero. A product with PMF has a retention curve that flattens — some percentage of users stay forever. Finding that flattening is finding your PMF.

---

## THE 5 PMF MEASUREMENT SYSTEMS

### System 1: Sean Ellis Test (The Gold Standard)

```
SEAN ELLIS SURVEY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE QUESTION: "How would you feel if you could no longer use [Product]?"
A. Very disappointed
B. Somewhat disappointed
C. Not disappointed
D. N/A — I no longer use it

PMF THRESHOLD: ≥40% answer "Very Disappointed"

BENCHMARKS FROM REAL COMPANIES:
→ Superhuman: 58% "Very Disappointed" → scaled aggressively
→ Slack: 51% → IPO
→ Airbnb: 48% → scaled
→ Companies below 40%: reposition, rebuild, or pivot

WHEN TO RUN IT:
→ AFTER third usage session (not at signup — too early)
→ AFTER user has reached their "Aha moment" (if they haven't, it's not a PMF signal)
→ MINIMUM 40 respondents (below this = statistically meaningless)
→ Never ask leading questions before the survey

WHAT TO DO WITH THE RESULTS:

If ≥40% "Very Disappointed":
→ Interview "Very Disappointed" users: "Who would you share this with? Who is it not for?"
→ This group defines your real ICP. Build more of what they love.
→ Scale acquisition targeting ONLY people who look like these users.

If 30-40% "Very Disappointed":
→ Approaching PMF. Segment the "Somewhat Disappointed" group.
→ Ask: "What would make you 'Very Disappointed' if it disappeared?"
→ Likely 1-2 features or use cases are blocking full PMF.
→ Build those. Re-test in 30 days.

If <30% "Very Disappointed":
→ Not at PMF. Do NOT scale.
→ Identify "bright spots" — who ARE the "Very Disappointed"?
→ What's different about them? Job title? Company size? Use case?
→ Narrow ICP to the bright spots and rebuild positioning for them.
→ Re-test after 60 days of focused development.

SETUP GUIDE (free, 5 minutes):
→ Use Typeform or Google Forms
→ Send to users who have logged in at least 3 times in the last 30 days
→ Subject line: "One question for our most active users"
→ Don't explain what the answers mean. Let them answer intuitively.
```

### System 2: Net Revenue Retention (NRR)

```
NRR PMF MEASUREMENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FORMULA: NRR = (Starting MRR - Churned MRR + Expansion MRR) / Starting MRR × 100

EXAMPLE:
Starting MRR: $10,000
Churned: -$500 (customers who left)
Contraction: -$200 (customers who downgraded)
Expansion: +$800 (customers who upgraded)
NRR = ($10,000 - $500 - $200 + $800) / $10,000 = 101%

PMF THRESHOLDS:
<90% NRR: Revenue is shrinking from existing customers. CRISIS. Fix before anything.
90-100% NRR: Flat. Acceptable but not PMF signal. Work on expansion revenue.
100-110% NRR: Strong PMF signal. Customers expand usage naturally.
>110% NRR: Elite PMF signal. Customers are so dependent they pay more every month.
            This is what allows you to scale acquisition aggressively — the bucket isn't leaking.

WHY NRR IS MORE IMPORTANT THAN CHURN RATE:
Churn rate tells you what's leaving. NRR tells you the net movement.
A company with 10% monthly churn but 15% expansion = NRR of 105% = net positive.
Focus on NRR, not just churn.

HOW TO IMPROVE NRR FROM BELOW 100%:
→ Add a usage-based upsell tier (pay for more of what you're already using)
→ Seat expansion for multi-user products (start with 1, grow to team)
→ Annual plan conversion (removes monthly churn risk)
→ Feature gating (lock advanced features in paid tier only)
→ Success milestones that trigger automatic upgrade prompts
```

### System 3: Cohort Retention Curves

```
RETENTION CURVE ANALYSIS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE PMF RETENTION TEST: Does your retention curve flatten?

WITHOUT PMF: Curve hits zero (every cohort eventually churns completely)
WITH PMF: Curve flattens at some percentage (a core group stays permanently)

RETENTION THRESHOLDS BY PRODUCT TYPE:

Daily-use tools (task management, email, analytics):
→ D7 retention: >40% = good
→ D30 retention: >25% = acceptable, >40% = strong PMF
→ D90 retention: >20% = PMF, >35% = strong

Weekly-use tools (reporting, CRM, content):
→ D30 retention: >40% = good
→ D90 retention: >30% = acceptable PMF
→ D180 retention: >25% = strong PMF

Monthly-use tools (billing, compliance, accounting):
→ D90 retention: >60% = expected (monthly use has high switching cost)
→ D365 retention: >50% = strong PMF

HOW TO BUILD A COHORT TABLE (even manually):
1. Group users by month of signup (Cohort: Jan, Feb, Mar...)
2. For each cohort, track what % are still active at D7, D30, D60, D90
3. Plot these curves. Watch for flattening.
4. The cohort with the highest flattening level = your PMF cohort.
   What changed between the low-retention and high-retention cohorts?
   → Product changes? ICP changes? Onboarding changes? Pricing changes?

FREE TOOLS:
→ PostHog: Free cohort analysis, event tracking
→ Mixpanel: Free up to 20M events/month
→ Manual: Google Sheets with COUNTIF formulas on your own exported data

THE BRIGHT SPOT METHOD (Kathy Sierra):
Find the top 20% of users by usage or longevity.
Interview 5-10 of them.
The common thread in WHY they stayed = your real value proposition.
Build your entire product and positioning around that thread.
```

### System 4: Organic Growth Rate

```
ORGANIC GROWTH MEASUREMENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PMF SIGNAL: >20% of new users come from referral/word-of-mouth (without a referral program)

WHY IT MATTERS:
Organic referral = people telling others because the product is so good they have to share.
This is impossible to fake. This is the highest-quality PMF signal.

HOW TO MEASURE:
→ Ask every new user: "How did you hear about us?" (simple text field or dropdown)
→ Options: Referral from friend/colleague / Organic search / Social media / Product Hunt /
           Paid ad / Content/blog / Other
→ Track monthly: what % is "Referral from friend/colleague"?

GROWTH SIGNAL BENCHMARKS:
<10% referral: Product not evangelizable. Good enough to keep, not good enough to share.
10-20% referral: Growing but not organic compounding. PMF partial.
>20% referral: Strong PMF signal. Each customer brings ~0.2 more customers.
>30% referral: Viral product. Acquisition cost approaches zero.

WHEN YOU DON'T HAVE REFERRAL TRACKING:
Use the "would you recommend" question from NPS.
NPS >50 = likely strong WOM. NPS <30 = unlikely referral behavior.
```

### System 5: The 40% Test (Alternative to Sean Ellis)

```
SIMPLIFIED PMF TEST (for early stages with <40 users):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

When you can't run a statistically valid Sean Ellis survey:

QUESTION: Ask each user directly:
"If we shut down tomorrow, would you be upset? Why / why not?"

"Extremely upset": Add to "Very Disappointed" bucket
"Would find an alternative, not urgent": Add to "Somewhat Disappointed"
"Could live without it": Not disappointed

If >40% of your conversations are "Extremely upset" + they describe SPECIFIC pain:
→ PMF signal. Continue.

If <40% are "Extremely upset":
→ Ask the "Extremely upset" ones: "Who else has this problem like you do?"
→ Their answer is your narrowed ICP.
→ Pivot messaging and feature development toward THAT segment.
→ Re-test in 30 days.

IMPORTANT: This requires honest conversation, not a survey.
Founders routinely over-count "enthusiastic" responses as PMF signals.
The test is not "did they say it was good?"
The test is: "Would they be genuinely upset if it disappeared, and can they name why?"
```

---

## THE PMF DIAGNOSTIC FRAMEWORK

### Finding the Real Problem When "It's Not Working"

```
PMF DIAGNOSTIC (fire when something feels off):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM 1 — No one signs up
→ NOT a PMF problem. Distribution/positioning problem.
→ Don't run PMF analysis yet.
→ Action: Fix the top-of-funnel. Run the validate.md flow first.

PROBLEM 2 — People sign up but don't activate (first action)
→ Onboarding problem (not PMF problem yet)
→ What is the "Aha moment" in your product?
→ Time-to-value: <30 seconds for consumer, <5 minutes for SMB SaaS
→ Action: Map the onboarding flow. Do 5 "copilot sessions" — sit with users and watch them.
          You will find the drop-off point in the first 2 sessions.

PROBLEM 3 — People activate but churn after 30 days
→ Habit formation failure (core PMF question)
→ Is there a natural recurrence trigger?
→ What is the user doing BETWEEN your product sessions?
→ Does the outcome they get justify returning?
→ Action: Exit interviews on every churned customer. Ask ONLY: "What made you stop using it?"
          Don't explain or defend. Just listen. Pattern emerges after 5-10 interviews.

PROBLEM 4 — People use it but won't pay
→ Value-price gap OR freemium trap OR wrong buyer (users ≠ buyers)
→ Freemium trap: free tier is too good — they have no reason to upgrade
→ Wrong buyer: the user has no budget authority; need the manager or finance team
→ Action: Van Westendorp survey (see finance.md). Identify what % of value they'd pay for.
          If <5% willing to pay any amount: value is too low.
          If >20% willing to pay: pricing or packaging issue, not value issue.

PROBLEM 5 — People pay but tell no one
→ "Politely useful" syndrome — good enough to keep, not good enough to evangelize
→ This is the hardest PMF problem to solve
→ Real PMF requires 10x value over alternative, not 10% better
→ Action: Find the use case where your product is 10x, not just better.
          Usually it's a specific workflow or user type.
          Reposition the entire product around that use case.

PROBLEM 6 — Early users love it, new users don't retain
→ ICP drift — you've expanded beyond the segment with the acute problem
→ Your early users had a specific context that made the product essential.
→ New users don't have that context.
→ Action: Profile your retained early users carefully.
          Re-narrow ICP to that exact profile.
          Stop trying to be for everyone.
```

---

## THE PREMATURE SCALING DETECTION SYSTEM

### Signs You're Scaling Before PMF

```
PREMATURE SCALING AUDIT (fire before any growth or acquisition recommendation):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 STOP: Do NOT scale if ANY of these are true:
□ Monthly churn >5% AND you're running paid acquisition
□ NPS <30 AND you're hiring a marketing team
□ D30 retention <25% AND you're investing in SEO content
□ Sean Ellis score <30% AND you're raising growth capital
□ You can't articulate WHY your best customers stay

🟡 CAUTION: Scale carefully if these are true:
□ Sean Ellis 30-40% (approaching but not confirmed PMF)
□ NRR 90-100% (flat, not growing)
□ D30 retention 25-35% (acceptable, not strong)
□ <50 paying customers (too early for statistical confidence)

🟢 PROCEED: Safe to scale if:
□ Sean Ellis ≥40% from ≥40 respondents
□ NRR ≥100% (customers expand)
□ D30 retention >35% AND flattening (not continuing to decline)
□ >20% of signups from WOM/referral without a referral program
□ You can describe your PMF customer in 1 sentence

RESEARCH CONTEXT:
Startup Genome found startups that scale prematurely are:
→ 2.3x more likely to fail than those who wait for PMF
→ Typically raise their burn rate by 3-5x before realizing they're not at PMF
→ Usually discover the problem 9-12 months after starting to scale

The insight: Premature scaling feels like growth. The metrics that reveal it are retention and NRR.
Revenue can grow while you're scaling yourself toward failure.
```

---

## THE PMF ACCELERATION PROTOCOL

### Once You Have 40+ Users: How to Find PMF Faster

```
PMF ACCELERATION (for early-stage founders with users but unclear PMF):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WEEK 1-2: THE LISTENING BLITZ
→ Schedule 15-minute calls with 10 most engaged users
→ ONLY ask: "Walk me through the last time you used [product]. What did you do? Why?"
→ DO NOT ask leading questions about features you want to build
→ Listen for: what problem they're solving, what they do when the product fails, who else they told

WEEK 2-4: THE BRIGHT SPOT ISOLATION
→ Identify the top 20% by engagement or longevity
→ What is statistically different about them?
  → Job title, company size, industry, use case, onboarding path, feature usage
→ Whatever is different = your PMF segment

WEEK 4-6: THE POSITIONING PIVOT
→ Rewrite your homepage for ONLY the bright spot segment
→ Change the example use case to their exact use case
→ Remove features prominently from marketing that the bright spot doesn't use
→ Measure: do new signups from this segment have better activation and retention?

WEEK 6-8: RE-TEST
→ Run Sean Ellis survey again with new cohort
→ If score improved: you're on the right track
→ If no improvement: repeat the listening blitz — you missed something

THE COPILOT SESSION (most underrated PMF technique):
Watch 5 users use your product in real time (screen share or Loom recording).
You will see:
→ Where they hesitate (hidden friction)
→ What they try that doesn't work (feature gap or UX failure)
→ What they DON'T do that you expected (feature that doesn't matter)
→ What they say out loud while doing it (their real mental model)

5 copilot sessions = more PMF insight than 50 survey responses.
```

---

## VERTICAL PMF vs HORIZONTAL PMF

```
ICP SCOPE CALIBRATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERTICAL PMF (recommended starting point):
→ Solve one problem for one industry perfectly
→ PMF signal is easier to find (less noise)
→ Reference customers validate each other
→ Sales cycle faster (everyone knows everyone in a vertical)
→ Example: Not "project management tool" but "project management for architecture firms"

HORIZONTAL PMF (harder to find and measure):
→ Solve one problem across many industries
→ PMF can exist in 1 vertical while failing in 3 others
→ Beware of "averaging" — your 30% average retention might be 55% in one segment
  and 8% in three others
→ You're at PMF when multiple verticals independently show the signal

HOW TO KNOW WHICH YOU HAVE:
→ If your best customers are all in the same industry: Vertical PMF (own it)
→ If your best customers are in 2+ different industries but same role: Role-based PMF
→ If randomly distributed: Horizontal → narrow aggressively

THE CHASM CROSSING SIGNAL (Geoffrey Moore):
Early adopters: tolerate rough edges for new capability
Early majority: need proven solutions, case studies, integrations
Signal you're ready to cross: >30% of new users come from referrals
from your early adopters TO their non-tech colleagues.
When this happens: you're crossing. Accelerate acquisition now.
```

---

## THE BHAGAVAD GITA ON PMF

### Nishkama Karma Applied to Validation

```
"Karmanye vadhikaraste ma phaleshu kadachana" — Gita 2.47
You have rights only to the action, not to its fruits.

APPLICATION TO PMF:
Your duty: Run the experiment correctly. Survey real users. Track real retention.
Not your duty: Guarantee the outcome will be PMF.

THE TRAP: Founders who are attached to achieving PMF start manipulating the measurement.
→ Survey only the most enthusiastic users
→ Discount churned users as "wrong fit"
→ Redefine PMF to match their current numbers

THE TRUTH: A clean negative PMF result is the second most valuable data point.
(First most valuable: a clean positive result.)
A clean negative tells you EXACTLY what hypothesis failed.
A manipulated positive sends you down 6 more months of the wrong path.

RUN THE EXPERIMENT CORRECTLY. Accept the result. Update the hypothesis. Try again.
This is the founder's dharma at the pre-PMF stage.
```

---

## Integration

PMF Engine connects to:
- `validate.md` → PMF gate is the post-launch equivalent of the pre-build validation gate
- `growth.md` → growth advice requires PMF gate check first (this skill auto-fires)
- `finance.md` → unit economics only matter post-PMF (LTV:CAC calculation is meaningless without retention)
- `morning.md` → PMF metrics added to daily brief once you have customers
- `soloos-core` MCP → `score_pmf()` tool runs quantitative scoring on your metrics
- `decide.md` → "should I scale?" decision always runs through this first

CLI: `soloos pmf --ellis 45 --nrr 108 --l30 38 --churn 2.1 --customers 55`

Log PMF milestones to `context/experiment-log.md`. A confirmed PMF date is one of the most important milestones to record — every future decision references it.
