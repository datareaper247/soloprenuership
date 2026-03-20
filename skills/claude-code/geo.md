# /geo — Geographic Expansion Skill

> Usage: `/geo [command] [arguments]`
>
> Activate: "use geo skill" or `/geo help`

---

## ⚠️ Solo Founder Stage Gate

**International expansion is almost never the right move at <$50K MRR.**

| Stage | Verdict | Reason |
|-------|---------|--------|
| <$20K MRR | ❌ Stop | You don't have PMF in your home market. Expanding spreads the problem. |
| $20–$50K MRR | ⚠️ Test only | Runs a single localized landing page test. No full geo build. |
| $50K+ MRR with inbound signals | ✅ Go | Organic signups from a market = pull signal. Now it's worth analyzing. |
| $50K+ MRR without signals | ⚠️ Validate first | Use `/research market` before committing budget. |

**Common trap**: A founder at $8K MRR asks "should I expand to Europe?" The correct answer is almost always: fix your churn in your current market first. International complexity (legal, currency, support timezone, localization) multiplies operational load at exactly the stage where focus is your only advantage.

**Exception**: If you already have 10+ paying customers from a country without doing any targeting, that's a pull signal worth analyzing with `/geo analyze`.

If you invoked this skill and you're <$20K MRR without inbound international signals, Claude will surface this flag automatically.

---


## Overview

The geo skill turns Claude into an international expansion strategist. Every command applies the CAGE Distance Framework, Hofstede cultural dimensions, and localization best practices to give you a rigorous, actionable plan — not generic "go global" advice.

---

## CAGE Distance Framework (Used Across Commands)

CAGE quantifies how "far" a target market is from your home market across four dimensions. Greater distance = higher market entry risk and cost.

| Dimension | Factors | High distance signals |
|-----------|---------|----------------------|
| **Cultural** | Language, values, religion, social norms | Different language, collectivist vs individualist, conservative culture |
| **Administrative** | Legal system, currency, trade agreements, colonial ties | No trade treaty, different legal tradition, currency controls |
| **Geographic** | Physical distance, shared border, time zones, climate | > 8 hours away, landlocked, extreme climate difference |
| **Economic** | Income level, wealth distribution, economic infrastructure | GDP/capita ratio > 5×, poor payment infrastructure |

**Score each dimension 1–5** (1 = close, 5 = very distant). Total CAGE score > 12 signals a high-effort market entry.

---

## Commands

### `/geo analyze [country] [market]`

**Purpose**: Full market entry analysis for a target country and product category.

**Methodology**:
1. CAGE distance score vs home market
2. Market sizing: TAM / SAM / SOM using GDP, internet penetration, and industry verticals
3. Competitive landscape: top 5 local competitors + global players with local presence
4. Regulatory overview: data privacy, business registration, tax, sector-specific rules
5. Cultural fit: buying behavior, communication style, trust signals, price sensitivity
6. Infrastructure: payment methods, preferred billing currency, connectivity
7. Go-to-market path: direct vs partner vs acquisition
8. Risk matrix with mitigations

**Output format**:
```
## Market Entry Analysis: [Country] — [Market Category]

### CAGE Distance Score (vs [home market])
| Dimension | Score (1–5) | Key factors |
|-----------|-------------|------------|
| Cultural | | |
| Administrative | | |
| Geographic | | |
| Economic | | |
| **Total** | **/20** | |

Interpretation: [Low (≤8) / Medium (9–12) / High (>12)] difficulty

### Market Sizing
- TAM: $XB (total addressable market in country for this category)
- SAM: $XM (serviceable given your ICP and positioning)
- SOM (Year 1): $XM (realistically capturable at current stage)
- Key assumption: [biggest sizing assumption]

### Competitive Landscape
| Player | Type | Est. market share | Key strength | Key weakness |
|--------|------|------------------|-------------|-------------|

### Regulatory Snapshot
| Area | Requirement | Blocking? | Timeline to comply |
|------|-------------|-----------|-------------------|
| Data privacy | | | |
| Business registration | | | |
| VAT/digital services tax | | | |
| Sector-specific | | | |

### Cultural Fit Summary
- Buying behavior: [key norms — e.g. consensus decisions, long sales cycles, relationship-first]
- Communication style: [direct vs indirect, formal vs informal]
- Trust signals: [what buyers look for — local case studies, certifications, local pricing]
- Localization must-haves: [language, currency, payment methods, date formats]

### Go-to-Market Recommendation
**Recommended path**: [Direct / Channel partner / Reseller / Acquisition]
Rationale: [2-3 sentences]

Alternative path: [Second option and when to choose it]

### Risk Matrix
| Risk | Likelihood (H/M/L) | Impact (H/M/L) | Mitigation |
|------|--------------------|----------------|-----------|

### Go / No-Go Recommendation
**[GO / NO-GO / GO WITH CONDITIONS]**
Conditions: [if applicable]
Suggested sequencing: [e.g. "Enter UK first as low-CAGE stepping stone before Germany"]
```

---

