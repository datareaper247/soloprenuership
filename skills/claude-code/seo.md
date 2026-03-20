# SEO — Search Engine Optimization Toolbox

**Usage**: `/seo [command] "[topic or URL]"`

Full SEO methodology from keyword research through technical audits. Produces actionable, prioritized outputs for each stage of SEO work.

---

## Commands

### `research` — Keyword Research
**Usage**: `/seo research "[seed keyword or topic]"`

#### Keyword Research Methodology

**Step 1: Seed Expansion**
Starting from the seed keyword, generate:
- Exact match variants
- Question-form variants (who, what, when, where, why, how)
- Problem-state variants ("can't", "not working", "alternative to")
- Comparison variants ("vs", "alternative", "review")
- Long-tail modifiers (best, free, cheap, enterprise, [year])
- LSI/semantic variants (related concepts and synonyms)

**Step 2: Intent Classification**
Classify each keyword by search intent:
- **Informational**: Want to learn (how to, what is, guide, tutorial)
- **Navigational**: Looking for a specific site/brand
- **Commercial investigation**: Researching before buying (best, review, comparison, alternative)
- **Transactional**: Ready to act (buy, pricing, sign up, free trial, download)

**Step 3: Opportunity Scoring**
Each keyword scored on:
- Volume estimate (use pattern matching to major categories)
- Competition level (number and quality of ranking pages)
- Business relevance (0-10 — how directly tied to your product)
- Current ranking position (if known)
- Featured snippet opportunity (question format, definition, listicle)

**Step 4: Cluster into Topics**
Group keywords into topic clusters with one "pillar" keyword and multiple supporting/long-tail keywords.

#### Output Format
```
KEYWORD RESEARCH REPORT: [SEED TOPIC]
=======================================
Date: [date]
Domain context: [product/site being researched]

KEYWORD UNIVERSE SUMMARY
Total keywords identified: X
High priority (score 7+): X
Quick wins (low competition): X
Featured snippet opportunities: X

TOP OPPORTUNITY KEYWORDS
| Keyword | Volume Est. | Competition | Intent | Biz Relevance | Priority Score |
|---------|-------------|-------------|--------|----------------|----------------|
| [kw] | Xk/mo | Low/Med/High | Info/Comm/Trans | 8/10 | 🔴High |
| ... | | | | | |

TOPIC CLUSTERS

CLUSTER 1: [Cluster Name]
Pillar keyword: [main keyword] | Volume: Xk | Intent: [type]
Supporting keywords:
  - [long-tail 1] | Volume: Xk | Intent: [type]
  - [long-tail 2] | Volume: Xk
  - [question variant] | Volume: Xk
  - [comparison variant] | Volume: Xk
Content asset needed: [pillar page / blog post / comparison page]

CLUSTER 2: ...
[repeat]

QUICK WIN KEYWORDS (low competition, decent volume)
| Keyword | Volume | Why It's a Win | Content Needed |
|---------|--------|----------------|----------------|
| ... | | | |

COMPETITOR KEYWORD GAPS
Keywords competitors rank for that you don't: [list]
(These are your highest-value targets)

FEATURED SNIPPET OPPORTUNITIES
| Keyword | Snippet Type | Current Snippet Holder | Win Strategy |
|---------|-------------|------------------------|--------------|
| ... | Definition/List/Table | [domain] | [approach] |

NEGATIVE KEYWORDS / EXCLUSIONS
Keywords that look related but aren't worth targeting: [list + reason]

RECOMMENDED CONTENT PRIORITY
1. [Content piece] → targets [cluster] → [expected impact]
2. ...
```

---

### `brief` — Content Brief Creation
**Usage**: `/seo brief "[target keyword]"`

A content brief so detailed that any writer (human or AI) can produce a ranking article from it.

