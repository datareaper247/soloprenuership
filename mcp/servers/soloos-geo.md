# soloos-geo MCP Server

**Purpose**: Geographic expansion intelligence — market entry analysis, localization, SEO, cultural fit scoring, and regulatory compliance for international growth.

## TypeScript Server Definition

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'soloos-geo',
  version: '1.0.0',
  description: 'International expansion toolkit — market entry, localization, geo SEO, regulatory compliance'
});

// ─── MARKET ENTRY ─────────────────────────────

server.tool('market_entry_analyze', 'Full market entry analysis for a target country', {
  target_country: z.string().describe('Country name or ISO code, e.g. "Germany" or "DE"'),
  product: z.string(),
  product_category: z.string().describe('e.g. "B2B project management SaaS", "HR software"'),
  existing_markets: z.array(z.string()).default(['US']).describe('Countries already operating in'),
  budget_range: z.enum(['bootstrap', 'under-100k', '100k-500k', '500k+']).optional()
}, async ({ target_country, product, product_category, existing_markets, budget_range }) => {
  // Market sizing: TAM/SAM/SOM for target country using GDP, internet penetration, industry data
  // Competitive landscape: top 5 local + global competitors, market share estimates
  // Regulatory overview: data privacy laws, business entity requirements, tax implications
  // Cultural fit: business culture norms, buying behavior, preferred communication channels
  // Go-to-market path: direct vs partner vs reseller, typical sales cycle length
  // Infrastructure: local payment methods, currency, billing preferences
  // Risk matrix: market entry risks (regulatory, competitive, execution) + mitigations
  // Return: structured market entry report — scoring matrix + recommended go/no-go + entry sequencing
});

server.tool('local_competitor_map', 'Map local and regional competitors in a target country', {
  target_country: z.string(),
  product_category: z.string(),
  include_global_players: z.boolean().default(true)
}, async ({ target_country, product_category, include_global_players }) => {
  // Identify local-first competitors (often unlisted on global review sites)
  // Map each competitor: product focus, pricing model, market position, strengths/weaknesses
  // Identify gaps: underserved segments or features local players miss
  // Channel analysis: where local competitors acquire customers (local SEO, trade shows, associations)
  // Return: competitor matrix + gap map + positioning recommendations for this market
});

// ─── LOCALIZATION ─────────────────────────────

server.tool('localization_audit', 'Audit product and content for localization readiness', {
  content_samples: z.array(z.string()).describe('UI copy, marketing content, or documentation samples'),
  target_locales: z.array(z.string()).describe('BCP 47 locale codes, e.g. ["de-DE", "fr-FR", "ja-JP"]'),
  product_type: z.enum(['web_app', 'mobile_app', 'marketing_site', 'documentation', 'email']),
  current_i18n_setup: z.string().optional().describe('Current internationalization framework or approach')
}, async (params) => {
  // Technical audit: hardcoded strings, date/number/currency formats, RTL support needed?
  // Content audit: idioms, cultural references, humor that won't translate
  // Missing locale requirements: character set support, text expansion (German +30%, CJK compression)
  // Priority locale ranking by market opportunity vs localization effort
  // Tooling recommendations: i18next, Crowdin, Lokalise, Phrase
  // Return: readiness score per locale + blocker list + prioritized localization roadmap
});

server.tool('translate_localize', 'Translate AND culturally localize content for a target market', {
  content: z.string(),
  source_locale: z.string().default('en-US'),
  target_locale: z.string().describe('BCP 47 code, e.g. "de-DE", "pt-BR", "ja-JP"'),
  content_type: z.enum(['ui_copy', 'marketing', 'legal', 'technical_docs', 'email', 'social']),
  brand_voice: z.string().optional().describe('Brand voice guidelines'),
  domain_glossary: z.record(z.string(), z.string()).optional().describe('Product-specific terms and their approved translations')
}, async (params) => {
  // Phase 1: Machine translation using DeepL API (best quality for EU languages)
  // Phase 2: Cultural adaptation — idiom replacement, example localization, formality adjustment
  // Phase 3: Glossary enforcement — ensure product terms use approved translations consistently
  // Phase 4: SEO alignment — adapt for local search terms, not just literal translation
  // Flags: phrases that are legally sensitive in target locale
  // Return: localized content + adaptation notes + glossary suggestions
});

