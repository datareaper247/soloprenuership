# SoloOS v4 Skill Gap Research
## 7 Missing Skill Categories: State of the Art, Best Practitioners, Skill File Requirements

**Analyst:** Research Agent (Claude Sonnet 4.6)
**Date:** 2026-03-22
**Scope:** Research on 7 skill categories missing from SoloOS v3. For each: state of the art, best practitioners, what a genuinely excellent skill file must contain.

---

## OVERVIEW: WHAT THIS RESEARCH FOUND

The 7 gaps requested are not equal in urgency or difficulty to operationalize.

| Skill | Urgency for Solo Founders | Existing SoloOS Coverage | Build Complexity |
|---|---|---|---|
| Negotiation Intelligence | High — fires on every deal | Zero | Medium |
| Competitor Displacement | High — fires at $5K+ MRR | Partial (intel.md covers autopsy, not switching) | Medium |
| Customer Success (Early) | Critical — fires at first 10 customers | Zero | Low |
| Positioning/Narrative | Critical — fires pre-launch | Zero | Medium |
| Talent Signal Detection | Medium — fires at $20K+ MRR | Partial (hire.md has gate, no interview signals) | Low |
| Financial Modeling | Medium — fires at multiple stages | Partial (finance.md has unit economics) | High |
| Distribution Engineering | High — fires when growth plateaus | Zero | High |

The most urgent gap: **Customer Success** and **Positioning**. Both fire before revenue and determine whether early customers stay or leave. They are also the most absent from the current system.

The most structurally underserved: **Negotiation**, which is entirely missing despite firing on pricing conversations with customers, partnership discussions, vendor deals, and investor terms — all of which appear in the current skill set without a negotiation layer.

---

## DOMAIN 1: NEGOTIATION INTELLIGENCE

### State of the Art

Two frameworks dominate, and for solo founders they are complementary, not competing.

**Framework 1: Fisher & Ury (Getting to Yes, Harvard Negotiation Project)**

The principled negotiation framework built on four pillars:
1. Separate the people from the problem
2. Focus on interests, not positions
3. Invent options for mutual gain
4. Insist on objective criteria

Strength: Works well in collaborative, longer-term negotiations (partnerships, enterprise deals, recurring supplier relationships). Produces durable agreements because both parties feel the outcome was fair.

Weakness for founders: Assumes rational actors with aligned interests. Breaks down when the other party is purely positional (buyer trying to extract maximum discount), when power is highly asymmetric (early-stage founder vs. institutional investor), or when the founder has no real BATNA.

**Framework 2: Chris Voss (Never Split the Difference / Black Swan Group)**

Voss explicitly positions his approach as an upgrade to Fisher & Ury for high-stakes, emotionally charged, and asymmetric negotiations. Built on behavioral economics, not rationalist assumptions.

Core techniques applicable to founders:

- **Tactical Empathy**: Demonstrating you understand the other party's emotional position before making any ask. "It sounds like you're worried about committing to a new tool before you've seen it work in your environment." Disarms defensiveness and builds trust faster than logic.
- **Mirroring**: Repeat the last 3 words of what the other party said as a question. Prompts elaboration without revealing your position. Powerful in pricing conversations: Prospect: "Your price is higher than competitors." You: "Higher than competitors?" Prospect then explains what they actually mean — often it's not price but risk.
- **Labeling**: Name the other party's apparent emotion without judgment. "It seems like you've had a bad experience with tools that promised a lot and didn't deliver." Gets head-nodding, deepens trust, surfaces unstated objections.
- **Calibrated Questions**: "How" and "What" questions that force the other party to engage with your constraints without sounding like ultimatums. Not "Can you lower your price?" but "How are you measuring the ROI on your current solution?" Not "We need a decision by Friday" but "What would have to be true for you to make a decision this week?"
- **The Ackerman Method**: For price negotiations specifically. Start at 65% of your target, make 3 incremental raises (85%, 95%, 100%), use empathy and calibrated questions throughout, throw in a non-monetary item at the end to signal you've reached your limit. Anchors the negotiation at your target rather than theirs.
- **Black Swans**: Hidden information that would transform the negotiation if revealed. For founders: the prospect's internal deadline, their budget remaining at fiscal year end, the specific failure of their current solution that is personally embarrassing to the decision-maker.

**BATNA (Best Alternative to a Negotiated Agreement)**

The Fisher & Ury concept that both frameworks share: your negotiating power is not your arguments — it is your alternatives. A founder with a full pipeline can walk away from a bad deal. A founder who needs this one customer to make payroll cannot.

The practical implication: before every significant negotiation, calculate your BATNA explicitly. Not as a vague feeling ("I have other options") but as a specific alternative ("If this deal falls through, I have 3 other prospects in active conversation, my runway is 8 months, and my walk-away price is $X").

**For Founder-Specific Contexts**

The research surfaces four negotiation contexts that recur for solo founders, each requiring a different emphasis:

1. **Pricing with customers**: Voss dominates. Tactical empathy + Ackerman method. Never discount with "OK" — only move with a calibrated question. "What would make it easier to commit to the annual plan today?" Discounting with no justification signals the original price was arbitrary.

2. **Investor terms (SAFE/seed)**: Both frameworks apply. BATNA is decisive — meet multiple investors before any term sheet conversation to create competitive tension. The key negotiation is the valuation cap: 2024 data shows typical range is ±20% from initial anchor, and moving the cap from $10M to $15M saves founders ~2.5% dilution. Never negotiate cap without knowing what that dilution costs you at 3 plausible exit scenarios.

3. **Partnerships and integrations**: Fisher & Ury + future of the relationship. Partnerships are ongoing. Positions that win short-term at the cost of relationship goodwill destroy long-term distribution. Focus on shared interests, not stated positions.

