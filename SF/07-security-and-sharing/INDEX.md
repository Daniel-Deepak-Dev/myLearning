# 07 · Security & Sharing

Sharing & Visibility architect depth, updated for permission-set-led access and **subtractive** rules. **21 topics** · phases [10](PHASES.md), [11](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **Two mental models are now wrong.** (1) Permissions are moving **off profiles** onto permission sets — profile-centric access design is a migration liability. (2) **Sharing is no longer additive-only**: Restriction Rules subtract access, so "the union of everything that grants it" is no longer the whole answer.

> Runs early (phases 10–11) because [06-integration](../06-integration-and-apis/INDEX.md) and [05-experience-cloud](../05-experience-cloud-lwr/INDEX.md) both rest on it.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | Security model layers overview | org → object → record → field mental model | 10 |
| 02 | Profiles & the permission-set-led model 🆕⚠️ | permissions moving off profiles; migration plan | 10 |
| 03 | Permission Set Groups & muting | grouping, muting, session-based activation | 10 |
| 04 | User Access Policies & lifecycle 🆕 | automated grant/revoke for joiner-mover-leaver | 10 |
| 05 | Org-wide defaults & record access | OWD, external OWD, implicit sharing | 10 |
| 06 | Role hierarchy & ownership | hierarchy grants, ownership skew risks | 10 |
| 07 | Sharing rules & manual sharing | owner/criteria rules, manual shares, share objects | 10 |
| 08 | Teams, territories & account sharing | account/opportunity teams, Enterprise Territory Management | 10 |
| 09 | Restriction Rules ⚠️ *(GA Winter '22)* | sharing is no longer additive-only | 10 |
| 10 | Scoping Rules *(GA Summer '22)* | default record scope without changing access | 10 |
| 11 | Field-level security & visibility layers | FLS vs layout vs Dynamic Forms visibility | 10 |
| 12 | Code execution context & security 🆕⚠️ | user mode defaults, run-as, guest and site contexts | 10 |
| 13 | Sharing recalculation & performance | deferred sharing, parallel recalc, group membership locks | 11 |
| 14 | Authentication, MFA & session security ⚠️ | MFA contractually required, session levels, high assurance | 11 |
| 15 | SSO, SAML, OIDC & identity | federated auth, JIT provisioning, Identity licences | 11 |
| 16 | My Domain, enhanced domains & Trusted URLs ⚠️ | enforced domains, CSP, Trusted URLs | 11 |
| 17 | Shield Platform Encryption | deterministic vs probabilistic, feature incompatibilities | 11 |
| 18 | Event Monitoring & Transaction Security | event log files, real-time policies, threat detection | 11 |
| 19 | Security Center & Health Check | baselines, drift, multi-org posture | 11 |
| 20 | Privacy, consent & data protection | Individual object, consent model, GDPR/DSR patterns | 11 |
| 21 | Secure coding checklist ⚠️ | injection, CRUD/FLS, sharing, LWS-era XSS realities | 11 |

## Related

- **12, 21** are the security half of [02-apex · 10–11](../02-apex-and-triggers/INDEX.md). Write them consistently — the currency anchor for both is [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).
- **13** pairs with [08-data · 08 Data skew](../08-data-modeling-and-large-data-volumes/INDEX.md) — ownership skew is a sharing-recalc problem before it is a query problem.
- **14–15** feed [06-integration · 13 OAuth](../06-integration-and-apis/INDEX.md) and [05-experience-cloud · 10 SSO](../05-experience-cloud-lwr/INDEX.md).
- **21** must reflect [03-lwc · 09 LWS](../03-lwc-and-slds/INDEX.md), not Locker-era XSS advice.
