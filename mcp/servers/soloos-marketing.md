# soloos-marketing MCP Server

**Purpose**: Full-stack marketing capabilities — SEO, content, email, social, ads, PR, community.

## TypeScript Server Definition

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'soloos-marketing',
  version: '1.0.0',
  description: 'Professional marketing capabilities for any AI agent'
});

// ─── SEO TOOLS ────────────────────────────────

server.tool('seo_research', 'Keyword research and SEO opportunity analysis', {
  keyword: z.string(),
  domain: z.string().optional().describe('Your domain for gap analysis'),
  competitors: z.array(z.string()).optional()
}, async ({ keyword, domain, competitors }) => {
  // Analyze keyword: volume, difficulty, CPC, SERP features
  // Find semantic variations and LSI keywords
  // Identify content gaps vs competitors
  // Return actionable SEO brief
});

server.tool('content_brief', 'Create a comprehensive SEO content brief', {
  keyword: z.string(),
  icp: z.string().describe('Ideal customer profile description'),
  tone: z.enum(['professional', 'casual', 'technical', 'conversational']).default('professional'),
  word_count: z.number().default(2000)
}, async ({ keyword, icp, tone, word_count }) => {
  // Research SERP top 10 for this keyword
  // Extract: title patterns, H2 structure, content coverage
  // Identify questions to answer (People Also Ask)
  // Return: full content brief with outline, word count targets per section, meta
});

server.tool('seo_content_write', 'Write a complete SEO-optimized article', {
  brief: z.string().describe('Content brief from content_brief tool or custom brief'),
  brand_voice: z.string().optional()
}, async ({ brief, brand_voice }) => {
  // Write complete article following brief
  // Optimize: title, meta, H1/H2/H3, keyword placement, internal linking suggestions
  // Add FAQ section for featured snippet capture
  // Return: complete article in markdown
});

server.tool('meta_optimizer', 'Optimize title tags and meta descriptions', {
  page_title: z.string(),
  page_content: z.string(),
  target_keyword: z.string()
}, async (params) => {
  // Generate 3 variants each for: title tag, meta description
  // Score each on: CTR potential, keyword inclusion, length
  // Return ranked options
});

// ─── CONTENT TOOLS ────────────────────────────

server.tool('blog_post_write', 'Write a high-quality blog post', {
  topic: z.string(),
  audience: z.string(),
  goal: z.enum(['awareness', 'consideration', 'conversion', 'retention']),
  word_count: z.number().default(1500),
  include_cta: z.boolean().default(true)
}, async (params) => { /* ... */ });

server.tool('content_repurpose', 'Repurpose one content piece into multiple formats', {
  source_content: z.string(),
  formats: z.array(z.enum([
    'twitter_thread', 'linkedin_post', 'email_newsletter',
    'youtube_script', 'tiktok_script', 'podcast_outline',
    'infographic_brief', 'press_release', 'case_study'
  ]))
}, async (params) => {
  // Transform source into each requested format
  // Optimize each for platform norms and algorithms
});

server.tool('content_calendar', 'Create a 30-90 day content calendar', {
  product: z.string(),
  audience: z.string(),
  channels: z.array(z.string()),
  days: z.number().default(30),
  cadence: z.object({
    blog_posts_per_week: z.number().default(2),
    social_posts_per_week: z.number().default(5),
    email_per_week: z.number().default(1)
  }).optional()
}, async (params) => { /* ... */ });

// ─── EMAIL TOOLS ──────────────────────────────

server.tool('email_sequence', 'Create a complete email marketing sequence', {
  sequence_type: z.enum([
    'onboarding', 'nurture', 'win_back', 'upsell', 'cold_outreach',
    'trial_to_paid', 'product_launch', 're_engagement'
  ]),
  product: z.string(),
  audience: z.string(),
  email_count: z.number().default(5),
  days_apart: z.array(z.number()).optional()
}, async (params) => {
  // Generate complete email sequence
  // Each email: subject line (A/B options), preheader, body, CTA
  // Include: send timing, segment criteria
});

server.tool('email_subject_lines', 'Generate and score email subject line variants', {
  email_context: z.string(),
  count: z.number().default(10),
  style: z.enum(['curiosity', 'benefit', 'urgency', 'personal', 'question']).optional()
}, async (params) => { /* ... */ });

// ─── SOCIAL TOOLS ─────────────────────────────

