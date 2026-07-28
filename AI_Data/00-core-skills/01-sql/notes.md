# SQL Fluency

> Track: Core skills · Roadmap: Phase 01 · Weeks 1–4 · Status: 🌱 learning
> Vendor-neutral. Salesforce-specific application lives in [01-data-cloud/](../../01-data-cloud/INDEX.md).

**Roadmap scope:** Joins, CTEs, window functions, aggregation. SQL is the lingua franca of Data 360 queries, calculated insights, and every pipeline you'll touch.

## What is it?

The query language for relational and lakehouse data. Four constructs carry most of the analytical work:

| Construct | What it does |
|---|---|
| **Joins** | Combine rows across tables — `INNER`, `LEFT`, `FULL`, and the `CROSS`/self-join edge cases |
| **Aggregation** | `GROUP BY` + `SUM`/`COUNT`/`AVG`, filtered with `HAVING` (not `WHERE`) |
| **CTEs** (`WITH`) | Name a subquery so a complex query reads top-to-bottom instead of inside-out |
| **Window functions** | Compute across a set of rows *without collapsing them* — running totals, rankings, lag/lead |

**Window functions are the one worth real practice.** They're what separates "can write SQL" from "can express an analytical question", and they're exactly what calculated insights are built from.

## Why it matters (for the AI-Salesforce architect role)

**Three places it pays off directly, and the third is new:**

1. **Calculated insights** are defined with SQL-like expressions. Lifetime value, engagement scores, churn risk — all window functions and aggregations.
2. **Pipelines and data engineering** — ELT means the transformation happens in the warehouse, in SQL.
3. **SQL from Apex (Summer '26)** — you can now run SQL from Apex against Data 360. This is the newest and most concrete payoff: SOQL genuinely cannot express the joins, aggregations and window functions lakehouse work needs, and the previous alternative was HTTP callouts to the Direct API. An Apex-backed agent action can now compute a rolling aggregate or multi-table join in one query.

That third point is why this topic is worth more attention in 2026 than it would have been in 2024. SQL stopped being "the thing the data team uses" and became something an Apex developer reaches for directly.

## How it works

### Window functions — the shape to internalize

```sql
SELECT
  profile_id,
  order_date,
  amount,
  SUM(amount) OVER (
      PARTITION BY profile_id          -- reset per customer
      ORDER BY order_date              -- accumulate in this order
      ROWS BETWEEN 90 PRECEDING AND CURRENT ROW
  ) AS rolling_90d_value
FROM orders;
```

Three parts: **`PARTITION BY`** (the group), **`ORDER BY`** (the sequence within it), **frame** (`ROWS BETWEEN …`, which rows count). Get those three right and most analytical questions fall out.

Common ones: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`/`LEAD()`, running `SUM`/`AVG`.

### CTEs for readability

```sql
WITH recent_orders AS (
  SELECT profile_id, SUM(amount) AS total
  FROM orders
  WHERE order_date >= CURRENT_DATE - 90
  GROUP BY profile_id
)
SELECT p.name, r.total
FROM profiles p
JOIN recent_orders r ON r.profile_id = p.id
WHERE r.total > 1000;
```

A nested subquery reads inside-out; a CTE reads top-down. On anything non-trivial, that's the difference between reviewable and not.

### Joins — the one that causes wrong answers

`LEFT JOIN` then filtering the right table in `WHERE` silently converts it to an `INNER JOIN`:

```sql
-- BUG: the WHERE clause drops the unmatched rows LEFT JOIN preserved
SELECT * FROM a LEFT JOIN b ON b.a_id = a.id WHERE b.status = 'X';

-- FIX: filter in the join condition
SELECT * FROM a LEFT JOIN b ON b.a_id = a.id AND b.status = 'X';
```

This produces a plausible-looking result with rows missing, which is the worst failure mode there is.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Work through SQLBolt end to end (a couple of hours).
- [ ] Mode's SQL tutorial through the window-functions section.
- [ ] Write a rolling-90-day-value query, then re-express it as a calculated insight.
- [ ] Write one SQL-from-Apex method against Data 360 returning an aggregate.

## Gotchas & sharp edges

- **`LEFT JOIN` + `WHERE` on the right table = `INNER JOIN`.** Silent, plausible, wrong.
- **`HAVING` filters groups, `WHERE` filters rows.** Aggregates can't appear in `WHERE`.
- **`NULL` propagates.** `NULL = NULL` is not true; use `IS NULL`. And in Data 360, whether `NULL` and `''` are distinct depends on `honorEmptyStrings` — see [data modeling](../../01-data-cloud/03-data-modeling-dso-dlo-dmo/notes.md).
- **`COUNT(*)` vs `COUNT(col)`** — the second skips `NULL`s.
- **Window frames default surprisingly.** With `ORDER BY` and no explicit frame you usually get `RANGE UNBOUNDED PRECEDING`, not the whole partition. Be explicit.
- **SQL dialects differ** on date functions and string handling. Check the target engine.

## Related topics

- [Insights & segmentation](../../01-data-cloud/05-insights-segmentation/notes.md) — where these expressions get used
- [Data modeling](../../01-data-cloud/03-data-modeling-dso-dlo-dmo/notes.md) — `SET OPTIONS`, dataspaces, null handling
- [Data engineering patterns](../04-data-engineering/notes.md) — ELT and transformation
- [Python for data work](../02-python-for-data/notes.md) — the other data-manipulation tool