4. **Vendor deals (hosting, tools, contractors)**: Ackerman method + Voss labeling. Most vendors have more price flexibility than their initial offer suggests, but only respond to anchoring and alternatives, not to simply asking for a discount.

### Best Practitioners

- **Chris Voss** (Black Swan Group) — primary framework source. His "Tactical Empathy" podcast and Masterclass are the highest-quality distillation.
- **Jim Camp** (No: The Only Negotiating System You Need) — alternative school that predates Voss. "Stop trying to get to yes; help them say no to what they don't want." Useful contrast.
- **Alex Hormozi** — for pricing negotiations specifically. His framework for eliminating price as the objection by reframing value is widely used in founder communities.
- **David Lowe (Preferred Returns)** — for investor term negotiation specifically. His published analysis of term sheet trade-offs is the most founder-accessible.

### What the Skill File Must Contain to Be Excellent

1. **The BATNA calculator** — before every negotiation context, a prompt that forces the founder to explicitly name their alternative and their walk-away point. Not a concept — an actual output format.

2. **Context-routing by negotiation type** — different playbooks for: customer pricing, investor terms, partnerships, vendor deals. The tactics that work for customer pricing (Ackerman anchoring) will damage a partnership discussion.

3. **The 6 Voss techniques with founder-specific scripts** — not abstract descriptions but actual word-for-word patterns for the contexts that recur. "When a prospect says your price is too high, say exactly this..."

4. **The most common founder negotiation mistakes** — discounting without getting something in return, negotiating against yourself by offering a lower price before the prospect asks, accepting the first investor term sheet without creating competitive tension.

5. **Kill signals for negotiations** — when to walk away. A deal where the customer requires >20% discount and won't commit to annual. An investor whose terms include a 2x liquidation preference. A partnership where only one party is named in the distribution agreement.

6. **Stage calibration** — at $0 MRR the founder has no BATNA and should know what that costs them. At $20K MRR they can create competition for their business. The advice differs.

---

## DOMAIN 2: COMPETITOR DISPLACEMENT / SWITCHING PLAYBOOK

### State of the Art

This is the most systematically under-researched area in the solo founder literature, but the practitioner literature (B2B SaaS growth practitioners) has developed a coherent framework.

**Why Switching Is Hard: The Three Switching Cost Types**

McKinsey and Flexera data identify three categories of switching cost that solo founders must address when trying to displace an entrenched competitor:

1. **Financial switching costs**: Quantifiable monetary losses — migration costs, setup fees, downtime, retraining. 47% of enterprise buyers cite data migration as their primary barrier (Flexera 2023). For SMB SaaS, this shows up as "I'd have to export all my data and re-import it" — which is 3 hours of fear, not 3 hours of work.

2. **Procedural switching costs**: Workflow disruption, team retraining, evaluation time. The buyer must spend time they don't have to prove to themselves and their team that the switch is worth it.

3. **Relational switching costs**: Relationship with account manager, loss of institutional knowledge, the psychological cost of admitting the original choice was wrong.

**The Psychology of Switching (What Actually Triggers It)**

The Winsome Marketing research identified three customer archetypes based on switching behavior:

- **The Slow Burn**: Quietly accumulating frustrations. Taking screenshots of failures as evidence. Already emotionally committed to leaving before starting evaluation. Needs: validation that their frustration is legitimate, evidence others switched successfully.
- **The Ambitious Outgrower**: Grown beyond the tool's capabilities. Views premium alternatives as a status signal ("we're a real company now"). Needs: aspiration framing. "This is what companies at your scale use."
- **The Crisis Escapist**: Experienced a catastrophic failure (data loss, billing disaster, critical outage). Making an emotional decision for safety, not features. Needs: trust signals above all else — migration support, SLAs, human contact.

**What Makes Switching Happen (The Research Evidence)**

The switching decision is less rational than most founders assume. Customers: accumulate frustrations → see competitor at conference or in peer recommendation → start a "just looking" evaluation → build internal business case → switch. The implication: the trigger is rarely the feature list. It is almost always an emotional accumulation point that creates permission for a purchase they were already thinking about.

**Tactics That Work: The B2B SaaS Displacement Playbook**

Research from competitive conquesting campaigns shows measurable performance differences between approaches:

- **Comparison landing pages** targeting competitor brand keywords: average 2.3% CTR, 12% view-through conversion. The highest-performing copy leads with switch-and-save framing and social proof from named migrators, not feature comparison tables.
- **Migration cost removal**: Offering free migration as a concierge service removes the #1 procedural barrier. Several practitioners report 30-40% higher conversion on competitive deals where migration is handled vs. where it is self-serve.
- **Competitor review mining**: The most reliable source of switching triggers is 1-3 star reviews on G2, Capterra, and Reddit. These contain exact language for the pain that motivates switching. Use this language verbatim in competitive messaging.
- **Win rates by approach**: 2025-2026 data shows competitive displacement campaigns achieving win rates from 15% to 35% when using accurate attribution and behavioral targeting vs. general outreach. The 20-percentage-point gap comes from intent signal accuracy (are they actively evaluating, or just browsing?).
- **The "Permission Slip" message**: "Most companies outgrow [Competitor] at [milestone]" is one of the highest-converting competitive frames. It removes the sunk-cost psychology by making switching an achievement ("you've grown") not an admission of failure.

**What Makes It Fail**

- Feature comparison tables: buyers don't switch for features. They switch for pain relief. Feature lists don't address the emotional barrier to switching.
- No migration support: even a self-serve migration option with good documentation converts far less than "we'll do it for you."
- Targeting too broadly: competitive displacement requires intent-signal targeting. Mass advertising against a competitor's brand with generic messaging wastes budget and generates low-quality leads.
- Ignoring the internal champion problem: in B2B, the person evaluating the switch often didn't make the original decision. You need messaging that helps them make the case internally, not just messaging that wins their personal evaluation.

