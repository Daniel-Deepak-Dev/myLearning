# Advanced SOQL, SOSL & Dynamic Queries

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 03

**Scope:** Querying past the basics — polymorphic traversal, locking, joins, runtime-built queries, SOSL and schema describe. Fundamentals are [03](03-soql-fundamentals-and-relationship-queries.md); access-mode semantics in depth are phase 04.

## Core idea

Everything here exists because a static SOQL literal cannot express the question. Sometimes the *shape* is unknown until runtime — a filter builder, a configurable report, an agent action taking arbitrary criteria — and you need dynamic SOQL. Sometimes the *target* is polymorphic and one field can point at half a dozen objects, which is `TYPEOF`. Sometimes the search is genuinely full-text across objects, which is SOSL, not SOQL. The unifying risk is that the moment a query stops being a literal, the compiler stops protecting you: no field validation, no type checking, and an injection surface. Bind variables are the answer to all three, and at 67.0 they come with an explicit access level attached.

## How it works

- **`TYPEOF` resolves polymorphic lookups** — `Task.What`, `Event.Who`, `Owner` — in one query: `SELECT TYPEOF What WHEN Account THEN Industry WHEN Opportunity THEN Amount ELSE Name END FROM Task`. Without it you query the Id, branch in Apex and query again.
- **Semi-joins and anti-joins filter by a related set.** `WHERE Id IN (SELECT AccountId FROM Opportunity WHERE …)` and its `NOT IN` twin. **At most two per query**, and the subquery may only select `Id` or a reference field.
- **`FOR UPDATE` locks the returned rows** for the remainder of the transaction, which is how you make read-then-update safe against concurrent saves. It cannot be combined with `ORDER BY`.
- **SOSL is a different engine, not a SOQL variant:**

| | SOQL | SOSL |
|---|---|---|
| Searches | one object, plus relationships | many objects at once |
| Matching | field predicates in `WHERE` | the full-text search index |
| Returns | `List<sObject>` | `List<List<sObject>>`, one list per `RETURNING` clause |
| Budget | 100 queries / 50,000 rows | 20 queries / 2,000 rows |

- **Bind variables are the injection defence, and the only complete one:**

```apex
String bad = 'SELECT Id FROM Account WHERE Name = \'' + input + '\'';  // injectable

Map<String, Object> binds = new Map<String, Object>{ 'name' => input };
List<Account> safe = Database.queryWithBinds(
    'SELECT Id, Name FROM Account WHERE Name = :name',
    binds,
    AccessLevel.USER_MODE
);
```

- **Schema describe reads the metadata at runtime** — `Schema.SObjectType.Account.fields.getMap()`, `getDescribe().getPicklistValues()` — which is how generic components discover fields they were not compiled against.

> **From my notes.** The dependent-picklist recipe: each entry returned by `getPicklistValues()` carries a **`validFor`** key in its serialised form — a base64-encoded bitmap of which controlling values enable that entry. Decode with `EncodingUtil.base64Decode()` and test the bit at the controlling value's index. Still the only way to read the dependency from Apex, still undocumented, and still worth a comment in the code saying so.

## 2026 currency

`Database.query()` and `Database.queryWithBinds()` now default to **user mode**, so a dynamic query enforces the running user's FLS and sharing unless you pass `AccessLevel.SYSTEM_MODE` deliberately. `queryWithBinds` (Spring '23) takes its binds from a `Map<String, Object>` rather than resolving `:variable` against Apex locals, which removes the old scoping surprise where a bind silently picked up a variable from an enclosing block. Note also that `WITH SECURITY_ENFORCED` **no longer compiles** — anything you find using it in a dynamic query string is dead code and should become `WITH USER_MODE` or an explicit `AccessLevel`. See [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **`String.escapeSingleQuotes()` only escapes quotes.** It does nothing for an injected object name, field name, `LIMIT` or `ORDER BY` — those need an allowlist, not escaping. Prefer binds and use escaping only where a bind is impossible.
- **A bind cannot substitute an identifier.** Object names, field names and clause keywords must be assembled from values you control.
- **`FOR UPDATE` holds its locks until the transaction ends**, so a long transaction turns into `UNABLE_TO_LOCK_ROW` for everyone else. Lock late, commit fast — the 10-second wait and the parent-lock behaviour behind it are [08-data · 12](../08-data-modeling-and-large-data-volumes/12-record-locking-and-concurrency.md).
- **SOSL returns one list per `RETURNING` clause, in declaration order**, and an object with no matches gives an empty list rather than being omitted — index positionally, never by guessing.
- **SOSL needs at least two characters** in the search term and searches the index, so very recently created records may not be findable yet.
- **`Schema.getGlobalDescribe()` builds a map of every object in the org** — real CPU and heap cost. Reach for `Type.forName()` or a named `Schema.SObjectType` instead.
- **Two semi-joins is a hard ceiling**, and it counts anti-joins in the same budget. A third one is a compile error, not a slow query.

## Recall

Q: What does `TYPEOF` solve?
A: Reading fields from a polymorphic lookup like `Task.What` in a single query, instead of querying the Id and branching in Apex.

Q: What are the two arguments to `Database.queryWithBinds` beyond the query string?
A: A `Map<String, Object>` of bind values keyed by name, and an `AccessLevel` — `USER_MODE` or `SYSTEM_MODE`.

Q: Why is `String.escapeSingleQuotes()` not a complete injection defence?
A: It only handles quote characters. An injected field name, object name or `LIMIT` passes straight through; those need an allowlist.

Q: What does SOSL return, and how do you read it?
A: `List<List<sObject>>` — one inner list per `RETURNING` clause, in declaration order, empty rather than absent when nothing matched.

Q: How long does `FOR UPDATE` hold a lock?
A: Until the transaction ends. There is no early release, so long transactions cause `UNABLE_TO_LOCK_ROW` elsewhere.

## Related

- [03 · SOQL fundamentals & relationship queries](03-soql-fundamentals-and-relationship-queries.md) — traversal, aggregates and the row budget these build on
- [02 · Modern Apex syntax](02-modern-apex-syntax.md) — multiline strings are what make an assembled query readable
- [07-security · INDEX](../07-security-and-sharing/INDEX.md) — injection defence as one control inside the wider access model