### `/geo localize [file-or-content] [target-locale]`

**Purpose**: Translate AND culturally adapt content for a target market.

**Localization ≠ Translation**: Translation converts words. Localization converts meaning, context, and persuasion.

**Methodology**:
1. Translate using high-quality neural MT (DeepL for EU/JP; Google Translate for broader language coverage)
2. Cultural adaptation: replace idioms, adjust examples, reframe value propositions for local context
3. Formality calibration: match local business communication norms (Sie vs du in German; keigo in Japanese)
4. Legal sensitivity scan: flag phrases that carry different legal weight in target jurisdiction
5. SEO alignment: adapt for local search intent, not just literal keyword translation
6. Glossary enforcement: apply product-specific term mappings consistently

**Localization checklist per locale**:
```
LOCALE CHECKLIST: [locale code]
================================
[ ] Language: [language name]
[ ] Currency: [code + symbol position]
[ ] Date format: [e.g. DD.MM.YYYY for Germany]
[ ] Number format: [e.g. 1.000,00 for Germany vs 1,000.00 for US]
[ ] Address format: [field order + postal code placement]
[ ] Phone format: [ITU E.164 + local display format]
[ ] Text expansion: [German +30%, CJK may compress — UI tested?]
[ ] RTL required: [Arabic, Hebrew, Farsi — yes/no]
[ ] Legal boilerplate: [jurisdiction-specific required disclosures]
[ ] Payment methods: [local payment methods beyond Visa/MC]
```

**Output format**:
```
## Localized Content: [locale]

### Original ([source locale])
[Original content]

### Translated ([target locale])
[Translated text]

### Adaptation Notes
1. [Phrase X] → Changed to [Y] because [cultural reason]
2. [Example Z] → Replaced with [local equivalent] — [original was US-specific]
3. [Tone adjustment]: [what changed and why — e.g. more formal for Japanese market]

### Glossary Mappings Applied
| Source term | Target term | Notes |
|-------------|-------------|-------|

### Flags for Human Review
- [Phrase that may have legal implications in target jurisdiction]
- [Humor or idiom that may not land — confirm with native speaker]
```

---

### `/geo seo [keywords] --countries [list]`

**Purpose**: Multi-country keyword research with locale-specific SERP analysis.

**Methodology**:
1. Translate seed keywords into target language(s)
2. Identify native-language equivalents (not just direct translations — locals search differently)
3. Estimate search volume and keyword difficulty per locale
4. Analyze SERP features available in each locale (local packs, featured snippets, Shopping)
5. Competitor keyword gap: what do local competitors rank for that you don't?

**Output format**:
```
## Multi-Country Keyword Research: [Topic]

### Keyword Matrix
| Keyword (EN) | [Locale 1] | [Locale 2] | [Locale 3] |
|--------------|------------|------------|------------|
| [term] | [translation] Vol:X Diff:Y | | |

### Locale-Specific SERP Analysis

#### [Country 1] — [locale code]
- Dominant content type: [blog / product pages / videos / local business]
- SERP features present: [featured snippets / local packs / knowledge panels]
- Top-ranking domains: [who owns the SERPs in this market]
- Keyword gap opportunity: [terms with volume where no strong competitor ranks]
- Recommended content format: [long-form / comparison / how-to / tool page]

#### [Country 2] — [locale code]
...

### Opportunity Matrix
| Keyword (localized) | Locale | Volume | Difficulty | Opportunity score | Recommended action |
|---------------------|--------|--------|------------|------------------|--------------------|

### Content Roadmap (by locale)
Priority 1 (quick wins — low difficulty, high volume):
Priority 2 (medium-term — medium difficulty, high intent):
Priority 3 (long-term authority plays):
```

---

### `/geo market-entry [country]`

**Purpose**: Market entry strategy with direct / partner / acquisition recommendation.

**Entry mode framework**:
| Mode | Best when | Risk | Speed | Investment |
|------|-----------|------|-------|-----------|
| **Direct (digital)** | Low regulatory barrier, proven PLG motion, English-acceptable | Low | Fast | Low |
| **Local partner / reseller** | Strong relationship-buying culture, complex regulatory env. | Medium | Medium | Medium |
| **Hire local team** | Large SAM, language-critical product, high-touch sales | Medium | Slow | High |
| **Acquisition** | Speed to market, buy existing customer base | High | Fastest | Very high |

**Output format**:
```
## Market Entry Strategy: [Country]

### Entry Mode Recommendation
**Recommended**: [Mode] — [1-sentence rationale]
**Alternative if budget allows**: [Mode]
**Avoid**: [Mode] — [why it's wrong for this market]

### Phase 1: Validate (0–3 months, ~$X budget)
- Objective: [What you need to prove before committing]
- Actions:
  1. [Specific action — e.g. "Run localized landing page test with $2K ad spend"]
  2. [Action]
  3. [Action]
- Success criteria: [measurable signal to proceed]

### Phase 2: Establish (3–12 months, ~$X budget)
- Objective: [First revenue milestone]
- Actions: [key operational and go-to-market steps]
- Hires or partners needed: [specific roles/profiles]

### Phase 3: Scale (12–24 months)
- Objective: [Revenue target + market position]
- Investment required: $X
- Key risks at this stage: [list]

### Operational Checklist
[ ] Legal entity: [required type + timeline to establish]
[ ] Banking: [local account needed?]
[ ] Tax registration: [VAT / GST / DST requirements]
[ ] Contracts: [local language contracts required?]
[ ] Hiring: [local employment law implications]
[ ] Data residency: [any local data hosting requirements]
```