// ─── GEO SEO ──────────────────────────────────

server.tool('hreflang_generate', 'Generate hreflang tags for multi-language SEO', {
  pages: z.array(z.object({
    path: z.string().describe('URL path, e.g. "/pricing"'),
    locales: z.array(z.object({
      locale: z.string().describe('BCP 47 code'),
      url: z.string().describe('Full canonical URL for this locale')
    }))
  })),
  domain_strategy: z.enum(['ccTLD', 'subdomain', 'subdirectory']).describe('e.g. de.example.com vs example.com/de/')
}, async (params) => {
  // Generate correctly formatted hreflang link elements for each page/locale combination
  // Include x-default tag pointing to primary language version
  // Validate: bidirectional reference requirement (every locale must reference all others)
  // Sitemap XML: generate hreflang sitemap entries for all pages
  // Common mistakes to avoid: wrong locale codes, missing x-default, broken bidirectional refs
  // Return: HTML hreflang tags per page + XML sitemap snippet + implementation checklist
});

server.tool('local_keyword_research', 'Keyword research for a specific locale and language', {
  topic: z.string(),
  locale: z.string().describe('BCP 47 locale code, e.g. "de-DE"'),
  competitor_domains: z.array(z.string()).optional(),
  keyword_types: z.array(z.enum(['informational', 'commercial', 'transactional', 'navigational'])).default(['commercial', 'transactional'])
}, async ({ topic, locale, competitor_domains, keyword_types }) => {
  // Research using locale-appropriate tools (Google SERP data via scraping/API)
  // Identify: native-language keywords (not just translated English terms)
  // Include: local slang, industry-specific terminology in target language
  // Search volume and difficulty estimates for target locale
  // SERP feature opportunities: local packs, featured snippets in that language
  // Competitor keyword gap: terms competitors rank for in this locale
  // Return: keyword list with volume/difficulty + priority matrix + content brief starters
});

// ─── CULTURAL & REGULATORY ────────────────────

server.tool('cultural_fit_score', 'Score product and messaging cultural fit for a target market', {
  product: z.string(),
  current_messaging: z.string().describe('Current tagline, positioning, key messages'),
  target_country: z.string(),
  icp_in_target_market: z.string().optional().describe('Ideal customer in target country')
}, async (params) => {
  // Hofstede cultural dimensions analysis: power distance, individualism, uncertainty avoidance
  // Messaging fit: direct vs indirect communication style, hierarchy sensitivity, trust signals
  // Product fit: feature emphasis that resonates locally (e.g. compliance features in Germany, group features in Japan)
  // Social proof types: local logos, certifications, and endorsement formats that carry weight
  // Taboos and sensitivities: colors, symbols, copy angles to avoid
  // Pricing perception: what price anchors, price formats, and discounting norms apply
  // Return: cultural fit score (0-100) + dimensions breakdown + messaging adaptation guide
});

server.tool('regulatory_check', 'Check regulatory requirements for market entry', {
  target_country: z.string(),
  product_type: z.string(),
  data_handling: z.object({
    collects_personal_data: z.boolean(),
    data_types: z.array(z.string()).optional().describe('e.g. ["email", "health records", "payment"]'),
    stores_data_in: z.array(z.string()).optional().describe('Cloud regions data is stored')
  }),
  revenue_model: z.enum(['subscription', 'usage_based', 'one_time', 'marketplace']),
  estimated_revenue_in_market: z.number().optional().describe('Annual revenue in USD — affects VAT/tax thresholds')
}, async (params) => {
  // Data privacy: GDPR (EU), LGPD (Brazil), PIPL (China), PDPA (Thailand), etc.
  // Data residency: mandatory local storage requirements
  // Business registration: entity requirements, local representative rules
  // Tax/VAT: digital services tax obligations, registration thresholds, invoice requirements
  // Sector-specific: financial services licensing, healthcare certifications, etc.
  // Payment regulations: supported payment methods, local acquiring requirements
  // Priority: sort requirements by blocking (cannot operate without) vs recommended
  // Return: regulatory checklist + blocking requirements + estimated compliance cost + timeline
});
```

## Open Source Tools Powering This Server

| Tool | Purpose | GitHub | License |
|------|---------|--------|---------|
| [DeepL API](https://www.deepl.com/docs-api) | High-quality translation (500K chars/month free) | — | Commercial free tier |
| [Jina Reader](https://github.com/jina-ai/reader) | Scrape local SERPs and competitor sites | 10k+ stars | Apache 2.0 |
| [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate) | Self-hosted translation alternative | 7k+ stars | AGPL 3.0 |
| [Argos Translate](https://github.com/argosopentech/argos-translate) | Offline neural machine translation | 3k+ stars | MIT |
| [i18next](https://github.com/i18next/i18next) | Industry-standard i18n framework | 7k+ stars | MIT |
| [Country.io data](https://github.com/annexare/Countries) | Country metadata, currencies, languages | 2k+ stars | MIT |

## Environment Variables

```env
# Translation
DEEPL_API_KEY=...               # DeepL API (free: 500K chars/month)
GOOGLE_TRANSLATE_API_KEY=...    # Fallback for DeepL unsupported languages

