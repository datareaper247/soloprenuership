# Research — Market Intelligence & Opportunity Analysis

**Usage**: `/research [type] "[topic or product]"`

Produces structured, actionable market intelligence using systematic research methodologies. Every output includes confidence levels, evidence citations, and opportunity scorecards.

---

## Research Types

### `market` — Full Market Analysis
**Usage**: `/research market "[market or industry]"`

#### Methodology
1. **Define the market**: Precise definition of the addressable market, excluding adjacent markets
2. **Size the opportunity**: Bottom-up AND top-down TAM/SAM/SOM calculation
3. **Map the structure**: Identify segments, geographic distribution, buyer types
4. **Identify dynamics**: Growth drivers, headwinds, regulatory factors
5. **Assess timing**: Why now? What's changing? What enables new entrants?

#### Research Sources (in priority order)
- Industry analyst reports (Gartner, Forrester, IDC — search for publicly available data)
- VC investment patterns (funding rounds as market validation signal)
- Public company filings (10-K revenue segments for comparable markets)
- Job posting data (hiring trends = market investment signals)
- Search trend data (Google Trends for consumer interest trajectory)
- Reddit/HN community activity (qualitative signal of practitioner interest)

#### Output Format
```
MARKET ANALYSIS: [MARKET NAME]
==============================
Report Date: [date]
Confidence Level: [High/Medium/Low] — [reason]

MARKET DEFINITION
- Core market: [precise definition]
- Excluded adjacent markets: [list]
- Primary buyers: [who pays]
- End users: [who uses]

MARKET SIZING
- TAM (Total Addressable Market): $Xb
  Method: [bottom-up/top-down/triangulation]
  Assumptions: [key assumptions]
- SAM (Serviceable Addressable Market): $Xm
  Rationale: [why this subset]
- SOM (Serviceable Obtainable Market, Year 3): $Xm
  Rationale: [realistic capture rate]

MARKET STRUCTURE
- Segments: [segment names with relative sizes]
- Geography: [where is money concentrated]
- Buyer type distribution: [SMB/Mid/Enterprise %]
- Sales cycle: [typical length and complexity]

GROWTH DYNAMICS
- Historical growth: X% CAGR (last X years)
- Projected growth: X% CAGR (next X years)
- Primary growth drivers: [3 bullets with evidence]
- Headwinds: [2 bullets]
- Regulatory factors: [if relevant]

TIMING ASSESSMENT
- Why is this market interesting NOW: [1 paragraph]
- Enabling factors (technology, regulation, behavior): [list]
- Window of opportunity: [assessment]

MARKET ATTRACTIVENESS SCORECARD
| Dimension | Score (1-5) | Evidence |
|-----------|-------------|----------|
| Market size | | |
| Growth rate | | |
| Fragmentation | | |
| Buyer pain intensity | | |
| Willingness to pay | | |
| Competitive intensity | | |
| Regulatory risk | | |
| OVERALL | /35 | |

STRATEGIC IMPLICATIONS
[2-3 paragraph synthesis of what this means for a new entrant]

RECOMMENDED NEXT STEPS
1. [Action]
2. [Action]
3. [Action]
```

---

### `competitor` — Deep Competitor Analysis
**Usage**: `/research competitor "[company name]"`

#### Methodology
1. **Public information sweep**: Website, blog, docs, pricing page, job listings
2. **Product intelligence**: Feature set from docs/screenshots/reviews
3. **Business intelligence**: Funding, team size, revenue signals, customers
4. **Marketing intelligence**: SEO profile, content strategy, acquisition channels
5. **Customer intelligence**: G2/Capterra/Trustpilot reviews, Reddit/HN mentions
6. **Strategic intelligence**: Recent pivots, announcements, executive messaging

#### Research Sources
- Company website (pricing, features, positioning, blog)
- LinkedIn (team size, hiring velocity, key people)
- Crunchbase/PitchBook (funding, investors)
- G2/Capterra/Trustpilot (customer reviews — especially negative ones)
- Reddit searches: "[company name] reddit" — look for honest community discussion
- HN searches: look for launch posts, discussions, criticisms
- Twitter/X: customer complaints, praise, comparisons
- Job postings: reveals investment areas, tech stack, growth plans
- GitHub: if open source, activity level, community health

