# Phases for 07 · Security & Sharing

21 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs before integration and Experience Cloud.** OAuth, named credentials and guest-user hardening all rest on this area. Phases 10–11 must land before 12–13 and 18–19.

---

## Phase 10 — Access model & record sharing · 12 files ⬜

```
01-security-model-layers-overview.md
02-profiles-and-the-permission-set-led-model.md    🆕⚠️
03-permission-set-groups-and-muting.md
04-user-access-policies-and-lifecycle.md           🆕
05-org-wide-defaults-and-record-access.md
06-role-hierarchy-and-ownership.md
07-sharing-rules-and-manual-sharing.md
08-teams-territories-and-account-sharing.md
09-restriction-rules.md                            ⚠️ (GA Winter '22)
10-scoping-rules.md                                (GA Summer '22)
11-field-level-security-and-visibility-layers.md
12-code-execution-context-and-security.md          🆕⚠️
```

**⚠️ corrections to lead with**
- **02** — permissions are moving **off profiles** onto permission sets. Profile-centric access design is now a migration liability. State the current status precisely from a source; **do not invent an end-of-life date for profiles.**
- **09** — **sharing is no longer additive-only.** Restriction Rules *subtract*. "The union of everything that grants access" stopped being the complete answer. This is the single most under-known change in the area.
- **12** — Apex runs in **user mode** by default at 67.0; guest and site contexts differ again. Anchor: [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

**🆕 — research before writing:** **02**, **04** (User Access Policies — automated joiner-mover-leaver), **12**.

**Notes on scope**
- **01** should be the mental model the other 20 hang off: org → object → record → field. Keep it genuinely short.
- **05** — include **implicit sharing**. It's invisible, it surprises people, and it's exam-critical.
- **10** — Scoping Rules change the *default view*, not access. Say so plainly; the two get conflated constantly.
- **11** — three different mechanisms hide a field (FLS, layout, Dynamic Forms visibility) and only one is security. Be explicit about which.

**Overlap** — **12** is the security-side twin of [02-apex · 10–11](../02-apex-and-triggers/INDEX.md), written in phase 04. Reconcile; do not let the two drift.

**Seed harvest** ([../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md)) — `UserRecordAccess Query Problem` (2025) is a real gotcha → **05** or **12**. `Apex Managed Sharing` (2023) → [02-apex · 11](../02-apex-and-triggers/INDEX.md). Two cert-prep pages (2023, 2025) may indicate weak areas worth extra depth.

---

## Phase 11 — Identity, encryption & monitoring · 9 files ⬜

```
13-sharing-recalculation-and-performance.md
14-authentication-mfa-and-session-security.md      ⚠️
15-sso-saml-oidc-and-identity.md
16-my-domain-enhanced-domains-and-trusted-urls.md  ⚠️
17-shield-platform-encryption.md
18-event-monitoring-and-transaction-security.md
19-security-center-and-health-check.md
20-privacy-consent-and-data-protection.md
21-secure-coding-checklist.md                      ⚠️
```

**⚠️ corrections to lead with**
- **14** — **MFA is contractually required**, not a recommendation. Anything framing it as optional hardening is out of date.
- **16** — **enhanced domains are enforced.** Hardcoded instance URLs and old `*.force.com` assumptions break.
- **21** — XSS advice must reflect **LWS**, not Locker ([03-lwc · 09](../03-lwc-and-slds/INDEX.md)). CRUD/FLS advice must reflect **user mode by default** — the old "always call `isAccessible()` manually" guidance is largely superseded.

**Notes on scope**
- **13** pairs with [08-data · 08 Data skew](../08-data-modeling-and-large-data-volumes/INDEX.md) — ownership skew is a sharing-recalculation problem before it is a query problem. Whichever lands first owns the detail.
- **17** — the **feature incompatibility list** is the useful part of Shield, not the crypto.
- **21** is the area's capstone: a checklist, not an essay. Every line should name the exact thing to grep for.

**Seed harvest** — `Transaction Security Policies` (2025) → **18**.