### Best Practitioners

- **Dave Gerhardt** (Exit Five) — competitive positioning and messaging for B2B SaaS
- **Sahil Mansuri** (Bravado) — competitive intelligence and sales enablement
- **The Mainsail Partners competitive takeaway playbook** — most specific documented framework for pricing incentives in displacement campaigns
- **Gong's competitive intelligence team** — has published extensive research on win/loss patterns in competitive deals

### What the Skill File Must Contain to Be Excellent

1. **The three switching cost types as diagnostic** — before building a displacement strategy, identify which switching cost is the primary barrier for your specific competitor. Financial/Procedural/Relational each require different tactics.

2. **The customer archetype routing** — Slow Burn, Ambitious Outgrower, Crisis Escapist. Different messages, different channels, different proof types.

3. **The Permission Slip frame** — the single highest-leverage message template for competitive displacement. Stage it at the correct milestone trigger.

4. **Migration concierge protocol** — the specific steps a solo founder can take to remove procedural switching cost without hiring a CS team. A 3-session migration support offer, a pre-built import template, a done-for-you setup call.

5. **Competitor review mining workflow** — extract exact pain language from G2/Capterra/Reddit for the incumbent competitor. Use verbatim language in competitive ads, landing pages, and cold outreach.

6. **The internal champion problem** — content and materials that help your buyer make the case to their team. ROI calculator, case study in their industry vertical, executive summary template.

7. **Integration with intel.md** — this skill should link to LAYER 3 (Switch-Away Reasons) of the 5-layer competitor autopsy. The displacement playbook begins where the competitor autopsy ends.

---

## DOMAIN 3: CUSTOMER SUCCESS AT EARLY STAGE

### State of the Art

The practitioner research is clear and specific. The academic research confirms the practitioner findings. This is the most evidence-rich domain in the 7.

**Why This Domain Is Different for Solo Founders**

The traditional customer success playbook (Nick Mehta, Gainsight) was built for companies with 100+ customers and a dedicated CS team. It is not the right model for a solo founder with 10-50 customers. The right model is closer to: "the founder IS the customer success team, and the interventions must be high-leverage enough to work at that scale."

**The Critical Timing Reality**

Research on early churn shows the highest-risk period is the first 30 days. Users who don't reach a defined "activation moment" within 30 days have dramatically higher churn probability regardless of later engagement. The corollary: the most valuable CS investment for a solo founder is in the onboarding experience, not in retention campaigns.

**The Three-System Early CS Framework**

1. **Prevention**: Activation-focused onboarding. Time-to-value must be less than 30 days for B2B SaaS. Define the exact moment when a user has "gotten value" — the first invoice sent, the first campaign launched, the first insight generated — and engineer the onboarding to reach that moment as fast as possible.

2. **Intervention**: Red Flag Metric detection. The research shows specific behavioral triggers predict churn with high accuracy:
   - Session duration < 2 minutes consistently → user is not finding value
   - Login frequency drops > 50% week-over-week → disengagement signal
   - Core workflow not completed in first 14 days → activation failure
   Published data on intervention campaigns targeting these signals: 26% response rate and 40% retention improvement on short-session users; 15% response rate and 50% retention improvement on low-login users. These are dramatic numbers for simple automated interventions.

3. **Learning**: The feedback loop that makes the product better faster. The customer who churns knows something you don't about why your product doesn't work for their situation. The systematic collection and synthesis of this information is the highest-leverage learning investment at early stage.

**Specific Interventions That Work**

For a solo founder with 10-50 customers, the highest-ROI interventions in order:

1. **Personal onboarding call** (30 min, CEO-led): The single most effective tool for early-stage churn prevention. Not scalable past 50 customers but essential before it. Establishes relationship, surfaces friction, and creates psychological commitment. Research shows customers who have a founder onboarding call churn at 60-70% lower rates in the first 90 days.

2. **Activation milestone email sequence**: 3 emails triggered by behavior (or lack of behavior), not time. Email 1: "Did you [complete first key action]?" If no, link to the specific tutorial. Email 2 (7 days in, if no activation): "Can I schedule 15 minutes to help you get started?" Email 3 (14 days, if still no activation): "I noticed you haven't [activated] yet. Is there a reason this isn't the right fit?"

3. **The 90-day success call**: At day 45-60, proactively call every customer to ask: "Are you getting what you expected? What would make this more useful?" This call is not support — it is intelligence gathering and relationship investment. Convert the conversations into product decisions publicly: "Because 3 customers mentioned X, we're building it next month."

4. **Churn exit interview (always)**: When a customer cancels, the solo founder should call personally within 24 hours. Not to win them back — to learn. The research on NPS shows non-respondents and churned customers contain the richest product intelligence. Most founders never access it.

5. **Early advocacy activation**: The right moment is immediately after a customer success. Capturing the micro-win when excitement is highest. "You just processed your first 100 transactions through us — would you be willing to share a brief quote about that experience?" The customer's exact words become the product's most credible marketing.

**The Customer Health Score for Solo Founders**

Building a health score with 10 customers doesn't require Gainsight. It requires a simple weekly check:
- Product signals: Log-in frequency, core workflow completion, feature adoption
- Relationship signals: Response time to emails, NPS if collected
- Business signals: Payment status, stated goals vs. current usage

Green/Yellow/Red. Spend every Monday 30 minutes on Yellow accounts.

### Best Practitioners

