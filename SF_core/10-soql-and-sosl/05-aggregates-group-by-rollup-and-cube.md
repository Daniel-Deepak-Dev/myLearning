# Aggregates, GROUP BY, ROLLUP & CUBE

> Area: 10-soql-and-sosl · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 22

**Scope:** Aggregate functions, grouping, and the subtotal clauses that let one query do what usually takes a report. Reading the results from Apex is [02-apex · 03](../02-apex-and-triggers/03-soql-fundamentals-and-relationship-queries.md).

## Core idea

An aggregate query stops returning records and starts returning **`AggregateResult` rows**, which is the fact everything else follows from: there are no SObjects to cast, every column needs an alias to be readable, and the row count is the number of *groups*, not the number of records scanned. That last point is why `COUNT()` over ten million rows is cheap — the platform returns one row, and **only returned rows count against the 50,000-row limit**. `ROLLUP` and `CUBE` extend grouping with subtotal rows computed by the database, which is the part most people never reach for and the part that removes the most application code: a cross-tabular summary that would otherwise be several queries and a nested map becomes one statement.

## How it works

- **`COUNT()` and `COUNT(field)` are different functions.** `COUNT()` returns a bare `Integer` and must be the only element in the `SELECT` list. `COUNT(field)` returns `AggregateResult` rows and **skips nulls**. Only `COUNT(Id)` matches `COUNT()`, because `Id` is never null.
- **`GROUP BY ROLLUP` adds subtotals, aggregating right to left**, and takes **up to 3 fields**. `GROUP BY CUBE` adds subtotals for *every combination* of the grouped fields — a cross-tab rather than a hierarchy.
- **`GROUPING(field)` tells you which rows are subtotals** — it returns **1** when the row is a subtotal for that field and **0** when it is real data. Without it, subtotal rows are indistinguishable from data rows with a null in that column:

```sql
SELECT LeadSource, Rating, GROUPING(LeadSource) grpSrc, GROUPING(Rating) grpRating,
       COUNT(Id) cnt
FROM Lead
GROUP BY ROLLUP(LeadSource, Rating)
```

- **`HAVING` filters the grouped rows** and is the only clause where an aggregate may appear in a condition — `HAVING COUNT(Id) > 5`.
- **Alias everything you intend to read.** `SELECT StageName stage, SUM(Amount) total` is retrieved as `ar.get('stage')` and `ar.get('total')`; unaliased aggregates come back as `expr0`, `expr1` in declaration order.

> **From my notes.** *"`COUNT()` cannot be used with `GROUP BY` — use `COUNT(Id)`."* The rule is correct and still current — but the same note then gives `select count() from case group by status` as an example, and **that query does not run.** `COUNT()` has been invalid with `GROUP BY` since API 19.0, and it must be the only element in the `SELECT` list. *(Carried here from `02-apex · 03` in phase 22, with the topic it belongs to.)*

## 2026 currency

Nothing in the aggregate surface changed in the 2024–2026 window; `ROLLUP`, `CUBE` and `GROUPING()` are long-standing and simply under-used. Two 67.0-adjacent facts do change results rather than syntax. **User mode means aggregates are computed over the rows the running user can see**, so a `SUM(Amount)` is now a per-user number — a genuine problem for any code that caches or compares one. And **`MIN`, `MAX` and `GROUP BY` fail outright on a Shield-encrypted field**, which takes the whole query with them and is the reason an encryption rollout breaks reporting queries that never mentioned encryption. → [07-security · 21](../07-security-and-sharing/21-shield-platform-encryption.md)

## Gotchas

- **`COUNT()` cannot be used with `GROUP BY`** — it must be the only element in the `SELECT` list, and has been invalid with `GROUP BY` since API 19.0. Use `COUNT(Id)`.
- **Aggregate queries cap at 2,000 rows in the result set.** Grouping on a high-cardinality field hits a ceiling nothing warned you about, and the result is silently truncated rather than an error.
- **`GROUP BY` and `GROUP BY ROLLUP` cannot be combined in one statement.** Choose one; there is no partial-rollup form.
- **`ROLLUP` takes at most 3 fields.** A fourth is a compile error, not a slower query.
- **A subtotal row is not distinguishable from a data row without `GROUPING()`** — both show null in the rolled-up column, so summing the result set double-counts.
- **Aliases are required to read anything reliably**; unaliased columns arrive as `expr0`, `expr1`, positionally, and inserting a column silently renumbers them.
- **You cannot `ORDER BY` a field that is not grouped or aggregated**, which rules out the natural "sort by the record's name" on a grouped query.

## Recall

Q: Why can't `COUNT()` be used with `GROUP BY`?
A: `COUNT()` returns a bare `Integer` and must be the only element in the `SELECT` list. `GROUP BY` requires the `COUNT(fieldName)` form, which returns `AggregateResult` rows.

Q: What does `GROUPING(field)` return and why is it necessary?
A: 1 if the row is a subtotal for that field, 0 if it is data. Without it, subtotal rows look identical to data rows with a null, so consumers double-count.

Q: What is the difference between `ROLLUP` and `CUBE`?
A: `ROLLUP` produces a hierarchy of subtotals aggregating right to left; `CUBE` produces subtotals for every combination of the grouped fields, which is a cross-tab.

Q: What is the row ceiling on an aggregate query's result set?
A: 2,000 rows. Grouping on a high-cardinality field hits it silently.

Q: Which rows of an aggregate query count against the 50,000-row limit?
A: Only the rows returned — the groups — not the records scanned. That is what makes `COUNT()` cheap over a very large object.

## Related

- [03 · Date, datetime & locale literals](03-date-datetime-and-locale-literals.md) — `CALENDAR_*` and `FISCAL_*` functions, the usual grouping keys
- [01 · Query anatomy & the SOQL model](01-query-anatomy-and-the-soql-model.md) — where `HAVING` sits in clause order and why it runs after grouping
- [02-apex · 03 SOQL in Apex](../02-apex-and-triggers/03-soql-fundamentals-and-relationship-queries.md) — reading `AggregateResult` and casting `ar.get('alias')`
- [07-security · 21 Shield Platform Encryption](../07-security-and-sharing/21-shield-platform-encryption.md) — why an encrypted field cannot be grouped, min'd or max'd
