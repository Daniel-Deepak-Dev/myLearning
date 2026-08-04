# SOQL in Apex

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 03 *(narrowed in phase 22)*

**Scope:** SOQL **as Apex sees it** — inline queries and binding, the `for` loop's heap behaviour, the governor budget, and reading `AggregateResult`. **The query language itself is [10-soql · 01–07](../10-soql-and-sosl/INDEX.md)**, which owns clause order, traversal rules, operators, date literals and aggregate syntax. Selectivity is [08-data · 08](../08-data-modeling-and-large-data-volumes/08-indexes-and-query-selectivity.md); query plans are [08-data · 09](../08-data-modeling-and-large-data-volumes/09-query-plan-and-performance-tuning.md).

## Core idea

Apex embeds SOQL in the language rather than passing it as a string, and that one decision produces everything specific about querying from Apex. **The query is compile-checked** — a misspelled field fails the deployment, not the transaction — and it can reference Apex variables directly with a colon. In exchange, the shape of the query is fixed at compile time; anything decided at runtime needs [04](04-advanced-soql-sosl-and-dynamic-queries.md). The second Apex-specific concern is that a query's result has to live somewhere: **the difference between assigning to a `List` and iterating with a SOQL `for` loop is the difference between materialising the whole result set in heap and holding 200 records at a time.** Nearly every Apex query decision is one of those two — is it compile-time or runtime, and does the result fit in heap.

## How it works

- **Bind an Apex variable with `:`**, including collections, which is how a bulkified query filters by a set gathered earlier:

```apex
Set<Id> accountIds = Trigger.newMap.keySet();
for (Opportunity o : [SELECT Id, Amount, Account.Name FROM Opportunity
                      WHERE AccountId IN :accountIds]) {   // collection bind
    // …
}
```

- **The SOQL `for` loop chunks records 200 at a time and keeps heap flat.** Assigning the same query to a `List` materialises everything. On a large result set this is the difference between working and a heap limit → [01](01-apex-language-core-and-governor-limits.md).
- **Aggregates return `AggregateResult`, not SObjects.** Alias every column and read it back with `ar.get('alias')`, casting to the type you expect. Unaliased columns arrive as `expr0`, `expr1` in declaration order.
- **The budget is per transaction: 100 queries (200 async) and 50,000 rows.** `Limits.getQueries()` and `getQueryRows()` read the current consumption, which is how a service class defends itself before the failure rather than after → [24](24-apex-performance-and-profiling.md).
- **`Database.getQueryLocator()`** hands the query to Batch Apex instead of executing it, raising the reach to 50 M rows → [14](14-batch-apex-and-stateful-processing.md).

## 2026 currency

SOQL runs in **user mode by default** at 67.0, and from Apex that changes what a query means rather than how you write it. FLS is enforced, so selecting a field the running user cannot read raises a `QueryException` instead of returning null; sharing applies, so the same query returns different row counts for different users. Two consequences specific to Apex: `FIELDS(ALL)` resolves to *accessible* fields only, so the same code returns different columns per user, and **a query tested as a System Administrator proves nothing about what a support agent gets** — which is why `System.runAs` moved from optional to necessary in tests. Pass `AccessLevel.SYSTEM_MODE` or use `WITH SYSTEM_MODE` where elevation is genuinely intended. → [10](10-apex-security-user-mode-and-fls.md), [20](20-apex-testing-fundamentals.md), [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md)

## Gotchas

- **A SOQL `for` loop over a `List` variable does not chunk.** The chunking comes from iterating the *query*; `for (Account a : someList)` has already paid the heap cost.
- **Each row an aggregate query *returns* costs one against the 50,000-row limit**, not each row it scanned — which is what makes `COUNT()` cheap over a very large object.
- **A subquery's child rows count toward the row limit too**, and the query fails rather than truncating → [10-soql · 01](../10-soql-and-sosl/01-query-anatomy-and-the-soql-model.md).
- **Querying inside a loop is the canonical governor-limit bug**, and it is easiest to write by accident when the query is short → [08](08-bulkification-patterns.md).
- **A bind variable cannot substitute an identifier** — only values. An object or field name decided at runtime means dynamic SOQL → [04](04-advanced-soql-sosl-and-dynamic-queries.md).
- **Accessing a field that was not in the `SELECT` list throws at runtime**, not compile time, when the SObject came from a query. The exception names the field, which is the only helpful part.
- **`Limits.getQueryRows()` counts rows retrieved across the whole transaction**, including rows a `for` loop has already discarded — a flat heap does not mean a small row count.

## Recall

Q: What does a SOQL `for` loop do that a `List` assignment does not?
A: It processes records in chunks of 200, keeping heap flat instead of materialising the whole result set. The chunking comes from iterating the query itself.

Q: How do you filter a query by a set of Ids gathered earlier in the transaction?
A: A collection bind — `WHERE AccountId IN :accountIds`. This is the core of the bulkification idiom.

Q: Which rows of an aggregate query count against the 50,000-row limit?
A: Only the rows returned, not the rows scanned — which is why `COUNT()` over a very large object is cheap.

Q: In user mode, what happens when you select a field the running user cannot read?
A: The query throws a `QueryException` rather than returning null. Sharing separately means the row count varies by user.

Q: What can a bind variable not do?
A: Substitute an identifier. Object names, field names and clause keywords are not bindable — that requires dynamic SOQL.

## Related

- [10-soql · INDEX](../10-soql-and-sosl/INDEX.md) — **the reference for the query language itself.** Clause order and the row budget are [· 01](../10-soql-and-sosl/01-query-anatomy-and-the-soql-model.md), traversal [· 04](../10-soql-and-sosl/04-relationship-queries-in-depth.md), aggregates and `ROLLUP` [· 05](../10-soql-and-sosl/05-aggregates-group-by-rollup-and-cube.md)
- [04 · Dynamic SOQL, SOSL & describe in Apex](04-advanced-soql-sosl-and-dynamic-queries.md) — when the shape is not known until runtime
- [08 · Bulkification patterns](08-bulkification-patterns.md) — why the map-from-query idiom exists and where to put the query
- [08-data · 08 Indexes & query selectivity](../08-data-modeling-and-large-data-volumes/08-indexes-and-query-selectivity.md) — why a valid query is simply slow, and the thresholds that decide it