server.tool('social_post', 'Create platform-optimized social media posts', {
  content: z.string().describe('Core message or URL to promote'),
  platforms: z.array(z.enum(['twitter', 'linkedin', 'instagram', 'facebook', 'threads', 'bluesky'])),
  goal: z.enum(['awareness', 'engagement', 'traffic', 'conversion'])
}, async (params) => {
  // Create platform-optimized version for each
  // Twitter: hook + thread if needed
  // LinkedIn: professional narrative format
  // Instagram: visual description + caption
});

server.tool('twitter_thread', 'Write a viral Twitter/X thread', {
  topic: z.string(),
  angle: z.string().describe('Unique perspective or insight'),
  tweet_count: z.number().default(8)
}, async (params) => { /* ... */ });

server.tool('linkedin_post', 'Write a high-performing LinkedIn post', {
  topic: z.string(),
  personal_story: z.boolean().default(true),
  cta: z.string().optional()
}, async (params) => { /* ... */ });

// ─── ADVERTISING TOOLS ────────────────────────

server.tool('ad_copy', 'Create advertising copy for multiple platforms', {
  product: z.string(),
  value_prop: z.string(),
  audience: z.string(),
  platform: z.enum(['google', 'linkedin', 'facebook', 'twitter', 'reddit']),
  format: z.enum(['search', 'display', 'video_script', 'sponsored_post'])
}, async (params) => {
  // Create: headlines (3), descriptions (3), CTAs (3)
  // Score each on estimated CTR
  // Return A/B test recommendations
});

server.tool('landing_page_copy', 'Write complete landing page copy', {
  product: z.string(),
  target_keyword: z.string().optional(),
  audience: z.string(),
  unique_selling_points: z.array(z.string()),
  social_proof: z.array(z.string()).optional()
}, async (params) => {
  // Complete landing page: hero, benefits, features, social proof, FAQ, CTA
  // Optimized for conversion
  // Include A/B test variants for hero headline
});

// ─── PR TOOLS ─────────────────────────────────

server.tool('press_release', 'Write a professional press release', {
  announcement: z.string(),
  company: z.string(),
  spokesperson_quote: z.string().optional(),
  boilerplate: z.string().optional()
}, async (params) => { /* ... */ });

server.tool('media_pitch', 'Create a personalized media pitch email', {
  story: z.string(),
  journalist: z.string().optional(),
  publication: z.string().optional(),
  angle: z.string()
}, async (params) => { /* ... */ });

// ─── GEO/LOCALIZATION TOOLS ───────────────────

server.tool('geo_content_adapt', 'Adapt content for a specific market/locale', {
  content: z.string(),
  source_locale: z.string().default('en-US'),
  target_locale: z.string(),
  cultural_notes: z.boolean().default(true)
}, async (params) => {
  // Translate + localize
  // Flag cultural sensitivities
  // Adapt idioms, examples, references
  // SEO keyword mapping for target locale
});

server.tool('geo_seo', 'SEO strategy for geographic market expansion', {
  product: z.string(),
  target_countries: z.array(z.string()),
  current_domain: z.string().optional()
}, async (params) => {
  // Keyword research per locale
  // hreflang recommendations
  // Country-specific competitor analysis
  // Local search engine recommendations (Baidu, Yandex, Naver)
  // Local directory/citation opportunities
});
```

## Open Source Tools Powering This Server

| Tool | Purpose | License |
|------|---------|---------|
| [Jina Reader](https://github.com/jina-ai/reader) | Web scraping for SEO SERP analysis | Apache 2.0 |
| [SerpAPI alternatives](https://github.com/nicholasmartino/serpapi-python) | SERP data (free tier) | MIT |
| [SEO analyzer (Python)](https://github.com/sethblack/python-seo-analyzer) | On-page SEO analysis | MIT |
| [GPT-SEO](https://github.com/) | AI-powered SEO content generation | MIT |
| [Phidata](https://github.com/phidatahq/phidata) | Agent with web search for research | MPL 2.0 |

## Environment Variables

```env
AHREFS_API_KEY=...          # For keyword data (paid)
SEMRUSH_API_KEY=...         # Alternative to Ahrefs (paid)
ANTHROPIC_API_KEY=...       # For content generation

# Optional
MAILCHIMP_API_KEY=...       # For email scheduling
BUFFER_ACCESS_TOKEN=...     # For social scheduling
DEEPL_API_KEY=...           # For localization/translation
GOOGLE_SEARCH_CONSOLE=...   # For rank tracking
```
