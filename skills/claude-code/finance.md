# Finance Engine — The CFO Solo Founders Never Had

## Auto-Trigger (No Slash Command Needed)

Fires automatically when:
- "runway", "burn rate", "cash flow" mentioned → cash position analysis
- Pricing question → unit economics first, price recommendation second
- "How much is my company worth?" → multi-method valuation
- Revenue target mentioned → reverse-engineer the required metrics
- "I need to raise" / "thinking about fundraising" → pre-raise checklist + right timing signal
- "Should I hire?" → cash flow impact model before recommendation
- Any revenue goal → break it down to daily/weekly actions

---

## Why This Exists

Solo founders systematically make bad financial decisions because they lack a CFO:
- **Underpricing**: $49/mo when customers would pay $199/mo (leaves 300% on the table)
- **No unit economics**: Acquiring customers at $400 CAC when LTV is $200 (accelerates death)
- **No cash flow model**: "I have 6 months of runway" → actually 3 months with upcoming expenses
- **Wrong valuation beliefs**: "I need $1M to build this" → actually need $30K to validate demand
- **Exit blindness**: Building for 5 years then accepting first offer without understanding value

This skill is your CFO: it stops you from making the financial decisions that kill profitable companies.

---

## UNIT ECONOMICS ENGINE

### The Fundamental 4 Metrics

Every financial decision flows from these 4:

```
UNIT ECONOMICS SNAPSHOT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MRR:    $[X]       ← Monthly Recurring Revenue
CAC:    $[X]       ← Cost to Acquire 1 Customer
LTV:    $[X]       ← Lifetime Value (ARPU / Monthly Churn Rate)
LTV:CAC: [X]x     ← Must be ≥3x (healthy) or ≥5x (excellent)
Gross Margin: [X]% ← Revenue minus COGS (for SaaS: API costs, hosting, support)
CAC Payback: [X]mo ← How many months to recover CAC

HEALTH CHECK:
LTV:CAC <2x → DANGER: Acquiring customers is destroying value
LTV:CAC 2-3x → WARNING: Barely viable; focus on reducing CAC or increasing LTV
LTV:CAC 3-5x → HEALTHY: Standard SaaS
LTV:CAC >5x → EXCELLENT: Strong growth potential
CAC Payback >18mo → High risk: tighten acquisition spend
CAC Payback 12-18mo → Monitor: acceptable for low churn businesses
CAC Payback <12mo → Healthy: scale acquisition confidently
```

### LTV Calculator

```
LTV CALCULATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Method 1 (Simple): LTV = ARPU ÷ Monthly Churn Rate
  Example: $99/mo ARPU, 3% monthly churn → LTV = $99 ÷ 0.03 = $3,300

Method 2 (Gross Margin Adjusted): LTV = (ARPU × Gross Margin %) ÷ Churn
  Example: $99 × 85% ÷ 3% = $2,805 (more conservative, more accurate)

Method 3 (Expansion Revenue): LTV = (ARPU × Gross Margin + Monthly Expansion) ÷ Churn
  Use when: Net Revenue Retention > 100% (customers expand spending over time)

Which to use:
→ Pre-PMF (<20 customers): Method 1 (simple estimate)
→ Post-PMF: Method 2 (accuracy matters for acquisition decisions)
→ $20K+ MRR with expansion: Method 3 (full model)
```

### CAC Calculator

```
CAC CALCULATION (by channel):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CAC = Total Channel Spend ÷ New Customers From That Channel

Include in spend:
→ Paid ads: Ad spend + management time ($X/hr × hours)
→ SEO: Content creation time + tools ($X/hr × hours) ÷ 12-month attribution
→ Cold outreach: Time to research + write + follow up ($X/hr × hours)
→ Community: Time spent in communities ($X/hr × hours)
→ Events/conferences: Cost + travel + prep time

Hidden CAC trap: Founder time is NOT free. At $10K MRR, your time is worth ~$100/hr.
40 hours of cold outreach generating 5 customers = $800 CAC before counting any tools.

Blended CAC = Total all channels ÷ Total new customers across all channels
```

