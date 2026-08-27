# Date, Datetime & Locale Literals

> Area: 10-soql-and-sosl · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 22

**Scope:** SOQL's built-in date literals, date functions, and the timezone and fiscal-calendar behaviour that makes them different from computing a date in code. General operators are [02](02-filtering-operators-and-literals.md).

## Core idea

Every date literal in SOQL is evaluated **by the platform, against the running user's timezone and the org's fiscal calendar**. That is the entire reason to prefer `LAST_N_DAYS:30` over a `Date.today().addDays(-30)` computed in Apex and bound in: the bound value is a single instant decided by the *server's* view of "now", while the literal is resolved per user with their locale and the org's fiscal year definition applied. In an org whose fiscal year starts in April, `THIS_FISCAL_QUARTER` is a question no application code can answer without re-implementing the fiscal calendar — and re-implementing it is how reports and queries end up disagreeing about the same quarter.

## How it works

| Literal family | Examples | Notes |
|---|---|---|
| Fixed | `YESTERDAY`, `TODAY`, `TOMORROW` | relative to the **running user's** timezone |
| Rolling window | `LAST_N_DAYS:n`, `NEXT_N_WEEKS:n`, `LAST_N_MONTHS:n` | `LAST_N_DAYS:n` **includes today**; `LAST_90_DAYS` does not exist — use the `N` form |
| Calendar period | `THIS_WEEK`, `LAST_MONTH`, `THIS_YEAR` | week start follows the org's locale |
| Fiscal period | `THIS_FISCAL_QUARTER`, `LAST_FISCAL_YEAR`, `NEXT_N_FISCAL_QUARTERS:n` | uses the org's **fiscal year settings**, not the calendar |

- **Date functions extract a component for grouping** — `CALENDAR_YEAR()`, `CALENDAR_MONTH()`, `DAY_ONLY()`, `FISCAL_QUARTER()`, `WEEK_IN_YEAR()`:

```sql
SELECT CALENDAR_YEAR(CloseDate) yr, FISCAL_QUARTER(CloseDate) q, SUM(Amount) total
FROM Opportunity
WHERE CloseDate = LAST_N_FISCAL_QUARTERS:4
GROUP BY CALENDAR_YEAR(CloseDate), FISCAL_QUARTER(CloseDate)
ORDER BY CALENDAR_YEAR(CloseDate)
```

- **`DAY_ONLY(dateTimeField)` converts a Datetime to a Date** so it can be grouped — grouping on a raw Datetime groups by the second and produces one row per record.
- **A literal date is written unquoted and in a fixed format** — `2026-08-04` for Date and `2026-08-04T00:00:00Z` for Datetime. **Quoting it is a compile error**, which is the fastest way to spot a query pasted from a SQL background.
- **`convertTimezone()`** shifts a Datetime into the user's timezone *inside* a date function: `CALENDAR_MONTH(convertTimezone(CreatedDate))`. Without it, grouping a Datetime by month is grouped in **GMT**.

## 2026 currency

Date literals themselves are long-stable and nothing changed in the 2024–2026 window. The one thing that did change is contextual and easy to miss: because **SOQL runs in user mode at 67.0**, a query using `TODAY` or `THIS_WEEK` is now evaluated for a running user who may not be the one you tested as — and those literals were *always* resolved against the running user's timezone. The flip did not change the literals; it changed how often the running user is somebody else. A scheduled job's queries resolve against the **job owner's** timezone, which is the usual explanation for a nightly report that is one day off for part of the year. → [02-apex · 15](../02-apex-and-triggers/15-scheduled-apex-and-cron.md)

## Gotchas

- **`LAST_N_DAYS:n` includes today; `LAST_N_MONTHS:n` does not include the current month.** The families are not consistent with each other and the docs state each separately.
- **Fiscal literals use the org's fiscal calendar, and custom fiscal years change their meaning.** An org that switches from standard to custom fiscal years silently changes what every fiscal literal returns.
- **Grouping on a Datetime groups by the second.** `DAY_ONLY()` or a `CALENDAR_*` function is required, or the "grouped" result is one row per record.
- **Date functions in a `WHERE` clause defeat the index on that field.** `WHERE CALENDAR_YEAR(CloseDate) = 2026` scans; `WHERE CloseDate = THIS_YEAR` does not.
- **Datetime grouping is GMT unless you wrap it in `convertTimezone()`**, so month and day boundaries land in the wrong bucket for most of the world.
- **Literals are unquoted.** `WHERE CloseDate = 'TODAY'` and `WHERE CloseDate = '2026-08-04'` are both compile errors.
- **A scheduled job resolves `TODAY` against the job owner's timezone**, not the org default and not the last person who edited it.

## Recall

Q: Why prefer `LAST_N_DAYS:30` over a date computed in Apex?
A: The literal is resolved by the platform against the running user's timezone and the org's fiscal calendar. A computed value is one fixed instant and cannot express fiscal periods at all.

Q: What does `DAY_ONLY()` solve?
A: Grouping a Datetime field. Without it, grouping happens at second precision and returns one row per record.

Q: Why might a nightly scheduled report be one day out?
A: Date literals resolve against the running user's timezone, and for a scheduled job that is the job owner — not the org default.

Q: What happens to the index when you write `WHERE CALENDAR_YEAR(CloseDate) = 2026`?
A: It is not used. Wrapping the field in a function forces a scan; `WHERE CloseDate = THIS_YEAR` stays selective.

Q: How is a literal date written in SOQL?
A: Unquoted, `2026-08-04` for a Date and `2026-08-04T00:00:00Z` for a Datetime. Quoting it is a compile error.

## Related

- [02 · Filtering, operators & literals](02-filtering-operators-and-literals.md) — the rest of the `WHERE` clause these sit inside
- [05 · Aggregates, GROUP BY, ROLLUP & CUBE](05-aggregates-group-by-rollup-and-cube.md) — where the `CALENDAR_*` and `FISCAL_*` functions actually earn their place
- [08-data · 08 Indexes & query selectivity](../08-data-modeling-and-large-data-volumes/08-indexes-and-query-selectivity.md) — why wrapping a field in a function costs the index
- [08-data · 22 Multi-currency, multi-language & locale](../08-data-modeling-and-large-data-volumes/22-multi-currency-multi-language-and-locale.md) — the org settings these literals read
