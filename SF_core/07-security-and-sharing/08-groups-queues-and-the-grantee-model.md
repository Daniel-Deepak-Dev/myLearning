# Groups, Queues & the Grantee Model

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** *Who* a record grant is made to. Every sharing mechanism in this area grants to one of these, so this note is the vocabulary for [09](09-sharing-rules-and-manual-sharing.md) and [10](10-teams-territories-and-account-sharing.md). Queue routing and assignment rules are [01-admin · 11](../01-admin-and-declarative-platform/11-queues-assignment-and-escalation-rules.md).

> **What changed.** *"Records owned by a queue are visible to everyone above the queue members in the role hierarchy"* is no longer universally true. **Summer '26 gave queues their own `Grant Access Using Hierarchies` setting**, and the default depends on when the queue was made: **on for queues that already existed, off for queues created from Summer '26 onward.** A design that relied on managers seeing the queue's backlog breaks silently on new queues.

## Core idea

Sharing rules, manual shares, teams and Apex managed sharing all do the same thing — write a row that says *this record is shared with this grantee at this level for this reason*. The grantee is almost never a single user. It is a **group**, and the platform models nearly everything as one: a public group is a group, a role is a group, a role-plus-subordinates is a different group, a territory is a group, and **a queue is a group too** (`Group.Type = 'Queue'`). Understanding that one object underlies all of them explains several otherwise arbitrary behaviours — why group membership changes are slow, why they lock, and why "share with the sales team" has five subtly different meanings.

## How it works

| Grantee | What it resolves to | Note |
|---|---|---|
| **Public group** | an explicit list — users, roles, other groups, territories | the reusable one; nest freely |
| **Role** | users assigned that role only | not the people under it |
| **Role and Subordinates** | that role plus everything beneath it | includes portal roles |
| **Role and Internal Subordinates** | as above, **excluding** portal and community roles | usually the one you meant |
| **Queue** | the queue's members, and the queue can also *own* records | `Group.Type = 'Queue'` |
| **Manager groups** | a user's management chain, or a manager's whole subtree | grants without touching the role hierarchy |
| **Territory / Territory and Subordinates** | territory model membership | → [10](10-teams-territories-and-account-sharing.md) |

- **A queue is the only grantee that can be a record *owner*.** `OwnerId` on a case or lead can point at a queue, and members take ownership by accepting.
- **Public groups nest.** A group can contain other groups, roles and territories, which is what makes them the right unit to grant to — you change membership in one place instead of editing every rule.
- **Group membership is stored in `Group` and `GroupMember`** and is queryable, which is how you audit "who is actually in this" rather than trusting the UI. → [15](15-auditing-and-troubleshooting-access.md)
- **Membership changes take a lock on the group maintenance tables.** Bulk user loads that touch roles or group membership concurrently produce `UNABLE_TO_LOCK_ROW`; **granular locking** narrows the lock so unrelated parts of the hierarchy can proceed in parallel.
- **`Grant access using hierarchies by default in new queues`** on the Sharing Settings page controls the org-wide default for *new* queues only. Existing queues keep their setting, and each queue can override it.
- **Report and dashboard folders share to these grantees too** — users, roles, roles-and-subordinates and public groups — but **not to queues**, which is the one grantee type folder sharing does not accept.

> **From my notes.** Two facts from my 2025 prep that only ever appear as exam answers and are genuinely useful. **Granular locking is the tool Salesforce enables for large-scale role-hierarchy realignment** — it is not a general performance setting, it is specifically what makes a mass reparent survivable, and it is the right thing to ask for *before* the migration rather than after the first `UNABLE_TO_LOCK_ROW`. And **three roles are created by default when the first external user is created on a partner account**, which is why partner-heavy orgs approach the role limit from a direction nobody planned for. → [05-experience-cloud · 08](../05-experience-cloud-lwr/08-licences-and-external-user-types.md)

## 2026 currency

The queue hierarchy setting is the change (above), and it is worth reading as part of a pattern rather than an isolated feature: the platform keeps adding *narrowing* controls to a model that was originally additive-only. Restriction rules subtract ([11](11-restriction-rules.md)); muting subtracts inside a permission set group ([04](04-permission-set-groups-and-muting.md)); and now upward inheritance from a queue is opt-in rather than automatic. The old summary — *"sharing is the union of everything that grants access"* — needs three exceptions attached to it at 67.0.

## Gotchas

- **New queues do not grant up the hierarchy.** Created Summer '26 or later, `Grant Access Using Hierarchies` is off by default and the org-level switch does not retrofit existing queues.
- **"Role" and "Role and Subordinates" are different grantees.** Picking Role shares with the handful of people holding exactly that role — usually not what was meant.
- **"Role and Subordinates" includes portal and community roles.** Use the *Internal* variant unless you intend external users to inherit. → [05-experience-cloud · 09](../05-experience-cloud-lwr/09-sharing-for-external-users.md)
- **Bulk user updates deadlock on group maintenance.** Serialise role and group changes, or enable granular locking, before a large user migration.
- **User Access Policies manage only directly-added group and queue members** — anyone inheriting through a role, territory or nested group is out of reach. → [05](05-user-access-policies-and-lifecycle.md)
- **Removing someone from a public group silently revokes every grant made through it**, across every sharing rule that names it, with no warning at removal time.
- **A queue with no members still accepts ownership.** Records land somewhere nobody can see, and the symptom is a backlog that appears empty.

## Recall

Q: What is a queue, structurally?
A: A group — `Group.Type = 'Queue'`. It is also the only grantee that can own records.

Q: What changed about queues in Summer '26?
A: They gained a `Grant Access Using Hierarchies` setting. It is on for pre-existing queues and **off** by default for newly created ones.

Q: What is the difference between "Role and Subordinates" and "Role and Internal Subordinates"?
A: The internal variant excludes portal and community roles. The plain variant includes them.

Q: Why do bulk user loads fail with `UNABLE_TO_LOCK_ROW`?
A: Group membership changes lock the group maintenance tables. Granular locking narrows the lock so unrelated branches can proceed concurrently.

Q: Where can you read actual group membership rather than the UI's view?
A: The `Group` and `GroupMember` objects, both queryable via SOQL.

## Related

- [09 · Sharing rules & manual sharing](09-sharing-rules-and-manual-sharing.md) — the grants that name these grantees
- [07 · Role hierarchy & ownership](07-role-hierarchy-and-ownership.md) — the upward inheritance queues can now opt out of
- [01-admin · 11 Queues, assignment & escalation rules](../01-admin-and-declarative-platform/11-queues-assignment-and-escalation-rules.md) — the routing side of the same object
- [15 · Auditing & troubleshooting access](15-auditing-and-troubleshooting-access.md) — resolving a group to its real membership
