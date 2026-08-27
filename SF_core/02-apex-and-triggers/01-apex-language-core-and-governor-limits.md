# Apex Language Core & Governor Limits

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 03

**Scope:** The type system, collections, state model and the per-transaction limit map every later note in this area refers back to. Security defaults and the async contexts that reset these limits are phase 04 — see [INDEX](INDEX.md).

## Core idea

Apex is a strongly typed, object-oriented language running on Salesforce servers, and nearly every design decision in it follows from one fact: your code shares a machine with other tenants. **Governor limits** are how the platform enforces that. They are not performance advice — they are a runtime contract, counted per **transaction** and thrown as an uncatchable `LimitException` the moment you cross one. A transaction is a single synchronous execution context: one record save with all its triggers, one controller action, one Queueable, one `execute()` of a batch chunk. Everything inside shares one budget and the budget resets at the boundary, which means most Apex design is really a question of *where you put the boundary* — and which collections and static state keep you inside it.

## How it works

- **Three type families.** Primitives (`Integer`, `Decimal`, `String`, `Id`, `Date`, `Datetime`, `Blob`), sObjects, and collections. Use `Decimal` and never `Double` for money — `Double` is binary floating point and loses cents.
- **Pick the collection by the question you ask it.** `List` for order and duplicates, `Set` for membership and dedup, `Map` for keyed lookup. `new Map<Id, Account>([SELECT …])` builds an Id-keyed map in one expression and is the most load-bearing idiom in the language.
- **Static state lives for the transaction, not the class.** A `static` variable resets at every transaction boundary — the natural home for a recursion guard, and a trap when each batch chunk quietly gets a fresh one. → [07](07-order-of-execution-and-recursion.md)
- **Interface for a contract, abstract class for shared implementation.** `Queueable` and the Stub API both key off interfaces. A **wrapper class** — a small inner class with `@AuraEnabled` fields or `Comparable` — is how you return a shaped payload instead of an sObject.

| Per-transaction limit | Synchronous | Asynchronous |
|---|---|---|
| SOQL queries | 100 | 200 |
| Rows retrieved by SOQL | 50,000 | 50,000 |
| SOSL queries | 20 | 20 |
| Rows retrieved by SOSL | 2,000 | 2,000 |
| DML statements | 150 | 150 |
| Rows processed by DML | 10,000 | 10,000 |
| CPU time | 10,000 ms | 60,000 ms |
| Heap size | 6 MB | 12 MB |
| Callouts | 100 | 100 |
| Cumulative callout timeout | 120 s | 120 s |
| Queueable jobs enqueued | 50 | 1 |
| Trigger stack depth | 16 | 16 |

- **Read the budget at runtime rather than guessing it.** Every row above has a `Limits.getX()` / `Limits.getLimitX()` pair, which is what lets a job degrade instead of dying:

```apex
// Optional enrichment only if there is headroom; otherwise finish it asynchronously
if (Limits.getQueries() < Limits.getLimitQueries() - 5
    && Limits.getCpuTime() < Limits.getLimitCpuTime() / 2) {
    enrich(records);
} else {
    System.enqueueJob(new EnrichmentJob(new Map<Id, Account>(records).keySet()));
}
```

## 2026 currency

The limit map itself is stable — nothing in it moved at 67.0. What moved is the **execution context** it applies to: SOQL now runs in user mode by default, so a query returns only rows the running user can see and consumes only those against your 50,000. The same code can therefore draw a different amount of budget in two orgs with different sharing models, which makes limit testing as an admin genuinely misleading. Detail in [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **`LimitException` is uncatchable.** `catch (Exception e)` will not save you — the platform is protecting other tenants, not your transaction. Check `Limits` *before* the work.
- **CPU time excludes waiting.** Database time, callout time and DML processing do not count; loops and collection manipulation do. A slow transaction is not necessarily a CPU-limit transaction.
- **Heap measures what is still reachable**, so a `List<sObject>` you have finished with keeps its memory until the reference goes out of scope.
- **SOSL is 20 queries and 2,000 rows** — reaching for it to dodge the 100-query SOQL limit trades one ceiling for a much lower one.
- **`Integer / Integer` truncates silently.** Use `Decimal` operands, or `Decimal.divide(value, scale)` where you need a defined scale.
- **`Map` keys are case-sensitive; SOQL comparisons are not.** Keying a map on `Name` and expecting it to match a query result is a classic silent miss — key on `Id` or normalise the case explicitly.

## Recall

Q: What is the per-transaction SOQL query limit, and how does it differ asynchronously?
A: 100 synchronous, 200 asynchronous — with the same 50,000-row ceiling either way.

Q: Why can't you catch a governor limit failure?
A: `LimitException` is uncatchable by design. Read the `Limits` class and degrade before you hit the ceiling instead.

Q: What resets a static variable?
A: The transaction boundary — not the class, not the method. Each batch chunk and each Queueable starts with fresh statics.

Q: Does CPU time include the time a callout spends waiting for a response?
A: No. Callout, database and DML processing time are all excluded; CPU time measures your own code's work.

Q: Why is `Double` the wrong type for a currency amount?
A: It is binary floating point, so it cannot represent most decimal fractions exactly and loses cents. Use `Decimal`.

## Related

- [08 · Bulkification patterns](08-bulkification-patterns.md) — the patterns that keep a transaction inside this budget
- [09 · Exception handling & custom exceptions](09-exception-handling-and-custom-exceptions.md) — what is catchable, what isn't, and what to do about it
- [04-flow · INDEX](../04-flow-and-automation/INDEX.md) — flows draw on this same per-transaction budget, so a save can exhaust it before your Apex runs
