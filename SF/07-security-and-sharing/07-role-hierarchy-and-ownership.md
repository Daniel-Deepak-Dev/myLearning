# Role Hierarchy & Ownership

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** Ownership as the primary record grant, and the hierarchy that propagates it upward. Groups and queues as grantees are [08](08-groups-queues-and-the-grantee-model.md); the performance consequences of concentrated ownership are [16](16-sharing-recalculation-and-performance.md).

## Core idea

Ownership is the strongest record grant there is: the owner gets full access regardless of sharing, and the **role hierarchy** hands that same access to everyone above them. The distinction worth holding is that a role is **not** a job title and not a permission container — it exists almost entirely to answer *whose records roll up to whom*, for both sharing and forecasting. That is why role hierarchies that mirror the org chart are usually wrong: two managers at the same level who must not see each other's pipeline need to be siblings, and a VP who genuinely should not see everything below them needs the hierarchy to stop, not the org chart. Ownership is also where record access becomes a **performance** problem, because access is derived from ownership and a million records owned by one user is a million rows the platform has to reason about.

## How it works

- **The hierarchy grants upward only.** A manager sees their subordinates' records; peers see nothing of each other; subordinates see nothing of their manager.
- **`Grant Access Using Hierarchies` is per object.** Forced on for standard objects, optional for custom ones — turning it off is the only declarative way to stop upward inheritance. → [06](06-org-wide-defaults-and-record-access.md)
- **Roles do not grant permissions.** No object, field or user permission lives on a role. A user can have no role at all and still work — they simply sit outside the hierarchy.
- **A user with no role is invisible to every hierarchy-based grant**, including "Roles and Subordinates" sharing rules. This is a real gap in orgs that assign roles casually.
- **Ownership change cascades.** Reassigning an account can reassign its children, recalculates sharing for every affected record, and **deletes manual shares** on the way through. → [09](09-sharing-rules-and-manual-sharing.md)
- **Territory hierarchy is a separate, parallel hierarchy** with its own upward grant. An org can run both. → [10](10-teams-territories-and-account-sharing.md)
- **Skew is the failure mode.** *Ownership skew* — one user owning a very large share of an object — makes every recalculation and every reparent expensive.

## 2026 currency

Nothing changed in the role hierarchy itself. What changed sits one step away and is easy to miss: **Summer '26 gave queues their own `Grant Access Using Hierarchies` setting**, defaulting **on for existing queues and off for new ones**. Queue-owned records are ownership-based grants like any other, so this is the first time in years that the upward inheritance rule has an exception you can configure — and the exception is now the default for anything you create. → [08](08-groups-queues-and-the-grantee-model.md)

## Gotchas

- **A role is not a permission container.** Nobody gets an object permission from a role; if access is missing, the role is almost never the answer. → [03](03-profiles-and-the-permission-set-led-model.md)
- **Users with no role fall out of hierarchy-based sharing entirely**, including "Roles and Subordinates" grants that look like they should include them.
- **Ownership skew is a sharing problem before it is a query problem.** The classic shape is an integration user owning every imported record. → [08-data · 08](../08-data-modeling-and-large-data-volumes/INDEX.md)
- **Changing a user's role triggers a sharing recalculation** for every record they own and everything the hierarchy derives — do it in bulk, off-hours.
- **Reassigning an owner deletes manual shares** on the record. Grants that must survive need an Apex sharing reason. → [02-apex · 11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md)
- **You cannot stop upward inheritance on a standard object.** No setting exists; the answer is a different object or a restriction rule. → [11](11-restriction-rules.md)
- **Deleting a role reparents its children silently**, quietly widening or narrowing access for everyone underneath.

## Recall

Q: What access does the role hierarchy grant, and in which direction?
A: Everyone above a record's owner gets the owner's access. Upward only — peers and subordinates get nothing.

Q: Do roles grant object or field permissions?
A: No. Roles exist for record roll-up — sharing and forecasting. Permissions come from the profile and permission sets.

Q: What happens to a user with no role assigned?
A: They work normally but sit outside the hierarchy, so no hierarchy-based sharing reaches them and no manager inherits their records.

Q: Which objects allow `Grant Access Using Hierarchies` to be switched off?
A: Custom objects only. It is forced on for standard objects.

Q: Why is ownership skew a security-area problem rather than a data-area one?
A: Because record access is derived from ownership, so concentrated ownership makes every sharing recalculation and reparent expensive.

## Related

- [06 · Org-wide defaults & record access](06-org-wide-defaults-and-record-access.md) — the baseline this hierarchy raises
- [08 · Groups, queues & the grantee model](08-groups-queues-and-the-grantee-model.md) — queue ownership and the Summer '26 hierarchy exception
- [10 · Teams, territories & account sharing](10-teams-territories-and-account-sharing.md) — the parallel hierarchy
- [08-data · 08 Data skew](../08-data-modeling-and-large-data-volumes/INDEX.md) — the volume side of ownership concentration
