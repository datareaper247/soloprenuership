# Geo — Geographic Expansion & International Growth

**Usage**: `/geo [command] "[context]"`

Full geographic expansion methodology — from market analysis through localization, international SEO, and cultural audits. Produces actionable plans for entering new markets.

---

## Commands

### `analyze` — Market Entry Analysis
**Usage**: `/geo analyze "[target country/region] for [product description]"`

Evaluates the attractiveness and feasibility of entering a specific geographic market.

#### Market Entry Analysis Framework

**Dimensions to evaluate**:
1. **Market attractiveness**: Size, growth, readiness for your category
2. **Competitive intensity**: Local and global competitors already present
3. **Customer readiness**: Awareness of the problem, willingness to pay, digital adoption
4. **Regulatory environment**: Compliance requirements, barriers to entry
5. **Go-to-market feasibility**: Channels available, cost of acquisition, language/culture requirements
6. **Operational requirements**: Support, legal entity, payments, tax

#### Output Format
```
MARKET ENTRY ANALYSIS: [COUNTRY/REGION]
=========================================
Product: [name]
Date: [date]
Analyst: [name/role]

EXECUTIVE SUMMARY
Recommendation: [Enter Now / Enter with Conditions / Monitor / Pass]
Overall Attractiveness Score: X/50
Top 3 reasons to enter: [bullets]
Top 3 risks: [bullets]

MARKET OVERVIEW
- Population: X million
- GDP per capita: $X (purchasing power context)
- Internet penetration: X%
- Mobile-first market: [Yes/No/Partially]
- Language(s): [Primary + secondary]
- Currency: [currency and FX stability]
- Business culture: [formal/informal, relationship vs. transactional, etc.]

MARKET SIZING
- Total relevant market (localized): [estimate with method]
- SaaS/software spending per company: $X avg (vs. US: $Y)
- Price sensitivity relative to US: [Higher/Similar/Lower pricing needed]
- Your SAM in this market: $X

COMPETITION ANALYSIS
Global competitors present: [list with estimated market share]
Local/regional competitors: [list — these are often strongest]
Market leader: [company — why they lead]
Gaps in competitive landscape: [unaddressed segments or needs]

CUSTOMER PROFILE
- Primary buyer: [role — does it differ from home market?]
- Decision process: [how long, who's involved — often longer in some markets]
- Key differences from home market ICP: [list]
- Local success stories (if any): [companies in the space that succeeded]

REGULATORY & COMPLIANCE
- Data residency requirements: [GDPR equivalent or local law]
- Industry-specific regulations: [if applicable]
- Entity requirements: [must you have local entity?]
- Tax implications: [VAT/GST, withholding tax]
- Employment law (if hiring locally): [key considerations]
- Barriers to entry: [anything that makes this harder]
- Estimated compliance cost: $X/year

PAYMENTS & FINANCIAL
- Preferred payment methods: [credit card / bank transfer / local method]
- Popular payment processors: [local options]
- Currency pricing: [local currency or USD? Recommendation]
- Payment infrastructure required: [what you'd need to set up]

GO-TO-MARKET FEASIBILITY
Primary acquisition channel for this market: [SEO / paid / partnerships / sales]
  Rationale: [why this channel works in this market]
  Estimated CAC (local): $X vs. home market $Y
  Key localization needed for GTM: [list]

Language: [English viable? / Must localize / Partial localization acceptable]
Localization effort estimate: [L/M/H]

Distribution partners available: [local resellers, agencies, integrators]
Media / press landscape: [key publications, influencers in this market]
Local tech community: [active? conferences? communities?]

OPERATIONAL REQUIREMENTS
- Support language: [English only / must offer local language]
- Support timezone: [hours needed to cover]
- Customer success: [local team needed or can run remotely?]
- Local team recommendation: [Yes/No/Later] — rationale

MARKET ENTRY OPTIONS
Option A: [Digital-only / no local presence]
  Investment: $X | Timeline: X months | Risk: Low
  Best if: [conditions]

Option B: [Local partnerships]
  Investment: $X | Timeline: X months | Risk: Medium
  Best if: [conditions]

Option C: [Local team / entity]
  Investment: $X | Timeline: X months | Risk: Higher but higher ceiling]
  Best if: [conditions]

Recommendation: Option [X] because [rationale]

MARKET ENTRY SCORECARD
| Dimension | Score (1-5) | Evidence |
|-----------|-------------|----------|
| Market size | | |
| Market growth | | |
| Competitive gap | | |
| Customer readiness | | |
| GTM feasibility | | |
| Regulatory ease | | |
| Operational cost | | |
| Price point viability | | |
| Language/culture fit | | |
| Strategic importance | | |
| TOTAL | /50 | |

90-DAY ENTRY PLAN (if entering)
Month 1: [Research, localization, compliance setup]
Month 2: [Soft launch, first customers, learning]
Month 3: [Optimize, scale what works, decide next investment]

Key milestones for continued investment:
- [Milestone 1]: Target X customers by month Y
- [Milestone 2]: CAC < $X
- [Milestone 3]: [Specific signal of PMF in market]
```

