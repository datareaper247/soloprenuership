# MARKET INTELLIGENCE
## Category Maps, Unit Economics, Pricing Benchmarks (2025–2026)

> Reference file for Claude when making market claims. Check this before any market sizing statement.
> All figures from publicly disclosed founder data and documented case studies.

---

## CATEGORY SATURATION MAP (2025–2026)

### Dead on Arrival — Don't Build
These categories are functionally over for new entrants without massive differentiation:

| Category | Why Dead | Who Killed It |
|---|---|---|
| General AI writing assistants | Native LLM interfaces absorbed use case | ChatGPT, Claude, Gemini |
| Grammar/spell check | Built into every writing surface | Grammarly free + native OS tools |
| Background removers | Free tools commoditized to $0 | Remove.bg free tier, Canva, Adobe |
| Basic image upscalers | Commoditized, free everywhere | Various free tools |
| AI article spinners | Penalized by Google, no legitimate use | Algorithm updates |
| Generic AI chatbots | Race to bottom, no moat possible | Every LLM provider |
| AI caption generators (generic) | TikTok/Instagram native tools suffice | Platform feature parity |

---

### Heavily Saturated — Need Clear Differentiation
Viable with quality moat + strong brand + specific niche:

| Category | Differentiation That Works | What Doesn't Work |
|---|---|---|
| AI headshot generators | Custom LoRA fine-tuning, output quality, specific profession niches | Generic styles, slow turnaround |
| Resume/cover letter tools | Job board integration, industry-specific templates, LinkedIn import | Generic templates |
| Logo generators | Specific industry style systems (legal, medical, tech startup) | Generic AI output |
| General social media tools | Platform-specific analytics + scheduling combined | Scheduling alone |
| AI SEO content | Niche topic authority (one industry only) + fact verification | General content mills |

---

### Viable with Niche Focus
Strong category fundamentals, but requires extreme specificity:

| Category | Winning Niche Pattern | Target TAM | Notes |
|---|---|---|---|
| AI writing for specific professions | Legal briefs, medical notes, real estate listings | 10K-500K practitioners in niche | Compliance angle multiplies retention |
| AI tools for specific platforms | YouTube creator tools (Subscribr model), Substack, LinkedIn | Platform's creator base | Marketplace distribution available |
| AI tools for specific industries | Dental practice management, insurance claims, construction | Industry-defined; 50K-500K businesses | High ARPU possible |
| Code review for legacy stacks | COBOL, Salesforce Apex, mainframe | Enterprise-specific | Very high ACV, long sales cycle |

---

### Open / Under-Served — Build Opportunity
Fragmented, high-pain, no dominant player, structural demand:

| Category | Why Open | Addressable Market | First-Mover Window |
|---|---|---|---|
| **Compliance document automation** | Fragmented regulatory landscape, SMBs underserved, high pain | ~15K Davis-Bacon subcontractors alone | 2-3 years |
| Regulated-industry workflow AI | Dental, pharmacy, healthcare — compliance-adjacent | 200K+ small practices in US | 2-4 years |
| SMB financial/accounting automation | Bookkeeping + reconciliation for trades, small businesses | Millions of SMBs | 2-4 years |
| Voice/audio for professionals | Meeting summaries for healthcare, legal, therapy | 3M+ licensed practitioners in US | 1-2 years |
| Trade contractor tools | Estimating, bid management, change orders | 600K+ US contractors | 2-3 years |
| Government contract management | SAM.gov, USASpending.gov complexity | 200K+ federal contractors | 2-4 years |

**Best open category** (from research synthesis): Compliance document generation (prevailing wage, GFE, CMMC) has the strongest combination of: structural retention + pricing power + moat-buildability + distribution clarity (identifiable customer, cold-outreach-able).

---

### Emerging — First-Mover Still Possible
Early market, infrastructure forming, 2025-2027 window:

| Category | Signal | Why Now |
|---|---|---|
| Agentic workflow orchestration (vertical-specific) | LLMs reliable enough for multi-step automation | API quality crossed threshold in 2024 |
| AI for physical-world compliance | OSHA documentation, safety inspections | Regulatory environment tightening |
| Vertical-specific RAG tools | Where hallucination tolerance is zero (legal, medical) | Retrieval quality improved enough |
| AI-powered government contract tools | SAM.gov complexity + federal AI adoption | Government digital transformation spending |

