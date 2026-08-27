# SQL Fluency — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Joins, aggregation, CTEs and window functions — the four constructs behind calculated insights, ELT pipelines, and (new in Summer '26) SQL run from Apex against Data 360.

## Key terms
| Term | Definition |
|---|---|
| CTE (`WITH`) | Named subquery; makes complex queries read top-down instead of inside-out. |
| Window function | Computes across rows **without collapsing them** — running totals, ranks, lag/lead. |
| `PARTITION BY` / `ORDER BY` / frame | The three parts of a window: group, sequence, which rows count. |
| `HAVING` | Filters **groups**; `WHERE` filters **rows**. Aggregates can't go in `WHERE`. |

## Rules of thumb

- Practise **window functions** hardest — they're what calculated insights are made of.
- Reach for a CTE the moment a subquery nests twice.
- Be **explicit about the window frame**; the default with `ORDER BY` isn't the whole partition.
- SQL-from-Apex (Summer '26) is the new payoff: joins/aggregations/window functions SOQL can't express.

## Exam traps / common confusions

- **`LEFT JOIN` + `WHERE` on the right table silently becomes an `INNER JOIN`** — filter in the `ON` clause instead. Plausible result, missing rows.
- `NULL = NULL` is not true — use `IS NULL`.
- `COUNT(*)` counts rows; `COUNT(col)` skips `NULL`s.
- In Data 360, whether `NULL` and `''` are distinct depends on `honorEmptyStrings`.

## Minimal example

```sql
-- rolling 90-day value per customer, rows preserved
SELECT profile_id, order_date, amount,
       SUM(amount) OVER (
         PARTITION BY profile_id
         ORDER BY     order_date
         ROWS BETWEEN 90 PRECEDING AND CURRENT ROW
       ) AS rolling_90d
FROM orders;

-- the join bug, and its fix
SELECT * FROM a LEFT JOIN b ON b.a_id=a.id WHERE b.status='X';    -- INNER, silently
SELECT * FROM a LEFT JOIN b ON b.a_id=a.id AND   b.status='X';    -- actually LEFT
```
