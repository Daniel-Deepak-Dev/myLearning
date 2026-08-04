# Phases for 07 · Security & Sharing

26 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs before integration and Experience Cloud.** OAuth, named credentials and guest-user hardening all rest on this area. Phases 10–11 must land before 12–13 and 18–19.

> **The area grew again at phase-11 plan time, from 24 to 26 — but by appending and shifting only, never inserting.** Files 16–26 moved; 01–15 did not. The phase-10 grep below was repeated first and found one inbound number reference outside the area, unaffected. **Do not renumber 01–15 at all now that they exist.**

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
- **Who Sees What Explorer is inside Security Center, a paid add-on.** Flagged in **15** so the free native surfaces (User Access Summary, Field Access tab, Sharing button, `UserRecordAccess`) are not confused with the licensed one. Product and posture detail deferred to phase 11 — which landed as **[24](24-security-center-and-health-check.md)**, renumbered from 22.

**Seed harvest** · *four pages read, all four substantive — the richest harvest of the build so far*

- **15** — `UserRecordAccess Query Problem` (**2025**). → *harvested, and it is **not** a duplicate of the phase-04 harvest in [02-apex · 11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md). That one covered the SOQL constraints; this page is about a **Flow Get Records** element, where **Store All Fields fails** because Flow retrieves unsupported fields such as `Id` (Salesforce KB `000383422`), and where "no access" is the **zero-row** case that needs* When no records are returned, set specified variables to null *or it errors instead of answering.*
- **06, 08, 10, 14** — `Salesforce Certified Sharing and Visibility Architect` (**2025**), which the inventory listed only as "may indicate weak areas". → *it is a 14-question scenario bank and four questions were worth harvesting: the **implicit-sharing** trap in its concrete form (Private Account OWD + Opportunity edit = **read-only** on the parent) → **06**; **granular locking as the tool for large-scale role-hierarchy realignment** and **three roles created with the first partner-account external user** → **08**; the **opportunity-team-plus-Apex** shape for a per-record helper grant → **10**; and one question whose **marked answer is now wrong** — `isUpdateable()` per field to fix an FLS bypass, when a 67.0 class enforces FLS by default and the `WITH SECURITY_ENFORCED` distractor no longer compiles → corrected inline in **14**.*
- **`Sharing and Visibility Architect` (2023)** → *read, thin as predicted: a Health Check screenshot and one line saying to group permission sets by job function. The Health Check half belongs to phase 11's Security Center note, **[24](24-security-center-and-health-check.md)** after renumbering; the permission-set line was already the substance of **04**. No callout.*
- **`Apex Managed Sharing` (2023)** → *inventory maps it to [02-apex · 11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md), written in phase 04. Re-read here for one line worth keeping: **sharing rules and manual sharing do not support high-volume community users**, who have no roles. That belongs to [05-experience-cloud · 09](../05-experience-cloud-lwr/09-sharing-for-external-users.md) — noted for phase 18 rather than harvested here.*

**Rule 1 exceeded deliberately, with approval** — three files added, and the correction sweep reached [../CURRENCY.md](../CURRENCY.md), [../PHASES.md](../PHASES.md), [../README.md](../README.md), [08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md) and [05-experience-cloud · INDEX + PHASES](../05-experience-cloud-lwr/INDEX.md), because the cancelled retirement made a published sentence wrong and the renumber moved three inbound links. Same call phases 08 and 09 made, for the same reason.

---

## Phase 11 — Identity, encryption & monitoring · 11 files ✅

```
16-sharing-recalculation-and-performance.md          🆕⚠️  (was 13; flags added at plan time)
17-authentication-and-mfa.md                         ⚠️    ← SPLIT from the planned 17
18-session-security-login-policies-and-step-up.md    🆕    ← ADDED at plan time (split half)
19-sso-saml-oidc-and-identity.md                     🆕    (was 15)
20-my-domain-enhanced-domains-and-trusted-urls.md    ⚠️    (was 16)
21-shield-platform-encryption.md                           (was 17)
22-field-audit-trail-and-data-retention.md                 ← ADDED at plan time
23-event-monitoring-and-transaction-security.md      🆕⚠️  (was 18, flags added)
24-security-center-and-health-check.md               🆕⚠️  (was 19, flags added)
25-privacy-consent-and-data-protection.md                  (was 20)
26-secure-coding-checklist.md                        ⚠️    (was 21)
```

**Two files added before the run**, and this time the numbering was *appended and shifted*, never inserted below 16 — because 15 files now exist in the area and phase 10's retro was explicit that a second renumber must be justified. The grep it demanded was repeated: **one** inbound line outside the area names an area-07 topic by number ([08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md), pointing at 16, unaffected), and **six** placeholder `[NN](INDEX.md)` forward links inside the area needed resolving anyway. Total renumber cost: one label.

- **18** — the planned 17 would have carried MFA, phishing-resistance, the method inventory, session levels, high assurance, the step-up period, login IP ranges and login flows inside an 80-line cap. The 2026 wave made the second half a topic: step-up has its own setting, its own exemption rule and its own auto-created policy.
- **22** — [01-admin · 17](../01-admin-and-declarative-platform/17-setup-audit-trail-monitoring-and-usage.md) forward-links here for *"Event Monitoring, Field Audit Trail and the paid tier of this story"*, and the 9-file plan answered two thirds of it. Field Audit Trail is Shield's second pillar and nothing in the vault owned it.

### Retro

**⚠️ — for the second phase running, the plan's headline correction was itself out of date**

