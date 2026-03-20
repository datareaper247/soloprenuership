# Sales — Solo Founder Sales Playbook

**Usage**: `/sales [command] "[context or target]"`

---

## The Solo Founder Sales Hierarchy

Sales motions that work depend entirely on ACV and stage. Wrong motion = burnout with no revenue.

```
ACV < $100/mo (self-serve): You are NOT the sales process.
  Product, onboarding, and trial experience close deals.
  Founder time: write better landing page copy, fix onboarding friction.
  Outbound ROI: negative. Time better spent on content and product.

ACV $100-500/mo (founder-led): You are the sales process.
  Cold outreach + founder discovery calls close deals.
  Target: 10 outreach messages/day, 1-2 calls/week.
  Close 20-30% of demos. If lower: qualification problem.

ACV $500-2K/mo (consultative): Value needs to be demonstrated.
  Outbound + inbound + free trial/demo environment.
  Discovery call is the most valuable hour you spend.
  Close 15-25% with proper discovery.

ACV >$2K/mo (enterprise motion): Not a solo play until you have process.
  Needs champion, multiple stakeholders, formal evaluation.
  Don't attempt this without a proven sales playbook from the lower tiers.
```

⚠️ Before running /sales: what's your target ACV? The commands below are calibrated to $100-500/mo founder-led sales. If your ACV is <$100, the recommendation may be "don't do outbound."

---

## The Discovery Call Framework (Most Valuable 30 Minutes)

Discovery done right is a research call, not a pitch. The founder who discovers
best closes best — because they understand the problem deeper than the prospect.

**The 5 discovery questions** (in this order):

```
Q1: "What made you take this call today?"
→ Surfaces the trigger event. This is the real reason, not the stated reason.

Q2: "Tell me about the last time [problem] was really frustrating. What happened?"
→ Gets them to tell their story. Do NOT interrupt. The story contains your pitch.

Q3: "What have you tried to solve it?"
→ Surfaces alternatives. Tells you what they're comparing you to.
→ Follow-up: "Why didn't [previous solution] work?"

Q4: "If this problem was solved, what changes for you specifically?"
→ Surfaces the emotional and business outcome. This becomes your closing language.

Q5: "What would make you say yes to solving this?"
→ They give you their own close criteria. Use their words in your proposal.
```

**After the call, within 24 hours**:
Write a 2-paragraph email:
- Para 1: "Based on what you told me, your situation is [their words]."
- Para 2: "Here's how [product] solves [their specific version of the problem]."

Do not send a proposal with features. Send back their problem in their language.

---

## Commands

### `outreach` — Cold Outreach Message
**Usage**: `/sales outreach "[prospect name + company + context]"`

Produces 3 variants of a cold email or LinkedIn message using different frameworks.

#### Framework 1: PAS (Problem → Agitate → Solution)
Best for: Pain-point-driven outreach when you know the problem
```
[SUBJECT: 1 line — specific to their situation, not generic]

[Identify the SPECIFIC problem they likely have — based on their role/company]

[Agitate: what does that problem cost them? Risk? Missed opportunity?]

[Bridge: "We help [specific persona] solve [specific problem] by [mechanism]"]

[Social proof: "Companies like [similar customer] went from X to Y"]

[CTA: one low-friction ask — not "hop on a 30-minute call" — try "worth a 10-minute chat?"]

[Name]
[Title] @ [Company]
```

#### Framework 2: AIDA (Attention → Interest → Desire → Action)
Best for: Outreach where you lead with value or insight, not problem
```
[SUBJECT: Curiosity-based or insight-based]

[Attention: Hook — share a data point, insight, or observation specific to THEM]

[Interest: Build on that insight — why does it matter for them]

[Desire: Connect to what we do — but keep it light, not a pitch]

[Action: Single soft CTA]
```

#### Framework 3: Relevant Reference
Best for: When you have a genuine connection point (mutual contact, trigger event, their content)
```
[SUBJECT: Mention the connection point]

[Reference: Be specific — "saw your post about X" / "noticed you just hired a VP Sales"]

[Connect to pain: "Companies going through [trigger] often find [specific challenge]"]

[We help with: brief, non-spammy mention]

[Social proof or proof of relevance]

[Soft CTA]
```

