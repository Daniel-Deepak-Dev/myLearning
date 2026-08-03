# User Access Policies & Lifecycle

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** Automating grant and revoke across the joiner–mover–leaver lifecycle, declaratively. What can be assigned is [02](02-licences-and-what-they-gate.md)–[04](04-permission-set-groups-and-muting.md); who a grant reaches once assigned is [08](08-groups-queues-and-the-grantee-model.md).

## Core idea

Access design fails in operation, not in design. The model is usually right on the day it is built and wrong six months later, because people join, change teams and leave, and every one of those events is a manual checklist somebody skipped. **User Access Policies** are the declarative answer: criteria over User fields, and a set of grants and revocations applied automatically when a user record is created or updated to match. It is the same shape as an assignment rule, applied to permissions instead of records — and it is the mechanism that makes a permission-set-led design survive contact with HR, which is the part of that design most write-ups skip.

## How it works

- **Criteria are User-record filters** — role, department, title, profile, a custom field fed from HR. Entitlement-based criteria (what the user currently holds) work too.
- **A policy can assign or remove**: permission sets, permission set groups, **permission set licences**, managed package licences, **public group** memberships and **queue** memberships.
- **Two modes.** *Automate Policy* runs it on user create and/or user update; the manual one-time application applies it to everyone matching right now and lets you pick who.
- **Status is `Design` → `Active`.** A policy in Design does nothing; activation is the switch.
- **Order decides conflicts.** When several policies match at once, the one with the **lowest `Order` value** wins. Add `Order` to your policy list view — it is not shown by default.
- **200 active policies per org**, in **Enterprise and Unlimited editions**. Complex or numerous filters increase application time, so the limit is not the real ceiling.
- **`Manage User Access Policies`** is the permission required to build them; *Recent User Access Changes* is where results and failures are reported.

## 2026 currency

The 🆕 flag here is about absence from older material, not recency — **User Access Policies have been GA since Summer '24** and almost nothing written before then mentions them, so the 2019–2021 answer to lifecycle management (a Flow that assigns a permission set, or a spreadsheet) is what most people still carry. Two things make them matter more in 2026 than in 2024: the **profile-permissions retirement being cancelled** ([03](03-profiles-and-the-permission-set-led-model.md)) means orgs will run mixed profile-and-permission-set models for years, and mixed models drift fastest; and policies can assign **permission set licences**, which is the assignment most commonly out of step with its permission set ([02](02-licences-and-what-they-gate.md)).

## Gotchas

- **Policies are not retroactive.** Activating one does nothing to users who already match — it applies only when a user record is *created or updated* into matching. Use the manual one-time application to catch the existing population.
- **A policy cannot trigger another policy.** No chaining, so a grant that changes a User field will not cascade into a second policy.
- **Group and queue membership is managed only for directly-added users.** Members who inherit through a role, territory or nested group are outside the policy's reach. → [08](08-groups-queues-and-the-grantee-model.md)
- **Insufficient licences fail quietly.** The shortfall is logged in *Recent User Access Changes*, not raised as an error, so the user is simply short an assignment.
- **Licence counts on Company Information can lag a revocation**, which makes "we freed up seats" hard to verify immediately.
- **Recent User Access Changes only shows changes still in effect.** A change later overridden disappears from the log, so it is not an audit trail.
- **Enterprise and Unlimited only.** A Professional-edition org has no declarative lifecycle mechanism and falls back to Flow or an external IdP.

## Recall

Q: When does an active User Access Policy apply to a user?
A: When the user record is created, or updated so that it matches the criteria. It is never retroactive to users who already match.

Q: What can a policy assign beyond permission sets and groups?
A: Permission set licences, managed package licences, public group memberships and queue memberships.

Q: How are conflicts between simultaneously matching policies resolved?
A: The policy with the lowest `Order` value is applied. `Order` is not on the default list view — add it.

Q: What is the active-policy limit and which editions have the feature?
A: 200 active policies per org, in Enterprise and Unlimited editions.

Q: Why is *Recent User Access Changes* not an audit trail?
A: It shows only changes still in effect — anything later overridden disappears from it.

## Related

- [04 · Permission Set Groups & muting](04-permission-set-groups-and-muting.md) — the persona bundles a policy is usually assigning
- [02 · Licences & what they gate](02-licences-and-what-they-gate.md) — why a policy's assignment can silently fall short
- [08 · Groups, queues & the grantee model](08-groups-queues-and-the-grantee-model.md) — why a policy only sees directly-added members
- [01-admin · 17 Setup Audit Trail & monitoring](../01-admin-and-declarative-platform/17-setup-audit-trail-monitoring-and-usage.md) — the durable record this feature's log is not