---

### `localize` — Localization Strategy & Checklist
**Usage**: `/geo localize "[product] for [target language/market]"`

Complete localization framework across product, content, and go-to-market.

#### Output Format
```
LOCALIZATION STRATEGY: [LANGUAGE/MARKET]
==========================================
Product: [name]
Target: [language code — e.g., de-DE, fr-FR, pt-BR]
Scope: [Full product / Marketing only / MVP localization]

LOCALIZATION SCOPE DECISION FRAMEWORK
| Tier | What it includes | When to do it |
|------|-----------------|---------------|
| Tier 1 (MVP) | UI strings, error messages, onboarding | Before soft launch |
| Tier 2 (Core) | + Help docs, email sequences, landing page | When validating market |
| Tier 3 (Full) | + Blog/SEO content, sales materials, support | After PMF signals |
Recommendation: [Tier + rationale]

PRODUCT LOCALIZATION CHECKLIST

UI/UX
[ ] All UI strings extracted to i18n file (never hardcoded text)
[ ] Translations reviewed by native speaker (not just machine translation)
[ ] Text expansion accounted for (German runs 30% longer than English)
[ ] RTL layout supported (if Arabic/Hebrew/Persian)
[ ] Date format localized: [e.g., DD.MM.YYYY for German, not MM/DD/YYYY]
[ ] Number format: [e.g., 1.000,00 vs 1,000.00]
[ ] Currency display: [local currency symbol placement]
[ ] Phone number format: [local format]
[ ] Address format: [local postal format]
[ ] Name order: [First Last vs Last First — matters for East Asian markets]

CONTENT LOCALIZATION
[ ] Landing page: headline and key messages adapted (not just translated)
[ ] Case studies: use local customer examples if possible
[ ] Blog/SEO content: written for local keywords (not translated from English)
[ ] Email sequences: adapted for local tone and communication norms
[ ] Pricing page: local currency, local VAT if applicable
[ ] Legal pages: jurisdiction-specific terms and privacy policy
[ ] FAQ: localized to address locally relevant questions
[ ] Support documentation: core help articles translated

CULTURAL ADAPTATION (beyond translation)
[ ] Imagery: Does hero image reflect local demographic?
[ ] Examples and analogies: Are they locally relevant?
[ ] Humor: Removed or adapted (humor rarely translates)
[ ] Colors: Any colors to avoid? (White = mourning in some Asian cultures)
[ ] Icons: Gestures/icons culturally appropriate?
[ ] Trust signals: Local logos, local certifications, local currency

LOCAL BUSINESS PRACTICES
[ ] Billing: Preferred payment method available (e.g., SEPA for Germany)
[ ] Invoicing: Local invoice format (required in many EU countries)
[ ] VAT: VAT number collection implemented
[ ] Contract: Local language contract option available for enterprise

TECHNICAL LOCALIZATION
[ ] i18n library implemented: [i18next / react-intl / locale-specific]
[ ] Language detection: Auto-detect browser language
[ ] Language switcher: Accessible from all pages
[ ] URL structure: /de/ or .de domain or ?lang=de (pick one, be consistent)
[ ] Hreflang tags: Correctly implemented for all language variants
[ ] SEO: Meta titles/descriptions localized, not translated
[ ] Fonts: Verify fonts support target character set (Cyrillic, CJK, Arabic)
[ ] Right-to-left (RTL): CSS direction and layout if applicable

LOCALIZATION WORKFLOW
Translation workflow:
  1. Extract strings from codebase
  2. Send to human translator (native speaker with product context)
  3. Review by second native speaker
  4. QA in product (check UI with full-length strings)
  5. Ship

Ongoing:
  - New strings flagged in CI/CD
  - Translation turnaround: X days
  - Review cycle: Quarterly

TRANSLATION PARTNER OPTIONS
[ ] Professional agency (highest quality, $X-X/word)
[ ] Crowdsourced platform (Crowdin, Transifex) (community-assisted)
[ ] Native-speaking freelancer (good balance for small scope)
[ ] Machine translation + human review (only for low-priority content)
Recommendation: [Option + rationale]

LOCALIZATION QA CHECKLIST
[ ] Native speaker full product walkthrough completed
[ ] No untranslated strings visible in UI
[ ] No text overflow (strings too long for UI containers)
[ ] Date/number formatting correct throughout
[ ] All links work (no English-only landing pages from localized UI)
[ ] Email sends use correct language based on user setting
[ ] Legal/compliance content reviewed by local counsel (if applicable)
```

