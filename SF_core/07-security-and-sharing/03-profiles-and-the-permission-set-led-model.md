# Profiles & the Permission-Set-Led Model

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** How object, field and user permissions are actually assigned, and the state of the profile-to-permission-set migration. Grouping and muting are [04](04-permission-set-groups-and-muting.md); automating assignment is [05](05-user-access-policies-and-lifecycle.md).

> **What changed.** *"Permissions are being retired from profiles in Spring '26"* was true when announced and is **wrong now.** Salesforce **cancelled the retirement on 6 June 2026** — Help article **003834041**, *"This enforcement has now been cancelled"*, citing customer feedback and remaining feature gaps. Profiles keep their permissions, **no end-of-life date exists**, and permission-set-led design is a recommendation rather than a deadline.

## Core idea

Every user has exactly one profile and any number of permission sets, and their effective access is the **union** of all of them. There is no deny: you cannot use a permission set to take something away that the profile grants, which is the single fact that drives the whole design debate. A profile-heavy org ends up with dozens of near-identical profiles that differ by two checkboxes, because the only way to vary access is to fork the profile. A permission-set-led org keeps one minimal profile — usually **Minimum Access - Salesforce** — and composes access from reusable grants. That is still the right answer in 2026. What changed is *why*: it is now a maintainability argument you make on merit, not a migration you are being forced through.

## How it works

- **A profile is mandatory and singular.** Permission sets are optional and additive. Both can grant object permissions, field-level security, user permissions, tabs, record types, apps, Apex class and Visualforce page access, and custom permissions.
- **Some settings only ever lived on the profile** and were never part of the migration proposal: **login hours, login IP ranges, the default record type per object, the default app, and page layout assignments**. Even a fully permission-set-led org still designs profiles for these.
- **`Minimum Access - Salesforce`** is the intended baseline profile — it grants little more than login. Newer orgs ship with it; older orgs usually still hand out `Standard User`, which is why an inherited org's audit starts here.
- **Permission sets are additive only.** The only subtractive tool in the permission layer is a **muting permission set inside a permission set group** → [04](04-permission-set-groups-and-muting.md).
- **`Modify All Data` is administrator by another name.** Treat it, `View All Data`, `Manage Users` and `Customize Application` as the four that turn an access review into an escalation review.

## 2026 currency

**The retirement is cancelled** (above) — the practical effect is that a migration you paused is no longer urgent, and one you completed was still worth doing. Salesforce's stated recommendation is unchanged: **profiles for baseline settings, permission sets for access**, under least privilege.

Two Summer '26 changes are live and do matter:

- **`Enable Profile Filtering` is a Release Update** — available Summer '26, **enforced Winter '27**. After enforcement a user sees only their own profile name unless granted **`View All Profiles`**. Anything that depends on users picking or reporting on profiles — support tooling, licence management, list view filters — needs that permission assigned first.
- **The enhanced profile view now previews indirect changes.** Editing a user, object or app permission shows the dependent permissions it will drag along, for approval **before** saving. The cascade always existed; it was just invisible.

## Gotchas

- **You cannot revoke with a permission set.** If a user has too much access, the grant is in the profile or another permission set — find it, do not try to counter it. → [15](15-auditing-and-troubleshooting-access.md)
- **"Retired" and "not recommended" are different words.** Six earlier features in this vault were called retired when they were not; profiles are the seventh. Saying it in a scoping call costs the room. → [../CURRENCY.md](../CURRENCY.md)
- **Cloning a profile to change two checkboxes** is how orgs reach 60 profiles. The clone inherits every drift the original had.
- **Record type *availability* is a profile or permission set grant; the *default* record type is profile-only.** Migrating availability to permission sets does not migrate the default. → [01-admin · 04](../01-admin-and-declarative-platform/04-record-types-and-picklist-architecture.md)
- **Permission set assignments can carry an expiry date.** Unused, they become the permanent grants that fail the next access review.
- **`View All Profiles` is not assigned by default**, and Winter '27 enforcement turns that from harmless into a broken report.
- **A profile change is an org-wide change.** There is no per-user override, which is exactly the coupling permission sets exist to break.

## Recall

Q: What is the current status of retiring permissions from profiles?
A: Cancelled on 6 June 2026 (Help 003834041). Profiles keep their permissions and no end-of-life date has been announced.

Q: Can a permission set remove access a profile grants?
A: No. Permission sets are purely additive; only a muting permission set inside a permission set group subtracts.

Q: Which settings stay on the profile even in a fully permission-set-led design?
A: Login hours, login IP ranges, the default record type per object, the default app, and page layout assignments.

Q: What does the `Enable Profile Filtering` Release Update do, and when is it enforced?
A: From Winter '27 a user sees only their own profile name unless granted `View All Profiles`. It is available to enable from Summer '26.

Q: Which profile is the intended baseline in a least-privilege design?
A: `Minimum Access - Salesforce` — it grants little beyond login, with everything else composed from permission sets.

## Related

- [04 · Permission Set Groups & muting](04-permission-set-groups-and-muting.md) — how to compose grants without a permission set per person
- [05 · User Access Policies & lifecycle](05-user-access-policies-and-lifecycle.md) — assigning all of this automatically as people join, move and leave
- [15 · Auditing & troubleshooting access](15-auditing-and-troubleshooting-access.md) — finding which profile or permission set granted a permission
- [02 · Licences & what they gate](02-licences-and-what-they-gate.md) — why a permission is sometimes not merely unchecked but absent
