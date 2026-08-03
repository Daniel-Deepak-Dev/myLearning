# 07 · Security & Sharing

Sharing & Visibility architect depth, updated for the access model as it stands at 67.0 — including the retirement that **did not happen** and the enforcement wave that did. **26 topics** · phases [10](PHASES.md), [11](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **Three mental models are now wrong, and one correction is itself a correction.** (1) **The retirement of permissions from profiles was cancelled on 6 June 2026** — announced in January 2023 for Spring '26, then withdrawn. Permission-set-led design is Salesforce's *recommendation*; there is **no end-of-life date for profiles**, and asserting one in a scoping call is a credibility loss. (2) **Sharing is no longer additive-only**: restriction rules subtract, muting subtracts inside a permission set group, and since Summer '26 new queues no longer grant up the role hierarchy by default. "The union of everything that grants access" now needs three exceptions attached. (3) **Security posture stopped being advisory in mid-2026.** MFA is enforced rather than contractual, privileged users need **phishing-resistant** methods, report exports over 10,000 rows trigger step-up, and legacy My Domain URLs 404 instead of redirecting. Anything describing these as recommendations predates July 2026.

> Runs early (phases 10–11) because [06-integration](../06-integration-and-apis/INDEX.md) and [05-experience-cloud](../05-experience-cloud-lwr/INDEX.md) both rest on it.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | [Security model layers overview](01-security-model-layers-overview.md) | licence → org → object → record → field, and the debugging order | 10 |
| 02 | [Licences & what they gate](02-licences-and-what-they-gate.md) 🆕 | user vs permission set vs feature licence; what a permission set cannot exceed | 10 |
| 03 | [Profiles & the permission-set-led model](03-profiles-and-the-permission-set-led-model.md) 🆕⚠️ | **retirement cancelled**; `Enable Profile Filtering` enforced Winter '27 | 10 |
| 04 | [Permission Set Groups & muting](04-permission-set-groups-and-muting.md) | grouping, muting's floor, session-based activation | 10 |
| 05 | [User Access Policies & lifecycle](05-user-access-policies-and-lifecycle.md) 🆕 | GA Summer '24; 200 active, never retroactive, EE/UE only | 10 |
| 06 | [Org-wide defaults & record access](06-org-wide-defaults-and-record-access.md) | OWD, external OWD, **implicit sharing** | 10 |
| 07 | [Role hierarchy & ownership](07-role-hierarchy-and-ownership.md) | upward grants, roles are not permissions, ownership skew | 10 |
| 08 | [Groups, queues & the grantee model](08-groups-queues-and-the-grantee-model.md) 🆕⚠️ | a queue is a group; **new queues don't grant up the hierarchy** | 10 |
| 09 | [Sharing rules & manual sharing](09-sharing-rules-and-manual-sharing.md) | share rows, `RowCause`, manual shares die on owner change | 10 |
| 10 | [Teams, territories & account sharing](10-teams-territories-and-account-sharing.md) | per-record grants, the second hierarchy, one active model | 10 |
| 11 | [Restriction rules](11-restriction-rules.md) ⚠️ *(GA Winter '22)* | sharing is no longer additive-only; 2/5 per object by edition | 10 |
| 12 | [Scoping rules](12-scoping-rules.md) *(GA Summer '22)* | default record scope, **not** access; the user can widen it | 10 |
| 13 | [Field-level security & visibility layers](13-field-level-security-and-visibility-layers.md) 🆕⚠️ | FLS vs layout vs Dynamic Forms; Summer '26 Field Access tab | 10 |
| 14 | [Code execution context & security](14-code-execution-context-and-security.md) 🆕⚠️ | user mode at 67.0, Flow did not follow, guest and agent contexts | 10 |
| 15 | [Auditing & troubleshooting access](15-auditing-and-troubleshooting-access.md) 🆕 | User Access Summary, `Access Granted By`, `UserRecordAccess`, `RowCause` | 10 |
| 16 | [Sharing recalculation & performance](16-sharing-recalculation-and-performance.md) 🆕⚠️ | **async recalc Release Update, enforced Spring '27**; deferred sharing, granular locking | 11 |
| 17 | [Authentication & MFA](17-authentication-and-mfa.md) ⚠️ | **MFA enforced, not contractual**; phishing-resistant MFA for privileged users | 11 |
| 18 | [Session security, login policies & step-up](18-session-security-login-policies-and-step-up.md) 🆕 | assurance levels, login IP, **step-up on report export** | 11 |
| 19 | [SSO, SAML, OIDC & identity](19-sso-saml-oidc-and-identity.md) 🆕 | federation, JIT, Identity licences, certificate expiry | 11 |
| 20 | [My Domain, enhanced domains & Trusted URLs](20-my-domain-enhanced-domains-and-trusted-urls.md) ⚠️ | **redirections ended Spring '26**; instanced URLs die Winter '27 | 11 |
| 21 | [Shield Platform Encryption](21-shield-platform-encryption.md) | deterministic vs probabilistic, the incompatibility list, key custody | 11 |
| 22 | [Field Audit Trail & data retention](22-field-audit-trail-and-data-retention.md) | 60 fields, 10 years, `FieldHistoryArchive`, `HistoryRetentionPolicy` | 11 |
| 23 | [Event Monitoring & Transaction Security](23-event-monitoring-and-transaction-security.md) 🆕⚠️ | **legacy framework retired**; auto-created report-export policy | 11 |
| 24 | [Security Center & Health Check](24-security-center-and-health-check.md) 🆕⚠️ | **Essentials free Jul 2026**; baselines, drift, Who Sees What Explorer | 11 |
| 25 | [Privacy, consent & data protection](25-privacy-consent-and-data-protection.md) | `Individual`, the four consent levels, DSR patterns, Data Mask | 11 |
| 26 | [Secure coding checklist](26-secure-coding-checklist.md) ⚠️ | 16 checks, each naming what to grep for | 11 |

## Related

- **14, 26** are the security half of [02-apex · 10–11](../02-apex-and-triggers/INDEX.md). The currency anchor for both is [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md) — notes here must not contradict it.
- **14** is also the security-side twin of [04-flow · 19 Flow run context](../04-flow-and-automation/19-flow-run-context-and-sharing.md). The two agree deliberately: **Apex flipped to user mode at 67.0 and Flow did not**, so the same logic is more permissive built in Flow.
- **[16](16-sharing-recalculation-and-performance.md)** pairs with [08-data · 10 Data skew](../08-data-modeling-and-large-data-volumes/10-data-skew.md) — ownership skew is a sharing-recalc problem before it is a query problem, and this note landed first so it owns the mechanics.
- **02, 06** hand off to [05-experience-cloud · 08 Licences](../05-experience-cloud-lwr/INDEX.md) and **· 09 Sharing for external users** — external licence types, sharing sets and share groups are owned there, not here.
- **17–19** feed [06-integration · 15 OAuth](../06-integration-and-apis/15-oauth-flows-and-authorization.md) and [05-experience-cloud · 10 SSO](../05-experience-cloud-lwr/INDEX.md).
- **21–23 are Shield's three pillars** — encryption, field audit, event monitoring — and are licensed together. Scope a compliance requirement against entitlement before design.
- **26** must reflect [03-lwc · 09 LWS](../03-lwc-and-slds/INDEX.md), not Locker-era XSS advice.
- **15 is the note the other 25 depend on in practice.** With eight granting mechanisms, three narrowing ones and two hierarchies in play, reading the configuration stopped being a reliable way to answer an access question.
