# Filtering, Operators & Literals

> Area: 10-soql-and-sosl · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 22

**Scope:** Everything that can appear in a `WHERE` clause — comparison operators, `LIKE`, set membership, and the multi-select picklist operators almost everyone gets backwards. Date literals are [03](03-date-datetime-and-locale-literals.md); filtering by a *related set* is [06](06-semi-joins-anti-joins-and-set-filtering.md).

## Core idea

The operator set is small and mostly unsurprising, and then there are two places it stops behaving like SQL. **`LIKE` has no `%` — the wildcards are `%` for many and `_` for one, but a leading wildcard silently destroys index use**, which is the single commonest cause of a query that worked in a sandbox and times out in production. And **`INCLUDES` / `EXCLUDES` invert the punctuation you expect**: inside a multi-select picklist filter a semicolon means AND and a comma means OR, which is the reverse of the reading most people bring to it. Both traps share a shape worth internalising — the query is valid, returns rows, and is wrong or slow rather than broken.

## How it works

| Operator | Notes |
|---|---|
| `= != < <= > >=` | `!=` on a null field does **not** match nulls; test `!= null` explicitly |
| `LIKE` | strings only; `%` = any number of characters, `_` = exactly one; case-insensitive |
| `IN` / `NOT IN` | a literal list or a bind collection; `NOT IN` excludes nulls too |
| `INCLUDES` / `EXCLUDES` | **multi-select picklists only** — see the punctuation rule below |

- **The multi-select rule, stated precisely:** each quoted string is one *combination* and a **semicolon inside it means AND**; the **comma between strings means OR**.

```sql
-- "has AAA and BBB both selected"          → one string, semicolon
WHERE Interests__c INCLUDES ('AAA;BBB')

-- "has AAA, or BBB, or CCC"                → three strings, commas
WHERE Interests__c INCLUDES ('AAA', 'BBB', 'CCC')

-- "has (AAA and BBB), or has CCC"          → both, combined
WHERE Interests__c INCLUDES ('AAA;BBB', 'CCC')
```

- **`NOT` needs parentheses to negate a compound condition.** `NOT (A AND B)` is not `NOT A AND B`, and SOQL will happily parse the wrong one.
- **`toLabel()` filters and returns the translated value**, not the API name — `WHERE toLabel(Status) = 'Abierto'`. Essential for a multi-language org, and a trap in a single-language one where the two happen to coincide.
- **`FORMAT()`** wraps a number, date or currency in the running user's locale and currency formatting for display — `SELECT FORMAT(Amount) FROM Opportunity`. It returns a **string**, so it is a presentation tool and never something to compare against.

## 2026 currency

Nothing in the operator set changed, but **user mode changes which rows a filter can even see** — a `WHERE` clause is now evaluated after sharing narrows the set, so a filter that returned rows for an admin may return none for a support agent. Two smaller Winter '25 improvements are worth knowing because they remove long-standing annoyances in *dynamic* queries specifically: **error messages for invalid dynamic SOQL are far more specific** than the old generic parse failure, and **negative currency values are now supported** in dynamic SOQL and API-issued queries. → [07](07-dynamic-soql-and-injection-defence.md)

## Gotchas

- **A leading wildcard — `LIKE '%acme'` — cannot use an index.** It forces a full scan and is the classic "fast in sandbox, times out in production" query → [08-data · 08](../08-data-modeling-and-large-data-volumes/08-indexes-and-query-selectivity.md).
- **The `INCLUDES` punctuation is the reverse of most people's guess.** Semicolon is AND, comma is OR. Getting it backwards returns a plausible, wrong row set with no error.
- **`!=` excludes nulls.** `WHERE Status != 'Closed'` drops every record whose Status is blank — almost never what was meant.
- **`NOT IN` with a subquery is an anti-join and is capped at two per query**, shared with semi-joins → [06](06-semi-joins-anti-joins-and-set-filtering.md).
- **`LIKE` does not work on picklists, IDs, or number fields** — only on string-typed fields. On a picklist use `IN`.
- **Escaping in `LIKE` is a backslash**, and the value must escape `%`, `_` and `\` itself if they are meant literally.
- **`FORMAT()` returns a string**, so ordering or filtering on it sorts lexically — `'1,000'` before `'900'`.

## Recall

Q: In `INCLUDES ('AAA;BBB', 'CCC')`, what does the query match?
A: Records that have both AAA and BBB selected, **or** records that have CCC selected. Semicolon is AND within a string; comma is OR between strings.

Q: Why is `LIKE '%acme'` a problem?
A: A leading wildcard prevents index use, forcing a full scan. It is the commonest cause of a query that is fast on small data and times out at volume.

Q: What does `WHERE Status != 'Closed'` do to records with a null Status?
A: Excludes them. `!=` does not match nulls, so a null check has to be added explicitly.

Q: When would you use `toLabel()`?
A: To filter or return the translated picklist label rather than the API value — necessary in a multi-language org, where the API name and the user's label differ.

Q: What does `FORMAT()` return, and what does that rule out?
A: A locale-formatted string. Because it is a string, it must not be used for comparison or ordering — sorting is lexical, not numeric.

## Related

- [03 · Date, datetime & locale literals](03-date-datetime-and-locale-literals.md) — the other half of the `WHERE` clause, and why computing dates in code is worse
- [06 · Semi-joins, anti-joins & set filtering](06-semi-joins-anti-joins-and-set-filtering.md) — filtering by a related record set, and the hard ceiling of two
- [07 · Dynamic SOQL & injection defence](07-dynamic-soql-and-injection-defence.md) — what happens to these operators when the clause is assembled from input
- [08-data · 08 Indexes & query selectivity](../08-data-modeling-and-large-data-volumes/08-indexes-and-query-selectivity.md) — which of these filters an index can serve
