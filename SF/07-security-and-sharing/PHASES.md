# Phases for 07 · Security & Sharing

24 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs before integration and Experience Cloud.** OAuth, named credentials and guest-user hardening all rest on this area. Phases 10–11 must land before 12–13 and 18–19.

> **The area grew from 21 to 24 at phase-10 plan time, and was renumbered in learning order.** Three topics were inserted — **02** (licences), **08** (groups, queues and grantees) and **15** (access auditing) — pushing the old 05–12 to 06–14 and the whole phase-11 block from 13–21 to 16–24. **This renumber was nearly free and will never be this cheap again:** not one file in the area existed, so intra-area churn was zero, and a grep found exactly **three** inbound lines in the whole vault that referenced area 07 by number. All three were fixed in the same commit. **Do not renumber this area again without repeating that grep.**

---

## Phase 10 — Access model & record sharing · 15 files ✅

```
01-security-model-layers-overview.md
02-licences-and-what-they-gate.md                  🆕    ← ADDED at plan time
03-profiles-and-the-permission-set-led-model.md    🆕⚠️
04-permission-set-groups-and-muting.md
05-user-access-policies-and-lifecycle.md           🆕
06-org-wide-defaults-and-record-access.md                (was 05)
07-role-hierarchy-and-ownership.md                       (was 06)
08-groups-queues-and-the-grantee-model.md          🆕⚠️  ← ADDED at plan time
09-sharing-rules-and-manual-sharing.md                   (was 07)
10-teams-territories-and-account-sharing.md              (was 08)
11-restriction-rules.md                            ⚠️    (was 09)
12-scoping-rules.md                                      (was 10)
13-field-level-security-and-visibility-layers.md   🆕⚠️  (was 11, flag added at plan time)
14-code-execution-context-and-security.md          🆕⚠️  (was 12)
15-auditing-and-troubleshooting-access.md          🆕    ← ADDED at plan time
```

**Three files added before the run.** Each closed a hole another note had already promised someone would fill:

- **02** — [01-admin · 01](../01-admin-and-declarative-platform/01-org-anatomy-and-editions.md) says *"Stops at licences and permission assignment — that is 07-security"*, and nothing in the 21-topic plan answered it. Licence is the outermost gate and the one people debug last.
- **08** — [01-admin · 11](../01-admin-and-declarative-platform/11-queues-assignment-and-escalation-rules.md) forward-links here for *"what queue ownership means for sharing"*. Nothing owned groups, queues or roles **as grantees**, despite every sharing mechanism in the area granting to one.
- **15** — nothing owned *"why can this user see this record?"*, which is the question the exam and the job both ask.

### Retro

**⚠️ — the plan's headline correction was itself out of date, and the wrong sentence was already published in this vault**

- **03 — Salesforce CANCELLED the retirement of permissions in profiles on 6 June 2026.** Help article **003834041**: *"Salesforce previously announced the retirement of permissions in profiles starting in Spring '26. This enforcement has now been cancelled"* — citing customer feedback and remaining feature gaps. Announced 23 January 2023, cancelled two months before this phase ran. The plan text and the **live area INDEX banner** both asserted that profile-centric design was "a migration liability" because permissions were "moving off profiles". Permission-set-led design remains Salesforce's stated *recommendation*; the **deadline is gone and no end-of-life date exists**. This is the **seventh instance of "old ≠ dead" in this build**, after Lightning Locker, `if:true`, `System.assertEquals`, page layouts, classic approvals and Workflow Rules/Process Builder — and the first where the vault had already published the error rather than merely planned it. The plan's own instinct (*"do not invent an end-of-life date for profiles"*) was right and did not go far enough.

**🆕 the plan did not flag — four Summer '26 changes, one of which is a default flip**

- **08 — queues gained `Grant Access Using Hierarchies`, and the default depends on the queue's age**: **on** for queues that already existed, **off** for queues created from Summer '26 onward, with an org-level *Grant access using hierarchies by default in new queues* switch on the Sharing Settings page that affects new queues only. Any model assuming managers see the queue backlog breaks silently on new queues. Recorded in [../CURRENCY.md](../CURRENCY.md).
- **13 — Unified Field Access review** puts a **Field Access tab** on every object in Object Manager, showing how each field's access is granted across profiles, permission sets and permission set groups. It is **read-only**, which is the caveat worth carrying.
- **03 — `Enable Profile Filtering` is a Release Update**, available Summer '26 and **enforced Winter '27**: users see only their own profile name without `View All Profiles`. The enhanced profile view also now previews **indirect permission changes** before saving.
- **05 — User Access Policies are GA since Summer '24, not new.** The 🆕 stands on absence from older material. Concrete limits found: **200 active policies**, **Enterprise and Unlimited only**, **never retroactive** (they fire on user create/update, so existing matching users need the manual one-time application), **policies cannot trigger policies**, and group/queue membership management reaches **only directly-added members**.

**Other corrections made while writing**

