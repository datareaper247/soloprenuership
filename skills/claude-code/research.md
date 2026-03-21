# Research — Market Intelligence for Solo Founders

## Auto-Trigger (No Slash Command Needed)
Fires automatically when founder says: "what's the market for X", "competitors doing X", "what do [customers] complain about", "is X market saturated"

---


**Usage**: `/research [type] "[topic]"`

**Examples**:
- `/research competitor "Fathom AI"`
- `/research market "B2B expense tracking under $100/mo"`
- `/research pain-mine "freelance developers"`
- `/research icp "VP of Engineering at Series A SaaS"`

This skill applies specific research frameworks — not generic analysis. Each type has a
defined methodology, output format, and quality bar. The output should make you feel
uncomfortable about assumptions you didn't know you were making.

---

## `competitor` — Competitor Intelligence

**The anti-pattern this prevents**: Building against a competitor you understand superficially.
Founders say "we're better than X" based on features. Customers switch based on switching cost,
trust, and workflow fit — not features.

**Framework**: The 5-Layer Competitor Autopsy

```
LAYER 1: What they sell (surface)
  - Core product claim (their tagline in their words)
  - Price points + tiers
  - Features they emphasize most prominently

LAYER 2: Who actually buys it (ICP reality)
  - Who reviews it on G2/Capterra? (title + company size signal)
  - Who complains in Reddit/communities? (tells you who it fails)
  - Job titles in their customer case studies

LAYER 3: Why people switch away (the gold)
  - Negative reviews: what's the complaint pattern?
  - "I moved from X to Y because..." posts in communities
  - Their Trustpilot 2-3 star reviews (more honest than 1-star)

LAYER 4: Their distribution moat
  - How do they acquire customers? (SEO, paid, community, outbound?)
  - What content ranks for them?
  - What partnerships or integrations drive them?

LAYER 5: Their Achilles heel
  - What do they consistently NOT fix despite repeated complaints?
  - What customer segment do they serve badly?
  - What's their strategic constraint? (enterprise focus = SMB gap, etc.)
```

**Output**:
```
COMPETITOR ANALYSIS: [Name]
════════════════════════════════════════════════════

LAYER 1: THE OFFER
  Positioning: "[their tagline in their words]"
  Price: [tiers + prices]
  Core claim: [what they say they do best]

LAYER 2: REAL ICP
  Who buys: [titles from reviews + case studies]
  Company size: [what size is actually using them]
  Mismatch: [who they claim to serve vs. who actually uses them]

LAYER 3: SWITCH-AWAY REASONS (complaint pattern)
  #1 complaint: "[exact quote pattern]" (seen N times)
  #2 complaint: "[exact quote pattern]" (seen N times)
  #3 complaint: "[exact quote pattern]" (seen N times)
  Most common churn trigger: [the thing that pushes people to leave]

LAYER 4: DISTRIBUTION
  Primary channel: [how they get customers]
  SEO strength: [what they rank for, estimated traffic]
  Content moat: [what's hard to replicate]

LAYER 5: THE GAP
  Who they serve badly: [specific segment]
  Recurring unfixed complaint: [what they won't fix because it conflicts with strategy]
  The opening: [1 sentence — how you could own what they abandon]

OPPORTUNITY ASSESSMENT
  Gap size: [Small / Medium / Large — basis]
  Difficulty to compete: [Low / Medium / High — why]
  Recommended angle: [how to position against them]
════════════════════════════════════════════════════
```

---

## `market` — Market Sizing with Solo Founder Lens

**The anti-pattern this prevents**: TAM theater — "$50B market" that doesn't tell you
whether anyone will pay $30/mo for your specific solution.

**Framework**: Bottom-up before top-down. Count real buyers, not market reports.

```
STEP 1: Count the buyers (bottom-up)
  How many companies/people fit this ICP description precisely?
  Where can you find them? (LinkedIn, job boards, communities)
  What's the realistic number of LinkedIn profiles with this combination?

STEP 2: What they pay today (market signal)
  What do they pay for the adjacent solution?
  What's the average spend per year in this category?
  Is there a line item for this in their budget, or would you be creating one?

STEP 3: Your realistic slice (SOM)
  If you captured 1% of reachable buyers in 12 months: how much MRR?
  Does that number justify building this?
  If 1% doesn't cover your burn, rethink the price, not the TAM.

STEP 4: Why now (timing)
  What changed in the last 18 months that makes this possible now?
  If nothing changed: why is this the right timing to enter?
```

**Output**:
```
MARKET ANALYSIS: [Market]
════════════════════════════════════════════════════

BUYER COUNT (bottom-up)
  ICP definition: [specific — not broad]
  LinkedIn proxy: [search term] = ~[N] profiles
  Realistic addressable: ~[N] after qualification
  Reachable in 12 months (solo, 10 outreach/day): ~[N]

MARKET SPEND
  Current solution category spend: ~$[X]/mo per buyer
  Your target price: $[X]/mo
  Price/current-spend ratio: [X%] — [high/medium/low switching cost]

YOUR REALISTIC OPPORTUNITY
  1% of reachable in 12 months = [N] customers × $[X]/mo = $[X] MRR
  Is this worth building? [Yes/No/Maybe — basis]

TIMING SIGNAL
  What changed: [specific 2026 change that creates this opportunity]
  Why this window: [what closes this window in 12-18 months]

CONFIDENCE: [High/Medium/Low]
  Strongest signal: [evidence you trust most]
  Biggest unknown: [what would make this analysis wrong]
════════════════════════════════════════════════════
```

