# soloos-research MCP Server

**Purpose**: Real-time market intelligence — replaces a 10-person market research team.

## TypeScript Server Definition

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'soloos-research',
  version: '1.0.0',
  description: 'Market intelligence and competitive research for solo founders'
});

// ─────────────────────────────────────────────
// TOOLS
// ─────────────────────────────────────────────

server.tool(
  'market_scan',
  'Scan a market for size, competitors, and opportunities',
  {
    topic: z.string().describe('Market or problem area to research'),
    depth: z.enum(['quick', 'standard', 'deep']).default('standard'),
    focus: z.enum(['b2b', 'b2c', 'both']).default('both')
  },
  async ({ topic, depth, focus }) => {
    // 1. Search Reddit for pain points
    // 2. Search HN for signals and discussions
    // 3. Find competitors on ProductHunt, G2, AppSumo
    // 4. Estimate market size from available data
    // 5. Score opportunity (0-10)
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          market: topic,
          pain_points: [], // From Reddit/HN
          competitors: [], // Identified competitors
          market_size: {}, // TAM/SAM/SOM estimates
          opportunity_score: 0,
          recommendation: '',
          sources: []
        })
      }]
    };
  }
);

server.tool(
  'competitor_analyze',
  'Deep analysis of a specific competitor',
  {
    competitor: z.string().describe('Company name or URL'),
    aspects: z.array(z.enum([
      'pricing', 'features', 'positioning', 'seo', 'reviews', 'funding', 'team'
    ])).default(['pricing', 'features', 'positioning', 'reviews'])
  },
  async ({ competitor, aspects }) => {
    // 1. Scrape their website (Jina/Firecrawl)
    // 2. Get G2/Capterra reviews
    // 3. Analyze SEO with Ahrefs if available
    // 4. Check LinkedIn for team size
    // 5. Check Crunchbase for funding
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          name: competitor,
          pricing: {},
          features: [],
          positioning: '',
          review_sentiment: {},
          complaints: [], // 1-3 star review patterns
          gaps: [], // What they don't do well
          seo_profile: {},
          funding: {}
        })
      }]
    };
  }
);

server.tool(
  'customer_pain_mine',
  'Mine a subreddit or community for validated pain points',
  {
    source: z.string().describe('Subreddit name (r/pharmacy) or HN/ProductHunt'),
    keywords: z.array(z.string()).describe('Keywords related to your problem space'),
    limit: z.number().default(50).describe('Number of posts to analyze')
  },
  async ({ source, keywords, limit }) => {
    // Mine Reddit/HN for pain point signals
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          source,
          pain_points: [], // { quote, upvotes, url, severity }
          patterns: [], // Recurring themes
          language: [], // Exact phrases customers use
          willingness_to_pay_signals: []
        })
      }]
    };
  }
);

server.tool(
  'opportunity_score',
  'Score a business opportunity on multiple dimensions',
  {
    idea: z.string().describe('Business idea description'),
    target_market: z.string().describe('Target customer segment'),
    context: z.string().optional().describe('Additional context or research already done')
  },
  async ({ idea, target_market, context }) => {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          scores: {
            problem_severity: 0,    // 0-10
            market_size: 0,         // 0-10
            competitive_gap: 0,     // 0-10
            willingness_to_pay: 0,  // 0-10
            solo_buildability: 0,   // 0-10
          },
          total: 0,
          recommendation: '',       // GO / VALIDATE / PASS
          rationale: '',
          next_steps: []
        })
      }]
    };
  }
);

server.tool(
  'trend_detect',
  'Detect trends and market signals for a topic',
  {
    topic: z.string(),
    timeframe: z.enum(['7d', '30d', '90d', '1y']).default('30d'),
    sources: z.array(z.enum(['hn', 'reddit', 'twitter', 'producthunt', 'github'])).default(['hn', 'reddit', 'producthunt'])
  },
  async ({ topic, timeframe, sources }) => {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          topic,
          trend_direction: 'rising|stable|declining',
          velocity: 0,          // Rate of change
          signal_strength: 0,   // 0-10
          key_events: [],       // Notable launches, discussions
          sentiment: '',
          recommendation: ''
        })
      }]
    };
  }
);

// ─────────────────────────────────────────────
// RESOURCES
// ─────────────────────────────────────────────

server.resource(
  'research://templates/opportunity-scorecard',
  'Opportunity scoring template',
  async () => ({
    contents: [{
      uri: 'research://templates/opportunity-scorecard',
      mimeType: 'text/markdown',
      text: '# Opportunity Scorecard Template...'
    }]
  })
);

server.resource(
  'research://templates/competitor-profile',
  'Competitor analysis template',
  async () => ({
    contents: [{
      uri: 'research://templates/competitor-profile',
      mimeType: 'text/markdown',
      text: '# Competitor Profile Template...'
    }]
  })
);

// ─────────────────────────────────────────────
// PROMPTS
// ─────────────────────────────────────────────

server.prompt(
  'market-discovery',
  'Full market discovery for a problem space',
  { topic: z.string(), focus: z.string().optional() },
  ({ topic, focus }) => ({
    messages: [{
      role: 'user',
      content: {
        type: 'text',
        text: `Conduct a full market discovery for: "${topic}"${focus ? ` focusing on ${focus}` : ''}.

Steps:
1. Use market_scan to get overview
2. Use customer_pain_mine on 2-3 relevant subreddits
3. Use competitor_analyze on top 3 competitors found
4. Use opportunity_score to synthesize findings
5. Return: opportunity brief with recommendation`
      }
    }]
  })
);
```

## Environment Variables

```env
# Required
ANTHROPIC_API_KEY=...      # For synthesis

# Optional (enhances results significantly)
REDDIT_CLIENT_ID=...       # For Reddit API access
REDDIT_CLIENT_SECRET=...
PERPLEXITY_API_KEY=...     # For real-time web search
AHREFS_API_KEY=...         # For SEO data
JINA_API_KEY=...           # For web scraping (free tier available)
```

## Integration with Open Source Tools

- **reddit-mcp** (if available) or direct Reddit API
- **Jina Reader** (free, no key needed) for web scraping
- **HN API** (free, no key) via hackernews-mcp
- **Perplexity API** for real-time search ($20/month)
- **Composio** for SimilarWeb, Ahrefs if available

## Usage Examples

```
# Claude Code with this MCP:
"Research the pharmacy audit software market and score the opportunity"
→ Automatically calls: market_scan → customer_pain_mine → competitor_analyze → opportunity_score

"Who are the top 5 competitors in pharmacy audit?"
→ Calls: market_scan(focus=competitors) → competitor_analyze x5

"Find all the pain points solo founders have with existing project management tools"
→ Calls: customer_pain_mine(r/projectmanagement, r/SaaS, r/entrepreneur)
```
