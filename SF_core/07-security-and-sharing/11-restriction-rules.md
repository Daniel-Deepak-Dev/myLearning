# Restriction Rules

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** The one mechanism that reduces record access. What grants it is [06](06-org-wide-defaults-and-record-access.md)–[10](10-teams-territories-and-account-sharing.md); changing the *default view* without changing access is [12](12-scoping-rules.md).

> **What changed.** *"A user's record access is the union of everything that grants it"* — the answer taught for a decade — became incomplete at **Winter '22**. **Restriction rules subtract.** They run after everything else and filter the result down, so sharing is no longer additive-only and reading every grant no longer tells you what a user can see.

## Core idea

Every other tool in this area answers *what should this user be able to see?* by adding to a pile. Restriction rules answer the opposite question — *of everything they can see, what should they not?* — and they answer it by filtering, per object, per user population, on record field values. That inversion is the whole point and it is why they exist: some access requirements are only expressible as an exclusion. "Support agents see all cases except those flagged HR-sensitive" cannot be built out of grants without rebuilding the entire access model around one field. The cost of that power is that a restriction rule is invisible from the grant side: nothing in the sharing rules, the hierarchy or the share table hints that a filter is removing rows afterwards.

## How it works

- **A rule names three things**: the object, a **user criteria** (which users the rule applies to), and a **record criteria** (which records those users retain access to). Everything outside the record criteria is removed for them.
- **It filters the result of sharing, not the sharing itself.** Share rows still exist; the user simply does not get the records back.
- **It applies broadly** — list views, reports, SOQL, **SOSL, search, lookups and related lists**. That breadth is the difference from scoping rules. → [12](12-scoping-rules.md)
- **Supported objects are a fixed list**, not everything: **custom objects, external objects, Contract, Event, Quote, Task, Time Sheet and Time Sheet Entry**. The core CRM objects are not on it.
- **Limits are per object and per edition**: **2 active rules per object** in Enterprise and Developer editions, **5** in Performance and Unlimited.
- **One rule per object per user.** A user should be matched by at most one restriction rule on a given object; overlapping user criteria are a design error, not a merge.
- **Built and deployed as metadata** (`RestrictionRule`), and manageable through the Tooling API — so they belong in source control alongside everything else. → [09-devops](../09-devops-sfdx-and-release-management/INDEX.md)

## 2026 currency

Restriction rules went GA in **Winter '22** and are still absent from most published access-model explanations, which is what makes them worth flagging four years on: the material people learn from predates them. Nothing changed in Summer '26, but they now sit in a pattern — **muting** subtracts inside a permission set group ([04](04-permission-set-groups-and-muting.md)), **queues** stopped granting up the hierarchy by default ([08](08-groups-queues-and-the-grantee-model.md)), and restriction rules subtract from record access. The platform is steadily adding narrowing controls to a model that began as pure union, and the summary sentence needs all three exceptions attached.

## Gotchas

- **Admins are not exempt.** A restriction rule applies to users matching its criteria regardless of `View All Data` — which is a feature, and also the first thing that confuses an admin debugging it.
- **The core CRM objects are unsupported.** Account, Contact, Opportunity, Lead and Case are not on the list, so the commonest ask cannot be built this way.
- **Nothing on the grant side reveals a restriction.** Share rows still exist and a sharing audit will report access the user does not have. → [15](15-auditing-and-troubleshooting-access.md)
- **Two active rules per object in Enterprise edition** is a low ceiling, and it is per object, not per rule set.
- **Overlapping user criteria are undefined design**, not a documented merge. Keep one rule per object per user population.
- **Code is not exempt either** — user-mode SOQL respects restriction rules, so a 67.0 Apex class returns the filtered set and a `without sharing`/system-mode query does not. → [14](14-code-execution-context-and-security.md)
- **Report and list-view results shrink without explanation.** There is no "some records were hidden" indicator anywhere in the UI.

## Recall

Q: What makes restriction rules architecturally different from every other sharing mechanism?
A: They subtract. Everything else grants, so record access stopped being the union of everything that grants it.

Q: Which objects support restriction rules?
A: Custom objects, external objects, Contract, Event, Quote, Task, Time Sheet and Time Sheet Entry. Not the core CRM objects.

Q: How many active restriction rules can one object have?
A: Two in Enterprise and Developer editions, five in Performance and Unlimited.

Q: Does `View All Data` bypass a restriction rule?
A: No. If the user matches the rule's user criteria, the filter applies to them.

Q: Where does a restriction rule apply, compared with a scoping rule?
A: Restriction rules apply to list views, reports, SOQL, SOSL, search, lookups and related lists. Scoping rules reach only list views, reports and SOQL.

## Related

- [12 · Scoping rules](12-scoping-rules.md) — the sibling feature that changes the default view without changing access
- [09 · Sharing rules & manual sharing](09-sharing-rules-and-manual-sharing.md) — the grants this filters afterwards
- [14 · Code execution context & security](14-code-execution-context-and-security.md) — why user-mode Apex sees the filtered set and system mode does not
- [15 · Auditing & troubleshooting access](15-auditing-and-troubleshooting-access.md) — the only reliable way to see a restriction's effect
