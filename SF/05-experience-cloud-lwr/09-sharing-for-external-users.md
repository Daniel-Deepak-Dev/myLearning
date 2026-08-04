# Sharing for External Users

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

**Scope:** Granting record access to authenticated external users — sharing sets, share groups, super user access, and why the internal mechanisms don't reach them. Guests are [07](07-guest-user-security-model.md); the licence that decides which of these you get is [08](08-licences-and-external-user-types.md).

## Core idea

> **From my notes, carried forward from phase 10.** *Sharing rules and manual sharing do not support high-volume community users.* Still true at 67.0, and it is the whole reason this note exists.

High-volume external users — Customer Community — have **no role**. Every internal grant mechanism in [07-security](../07-security-and-sharing/INDEX.md) is built on roles, groups or ownership, and none of them can name a user who has no place in the hierarchy. So Salesforce built a parallel mechanism: **a sharing set grants access by *relationship* rather than by group membership** — the record's Account or Contact matches the one on the user's own record, therefore the user sees it.

That is the mental shift. Internally you ask *who is this user and what group are they in*. Externally, for high-volume users, you ask *what record is this user attached to, and what hangs off it*.

## How it works

- **A sharing set maps a lookup on the target object to the user's Contact or Account**, directly or through an indirect lookup, and grants Read Only or Read/Write. Configured under **Setup → Digital Experiences → Settings**.
- **A share group is the return path.** Records *owned by* high-volume users are invisible to internal staff by default; a share group — created inside a sharing set — grants named internal and external users access to them. Without it, a case a portal user filed is a case nobody in support can see.
- **Role-based external users use the ordinary mechanisms**: OWD, role hierarchy, sharing rules, manual sharing, teams. Their roles sit *under* the account's owner in the hierarchy.
- **Super user access widens a role-based external user sideways** — records created by others on their account, at or below their role, for Cases, Leads, Opportunities and custom objects. Granted by permission set for Customer Plus.
- **The external OWD is the floor for all of this** and cannot be more permissive than the internal one → [07-security · 06](../07-security-and-sharing/06-org-wide-defaults-and-record-access.md).
- **"Roles and Subordinates" includes portal and community roles.** Use the *Internal* variant unless you intend external users to inherit → [07-security · 08](../07-security-and-sharing/08-groups-queues-and-the-grantee-model.md).

## 2026 currency

Two platform changes reach external sharing without being about it. **Asynchronous sharing recalculation** is a Release Update available now and enforced Spring '27: after enforcement, share rows are not guaranteed to exist immediately after a write, so a portal test that asserts access straight after creating a record becomes flaky rather than wrong → [07-security · 16](../07-security-and-sharing/16-sharing-recalculation-and-performance.md). And **restriction rules subtract**, which means "the union of everything that grants access" now needs exceptions attached before you use it to explain a portal user's visibility → [07-security · 11](../07-security-and-sharing/11-restriction-rules.md).

## Gotchas

- **Sharing sets are for high-volume licences.** Pointing one at a role-based user is a design smell — they already have sharing rules.
- **Forgetting the share group is the classic portal defect.** Everything works for the customer and nothing is visible to support.
- **A sharing set follows a lookup, so a null lookup grants nothing** — records created without the Account or Contact populated silently disappear from the portal.
- **Ownership skew arrives fast in portals**, because a handful of accounts carry most of the records → [08-data · 10](../08-data-modeling-and-large-data-volumes/10-data-skew.md).
- **Super user access is per-user, not per-role**, and is routinely granted once and never reviewed → [07-security · 15](../07-security-and-sharing/15-auditing-and-troubleshooting-access.md).
- **Portal roles count against the org's role limit**, three per partner account → [08](08-licences-and-external-user-types.md).

## Recall

Q: Why can't sharing rules grant access to a Customer Community user?
A: High-volume users have no role. Sharing rules grant to groups, roles and territories, none of which can name a role-less user.

Q: What does a sharing set actually match on?
A: A lookup on the target object resolving to the user's own Contact or Account — access by relationship, not by group membership.

Q: What problem does a share group solve?
A: Records owned by high-volume external users are invisible to internal staff; a share group grants named users access to them.

Q: Which external users use the ordinary sharing mechanisms?
A: Role-based ones — Customer Community Plus, Partner Community and External Apps — whose roles sit under the account owner in the hierarchy.

Q: What breaks about "Roles and Subordinates" in an org with a portal?
A: It includes portal and community roles. Use the *Internal* variant unless external inheritance is intended.

## Related

- [08 · Licences & external user types](08-licences-and-external-user-types.md) — the licence that decides which mechanism applies
- [07 · Guest user security model](07-guest-user-security-model.md) — the unauthenticated case, which uses none of this
- [07-security · 09 Sharing rules & manual sharing](../07-security-and-sharing/09-sharing-rules-and-manual-sharing.md) — the internal mechanisms and why they stop at the portal boundary
- [07-security · 15 Auditing & troubleshooting access](../07-security-and-sharing/15-auditing-and-troubleshooting-access.md) — how to answer "why can this portal user see this record"
