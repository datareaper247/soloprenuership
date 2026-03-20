# Example: /decide running adversarial debate on free tier

**Command used**: `/decide "Should I add a free tier to Rankly?"`

**Context**: Rankly is a keyword rank tracking tool at $4,200 MRR (140 customers × $30/mo).
Founder is considering a free tier after 3 prospects said "I'd try it if it was free first."

---

## Input

```
/decide "Should I add a free tier to Rankly?"

Context:
- Product: Rankly — daily keyword rank tracking with Slack alerts
- Current: $30/mo only, 140 customers, $4,200 MRR
- Growth: flat for 6 weeks
- Trigger: 3 recent prospects said they'd try it free first
- Concern: will free tier cannibalize paid?
```

---

## Output

```
DECISION: Should I add a free tier to Rankly?
Date: 2026-03-20
════════════════════════════════════════════════════

THE DEBATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPERATOR (Pragmatist):
"6 weeks of flat growth is a real signal. You've proven $30/mo pricing works
for 140 customers, which means the product has value. The question is whether
flat growth means (a) your distribution is broken or (b) your funnel converts
badly. A free tier fixes (b) — it doesn't fix (a). Before adding complexity,
diagnose which problem you actually have."

Evidence for free tier:
- 3 prospects explicitly said they'd try free first
- Flat growth suggests conversion problem exists somewhere
- Free tier creates top-of-funnel SEO lift ('free keyword tracker')
- Trial-to-paid conversion data is more valuable than assumptions

Evidence against:
- 3 prospects isn't a sample size — it's noise
- Flat growth for 6 weeks could be distribution, not conversion
- Free tier adds infrastructure cost and support burden
- Risk: existing customers ask for downgrade or feel price-anchored

────────────────────────────────────────────────────

DEVIL'S ADVOCATE (Contrarian):
"You're about to solve a problem you haven't proven exists.

Three prospects said 'I'd try it free' — but did they say why they didn't
pay? Did you ask? 'I'd try it free' is not the same as 'the price is the
reason I didn't convert.' They may have not converted because:
- They didn't believe it worked (→ fix: free trial, not free tier)
- They didn't trust you (→ fix: social proof, not free tier)
- The product doesn't solve their specific problem (→ fix: ICP, not pricing)
- They were browsing, not buying (→ fix: qualification, not pricing)

A free tier answers 'can I test before buying?' — which a 14-day free trial
already answers at lower cost and risk. Why build a permanent free tier
when a free trial gives the same signal for $0 infrastructure cost?

Also: you're at $4,200 MRR and flat for 6 weeks. That's a distribution
problem, not a conversion rate problem. Where are your leads coming from?
If you're not generating new qualified leads, free tiers don't help."

────────────────────────────────────────────────────

MARKET EXPERT (Revenue Lens):
"Let's look at what similar tools do:

Semrush: No free tier, 7-day trial → $129/mo. Converted at scale.
Ahrefs: No free tier, trial at $7 → $99/mo.
Mangools: Free trial, then $29/mo. $5M+ ARR.
SerpRobot: Free tier (10 keywords) → paid plans.

The ones with free tiers attract a very different ICP: side-project developers,
freelancers, early-stage founders. These convert to paid at 2-5%.

Your current ICP at $30/mo is more likely professional SEOs and small
agencies. Free-tier users skew toward people who won't pay.

The question is: is your ICP actually people who need to test first,
or are you acquiring the wrong leads?"

════════════════════════════════════════════════════
OPTIONS COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option A: Add free tier (5 keywords, no alerts)
  Revenue impact: Unknown — adds top-of-funnel but conversion rate unclear
  Cost: Engineering time (estimate 2-3 weeks), ongoing infrastructure + support
  Risk: Existing customers see free tier and request downgrade; free users
        never convert; support burden grows without revenue
  Reversibility: Hard to remove once launched — users build workflows on free tier

Option B: Add free trial (14 days, full access)
  Revenue impact: Likely positive — removes "I need to see it first" objection
  Cost: Billing system change only (1-2 days of work)
  Risk: Trial users abuse system; churn after trial if onboarding weak
  Reversibility: Easy to change or remove

Option C: Diagnose first, then decide
  Action: Talk to the 3 prospects who said free + 5 churned users.
           Ask: "What would have made you pay $30/mo?" Listen hard.
  Cost: 5 hours of calls
  Risk: None
  Reversibility: N/A — you're gathering data, not building

════════════════════════════════════════════════════
RECOMMENDATION
════════════════════════════════════════════════════
Recommendation: Option C first, Option B if confirmed.
Confidence: High
Reversibility: Option C is fully reversible; Option B is easy to change
Speed: Option C takes 1 week; Option B takes 2 days to ship after

WHY:
- 3 data points isn't enough to build a permanent free tier
- A free trial (Option B) gives you 80% of the conversion benefit at 5% of the cost
- If calls reveal that "price is the barrier" → Option B fixes it immediately
- If calls reveal something else → you've avoided 2-3 weeks of wrong building

KILL SIGNAL:
If after adding free trial (Option B) your trial-to-paid conversion is
below 15% at 30 days, the problem is not pricing — it's product value,
onboarding, or ICP fit. Free tier won't fix those either.

FIRST ACTION (today):
Email the 3 prospects who mentioned free: "Quick question — what would
have made you sign up at $30/mo without a free tier?" One sentence, no pitch.

════════════════════════════════════════════════════
```

---

## What This Example Demonstrates

1. **The Devil's Advocate voice prevents the most common founder mistake** — solving a problem you haven't diagnosed
2. **Market Expert adds the competitor pricing lens automatically** — without the founder needing to research it
3. **Options comparison forces explicit cost/reversibility thinking** — not just "good idea vs. bad idea"
4. **The kill signal is the most underused feature** — it tells you when to stop before you've sunk too much
5. **First action is always today-executable** — not "think about it" but "send this email today"

The founder in this example sent the 3 emails. Two didn't respond. One said:
"Honestly I just wasn't sure the Google Search Console integration would work with my setup."
That's an onboarding/trust problem, not a pricing problem.
They added a 14-day free trial instead of a free tier. Conversion from trial to paid: 22%.