#### Output Format
```
SEO CONTENT BRIEF
==================
Target Keyword: [keyword]
Secondary Keywords: [list]
Monthly Search Volume: ~X
Competition: [Low/Medium/High]
Search Intent: [Informational / Commercial / Transactional]
Content Goal: [Rank #1 / Featured snippet / Link acquisition / Conversion]

CURRENT SERP ANALYSIS
Top 3 ranking pages:
1. [URL] — Title: [title] — Approx. word count: X — Strengths: [what makes it rank]
2. [URL] — ...
3. [URL] — ...

What the current results do well: [patterns in top results]
What they're MISSING (your opportunity): [gaps to fill]
Featured snippet currently shows: [content type / no snippet]

CONTENT SPECIFICATIONS
Recommended length: X,000 words
Recommended format: [How-to / Listicle / Guide / Comparison / Definition]
Reading level target: Grade 8-10
Content angle: [Your unique positioning — why your piece will be BETTER]

REQUIRED ELEMENTS
[ ] Primary keyword in H1 (exact match or close variant)
[ ] Primary keyword in first 100 words
[ ] Primary keyword in at least 2 H2s
[ ] Meta title (include keyword, <65 chars)
[ ] Meta description (include keyword, CTA, <160 chars)
[ ] Table of contents (for 1,500+ word pieces)
[ ] FAQ section (target featured snippets)
[ ] Internal links: [2-3 specific pages to link to]
[ ] External links: [1-2 authoritative sources]
[ ] Image alt text with keyword

CONTENT OUTLINE

H1: [Suggested title — must include keyword]

INTRODUCTION
- Hook: [specific angle — surprising stat, bold claim, or relevant question]
- Promise: what reader will learn/be able to do
- Brief context for why this matters

H2: [First major section — should answer "what is" if informational]
  H3: [Subsection if needed]
  H3: [Subsection]

H2: [Second major section]
  Key points to cover:
  - [specific point with evidence]
  - [specific point]
  - [data/stat to include if available]
  H3: [Subsection]

H2: [Third major section]
...

H2: [Comparison section if applicable]
  Include: comparison table

H2: Frequently Asked Questions About [Topic]
  Q: [Question 1 — how people actually search it]
  A: [Answer in 40-60 words — formatted for featured snippet]
  Q: [Question 2]
  A: [Answer]
  [3-5 FAQs total]

CONCLUSION
- Summarize top 3 insights
- Clear next step for reader
- Internal link to related resource or conversion page

SCHEMA MARKUP RECOMMENDATION
Type: [Article / FAQ / HowTo / Product]
Reason: [why this schema fits]

ON-PAGE SEO CHECKLIST
[ ] Keyword in URL slug (short, clean: /target-keyword/)
[ ] Keyword in title tag and H1
[ ] Keyword in meta description
[ ] Keyword in first paragraph
[ ] Keyword in image alt text
[ ] Semantic keywords distributed naturally
[ ] Internal links to hub/pillar pages
[ ] Table of contents with anchor links
[ ] Schema markup implemented
[ ] Page speed < 3 seconds
[ ] Mobile responsive

LINK BUILDING STRATEGY FOR THIS PAGE
Primary link type: [Resource link / Guest post / Competitor link reclamation]
Target linking domains: [types of sites that would naturally link to this]
Outreach angle: [why someone would link to this specific piece]
```

---

### `audit` — On-Page SEO Audit
**Usage**: `/seo audit "[URL or page description]"`

#### Audit Categories and Checks

**Technical On-Page**
- Title tag: length (50-65 chars), keyword presence, uniqueness, click-worthiness
- Meta description: length (150-160 chars), keyword presence, CTA present
- H1: one only, contains keyword, matches search intent
- H2-H6: logical hierarchy, keyword variations present
- URL: short, descriptive, keyword-containing, no parameters or dates
- Canonical tag: present and pointing to correct URL
- Schema markup: appropriate type implemented

**Content Quality**
- Word count vs. competing pages
- Keyword density (natural, not stuffed)
- Reading level and sentence length
- Unique angle or insight vs. competing content
- Freshness (last updated date)
- E-E-A-T signals (Experience, Expertise, Authority, Trustworthiness)

**Internal Linking**
- Links from relevant high-authority pages on same site
- Links to relevant pages from this page
- Anchor text variation (exact match, partial match, branded, naked URL)
- Number of internal links (enough, not excessive)

**Images and Media**
- Alt text on all images
- File size optimized
- Descriptive filenames
- Video/rich media present (can increase dwell time)

**User Experience Signals**
- Page load speed
- Mobile friendliness
- Core Web Vitals (LCP, CLS, FID)
- Bounce rate signals (estimated from content quality)