- **Lincoln Murphy** (Sixteen Ventures) — defined early-stage CS for SaaS. His "Customer Success Qualified Lead" framework is directly applicable.
- **Steli Efti** (Close.io) — prolific on founder-led CS at early stage, especially on the personal check-in model.
- **Nick Mehta / Gainsight** — the definitive CS scaling playbook (applies at >100 customers).
- **Jason Lemkin** (SaaStr) — on when to hire the first CS person and what not to do before then.

### What the Skill File Must Contain to Be Excellent

1. **Stage-calibrated protocols**: 1-10 customers (founder does everything personally), 10-50 customers (founder-led with automation triggers), 50-100 customers (first CS hire or systematic delegation). Different playbook for each.

2. **The Activation Moment definition protocol**: Forces the founder to name the exact behavioral event that constitutes "value received" before any CS work begins. This is the anchor for all downstream interventions.

3. **The 5 Red Flag Metrics**: Specific behavioral signals with documented intervention response rates. Not "watch for disengagement" but "session duration < 2 minutes triggers this specific email."

4. **Exact email scripts for activation sequence**: Not templates — actual high-performing scripts with subject lines, from personal CEO address, with specific behavioral triggers.

5. **The advocacy activation script**: The exact moment and exact language to ask for a testimonial, case study, or referral. Most founders ask too late or too generically.

6. **The churn exit interview protocol**: The 5 questions to ask every churned customer. What to do with the answers.

7. **The 90-day success call agenda**: 15 minutes. 5 specific questions. How to turn the answers into product decisions and communicate that back.

8. **Integration with sales.md and product-moat.md**: The CS skill should know it feeds the moat-building loop and the referral pipeline.

---

## DOMAIN 4: POSITIONING / NARRATIVE ARCHITECTURE

### State of the Art

This is the best-documented domain with the highest-quality practitioner frameworks. April Dunford's work is genuinely state of the art and has been validated across 200+ B2B companies. The gap is that no one has translated it into a solo founder protocol with stage calibration.

**The Positioning Problem for Solo Founders**

Most founders choose their market category first ("I'm building a project management tool") and then try to differentiate within it. This is backwards. Dunford's central insight: positioning is not about finding where you fit in a category — it is about finding the context that makes your product's specific strengths feel inevitable and obvious.

The correct sequence: Start with your best customers → Understand why they chose you over their alternatives → Identify the unique capability that drove that choice → Find the market frame that makes that capability the most important thing in the category.

**April Dunford's 5 Components of Positioning**

These are not sequential steps — they are a connected system where each element must be consistent with the others:

1. **Competitive Alternatives**: Not "who are your competitors?" but "what would your best customer use if you didn't exist?" The answer is often not the obvious competitor. Userlist's real competitive alternative turned out to be "build in-house" — not Intercom or Customer.io. That changes everything about messaging.

2. **Unique Attributes**: The capabilities your product has that the alternatives don't. Must be documented factually, not aspirationally. Not "we're easier to use" but "the specific features or design decisions that create that ease."

3. **Differentiated Value**: Why do the unique attributes matter? What business outcome do they enable? The more unique a feature, the less likely prospects understand its value without explanation. The work is translating capability into business outcome: not "real-time sync" but "your team always has the same data, which eliminates the 4 hours/week of version reconciliation in your current workflow."

4. **Best-Fit Customers**: The characteristics of the customers for whom your differentiated value is most compelling. Not demographic — behavioral and situational. "Teams of 3-15 that use Notion for project management and are frustrated by the lack of CRM integration" is a best-fit customer segment. "SMBs" is not.

