# Query Anatomy & the SOQL Model

> Area: 10-soql-and-sosl · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 22

**Scope:** What a SOQL statement is made of, the order the platform evaluates it in, and the budgets every query spends from. Why a *valid* query is slow is [08-data · 08](../08-data-modeling-and-large-data-volumes/08-indexes-and-query-selectivity.md); calling SOQL from Apex is [02-apex · 03](../02-apex-and-triggers/03-soql-fundamentals-and-relationship-queries.md).

## Core idea

SOQL looks like SQL and is not one. **There is no `FROM a, b` and no `JOIN` — a query has exactly one driving object, and everything else is reached by traversing relationships that already exist in the schema.** That single constraint explains nearly all of SOQL's shape: why the field list is where relationships appear, why going up is cheap and going down needs a subquery, why the optimizer can be predictable enough to publish selectivity thresholds. The second thing to internalise is that a query is not free and not unbounded. Every statement spends from a per-transaction budget of **100 queries and 50,000 rows**, and rows are counted as *returned*, including a subquery's children. Most SOQL design questions are really "how many rows does this shape return, and can the filter use an index?"

## How it works

- **Clause order is fixed** — the platform rejects any other sequence:

```sql
SELECT   fieldList, (subquery), aggregate alias    -- what comes back
FROM     ObjectType                                -- exactly one driving object
[USING SCOPE  scope]                               -- mine, team, everything…
[WHERE   condition]                                -- row filter, pre-aggregation
[WITH    USER_MODE | SECURITY_ENFORCED | DATA CATEGORY …]
[GROUP BY field [ROLLUP|CUBE] [HAVING condition]]  -- post-aggregation filter
[ORDER BY field [ASC|DESC] [NULLS FIRST|LAST]]
[LIMIT n] [OFFSET n]
[FOR VIEW | FOR REFERENCE | FOR UPDATE]
[ALL ROWS]                                         -- include soft-deleted
```

- **`WHERE` filters rows, `HAVING` filters groups.** `HAVING` is the only place an aggregate can appear in a condition, and it runs after grouping — so filtering on a non-aggregated field belongs in `WHERE`, where an index can still help.
- **`LIMIT` does not reduce the work the database does.** It caps what is returned; a non-selective filter still scans. `LIMIT 1` on an unindexed field is a full scan that throws away everything but one row.
- **`USING SCOPE`** pre-filters by ownership — `mine`, `myTeam`, `delegated`, `everything` — and is how a list view expresses "my accounts" without a `WHERE OwnerId =` that the optimizer treats differently.
- **The budget is per transaction, not per query:** 100 SOQL queries (200 async), 50,000 rows total, 20 SOSL queries, 2,000 SOSL rows. → [02-apex · 01](../02-apex-and-triggers/01-apex-language-core-and-governor-limits.md)

## 2026 currency

**SOQL defaults to user mode at API 67.0**, which changes what a query *means* rather than how it is written: FLS is enforced, so selecting a field the running user cannot read raises an exception instead of returning null, and sharing applies, so the same query returns different row counts for different users. The practical consequence is that a query verified as System Administrator proves nothing about what anyone else gets. `WITH SECURITY_ENFORCED` **no longer compiles** — `WITH USER_MODE` replaces it. Salesforce also began shipping query diagnostics into the platform: **Database Insights** (Winter '26) surfaces inefficient SOQL with recommendations, and **Platform Cache Detection for SOQL** flags repeated queries that should be cached rather than re-run. → [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md), [02-apex · 25](../02-apex-and-triggers/25-platform-cache.md)

## Gotchas

- **There are no joins.** A question spanning two unrelated objects is two queries and a map in application code, not one clever statement.
- **A subquery's child rows count against the 50,000-row limit.** 10,000 accounts each with five opportunities is 60,000 rows and the query *fails* rather than truncating.
- **`OFFSET` caps at 2,000 and re-runs the whole query per page.** Real pagination filters on the last Id seen, or uses a cursor → [02-apex · 17](../02-apex-and-triggers/17-database-cursor-and-large-result-sets.md).
- **`ORDER BY` puts nulls first by default** — say `NULLS LAST` whenever the ordering is user-visible.
- **`ALL ROWS` is the only way SOQL sees soft-deleted records**, and it cannot be combined with `FOR UPDATE` → [08-data · 13](../08-data-modeling-and-large-data-volumes/13-deletes-recycle-bin-and-physical-deletion.md).
- **`FOR UPDATE` locks the returned rows for the rest of the transaction and cannot be combined with `ORDER BY`.** There is no early release, so a long transaction converts other users' saves into `UNABLE_TO_LOCK_ROW`. What the lock actually does, the lock-wait timeout and the parent-lock behaviour are [08-data · 12](../08-data-modeling-and-large-data-volumes/12-record-locking-and-concurrency.md) — **this note owns the clause, that one owns the concurrency.**
- **`FIELDS(ALL)` requires `LIMIT 200` or fewer**, and at 67.0 resolves to the fields the *running user* can read — so the same query returns different columns for different people.
- **Querying a field you did not select throws at runtime, not compile time**, when the object came from a query rather than a constructor. The exception names the field, which is the only helpful thing about it.

## Recall

Q: Why does SOQL have no `JOIN` keyword?
A: A query has exactly one driving object and reaches everything else by traversing existing schema relationships. Unrelated objects require two queries and application-side correlation.

Q: What is the difference between `WHERE` and `HAVING`?
A: `WHERE` filters rows before grouping and can use an index; `HAVING` filters groups after aggregation and is the only place an aggregate function may appear in a condition.

Q: Does `LIMIT` make a query cheaper for the database?
A: No. It caps what is returned, not what is scanned. A non-selective filter with `LIMIT 1` still scans.

Q: What counts against the 50,000-row transaction limit in a parent-to-child query?
A: Both parent and child rows. Ten thousand parents with five children each is 60,000 rows, and the query fails rather than truncating.

Q: What replaced `WITH SECURITY_ENFORCED` at 67.0?
A: `WITH USER_MODE`. The old clause no longer compiles, and user mode is now the default anyway.

## Related

- [02 · Filtering, operators & literals](02-filtering-operators-and-literals.md) — the `WHERE` clause in detail, including `INCLUDES` for multi-select picklists
- [04 · Relationship queries in depth](04-relationship-queries-in-depth.md) — traversal, the direction asymmetry, and polymorphic lookups
- [08-data · 08 Indexes & query selectivity](../08-data-modeling-and-large-data-volumes/08-indexes-and-query-selectivity.md) — why a correct query is still slow, and the numbers that decide it
- [02-apex · 03 SOQL in Apex](../02-apex-and-triggers/03-soql-fundamentals-and-relationship-queries.md) — binding, the SOQL `for` loop and the governor budget from Apex's side
