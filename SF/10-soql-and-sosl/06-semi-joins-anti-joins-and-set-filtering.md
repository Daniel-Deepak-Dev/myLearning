# Semi-Joins, Anti-Joins & Set Filtering

> Area: 10-soql-and-sosl · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 22

**Scope:** Filtering one object by the existence of related records — `IN (SELECT …)`, `NOT IN (SELECT …)`, and when a two-query-and-a-map is the better answer. Traversal is [04](04-relationship-queries-in-depth.md).

## Core idea

Traversal answers "give me the parent's fields" and cannot answer **"give me the parents that have a child matching X"**. That question is a semi-join: a subquery in the `WHERE` clause used purely as a set membership test, where nothing from the subquery is returned. Its negation is an anti-join. Both exist because SOQL has no `EXISTS` and no `JOIN`, and both are tightly rationed — **at most two per query, counted together** — which is not a performance guideline but a compile-time ceiling. That ration is the whole design pressure here: real filtering questions routinely need three related sets, and the answer is then two queries and a `Set<Id>` in application code, not a cleverer statement.

## How it works

- **A semi-join tests membership; an anti-join tests absence:**

```sql
-- accounts that have at least one open opportunity
SELECT Id, Name FROM Account
WHERE Id IN (SELECT AccountId FROM Opportunity WHERE StageName != 'Closed Won')

-- accounts with no case at all
SELECT Id, Name FROM Account
WHERE Id NOT IN (SELECT AccountId FROM Case)
```

- **The subquery may select exactly one field**, and it must be an `Id` or a reference (lookup/master-detail) field. Selecting anything else is a compile error.
- **The comparison field must be an Id or a reference field too** — you cannot semi-join on `Name` or a text external Id.
- **Two is the hard ceiling**, shared between semi-joins and anti-joins in the same statement. A third is rejected at compile time.
- **The alternative is a bind against a collection**, which is what most bulkified Apex actually does: query the child object, collect `Set<Id>` of parent Ids, then `WHERE Id IN :parentIds`. Two queries instead of one, no ceiling, and each is independently selective → [02-apex · 08](../02-apex-and-triggers/08-bulkification-patterns.md).

## 2026 currency

The syntax and the ceiling are unchanged. What changed at 67.0 is that **the subquery is evaluated in user mode too**, so a semi-join silently narrows twice: once by the subquery's own sharing visibility and again by the outer query's. An anti-join is the dangerous half of that — `NOT IN (SELECT …)` returns parents whose children the running user *cannot see*, which reads as "accounts with no cases" and actually means "accounts with no cases **you** can see". A support-tier user therefore gets a *larger* result set from an anti-join than an administrator, which is the opposite of the usual user-mode symptom and correspondingly harder to spot. → [02-apex · 10](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)

## Gotchas

- **Two semi-joins/anti-joins per query, total.** It is a compile error, not a slow query, and it is the reason a filter that reads naturally has to be split.
- **`NOT IN` with a subquery that returns any null excludes everything.** Standard SQL three-valued-logic behaviour, and the failure is a silently empty result rather than an error.
- **An anti-join over a large child object is expensive** — the platform must establish absence, which cannot use the child index the way a positive test can → [08-data · 09](../08-data-modeling-and-large-data-volumes/09-query-plan-and-performance-tuning.md).
- **The subquery ignores `LIMIT` and `ORDER BY`** — it is a set, not a list, and including them is either an error or meaningless.
- **A semi-join cannot reference the outer query.** There is no correlated subquery in SOQL, so "children whose amount exceeds the parent's" is not expressible.
- **`IN :collection` and `IN (SELECT …)` look alike and are not.** The bind form has no ceiling and no reference-field restriction; only the subquery form is rationed.
- **Semi-joining on a formula field is not allowed**, even a formula that returns an Id.

## Recall

Q: What question does a semi-join answer that traversal cannot?
A: "Which parents have at least one child matching X" — membership. Traversal only fetches a parent's fields; it cannot filter by the existence of related records.

Q: How many semi-joins and anti-joins may one query contain?
A: Two in total, counted together. A third is a compile error.

Q: What may the subquery of a semi-join select?
A: Exactly one field, and it must be an Id or a reference field. Anything else is rejected at compile time.

Q: Why can an anti-join return *more* rows for a low-privilege user at 67.0?
A: The subquery runs in user mode, so children the user cannot see do not exist for the test. "Accounts with no cases" becomes "accounts with no cases you can see".

Q: When is two queries and a `Set<Id>` better than a semi-join?
A: Whenever the filter needs more than two related sets, or when each side benefits from being independently selective. The bind form has no ceiling.

## Related

- [04 · Relationship queries in depth](04-relationship-queries-in-depth.md) — traversal, which answers the "give me the parent's fields" half
- [02 · Filtering, operators & literals](02-filtering-operators-and-literals.md) — `IN` and `NOT IN` against literal lists and bind collections
- [02-apex · 08 Bulkification patterns](../02-apex-and-triggers/08-bulkification-patterns.md) — the query-collect-query idiom that replaces a rationed semi-join
- [08-data · 09 Query Plan & performance tuning](../08-data-modeling-and-large-data-volumes/09-query-plan-and-performance-tuning.md) — diagnosing what an anti-join actually costs
