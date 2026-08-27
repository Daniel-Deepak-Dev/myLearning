# Dynamic SOQL, SOSL & Describe in Apex

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 03 *(narrowed in phase 22)*

**Scope:** The **Apex API** for querying at runtime — `Database.query` / `queryWithBinds` / `AccessLevel`, `Search.find()`, and schema describe. **The languages themselves are [10-soql](../10-soql-and-sosl/INDEX.md)**: traversal and `TYPEOF` are [· 04](../10-soql-and-sosl/04-relationship-queries-in-depth.md), semi-joins [· 06](../10-soql-and-sosl/06-semi-joins-anti-joins-and-set-filtering.md), injection defence [· 07](../10-soql-and-sosl/07-dynamic-soql-and-injection-defence.md), SOSL [· 08–09](../10-soql-and-sosl/08-sosl-mechanics-and-the-search-index.md). Static queries from Apex are [03](03-soql-fundamentals-and-relationship-queries.md).

## Core idea

Everything here exists because the query cannot be written as a literal. Sometimes the *shape* is unknown until runtime — a filter builder, a configurable report, an agent action taking arbitrary criteria. Sometimes the *schema* is unknown, and the code must discover fields it was never compiled against, which is describe. The unifying consequence is that **the moment a query stops being a literal, the compiler stops protecting you**: no field validation, no type checking, and an injection surface. Apex's answer is a small API — a query method that takes binds from a map and an explicit access level, a `Search` class for SOSL, and a describe layer for asking the schema what exists. Knowing which of those three you need is most of the work.

## How it works

- **`Database.queryWithBinds(query, bindMap, AccessLevel)`** is the modern entry point. Binds resolve from the map **by key**, not from Apex locals, which removes the old scoping surprise where a bind silently picked up a variable from an enclosing block:

```apex
Map<String, Object> binds = new Map<String, Object>{ 'name' => input };
List<Account> safe = Database.queryWithBinds(
    'SELECT Id, Name FROM Account WHERE Name = :name', binds, AccessLevel.USER_MODE);
```

- **`Database.query()`** is the older form and resolves `:variable` against Apex scope. Still supported; prefer `queryWithBinds` for anything taking input.
- **`Database.getQueryLocatorWithBinds()`** is the batch-facing twin, for a `start()` method whose query is assembled at runtime → [14](14-batch-apex-and-stateful-processing.md).
- **`Search.find()` and `Search.query()`** run SOSL dynamically, returning `Search.SearchResults` or `List<List<SObject>>`.
- **Describe reads the schema at runtime** — `Schema.SObjectType.Account.fields.getMap()`, `getDescribe().getPicklistValues()`, `Type.forName()` — which is how a generic component discovers fields, and how an identifier allowlist stays honest → [10-soql · 07](../10-soql-and-sosl/07-dynamic-soql-and-injection-defence.md).

> **From my notes.** The dependent-picklist recipe: each entry returned by `getPicklistValues()` carries a **`validFor`** key in its serialised form — a base64-encoded bitmap of which controlling values enable that entry. Decode with `EncodingUtil.base64Decode()` and test the bit at the controlling value's index. Still the only way to read the dependency from Apex, still undocumented, and still worth a comment in the code saying so.

## 2026 currency

`Database.query()` and `Database.queryWithBinds()` now default to **user mode**, so a dynamic query enforces the running user's FLS and sharing unless you pass `AccessLevel.SYSTEM_MODE` deliberately. `WITH SECURITY_ENFORCED` **no longer compiles** — anything found using it inside a dynamic query string is dead code and should become `WITH USER_MODE` or an explicit `AccessLevel`. Two Winter '25 improvements land specifically on this API: **invalid dynamic SOQL now returns specific error messages** rather than a generic parse failure, and **negative currency values are supported** in dynamic and API-issued queries. Winter '25 also added **SOQL stub methods for mocking external-object query responses** in Apex tests, which is the first way to test a Salesforce Connect-backed query without the remote system → [21](21-apex-testing-advanced-and-mocking.md). → [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md)

## Gotchas

- **`Database.query()` with a literal string is still dynamic** — not compile-checked even when nothing is concatenated in, so a typo deploys cleanly and fails at runtime.
- **`queryWithBinds` throws if a bind named in the string is missing from the map**, rather than binding null. The message names the key.
- **A bind cannot substitute an identifier.** Object names, field names and clause keywords must be assembled from values you control, and that means an allowlist → [10-soql · 07](../10-soql-and-sosl/07-dynamic-soql-and-injection-defence.md).
- **`Schema.getGlobalDescribe()` builds a map of every object in the org** — real CPU and heap cost. Prefer `Type.forName()` or a named `Schema.SObjectType`.
- **Describe results are cached per transaction, not across them**, so a "cheap second call" is only cheap inside the same execution context.
- **`Search.find()` returns nothing in a test context** unless seeded with `Test.setFixedSearchResults()` → [10-soql · 08](../10-soql-and-sosl/08-sosl-mechanics-and-the-search-index.md).
- **`AccessLevel.USER_MODE` on a dynamic query does not make injection safe** — it bounds the damage to what the attacker can already see, which in a portal context can still be substantial.

## Recall

Q: What are the two arguments to `Database.queryWithBinds` beyond the query string?
A: A `Map<String, Object>` of bind values keyed by name, and an `AccessLevel` — `USER_MODE` or `SYSTEM_MODE`.

Q: How does `queryWithBinds` differ from `Database.query` in how binds resolve?
A: It resolves them from the map by key. `Database.query` resolves `:variable` against Apex scope, which could silently capture a variable from an enclosing block.

Q: What is `validFor` and what is it for?
A: A base64-encoded bitmap on each picklist entry recording which controlling values enable it — the only way to read a dependent picklist's dependency from Apex, and undocumented.

Q: Why avoid `Schema.getGlobalDescribe()`?
A: It builds a map of every object in the org, costing real CPU and heap. A named `Schema.SObjectType` or `Type.forName()` gets one object instead.

Q: What happens to `Search.find()` inside a test?
A: It returns nothing unless the test seeds results with `Test.setFixedSearchResults()`.

## Related

- [10-soql · 07 Dynamic SOQL & injection defence](../10-soql-and-sosl/07-dynamic-soql-and-injection-defence.md) — **the reference for injection defence**: binds cover values, identifiers need an allowlist
- [10-soql · 08 SOSL mechanics & the search index](../10-soql-and-sosl/08-sosl-mechanics-and-the-search-index.md) — the search groups, `RETURNING`, wildcards and escaping behind `Search.find()`
- [03 · SOQL in Apex](03-soql-fundamentals-and-relationship-queries.md) — the governor budget and the `for` loop these build on
- [28 · Dependency injection & pluggable Apex](28-dependency-injection-and-pluggable-apex.md) — `Type.forName()` again, used to choose an implementation rather than a field
