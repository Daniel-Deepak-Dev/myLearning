# Relationship Queries in Depth

> Area: 10-soql-and-sosl · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 22

**Scope:** Traversal in both directions, the naming rules that decide what you type, polymorphic lookups with `TYPEOF`, and junction objects. The data-model consequences of a relationship choice are [08-data · 02](../08-data-modeling-and-large-data-volumes/02-relationships-deep-dive.md).

## Core idea

Traversal is asymmetric, and the asymmetry is the single most consequential fact in SOQL. **Child-to-parent is dot notation and reaches five levels; parent-to-child is a subquery and reaches exactly one.** The reason is structural rather than arbitrary: going up, every step resolves to at most one record, so the planner knows the cost in advance. Going down, each step multiplies rows by an unknown factor, so the platform allows one level and makes you ask for it explicitly. Almost every "one query or two?" decision follows from this — and so does the commonest row-limit failure, because **a subquery's children are counted in the same 50,000-row budget as the parents**.

## How it works

- **Child-to-parent: dot notation, up to five levels.** `Contact.Account.Owner.Manager.Name`. Custom relationships take `__r`: `Opportunity.Custom_Deal__r.Owner.Email`.
- **Parent-to-child: a subquery, one level, using the plural relationship name.** At most **20** parent-to-child relationships per query.

```sql
SELECT Id, Name, Owner.Manager.Email,                    -- 3 levels up
       (SELECT Id, Amount FROM Opportunities             -- 1 level down, plural name
        WHERE StageName != 'Closed Lost' ORDER BY Amount DESC LIMIT 5)
FROM Account
WHERE Owner.Profile.Name = 'Sales Manager'               -- traversal works in WHERE too
```

- **The name you type is not the field name.** For a custom lookup `Deal__c`, the *field* is `Deal__c` and the *relationship* is `Deal__r`. Parent-to-child uses the **Child Relationship Name** from the field definition, which is separately editable and often plural.
- **`TYPEOF` resolves a polymorphic lookup in one query** — `Task.What`, `Event.Who`, `Owner`, which can point at several object types:

```sql
SELECT TYPEOF What WHEN Account THEN Industry WHEN Opportunity THEN Amount ELSE Name END
FROM Task
```

- **A junction object is queried from either side as an ordinary parent-to-child hop**, one level each way — so "which courses is this student on" and "which students are on this course" are both single queries, and "which students share a course with this student" is not.

## 2026 currency

Traversal syntax is unchanged, but **user mode makes traversal a permissions surface it never was**. At 67.0, reaching `Owner.Manager.Email` requires the running user to have read access to *every field along the path* and sharing access to the intermediate records — otherwise the query throws on the field, or silently returns null where a record is not visible. A five-level path is five chances to fail for a user who is not an administrator, and the failure mode differs by cause: **FLS raises an exception, sharing returns null**. That distinction is the fastest way to diagnose a traversal that "works for me". → [02-apex · 10](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)

## Gotchas

- **Child rows count against the 50,000-row limit.** A parent-to-child subquery over a large object fails the whole query rather than truncating → [01](01-query-anatomy-and-the-soql-model.md).
- **`__r` in the field list, `__c` in the filter** — mixing them up is the most common SOQL compile error, and the message names the wrong one first.
- **The child relationship name is editable and often not what you expect.** It is not derivable from the object name; check the field definition rather than guessing the plural.
- **Five levels is the ceiling for custom-object traversal specifically**; standard-object paths in some contexts allow fewer, and a `WHERE` clause on a deep path can be rejected where the same path in the `SELECT` list is accepted.
- **A subquery cannot itself contain a subquery.** One level down is one level, and no nesting recovers it.
- **`TYPEOF` cannot be used in a `WHERE` clause** — it shapes the returned fields only. Filtering by the polymorphic target still means filtering on `What.Type`.
- **Ordering by a parent field forces the sort onto the joined data** and cannot use a child-side index; on large result sets this is a real cost.

## Recall

Q: How far can you traverse in each direction, and why the asymmetry?
A: Five levels child-to-parent, one level parent-to-child. Upward each step resolves to at most one record so cost is predictable; downward each step multiplies rows by an unknown factor.

Q: What is the difference between `Deal__c` and `Deal__r`?
A: `Deal__c` is the lookup field, holding the Id and used in `WHERE`. `Deal__r` is the relationship, used in the field list to traverse to the parent's fields.

Q: How many parent-to-child relationships can one query reference?
A: Twenty.

Q: What does `TYPEOF` solve, and where can it not be used?
A: It reads fields from a polymorphic lookup like `Task.What` in one query instead of branching in code. It cannot appear in a `WHERE` clause.

Q: In user mode, how do FLS and sharing failures differ along a traversal path?
A: A field the user cannot read raises an exception; a record the user cannot see returns null. The difference identifies which of the two is the cause.

## Related

- [01 · Query anatomy & the SOQL model](01-query-anatomy-and-the-soql-model.md) — why there are no joins, and the row budget these subqueries spend from
- [06 · Semi-joins, anti-joins & set filtering](06-semi-joins-anti-joins-and-set-filtering.md) — filtering a parent by its children, which traversal cannot express
- [08-data · 02 Relationships deep dive](../08-data-modeling-and-large-data-volumes/02-relationships-deep-dive.md) — master-detail vs lookup, cascade and reparenting, and why the model constrains the query
- [08-data · 04 Standard CRM object map](../08-data-modeling-and-large-data-volumes/04-standard-crm-object-map.md) — `WhoId` and `WhatId`, the polymorphic joints `TYPEOF` exists for