---

### `seo` — International/Geo SEO Strategy
**Usage**: `/geo seo "[domain and target markets]"`

Geo-targeted SEO strategy including technical implementation, content strategy, and local link building.

#### Output Format
```
INTERNATIONAL SEO STRATEGY
============================
Domain: [domain]
Current markets: [list]
Target new markets: [list]

TECHNICAL STRUCTURE DECISION

Option A: ccTLD (country code top-level domains)
  Structure: de.yourdomain.com OR yourdomain.de
  Pros: Strongest geo-signal to Google, trusted by local users
  Cons: Each domain needs to build authority separately
  Use when: Committed to a market long-term, have resources to build separate sites

Option B: Subdirectories (RECOMMENDED for most)
  Structure: yourdomain.com/de/ | yourdomain.com/fr/
  Pros: Shares domain authority, easier to manage, scalable
  Cons: Slightly weaker geo-signal than ccTLD
  Use when: Starting international expansion, limited resources

Option C: Subdomains
  Structure: de.yourdomain.com
  Pros: Easier to set up than ccTLD
  Cons: Treated somewhat like separate sites by Google
  Use when: Technical reasons require it

Recommendation: [Option + rationale]

HREFLANG IMPLEMENTATION
Critical rules:
1. Every localized page must reference ALL its language variants
2. Always include x-default for language-selector pages
3. Must be bidirectional (each page references the other)
4. URLs must be absolute, not relative
5. Must be consistent: if in <head>, also return in HTTP headers or sitemap

Hreflang tag template:
<link rel="alternate" hreflang="[lang-country]" href="[absolute-URL]" />
<link rel="alternate" hreflang="x-default" href="[default-URL]" />

Languages and codes to implement:
| Market | Hreflang code | URL |
|--------|--------------|-----|
| [Market 1] | [code e.g., de-DE] | [url] |
| [Market 2] | [code] | [url] |

KEYWORD STRATEGY PER MARKET

Do NOT just translate English keywords. Research local search behavior:
1. Run keyword research in local language
2. Local competitors may rank for different terms
3. Search volume distribution differs by market

Market: [Country]
| English keyword | Local equivalent | Local volume | Difficulty | Priority |
|-----------------|-----------------|-------------|------------|----------|
| [keyword] | [local keyword] | Xk/mo | Med | High |

CONTENT STRATEGY

Tier 1 — Translate and adapt (core commercial pages):
- Homepage
- Product/feature pages
- Pricing page
- Landing pages for top campaigns

Tier 2 — Create locally (SEO-performing blog content):
- Do NOT translate English blog posts for SEO
- Research LOCAL keyword opportunities
- Write content that ranks for LOCAL searches
- Use local examples, local case studies

Tier 3 — English acceptable:
- Technical documentation (for developer markets)
- Release notes
- Less-trafficked support articles

LOCAL LINK BUILDING
Links from local domains signal geo-relevance to Google.

Strategies for each market:
1. Local directory listings (business directories, industry directories)
2. Local press coverage (pitch local tech/business press)
3. Local partnership/integration pages (co-marketing with local tools)
4. Local industry associations
5. Local events and sponsorships (get on events pages)
6. Translated guest posts on local blogs

Target domains for [Market]:
- [Local directory 1]
- [Local tech media outlet]
- [Industry association]

GOOGLE SEARCH CONSOLE SETUP
[ ] Add each subdirectory/ccTLD as separate property
[ ] Set geographic target per property
[ ] Submit localized sitemaps
[ ] Monitor international targeting report
[ ] Monitor hreflang errors

MEASUREMENT
| Market | Organic Traffic | Target (6mo) | Primary keywords ranking |
|--------|----------------|-------------|--------------------------|
| [Market 1] | X/mo | Y/mo | [list top 5] |

Review cadence: Monthly for active markets, quarterly for new entries.
```