# SEO Data
AHREFS_API_KEY=...              # Keyword data per locale (paid)
SEMRUSH_API_KEY=...             # Alternative — geo-specific keyword research

# Web Scraping
JINA_API_KEY=...                # Jina Reader for competitor scraping (free tier)

# AI
ANTHROPIC_API_KEY=...           # Cultural analysis and content localization

# Optional
DEEPL_GLOSSARY_ID=...           # Pre-configured domain glossary in DeepL
LOKALISE_API_KEY=...            # TMS integration for sending translated content
CROWDIN_API_KEY=...             # Alternative TMS
```

## Example Usage

```typescript
// Full market entry analysis for Germany
await client.callTool('market_entry_analyze', {
  target_country: 'Germany',
  product: 'B2B project management software for engineering teams',
  product_category: 'Project Management SaaS',
  existing_markets: ['US', 'Canada'],
  budget_range: 'under-100k'
});

// Check if homepage copy is culturally appropriate for Japan
await client.callTool('cultural_fit_score', {
  product: 'AI writing assistant for marketing teams',
  current_messaging: 'Move fast. Ship more. Beat your competition with AI.',
  target_country: 'Japan',
  icp_in_target_market: 'Marketing managers at mid-size Japanese tech companies'
});

// Translate and localize a landing page for German market
await client.callTool('translate_localize', {
  content: 'Stop wasting time on manual reports. Our AI writes them in seconds.',
  source_locale: 'en-US',
  target_locale: 'de-DE',
  content_type: 'marketing',
  brand_voice: 'Professional but approachable. Direct. Never hype-y.',
  domain_glossary: { 'AI': 'KI', 'dashboard': 'Dashboard' }
});

// Generate hreflang for a 3-language site
await client.callTool('hreflang_generate', {
  pages: [{
    path: '/pricing',
    locales: [
      { locale: 'en-US', url: 'https://acme.com/pricing' },
      { locale: 'de-DE', url: 'https://acme.com/de/preise' },
      { locale: 'fr-FR', url: 'https://acme.com/fr/tarifs' }
    ]
  }],
  domain_strategy: 'subdirectory'
});

// Check GDPR and German-specific regulatory requirements
await client.callTool('regulatory_check', {
  target_country: 'Germany',
  product_type: 'B2B SaaS processing employee data',
  data_handling: {
    collects_personal_data: true,
    data_types: ['email', 'name', 'work activity logs'],
    stores_data_in: ['us-east-1']
  },
  revenue_model: 'subscription',
  estimated_revenue_in_market: 50000
});
```

## Integration Notes

- **soloos-memory**: Market entry research saved via `business_context_save` with category "geo-expansion"; competitor data stored via `competitor_update` per country
- **soloos-marketing**: `translate_localize` outputs feed directly into `geo_content_adapt` in soloos-marketing; `local_keyword_research` informs `seo_research` per locale
- **soloos-ops**: `regulatory_check` results feed `compliance_check` and `policy_generate` with jurisdiction-specific requirements
- **soloos-growth**: `market_entry_analyze` TAM data feeds `growth_model` for international revenue projections; `cultural_fit_score` informs `channel_score` for local acquisition channels
- **soloos-product**: `localization_audit` results feed `prd_create` for i18n feature requirements; market gaps from `local_competitor_map` feed `feature_prioritize`
