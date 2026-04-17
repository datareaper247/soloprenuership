# Governance, Security, Privacy, and Compliance

**Status:** Draft; legal/privacy review required
**Last updated:** 2026-04-17
**Source IDs:** U05-U06, E03-E08, E10-E25, L03-L07

> This document is operational guidance, not legal/tax/immigration advice. Verify privacy, advertising, consumer, KVK, WBSO, tax, and immigration-sensitive claims with qualified professionals before relying on them publicly.

## Governance principles

1. **Least privilege** — give each person/tool only what they need.
2. **No shared passwords** — use role-based access, Business Manager, org roles, or invite systems.
3. **Business-controlled recovery** — ownership and recovery should not depend on one personal inbox.
4. **Human approval before public output** — AI can draft, clip, subtitle, repurpose, and summarize; humans approve.
5. **Privacy by design** — every DM, waitlist, form, testimonial, and support conversation has a processing basis and retention rule.
6. **Proof with permission** — no screenshots, names, logos, quotes, or customer stories without consent.
7. **Compliance humility** — do not overstate legal/tax/WBSO/visa conclusions in marketing.

## Ownership and access model

### Account ownership minimums

| Platform/surface | Primary owner | Backup owner | Least-privilege roles |
|---|---|---|---|
| Domain/DNS | Founder business email | backup admin | registrar admin only as needed |
| Email/workspace | Founder | backup admin | mailbox-specific access |
| LinkedIn Page | Founder personal account as super admin | trusted backup super admin | content admin, analyst, paid-media roles |
| GitHub org | Founder personal GitHub account | second org owner | member, repo roles, security manager |
| YouTube Brand Channel | founder Google account | second owner | manager/editor roles where possible |
| Product Hunt pages | founder maker account / product owner | trusted member | Owner/Member roles |
| Meta/Instagram | business portfolio owner | backup admin | task/content/ad access |
| Reddit Pro | business username owner | recovery email owner | avoid shared login if no proper roles |
| TikTok | business/organization account owner | backup recovery owner if available | avoid contractor password sharing |
| Pinterest | Account Owner | Manager | Employee/Partner/Publisher |
| Password manager | Founder | emergency access contact | vault item access by need |

### Non-negotiables

- MFA/2FA on every platform.
- Password manager vaults, not chat/email passwords.
- Recovery codes stored in secure vault with emergency access.
- Monthly access review.
- Immediate offboarding after contractor/agency/project changes.
- Platform ownership documented in access matrix.
- No personal-device-only recovery for business-critical channels.

## Platform-specific governance notes

### LinkedIn

- Use founder account to create/manage Page.
- Founder should remain super admin.
- Content operators get content admin, not super admin.
- Analysts get analyst role only.
- Admin candidates need to follow Page and generally be within 1st/2nd/3rd-degree connection.
- Do not create Showcase Pages without a maintenance cadence; inactive Showcase Pages can become problematic after six months without posts.

### GitHub

- Keep at least two organization owners, but minimize owner count.
- Require 2FA where available.
- Use teams and repository roles; avoid everyone-as-admin.
- Restrict repo creation/visibility changes once collaborators exist.
- Use private repos until public proof is intentionally ready.
- Add security/contact policy before public repos receive users.

### YouTube

- Use Brand Account/channel for company/product channel.
- Add backup owner; primary owner transfer has a 7-day owner-status condition.
- Use YouTube Studio permissions/Brand Account roles instead of shared Google credentials.
- Keep raw source files in company storage, not only on one editor’s machine.

### Product Hunt

- Founder/maker account must be real and personal.
- Company accounts cannot post/hunt products.
- Claim Product Pages with company-domain email when possible.
- Keep owner/member roles current after launches.

### Meta / Instagram

- Use professional/business account only if public profile and business tools are intended.
- Configure Meta Business access from desktop and avoid sharing Instagram login.
- Contractors should receive task/content access, not full admin by default.
- Verify in Meta Business Suite directly because help-page retrieval and UI behavior can vary.

### Reddit Pro

- Use a new business username if the founder already has a personal Reddit identity.
- Treat Pro insights as internal research; do not publish Reddit Pro screenshots/data without Reddit consent.
- Do not quote or reuse redditor content in marketing without permission.
- If replying publicly, disclose affiliation and be useful before linking.

### TikTok

- Use Business Account when primary goal is business promotion.
- Use Commercial Music Library for business content.
- Use content disclosure setting for promotional/commercial content.
- Label realistic/significantly AI-generated content.
- Do not reserve a TikTok handle unless someone logs in and keeps it active; inactive accounts may lose username after 180 days.

### Pinterest

- Use professional email/name for employees/agencies.
- Distinguish Account Owner, Manager, Employee, Partner, Publisher.
- Publisher can create/edit/organize Pins and boards; treat it as powerful organic-content access.

## Privacy operating model

If socials collect or process personal data, they are part of the data-processing footprint.

Examples:

- social DMs,
- contact forms,
- waitlists,
- newsletter signups,
- webinar registrations,
- Product Hunt commenters you follow up with,
- support tickets,
- testimonial permissions,
- customer logos,
- community member data,
- analytics tied to identifiable users.

KVK guidance says a processing register should capture purposes, data subjects, data types, recipients, security measures, retention, and non-EU transfers.

### Processing register starter entries