---

## UNIT ECONOMICS DATABASE

### By Product Category (Real Data, 2023-2025)

| Category | Gross Margin | Typical LTV | Typical CAC | LTV:CAC | Monthly Churn | Notes |
|---|---|---|---|---|---|---|
| AI image generation (one-time) | 92-96% | $29-49 | <$5 (viral/SEO) | >5x | N/A | One-time payment |
| Developer tools (subscription) | 85-92% | $400-800 | $20-50 (community) | 8-40x | 5-8% | Low support burden |
| B2B SaaS ($50-200/mo) | 75-85% | $800-3,000 | $100-300 | 5-10x | 4-8% | Support scales |
| Compliance SaaS ($100-500/mo) | 88-95% | $2,400-12,000 | $150-400 | 6-30x | 1-3% | Regulatory lock-in |
| Consumer AI ($9-29/mo) | 70-80% | $100-200 | $30-80 (paid) | 2-4x | 10-20% | Hard to scale profitably |
| AI content tools ($29-99/mo) | 78-88% | $300-800 | $50-150 | 3-8x | 7-15% | SEO-driven acquisition |

**Healthy benchmarks**:
- LTV:CAC > 3x: Viable
- LTV:CAC > 5x: Healthy
- LTV:CAC > 10x: Excellent (community/SEO driven)
- Monthly churn < 5%: Healthy for B2B
- Monthly churn < 3%: Healthy for compliance

---

## AI API COST STRUCTURE

### Text Generation (as of early 2026)

| Model | Input $/1M tokens | Output $/1M tokens | Practical $/request |
|---|---|---|---|
| GPT-4o | $5 | $15 | $0.002-0.015 |
| GPT-4o-mini | $0.15 | $0.60 | $0.0001-0.001 |
| Claude Sonnet 4.6 | $3 | $15 | $0.002-0.012 |
| Claude Haiku 4.5 | $0.80 | $4 | $0.0003-0.003 |
| Gemini 2.0 Flash | $0.075 | $0.30 | <$0.001 |

**At $19/mo pricing**: User can make ~1,000-15,000 typical requests before COGS > revenue. Depends on model choice.

### Image Generation

| Service | Cost/Image | Quality | Notes |
|---|---|---|---|
| Replicate (FLUX.1-dev) | $0.025-0.055 | High | Best quality/cost for fine-tuning |
| Replicate (SDXL) | $0.002-0.008 | Medium-High | Faster, older |
| OpenAI DALL-E 3 | $0.04 (1024px standard) | High | No fine-tuning |
| fal.ai (FLUX) | $0.006-0.050 | High | Fast inference |

**HeadshotPro economics**: 20 images at $0.025 avg = $0.50 COGS vs $29-49 revenue = 98-99% gross margin.

### Document Processing

| Task | Model | Cost/Document |
|---|---|---|
| Extract structured data from PDF | Claude/GPT-4o | $0.01-0.05 |
| Generate compliance form | Claude Sonnet | $0.005-0.02 |
| Classify + route document | GPT-4o-mini | $0.001-0.005 |
| Full document audit (long) | Claude Sonnet | $0.05-0.25 |

**Compliance SaaS margin check**: $97/mo, 50 forms/mo at $0.02 = $1 COGS → 99% margin. At heavy usage (500 forms/mo) = $10 COGS → 90% margin.

---

## PRICING CONVERSION BENCHMARKS

### Real Conversion Data (2023-2025)

| Product Type | Price Point | Conversion Rate (visitors→paid) | Annual Uplift |
|---|---|---|---|
| AI headshots (one-time) | $29-49 | 3-8% | N/A |
| Developer tools (one-time) | $29-99 | 2-5% | N/A |
| Boilerplate/template | $99-299 | 1-4% | N/A |
| SaaS individual | $9-19/mo | 2-5% | 20-30% choose annual |
| SaaS professional | $29-49/mo | 1-3% | 25-35% choose annual |
| SaaS team | $79-149/mo | 0.5-2% | 30-40% choose annual |
| Compliance tool | $97-297/mo | 2-6% (direct outreach) | 40-50% choose annual |

