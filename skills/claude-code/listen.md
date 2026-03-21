# Listen — Community Intelligence Pipeline

## Auto-Trigger (No Slash Command Needed)
Fires automatically when founder says: "find out what customers want", "where do customers hang out", "community research", "what subreddits", "monitoring [market]"

---


**Usage**: `/listen "[market or problem space]"`

**Examples**:
- `/listen "B2B SaaS onboarding"`
- `/listen "freelance developers"`
- `/listen "solo founders using AI tools"`
- `/listen "Shopify store owners"`

The Arvid Kahl discovery: **the best product ideas don't come from brainstorming — they emerge from
sustained listening inside specific communities**. This skill turns community conversations into
a structured intelligence feed: pain signals → product opportunities → content angles → outreach hooks.

---

## The Core Pattern (Arvid Kahl's "Embedded Entrepreneur")

From "The Embedded Entrepreneur" and "Zero to Sold":

> "Don't find a problem for your audience. Find an audience, and listen until the problem finds you."

The sequence that actually works:
1. **Identify** 3-5 communities where your ICP concentrates
2. **Listen** for recurring patterns (not one-off complaints)
3. **Classify** signals: pain / workaround / product request / competitor complaint
4. **Surface** the patterns with enough frequency to validate demand
5. **Engage** genuinely before ever mentioning a product
6. **Test** with content before testing with product

Most founders skip steps 1-5 and go straight to building. This skill makes 1-5 systematic.

---

## What This Skill Produces

### When run without context files:
A listening framework + community map + signal classification system for your space.

### When `context/customer-voice.md` is populated:
Cross-referenced analysis — "here's what you've already heard vs. what the community is saying."

### When run on a specific URL or post:
Deep analysis of a single community thread — pain extraction + competitive intelligence + hook mining.

---

## Phase 1: Community Mapping

First, identify where your ICP concentrates and what channels to monitor:

```
COMMUNITY MAP: [Market/Problem Space]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIER 1 — Primary Communities (highest signal density)
[Where they complain, ask for help, and share wins]
  Reddit: r/[subreddit] — [why it's high signal]
  Reddit: r/[subreddit] — [why it's high signal]
  Facebook: [group] — [why it's high signal]

TIER 2 — Secondary Communities (good volume, lower signal)
[Where they discuss tools, share content, and debate approaches]
  Slack: [community] — [why it's relevant]
  Discord: [community] — [why it's relevant]
  LinkedIn: [group or hashtag] — [why it's relevant]

TIER 3 — Signal Amplifiers (early warning system)
[Where trends start before they hit mainstream]
  HackerNews: [search terms to monitor]
  Twitter/X: [accounts, hashtags, or search terms]
  Indie Hackers: [forums or specific threads]

MONITORING CADENCE:
  Daily (5 min): [Tier 1 communities]
  Weekly (30 min): [Tier 2 communities]
  Monthly (1 hour): [Tier 3 — deeper dive]
```

---

## Phase 2: Signal Classification

Not all community content is equal. Train yourself to recognize signal types:

```
SIGNAL TYPES (ranked by product value):

🔴 HIGH VALUE — BUILD SIGNALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pattern: WORKFLOW HACK
"I do this manually every week: [boring, repetitive process]"
"My spreadsheet for [thing] has 47 tabs"
Signal: Automation or tool opportunity

Pattern: COBBLED SOLUTION
"I use [Tool A] + [Tool B] + [Tool C] together to do [thing]"
"We have a Zapier workflow for [thing] but it keeps breaking"
Signal: Integration gap or unified solution opportunity

Pattern: MONEY PAIN
"We're paying [$large amount] for [Tool] just to use [one feature]"
"The cheapest option that does [X] is [$ridiculous price]"
Signal: Pricing gap — cheaper alternative opportunity

Pattern: ENTERPRISE GATE
"[Tool] only has this in their enterprise plan at [$X/year]"
"We need [feature] but our company won't pay for [enterprise]"
Signal: Prosumer / SMB opportunity below enterprise tier

🟡 MEDIUM VALUE — CONTENT SIGNALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pattern: RECURRING QUESTION
Same question asked 3+ times in 30 days
Signal: Content gap — tutorial, guide, or explainer needed

Pattern: FRUSTRATED SEARCH
"I've googled this for 2 hours and can't find [X]"
Signal: SEO + content opportunity — someone would pay for clarity

Pattern: COMPARISON SHOPPING
"Has anyone compared [Tool A] vs [Tool B] for [use case]?"
Signal: Positioning opportunity — own this comparison

🟢 LOWER VALUE — VALIDATION SIGNALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pattern: WISHLIST
"I wish [tool] had [feature]"
"Someone should build [X]"
Note: Common but weak — interest ≠ payment intent

Pattern: COMMUNITY FRUSTRATION
"[Category] tools are all terrible because [reason]"
Note: Directional but vague — needs narrowing before building

Pattern: POSITIVE SIGNAL
"[Tool] saved us 3 hours/week on [task]"
Note: Validate what's working for clues on what's missing
```