| Process | Data subjects | Data | Purpose | Legal basis placeholder | Recipients/processors | Retention draft | Security |
|---|---|---|---|---|---|---|---|
| Social DMs | prospects, users, partners | name/handle, messages, contact info | support, sales, research | legitimate interest / consent / contract depending case | platform, CRM/helpdesk if used | 12-24 months unless support/legal need | MFA, least privilege |
| Newsletter | subscribers | email, name optional, preferences, opens/clicks | send updates | consent | email provider | until unsubscribe + suppression record | MFA, DPA |
| Waitlist | prospects | email, role, problem, product interest | beta/access notification | consent / pre-contract | form tool, database/email provider | until launch + 12 months unless opted in | access controls |
| Product support | users/customers | email, issue content, device/browser, attachments | resolve support | contract / legitimate interest | helpdesk, engineering tools | 24 months unless legal/accounting need | ticket permissions |
| Testimonials | customers/users | quote, name, company, image/logo if applicable | proof/marketing | explicit permission | website/social tools | until withdrawn or campaign ends | permission log |
| Community research | public commenters/users | public handles/comments summarized | market research | legitimate interest; verify | research docs, Reddit Pro | minimize; do not store unnecessary personal data | anonymize where possible |
| Creator partnerships | creators | contracts, handles, payment info, content approvals | campaign execution | contract/legal obligation | accountant, payment provider | fiscal retention as required | restricted vault |

### Permission log for proof assets

Maintain a `proof-permissions` sheet with:

- person/company,
- asset type: quote/logo/screenshot/case study/video,
- exact approved wording,
- approved channels,
- date granted,
- expiry/withdrawal terms,
- approver/contact,
- storage link,
- revocation status.

## AI-content guardrails

### Default rule

> AI may draft, brainstorm, repurpose, subtitle, clip, summarize, and generate variants. A human approves every public post, reply, DM, ad, and creator brief.

### Approval checklist for AI-assisted content

Before publishing, confirm:

- facts verified,
- no confidential data,
- no unapproved personal data,
- no implied customer endorsement without permission,
- no IP/trademark issue,
- platform AI disclosure considered,
- commercial/promotional disclosure considered,
- tone matches founder/company voice,
- no legal/tax/medical/financial certainty beyond evidence,
- source links retained where claims matter.

### Platform AI rules to encode

| Platform | Guardrail |
|---|---|
| LinkedIn | Review, edit, and approve AI-assisted content; poster remains responsible; disclose heavy AI use when not obvious; avoid IP/privacy infringement. |
| YouTube | Disclose meaningfully altered/synthetic realistic content during upload. Minor production assistance like outline, captions, thumbnail, or color correction may not require disclosure, but realistic/meaningful edits do. |
| TikTok | Label realistic/significantly AI-generated content; commercial/promotional content also needs content disclosure setting. |
| Instagram/Threads | Verify current Meta labeling behavior before publishing synthetic or heavily AI-altered content; maintain human approval. |

## Cookies, analytics, and paid targeting

Before enabling analytics pixels, retargeting, conversion tags, or custom audiences:

- document which tool is used,
- update privacy/cookie notices,
- obtain cookie consent where required,
- avoid pre-checked or misleading cookie banners,
- document retention and international transfer risk,
- avoid sensitive-category targeting,
- keep screenshots/exports of consent text and privacy policy versions.

For early-stage validation, prefer privacy-light measurement first: server logs, first-party form source fields, UTM parameters, and aggregate dashboarding before heavy ad-tech.

## Creator / influencer partnerships

If creators promote the company/product:

- contract the deliverables,
- require clear ad/sponsorship disclosure,
- define review/approval rights,
- define usage rights and duration,
- collect invoice/payment/tax info securely,
- maintain proof of approvals,
- keep claims substantiated.

KVK notes that advertisers hiring influencers are responsible and that ad relationships must be clearly recognizable under applicable rules.

## Support and escalation rules

### Public replies

Acknowledge, route, and resolve without exposing personal data.

Template:

> Thanks for flagging this. We’ll look into it. Please email `support@...` with the details so we can help without exposing private information here.

### Escalation matrix

| Issue | Public response | Private action | Owner |
|---|---|---|---|
| Bug report | thank + route to support | create ticket | support/product |
| Billing/refund | do not discuss details | support inbox | founder/support |
| Privacy request | route to privacy email | log request | privacy owner |
| Security report | route to security contact | triage privately | security owner |
| Legal/tax question | general caveat only | refer to qualified adviser | founder/legal |
| Harmful/abusive comment | enforce moderation policy | screenshot + hide/block/report as needed | community owner |
| Viral complaint | acknowledge + investigate | incident log + response plan | founder |

## Monthly access review

Every month:

- export/check platform admins,
- verify MFA status,
- review contractors/agencies,
- rotate shared legacy credentials if any still exist,
- verify backup owner access,
- update recovery codes,
- review connected third-party apps,
- review public profiles for stale links,
- update the access matrix.

## Incident playbook

If account compromise or risky post occurs:

1. Freeze publishing.
2. Change/rotate affected credentials and revoke sessions.
3. Remove suspicious third-party apps.
4. Preserve screenshots/logs.
5. Notify platform support if needed.
6. Assess personal data exposure.
7. If personal data may be breached, consult GDPR/data-breach obligations immediately.
8. Publish correction only after facts are known.
9. Document root cause and prevention.
