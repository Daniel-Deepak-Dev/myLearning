# Bulkification Patterns

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 03

**Scope:** Writing Apex that costs the same whether it processes one record or two hundred. The limits being defended are [01](01-apex-language-core-and-governor-limits.md); the DML end of it is [05](05-dml-database-methods-and-savepoints.md).

## Core idea

Bulkification is one rule with several shapes: **the cost of a transaction must not scale with the number of records in it.** A query inside a loop costs one of your 100 queries per record, so it works perfectly in the sandbox where you tested it with one record and fails on the first real import. The fix is always the same three moves — collect the keys, do the expensive thing once outside the loop, then look the results up inside it. What makes this a discipline rather than a tip is that you never get to choose the batch size. A trigger receives up to 200 records whether a user clicked Save or Data Loader sent 50,000, so every handler must be written as though the large case is the normal one, because eventually it is.

## How it works

| Antipattern | What it burns | The fix |
|---|---|---|
| SOQL inside a `for` | 100 queries | collect Ids, one query with `IN :ids` |
| DML inside a `for` | 150 statements | collect into a `List`, one DML after |
| `List` holding a large result set | 6 MB heap | SOQL `for` loop, chunked at 200 |
| Counting children per record | queries and CPU | `COUNT(Id)` with `GROUP BY` |
| Re-reading the same parent | queries | `Map<Id, sObject>` built once |

- **Collect into a `Set`, not a `List`.** Two hundred opportunities may point at three accounts; a `Set<Id>` deduplicates before the query so you fetch three rows instead of two hundred.
- **`new Map<Id, Account>([SELECT …])` is the workhorse.** It turns a query straight into an O(1) lookup, and the map constructor keys on `Id` automatically:

```apex
Set<Id> accountIds = new Set<Id>();
for (Opportunity o : Trigger.new) {
    if (o.AccountId != null) { accountIds.add(o.AccountId); }
}
// one query, outside the loop, keyed for lookup inside it
Map<Id, Account> accounts = new Map<Id, Account>([
    SELECT Id, Rating FROM Account WHERE Id IN :accountIds
]);
for (Opportunity o : Trigger.new) {
    o.Priority__c = accounts.get(o.AccountId)?.Rating == 'Hot' ? 'P1' : 'P3';
}
```

- **For children, group into a `Map<Id, List<SObject>>`** keyed by the parent Id, in one pass over one query. The inner list has to be created on first touch — a missing key returns null, not an empty list.
- **A parent-to-child subquery replaces the second query entirely** when you need both sides: `SELECT Id, (SELECT Amount FROM Opportunities) FROM Account WHERE Id IN :ids`. → [03](03-soql-fundamentals-and-relationship-queries.md)
- **Bulkification is not a trigger concern.** An `@InvocableMethod` receives a `List` and a Queueable can be enqueued per chunk for exactly the same reason.

## 2026 currency

The patterns are unchanged, but user-mode SOQL gives one of them a new failure mode. A bulk query now returns only the rows the running user can see, so `accounts.get(o.AccountId)` can come back null because of **sharing**, not because of missing data — for the same code, the same records, and a different user. Null-handling in a bulk lookup has therefore stopped being defensive coding and become a genuine branch you need a decision for: skip the record, `addError()` it, or elevate that one query with `AccessLevel.SYSTEM_MODE` and document why. Context in [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **200 is the trigger chunk, not the ceiling.** `Database.update` can process 10,000 rows in one statement, so a handler called directly must be bulk-safe on its own terms.
- **`Map.get()` on a missing key returns null**, silently. Safe-navigate it or branch on it — never assume the query returned every Id you asked for.
- **A `Map<Id, List<Child>>` needs its inner list initialised** before the first `add()`, or you get a `NullPointerException` on the first child of every parent.
- **`Trigger.new` has no Ids in `before insert`**, so an Id-keyed map is impossible there. Key on an External Id or a composite of field values instead.
- **Nested loops over two collections are quadratic** and hit CPU time long before they hit a query limit — 200 × 200 is 40,000 iterations for one save.
- **A SOQL `for` loop keeps heap flat but still consumes rows** against the 50,000 limit. It solves memory, not budget.
- **Aggregate queries do not respect `Trigger.new` ordering**, so match results back by key rather than by position.

## Recall

Q: What is the single rule bulkification expresses?
A: The cost of a transaction must not scale with the number of records in it — queries and DML stay constant as the batch grows.

Q: Why collect Ids into a `Set` rather than a `List` before querying?
A: It deduplicates, so 200 child records pointing at three parents fetch three rows instead of 200.

Q: How many records does a trigger receive at once, and what does that imply?
A: Up to 200 per invocation — so a large load calls the handler repeatedly, and the handler must be correct for both one record and 200.

Q: What does `Map.get()` return for a key that isn't present?
A: Null. Not an exception, not an empty value — which at 67.0 can mean "no such record" or "the running user can't see it".

Q: Which pattern replaces querying children once per parent?
A: A parent-to-child subquery, or one query over the children grouped into a `Map<Id, List<SObject>>`.

## Related

- [01 · Apex language core & governor limits](01-apex-language-core-and-governor-limits.md) — the per-transaction budget every pattern here defends
- [05 · DML, Database methods & savepoints](05-dml-database-methods-and-savepoints.md) — handling per-row failures once the collected list is written
- [09-devops · INDEX](../09-devops-sfdx-and-release-management/INDEX.md) — Code Analyzer catches SOQL-in-loop in the pipeline, before a reviewer has to
