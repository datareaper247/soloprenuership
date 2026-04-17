# Register Templates

**Status:** Draft
**Last updated:** 2026-04-17
**Purpose:** Operational templates for social-account governance, GDPR/privacy hygiene, AI-tool use, and monthly reviews.

## 1. Account inventory register

Maintain one row per social/platform/business-critical account.

| Field | Requirement |
|---|---|
| Account name | Exact display name and handle |
| Platform | LinkedIn, GitHub, YouTube, Product Hunt, Reddit, Instagram, TikTok, Pinterest, domain, email, analytics, etc. |
| Brand role | Founder, company, product, support, ads, analytics, newsletter, community, partner |
| Public URL | Public account URL |
| Admin URL | Admin/Business Manager URL where applicable |
| Business owner | Accountable person |
| Backup owner | Named continuity owner |
| Admins | Named humans only |
| External users | Agencies, freelancers, creators, vendors |
| Access level | Owner/admin/editor/content admin/analyst/viewer/publisher |
| Login method | Business role, personal profile delegation, SSO, email/password, OAuth |
| Password manager item | Vault/path reference |
| MFA method | Security key/passkey/authenticator/SMS fallback |
| Recovery codes location | Secure note or break-glass vault path |
| Recovery email/phone | Business-controlled where possible |
| Data processed | DMs, comments, leads, analytics, ad audiences, testimonials, screenshots |
| Processor/subprocessor | Platform/vendor name |
| Transfer risk | EEA/non-EEA/unknown; review notes |
| Retention rule | How long copied/exported data is retained |
| Last access review | Date + reviewer |
| Last password/MFA review | Date |
| Connected apps | OAuth/tools/plugins with access |
| Incident history | Links to incidents/lockouts/phishing/impersonation |
| Decommission plan | Archive, transfer, redirect, delete |

## 2. Processing register template

Use for GDPR/AVG record of processing activities. Professional review required.

| Field | Description |
|---|---|
| Processing ID | Stable ID, e.g. `SOCIAL-DM-001` |
| Processing name | Social DMs, lead capture/contact forms, newsletter, waitlist, testimonials, support, creator partnerships |
| Business owner | Accountable person |
| Privacy owner | Reviewer/owner |
| Controller | Legal/trade name and contact |
| Purpose | Specific purpose, not just “marketing” |
| Data subjects | Leads, users, customers, creators, partners, commenters |
| Personal data categories | Email, name, handle, DM content, analytics IDs, consent records |
| Special category data | Normally “not intentionally collected”; note accidental handling process |
| Source | Direct, platform, form, public profile, partner |
| Lawful basis | Consent, contract, legitimate interest, legal obligation, etc. |
| Consent record location | Form/tool/database path |
| Recipients | Platforms, CRM, email provider, analytics, contractors |
| Processors | Vendors processing on behalf of business |
| Joint controllers | Platform ads/targeting contexts if applicable; verify |
| International transfers | Non-EEA? adequacy/SCC/TIA notes |
| Retention period | Concrete period or event-driven rule |
| Deletion method | Manual/automated/platform-dependent |
| Data subject rights process | Access/delete/correction route |
| Security measures | MFA, RBAC, encryption, password manager, logging |
| Cookie/ePrivacy impact | Yes/no; consent mechanism |
| AI use | None / anonymized / personal data / prohibited |
| Risk level | Low/Medium/High |
| Review frequency | Monthly/quarterly/annual |
| Last reviewed | Date |
| Professional verification | Not reviewed / reviewed / needs review |

## 3. AI tools register

| Field | Requirement |
|---|---|
| Tool/vendor | Name and URL |
| Use case | Drafting, images, video, subtitles, analytics, support, summarization |
| Data allowed | Public only / internal / personal data / prohibited |
| Data prohibited | Explicit categories not allowed |
| Training setting | Whether inputs can train models; setting chosen |
| DPA/terms reviewed | Yes/no/date |
| International transfer review | Yes/no |
| Owner | Named |
| Risk level | Low/Medium/High |
| Approved until | Review date |
| Human approval required | Always for public content |
| Disclosure needed? | By platform/content type |
| Notes | Restrictions and escalation |

## 4. Monthly access review template

| Check | Status | Notes |
|---|---|---|
| All accounts still needed |  |  |
| Owners and backup owners correct |  |  |
| No unknown admins |  |  |
| Contractors/agencies still valid |  |  |
| MFA enabled |  |  |
| Recovery codes present |  |  |
| Password manager items current |  |  |
| OAuth/connected apps reviewed |  |  |
| Ad account/payment users reviewed |  |  |
| CRM/newsletter exports reviewed |  |  |
| AI tools with personal data reviewed |  |  |
| Privacy/processing register updated |  |  |
| Testimonial permissions still valid |  |  |
| Underused accounts pruned/redirected |  |  |
| Incidents closed or escalated |  |  |

## 5. Testimonial permission record

| Field | Requirement |
|---|---|
| Person/company | Name as approved |
| Quote/content | Exact approved text or asset |
| Attribution | Full name / first name / company / anonymous |
| Channels allowed | Website, LinkedIn, Product Hunt, pitch deck, ads, etc. |
| Logo/photo allowed | Yes/no + asset link |
| Editing rights | Exact only / light edits / anonymized / paraphrase |
| Expiry/review date | Recommended 12 months |
| Withdrawal route | Email/form |
| Consent timestamp | Required |
| Consent evidence | Stored link/path |
| Sensitive claims review | Required for financial/legal/tax/health outcomes |
