# Social Account Architecture

**Status:** Draft
**Last updated:** 2026-04-17
**Source IDs:** U01-U05, L01-L09, E01-E20, E23

## Operating principle

Every account must have:

1. a job,
2. a named owner,
3. a content cadence,
4. a support/reply rule,
5. a metric,
6. an exit/inactivity rule.

If not, do not create it.

## Identity x platform matrix

| Platform | Founder | Company | Product/app | Create now? | Primary job |
|---|---:|---:|---:|---|---|
| LinkedIn | Yes | Yes | Later via Product/Showcase if warranted | Yes | B2B trust, category narrative, proof, partnerships |
| GitHub | Personal account | Organization | Repos/projects | Yes | technical credibility, open-source/proof, collaboration |
| YouTube | Optional personal appearances | Brand channel | Playlists per product | Yes | demos, explainers, tutorials, launch videos |
| Product Hunt | Personal maker account | Product pages claimed by domain email | Product pages | Yes for founder; product pages when launching | launch credibility and maker discovery |
| Website | Founder bio page | Official hub | product/service pages | Yes | canonical source of truth |
| Reddit Pro | Business username + founder may listen personally | Business profile | Not initially | Yes for research/listening | market research, language mining, support if appropriate |
| Instagram | Optional founder clips | Professional company account | not initially | Conditional | short-form demos, visuals, social proof |
| TikTok | Optional personal creator account | Business account only if cadence exists | not initially | Defer unless video engine exists | native short-form discovery |
| Pinterest | No | Business account only if visual/search library exists | not initially | Defer | visual/search discovery, long-tail pins |
| X/Bluesky/Threads | Optional founder | Company if active | product only if active | Defer | real-time commentary, build-in-public |
| Discord/Slack | No | Community only after demand | product community | Defer | power-user community/support |

## Tier 1 — create now

### 1. Founder LinkedIn

**Job:** trust, category design, relationship-building, launch narration.

Use for:

- founder thesis,
- build-in-public,
- lessons from product/service work,
- customer language observations,
- partnership outreach,
- Product Hunt launch support.

Cadence:

- 3 posts/week for first 90 days.
- 10 meaningful comments/week on relevant people/communities.
- 1 founder story or build-note per week.

Profile requirements:

- headline: specific audience + outcome,
- banner: current company/product thesis,
- featured links: company site, flagship demo, newsletter/waitlist,
- about section: founder credibility + current build lanes + how to contact,
- no inflated team language.

### 2. Company LinkedIn Page

**Job:** official trust shell.

Use for:

- official company description,
- product roundups,
- announcements,
- proof/case studies,
- hiring/contractor/collaboration posts,
- media kit/contact routing.

Cadence:

- 1-2 posts/week.
- Repost strongest founder/product posts with official context.
- Monthly proof roundup.

Platform constraints:

- LinkedIn Company Pages require a personal account to create and manage.
- LinkedIn Page verification is not automatic; eligibility/review can depend on accurate Page data, website URL, active admin presence, claimed Page status, policy compliance, and sometimes paid LinkedIn products.
- Page admin roles should use least privilege: super admin only for ownership/admin operations, content admin for publishing, analyst for measurement.
- Admin candidates generally must be connected to the super admin and follow the Page.
- Showcase Pages can go inactive if unused for six months; do not create them without a maintenance owner.

### 3. GitHub organization

**Job:** technical credibility and collaboration shell.

Use for:

- public demo repos when appropriate,
- product docs/open-source utilities,
- roadmap/discussions only for developer-facing products,
- security policy and responsible disclosure,
- visible engineering standards.

Setup rules:

- Use company org, not founder personal repos, for serious products.
- If you want a GitHub verified badge, align org profile website/email with a verified domain.
- Keep at least two organization owners where possible.
- Restrict repository creation if collaborators are added.
- Require MFA/2FA for members.
- Use teams and repo roles, not ad hoc admin rights.
- Add `SECURITY.md`, `CODE_OF_CONDUCT.md`, and issue templates only when public community collaboration begins.

### 4. YouTube Brand Channel

**Job:** visual proof, demos, tutorials, launch assets.

Use for:

- product explainers,
- architecture/design breakdowns,
- founder walkthroughs,
- short demos for Product Hunt galleries,
- captioned tutorials and accessibility-oriented videos.

Setup rules:

- Use a Brand Account/channel so the public channel can have company/product naming separate from the founder's Google Account.
- Treat Owner as a high-trust role because owners can take destructive channel actions; use manager/editor permissions where possible.
- Add a backup owner; YouTube recommends at least one other owner for Brand Accounts.
- Do not share Google passwords.
- Keep raw recordings and edited exports in an organized asset library.

Cadence:

- Month 1: 1 company explainer + 2 short demos.
- Months 2-3: 1 long-form demo/tutorial per month + 2-4 Shorts cutdowns if bandwidth allows.

### 5. Product Hunt founder account + future Product Pages

**Job:** launch credibility and maker/community discovery.

Rules:

- Product Hunt posting requires a personal account; company accounts cannot hunt/post products.
- New personal accounts generally need onboarding and about a one-week wait before posting, so create the founder/maker account before launch week.
- Build the founder profile before launch: bio, links, avatar, maker credibility, prior activity.
- Claim Product Pages with company-domain email when possible.
- Product pages belong to serious products, not every idea.

Prepare for each launch:

- tagline,
- 260-character description,
- maker comment,
- gallery images,
- YouTube demo URL,
- pricing tag,
- topics,
- first-comment strategy,
- responder schedule.

### 6. Website and email routing

**Job:** canonical trust + conversion source.

Minimum pages before serious posting:

- home / company one-liner,
- about/founder,
- product/service pages,
- contact,
- support,
- privacy statement,
- terms where needed,
- media kit / press / partnerships page,
- status/changelog page when product is live.

Emails:

- `hello@...` general,
- `support@...` support,
- `privacy@...` privacy/data requests,
- `press@...` optional later,
- `partners@...` optional later.

## Tier 2 — create only if relevant in first 60-90 days

### Reddit Pro / business Reddit profile

**Job:** market research first, engagement second, support third.

Use for:

- keyword tracking,
- finding communities and objections,
- mining customer language,
- answering questions authentically,
- monitoring competitor/category pain.

Rules:

- Reddit itself suggests using a new username for the business if the founder is already a redditor.
- Do not scrape/export/publish redditor content from Reddit Pro without permission/consent.
- Do not post product links before becoming a credible community participant.
- Treat Reddit as listening infrastructure, not an ad channel.

Cadence:

- 15 minutes/day listening.
- 3-5 useful comments/week.
- No product posts until at least 10 value-first interactions in the relevant community.

### Instagram professional account

**Job:** visual trust, short demos, founder/product clips, DM surface.

Create only if:

- there are demos/screenshots/clips to post weekly,
- someone owns visual templates,
- DMs can be monitored,
- Meta Business access is configured without sharing passwords.

Use for:

- product demos,
- behind-the-scenes build clips,
- visual proof cards,
- founder face/trust moments,
- accessibility-friendly explainers.

### TikTok Business Account

**Job:** native short-form discovery.

Defer unless:

- the company can create 2-4 native short videos/week,
- commercial disclosure rules can be followed,
- business/creator account strategy is clear,
- account will not sit inactive for 180+ days.

Rules:

- Business Accounts are public profiles for brands/businesses.
- Business Accounts use the Commercial Music Library; general music library tracks may not be cleared for commercial use.
- Promotional/commercial content must use TikTok's content disclosure setting.
- Realistic AI-generated/significantly edited content needs AI labeling.
- Inactive accounts may lose username after 180 days.

### Pinterest business account

**Job:** visual/search discovery and long-tail content.

Create only if:

- there is a repeatable visual library,
- the target user searches visually,
- the website has claimable pages and assets,
- someone can pin consistently.

Use for:

- educational infographics,
- workflow checklists,
- product templates,
- app screenshots,
- accessible tutorial visuals.

## Tier 3 — optional / selective

Create only when audience evidence says yes:

- X / Bluesky for real-time founder commentary.
- Threads for softer consumer/product presence.
- Facebook Page if needed for Meta Business assets, paid social, groups, or older demographics.
- Discord/Slack only after repeated community/support demand.
- Telegram/WhatsApp groups only after there is a support/community operator.

## Dedicated product account decision tree

Create a product account if:

```text
Distinct ICP?                         yes/no
Weekly/biweekly content?              yes/no
Support/community replies needed?     yes/no
Launch beyond founder network?        yes/no
Ads/creators planned?                 yes/no
Future spin-out/sale plausible?       yes/no
```

Decision:

- 0-2 yes: no product account; use company/founder.
- 3-4 yes: create product page/playlist/repo; defer separate social unless owner/cadence exists.
- 5-6 yes: create product identity and social accounts with explicit maintenance plan.

## Recommended initial account map

| Identity | LinkedIn | GitHub | YouTube | Product Hunt | Reddit | Instagram | TikTok | Pinterest |
|---|---|---|---|---|---|---|---|---|
| Founder | optimize now | personal account remains | appears in company videos | maker account now | personal listening only | optional | optional | no |
| Company | Page now | org now | Brand Channel now | claimed product/company pages when launching | Pro business profile now | conditional now | defer | defer |
| TapTap | no separate social yet | repo under org when public | playlist/demo series | Product Page at launch | no | no | no | no |
| SpatialSense | no separate social yet | repo later | playlist/demo series later | Product Page at launch | no | no | no | no |
| ZZP/freelance product | no separate social yet | repo private/public as needed | demo playlist | Product Page when live | research keywords now | conditional | defer | maybe if templates/checklists |

## Inactivity rule

If any public account cannot maintain at least one meaningful update every 30 days, either:

1. convert it to a static profile with clear “updates at [main channel]” redirect, or
2. archive/de-emphasize it.

Inactive profiles harm trust more than missing profiles.