- **The additive-only summary now needs three exceptions, not one.** The plan named restriction rules. Muting subtracts inside a permission set group (**04**), and Summer '26's queue setting removes an upward grant (**08**). Stated as a pattern in **08** and **11**: the platform keeps adding narrowing controls to a model that began as pure union.
- **Restriction rules do not cover the core CRM objects.** Supported list is custom objects, external objects, Contract, Event, Quote, Task, Time Sheet and Time Sheet Entry — **not** Account, Contact, Lead, Opportunity or Case, which is the commonest ask. Limits are **2** active rules per object in Enterprise/Developer and **5** in Performance/Unlimited.
- **Who Sees What Explorer is inside Security Center, a paid add-on.** Flagged in **15** so the free native surfaces (User Access Summary, Field Access tab, Sharing button, `UserRecordAccess`) are not confused with the licensed one. Product and posture detail deferred to **22** in phase 11.

**Seed harvest** · *four pages read, all four substantive — the richest harvest of the build so far*

- **15** — `UserRecordAccess Query Problem` (**2025**). → *harvested, and it is **not** a duplicate of the phase-04 harvest in [02-apex · 11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md). That one covered the SOQL constraints; this page is about a **Flow Get Records** element, where **Store All Fields fails** because Flow retrieves unsupported fields such as `Id` (Salesforce KB `000383422`), and where "no access" is the **zero-row** case that needs* When no records are returned, set specified variables to null *or it errors instead of answering.*
- **06, 08, 10, 14** — `Salesforce Certified Sharing and Visibility Architect` (**2025**), which the inventory listed only as "may indicate weak areas". → *it is a 14-question scenario bank and four questions were worth harvesting: the **implicit-sharing** trap in its concrete form (Private Account OWD + Opportunity edit = **read-only** on the parent) → **06**; **granular locking as the tool for large-scale role-hierarchy realignment** and **three roles created with the first partner-account external user** → **08**; the **opportunity-team-plus-Apex** shape for a per-record helper grant → **10**; and one question whose **marked answer is now wrong** — `isUpdateable()` per field to fix an FLS bypass, when a 67.0 class enforces FLS by default and the `WITH SECURITY_ENFORCED` distractor no longer compiles → corrected inline in **14**.*
- **`Sharing and Visibility Architect` (2023)** → *read, thin as predicted: a Health Check screenshot and one line saying to group permission sets by job function. The Health Check half belongs to **22** in phase 11; the permission-set line was already the substance of **04**. No callout.*
- **`Apex Managed Sharing` (2023)** → *inventory maps it to [02-apex · 11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md), written in phase 04. Re-read here for one line worth keeping: **sharing rules and manual sharing do not support high-volume community users**, who have no roles. That belongs to [05-experience-cloud · 09](../05-experience-cloud-lwr/INDEX.md) — noted for phase 18 rather than harvested here.*

**Rule 1 exceeded deliberately, with approval** — three files added, and the correction sweep reached [../CURRENCY.md](../CURRENCY.md), [../PHASES.md](../PHASES.md), [../README.md](../README.md), [08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md) and [05-experience-cloud · INDEX + PHASES](../05-experience-cloud-lwr/INDEX.md), because the cancelled retirement made a published sentence wrong and the renumber moved three inbound links. Same call phases 08 and 09 made, for the same reason.

---

## Phase 11 — Identity, encryption & monitoring · 9 files ⬜

```
16-sharing-recalculation-and-performance.md              (was 13)
17-authentication-mfa-and-session-security.md      ⚠️    (was 14)
18-sso-saml-oidc-and-identity.md                         (was 15)
19-my-domain-enhanced-domains-and-trusted-urls.md  ⚠️    (was 16)
20-shield-platform-encryption.md                         (was 17)
21-event-monitoring-and-transaction-security.md          (was 18)
22-security-center-and-health-check.md                   (was 19)
23-privacy-consent-and-data-protection.md                (was 20)
24-secure-coding-checklist.md                      ⚠️    (was 21)
```

**⚠️ corrections to lead with**
- **17** — **MFA is contractually required**, not a recommendation. Anything framing it as optional hardening is out of date.
- **19** — **enhanced domains are enforced.** Hardcoded instance URLs and old `*.force.com` assumptions break.
- **24** — XSS advice must reflect **LWS**, not Locker ([03-lwc · 09](../03-lwc-and-slds/INDEX.md)). CRUD/FLS advice must reflect **user mode by default** — the old "always call `isAccessible()` manually" guidance is largely superseded, and phase 10 already corrected a seed page that got this wrong ([14](14-code-execution-context-and-security.md)).

**Notes on scope**
- **16** pairs with [08-data · 08 Data skew](../08-data-modeling-and-large-data-volumes/INDEX.md) — ownership skew is a sharing-recalculation problem before it is a query problem. Whichever lands first owns the detail. **Phase 10 already placed granular locking in [08](08-groups-queues-and-the-grantee-model.md)** as the role-hierarchy-realignment tool; **16** owns the recalculation mechanics, not that framing.
- **20** — the **feature incompatibility list** is the useful part of Shield, not the crypto.
- **22** — owns **Who Sees What Explorer** as a product, including that Security Center is a **paid add-on**. [15](15-auditing-and-troubleshooting-access.md) already owns its five lenses as an access tool; do not duplicate.
- **24** is the area's capstone: a checklist, not an essay. Every line should name the exact thing to grep for.

**Seed harvest** — `Transaction Security Policies` (2025) → **21**. The Health Check half of `Sharing and Visibility Architect` (2023) → **22**, read in phase 10 and left unharvested for it.