**Annual conversion rule**: 20-35% of new paid users choose annual when offered at 20% discount. Annual users have 2-4x lower churn.

---

## MOAT STRENGTH MATRIX

| Moat Type | How to Build | Clone Resistance | Build Time | Examples |
|---|---|---|---|---|
| Proprietary dataset | Ingest unique data source | Strong | 3-6 months | Subscribr (YouTube benchmarks), compliance tools (reg parsing) |
| Fine-tuned model | Train on domain corpus | Medium | 2-4 months | HeadshotPro LoRA, PhotoAI |
| User-specific learning | Style profiles, history, preferences | Medium | 6+ months accumulation | Tweet Hunter, Jasper |
| API/integration depth | Deep CMS/ERP/CRM integration | Strong | 3-9 months | Platform-specific tools |
| Network effects | Reviews, benchmarks, community data | Very Strong | 12+ months | Niche review platforms |
| Compliance data | Regulatory parsing + form logic | Very Strong | 6-12 months | Prevailing wage tools, CMMC tools |

**Assessment question**: "Can a funded competitor replicate this in 30 days?" If yes → weak moat. If 6+ months → defensible.

---

## ACQUISITION CHANNEL PERFORMANCE

### By Stage and Channel (Real CAC Data)

| Channel | Best Stage | Typical CAC | Notes |
|---|---|---|---|
| Community (authentic) | $0-5K MRR | ~$0-10 | Requires authentic member status |
| Direct outreach (cold) | $0-5K MRR | $50-200/conversion | 0.5-3% demo rate from cold email |
| Audience (existing) | Any | ~$0-5 | Marc Lou, Pieter Levels model |
| HackerNews | Launch only | ~$0-20 (organic) | One-time event, not repeatable |
| ProductHunt | Launch only | ~$5-50 | Diminishing returns, launch day spike |
| SEO (bottom-funnel) | $5-20K MRR | $20-80 (long-term) | 90-day minimum |
| Affiliate/partnerships | $10K+ MRR | $50-200 | Needs product-market fit first |
| Paid (Meta/Google) | $20K+ MRR | $100-400 | Only if LTV:CAC >3x confirmed |
| App Store (iOS/Android) | Any | Platform-dependent | Platform takes 30%, but distribution |

---

## LEGAL + TAX STRUCTURES

Best structure by revenue level (from documented founder practices):

| Annual Revenue | Optimal Structure | Effective Tax | Setup Cost | Annual Compliance |
|---|---|---|---|---|
| $0-50K | US LLC (pass-through) or sole proprietor | Varies by state/bracket | $100-500 | $0-500 |
| $50K-200K | US S-Corp election (saves $5-15K/yr self-employment tax) | ~20-25% effective | $500-1,000 | $500-2,000 |
| $200K+ (IP-heavy) | Dutch BV + Innovation Box | ~5% on IP income | €2,000-5,000 | €3,000-8,000 |
| $200K+ (retained earnings) | Estonian OÜ via e-Residency | 0% corp on retained profits | €200 + notary | €800-2,000 |
| $100K+ (APAC-focused) | Singapore Pte Ltd | 17% (first $74K exempt) | S$1,000-2,000 | S$2,000-5,000 |

**Dutch BV + Innovation Box** (Pieter Levels): 5% effective rate on IP income vs 25.8% standard. Requires documented R&D (WBSO declaration). Break-even vs US LLC: ~$80-100K/year IP income.

**Estonian OÜ** (Marc Lou): 0% corporate tax on retained profits. 20% withholding when dividends paid. 100% online setup via e-Residency.

---

## SUCCESS RATE REALITY CHECK

From analysis of ~300 AI micro-products launched 2023-2024:

```
$0 MRR (never monetized):     45-50%
$1-$500 MRR:                  25-30%
$500-$2K MRR:                 12-15%
$2K-$5K MRR:                   6-8%
$5K-$20K MRR:                  3-5%
$20K-$50K MRR:               1.5-2%
$50K+ MRR:                     <1%
```

**Survival at 18 months**: Of those who reached $5K MRR, 35-45% maintained or grew it at 18 months. 55-65% declined due to competition or founder attention shift.

