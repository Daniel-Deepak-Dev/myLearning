# Queues, Assignment & Escalation Rules

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 01

**Scope:** Declarative record routing — queues as pseudo-owners, assignment rules on create, and time-based escalation. Sharing consequences of ownership are [07-security](../07-security-and-sharing/INDEX.md).

## Core idea

A **queue** is an owner that is not a person: assign a record to it and every queue member can see and claim the record. **Assignment rules** are the declarative router that decides which user or queue a new record lands on, evaluated as an ordered list where the **first matching entry wins and evaluation stops**. **Escalation rules** add the time dimension for Cases — if a case has not moved within a business-hours-aware window, reassign or notify. All three fire late in the save order, after triggers have already run, which is the source of most surprises about them.

## How it works

- **Queue membership** can be users, roles, public groups, territories or partner users. A record owned by a queue is visible to all members regardless of the role hierarchy, because a queue has no place in that hierarchy.
- **Accepting** a queue record transfers ownership to the accepting user, removing it from the shared pool.
- Queues are supported on `Case`, `Lead`, `Task`, `Order`, Knowledge articles, Service Contracts and **custom objects**.
- **One active assignment rule per object.** A rule holds ordered rule entries; activating a second rule deactivates the first, which makes deployment order significant.
- **The API does not run assignment rules by default.** A write must supply `AssignmentRuleHeader` — Data Loader exposes this as a setting. Without it the record keeps the creating user as owner.
- **Save-order positions:** assignment rules at step 9, auto-response rules at step 10, escalation rules at step 12 — all *after* after-triggers at step 8. See [14 · Order of execution](14-order-of-execution-declarative-view.md).
- **Escalation is Case-only** and evaluates against **business hours**, so the clock stops outside them.

## 2026 currency

Queue-plus-assignment-rule remains correct for record routing, but it is no longer the answer for real-time work distribution in Service Cloud — **Omni-Channel** owns that, with capacity-based routing and presence. Treat assignment rules as the mechanism for *ownership on create* and Omni-Channel as the mechanism for *who works it now*.

## Gotchas

- **First match wins.** Without a catch-all final entry, non-matching records silently keep the creator as owner.
- Assignment rules run after after-triggers, so a trigger can never see the final owner. Logic that depends on the routed owner belongs in a later automation.
- A queue has no role, so **role-hierarchy sharing does not grant access upward** from a queue-owned record — managers do not automatically see it.
- Reassignment by an assignment rule does not re-trigger assignment rules, but it does re-run the save path for field updates, which can look like recursion in debug logs.
- Escalation timing without configured **business hours** falls back to a default that is rarely what the business meant.
- Changing owner re-evaluates sharing for that record and its children — cheap for one record, expensive in a bulk load. See [08-data](../08-data-modeling-and-large-data-volumes/INDEX.md).
- Queue email notifications plus "send email to members" can flood a large queue on a bulk insert.
- Deploying an assignment rule is an activation event: two deployments each carrying an "active" rule leave whichever landed last as the only active one.

## Recall

Q: How are assignment rule entries evaluated?
A: In order, first match wins, and evaluation stops there — so a catch-all last entry is needed to avoid records keeping the creator as owner.

Q: How many assignment rules can be active on an object at once?
A: Exactly one. Activating another deactivates the current one.

Q: Why does a record loaded via Data Loader keep the loading user as owner despite an active assignment rule?
A: API writes do not run assignment rules unless `AssignmentRuleHeader` is supplied — in Data Loader that is a setting you must enable.

Q: Why can a manager not see a queue-owned record through the role hierarchy?
A: A queue is not a person and holds no position in the role hierarchy, so there is nothing for the hierarchy to roll up from.

Q: Where do assignment, auto-response and escalation rules sit relative to after-triggers?
A: All after them — steps 9, 10 and 12 respectively, against after-triggers at step 8.

## Related

- [14 · Order of execution](14-order-of-execution-declarative-view.md) — the authoritative positions for all three rule types
- [07-security · INDEX](../07-security-and-sharing/INDEX.md) — what queue ownership means for sharing
- [04-flow · INDEX](../04-flow-and-automation/INDEX.md) — when routing logic outgrows an assignment rule
