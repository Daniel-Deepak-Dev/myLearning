# Async Apex Overview & Choosing

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 04

**Scope:** The five asynchronous mechanisms, what each is actually for, and the limits they share. Each has its own note — [13](13-queueable-apex-and-chaining.md) to [16](16-transaction-finalizers.md) and [18](18-platform-events-and-cdc-in-apex.md); this one is the decision.

## Core idea

Going async is not a way to get more governor budget — it is a way to get **another transaction**, which comes with its own budget and its own failure. That trade is the whole subject. You gain fresh limits, higher async ceilings, and the ability to do work the user should not wait for; you lose the ability to tell that user what happened, to roll their save back if it fails, and to reason about ordering. So the question is never "should this be async" in the abstract. It is: does this work have to be atomic with the user's save? If yes, it stays synchronous and must fit. If no, the choice among the five mechanisms follows from the *shape* of the work — one deferred unit, a job needing typed state, a data set larger than one transaction, a clock, or a fan-out to subscribers you do not control.

## How it works

| Mechanism | Shape of work it fits | Typed state | Chaining | Callouts |
|---|---|---|---|---|
| `@future` | legacy — one fire-and-forget unit | primitives only | no | `(callout=true)` |
| **Queueable** | the default async choice | any member variable | yes, one child | `Database.AllowsCallouts` |
| Batch | a record set too large for one transaction | `Database.Stateful` | from `finish()` | `Database.AllowsCallouts` |
| Schedulable | "at 02:00 every night" | member variables | usually starts a batch | not directly |
| Platform Event | fan-out to unknown subscribers | the event payload | n/a | in the subscriber |

- **The daily async ceiling is shared across all of them**: 250,000 executions per 24 hours, or 200 × your user licences, whichever is greater. `@future` calls, Queueable jobs, batch chunks and scheduled runs all draw on the same pool.
- **Async transactions get bigger limits, not unlimited ones** — 200 SOQL queries instead of 100, 12 MB heap instead of 6, 60,000 ms CPU instead of 10,000. The 150-DML-statement limit does not change. → [01](01-apex-language-core-and-governor-limits.md)
- **Only 100 unstarted jobs sit in the flexible queue.** Beyond that, `System.enqueueJob` throws — a burst of trigger-driven enqueues is a real way to hit it.
- **`AsyncApexJob` is the audit trail** for everything except platform events, and it is queryable, so a monitoring page or a failure alert is a SOQL query rather than a support ticket.

```apex
// What actually failed last night, without opening Setup → Apex Jobs.
List<AsyncApexJob> broken = [
    SELECT Id, JobType, ApexClass.Name, Status, ExtendedStatus,
           NumberOfErrors, TotalJobItems, CompletedDate
    FROM AsyncApexJob
    WHERE Status IN ('Failed', 'Aborted') AND CreatedDate = LAST_N_DAYS:1
    ORDER BY CompletedDate DESC
];
```

## 2026 currency

**Elastic limits for async jobs are in Beta at 67.0**: `Queueable` and `@future` jobs can be enqueued up to *twice* the licensed daily limit, with the overflow throttled rather than rejected. That changes the failure mode from a hard `LimitException` at the enqueue site to slower execution, which is better for the user and worse for anyone who was relying on the exception as a signal that something had gone into a loop. Track it with `DailyAsyncApexElasticExecutions` and `DailyAsyncApexProcessed` in `System.OrgLimits.getMap()` rather than assuming headroom. Beta status and sources: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

## Gotchas

- **Async is not a limit reset for the transaction that queued it.** Enqueuing costs you nothing back — the synchronous transaction still has to finish inside its own budget.
- **`@future` cannot take an sObject argument.** Pass a `Set<Id>` and re-query; passing serialized records means acting on data that may already be stale.
- **You cannot call `@future` from `@future`, or from a batch `execute()` beyond one call.** Async contexts are allowed exactly one enqueue each. → [13](13-queueable-apex-and-chaining.md)
- **Async work runs as the user who queued it**, but with no UI to surface the failure — an unhandled exception produces an email to the last person who edited the class, which is nobody's monitoring strategy. → [16](16-transaction-finalizers.md)
- **`Test.startTest()`/`stopTest()` runs queued async work synchronously**, so tests never exercise ordering, delay or concurrency. A passing test proves the code runs, not that the design is sound.
- **Mixed DML rules still apply per transaction** — moving the second half of a save into async is the standard fix, and the async job then has the same restriction internally. → [05](05-dml-database-methods-and-savepoints.md)
- **There is no ordering guarantee between independent async jobs.** Two Queueables enqueued in sequence are not guaranteed to run in that sequence; if order matters, chain them.

## Recall

Q: What do you actually gain by moving work into an async context?
A: A separate transaction with its own governor budget and higher async ceilings — at the cost of atomicity with the user's save and any ability to report back synchronously.

Q: What is the daily async execution limit, and which mechanisms draw on it?
A: 250,000 or 200 × user licences per 24 hours, whichever is greater — shared across `@future`, Queueable, batch chunks and scheduled Apex.

Q: How many unstarted jobs can the flexible queue hold?
A: 100. Past that, `System.enqueueJob` throws rather than queueing.

Q: Why can't `@future` take an sObject parameter?
A: It only accepts primitives and collections of primitives. Pass IDs and re-query inside the method, which also avoids acting on stale field values.

Q: What do async transactions get that synchronous ones don't?
A: 200 SOQL queries, 12 MB heap and 60,000 ms CPU. The DML statement limit stays at 150.

## Related

- [13 · Queueable Apex & chaining](13-queueable-apex-and-chaining.md) — the default choice, and why `@future` is not
- [01 · Apex language core & governor limits](01-apex-language-core-and-governor-limits.md) — the synchronous limit map these ceilings are measured against
- [04-flow · Flow at scale](../04-flow-and-automation/INDEX.md) — the declarative side of the same deferral decision, including scheduled paths
