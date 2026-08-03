# 07 · Security & Sharing

Sharing & Visibility architect depth, updated for the access model as it stands at 67.0 — including the retirement that **did not happen**. **24 topics** · phases [10](PHASES.md), [11](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **Two mental models are now wrong, and one correction is itself a correction.** (1) **The retirement of permissions from profiles was cancelled on 6 June 2026** — announced in January 2023 for Spring '26, then withdrawn. Permission-set-led design is Salesforce's *recommendation*; there is **no end-of-life date for profiles**, and asserting one in a scoping call is a credibility loss. (2) **Sharing is no longer additive-only**: restriction rules subtract, muting subtracts inside a permission set group, and since Summer '26 new queues no longer grant up the role hierarchy by default. "The union of everything that grants access" now needs three exceptions attached.

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
| 16 | Sharing recalculation & performance | deferred sharing, parallel recalc, group membership locks | 11 |
| 17 | Authentication, MFA & session security ⚠️ | MFA contractually required, session levels, high assurance | 11 |
| 18 | SSO, SAML, OIDC & identity | federated auth, JIT provisioning, Identity licences | 11 |
| 19 | My Domain, enhanced domains & Trusted URLs ⚠️ | enforced domains, CSP, Trusted URLs | 11 |
| 20 | Shield Platform Encryption | deterministic vs probabilistic, feature incompatibilities | 11 |
| 21 | Event Monitoring & Transaction Security | event log files, real-time policies, threat detection | 11 |
| 22 | Security Center & Health Check | baselines, drift, multi-org posture, Who Sees What Explorer | 11 |
| 23 | Privacy, consent & data protection | Individual object, consent model, GDPR/DSR patterns | 11 |
| 24 | Secure coding checklist ⚠️ | injection, CRUD/FLS, sharing, LWS-era XSS realities | 11 |

## Related

- **14, 24** are the security half of [02-apex · 10–11](../02-apex-and-triggers/INDEX.md). The currency anchor for both is [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md) — notes here must not contradict it.
- **14** is also the security-side twin of [04-flow · 19 Flow run context](../04-flow-and-automation/19-flow-run-context-and-sharing.md). The two agree deliberately: **Apex flipped to user mode at 67.0 and Flow did not**, so the same logic is more permissive built in Flow.
- **16** pairs with [08-data · 08 Data skew](../08-data-modeling-and-large-data-volumes/INDEX.md) — ownership skew is a sharing-recalc problem before it is a query problem.
- **02, 06** hand off to [05-experience-cloud · 08 Licences](../05-experience-cloud-lwr/INDEX.md) and **· 09 Sharing for external users** — external licence types, sharing sets and share groups are owned there, not here.
- **17–18** feed [06-integration · 13 OAuth](../06-integration-and-apis/INDEX.md) and [05-experience-cloud · 10 SSO](../05-experience-cloud-lwr/INDEX.md).
- **24** must reflect [03-lwc · 09 LWS](../03-lwc-and-slds/INDEX.md), not Locker-era XSS advice.
- **15 is the note the other 23 depend on in practice.** With eight granting mechanisms, three narrowing ones and two hierarchies in play, reading the configuration stopped being a reliable way to answer an access question.
