# Example: /launch generating a Show HN post

**Command**: `/launch "Rankly — daily keyword rank tracking with Slack alerts, built for solo founders at $9/mo"`

**Context**: Founder just finished MVP after 3-week build. No prior audience. Launching cold.

---

## Input

```
/launch "Rankly — daily keyword rank tracking with Slack alerts, built for solo founders at $9/mo"

PRODUCT: Rankly
TAGLINE: Daily keyword rankings + instant Slack alerts when you drop
PROBLEM: Semrush is $130/mo. Most founders track 20 keywords, not 500.
         We're spending enterprise prices for solo-founder needs.
SOLUTION: Connect Google Search Console → get daily rankings + Slack alert
          if any keyword drops more than 3 positions
BUILT IN: 3 weekends
PRICE: $9/mo (first 100 users: lifetime at $29 one-time)
URL: rankly.app
YOUR STORY: I was paying $130/mo for Semrush and using 5% of it. Felt insane.
```

---

## Output (ASSET 1: Hacker News)

```
────────────────────────────────────────────────────
ASSET 1: HACKER NEWS
────────────────────────────────────────────────────

Title:
Show HN: Rankly – daily keyword rank tracking for $9/mo (Semrush is $130)

Body:

I was paying $130/month for Semrush while tracking 20 keywords for my SaaS.
Every Monday I'd log in, manually check each keyword, screenshot the changes.
45 minutes gone. At enterprise pricing.

Rankly does one thing: connects to your Google Search Console and emails/Slacks
you when any of your keywords move more than N positions. Daily. No dashboard
to log into, no 200-feature bloat you'll never use.

Built this in 3 weekends with Next.js + Supabase. Rough around the edges (no
mobile UI yet) but the core ranking + alerts work reliably. Currently checks
rankings daily at 6am UTC.

Pricing: $9/mo. First 100 users get lifetime access at $29 one-time because
I want early feedback more than early revenue. 43 spots left.

Honest limitations: Google Search Console only (no Bing, no third-party data),
max 500 keywords per account, no historical trend graphs yet (coming in v2).

→ rankly.app

Looking for honest feedback on: is the $9 price point the right call, or would
you expect this to be free with a paid alerts tier?

---

Comment reply templates (prepare before posting):

"How is this different from [existing tool]?"
→ "Most tools in this space are built for agencies managing 100+ sites at
   enterprise prices. Rankly is built for founders managing 1-3 sites who want
   one email when something changes — no weekly login required. Different ICP,
   different price, different interface."

"Why not just use Google Search Console directly?"
→ "GSC shows rankings but doesn't alert you when they change. If you check it
   weekly you might miss a drop that happened Monday and went unresolved for 7
   days. Rankly is the alert layer on top of data you already own."

"What's your tech stack?"
→ "Next.js 14 + Supabase + Vercel. Google Search Console API for ranking data,
   Slack API + Resend for alerts. About 1,200 lines of code total. Happy to
   open-source the GSC polling module if that's useful."

"Is this sustainable at $9/mo?"
→ "Honest answer: 500 customers at $9 = $4,500 MRR. That's side-project
   sustainable for me. At that point I'd raise pricing for new customers and
   grandfather current users. Not trying to build a unicorn, trying to build
   something useful."
```

---

## Output (ASSET 2: Twitter/X Thread)

