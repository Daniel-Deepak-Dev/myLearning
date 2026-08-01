# SOQL Fundamentals & Relationship Queries

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 03

**Scope:** Reading data with SOQL — traversal, aggregation, filtering and the row budget. Dynamic SOQL, SOSL and injection defence are [04](04-advanced-soql-sosl-and-dynamic-queries.md); selectivity and query plans are [08-data](../08-data-modeling-and-large-data-volumes/INDEX.md).

## Core idea

SOQL reads one object at a time and reaches everything else through **relationships**, which is the single structural difference from SQL: there are no joins, only traversal along fields that already exist in the schema. That constraint is what makes the query planner predictable and what makes the direction of a relationship matter so much. Going *up* from child to parent is cheap dot notation and can climb five levels. Going *down* from parent to children needs a subquery and only goes one level. Almost every SOQL design question — one query or two, subquery or map — is really a question about which direction you are travelling and how many rows come back, because rows retrieved is a governor limit and the shape of the query decides it.

## How it works

- **Child-to-parent uses dot notation, up to five levels.** `Contact.Account.Owner.Manager.Name`. Custom relationships take the `__r` suffix: `Opportunity.Custom_Deal__r.Owner.Email`.
- **Parent-to-child uses a subquery, one level only**, and the relationship name is plural — `SELECT Id, (SELECT Id, Amount FROM Opportunities) FROM Account`. A query may reference at most 20 parent-to-child relationships.
- **Aggregates return `AggregateResult`, not sObjects.** `COUNT(field)`, `SUM`, `AVG`, `MIN`, `MAX` combine with `GROUP BY` and `HAVING`; alias each column and read it back with `ar.get('alias')`, casting to the type you expect.

> **From my notes.** *"`COUNT()` cannot be used with `GROUP BY` — use `COUNT(Id)`."* The rule is correct and still current — but the same note then gives `select count() from case group by status` as an example, and **that query does not run.** `COUNT()` has been invalid with `GROUP BY` since API 19.0, and it must be the only element in the `SELECT` list.

- **Date literals beat computing dates in Apex.** `TODAY`, `LAST_N_DAYS:30`, `THIS_FISCAL_QUARTER`, `NEXT_WEEK` are evaluated against the org's locale and fiscal calendar, which your `Date.today().addDays(-30)` is not.
- **`FIELDS(ALL)`, `FIELDS(STANDARD)` and `FIELDS(CUSTOM)`** save typing during exploration. `FIELDS(ALL)` requires a `LIMIT` of 200 or fewer and is a poor fit for production code, where naming fields is the documentation.

```apex
// COUNT(Id), not COUNT() — GROUP BY requires the field form
for (AggregateResult ar : [
    SELECT StageName stage, COUNT(Id) deals, SUM(Amount) total
    FROM Opportunity
    WHERE CloseDate = THIS_FISCAL_QUARTER
    GROUP BY StageName
    HAVING COUNT(Id) > 5
]) {
    System.debug(ar.get('stage') + ' ' + (Integer) ar.get('deals'));
}
```

## 2026 currency

SOQL runs in **user mode by default** at 67.0, and that changes what a query means rather than how you write it. Field-level security is enforced, so selecting a field the running user cannot read raises a `QueryException` instead of returning null — and because sharing applies too, the same query returns different row counts for different users. Two practical consequences: `FIELDS(ALL)` now resolves to *accessible* fields only, and a query tested as a System Administrator proves nothing about what a support agent will get. Full detail in [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **`COUNT()` returns an `Integer`; `COUNT(fieldName)` returns `AggregateResult` rows and skips nulls.** `COUNT(Id)` matches `COUNT()` only because `Id` is never null — `COUNT(Phone)` will not.
- **Aggregate queries cap at 2,000 rows in the result set.** A `GROUP BY` over a high-cardinality field silently hits a ceiling you did not ask about.
- **Each row an aggregate query *returns* costs one against the 50,000-row limit**, not each row it scanned — which is exactly what makes `COUNT()` cheap over a large object.
- **A subquery's child rows count toward the row limit too.** Ten thousand accounts each with five opportunities is 60,000 rows, and the query fails rather than truncating.
- **`ORDER BY` puts nulls first by default.** Say `NULLS LAST` when the ordering is user-visible.
- **`OFFSET` caps at 2,000** and re-runs the whole query each page. For real paging, filter on the last Id seen instead.
- **A SOQL `for` loop chunks records 200 at a time and keeps the heap flat**; assigning the same query to a `List` materialises everything. On large result sets this is the difference between working and a heap limit. → [01](01-apex-language-core-and-governor-limits.md)

## Recall

Q: How many levels can you traverse child-to-parent, and parent-to-child?
A: Five levels up with dot notation; one level down with a subquery, and at most 20 parent-to-child relationships per query.

Q: Why can't you use `COUNT()` with `GROUP BY`?
A: `COUNT()` returns a bare `Integer` and must be the only element in the `SELECT` list. `GROUP BY` needs the `COUNT(fieldName)` form, which returns `AggregateResult`.

Q: What is the row ceiling on an aggregate query's result set?
A: 2,000 rows. Grouping on a high-cardinality field hits it silently.

Q: What does a SOQL `for` loop do that a `List` assignment does not?
A: It processes records in chunks of 200, keeping heap flat instead of materialising the entire result set.

Q: In user mode, what happens when you select a field the running user cannot read?
A: The query throws a `QueryException` rather than returning null — and sharing means the row count varies by user too.

## Related

- [04 · Advanced SOQL, SOSL & dynamic queries](04-advanced-soql-sosl-and-dynamic-queries.md) — semi-joins, `TYPEOF`, `FOR UPDATE` and building queries at runtime
- [08 · Bulkification patterns](08-bulkification-patterns.md) — why the map-from-query idiom exists and where to put the query
- [08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md) — selectivity, indexes and reading a Query Plan when a valid query is simply slow