#### Output Format
```
COMPETITOR ANALYSIS: [COMPANY NAME]
====================================
Analysis Date: [date]
Data Quality: [Strong/Adequate/Limited]

COMPANY SNAPSHOT
- Founded: [year]
- HQ: [location]
- Team size: ~X employees (LinkedIn signal)
- Funding: $Xm total | Last round: [Series, amount, date, investors]
- Revenue estimate: $X ARR [source/confidence]
- Key customers: [logos if known]
- Website: [URL]

PRODUCT
- Core offering: [1-2 sentence description]
- Key features: [bulleted list]
- Notable capabilities: [what they do uniquely well]
- Notable gaps: [what's missing or weak]
- Tech stack (if determinable): [list]
- Integrations: [key integrations]

PRICING
[Current pricing tiers — name, price, what's included]
[Pricing strategy assessment: penetration/value/skimming/freemium]
[Pricing gaps or opportunities]

POSITIONING
- Self-description: "[quote from their website]"
- Target customer: [ICP as they define it]
- Key messages: [3 bullets]
- Brand personality: [adjectives]

MARKETING & ACQUISITION
- Primary channels: [list with evidence]
- Content strategy: [volume, topics, quality]
- SEO profile: [domain authority, estimated traffic, top keywords]
- Paid advertising: [evidence of paid channels]
- Community presence: [where they're active]

CUSTOMER SENTIMENT
Positive themes (from reviews):
- [theme 1]: "[example quote]"
- [theme 2]: "[example quote]"

Negative themes (from reviews):
- [theme 1]: "[example quote]"  ← THESE ARE YOUR OPPORTUNITIES
- [theme 2]: "[example quote]"

HN/Reddit sentiment: [summary]

STRATEGIC ASSESSMENT
- Momentum: [Growing/Stable/Declining] — evidence
- Strategic direction: [where they seem to be heading]
- Recent pivots: [any notable changes]
- Key executives: [names, backgrounds, LinkedIn]

WIN/LOSS PROFILE
- When you'd beat them: [specific conditions]
- When they'd beat you: [honest assessment]
- Key differentiators (yours): [list]

THREAT ASSESSMENT
Level: [Critical/High/Medium/Low]
Rationale: [1 paragraph]

BATTLE CARD SUMMARY
When prospect mentions them: [your go-to response]
Their top objection against you: [objection + your counter]
```

---

### `opportunity` — Opportunity Validation & Scoring
**Usage**: `/research opportunity "[product idea or problem space]"`

#### Methodology
Framework: **PRISM** — Problem, Reach, Income, Solution, Market

1. **Problem validation**: Is this a real, recurring, painful problem?
2. **Reach assessment**: How many people have this problem?
3. **Income potential**: Would people pay? How much?
4. **Solution landscape**: What exists? What's the gap?
5. **Market dynamics**: Is this market growing? Timing right?

#### Research Process
1. Search Reddit for the problem: "[problem] site:reddit.com" — count threads, upvotes
2. Search HN: "[problem] site:news.ycombinator.com"
3. Google Trends: trend line for problem keywords
4. Product Hunt: have similar products launched? With what reception?
5. App stores: are there apps trying to solve this? Reviews?
6. Job postings: are companies hiring for roles related to this problem?