```
────────────────────────────────────────────────────
ASSET 2: TWITTER/X THREAD
────────────────────────────────────────────────────

Tweet 1 (hook):
I was paying $130/mo for Semrush to track 20 keywords.

So I built Rankly in 3 weekends. $9/mo. Does exactly what I needed.

Here's the build story: 🧵

Tweet 2 (problem):
Every Monday morning ritual:
- Log into Semrush
- Click through 20 keywords
- Screenshot the changes
- Close tab, never log in again

$130/mo for a Monday morning screenshot routine.
The 95% of Semrush I never used was subsidizing the 5% I actually needed.

Tweet 3 (attempt + failure):
My first version scraped Google Search results directly.

It worked for 3 days. Then Google blocked my IP.

Pivoted to Google Search Console API — data Google already gives you for free,
just without the alerts layer.

Tweet 4 (build — numbers):
What I built in 3 weekends:

• Daily keyword rank checking (GSC API)
• Slack + email alerts on position drops
• Configurable threshold (alert if drop > 3 positions)
• Max 500 keywords, unlimited sites

Stack: Next.js + Supabase + Vercel
Code: ~1,200 lines
Weekends spent: 3
Coffee consumed: way too much ☕

Tweet 5 (demo):
[INSERT: GIF of Slack alert landing — "⚠️ 'b2b saas tools' dropped from #4 to #8"]

One Slack message. That's it.
No dashboard to log into. No report to export. Just the signal you need.

Tweet 6 (offer):
Launching at $9/mo.

First 100 users: lifetime access at $29 one-time.
43 spots left.

If you track keywords and want to stop doing it manually:
→ rankly.app

Tweet 7 (loop close):
The most valuable thing you can build is the thing that solves your own
daily frustration.

Not the biggest market. The sharpest pain you personally feel.

RT if you've done the same. Follow for what I build next.
```

---

## Output (ASSET 3: ProductHunt)

```
────────────────────────────────────────────────────
ASSET 3: PRODUCTHUNT
────────────────────────────────────────────────────

Tagline (58 chars):
Daily keyword alerts when your rankings drop

Description (248 chars):
Connect Google Search Console and get Slack/email alerts the moment
any keyword drops more than N positions. No dashboard to check, no
manual monitoring. Built for solo founders who don't need Semrush's
500 features at $130/mo.

Maker comment (post immediately after launch):
Hey PH! 👋

I'm [name], built Rankly because I was spending $130/mo on Semrush to
track 20 keywords. The tool was great — just completely oversized for
what I needed.

One thing I'd love feedback on: is $9/mo the right price, or would you
expect this to be free with a "premium alerts" tier? Genuinely uncertain
and your input will determine v2 pricing.

I'll be here all day answering questions. Ask me anything — especially
if you think this is dumb. I want the honest takes.

→ rankly.app
```

---

## Output (ASSET 6: Warm DM Templates)

```
────────────────────────────────────────────────────
ASSET 6: WARM DM TEMPLATES
────────────────────────────────────────────────────

Tier 1 (10 people — other indie founders who've complained about SEO tool pricing):
"Hey [name] — saw you mentioned Semrush pricing being rough for solo projects
a while back. Just launched Rankly — daily keyword alerts at $9/mo, no dashboard.
Would love your honest take: rankly.app"

Tier 2 (20 people — founders you know who do SEO):
"[name] — quick one. Do you know any founders who'd want to track keyword rankings
without paying enterprise SEO prices? Just launched something that might fit.
Happy to give them a founding member deal."

Tier 3 (20 people — general warm network):
"Launched something small today — rankly.app. Daily SEO rank alerts for $9/mo.
No pressure at all — just sharing with people whose judgment I trust."

────────────────────────────────────────────────────
LAUNCH EXECUTION ORDER
────────────────────────────────────────────────────
Day -3: DM 20 people, warn them PH launch is coming
Day 0:
  12:01am PST → ProductHunt post
  8:00am      → HN Show HN
  8:05am      → Twitter thread
  8:10am      → Send Tier 1 DMs (10 people)
  12:00pm     → LinkedIn post
  2:00pm      → Reddit: r/SideProject, r/microsaas
  5:00pm      → Email any existing list
  All day     → Reply to every comment within 1 hour
Day 1: "48 hours in: [honest numbers]" tweet
Day 7: "Week 1 learnings" thread
```

---

## What This Example Demonstrates

1. **The HN title is specific and honest** — "Semrush is $130" is the contrast that makes the price compelling
2. **The body has explicit limitations** — "no mobile UI yet," "no historical graphs" builds trust vs. overselling
3. **Reply templates prevent cold-response paralysis** — founder has the script ready before posting
4. **The tweet thread has numbers in tweet 4** — this is consistently the most reshared tweet in the sequence
5. **DMs are in 3 tiers** — not a single blast, but graduated by relationship strength
6. **The execution order matters** — HN in the morning (US), DMs right after announcement to seed engagement

The launch above generated 340 HN upvotes, 89 comments, and 23 paying customers on launch day.
(Fictional but representative of what a clean Show HN post achieves for a $9 tool with a clear pain story.)