**Top failure modes (ranked)**:
1. ChatGPT/Claude absorbed the use case: 25-30%
2. Commoditization without differentiation: 25-30%
3. No sustainable acquisition channel: 20-25%
4. Unit economics collapsed (API cost increases): 8-12%
5. Founder burnout / lost interest: 5-10%

---

## SaaS BENCHMARK REFERENCE TABLE

Reference when evaluating founder health metrics. Use these before any "is this good or bad" assessment.

| Metric | Healthy | Warning | Kill Signal | Notes |
|--------|---------|---------|-------------|-------|
| Monthly churn (B2B SaaS) | <3% | 5-7% | >8% | General SaaS benchmark |
| Monthly churn (compliance tools) | <1.5% | 2-4% | >4% | Compliance = higher retention |
| Monthly churn (consumer SaaS) | <5% | 7-10% | >12% | Consumer churns faster |
| D30 retention | >45% | 30-40% | <30% | Core PMF signal |
| D90 retention | >35% | 20-30% | <20% | Long-term value signal |
| LTV:CAC ratio | >3x | 2-3x | <2x | Below 2x = broken unit economics |
| Gross margin (SaaS) | >75% | 60-75% | <60% | AI products: watch API costs |
| Annual plan take rate | >25% | 10-20% | <10% | Higher = healthier cash flow |
| NRR (Net Revenue Retention) | >100% | 90-100% | <90% | >110% = expansion-led growth |
| Support time at $20K MRR | <30 min/day | 1-2 hrs/day | >2 hrs/day | >2 hrs = systematize now |
| Cold email to demo rate | >1.5% | 0.5-1% | <0.5% | Below 0.5% = wrong message or ICP |
| Demo to paid conversion | >20% | 10-15% | <10% | Below 10% = price, objections, or wrong buyer |
| PMF signal (Sean Ellis) | >40% "very disappointed" | 25-40% | <25% | Below 25% = do not scale |
| MoM growth ($0-$10K ARR) | >20% | 10-20% | <10% for 2+ months | Below 10% for 2 months = change hypothesis |
| MoM growth ($10K-$100K ARR) | >15% | 8-15% | <8% for 3 months | Channel saturation or PMF incomplete |
| MoM growth ($100K+ ARR) | >10% | 5-10% | <5% for 3 months | Requires new channel or pricing expansion |
| Working hours at $30K MRR | 30-35 hrs/wk | 35-45 hrs/wk | >45 hrs/wk | Leverage problem, not capacity problem |
| CAC payback period | <6 months | 6-12 months | >12 months | Long payback = cash flow risk |
| API cost as % of revenue | <15% | 15-25% | >30% | AI-specific: watch LLM cost creep |
| Activation rate (to milestone) | >60% | 40-60% | <40% | Onboarding problem if low |
| Time to activation milestone | <10 minutes | 10-30 minutes | >30 minutes | >30 min = redesign onboarding |

### Stage-Specific Benchmark Application

| Stage | Primary Benchmark | Secondary Benchmark | What to Ignore |
|-------|------------------|--------------------|----|
| $0-$10K ARR | Demo to paid >15% | D30 retention >40% | Monthly churn (too few customers for signal) |
| $10K-$100K ARR | MoM growth >15% | NRR >95% | Gross margin (fine-tune later) |
| $100K-$500K ARR | NRR >100% | LTV:CAC >3x | MoM absolute growth (focus on rates) |
| $500K+ ARR | NRR >110% | Annual take rate >30% | CAC alone (look at blended + payback) |

### Moat-Type Retention Benchmarks

| Product Type | 6-Month Retention | 12-Month Retention | Monthly Churn |
|---|---|---|---|
| Compliance tools | 80-90% | 70-80% | 1-2% |
| Workflow lock-in (B2B) | 70-80% | 60-70% | 2-3% |
| Data/analytics tools | 60-70% | 50-60% | 3-5% |
| General B2B SaaS | 50-65% | 40-55% | 4-6% |
| Consumer/prosumer | 35-50% | 25-40% | 6-10% |
| AI commoditized tools | 25-40% | 15-30% | 8-14% |

*Sources: Baremetrics Open benchmarks, SaaStr annual survey, Stripe Atlas published data, ChartMogul SaaS benchmarks, 300+ documented founder cases (Indie Hackers, Twitter/X, podcasts 2018-2026)*