---

## Phase 3: Signal Extraction Templates

### Reddit / Forum Thread Analysis

When reviewing a community thread or post:

```
THREAD ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: [URL or description]
Date: [date]
Votes/engagement: [number — proxy for how widely this resonates]

PAIN STATEMENT (in their exact words):
"[Quote — use their language, not yours]"

SIGNAL TYPE: [BUILD / CONTENT / VALIDATION from Phase 2]

ROOT CAUSE (one level deeper):
[Why does this pain exist? What's the upstream cause?]

CURRENT WORKAROUND:
[What are they doing instead? What are they tolerating?]

WILLINGNESS TO PAY SIGNAL:
[Any indication they'd pay for a solution? Mention of existing tools they use?]

PRODUCT HYPOTHESIS:
If someone built [X], it would [eliminate/reduce] this pain because [Y].

CONTENT ANGLE:
An article/thread titled "[X]" would attract this person because [Y].

OUTREACH HOOK:
"I saw you mentioned [their pain] in [community]. We're building [product] for exactly that —
would love your 5-minute take on whether we're solving it right."
```

### Batch Signal Capture (Weekly Review)

```
WEEKLY INTELLIGENCE REPORT: [Market]
Week of: [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOP SIGNALS THIS WEEK
─────────────────────
#1 Signal (times seen: [N])
Pain: "[quote in their words]"
Where: [community/source]
Pattern: [signal type]
Action: [build / content / validate / monitor]

#2 Signal (times seen: [N])
[same format]

#3 Signal (times seen: [N])
[same format]

EMERGING PATTERNS
─────────────────
[Pattern that appeared for the first time this week]
[Pattern that increased in frequency vs. last week]
[Pattern that decreased — what changed?]

COMPETITOR MENTIONS
──────────────────
[Tool mentioned]: [what people are saying, positive and negative]
[Tool mentioned]: [same]

CONTENT GAPS IDENTIFIED
───────────────────────
[Question asked repeatedly with no good answer]: [opportunity to create this content]

PEOPLE TO FOLLOW UP WITH
────────────────────────
[Username/handle]: "[what they said]" — [why worth engaging]
[Username/handle]: "[what they said]" — [why worth engaging]

THIS WEEK'S HIGHEST VALUE SIGNAL
─────────────────────────────────
Signal: [the one that, if true, changes your product roadmap]
Confidence: [Low/Medium/High — how often did you see this?]
Test: [cheapest way to validate this signal in 7 days]
```

---

## Phase 4: From Signal to Action

Every signal has a next action. The decision tree:

```
SIGNAL → ACTION DECISION TREE

If signal seen 1x:
  → Log it. Don't act yet.

If signal seen 3x from different people in 30 days:
  → Create content addressing it (post, article, tweet)
  → Track if the content gets engagement

If signal seen 5x AND people are paying for workarounds:
  → Run /validate on the product hypothesis
  → Engage directly with 3 of the people who expressed the pain

If signal seen 10x AND you can build an MVP in <2 weeks:
  → Run /validate → get 5 Tier 4+ commitments → build

If content you created gets 3x expected engagement:
  → Strong demand signal for related product
  → Build landing page before building product

ENGAGEMENT SEQUENCE (before you have a product):
Week 1: Comment helpfully in the thread. No product mention.
Week 2: Share a useful resource (your own or someone else's).
Week 3: DM the most vocal people asking if you can interview them.
Week 4: In the interview, ask: "If something made [pain] easier, what would it do?"
Week 5: Test positioning: "I'm building [X] for this — does this resonate?"
Week 6: /validate — get 5 commitments before writing code
```

---

## Phase 5: Content-as-Product-Validation

The underused hack: **publish content solving the problem before building the solution**.

Benefits:
- SEO: ranks for the problem's search terms
- Validation: engagement tells you how much people care
- Distribution: content brings the audience to you before you launch
- Trust: you're the expert before you're the vendor

