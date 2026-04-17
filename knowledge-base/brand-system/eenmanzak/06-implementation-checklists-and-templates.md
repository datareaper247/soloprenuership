# Implementation Checklists and Templates

**Status:** Draft
**Last updated:** 2026-04-17
**Source IDs:** U04-U06, E01-E25

## Master setup checklist

### Identity

- [ ] Decide provisional spelling: `Eenmanzak` vs `Eenmanszaak`.
- [ ] Confirm domain availability.
- [ ] Confirm handle availability.
- [ ] Confirm KVK/trademark/search risk with adviser where needed.
- [ ] Write company one-liner.
- [ ] Write founder one-liner.
- [ ] Write category statement.
- [ ] Define 3-5 content pillars.
- [ ] Define voice rules.
- [ ] Create profile avatar/logo placeholder.
- [ ] Create banner/cover image placeholder.
- [ ] Create CTA library.

### Trust

- [ ] Website live.
- [ ] Canonical company-site router live.
- [ ] About/founder page.
- [ ] Contact page.
- [ ] Support page/inbox.
- [ ] Privacy statement.
- [ ] Terms where needed.
- [ ] Proof page or proof section.
- [ ] Claims/compliance register seeded and linked from public-copy drafts.
- [ ] Media/press/partnerships page or section.
- [ ] Links/footer routes to official social and proof surfaces.
- [ ] Lead capture form and privacy notice tested.
- [ ] Cookie/banner consent reviewed if tracking exists.
- [ ] Processing register started.
- [ ] Media/press/partnership email.
- [ ] Founder bio.
- [ ] First proof assets.

### Accounts

- [ ] Founder LinkedIn optimized.
- [ ] Company LinkedIn Page created.
- [ ] LinkedIn admin roles documented.
- [ ] GitHub org created.
- [ ] GitHub owners/2FA/settings configured.
- [ ] YouTube Brand Channel created.
- [ ] YouTube backup owner added.
- [ ] Product Hunt founder account created/onboarded.
- [ ] Reddit Pro business username created.
- [ ] Instagram professional account decision made.
- [ ] TikTok/Pinterest deferred or created with owner/cadence.

### Security

- [ ] Password manager vault created.
- [ ] MFA enabled everywhere.
- [ ] Recovery codes stored securely.
- [ ] Backup owner verified.
- [ ] No shared credentials in chat/docs.
- [ ] Third-party app access reviewed.
- [ ] Monthly access review scheduled.

### Ops

- [ ] Content calendar created.
- [ ] Reply playbook created.
- [ ] Escalation matrix created.
- [ ] UTM convention created.
- [ ] Asset naming convention created.
- [ ] Test dashboard created.
- [ ] Test support/private-message flow.

## Platform bio drafts

### Founder LinkedIn headline options

1. `Building AI-enabled tools and operating systems for one-person businesses | Senior software engineer in NL`
2. `Solo founder building accessible apps + one-person business systems | AI-agent operator | Netherlands`
3. `Senior engineer building practical products for solo operators, seniors, and accessibility-first workflows`

### Founder about-section skeleton

```text
I’m Ash / Ashwin SP — a senior software engineer in the Netherlands building a one-person product company in public.

My work sits at the intersection of:
• practical AI-agent operating systems for solo founders
• Dutch one-person business / ZZP workflows
• accessible mobile products such as TapTap and SpatialSense

I share what I’m learning while building: decisions, constraints, product demos, market research, mistakes, and proof.

If you’re a Dutch solo operator, technical founder, accessibility-minded builder, or potential partner, reach out: [email/link].
```

### Company LinkedIn tagline options

1. `A practical operating system for one-person businesses.`
2. `Tools, systems, and proof for solo operators building with leverage.`
3. `Helping solo founders and Dutch self-employed professionals run cleaner, calmer businesses.`

### Company description skeleton

```text
Eenmanzak is a founder-led company building practical tools, systems, and proof assets for one-person businesses and solo technical operators.

Current focus areas:
• Dutch solo-business / ZZP operating workflows
• accessible mobile apps such as TapTap and SpatialSense
• AI-enabled founder operations without hype or unsafe automation

We believe small companies can be serious companies: clear systems, honest proof, privacy-aware operations, and focused shipping.
```

## CTA library

| Use case | CTA |
|---|---|
| Founder conversation | `Reply with how you handle this today.` |
| Research | `If this is a problem in your workflow, I’d like to hear your current workaround.` |
| Waitlist | `Join the early list for the first release.` |
| Demo | `Watch the 2-minute walkthrough.` |
| Partnership | `Email partners@... with “Partner” in the subject.` |
| Support | `Email support@... so we can help privately.` |
| Privacy | `Email privacy@... for data/privacy requests.` |
| Product Hunt | `Try it, ask anything, and tell me what’s unclear.` |

## Company-site router checklist

Use this to verify the main site is the authoritative brand hub before heavy posting.