---

### `market-entry` — Full Market Entry Plan
**Usage**: `/geo market-entry "[product] entering [country/region]"`

Produces an executable 90-day market entry plan.

#### Output Format
```
MARKET ENTRY PLAN: [COUNTRY]
==============================
Product: [name]
Entry approach: [Option chosen from geo analyze]
Budget: $[X]
Timeline: [start date] - [90 days]
Owner: [who is accountable]

SUCCESS CRITERIA (pre-defined before entry)
- Month 1: [First milestone — e.g., 50 signups, 5 paying customers]
- Month 2: [Second milestone — e.g., $5k MRR, CAC < $X]
- Month 3: [Go/No-Go milestone — e.g., $15k MRR or 40% "very disappointed" survey]

PHASE 1: FOUNDATION (Days 1-30)

Legal & Compliance (Week 1-2)
[ ] Legal review of compliance requirements complete
[ ] Privacy policy updated for local law
[ ] Tax setup complete (if selling to local customers)
[ ] Payment method enabled (local payment method if required)

Localization (Week 1-3)
[ ] Tier 1 localization complete (core UI, landing page, pricing)
[ ] Native speaker review done
[ ] Hreflang and technical SEO setup
[ ] Local landing page live

Analytics & Measurement (Week 1)
[ ] Local UTM parameters set up
[ ] Local conversion tracking configured
[ ] Market-specific dashboard created

PHASE 2: SOFT LAUNCH (Days 31-60)

Acquisition
[ ] First local paid campaign launched ($X budget)
[ ] 5-10 warm outbound prospects contacted
[ ] Local community presence established (relevant forums, Slack, LinkedIn groups)
[ ] First local press/media outreach

Conversion Optimization
[ ] 50 users acquired — qualitative interviews scheduled
[ ] Local onboarding flow monitored for friction
[ ] Support tickets from local users reviewed and patterns noted

Learning Loop
[ ] Week 5 review: first CAC data, qualitative themes
[ ] Adjust messaging based on early signals
[ ] Identify one experiment to improve conversion

PHASE 3: OPTIMIZE & SCALE (Days 61-90)

Based on Phase 2 learnings:
[ ] Top-performing channel identified — double down
[ ] Messaging refined based on customer language
[ ] First local case study or testimonial captured
[ ] Referral mechanism enabled for local market
[ ] 90-day go/no-go decision: [criteria for continuing vs. deprioritizing]

BUDGET ALLOCATION
| Category | Budget | Notes |
|----------|--------|-------|
| Localization | $X | Translation, native review |
| Paid acquisition | $X | Test budget, 2-3 channels |
| Tools/infrastructure | $X | Local payments, compliance |
| PR/outreach | $X | Local media, community |
| Travel (if any) | $X | On-site if required |
| TOTAL | $X | |

RISKS & MITIGATIONS
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Higher CAC than modeled | Medium | High | Set CAC ceiling, pause if exceeded |
| Regulatory surprise | Low | High | Legal review in Month 1 |
| Product-market fit doesn't transfer | Medium | High | 90-day go/no-go with clear criteria |
| Competition responds | Low | Medium | Competitive monitoring, differentiation |
```