---

### `/geo cultural-audit [content]`

**Purpose**: Audit content for cultural fit and sensitivity issues in a target market.

**Evaluation dimensions** (based on Hofstede + GLOBE research):
| Dimension | Low score | High score | Examples |
|-----------|-----------|------------|---------|
| Power distance | Flat hierarchy messaging works | Authority/seniority signals matter | US low, Malaysia high |
| Individualism | Collective/team benefits | Personal achievement emphasis | Japan low, US high |
| Uncertainty avoidance | Risk-taking appeals work | Stability/safety proof needed | UK low, Germany high |
| Long-term orientation | Quick ROI messaging | Investment / partnership framing | US short, China long |
| Indulgence | Hedonic appeals | Duty/work appeals | Mexico high, China low |

**Output format**:
```
## Cultural Audit: [Target Country]

### Hofstede Dimensions for [Country]
| Dimension | Score | Implication for your content |
|-----------|-------|------------------------------|

### Content Review

#### Red Flags (Change before launching)
| Item | Current content | Issue | Suggested change |
|------|----------------|-------|-----------------|

#### Yellow Flags (Review with local expert)
| Item | Current content | Potential issue | Options |
|------|----------------|-----------------|---------|

#### Strengths (Content that will land well)
| Item | Why it works in this market |
|------|-----------------------------|

### Overall Fit Score: X/10
[2-3 sentence summary of overall cultural alignment]

### Priority Changes (before launch)
1. [Most critical change]
2. [Second]
3. [Third]
```

---

### `/geo hreflang [sitemap]`

**Purpose**: Generate a complete hreflang implementation specification.

**Implementation rules** (common mistakes prevented):
- Every locale page must reference ALL other locale pages (bidirectional requirement)
- `x-default` must point to the primary language version or a language-selector page
- Use BCP 47 locale codes (e.g. `en-US`, `de-DE`) not just language codes (`en`, `de`) for region-specific content
- URLs must be canonical (absolute, including HTTPS)
- Implement in both `<head>` HTML tags AND XML sitemap for full coverage

**Domain strategy trade-offs**:
| Strategy | Example | SEO | Trust | Cost |
|----------|---------|-----|-------|------|
| ccTLD | acme.de | Strong | High | High |
| Subdomain | de.acme.com | Medium | Medium | Low |
| Subdirectory | acme.com/de/ | Medium | Medium | Lowest |

**Output format**:
```
## hreflang Implementation Spec

### Domain Strategy Recommendation
**Recommended**: [strategy] — [rationale for your stage]

### HTML Implementation (in <head>)
For each page, include these link elements:

<!-- Page: /pricing -->
<link rel="alternate" hreflang="en-US" href="https://acme.com/pricing" />
<link rel="alternate" hreflang="de-DE" href="https://acme.com/de/preise" />
<link rel="alternate" hreflang="fr-FR" href="https://acme.com/fr/tarifs" />
<link rel="alternate" hreflang="x-default" href="https://acme.com/pricing" />

[Repeat for each page]

### XML Sitemap Implementation
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://acme.com/pricing</loc>
    <xhtml:link rel="alternate" hreflang="en-US" href="https://acme.com/pricing"/>
    <xhtml:link rel="alternate" hreflang="de-DE" href="https://acme.com/de/preise"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://acme.com/pricing"/>
  </url>
  ...
</urlset>

### Validation Checklist
[ ] Every locale references all other locales (bidirectional)
[ ] x-default tag present on all pages
[ ] All URLs are canonical (HTTPS, no trailing slash inconsistency)
[ ] Locale codes are BCP 47 format (not just "en" or "de")
[ ] Implemented in both HTML head AND XML sitemap
[ ] Sitemap submitted to Google Search Console for each locale
[ ] No orphaned locale pages (pages in one locale with no hreflang match)

### Tools to Validate Implementation
- Google Search Console: Coverage → International Targeting tab
- hreflang.org validator (free): paste sitemap URL
- Screaming Frog: crawl and export hreflang report
```

---

## Quality Standards (All Commands)

- CAGE distance must be scored for every market analysis — never skip it
- Cultural recommendations must cite specific Hofstede or GLOBE data dimensions, not just intuition
- All localization outputs must include an adaptation notes section — translation alone is never sufficient
- hreflang specs must include both HTML and XML sitemap implementations
- Every market entry recommendation must state the minimum viable test before full commitment
- Flag any regulatory requirement that is a hard blocker (cannot legally operate without resolving)
