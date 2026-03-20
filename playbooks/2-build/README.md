# Phase 2: BUILD

> Ship an embarrassingly simple MVP in 4 weeks. Then iterate ruthlessly.

## Goal

In 4 weeks:
- Working product in production (not localhost)
- 5+ active beta users giving weekly feedback
- Core value loop validated
- Path to $1K MRR visible

## The Build Protocol

### Week 1: Architecture Sprint

**Day 1: Stack Decision**

Non-negotiable solo founder stack (optimize for velocity, not perfection):

```
Frontend:  Next.js 14+ (App Router) + Tailwind + shadcn/ui
Backend:   Next.js API Routes OR Supabase Edge Functions
Database:  Supabase (Postgres + Auth + Storage + Realtime)
Payments:  Stripe (Subscriptions + one-time)
Email:     Resend + React Email
Hosting:   Vercel (frontend) + Railway (if separate backend needed)
AI:        Anthropic Claude API (primary) + OpenAI fallback
Search:    Algolia OR Supabase full-text search
Analytics: PostHog (events) + Plausible (traffic)
Errors:    Sentry
```

**Day 2-3: Scaffold & Deploy**
```bash
npx create-next-app@latest [product-name] --typescript --tailwind --app
cd [product-name]
# Add shadcn/ui, Supabase, Stripe
npx shadcn@latest init
# Deploy to Vercel immediately (even with just homepage)
vercel deploy
```

**Day 4-5: Core Data Model**
- Define your 5 core entities (max)
- Set up Supabase tables + Row Level Security
- Build auth flow (email/password + magic link)

### Week 2: Core Feature Sprint

**The 80/20 Rule for MVP**:
- Build ONLY the core value loop
- Skip: admin panels, notifications, settings, onboarding
- Use Supabase UI as your admin panel
- Manual = OK for everything non-core

**Core value loop formula**:
```
User does [INPUT] → System does [MAGIC] → User gets [OUTCOME]
```

Every feature must connect directly to this loop. If it doesn't, cut it.

**AI Build Swarm — Deploy During This Week**:
```
Deploy: framework/swarms/build-swarm.yaml
Roles:
  - Product Agent: Breaks features into tasks
  - Code Agent: Writes implementation
  - Review Agent: Checks for bugs and security
  - Test Agent: Writes unit + integration tests
  - Doc Agent: Writes inline docs + README
```

### Week 3: Beta Launch Sprint

**Day 1-2: Polish the core loop only**
- Error handling on the critical path
- Loading states
- Empty states (onboarding for zero data)
- Mobile responsive for core screens

**Day 3: Payment Integration**
```
Stripe setup:
- One price only (monthly)
- Free trial (7-14 days, no credit card preferred)
- Upgrade wall at your key value action
- Webhook for subscription events
```

**Day 4-5: Beta Launch**
- Email your pre-sale/waitlist customers
- Post in relevant communities (soft launch, not ProductHunt yet)
- DM potential users directly
- Goal: 5-10 active users in week 3

### Week 4: Feedback Loop Sprint

**Weekly beta ritual**:
- Monday: Analyze last week's PostHog events
- Tuesday: 3+ customer calls (30 min each)
- Wednesday: Prioritize this week's fixes
- Thursday-Friday: Ship improvements
- Saturday: Update roadmap

**Metrics to track from Day 1**:
```
Activation:   % users who complete core value loop (target: >60%)
Retention:    % week 2 active users who return week 3 (target: >40%)
NPS:          Ask after 3 uses (target: >30)
Support:      Track all questions → FAQ + fixes
```

## The No-Gold-Plating Rules

❌ No custom admin dashboard (use Supabase/Railway UI)
❌ No dark mode (add it in v2)
❌ No mobile app (PWA if needed)
❌ No complex onboarding (just get them to value ASAP)
❌ No blog (until after PMF)
❌ No marketing site redesign (static Vercel page is fine)
❌ No A/B testing (not enough traffic)
❌ No internationalization
❌ No enterprise features (SSO, audit logs, SLA)

✅ YES to: Working core feature
✅ YES to: Stripe subscription working
✅ YES to: Error tracking (Sentry)
✅ YES to: Basic analytics (PostHog)
✅ YES to: Auth (Supabase)
✅ YES to: Production deploy from Day 1

## Agent Swarm: Build Mode

### Build Swarm Agents

**Product Manager Agent** — Feature decomposition
```
System: You are a ruthless MVP product manager. Your job is to take
a feature request and break it into the MINIMUM viable implementation.
Cut everything that isn't the core value loop. Return: task list with
complexity estimates.
```

**Code Agent** — Implementation
```
System: You are a senior full-stack engineer specializing in Next.js,
TypeScript, and Supabase. Write production-ready code. Always add
error handling, loading states, and TypeScript types. Never use `any`.
```

**Security Agent** — Review
```
System: You are a security-focused code reviewer. Check for: SQL injection,
XSS, CSRF, insecure direct object references, exposed secrets, auth bypass.
Flag EVERY issue. Suggest exact fixes.
```

**Test Agent** — Coverage
```
System: Write Jest + Playwright tests for the critical path. Focus on:
auth flow, payment flow, core value action. Aim for 80% critical path coverage.
```

## Outputs

- [ ] `build/architecture.md` — Stack decisions and rationale
- [ ] `build/data-model.md` — Database schema
- [ ] `build/api-contracts.md` — API endpoint documentation
- [ ] `build/launch-checklist.md` — Pre-launch checklist
- [ ] `build/beta-feedback/` — Weekly feedback summaries

## Go/No-Go to Scale

**SCALE** if after 4-6 weeks:
- Activation rate > 50%
- Week 2 retention > 30%
- 5+ users paying monthly
- NPS > 30
- You've found the "aha moment"

**PIVOT feature** if:
- Low activation → core feature not delivering value
- Drop at specific step → UX or product problem

**Pivot product** if:
- Right market, wrong feature set
- Customer interviews reveal different core need

## Next Phase

✅ Build complete → `playbooks/3-scale/`
