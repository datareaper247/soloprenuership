# Phase 3: SCALE

> Build the engine that grows without you.

## Goal

Go from $1K MRR to $50K MRR through systematic, compounding growth channels.

**Milestones**:
- Month 1-3: $1K → $5K MRR (product-market fit signal)
- Month 4-6: $5K → $15K MRR (channel repeatability)
- Month 7-12: $15K → $50K MRR (system compounding)

## The Scale Framework

### Pillar 1: Retention First

You cannot fill a leaky bucket. Retention comes before acquisition.

**Target benchmarks**:
- Monthly churn < 3% (annual churn < 30%)
- NPS > 40
- Activation > 70%
- Feature adoption of core loop > 80%

**Retention levers**:
1. **Onboarding optimization** — Get users to value in <5 minutes
2. **Success milestones** — Email triggers at each aha moment
3. **Power user identification** — Find your 20% who get 80% of value
4. **Expansion revenue** — Usage-based billing, seat expansion, upgrades

### Pillar 2: Content Moat (SEO Engine)

Solo founder's most powerful long-term lever. Takes 6 months to work, compounds forever.

**Content Strategy**:
```
Tier 1 (Highest intent): "[Competitor] alternatives" "[Problem] software"
Tier 2 (Educational): "How to [solve problem]" "Best [tool category]"
Tier 3 (Awareness): Industry trends, case studies, frameworks

Publishing cadence:
- Week 1-2: 4 long-form posts (2000+ words, Tier 1)
- Week 3-4: 4 long-form posts (Tier 2)
- Ongoing: 2 posts/week minimum
```

**Content Factory Agent Swarm**:
```
Deploy: framework/swarms/content-swarm.yaml
Weekly output: 10 pieces of content from 2 hours of human input
  - 2 long-form blog posts (SEO optimized)
  - 5 social posts (LinkedIn/Twitter distribution)
  - 1 email newsletter
  - 2 short-form repurposing
```

### Pillar 3: Community Distribution

Organic distribution in communities where your customers gather.

**Community playbook**:
```
Phase 1 (Month 1-2): Lurk and learn
  - Join 5-10 relevant Slack/Discord/Reddit communities
  - Identify top questions, recurring problems
  - Answer helpfully, no promotion

Phase 2 (Month 2-4): Become a known contributor
  - Answer 2-3 questions per week in each community
  - Share genuinely useful content (not your product)
  - Build relationships with power users

Phase 3 (Month 4+): Soft product integration
  - When relevant, mention your tool as a solution
  - Share case studies (permission-based)
  - Run community-exclusive offers
```

### Pillar 4: Paid Acquisition (After Organic Proof)

Only start paid after:
- Organic CAC is established
- LTV is proven (3+ months retention data)
- Conversion rate on landing page > 5%

**Paid channel priority**:
1. Google Search (high-intent keywords only)
2. LinkedIn (B2B, job title targeting)
3. Reddit (targeted subreddit ads)
4. Meta (if B2C or prosumer)

**Budget framework**:
```
Start: $500/month test budget
Measure: CAC < LTV/3 (payback in 4 months)
Scale: If CAC target hit → 2x budget monthly until CAC rises
Cap: Never exceed 30% of monthly revenue on paid
```

### Pillar 5: Partnership & Integration Growth

Build integrations where your customers already live.

**Integration strategy**:
```
Step 1: Identify the tools your customers use daily
Step 2: Build native integrations (Zapier, direct API)
Step 3: Submit to their marketplace/directory
Step 4: Co-market with complementary tools
```

**Partnership types**:
- Integration partners: Access their customer base via marketplace
- Referral partners: Complementary tools (revenue share)
- Resellers: Agencies serving your customer segment
- Affiliates: Influencers/creators in your space

## Growth Agent Swarm

**Deploy**: `framework/swarms/growth-swarm.yaml`

**Acquisition Agent** → Runs experiments on new channels
**Activation Agent** → Analyzes onboarding drop-off, suggests fixes
**Retention Agent** → Monitors churn signals, triggers intervention
**Content Agent** → Produces SEO content at scale
**Revenue Agent** → Models pricing changes, expansion opportunities

## Solo Founder Growth Stack

```
Analytics:     PostHog (product) + Plausible (web)
Email:         Loops.so or Customer.io (lifecycle automation)
SEO:           Ahrefs or Semrush (content strategy)
CRM:           Attio or Folk (lightweight B2B CRM)
Content:       Notion (planning) + Claude (generation)
Social:        Buffer (scheduling) + Typefully (Twitter)
Support:       Plain or Intercom (lightweight)
Referrals:     Rewardful or PartnerStack
Landing pages: Framer (A/B testing)
```

## The Weekly Growth Ritual

**Monday (30 min)**:
- Review last week's metrics dashboard
- Flag churn risks (anyone not active in 7 days)
- Check content performance

**Tuesday (2 hours)**:
- 2 customer calls
- Update content calendar
- Review support tickets for product signals

**Wednesday (3 hours)**:
- Ship retention fix or activation improvement
- Publish 1 content piece
- Community engagement (answer 3 questions)

**Thursday (2 hours)**:
- Growth experiment design + launch
- Email newsletter if weekly cadence
- Outreach to 5 potential partners/users

**Friday (1 hour)**:
- Week in review
- Update metrics dashboard
- Queue next week's content

## Metrics Dashboard

Track weekly, review monthly:

```
Revenue:
  MRR: $___
  MRR Growth MoM: ___%
  Churn MRR: $___
  Net Revenue Retention: ___%

Users:
  New signups: ___
  Activated users: ___
  Activation rate: ___%
  Active users (30d): ___
  Churned users: ___

Acquisition:
  Organic traffic: ___
  Trial signups: ___
  Paid → Trial conversion: ___%
  Trial → Paid conversion: ___%
  CAC (blended): $___

Economics:
  ARPU: $___
  LTV: $___
  LTV:CAC ratio: ___
  Payback period: ___ months
```

## Outputs

- [ ] `scale/growth-experiments.md` — Running log of experiments
- [ ] `scale/content-calendar.md` — 90-day content plan
- [ ] `scale/metrics-dashboard.md` — Weekly metrics template
- [ ] `scale/partner-pipeline.md` — Integration & partner tracking
- [ ] `scale/channel-analysis.md` — Channel ROI analysis

## Next Phase

✅ Scale complete ($50K+ MRR, strong NRR) → `playbooks/4-exit/`