#### Output Format
```
OPPORTUNITY VALIDATION: [IDEA NAME]
=====================================
Validation Date: [date]
Overall Score: X/50
Recommendation: [Pursue/Validate Further/Pass]

PROBLEM DEFINITION
- Core problem: [1 sentence — specific, not broad]
- Who has it: [specific persona]
- When does it occur: [trigger/context]
- Current workarounds: [how people cope today]
- Cost of the problem: [time, money, frustration]

EVIDENCE OF PROBLEM
- Reddit signals: [X threads, avg Y upvotes] "[best quote found]"
- HN signals: [evidence]
- Google Trends: [trajectory — rising/flat/declining]
- Other signals: [any other evidence]

REACH ASSESSMENT
- Total universe with problem: [estimate with method]
- Reachable segment: [realistic target]
- Evidence of search demand: [keywords, volumes]

INCOME POTENTIAL
- Current spend on problem: [what people pay for workarounds]
- Willingness to pay signals: [evidence from reviews, surveys, similar products]
- Pricing hypothesis: [$/mo or one-time]
- Revenue potential (Year 3, conservative): [calculation]

SOLUTION LANDSCAPE
| Solution | What they do | Weakness | Our angle |
|----------|-------------|----------|-----------|
| [Competitor 1] | | | |
| [DIY/manual] | | | |
| [Adjacent tool] | | | |

DIFFERENTIATION ANGLE
[Why a new solution could win — specific insight, not generic]

OPPORTUNITY SCORECARD
| Dimension | Score (1-5) | Evidence |
|-----------|-------------|----------|
| Problem pain intensity | | |
| Problem frequency | | |
| Market size | | |
| Competition level | | |
| Willingness to pay | | |
| Ease of reaching buyers | | |
| Timing / trend | | |
| Founder fit (if known) | | |
| Defensibility | | |
| MVP buildability | | |
| TOTAL | /50 | |

VALIDATION EXPERIMENTS (if score 30+)
1. [Cheapest way to validate willingness to pay]
2. [Fastest way to get 20 customer interviews]
3. [Minimum viable landing page test]

RISKS
1. [Biggest risk] — Mitigation: [how to de-risk]
2. [Second risk] — Mitigation: [how to de-risk]

RECOMMENDATION
[1 paragraph with specific next step]
```

---

### `pain-mine` — Customer Pain Point Discovery
**Usage**: `/research pain-mine "[industry or persona]"`

Systematically mines online sources for authentic customer pain points.

#### Mining Sources
1. **Reddit**: r/[industry], r/[job title], r/[software name] — search "hate", "wish", "frustrated", "broken", "why doesn't", "anyone else"
2. **HN**: Search Ask HN for "what's broken in [industry]", complaints about category
3. **G2/Capterra**: 1-3 star reviews of incumbent software (gold mine)
4. **Twitter/X**: "@[competitor] doesn't", "I hate [tool]"
5. **App Store**: 1-2 star reviews
6. **LinkedIn**: Complaints from practitioners in their industry

#### Output Format
```
PAIN POINT DISCOVERY: [INDUSTRY/PERSONA]
=========================================
Mining Date: [date]
Sources Searched: [list]
Total Pain Points Found: X

PERSONA DEFINITION
- Role/title: [who was sampled]
- Context: [when/why they experience these pains]

PAIN POINT CLUSTERS

CLUSTER 1: [Theme Name] — Frequency: X mentions — Intensity: High/Med/Low
Description: [what the pain is]
Evidence quotes:
- "[exact quote from a real post]" — source: [subreddit/site]
- "[exact quote]" — source: [site]
Product hypothesis: [what would fix this]

CLUSTER 2: [Theme Name] ...
[repeat for each cluster]

PAIN PRIORITY MATRIX
| Pain | Frequency | Intensity | Addressability | Priority |
|------|-----------|-----------|----------------|----------|
| ... | High/Med/Low | High/Med/Low | High/Med/Low | 1-5 |

HIGHEST VALUE PAIN POINTS (top 3)
For each:
- Pain: [specific description]
- Evidence: [number of mentions, best quote]
- Current solutions (and why they fail): [list]
- Product opportunity: [what to build]
- Monetization angle: [how to charge]

VERBATIM GOLD (best quotes for landing page/messaging)
1. "[quote]" — [source]
2. "[quote]" — [source]
3. "[quote]" — [source]
```

---

### `trends` — Trend Analysis & Signal Detection
**Usage**: `/research trends "[domain or technology]"`

#### Methodology
1. **Leading indicators**: Venture funding, job postings, conference talks
2. **Practitioner signals**: What are experts discussing on HN, Twitter, LinkedIn?
3. **Consumer signals**: Google Trends, app store categories, social media
4. **Technology readiness**: What tech is becoming "good enough" to enable new products?
5. **Regulatory signals**: New laws, compliance requirements, enforcement actions