---

## CASH FLOW FORTRESS

### 12-Month Cash Flow Model

```
12-MONTH CASH FLOW MODEL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Starting cash: $[X]
Current MRR: $[X]
Monthly churn rate: [X]%
Monthly new MRR target: $[X]

Month-by-month projection:
Month 1: MRR × (1 - churn) + new_MRR - OpEx = Net cash
Month 2: [updated MRR] × (1 - churn) + new_MRR - OpEx = Net cash
...

Operating expenses (monthly):
→ Infrastructure (Vercel/AWS/Railway): $[X]
→ SaaS tools (analytics, email, CRM): $[X]
→ AI/API costs (OpenAI, Anthropic): $[X]
→ Marketing (ads, tools): $[X]
→ Founder salary/draw: $[X]
→ Contractor costs: $[X]
→ Misc (accountant, bank fees): $[X]

KEY OUTPUTS:
Break-even MRR: OpEx ÷ Gross Margin %
Runway (months): Cash ÷ Monthly Burn Rate
Runway extension per +$1K MRR: Calculated automatically

RULE: Never let runway drop below 6 months without active fundraise or cost cut.
Red zone: <3 months → crisis protocol fires.
```

### The Runway Reality Check

```
RUNWAY REALITY CHECK (fires whenever "runway" or "cash" mentioned):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Common founder mistake: "I have $30K left = 10 months at $3K/month burn"
Reality check: Add upcoming expenses:
→ Annual software renewals (often $2-5K lump)
→ Tax obligations (quarterly estimated taxes)
→ Equipment/contractor spikes
→ Personal emergency buffer

Adjusted runway formula:
True Runway = (Cash - Committed Expenses) ÷ Real Monthly Burn
where Real Monthly Burn = avg(last 3 months) × 1.2 (20% buffer)

The "18-month rule" (Sequoia Capital):
→ If bootstrapped: optimize for default alive (revenue > burn)
→ If venture-backed: maintain 18-month runway or raise now
→ If approaching 6 months: fundraise mode ON regardless

Default alive test: If acquisition rate stays flat, do you reach profitability before cash out?
```

---

## PRICING OPTIMIZATION ENGINE

### The 3-Tier Price Discovery Method

```
PRICING DISCOVERY (fires on any pricing question):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1: Calculate Problem Value
  "What does this problem cost your customer per month?"
  → Lost revenue, wasted time × hourly rate, compliance risk, missed opportunities
  Target price = 10-20% of problem value

Step 2: Van Westendorp Survey (4 questions)
  Ask 10+ target customers:
  1. "At what price would you consider this too cheap (unreliable)?" → FLOOR
  2. "At what price would this be a bargain?" → IDEAL LOW
  3. "At what price would this start to feel expensive?" → IDEAL HIGH
  4. "At what price would this be too expensive (you wouldn't buy)?" → CEILING
  Optimal price range: Between Q2 and Q3 answers

Step 3: Anchor Test
  Set initial price 2x what feels comfortable.
  Measure conversion for 2 weeks. If >3% convert → price is too low, raise again.
  If <1% convert → gather objection data first (is it price or value?)

Price escalation rule (Marc Lou Pattern):
  Start at [comfort price]. Announce increase when 20% of capacity filled.
  Never "discount" → always "grandfather." Scarcity of terms, not price.
```

### The Pricing Psychology Matrix

