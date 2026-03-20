# Example: CLAUDE.md Before vs. After

The same question asked to Claude, with and without CLAUDE.md in the project.

---

## Question 1: "How should I market my B2B SaaS?"

### Without CLAUDE.md

```
Great question! Here are some effective marketing strategies for B2B SaaS:

1. Content Marketing
   - Write blog posts about your industry
   - Create thought leadership content
   - Use SEO to drive organic traffic

2. LinkedIn Marketing
   - Post regularly about your niche
   - Engage with potential customers
   - Run LinkedIn Ads for targeted reach

3. Email Marketing
   - Build an email list
   - Send regular newsletters
   - Use drip campaigns for nurturing

4. Cold Outreach
   - Identify your ideal customer profile
   - Send personalized cold emails
   - Follow up consistently

5. Partnerships
   - Partner with complementary tools
   - Build an affiliate program
   - Attend industry events

Would you like me to go deeper on any of these?
```

**Problem**: Generic. No context. No prioritization. Could apply to any B2B SaaS at any stage.
Founder still has to figure out what to actually do.

---

### With CLAUDE.md (+ context/business-context.md populated)

```
⚠️ LEVERAGE CHECK before answering:
You're at $4,200 MRR, flat 6 weeks. At this stage, retention drives more
value than acquisition — a 1% churn reduction worth more than a new channel.

What does your D30 retention look like right now? (If you don't know this
number, finding it out is the highest-leverage thing you can do before
touching marketing.)

Assuming retention is solid (>85% D30), here's the 80/20 answer:

RECOMMENDATION: One channel, deep — not five channels shallow.
WHY:
- You have 140 customers. That's 140 potential referrals and case studies.
  Your best marketing asset already exists and you're not using it.
- At $4,200 MRR, paid acquisition math doesn't work yet (need to know CAC
  vs. LTV:CAC ratio to even know if paid is viable).
- SEO compounds — every article you write keeps ranking. Cold outreach doesn't.

THE 20% THAT DRIVES 80%:
  1. Talk to 5 of your best customers this week. Ask: "How did you find us?
     What would you tell a colleague about Rankly?" Record exact language.
  2. Write 3 SEO articles using their language targeting the keywords they
     used when searching for you. (Run /seo research "keyword rank tracking"
     to get the specific terms.)
  3. Ask those 5 customers for one referral each. That's your fastest 5 leads.

RISKS:
- Starting a new channel before understanding why existing customers stay/leave
  is premature optimization. You'll build for the wrong ICP.

FIRST ACTION:
Email your 5 highest-LTV customers today:
"Quick 15-min call this week? I want to understand how you're using Rankly
and what you'd tell a friend about it. Happy to share what I'm seeing across
all our customers in return."

⚠️ ANTI-PATTERN FLAGGED: "Marketing before retention check" — you mentioned
flat growth without sharing churn rate. Don't start a new channel until you
know why you're flat.
```

**What changed**:
- Specific to $4,200 MRR stage (not generic)
- References their actual product (Rankly) and customer count (140)
- Flags that retention check should come first (anti-pattern detection)
- Top 2 actions, not 10 equal items
- Explicit "first action" that can be done today

---

## Question 2: "Should I build [feature]?"

### Without CLAUDE.md

```
Building new features depends on several factors:

1. User demand - Have users requested this feature?
2. Strategic fit - Does it align with your product vision?
3. Technical feasibility - Can your team build it?
4. Resource allocation - Do you have the time/budget?
5. Competitive analysis - Do competitors have it?

If these factors align, it could be worth building. Consider creating a
lightweight prototype or MVP to test the concept first.
```

**Problem**: Five equal considerations. No clear answer. Founder is no closer to a decision.

---

### With CLAUDE.md

```
VALIDATE FIRST — before I answer this:

Has a customer explicitly said "I would pay more / I would not have churned /
I would have signed up earlier if this existed?" (In their words, not inferred.)

If YES → proceed to decision framework below.
If NO → this is a founder assumption, not a customer request.
         ⚠️ VALIDATE: Talk to 5 customers this week. Ask them: "What's the
         most annoying thing about [product] right now?" Listen. Don't lead.
         If this feature comes up unprompted from 3+ customers → then build.

Assuming YES (customer-validated request):

DECISION FRAMEWORK:
Reversibility: HIGH — you can ship and roll back
Assumption: This feature drives retention, not just activation
Kill signal: If feature ships and D30 retention doesn't improve in 60 days

PRIORITY TEST:
- Does this fix a reason customers churn? → Build it next.
- Does this attract new customers? → Build it after retention is solved.
- Does this serve 1 loud customer but not the ICP? → Don't build it, offer consulting.

RECOMMENDATION: [specific to your context once I know which feature]
```

**What changed**:
- Hard stop: is this customer-validated or founder assumption?
- Anti-pattern flagged automatically (building before validation)
- Decision framework is 3 questions, not 5 generic factors
- Kill signal defined upfront so founder knows when to reverse
- Specific test for ICP fit vs. single-customer noise

---

## The Pattern Difference

Without CLAUDE.md, Claude gives answers.

With CLAUDE.md, Claude gives answers **calibrated to your stage, your context, and the
specific failure modes that kill founders at your exact MRR**.

The behavioral rules don't just add information. They change what Claude notices,
what it flags before answering, and what it refuses to recommend without more data.

That's the unlock.