#### Output Format
```
SEO AUDIT REPORT: [URL or Page Name]
======================================
Date: [date]
Overall Score: X/100
Priority: [High / Medium / Low urgency fixes]

CRITICAL ISSUES (fix immediately)
1. [Issue]: [Specific problem] → [Exact fix]
2. [Issue]: ...

HIGH IMPACT IMPROVEMENTS
1. [Opportunity]: [What to do] → [Expected impact]
2. ...

TECHNICAL CHECKLIST
| Element | Current State | Status | Recommendation |
|---------|--------------|--------|----------------|
| Title tag | "[current title]" | ✅/⚠️/❌ | [fix if needed] |
| Meta desc | "[current]" | ✅/⚠️/❌ | [fix if needed] |
| H1 | "[current]" | ✅/⚠️/❌ | [fix if needed] |
| H2s | X H2 tags | ✅/⚠️/❌ | [fix if needed] |
| URL | [url] | ✅/⚠️/❌ | [fix if needed] |
| Word count | X words | ✅/⚠️/❌ | [target: X] |
| Internal links | X links | ✅/⚠️/❌ | [recommendation] |
| Images | X images, X with alt | ✅/⚠️/❌ | [fix] |
| Schema | [type or none] | ✅/⚠️/❌ | [recommendation] |
| Mobile | [assessment] | ✅/⚠️/❌ | |
| Page speed | [est.] | ✅/⚠️/❌ | |

CONTENT QUALITY ASSESSMENT
Unique angle vs. competition: [Strong/Adequate/Weak]
E-E-A-T signals: [assessment]
Content gaps vs. top competitors: [list]
Featured snippet potential: [Yes/Maybe/No] — [type]

RECOMMENDED REWRITE SECTIONS
[Specific sections to improve with guidance]

PRIORITY ACTION LIST
1. [Action] — Impact: High — Effort: Low — ETA: [days]
2. ...
```

---

### `gaps` — Competitive Content Gap Analysis
**Usage**: `/seo gaps "[your domain] vs [competitor domain(s)]"`

Identifies keywords and content topics your competitors rank for that you don't.

#### Output Format
```
CONTENT GAP ANALYSIS
=====================
Domains analyzed: [yours] vs [competitors]
Date: [date]

HIGHEST PRIORITY GAPS
(Keywords competitors rank for, you don't, with commercial value)

| Keyword | Volume | Competitor Ranking | Your Position | Content to Create |
|---------|--------|-------------------|---------------|-------------------|
| ... | Xk | [domain] #X | Not ranking | [content type] |

TOPIC GAPS BY CATEGORY

Category: [Topic area]
- Competitor has [X pages] on this topic; you have [Y]
- Key keywords missing: [list]
- Recommended content: [specific content pieces]

QUICK WIN GAPS
(Low competition, decent volume, competitor ranked #4-10 — easiest to beat)
| Keyword | Volume | Best Competitor Pos. | Difficulty | Action |
|---------|--------|---------------------|------------|--------|
| ... | | | | |

CONTENT INVENTORY COMPARISON
| Content Category | Competitor A | Competitor B | You | Gap |
|-----------------|-------------|-------------|-----|-----|
| Blog posts | X | Y | Z | +/- |
| Feature pages | | | | |
| Comparison pages | | | | |
| Integration pages | | | | |
| Use case pages | | | | |

90-DAY CONTENT PLAN TO CLOSE GAPS
Month 1: [Top 4 content pieces — focus on highest opportunity gaps]
Month 2: [Next 4 pieces]
Month 3: [Next 4 pieces]
```

---

### `content-plan` — SEO Content Calendar
**Usage**: `/seo content-plan "[site or product] [timeframe: 30/60/90 days]"`

#### Output Format
```
SEO CONTENT PLAN: [X] Days
============================
Domain: [site]
Goal: [Traffic target / Keyword rankings target]

CONTENT STRATEGY SUMMARY
- Total pieces: X
- Pillar pages: X
- Supporting blog posts: X
- Comparison pages: X
- Feature/use case pages: X
- Integration pages: X

PRIORITIZATION CRITERIA (how this list was ranked)
1. Search volume × commercial intent
2. Competitive difficulty (targeting winnable positions)
3. Internal linking value to pillar pages
4. Alignment with product messaging

CONTENT CALENDAR

WEEK 1-2
| # | Title | Target Keyword | Volume | Intent | Type | CTA | Owner |
|---|-------|---------------|--------|--------|------|-----|-------|
| 1 | | | | | | | |

WEEK 3-4
[same table]

[Continue for full timeframe]

CONTENT ARCHITECTURE
[Diagram showing pillar-cluster relationships in text format]
Pillar: [Topic] → supporting: [list of supporting pieces]
Pillar: [Topic] → supporting: [list]

INTERNAL LINKING PLAN
| New Page | Link FROM These Pages | Link TO These Pages |
|----------|----------------------|---------------------|
| ... | | |

EXPECTED IMPACT
Month 1: [baseline, foundational content published]
Month 2: [pages begin indexing, early rankings]
Month 3: [traffic begins building on early pieces]
6 months: [realistic traffic projection]

SUCCESS METRICS
- Pages ranking top 10: X (from current Y)
- Organic traffic: X sessions/mo (from current Y)
- Organic conversions: X/mo (from current Y)
```

---