```
PRICING MODEL SELECTION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ONE-TIME PAYMENT wins when:
→ Clear discrete output (headshot, logo, template, course, report)
→ Customer doesn't want ongoing commitment
→ B2C with low average transaction
→ Conversion psychology: removes subscription anxiety

SUBSCRIPTION wins when:
→ Ongoing workflow integration (scheduling, analytics, CRM, reporting)
→ Product improves with continued use
→ Customer's problem is recurring, not one-time
→ LTV economics support customer acquisition cost

USAGE-BASED wins when:
→ Value is clearly tied to usage volume (API calls, seats, transactions)
→ Customers have variable usage (reduces churn from low-use months)
→ Customers start small and expand (usage = commitment signal)
→ Plaid, Twilio, Stripe model: land small, expand naturally

TIERED wins when:
→ Customer segments have dramatically different WTP
→ Features clearly map to value received by tier
→ Single price excludes either end of market

HYBRID (usage + subscription) wins when:
→ Enterprise wants predictability, SMB wants flexibility
→ Base fee covers infrastructure; usage covers variable costs
```

---

## VALUATION ENGINE

### Multi-Method Company Valuation

```
COMPANY VALUATION CALCULATOR:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Input your metrics:
→ Current ARR (Annual Recurring Revenue): $[X]
→ YoY Growth Rate: [X]%
→ Net Revenue Retention (NRR): [X]%
→ Gross Margin: [X]%
→ Monthly Churn: [X]%
→ CAC Payback Period: [X] months
→ Category: [SaaS / Marketplace / Content / Services / Other]

METHOD 1: ARR Multiple (most common for SaaS)
  Base multiple by growth rate:
  <20% YoY → 2-4x ARR
  20-50% YoY → 4-8x ARR
  50-100% YoY → 8-12x ARR
  >100% YoY → 12-20x ARR

  Adjustments (±):
  NRR >120%: +2-3x (customers expand — strongest signal)
  NRR 100-120%: +1x
  NRR <90%: -2x (customers are shrinking — red flag)
  Gross Margin >80%: +1x
  Gross Margin <60%: -2x
  Bootstrapped (no VC dilution): +0.5x to buyers who want clean cap table

METHOD 2: Acquirer ROI Method
  Strategic acquirer pays: ARR × (Acquirer's Revenue Multiple)
  If acquirer trades at 10x ARR: they can pay up to 10x your ARR and still create value
  Typical bootstrapped acquisition: 3-5x ARR
  Typical VC-backed growth acquisition: 5-10x ARR

METHOD 3: SDE Multiple (for profitable bootstrapped companies)
  SDE = Revenue - COGS - Operating Expenses (excluding founder salary)
  Typical SDE multiple: 2.5-4x for SaaS (higher than traditional business due to recurring revenue)

RULE: Use all 3 methods. Present range. Best exit preparation = optimize for NRR first,
then growth rate. These are the biggest multiple drivers.
```

### The Exit Readiness Checklist

```
EXIT READINESS AUDIT (fires when exit or acquisition mentioned):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Financial documentation (3 years):
□ Clean P&L (accrual basis)
□ MRR/ARR broken down by cohort
□ Churn analytics by customer segment
□ CAC by channel
□ LTV by customer segment
□ Net Revenue Retention month by month

Business transferability:
□ Product runs without founder in every process
□ Documentation for all key processes (SOPs)
□ No customer concentration >20% of revenue in single account
□ Tech stack documented; no single points of failure
□ IP is owned by company (not founder personally)

Growth proof:
□ 12+ months of consistent MRR growth
□ Defined, repeatable acquisition channel
□ NPS or Sean Ellis score documented
□ Customer testimonials and case studies

Common acquirers for bootstrapped SaaS:
→ MicroAcquire / Acquire.com (marketplace, 1-5x ARR)
→ Tiny Capital (technical founders, 3-5x ARR)
→ Ramen (profitable bootstrapped, 3-5x ARR)
→ Strategic buyers (your largest customers or competitors, 4-10x)
→ Private Equity (>$500K ARR threshold, 3-6x ARR)
```

---

## FUNDRAISING INTELLIGENCE

### When (and When NOT) to Raise