| Page/surface | Required job |
|---|---|
| Home | one-line value prop, primary CTA, trust cues |
| About/founder | founder credibility, current role context, mission |
| Proof | demos, screenshots, case studies, permissioned testimonials |
| Product/service | current offer, pricing or next step, FAQ |
| Contact | business inbox and response route |
| Support | issue reporting and escalation route |
| Privacy | data collection, consent, retention, rights |
| Terms | only where required or useful |
| Media/partners | press, collaboration, and partnership routing |
| Links/footer | canonical outbound links to social and proof pages |

Checklist:

- [ ] All profile bios point back to the same canonical domain.
- [ ] The site contains the current company and founder language used on social profiles.
- [ ] Every public CTA has a stable URL on the site.
- [ ] Proof assets are on the site, not only in posts.
- [ ] Forms and lead capture have privacy language before traffic arrives.
- [ ] Cookie/analytics consent is in place before any tracking pixel or retargeting tool is enabled.
- [ ] The support path is separated from general inbox traffic.
- [ ] There is a documented owner for future updates.

## UTM convention

Format:

```text
utm_source={platform}
utm_medium={organic|paid|community|email|launch}
utm_campaign={yyyymm}_{campaign_slug}
utm_content={identity}_{format}_{topic_slug}
utm_term={optional_keyword_or_audience}
```

Examples:

```text
?utm_source=linkedin&utm_medium=organic&utm_campaign=202604_brand_launch&utm_content=founder_post_identity
?utm_source=producthunt&utm_medium=launch&utm_campaign=202611_taptap_launch&utm_content=maker_comment
?utm_source=reddit&utm_medium=community&utm_campaign=202604_zzp_research&utm_content=business_profile_reply
```

## Asset naming convention

```text
YYYYMMDD_identity_platform_format_topic_vNN.ext
```

Examples:

```text
20260417_company_linkedin_banner_brand-system_v01.png
20260417_founder_linkedin_post_why-eenmanzak_v01.md
20260502_taptap_youtube_demo_auto-calibration_v02.mp4
20260502_company_proof-card_processing-register_v01.png
```

## Access matrix template

| Platform | Account/URL | Owner | Backup owner | Admins | MFA | Recovery stored | Last review | Notes |
|---|---|---|---|---|---|---|---|---|
| LinkedIn |  |  |  |  |  |  |  |  |
| GitHub |  |  |  |  |  |  |  |  |
| YouTube |  |  |  |  |  |  |  |  |
| Product Hunt |  |  |  |  |  |  |  |  |
| Reddit Pro |  |  |  |  |  |  |  |  |
| Instagram |  |  |  |  |  |  |  |  |
| TikTok |  |  |  |  |  |  |  |  |
| Pinterest |  |  |  |  |  |  |  |  |

## Content calendar template

| Week | Pillar | Founder post | Company post | Video/demo | Research/listening | CTA | Status |
|---|---|---|---|---|---|---|---|
| W1 | Why / thesis |  |  |  |  |  |  |
| W2 | Problem research |  |  |  |  |  |  |
| W3 | Proof/demo |  |  |  |  |  |  |
| W4 | Lessons/roundup |  |  |  |  |  |  |

## Reply playbook

### Positive comment

```text
Thanks — this is exactly the kind of workflow I’m trying to understand better. What are you using for it today?
```

### Skeptical comment

```text
Fair challenge. The current assumption is [assumption]. The part I’m trying to validate next is [validation step]. What would make this useful/unconvincing for you?
```

### Product question

```text
Short answer: [answer]. Longer answer: [link if available]. If you want early access or want to test it, join here: [link].
```

### Support issue

```text
Thanks for flagging. Please send details to support@... so we can help without exposing private info in public comments.
```

### Legal/tax/immigration question

```text
I can share the operating context, but I don’t want to give legal/tax advice from a social thread. This needs verification with a qualified adviser. The general resource I’m using is: [official link].
```

### Creator/partnership inquiry

```text
Potentially interested. Please email partners@... with your channel, audience, proposed collaboration, and any rate card/details.
```

## Testimonial permission template

```text
Hi [Name],

Thanks again for sharing this feedback:

“[exact quote]”

Would you be comfortable with us using this quote in our public materials?

If yes, please confirm:
1. Approved quote text: [quote]
2. Attribution: [name / first name only / company / anonymous]
3. Channels allowed: website, LinkedIn, Product Hunt, pitch deck, other: ___
4. Logo/image allowed? yes/no
5. Any expiry or restrictions?

You can withdraw permission later by emailing privacy@... / support@...

Thanks,
[Name]
```

## Weekly operating rhythm

### Monday — plan

- Choose 3 founder posts.
- Choose 1 company proof post.
- Select 1 research question.
- Check product/demo asset needs.

### Tuesday-Thursday — publish and engage

- Publish founder posts.
- Comment on relevant accounts/communities.
- Capture replies/DMs into research board.

### Friday — synthesize

- Review analytics.
- Extract customer language.
- Update FAQ/objection map.
- Create next week’s asset ideas.

### Monthly — governance

- Access review.
- Privacy/processing register update.
- Channel pruning decision.
- Proof asset inventory.
- Positioning update if evidence changed.
