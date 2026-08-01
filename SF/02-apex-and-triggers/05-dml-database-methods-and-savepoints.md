# DML, Database Methods & Savepoints

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 03

**Scope:** Writing data — the two DML syntaxes, per-row result handling, transaction control and Mixed DML. What the save itself then triggers is [07](07-order-of-execution-and-recursion.md); batching the writes is [08](08-bulkification-patterns.md).

## Core idea

Apex gives you the same six operations twice. The **DML statement** form — `insert accounts;` — is all-or-nothing: one bad row throws a `DmlException` and the entire transaction unwinds. The **`Database` method** form — `Database.insert(accounts, false)` — lets the good rows commit and hands you a per-row result describing what happened to the rest. Choosing between them is a business decision disguised as a syntax choice: does a partial success leave the org in a coherent state, or not? A 500-row import wants partial success and an error report. A two-record transfer between accounts does not. **Savepoints** are the third option for when you want to attempt something, inspect the outcome, and undo it — bounded by the fact that a rollback returns your data but not your governor budget.

## How it works

| | DML statement | `Database` method |
|---|---|---|
| Syntax | `insert cases;` | `Database.insert(cases, false)` |
| Partial failure | whole transaction rolls back | good rows commit, bad rows reported |
| Returns | nothing | `SaveResult[]`, positionally matched to the input |
| Throws | always, on any row failure | only when `allOrNone` is `true` |

- **`Database.Error` carries three things worth logging** — `getMessage()`, `getStatusCode()` (a `StatusCode` enum, matchable in code) and `getFields()` (the field API names that failed).
- **`upsert` keys on an External ID field**, or on `Id` if you omit one. Mark the field Unique as well, or an ambiguous match fails that row rather than choosing.
- **`Database.DMLOptions` carries the behaviour you cannot express in the operation** — running assignment rules, `allowSave` past a duplicate rule, suppressing the user email header, allowing field truncation.
- **`merge` is Account, Contact, Case and Lead only**, three records at a time — one master plus up to two — and it reparents children rather than deleting them.

```apex
Database.SaveResult[] results = Database.insert(cases, false);   // allOrNone = false
List<Load_Error__c> failures = new List<Load_Error__c>();
for (Integer i = 0; i < results.size(); i++) {
    if (results[i].isSuccess()) { continue; }
    for (Database.Error e : results[i].getErrors()) {
        failures.add(new Load_Error__c(
            Row__c     = i,
            Status__c  = String.valueOf(e.getStatusCode()),
            Message__c = e.getMessage(),
            Fields__c  = String.join(e.getFields(), ',')
        ));
    }
}
insert failures;
```

> **From my notes.** Savepoints are not free and the rollback is not a reset. **Setting a savepoint costs one DML statement, and rolling back costs another** — both against the same 150. More importantly, a rollback restores your *data* and nothing else: the SOQL queries and DML statements already spent stay spent, and static variables keep whatever they were set to. Treat a savepoint as a data undo, never as a way to retry your way out of a limit.

## 2026 currency

DML runs in **user mode by default** at 67.0, so `insert` now enforces the running user's object permissions and field-level security — code that wrote a field the user cannot edit used to succeed silently and now throws. Elevation is explicit: `Database.insert(records, false, AccessLevel.SYSTEM_MODE)`. The asymmetry to watch is that this applies to classes *compiled* at 67.0, so an untouched old class keeps the old behaviour until someone bumps its API version, at which point its write semantics change without its code changing. Detail and the team-convention argument in [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **Mixed DML.** Setup objects — `User`, `Group`, `GroupMember`, `PermissionSetAssignment`, `QueueSobject` — cannot be written in the same transaction as standard or custom objects. Split the second half into an async context; in tests, `System.runAs()` also creates the boundary.
- **Rolling back to an earlier savepoint invalidates every savepoint taken after it.** Using a stale one is a runtime error, not a no-op.
- **`SaveResult[]` is positional.** It matches the input list index for index, and that index is the only link back to the record that failed — `getId()` is null on a failed insert.
- **`allOrNone = false` does not make the operation safe**, only survivable. Something still has to decide what a half-applied change means.
- **`delete` is a soft delete** into the Recycle Bin and fires triggers; `Database.emptyRecycleBin()` and hard delete are separate, unrecoverable operations.
- **A DML statement inside a loop burns the 150-statement limit at one per iteration** — the single most common cause of a failed trigger. → [08](08-bulkification-patterns.md)
- **`undelete` restores children too**, which can resurrect records a later cleanup job assumed were gone.

## Recall

Q: What is the practical difference between `insert cases;` and `Database.insert(cases, false)`?
A: The statement form rolls the whole transaction back on any failure. The `Database` form commits the good rows and returns a `SaveResult` per row.

Q: How much of your governor budget does a savepoint cost?
A: One DML statement to set it and one to roll back — and the rollback does not return any budget already spent.

Q: Which objects trigger a Mixed DML exception?
A: Setup objects — `User`, `Group`, `GroupMember`, `PermissionSetAssignment`, `QueueSobject` — written in the same transaction as standard or custom objects.

Q: How do you find which input record a failed `SaveResult` belongs to?
A: By index — the results list matches the input list positionally. `getId()` is null for a failed insert.

Q: What does `Database.Error.getFields()` return?
A: The API names of the fields that caused the failure, alongside `getMessage()` and a matchable `getStatusCode()` enum.

## Related

- [09 · Exception handling & custom exceptions](09-exception-handling-and-custom-exceptions.md) — what to do with the errors a `SaveResult` hands back
- [08 · Bulkification patterns](08-bulkification-patterns.md) — collecting records so there is one DML statement left to make
- [01-admin · 13 Data import, export & loading tools](../01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md) — the same partial-success problem seen from a bulk load