---

## `pain-mine` — Community Pain Extraction

**The anti-pattern this prevents**: Building based on one Reddit post you happened to see.
Pain mining is systematic — signal through volume and specificity, not anecdote.

**Framework**: The Signal Classifier

```
For each community post or comment, classify:

🔴 BUILD SIGNAL:
  - Cobbled solution: "I use 3 tools to do what should be 1 tool"
  - Price signal: "I'm paying [$large amount] for [one feature]"
  - Manual work: "I do this by hand every [week/day]"
  - Repeating question: same question asked 3+ times in 30 days

🟡 CONTENT SIGNAL:
  - Unanswered question: lots of upvotes, no satisfying answer
  - Comparison shopping: "X vs Y for Z use case?" with no clear winner
  - Tutorial request: "How do I [thing]?" with no good resource

🟢 WATCH SIGNAL:
  - Wishlist: "I wish [tool] had [feature]"
  - Category frustration: "[Category] tools all suck"
  - Positive signal: what people love (tells you what to match)
```

**Output**:
```
PAIN MINING REPORT: [Community / Market]
════════════════════════════════════════════════════

TOP BUILD SIGNALS (seen 3+ times)
  #1: "[exact quote]" — seen N times — workaround: [what they do instead]
  #2: "[exact quote]" — seen N times — workaround: [what they do instead]
  #3: "[exact quote]" — seen N times — workaround: [what they do instead]

TOP CONTENT SIGNALS (unanswered demand)
  #1: "[question that gets upvotes but no answer]" — N upvotes
  #2: "[comparison question with no clear winner]" — N upvotes

COMPETITOR VULNERABILITIES MENTIONED
  [Tool] complaint: "[exact quote]" — N mentions
  [Tool] complaint: "[exact quote]" — N mentions

EXACT LANGUAGE TO USE
  They call the pain: "[their word]"
  They call the solution: "[their word]"
  They measure success by: "[their metric]"

HIGHEST CONFIDENCE OPPORTUNITY
  Pain: [one sentence — the strongest signal]
  Who: [the specific person expressing it most often]
  Why it's real: [frequency + workaround evidence + money mentioned]
  Next step: Run /validate on "[idea]"
════════════════════════════════════════════════════
```

---

## `icp` — ICP Definition from Evidence (Not Personas)

**The anti-pattern this prevents**: ICP documents that describe who you wish would buy,
not who actually buys.

**Framework**: Work backward from your best customers.

```
If you have customers:
  1. Who are your top 3 by LTV?
  2. Who referred other customers?
  3. Who activated fastest (time-to-value)?
  4. What do they have in common? (Title, company size, tech stack, context)

If you don't have customers yet:
  1. Who has this problem most acutely? (10x more than average)
  2. Who is already paying for an adjacent solution?
  3. Who would lose money / time if the problem went unsolved?
  4. Who can you find 20 of on LinkedIn in 30 minutes?
```

**Output**:
```
ICP DEFINITION: [Product]
════════════════════════════════════════════════════

PRIMARY ICP (your best customer type)
  Title: [specific — not "manager or director"]
  Company: [size + stage + industry]
  Tech context: [what tools they already use — signals maturity]
  Buying trigger: [what event creates urgency — not a persona, an event]
  Budget authority: [do they control the budget or need approval?]
  Alternatives they use now: [what they're currently paying for]

HOW TO FIND 20 IN 30 MINUTES
  LinkedIn search: [exact search string]
  Community: [subreddit or Slack where they concentrate]
  Signal: [job posting keyword, tech stack signal, or event trigger]

ANTI-ICP (looks like a fit but isn't)
  Who to avoid: [type that costs CAC but churns]
  Why they look like a fit: [surface similarity]
  Why they're not: [the thing that causes churn or non-payment]

VALIDATION QUESTION
  Ask this to confirm ICP fit in the first call:
  "[One question that separates ICP from non-ICP buyers]"
════════════════════════════════════════════════════
```

---

## Quality Standard

Every `/research` output must pass this test:

**Did this surface something the founder didn't already know?**

If the output only confirms what the founder already believed, the research failed.
The value of research is uncomfortable data — competitor gaps you didn't know existed,
pain language you hadn't heard, ICP filters that cut your market in half (and save you
from spending 12 months selling to the wrong people).

If you find yourself writing research that just validates the founder's existing view,
state explicitly: "This confirms your hypothesis — confidence: high."
If you find contrary evidence, lead with it: "⚠️ Finding: [contrary evidence]."