### `technical` — Technical SEO Checklist
**Usage**: `/seo technical "[site URL or description]"`

#### Full Technical SEO Checklist

**Crawlability**
- [ ] robots.txt: exists, not blocking important pages, not blocking CSS/JS
- [ ] XML sitemap: exists, submitted to GSC/Bing, no broken URLs, auto-updating
- [ ] No orphan pages (all important pages linked from site)
- [ ] Crawl depth: important pages within 3 clicks of homepage
- [ ] Pagination: proper rel=prev/next or paginated pages consolidated
- [ ] Faceted navigation: filtered URLs blocked or canonicalized appropriately

**Indexability**
- [ ] No unintentional noindex tags on important pages
- [ ] Canonical tags: present, correct, no chains or conflicts
- [ ] 404s: custom 404 page, no important pages returning 404
- [ ] Redirect chains: no chains longer than 1 hop
- [ ] HTTPS: full site on HTTPS, no mixed content
- [ ] Hreflang: correctly implemented for international sites

**Site Structure**
- [ ] URL structure: clean, descriptive, consistent hierarchy
- [ ] Breadcrumbs: implemented and in schema markup
- [ ] Site architecture: shallow, logical, supports topical authority
- [ ] Internal linking: contextual links, distributed PageRank effectively

**Speed (Core Web Vitals)**
- [ ] LCP (Largest Contentful Paint): < 2.5 seconds
- [ ] CLS (Cumulative Layout Shift): < 0.1
- [ ] FID/INP (Interaction to Next Paint): < 200ms
- [ ] Time to First Byte (TTFB): < 800ms
- [ ] Image optimization: WebP format, lazy loading, compressed
- [ ] CSS/JS: minified, defer non-critical, eliminate render-blocking resources
- [ ] Hosting/CDN: appropriate for audience geography

**Mobile**
- [ ] Mobile-first indexing ready
- [ ] No intrusive interstitials
- [ ] Touch targets min 48px
- [ ] Text readable without zooming
- [ ] No horizontal scroll

**Structured Data**
- [ ] Organization schema on homepage
- [ ] WebSite schema with SearchAction (sitelinks search box)
- [ ] BreadcrumbList on all pages
- [ ] Article schema on blog posts
- [ ] FAQPage schema on FAQ sections
- [ ] Product/Review schema on product pages
- [ ] No schema validation errors (test with Google Rich Results Test)

**International (if applicable)**
- [ ] hreflang attributes: correct language/region codes, bidirectional, x-default present
- [ ] Country-specific domains or subdirectories
- [ ] Local address and phone in schema

#### Output Format
```
TECHNICAL SEO AUDIT: [SITE]
============================
Date: [date]
Severity Summary: [X critical, Y high, Z medium]

CRITICAL ISSUES (blocking rankings or indexing)
1. [Issue] — Impact: [what it's causing] — Fix: [exact steps]

HIGH PRIORITY ISSUES
1. [Issue] — Fix: [steps] — Effort: [hours/days]

MEDIUM PRIORITY
1. [Issue] — Fix: [steps]

QUICK WINS (easy fixes, meaningful impact)
1. [Issue] — Fix: [steps] — Time: [minutes]

CORE WEB VITALS
| Metric | Current | Target | Status | Fix |
|--------|---------|--------|--------|-----|
| LCP | Xs | <2.5s | ✅/⚠️/❌ | |
| CLS | X | <0.1 | | |
| INP | Xms | <200ms | | |

STRUCTURED DATA STATUS
[What's implemented, what's missing, any errors]

INDEXING STATUS
- Total pages indexed: X
- Total pages on site: X
- Unintentionally not indexed: [count + pages]

RECOMMENDED IMPLEMENTATION ROADMAP
Sprint 1 (Week 1-2): [Critical fixes]
Sprint 2 (Week 3-4): [High priority]
Sprint 3 (Month 2): [Medium priority]
```

---

## SEO Mental Models

### Search Intent First
Before any keyword targeting decision, ask: "What does someone searching this actually want?" Google rewards pages that best satisfy the intent, not just keyword-matching pages.

### Topical Authority Over Single-Page Rankings
The modern SEO game is about proving your site is the best resource on a topic. This means pillar pages + clusters, not isolated posts.

### E-E-A-T Signals
For every content decision, ask: How does this page demonstrate Experience, Expertise, Authority, and Trust? (Author bios, citations, original research, testimonials, and credentials all matter.)

### The Compound Content Effect
SEO content compounds. A piece published today may not rank for 3-6 months. A piece that's ranked for 2 years continues to compound. Always plan with 6-12 month horizons.