```
CONTENT VALIDATION LADDER:

Level 1: Tweet or Reddit post about the problem
  Success signal: 10+ replies/comments
  What it tells you: Enough people recognize the problem

Level 2: Longer piece (blog post, newsletter, thread)
  Success signal: 100+ organic views, shares, or saves
  What it tells you: People will actively seek this content

Level 3: Free tool or resource solving a piece of the problem
  Success signal: 50+ email captures
  What it tells you: People are so interested they'll give you their email

Level 4: Waitlist for the full solution
  Success signal: 100+ signups, 20+ Tier 3+ commitments
  What it tells you: Demand is real enough to build

RULE: You don't have to build anything until Level 3 is validated.
The content itself is the product at levels 1-2.
```

---

## Full Output Format

```
INTELLIGENCE REPORT: [Market/Problem Space]
Date: [date]
════════════════════════════════════════════════════

COMMUNITY MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Tier 1, 2, 3 communities as outlined in Phase 1]

MONITORING PROTOCOL
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Daily (5 min): [Specific sources]
Weekly (30 min): [Specific sources]
Monthly: [Specific deeper dives]

TOP PAIN SIGNALS (ranked by frequency + intensity)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Pain] — Signal type: [BUILD/CONTENT/VALIDATE]
   Evidence: "[Direct quote]"
   Workaround: [What they're doing instead]
   Action: [Specific next step]

2. [Pain] — Signal type: [BUILD/CONTENT/VALIDATE]
   Evidence: "[Direct quote]"
   Workaround: [What they're doing instead]
   Action: [Specific next step]

3. [Pain] — Signal type: [BUILD/CONTENT/VALIDATE]
   [same format]

PRODUCT OPPORTUNITIES (sorted by confidence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 HIGH CONFIDENCE
[Opportunity]: [Why high confidence — frequency + money pain signals]
Next step: Run /validate on this

🟡 MEDIUM CONFIDENCE
[Opportunity]: [Why medium — seen but unclear willingness to pay]
Next step: Create content, measure engagement

🟢 WATCH
[Opportunity]: [Why to watch — early signal, not yet confirmed]
Next step: Monitor for 30 more days

CONTENT OPPORTUNITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Title]: "[Content idea that would attract the ICP]"
  Target pain: [which pain this addresses]
  Where to publish: [community, blog, Twitter]
  Validation test: [how to know if it resonates]

OUTREACH HOOKS (for warm ICP outreach)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"[Personalized hook referencing observed pain + relevant product or resource]"

PEOPLE TO ENGAGE (from this round of listening)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Username]: [Platform] — [What they said and why they're worth engaging]
[Username]: [Platform] — [same]

════════════════════════════════════════════════════
MONTHLY META-PATTERN
════════════════════════════════════════════════════
Consistent theme across all signals: [the thread that ties it together]
Signal that surprised me: [something unexpected]
Signal that confirmed hypothesis: [something that matched expectation]

STRATEGIC IMPLICATION:
[What this month of listening tells you about where the real opportunity is]
```

---

## Special Modes

### `/listen --thread "[URL or paste of a community thread]"`
Deep analysis of a single post or thread.
Returns: pain extraction, signal classification, 3 content angles, 1 product hypothesis, outreach template.

### `/listen --competitor "[competitor name or URL]"`
Competitive listening mode — what are people saying about a specific competitor?
Surfaces: complaints, workarounds, switching signals, feature gaps.
Returns: opportunity map relative to that competitor's weaknesses.

### `/listen --weekly`
Structured weekly review mode. Expects you to paste in notable community posts/quotes.
Returns: formatted weekly intelligence report + priority actions.

### `/listen --compare "[current customer voice file]"`
Cross-references your `context/customer-voice.md` against new community signals.
Identifies: gaps between what existing customers say and what the broader market says.
Surfaces: features your customers haven't asked for but the market needs.

---

## The Embedded Entrepreneur Principle

From Arvid Kahl's documented approach that led to FeedbackPanda (acquired):

> He spent 6 months inside teacher communities before writing a line of code.
> By the time he launched, he had:
> - The exact language teachers used to describe their pain
> - 20 teachers ready to test the first version
> - A pricing intuition built from watching what they paid for
> - Content that ranked for their search terms before the product shipped

The product was almost a formality. The audience was the asset.

This skill is the systematic version of that approach.

---

## Integration with SoloOS

1. Run `/listen` weekly → populate `context/customer-voice.md` with exact quotes
2. Use `/validate` when a signal hits 5+ sightings with pay signals
3. Use `/launch` when validated — the listening gives you their language for every launch asset
4. Use `/prospect` to engage the specific people who expressed the pain
5. Use `/morning` to track whether your listening is converting to pipeline
