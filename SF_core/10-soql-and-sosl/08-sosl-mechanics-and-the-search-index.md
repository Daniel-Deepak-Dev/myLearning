# SOSL Mechanics & the Search Index

> Area: 10-soql-and-sosl · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 22

**Scope:** What SOSL is, how the search index differs from the database, and the `FIND` / `IN` / `RETURNING` statement. Relevance tuning and the `WITH` modifiers are [09](09-sosl-search-modifiers-and-relevance.md).

## Core idea

SOSL is not a variant of SOQL — **it is a different engine querying a different data store.** SOQL reads the database and evaluates field predicates. SOSL reads a **full-text search index** that the platform maintains asynchronously, and asks it which records contain a term. That single difference produces every practical consequence: SOSL can search many objects in one statement where SOQL cannot search two, it matches on word tokens rather than substrings, it returns results ranked by relevance rather than by a sort you specified, and **a record that was created moments ago may not be findable yet** because indexing has not caught up. The decision rule is short. Searching for a *value* in a known field is SOQL. Searching for *text* a human typed, across objects, is SOSL.

## How it works

- **The statement has three parts**, of which only `FIND` is required:

```apex
List<List<SObject>> results = [
    FIND 'acme' IN NAME FIELDS
    RETURNING Account(Id, Name WHERE BillingCountry = 'UK' ORDER BY Name LIMIT 10),
              Contact(Id, LastName), Lead(Id, Company)
];
List<Account> accounts = (List<Account>) results[0];   // positional, always
```

- **`IN <SearchGroup> FIELDS` narrows which fields are searched.** The five options are **`ALL FIELDS`** (the default when `IN` is omitted), **`NAME FIELDS`**, **`EMAIL FIELDS`**, **`PHONE FIELDS`** and **`SIDEBAR FIELDS`**. Narrowing is both a relevance and a performance decision.
- **`RETURNING` decides the shape of the result**, and each object may carry its own `WHERE`, `ORDER BY` and `LIMIT` — so one statement can search broadly and filter each object type differently.
- **The return type is `List<List<SObject>>`, indexed positionally in `RETURNING` declaration order.** An object with no matches yields an **empty inner list, not a missing one**, so the indexes never shift.
- **Wildcards work in the middle and at the end only.** `*` matches zero or more characters, `?` matches exactly one. **Neither may lead** — there is no way to ask "ends with".
- **The budget is separate from SOQL's and much smaller: 20 SOSL queries and 2,000 rows per transaction**, against SOQL's 100 and 50,000 → [02-apex · 01](../02-apex-and-triggers/01-apex-language-core-and-governor-limits.md).

## 2026 currency

SOSL's syntax is stable; what moved is the security context around it. **SOSL runs in user mode at 67.0 like everything else**, so results are filtered by the running user's sharing and FLS — and the honest framing is that this changed less for SOSL than for SOQL, because search has always been permission-filtered. The genuinely useful 67.0-era fact is a different one: **restriction rules apply to SOSL, search, lookups and related lists**, not only to SOQL, and **`View All Data` does not exempt you** from them. That makes search the place where a restriction rule is most likely to surprise someone, because the user experiences it as "the record does not exist" rather than as an access error. → [07-security · 11](../07-security-and-sharing/11-restriction-rules.md)

## Gotchas

- **The search term needs at least two characters.** A single character returns nothing rather than everything.
- **Indexing is asynchronous, so a just-created record may not be findable.** In tests this is absolute: **SOSL returns nothing in a test context unless you seed results with `Test.setFixedSearchResults()`** — the commonest reason a search-backed feature has passing tests and does not work.
- **Results are positional and empties are preserved.** Reading `results[1]` assuming it is the second *matching* object is wrong; it is the second *declared* object, matching or not.
- **A leading wildcard is not supported.** `FIND '*acme'` does not do what a `LIKE '%acme'` would, which is the one thing SOQL can express here and SOSL cannot.
- **SOSL matches whole tokens, not substrings.** Searching `acm` does not find `acme` without an explicit `acm*`.
- **These characters must be escaped with a backslash:** `? & | ! { } [ ] ( ) ^ ~ * : \ " ' + -`. Unescaped, they are operators and a user's literal `+` silently changes the query.
- **`ORDER BY` inside `RETURNING` orders within that object's list only** — there is no global ordering across the result lists, because relevance ranking is per object.

## Recall

Q: What is the fundamental difference between SOQL and SOSL?
A: SOQL queries the database with field predicates against one driving object; SOSL queries an asynchronously maintained full-text index and can search many objects at once.

Q: What are the five SOSL search groups, and which is the default?
A: `ALL FIELDS`, `NAME FIELDS`, `EMAIL FIELDS`, `PHONE FIELDS`, `SIDEBAR FIELDS`. `ALL FIELDS` applies when the `IN` clause is omitted.

Q: What does SOSL return, and how is it read?
A: `List<List<SObject>>` — one inner list per `RETURNING` clause in declaration order. Objects with no matches give an empty list rather than being omitted, so indexes are stable.

Q: Why does a SOSL-backed feature often pass its tests and fail in production, or vice versa?
A: Search results are not available in a test context unless seeded with `Test.setFixedSearchResults()`. And in production, asynchronous indexing means a newly created record may not be findable immediately.

Q: What are SOSL's governor limits?
A: 20 SOSL queries and 2,000 rows per transaction — a much smaller budget than SOQL's 100 queries and 50,000 rows.

## Related

- [09 · SOSL search modifiers & relevance](09-sosl-search-modifiers-and-relevance.md) — the `WITH` clauses, snippets, spell correction and how ranking is influenced
- [01 · Query anatomy & the SOQL model](01-query-anatomy-and-the-soql-model.md) — the engine SOSL is being contrasted with
- [07-security · 11 Restriction rules](../07-security-and-sharing/11-restriction-rules.md) — the access control that applies to search and that `View All Data` does not bypass
- [02-apex · 04 Dynamic SOQL, SOSL & describe in Apex](../02-apex-and-triggers/04-advanced-soql-sosl-and-dynamic-queries.md) — `Search.find()` and building a SOSL string at runtime