#### Output Format
```
COLD OUTREACH VARIANTS: [Prospect Name] @ [Company]
====================================================
Research Summary:
- Role: [their title and responsibilities]
- Company: [size, industry, recent news if any]
- Trigger event: [anything notable — funding, hiring, launch, article]
- Pain hypothesis: [what pain they likely have based on role/context]

VARIANT 1 — PAS Framework
Subject: [subject]
[body]

VARIANT 2 — AIDA Framework
Subject: [subject]
[body]

VARIANT 3 — Relevant Reference
Subject: [subject]
[body]

RECOMMENDED VARIANT: [which one and why]
SEND CHANNEL: [Email / LinkedIn / Both in sequence]
FOLLOW-UP TIMING: [when to follow up if no response]
```

---

### `sequence` — Multi-Touch Outbound Sequence
**Usage**: `/sales sequence "[persona and ICP description]"`

Full multi-touch outbound sequence across email and LinkedIn.

#### Sequence Design Principles
- First touch: Lowest ask (don't ask for time immediately)
- Each touch: Different angle, new value, not just "just following up"
- Space: 3-4 days between touches
- Break-up email: Last touch — give them permission to say no (high response rate)
- LinkedIn touches: Connection request + message = 2 touches without email

#### Output Format
```
OUTBOUND SEQUENCE: [Persona Name]
==================================
Total touches: X over Y days
Goal: Book discovery call / Demo / Response

TOUCH 1 — Day 1 — Email
Goal: Create curiosity, not pitch
Subject: [subject]
[body — PAS or AIDA]
CTA: [Soft — "worth a chat?"]

TOUCH 2 — Day 4 — LinkedIn Connection Request
Message: [Connection note — 1-2 sentences, no pitch]
Goal: Warm up before next email

TOUCH 3 — Day 7 — Email
Goal: Share value (not follow up — add something new)
Subject: [different angle or resource share]
[body — share insight, case study, or relevant content]
CTA: [Slightly more direct — "15 min this week?"]

TOUCH 4 — Day 10 — LinkedIn Message (post-connection)
Goal: Engage after they accepted connection
[body — comment on their content or share something relevant]

TOUCH 5 — Day 14 — Email
Goal: Different angle — ROI or urgency
Subject: [ROI or time-bound angle]
[body]
CTA: [More direct CTA]

TOUCH 6 — Day 21 — Break-up Email
Goal: Final touch — give permission to decline
Subject: [Something like "Should I stop reaching out?"]
[body — gracious, not desperate, permission to say no]
CTA: [Easy yes or no CTA]

---
SEQUENCE TRACKING
- Track: Opens, clicks, replies per touch
- A/B test: Touch 1 subject line (2 variants)
- Response triggers: [If they open 3x without replying = call trigger]
- Positive response → move to: [discovery call agenda template]
```

---

### `qualify` — Lead Qualification Framework
**Usage**: `/sales qualify "[prospect description or call context]"`

Qualification scoring using MEDDIC, BANT, or SPICED depending on sales context.

#### MEDDIC Framework (Complex B2B Sales)
- **M**etrics: What are the measurable outcomes they need?
- **E**conomic Buyer: Who controls the budget and has final say?
- **D**ecision Criteria: What criteria will they use to make the decision?
- **D**ecision Process: What's the buying process, steps, and timeline?
- **I**dentify Pain: What's the confirmed, quantified pain?
- **C**hampion: Who internally is advocating for our solution?

#### BANT Framework (SMB/Transactional Sales)
- **B**udget: Do they have budget? How much?
- **A**uthority: Can they make the decision or do they need approval?
- **N**eed: Is there a confirmed, urgent need?
- **T**imeline: When do they need to solve this?

#### SPICED Framework (Modern SaaS)
- **S**ituation: Current state — context and environment
- **P**ain: Specific pain points and their business impact
- **I**mpact: Quantified cost of the problem
- **C**ritical Event: What drives urgency? What happens if they don't solve it?
- **D**ecision: Who, how, when they'll decide

#### Output Format
```
QUALIFICATION ASSESSMENT: [Prospect Name] @ [Company]
======================================================
Framework used: [MEDDIC / BANT / SPICED]
Qualification Score: X/10
Recommendation: [Advance / Nurture / Disqualify]

MEDDIC SCORECARD
| Dimension | Confirmed | Notes | Gap |
|-----------|-----------|-------|-----|
| Metrics | ✅/⚠️/❌ | [what we know] | [what to find out] |
| Economic Buyer | | | |
| Decision Criteria | | | |
| Decision Process | | | |
| Identified Pain | | | |
| Champion | | | |

CONFIRMED PAIN
- Primary pain: [specific, in their words if possible]
- Business impact: [$X/mo or X hours/week — quantified]
- Urgency: [why now — critical event or deadline]

BUDGET
- Budget confirmed: [Yes / No / Unknown]
- Budget range: [$X - $Y or "matches our pricing"]
- Budget source: [what budget line]
- Approval required: [who and process]

DECISION PROCESS
- Timeline: [when they want to make a decision]
- Stakeholders: [who else is involved]
- Steps remaining: [list]
- Evaluation criteria: [how they'll decide]

CHAMPION
- Name: [if known]
- Motivation: [why do they want this]
- Influence level: [High/Med/Low]
- Coach status: [do they share internal info]

COMPETITIVE SITUATION
- Current solution: [what they're using today]
- Alternatives considering: [competitors in the deal]
- Our position: [how we're positioned vs alternatives]

NEXT STEPS
1. [Specific action] — Owner: [rep or prospect] — By: [date]
2. ...

DEAL RISK FACTORS
1. [Risk] — Mitigation: [how to address]
```

---

### `proposal` — Sales Proposal
**Usage**: `/sales proposal "[deal context: company, pain, proposed solution, price]"`

#### Proposal Structure
A winning proposal is organized around THEIR problem, not YOUR product.

```
SALES PROPOSAL
==============
Prepared for: [Contact Name], [Title], [Company]
Prepared by: [Rep Name], [Title], [Your Company]
Date: [date]
Valid until: [date]

---

EXECUTIVE SUMMARY
[For the Economic Buyer — 1 page max]

[Company Name] is experiencing [specific problem] which is costing approximately
[$X per month / X hours per week / X% [metric]] based on our conversations.

[Your Company] proposes to solve this through [brief solution description],
which [similar customer] used to achieve [specific result] in [timeframe].

Proposed investment: $[X]/month (or $X total)
Expected ROI: [specific, calculated if possible]
Time to value: [how long until they see results]

[Signature line for approval]

---

UNDERSTANDING YOUR SITUATION
[Demonstrate you listened — mirror back their pain and goals]

Current State:
- [Pain point 1 — in their words]
- [Pain point 2]
- [Quantified cost of the problem]

Desired State:
- [What success looks like to them]
- [Metrics that would matter to them]
- [Timeline for results]

---

PROPOSED SOLUTION
[Not a feature list — a narrative about HOW you solve THEIR problem]

[Phase 1: Quick Win]
- What we do: [specific actions]
- Timeline: [X weeks]
- Result: [specific deliverable or outcome]

[Phase 2: Core Implementation]
- What we do: [actions]
- Timeline: [X weeks/months]
- Result: [outcome]

[Phase 3: Ongoing Value]
- What ongoing looks like
- How we ensure continued success

---

INVESTMENT & OPTIONS

[OPTION A — Recommended: Name]
[What's included]
Investment: $X/month (or $X)
Best for: [who this is right for]

[OPTION B — Accelerated: Name]
[What's included — more scope]
Investment: $X/month
Best for: [who this is right for]

[Payment terms, contract length, cancellation policy]

---

PROOF THEY SHOULD BELIEVE YOU

Case Study: [Similar company]
[2-3 sentences: who they are, what their problem was, what result we delivered]

Customer Quote:
"[Specific result-focused testimonial]" — [Name, Title, Company]

Other customers in their space: [logo list or names]

---

IMPLEMENTATION & SUPPORT
- Onboarding: [what happens in first X days]
- Dedicated support: [what level of support included]
- Success metrics: [what we track together]
- QBR cadence: [how often we review]

---

NEXT STEPS
1. [You review this proposal — by date]
2. [Call to address questions — propose time]
3. [Contract signature — target date]
4. [Kickoff — target date]

To proceed: [signature block or DocuSign link]
Questions? [contact info]
```

---

### `crm-update` — CRM Deal Note & Next Step
**Usage**: `/sales crm-update "[call summary or meeting context]"`

Produces a structured CRM note that can be copy-pasted into Salesforce, HubSpot, or any CRM.

#### Output Format
```
CRM UPDATE: [Company] — [Deal Stage]
======================================
Date: [date]
Rep: [name]
Meeting type: [Discovery / Demo / POV / Negotiation / Renewal]
Attendees: [names and titles]

SUMMARY (2-3 sentences for exec visibility)
[Concise summary of where the deal stands and what happened]

PAIN CONFIRMED
- [Pain 1]: [specifics, in their words if possible]
- [Pain 2]: [specifics]
- Quantified impact: [$X / X hours / X% metric]

NEXT STEPS (MUST be mutual, specific, time-bound)
| Action | Owner | Due Date |
|--------|-------|----------|
| [Action] | [Rep / Prospect Name] | [Date] |
| [Action] | | |

MEDDIC UPDATE
- Economic Buyer: [confirmed / identified as: name/title / unknown]
- Champion: [name, engagement level]
- Decision Timeline: [confirmed / moved / unknown]
- Competitors: [in deal / eliminated]
- Budget: [confirmed / range / TBD]

RISKS
1. [Risk] — Plan: [mitigation]

DEAL HEALTH: [🟢 On Track / 🟡 At Risk / 🔴 Stalled]
Forecast Category: [Commit / Best Case / Pipeline]
Estimated Close Date: [date]
Deal Value: $[X]
```

---

### `competitor-battle-card` — Competitive Battle Card
**Usage**: `/sales competitor-battle-card "[competitor name]"`

#### Output Format
```
BATTLE CARD: [COMPETITOR NAME]
================================
Last updated: [date]
Primary use: [Sales calls / RFP responses / Discovery]

ELEVATOR PITCH (how to position when they come up)
"[Competitor] is great for [use case X]. Our customers typically choose us when
they need [differentiating capability Y] — especially if [specific condition]."

THEIR STRENGTHS (be honest — your reps need to know)
1. [Strength] — How to handle: [response]
2. [Strength] — How to handle: [response]

OUR STRENGTHS VS THEM
1. [Our advantage] — Proof point: [specific evidence]
2. [Our advantage] — Proof point: [evidence]
3. [Our advantage] — Proof point: [evidence]

THEIR KNOWN WEAKNESSES (from customer reviews, win/loss)
1. [Weakness] — How to surface: [question to ask]
2. [Weakness] — How to surface: [question to ask]

QUALIFYING QUESTIONS (to surface where we win)
- "How important is [capability we do better]?"
- "Have you had issues with [their known weakness]?"
- "What does your team currently do for [area they're weak in]?"

TRAPS TO SET DURING DEMO
1. Demonstrate [feature] early — they don't have this
2. Ask about [their weakness] — get prospect to voice it

OBJECTION HANDLERS

"[Competitor] is cheaper"
Response: "That's true for [their tier]. Our customers find that when they add [X/Y/Z],
the total cost is comparable — plus they get [differentiator]. Is cost the only criteria?"

"[Competitor] has feature X that you don't"
Response: [Honest response — either we have it (show it) or acknowledge gap and redirect to our strengths]

"We already use [Competitor]"
Response: "Totally understand — we actually work alongside them for [X use case].
Many customers use both. What's one thing you wish [Competitor] did better?"

WIN STORIES AGAINST THEM
Customer: [Company name or type]
Why they switched: [specific reason]
Result: [specific outcome]

LOSE GRACEFULLY (when to concede)
If they need [specific capability we don't have], [competitor] is the better choice.
Don't waste cycles — qualify out early if [condition].

PRICING COMPARISON
| Tier | Competitor | Us | Notes |
|------|------------|----|----|
| SMB | $X | $Y | [context] |
| Mid | $X | $Y | [context] |
| Enterprise | [custom] | [custom] | [context] |
```

---

## Sales Frameworks Reference

### Discovery Questions by Stage

**Problem Discovery**
- "Walk me through how you currently handle [process]"
- "What's the most frustrating part of that process?"
- "How much time does that take per [week/month]?"
- "What's the cost when that goes wrong?"

**Urgency & Priority**
- "Why is this a priority for you right now?"
- "What happens if you don't solve this in the next 6 months?"
- "Is there a specific event or deadline driving this?"

**Decision Process**
- "Who else will be involved in evaluating this decision?"
- "What does your typical procurement process look like?"
- "Have you gone through this kind of evaluation before? How long did it take?"
- "If we get to a place where this makes sense, what would need to happen to move forward?"

**Economic Buyer Discovery**
- "Who controls the budget for this kind of initiative?"
- "Will this come from an existing budget or require new budget approval?"

### Email Subject Line Formulas
- Pain-specific: "[Their specific pain] — quick question"
- Peer proof: "How [Similar Company] solved [Problem]"
- Trigger event: "Congrats on [funding/hire/launch] — question"
- Curiosity: "The [metric] number for [their industry]"
- Direct: "[Company]'s [specific process] — 2 ideas"

### Objection Handling Framework (LAER)
- **L**isten: Let them finish, don't interrupt
- **A**cknowledge: "I hear you — that's a fair concern"
- **E**xplore: "Can you tell me more about what's driving that?"
- **R**espond: Address the root concern, not the surface objection