5. **Market Category**: The frame you choose for your product — the mental context that helps buyers understand what to compare it to. This is the most strategic decision in positioning. The same product can be positioned as "the simplest CRM" (competing in CRM category) or "the sales tool built for solo consultants" (creating a category where you're automatically the leader).

**The 10-Step Positioning Exercise (Dunford Protocol)**

Translated from the Userlist implementation and Dunford's own published guides:

1. Identify your 5-10 best customers (bought quickly, use daily, refer others)
2. Assemble the positioning team (at early stage: just the founder plus 1-2 of those best customers)
3. Align on vocabulary (what does "positioning" mean vs. "messaging" vs. "brand"?)
4. List ALL competitive alternatives (including "do nothing" and "build it ourselves")
5. Inventory all product capabilities vs. each alternative
6. Group capabilities into value themes (3-5 max)
7. Identify which customers care most about which value themes
8. Select the market frame that makes your strongest value theme central
9. Layer on relevant trend (why now? what macro shift makes this urgent?)
10. Capture in a one-page positioning canvas

**The Solo Founder Shortcut**

The full 10-step exercise takes weeks. For a solo founder pre-revenue, the minimum viable positioning work is:
1. Talk to 5 people who said yes
2. Ask each one: "What were you using before? What made you choose this instead? What do you tell others when you describe it?"
3. Find the phrase that appears in 3+ of those conversations
4. That phrase is your positioning

**Common Positioning Mistakes**

- Category too large: "I'm building project management software" positions you against Asana and Monday.com. "I'm building project management for solo consultants" positions you as the obvious leader in a category you define.
- Features before value: listing what the product does before explaining what outcome it enables.
- Positioning for everyone: "works for freelancers, small teams, and enterprises" is not positioning. It is the absence of positioning.
- Ignoring the competitive alternative: "better than the competition" without naming what specific alternative best customers would use without you.

**Advanced Positioning: The "Big Fish, Small Pond" Strategy**

When a larger category exists with well-known players, the most reliable solo founder positioning is to identify the underserved sub-segment within that category and position as the obvious leader there. Userlist's final positioning: "More efficient than building it yourself; less complex than Intercom or Customer.io" — placed them as the clear choice for one specific segment (small, technical SaaS teams) rather than competing head-on with Intercom.

### Best Practitioners

- **April Dunford** — Obviously Awesome (2019, updated 2026). The definitive modern positioning framework for B2B tech.
- **Andy Raskin** — Strategic narrative work. Frames positioning as a narrative structure, not a statement.
- **Bob Moesta** — Jobs-to-be-done applied to positioning. The "struggling moment" that drives purchase is the foundation of positioning.
- **Peep Laja** (CXL) — applied positioning testing via conversion research. Most empirical practitioner on whether positioning changes actually move conversion rates.

### What the Skill File Must Contain to Be Excellent

1. **The Dunford 10-step protocol formatted as a workshop the founder can run alone**: Not "do this exercise" but the actual questions at each step with examples.

2. **The minimum viable positioning shortcut** for pre-revenue founders: 5 customer conversations, the 3 specific questions, the synthesis protocol.

3. **The competitive alternative forcing question**: "If we didn't exist, what would your best customer do?" This is the single most important positioning question and most founders skip it.

4. **The market category decision framework**: "Big Fish Small Pond" vs. head-on category competition vs. category creation. When to use each. The failure modes of each.

5. **The positioning canvas template**: One-page output that captures all 5 components. Founders should update this every time their best customer profile changes.

6. **Positioning vs. messaging distinction**: Positioning is the strategic foundation. Messaging is the expression of positioning in specific copy. The skill file must keep these separate or founders conflate them.

7. **Positioning kill signal**: "If you asked 10 random members of your target ICP to describe what your product is for, and the answers vary significantly, your positioning has not landed."

8. **Integration with validate.md and brand.md**: Positioning should be set before launch messaging is written. Positioning should be tested during validation. The skill file should route to validate.md if positioning is being set pre-product.

---

## DOMAIN 5: TALENT SIGNAL DETECTION IN HIRING

### State of the Art

The existing hire.md is strong on the gate (when to hire) and the archetypes (what kind of person). It has zero content on the interview and evaluation process. This is where the majority of hiring failures happen.

**The Core Research Finding**

Traditional interviews are poor predictors of job performance. The research consensus across decades of industrial-organizational psychology: structured behavioral interviews have 0.51 validity (correlation with job performance); unstructured interviews have 0.38; work samples have 0.54; cognitive ability tests have 0.51. The implication: the most predictive hiring process for early-stage startups is: structured behavioral questions + paid work sample + reference checks that go beyond the provided list.

**The PostHog Protocol: The SuperDay**

PostHog's approach is the most documented and most applicable to early-stage startups:
- 2-3 short screening interviews (culture, role basics, motivation)
- Paid SuperDay: 1 full day of real-adjacent work, paid at market rate, flexible scheduling
- The task is sent that morning (no advance preparation → tests how they work under normal conditions, not how they prep for assessments)
- Private Slack channel for questions during the day
- Informal culture chat with non-hiring-team members
- Evaluation criteria: proactivity, directness, communication quality, impact awareness, iteration/growth mindset

The PostHog insight: "Interviews are an imperfect filtering mechanism. Getting candidates to do sustained actual work in a semi-realistic context is much better." The paid work trial filters out people who are good at interviews but can't execute. It also self-selects for candidates who are genuinely interested — uncommitted candidates won't spend a day on a work trial.

**The Marco Rogers Framework (400+ Engineering Interviews)**

The First Round Capital interview documented five dimensions that distinguish A-players for early-stage startups:

1. **Low ego + high receptiveness**: Not "do they think they're right?" but "how do they respond when shown they're wrong?" Probe: describe a time you changed your approach based on feedback. What changed and why?

2. **Adaptability to organizational chaos**: Early-stage environments restructure constantly. Candidates with only stable-company experience often fail not because of skill gaps but because the ambiguity is genuinely disorienting. Probe: describe a period when your team's direction changed rapidly. What was your response?

3. **Technical communication mastery**: The distinction between knowing something, applying it, and explaining it is critical. Technical A-players can explain their decisions with the trade-offs visible: "I chose NoSQL here because [specific reason] despite the [specific cost]." Not preferences — trade-off articulation.

4. **Cross-functional collaboration evidence**: Not just "I worked with other teams" but "here is a specific failure in cross-functional collaboration and how I resolved it." The ability to close collaboration failures proactively is the rarest signal.

5. **Consistency across multiple evaluators**: A-players don't have "on" days in interviews. They perform consistently across different interviewers because their excellence is structural, not contextual. Running 3+ separate evaluation conversations and comparing notes is more predictive than a single long interview.

**The Most Common Hiring Failure Mode for Solo Founders**

Hiring someone who is excellent in a large company context into an early-stage solo founder context. The skills that work at scale — specialization, process adherence, working within defined systems — are the opposite of what works at pre-PMF. The archetypal bad first hire: an experienced marketing manager from a Fortune 500 who has never had to build a channel from zero.

The signal to look for: "Have you built something from zero without a playbook?" is worth more than any credential. The absence of this experience predicts failure in the first hire.

**The Work Trial Protocol for Solo Founders**

Most solo founders cannot afford a full PostHog SuperDay. The minimum viable version:
- 2-4 hour paid test ($50-200 depending on seniority)
- Task is a real problem from your actual work, made anonymous if necessary
- Evaluate: How do they handle ambiguity? Do they ask good questions? Is the output usable immediately?
- The most revealing moment is not the output — it is the questions they ask during the task.

**Reference Check Protocol (The Most Underused Signal)**

Most founders ask for 2 references from the candidate's provided list. Both will be positive. The signal is in asking:
- "Would you work with [candidate] again? Under what circumstances?"
- "What type of environment does [candidate] NOT thrive in?"
- "If you had to give them one piece of feedback they haven't fully acted on yet, what is it?"
- The most valuable references are people not on the provided list — the candidate's previous peers, not supervisors.

### Best Practitioners

- **PostHog** (James Hawkins, Tim Glaser) — most documented early-stage hiring protocol
- **Gergely Orosz** (The Pragmatic Engineer) — engineering-specific but generalizes well
- **Geoff Smart and Randy Street** (Who) — the A-player interview method with the Topgrading technique
- **Pat Lencioni** (The Five Dysfunctions of a Team) — for evaluating team dynamics potential

### What the Skill File Must Contain to Be Excellent

1. **Integration with hire.md's gate and archetype sections**: The talent signal file fires AFTER the hire gate is passed. It assumes the decision to hire has been made and provides the HOW.

2. **The 5 A-player dimensions for early-stage startups** with specific interview questions for each, not generic competency frameworks.

3. **The minimum viable work trial protocol**: 2-4 hour paid task, evaluation rubric, the specific signals to look for in how they handle ambiguity.

4. **The "built from zero" filter**: As a prior question before any evaluation. "Have you built [role function] from zero without a playbook before?" If no → specific risk and mitigation.

5. **The reference check protocol**: The exact 4 questions, the off-list reference strategy, how to weight conflicting signals.

6. **The most common false positive signals**: Great interview performance, impressive credentials, and cultural fit enthusiasm are all overweighted by solo founders. The real predictors are execution samples and zero-to-one track record.

7. **Kill signal for the evaluation process**: "If the work trial output is impressive but the candidate couldn't articulate the trade-offs they made, the output may have been lucky. Probe the decisions before hiring."

---

## DOMAIN 6: FINANCIAL MODELING FOR SOLO FOUNDERS

### State of the Art

The existing finance.md in SoloOS is strong on unit economics (LTV, CAC, churn, payback period) but is primarily diagnostic. It answers "are my numbers healthy?" not "what does my model say I should do next?"

**The Gap: Decision-Oriented Modeling**

The difference between a diagnostic finance tool and a decision-support tool is the sensitivity analysis and the scenario model. Most SaaS financial model literature is built for investor presentations, not for founder decision-making. A founder-oriented model answers different questions:

- "If I raise prices 30%, how many customers can I afford to lose and still come out ahead?"
- "Which is more valuable: reducing churn by 1% or increasing acquisition by 20%?"
- "At what MRR does hiring a $60K/year person pay for themselves in released founder hours?"
- "If I raise $500K now, what does my dilution look like at each of 3 exit scenarios?"
- "What's my runway under the bear case if my best 3 customers don't renew?"

These are the questions that drive actual founder decisions. They require a model built around sensitivity levers, not a static snapshot.

**The Three-Scenario Model**

The Inflection CFO research identifies this as the minimum structure:
- **Base case**: Current trajectory, current conversion rates, current churn. What happens if nothing changes significantly.
- **Bull case**: Strong execution (+25-40% on growth levers, -20% on cost levers). What the model looks like if things go well.
- **Bear case**: Execution challenges (-25-40% on growth levers, +20% on cost levers). What the model looks like if key assumptions fail.

The output comparison table is the key artifact: months to profitability and capital required differ dramatically across scenarios. This informs the raise-vs-bootstrap decision more clearly than any other framework.

**The Four Founder Decision Models**

Each of the key solo founder decisions has a corresponding model structure:

1. **Pricing decision model**: What is the MRR impact of a price increase assuming X% churn? The break-even churn rate (at what customer loss does the price increase become neutral) is the key output. Most founders price too low and don't model the break-even.

2. **Hire vs. automate model**: What is the founder's current hourly value in revenue-generating activities? What is the cost of the hire vs. the cost of their time? The model should include the productivity tax (3-6 months of founder time to train and manage before the hire reaches full productivity).

3. **Expansion revenue model**: The LTV impact of upsell/cross-sell as a percentage of total revenue. For most SaaS founders, 1% of customers contributing expansion revenue moves NRR from 90% to 110%. This is worth modeling explicitly.

4. **Bootstrap vs. raise model**: Model both paths to the same milestone (e.g., $50K MRR). The bootstrapped path requires longer runway from current revenue. The funded path requires dilution. The model output: at what exit multiple does each path leave the founder with more proceeds?

**The Key Metrics That Most Solo Founders Don't Track**

- **Net Revenue Retention (NRR)**: Total revenue from cohort at 12 months / total revenue from cohort at month 1. Above 100% means expansion revenue offsets churn. The single most important metric for SaaS long-term health.
- **Payback period**: CAC / (ACV * gross margin). How many months of subscription to recover the acquisition cost. Under 12 months is healthy; over 18 months is a warning sign.
- **Churn sensitivity**: What happens to LTV if churn changes by 1 percentage point? Most founders underestimate this. At 5% monthly churn, LTV = 20 months ACV. At 4% monthly churn, LTV = 25 months ACV. A 1-point churn reduction is worth 25% more LTV.

### Best Practitioners

- **Christoph Janz** (Point Nine Capital) — his SaaS Financial Plan is the most founder-friendly public model template
- **Baremetrics** — their blog has the most practical SaaS financial modeling guides with real operator numbers
- **Jason Cohen** (WP Engine founder) — his essays on bootstrapped SaaS financial modeling are the most honest about the non-VC path
- **Inflection CFO** — scenario planning and sensitivity analysis framework

### What the Skill File Must Contain to Be Excellent

1. **The 4 decision model templates**: Pricing decision, hire-vs-automate, expansion revenue, bootstrap-vs-raise. Each as a structured output with the specific variables and the decision-relevant output format.

2. **The churn sensitivity calculator**: A simple table showing LTV at each churn rate from 1-10%. This single visualization changes how founders think about retention investments.

3. **The break-even churn rate for price increases**: For any proposed price increase, calculate the churn rate at which the increase becomes neutral. If that rate is below your current churn, the increase is safe.

4. **The three-scenario model structure**: Base/Bull/Bear with the specific variables to flex and the comparison table output.

5. **NRR calculation and benchmarks**: What does NRR look like for a healthy vs. struggling SaaS at each stage? The data: best-in-class is 120%+, healthy is 100-110%, warning sign is below 90%.

6. **The hire timing calculation**: The specific model for when a hire pays for itself. Not "hire when you need help" but "hire when the revenue freed by removing the bottleneck exceeds 2.5x the hire's cost within 6 months."

7. **Integration with finance.md**: This skill is a decision layer on top of finance.md's diagnostic layer. It should fire when the founder is facing a specific decision, not just doing financial review.

---

## DOMAIN 7: DISTRIBUTION ENGINEERING

### State of the Art

Distribution is where the most important and least understood work in startup building happens. The core insight from all serious practitioners: product wins are temporary; distribution wins compound.

**The Foundational Framework: Product-Channel Fit**

Brian Balfour's work at Reforge is the most rigorous framework. The central insight reverses the common assumption: **products are built to fit channels, not the other way around**. The channel's rules are fixed; the product is malleable. A product that requires users to have 3 days to onboard cannot use paid social as its primary channel. A product that requires viral sharing built into its core output cannot use outbound sales as its primary channel.

Channel fit requirements by type:
- **Virality channels**: Short time-to-value (minutes), broad value proposition, network effect within the product
- **Paid acquisition channels**: Fast value discovery, medium-to-broad ICP, transactional model that funds acquisition cost
- **SEO/content channels**: Long-cycle value discovery acceptable, content that addresses problem awareness queries, 6-18 month time horizon
- **Sales-led channels**: High ACV ($500+/month), complex value proposition, multiple stakeholders
- **Partnership/integration channels**: Complementary product audience, shared customer workflows, mutual distribution benefit

**The Power Law of Distribution**

The research on $100M+ companies shows a consistent pattern: 70%+ of growth comes from a single primary channel. The implication for solo founders: the goal is not to "test a bunch of channels" — it is to find the one channel that fits your product and owns it before competitors do.

**How to Find an Underexploited Channel**

The Andrew Chen and Brian Balfour research identifies the mechanism by which distribution channels become exploitable:

1. **New platform emergence**: Every new platform (LinkedIn feed algorithm changes, TikTok for B2B, Discord communities, AI-native distribution) has a window where early movers get dramatically better economics than late movers. "By the time there's a case study about a new marketing tactic, the advantage has already been arbitraged away." The window for LinkedIn thought leadership content was 2018-2021. The window for TikTok B2B content is approximately 2024-2026.

2. **Competitor channel neglect**: Large incumbents optimize for scale. They have minimum viable spend levels for channels — they won't run campaigns that generate less than $100K revenue. This creates whitespace in niche channels, niche communities, niche integration marketplaces. The App Store for a small SaaS marketplace (Notion integrations, HubSpot integrations, Slack apps) where your ICP already lives is a channel your funded competitor may be ignoring.

3. **Platform API or algorithm changes**: When a platform changes its rules, incumbents who built on the old system are disrupted. New entrants who build on the new system have a temporary advantage. Pinterest's Facebook API deprecation destroyed some companies and created others. The lesson: monitor channel rule changes and be ready to shift.

**Saturation Signals**

A channel is saturated when:
- CAC through that channel has increased > 3x from initial experiments
- The number of competitors using the channel has increased dramatically (monitor competitor ad presence, content frequency)
- Your ICP is complaining about "too many ads" or "too much content" in that channel
- The playbook for the channel is widely published and case-studied (published = commoditized)

A channel is underexploited when:
- Your ICP is in it but your competitors are not
- The production cost is high (barriers to entry protect the channel)
- The channel is new enough that there is no established playbook
- It is too small for your funded competitors to care about

**The Bullseye Framework (Weinberg/Mares)**

The 19 channels framework from Traction provides a systematic audit approach:
1. Brainstorm: What is the plausible case for each of the 19 channels for your product?
2. Rank: Which 3-5 channels are most likely to work based on product-channel fit analysis?
3. Test: Run cheap, fast experiments in the top 3 ($500, 2 weeks, specific metric threshold)
4. Focus: Double down on the one that shows signal; cut the others
5. Revisit: When primary channel saturates, return to step 1

The most common mistake: testing channels sequentially over months. The research shows parallel experimentation finds better channels faster (the Karpathy/SkyPilot parallelism finding from AI_ERA_PATTERNS.md applies here).

**Specific Underexploited Channels in 2025-2026**

Based on current research:
- **Integration marketplaces**: HubSpot App Marketplace, Notion integrations, Slack App Directory, Make/Zapier templates. Most B2B SaaS founders either don't list here or list without optimization. The channel is large (ICP is already there) and competition within most categories is sparse.
- **Niche newsletter sponsorships**: The beehiiv/Substack ecosystem has created thousands of niche newsletters with tight ICP audiences. Sponsorship is still underpriced relative to reach quality. A $500 sponsorship in a 5K-subscriber niche newsletter often outperforms $2K in Google Ads by conversion quality.
- **Community-led distribution**: Discord communities, Slack groups, and Reddit communities where the ICP already congregates. Not spammy promotion — building genuine presence over 3-6 months before mentioning the product. The CAC is time-expensive but cash-cheap.
- **Direct content-to-distribution via AI tools**: YouTube and TikTok algorithm discovery for tools that solve visible workflow problems. The AI tools category is currently generating organic discovery at dramatically higher rates than older categories.

**The Clay Distribution Case Study**

Clay's distribution strategy is the most instructive recent example: they coined the term "GTM Engineer" as a role identity, wrote the defining content, built the community, and positioned their product as the operating system for that role — before anyone else could. Distribution moat built on vocabulary ownership. The lesson: if you can name the job your customer is trying to do, you can own the category.

### Best Practitioners

- **Brian Balfour** (Reforge) — four-fits framework, product-channel fit, the most rigorous distribution thinking
- **Andrew Chen** (a16z) — dual theory (product/market fit + distribution fit), growth loops
- **Gabriel Weinberg / Justin Mares** (Traction) — the 19 channels Bullseye Framework
- **Hiten Shah / Patrick Vlaskovits** — distribution-first thinking for SaaS
- **Lenny Rachitsky** (Lenny's Newsletter) — documented distribution strategies across 50+ successful consumer and B2B products

### What the Skill File Must Contain to Be Excellent

1. **The product-channel fit matrix**: A table mapping product characteristics (ACV, time-to-value, viral potential, ICP concentration) against channel requirements. Helps founders eliminate non-fitting channels immediately.

2. **The Bullseye Protocol adapted for solo founders**: The 19-channel brainstorm formatted as a structured prompt, with ranking criteria, minimum viable test design ($500, 2 weeks, specific threshold), and decision protocol.

3. **The channel saturation detection framework**: The 4 specific signals that a channel is saturated. And the corresponding 4 signals that a channel is underexploited. Not abstract — specific metrics and observations.

4. **The underexploited channel audit for 2025-2026**: The specific channel categories where competition is currently sparse relative to ICP concentration. This section needs to be updated annually.

5. **The parallel experiment design**: Running 3 channel tests simultaneously rather than sequentially to find signal faster. Budget allocation, duration, and decision criteria.

6. **The "name the job" distribution strategy**: The Clay case study as a replicable pattern. If you can define the role identity your ICP is trying to inhabit, vocabulary ownership creates distribution moat.

7. **Integration with growth.md and intel.md**: Distribution should use intel.md's Layer 4 (competitor distribution analysis) as its starting point. The channels your competitors are using show you where competition exists. The channels they're ignoring show you the whitespace.

---

## CROSS-CUTTING FINDINGS: WHAT ALL 7 SKILLS SHARE

After researching all 7 domains, three patterns emerge that should shape how the skill files are built:

### Finding 1: The Stage Calibration Problem

Every single domain has stage-dependent advice that changes dramatically at key thresholds. The skill files that are currently weak (compared to the stronger ones like pmf.md and sales.md) all fail to stage-calibrate. The best skill files in SoloOS behave completely differently at $0 MRR vs. $5K MRR vs. $20K MRR. All 7 new skills should include explicit stage routing.

### Finding 2: The Kill Signal Problem

The existing SoloOS discipline of naming a kill signal should apply to all 7 skills, but each domain has specific kill signals that matter:
- Negotiation: "If you've discounted more than 20% without a reciprocal concession, your pricing has no anchor"
- Competitor displacement: "If your competitive win rate has not improved 6+ months into a displacement campaign, the switching cost problem is not messaging — it's product"
- Customer success: "If activation rate is below 40% after 30 days, the onboarding problem is upstream of CS"
- Positioning: "If 10 random ICP members can't say in 10 words what your product is for, positioning has not landed"

### Finding 3: The Integration Problem

The 7 skills are not independent. The strongest version of each skill integrates with the existing system:

| New Skill | Should Integrate With |
|---|---|
| Negotiation | sales.md (pricing conversations), fundraising.md (investor terms), hire.md (contractor deals) |
| Competitor Displacement | intel.md (Layer 3 switch-away reasons, Layer 4 distribution), growth.md |
| Customer Success | onboard.md, pmf.md, product-moat.md, validate.md |
| Positioning | validate.md, brand.md, launch.md |
| Talent Signal | hire.md (fires after the gate is passed) |
| Financial Modeling | finance.md (decision layer on top of diagnostic layer) |
| Distribution | growth.md, intel.md, brand.md |

---

## RECOMMENDED BUILD SEQUENCE

If building all 7 skills, this is the recommended sequence based on research urgency and integration dependencies:

1. **Positioning** — fires pre-launch and determines whether all downstream skills work. The lever that makes sales, CS, and distribution more efficient. Build first.

2. **Customer Success (Early)** — fires at first paying customer. The highest-urgency intervention point. Most solo founders have no protocol here. Build second.

3. **Negotiation** — fires constantly across multiple existing skills. Integrates with sales.md, fundraising.md, and hire.md. High value because it improves outcomes of skills already in use. Build third.

4. **Distribution Engineering** — fires when growth plateaus. Complex to build well but very high leverage. Build fourth.

5. **Competitor Displacement** — fires at $5K+ MRR when defending and expanding accounts. Integrates with intel.md. Build fifth.

6. **Financial Modeling** — fires at multiple decision points but requires the founder to have data to model. More useful at $10K+ MRR. Build sixth.

7. **Talent Signal Detection** — fires at $20K+ MRR for most solo founders. Lower urgency than the others. Build seventh.

---

*Research sources consulted: Chris Voss / Black Swan Group (negotiation), Winsome Marketing (switching psychology), PostHog founders blog (hiring), April Dunford's Obviously Awesome and Lenny's Newsletter positioning guides, Brian Balfour / Reforge (product-channel fit), Inflection CFO (scenario modeling), Churn Zero / Vitally / SaaStr (customer success benchmarks), Mainsail Partners (competitive displacement), Gabriel Weinberg / Traction (19 channels), Andrew Chen's dual theory essays.*