#### Output Format
```
TREND ANALYSIS: [DOMAIN]
=========================
Report Date: [date]
Signal Strength: [Strong/Moderate/Early]

MACRO TRENDS (2-5 year horizon)
1. [Trend name]: [description + evidence]
   Implication for products: [so what]

EMERGING TRENDS (6-18 month horizon)
1. [Trend name]: [description + evidence]
   Early signals: [leading indicators seen]
   Who's investing: [VCs/companies]
   Implication: [product/market opportunity]

COUNTER-TRENDS (things going away)
1. [Declining pattern]: [evidence of decline]
   Creates space for: [opportunity]

TECHNOLOGY ENABLERS
[Technologies reaching "good enough" that enable new products]

WEAK SIGNALS (unconfirmed, worth watching)
1. [Signal]: [where observed, what it might mean]

OPPORTUNITY WINDOWS
| Opportunity | Trend driver | Window | Confidence |
|-------------|-------------|--------|------------|
| ... | | 6mo/1yr/3yr | High/Med/Low |

WATCHLIST
Things to monitor monthly: [list with sources]
```

---

### `customer-profile` — Ideal Customer Profile Development
**Usage**: `/research customer-profile "[product or market]"`

#### Methodology
1. **Behavioral signals**: What do good customers do in the product? (if data available)
2. **Firmographic patterns**: Company size, industry, geography, funding stage
3. **Pain intensity mapping**: Which segment hurts most and pays most
4. **Buying behavior**: How do they buy? Who's involved? Budget source?
5. **Community research**: Where do they hang out? What do they read? Who do they trust?

#### Output Format
```
CUSTOMER PROFILE RESEARCH: [PRODUCT/MARKET]
=============================================

PRIMARY ICP (Ideal Customer Profile)

FIRMOGRAPHICS
- Company size: [employee count range]
- Industry/vertical: [specific, not broad]
- Geography: [markets]
- Stage: [startup/SMB/mid-market/enterprise]
- Revenue: [$X - $Y ARR range]
- Tech stack signals: [tools they use]

PSYCHOGRAPHICS
- Role: [title(s)]
- Seniority: [IC/manager/director/VP/C-suite]
- Primary motivation: [what drives decisions]
- Risk tolerance: [early adopter/majority/laggard]
- Buys based on: [ROI/peers/features/support]

PAIN PROFILE
- Primary pain (functional): [specific workflow pain]
- Secondary pain (emotional): [frustration/anxiety]
- Cost of problem: [time/money/risk quantified]
- Urgency trigger: [what makes them act NOW]

BUYING BEHAVIOR
- Discovery: [how they find solutions]
- Evaluation: [what they compare, how long]
- Decision: [who approves, what they need to see]
- Budget: [source, cycle, typical size]
- Preferred purchase: [trial/demo/self-serve/sales-led]

CONTENT & COMMUNITY
- Where they learn: [publications, podcasts, newsletters]
- Where they hang out: [communities, subreddits, Slack groups]
- Trusted voices: [influencers, analysts, peers]
- Conference attendance: [events they go to]

QUALIFICATION SIGNALS (for sales/marketing targeting)
Positive signals: [things that indicate good fit]
Negative signals: [disqualifiers]

ICP SEGMENTS (if multiple)
Segment A: [name] — [difference from primary]
Segment B: [name] — [difference from primary]

MESSAGING IMPLICATIONS
- Lead with: [what they care about most]
- Avoid: [what turns them off]
- Social proof they want: [what kind of reference]
- Objections to prepare for: [list]
```

---

## Research Quality Standards

### Confidence Levels
- **High**: Multiple independent sources confirm the finding; data is recent (< 12 months)
- **Medium**: 1-2 sources, data may be 1-2 years old, some assumptions required
- **Low**: Inference from indirect signals, significant uncertainty, validate before acting

### Citation Standards
Always attribute findings to their source type (e.g., "Reddit signal", "G2 review", "Crunchbase data") even when the exact URL isn't accessible. Never present guesses as research findings — label them as hypotheses.

### What Good Research Looks Like
- Specific, not generic (quantified where possible)
- Evidence-based (every claim supported)
- Actionable (tells you what to DO next)
- Honest about gaps (states what's unknown)
- Opinionated (gives a clear recommendation, not just a data dump)