- **17 — MFA is enforced, not contractual.** The plan said *"MFA is contractually required, not a recommendation"*, which was the correct 2022–2025 framing. In **June–July 2026** it became a technical control, and a second requirement landed on top: **phishing-resistant MFA (WebAuthn/FIDO2 only) for the System Administrator profile and anyone with `Modify All Data`, `View All Data`, `Customize Application` or `Author Apex`.** Salesforce Authenticator, TOTP, SMS and email codes **stopped qualifying for those users**. Sandboxes from 22 June, production from 1 July, wave-rolled. Writing the planned correction would have published a stale one — the same failure phase 10 hit one phase earlier, when its own headline ⚠️ still asserted a profile-permissions retirement that had been **cancelled**.
- **16 carried no flag and needed two.** *Asynchronous Sharing Recalculation After Group Membership Changes* is a Release Update: **available Spring '26, enforced Spring '27**, with the underlying behaviour rolling out from Summer '25 and fully enabled April 2026. It breaks working code in two documented ways — a query or assertion expecting `RowCause = 'Rule'` share rows immediately, and **`System.runAs()` not reflecting new access**. A *Test asynchronous sharing recalculation in Apex tests* flag exists to force it in a sandbox. An unflagged topic with a code-breaking Release Update is a plan defect worth naming.

**🆕 the plan did not flag — a whole enforcement wave, concentrated in six weeks**

- **18 — step-up authentication is real and narrow.** Report exports **over 10,000 rows through the UI**, internal users only, production 13 July 2026. `Step-Up Authentication Period (Minutes)` is settable **1–120**. It is **skipped** where the profile has login IP restrictions and either the IP is unchanged since login or *Enforce login IP ranges on every request* is on — which turns an IP range into a UX lever, not just a control.
- **23 — Salesforce provisioned security config into customer orgs.** A default `ReportEvent` Transaction Security Policy was **auto-created**, but only in orgs with **Shield or Event Monitoring** and only where no `ReportEvent` policy existed; it is fully editable. Two orgs on the same release now behave differently on export and neither admin changed anything. Also new: **`Modify Transaction Security Policy`** is required alongside `Customize Application` to manage policies.
- **20 — the ⚠️ was understated.** The plan said enhanced domains "are enforced". Stronger: **legacy My Domain hostname redirections ended in production in Spring '26**, so old URLs **404 rather than forward** — the failure mode changed from invisible to total. The API half is still in flight: an opt-in *Block API traffic that uses an incorrect instanced URL* switch from **19 June 2026**, support ending **Winter '27**.
- **24 — Security Center Essentials went free in every org in July 2026.** Configuration metrics only — Health Check score and baselines, connected apps, packages, trusted and login IP ranges. **Who Sees What Explorer is not in it**: that lives in the Security Center *Extension Package*, for paid Security Center customers. Also **weekly Health Check notifications are on by default for new production orgs**.

**Other corrections made while writing**

- **The legacy Transaction Security framework is retired**, replaced by **Enhanced Transaction Security**, which arrives automatically with Real-Time Event Monitoring. Stated as the ⚠️ in **23** because the seed page names the feature without the qualifier.
- **Event Monitoring has a free tier worth knowing** — EE/UE/PE get roughly seven log types (Login, Logout, API Total Usage, Apex Unexpected Exception, CORS Violation, CSP Violation, **Hostname Redirects**) at **one day** retention. That last one is exactly the log needed to find integrations still on instanced URLs before Winter '27, and it costs nothing.
- **Phase 10's sentence in [15](15-auditing-and-troubleshooting-access.md) needed a nuance, not a correction.** "Who Sees What Explorer lives in Security Center, which is a paid add-on" is still true; Essentials being free could be misread as contradicting it, so the Essentials carve-out was added inline.
- **Deferred to phase 13, deliberately.** [../CURRENCY.md](../CURRENCY.md) lists *"Connected Apps for new integrations — superseded by External Client Apps"*. That **understates** it: creation was disabled by default for new orgs in Winter '26 and is **Support-gated org-wide since Spring '26**. Not wrong, so area 06 fixes it when it runs. Recorded here so it is not lost.

**Seed harvest** · *two pages read, one substantive — and one page found that the inventory does not list*

- **23** — `Transaction Security Policies` (**2025**). → *harvested. Its use-case list is sound and still current, and it carries a real project detail: **on the GallagherRe project a policy was used to prevent report exports**. That bespoke control became a platform default in July 2026 — with a changed posture, since Salesforce's version **challenges with step-up** rather than **blocks**. The page also says "Transaction Security Policies" unqualified; the framework it describes is the Enhanced one.*
- **24** — the Health Check half of `Sharing and Visibility Architect` (**2023**). → *read, and phase 10's assessment was exact: one sentence of definition plus a screenshot. **No callout.** The prediction that it was worth deferring rather than harvesting was wrong in the harmless direction — there was nothing to defer.*
- **Not in [INVENTORY.md](../_notion-seed/INVENTORY.md): `Security Levels` (2025-03).** A clean layer-by-layer summary of org/object/field/record security that maps to [01](01-security-model-layers-overview.md) and [13](13-field-level-security-and-visibility-layers.md) — **phase 10 files, already written**, so nothing to harvest here. Its one substantive gotcha (*lookup and formula fields cannot be used in sharing rules*) is still correct. Worth adding to the inventory when area 07's seed list is next touched.

**Rule 1 exceeded deliberately, with approval** — two files added, and the sweep reached [../CURRENCY.md](../CURRENCY.md), [../PHASES.md](../PHASES.md), [../README.md](../README.md), [08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md), [AI_Data/GLOSSARY.md](../../AI_Data/GLOSSARY.md) and six phase-10 files whose forward links pointed at `INDEX.md`. Fourth phase running to make the same call.