---

### `cultural-audit` — Cultural Fit & Sensitivity Audit
**Usage**: `/geo cultural-audit "[product or content] for [market]"`

Audits product, messaging, and marketing for cultural fit and potential sensitivity issues.

#### Output Format
```
CULTURAL AUDIT: [PRODUCT/CONTENT] FOR [MARKET]
================================================
Market: [Country/Region]
Auditor note: [Ideal to have native from target culture review this]
Date: [date]

COMMUNICATION STYLE MATRIX
| Dimension | Home market | [Target market] | Adjustment needed |
|-----------|------------|-----------------|-------------------|
| Directness | Direct | High/Low-context | [example] |
| Formality | Informal | Formal/Informal | [adjust to formal "Sie" in German, etc.] |
| Humor | Used | Avoid/Adapt | [be specific] |
| Urgency language | Common | Inappropriate | [e.g., "limited time!" may feel pushy] |
| Testimonials | First-name | Full name + title | [credibility signals differ] |

CONTENT & IMAGERY REVIEW

Text/Messaging
[ ] Idioms and colloquialisms checked (idioms don't translate)
[ ] Sports/pop culture references: [relevant to target market or should be removed]
[ ] Measurement units: [metric vs. imperial — US uses imperial, rest of world metric]
[ ] Legal/compliance language: [jurisdiction-appropriate]
[ ] Date references: [month/day order, fiscal year differences]

Imagery
[ ] People shown reflect target market demographic
[ ] Hand gestures used: [thumbs up = offensive in some Middle East markets]
[ ] Colors: [white = mourning in parts of Asia; green = religious significance in some markets]
[ ] Icons: [mail icon, phone icon — are they recognizable locally?]
[ ] Money/finance images: [local currency shown?]

TRUST SIGNALS BY MARKET
What builds trust in [target market]:
- Local customers / logos (not US logos for EU market)
- Local certifications or compliance badges
- Local phone number (not just 1-800 US number)
- Local address (even if virtual office)
- Language precision (sloppy translation = low trust)
- [Market-specific trust signals]

TABOOS & SENSITIVITIES
[ ] No religious references that could be misinterpreted
[ ] No political content or imagery
[ ] No insensitive cultural stereotypes
[ ] [Specific taboos for this market — research required]

PRICING PSYCHOLOGY BY MARKET
- Price anchoring: [local norms for price presentation]
- Discount culture: [Germans are discount-driven; some markets expect negotiation]
- Free trial: [length expectations may differ]
- Annual vs. monthly: [local preference]
- Local payment expectation: [SEPA, Boleto, Alipay, etc.]

RECOMMENDATIONS
Critical fixes (cultural risks):
1. [Issue] — Fix: [specific change]

Important improvements:
1. [Opportunity]

Nice-to-haves (polish):
1. [Enhancement]

SIGN-OFF REQUIREMENTS
[ ] Native speaker linguistic review
[ ] Native speaker cultural review (different person than translator)
[ ] Local legal counsel review (for regulated content)
[ ] Product manager sign-off on adaptation scope
```

---

## Geographic Expansion Mental Models

### Sequencing Markets
Don't expand to all markets at once. Use this prioritization framework:
1. **English-first**: UK, Canada, Australia before non-English (lower cost, higher speed)
2. **Similarity cluster**: Markets similar to your home market (regulation, buyer behavior, channels)
3. **Largest TAM**: Larger markets before smaller (German-speaking DACH before Netherlands, despite Netherlands being more English-friendly)
4. **Strategic positioning**: Sometimes a smaller market is a strategic beach-head (Singapore for SE Asia access)

### The Localization Debt Trap
Many companies under-invest in localization, ship a poor experience, get few customers, conclude "that market doesn't work," and never try again — when actually the market was fine but the localized experience was too poor to convert. If you enter, localize properly. A mediocre product in English competing against a mediocre product in German will lose every time.

### When to NOT Expand Geo
- You haven't hit PMF in your home market
- Your team is smaller than 10 people
- Your current market still has significant untapped growth
- You can't commit to proper localization resources
- Your unit economics don't support higher CAC of new markets