```
FUNDRAISING GATE (fires when "raise" or "investors" mentioned):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DO NOT RAISE if:
→ <$10K MRR (pre-PMF — investors will either say no or give bad terms)
→ Churn >5%/month (money poured into leaky bucket)
→ No repeatable acquisition channel (money doesn't help non-repeatable channels)
→ Bootstrapped to profitability is possible in <24 months (dilution not worth it)

CONSIDER RAISING if:
→ $20K+ MRR with proven repeatable acquisition channel
→ You need capital to hire BEFORE revenue catches up to the opportunity
→ Market is winner-take-all and speed matters more than margin
→ Your acquisition channel is paid (money directly converts to growth)

FUNDRAISING MATH CHECK:
If raising $500K at $2M post-money valuation = 25% dilution
You must believe the $500K gets you to a valuation where 75% of that value > 100% of current value
i.e., new_valuation × 75% > current_valuation

At what ARR would you be worth the post-money valuation you're raising at?
Reverse-engineer: Target ARR = Post-money ÷ Expected ARR multiple at exit stage

Alternative math check: "If I had $500K, could I get to $1M ARR?"
If yes → raise. If uncertain → build to $20K MRR first for better terms.
```

---

## REVENUE ARCHITECTURE BY STAGE

### The Revenue Mechanics That Work at Each Stage

```
$0 → $10K MRR MECHANICS:
→ Acquisition: Direct outreach ONLY (DMs, cold email, warm intros)
→ Pricing: One time or simple subscription, no complex tiers
→ Retention: Personal attention (your phone number, weekly calls)
→ Expansion: Manual (spot upsell on calls, no automated flows)
→ Weekly focus: 80% talking to customers, 20% building

$10K → $50K MRR MECHANICS:
→ Acquisition: 1 scalable channel emerges (SEO, community, or paid)
→ Pricing: Introduce annual plan (gives cash flow + retention signal)
→ Retention: Systematized onboarding + 30-day activation checklist
→ Expansion: Introduce tiered pricing with clear upgrade trigger
→ Weekly focus: 50% customer, 30% building, 20% marketing

$50K → $200K MRR MECHANICS:
→ Acquisition: 2 channels, with 1 primary and 1 backup
→ Pricing: Usage-based tier available; enterprise pilot program
→ Retention: CS system; customer health score; quarterly reviews
→ Expansion: In-app upgrade prompts; expansion revenue target (NRR >105%)
→ Weekly focus: 30% customer, 30% building, 30% marketing, 10% ops

$200K+ MRR MECHANICS:
→ Acquisition: Team running 3+ channels; affiliate/partner program
→ Pricing: Full tier structure; annual/multi-year contracts available
→ Retention: Dedicated CS; SLA commitments; customer advisory board
→ Expansion: Land-and-expand with seat/usage expansion built in
→ Weekly focus: 20% direct customer, 40% team/product, 40% strategy/BD
```

---

## The 5 Financial Mistakes That Kill Profitable Companies

1. **LTV blindness**: Growing MRR while CAC > LTV. The faster you grow, the faster you die.
2. **Annual plan addiction**: Converting 80% to annual gives great cash flow but masks churn. When those annuals don't renew: cliff.
3. **COGS ignorance**: AI API costs scale with users. Gross margin can collapse from 85% to 40% as you scale if you don't model it.
4. **Tax ambush**: Self-employment tax + estimated quarterly taxes often equal 30-40% of profit. Not modeling this destroys cash flow.
5. **Wrong first hire**: Hiring for growth (marketing) before fixing retention creates a churn machine. Fix retention first.

---

## Integration

Finance Engine connects to:
- `decide.md` → financial impact modeling fires before strategic decisions
- `morning.md` → MRR trajectory, runway update, unit economics health
- `growth.md` → channel economics, CAC tracking
- `validate.md` → pricing sanity check, unit economics gate
- `soloos-core` MCP → `calculate_ev` tool uses financial parameters

Log decisions to `context/financial-model.md`.
