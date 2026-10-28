---
vault: SF_core
area: 02-apex-and-triggers
format: dense
status: learning
created: 2026-08-02
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 4
---
# Async Apex Overview & Choosing

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
- **Async transactions get bigger limits, not unlimited ones** — 200 SOQL queries instead of 100, 25 MB heap instead of 10 (12 and 6 before Winter '27), 60,000 ms CPU instead of 10,000. The 150-DML-statement limit does not change. → [01](01-apex-language-core-and-governor-limits.md)
- **The Apex flex queue holds 100 batch jobs in `Holding` status.** Beyond that, `Database.executeBatch` throws a `LimitException` — a burst of trigger-driven batch submissions is a real way to hit it.
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

**Elastic limits for async jobs are still Beta at 68.0, off by default, and Winter '27 extended them to Batch Apex.** With *Use elastic limits for asynchronous Apex jobs (Beta)* turned on in Apex Settings, `Queueable`, `@future` and batch jobs can be enqueued past the licensed daily limit, by that limit again or 2 million, whichever is less. The overflow is throttled rather than rejected; scheduled jobs stay capped. That changes the failure mode from a hard `LimitException` at the enqueue site to slower execution, which is better for the user and worse for anyone who was relying on the exception as a signal that something had gone into a loop. Track it with `DailyAsyncApexExecutions` and `DailyAsyncApexElasticExecutions` in `System.OrgLimits.getMap()` rather than assuming headroom; the elastic key is absent while the setting is off. A sandbox gets no elastic headroom, so testing it needs the 68.0 `asyncApexExecutionsOverride` set below the licensed limit. Beta status and sources: [RELEASE-RADAR/developer-tooling-and-apis.md](../../RELEASE-RADAR/developer-tooling-and-apis.md).

## Gotchas

- **Async is not a limit reset for the transaction that queued it.** Enqueuing costs you nothing back — the synchronous transaction still has to finish inside its own budget.
- **`@future` cannot take an sObject argument.** Pass a `Set<Id>` and re-query; passing serialized records means acting on data that may already be stale.
- **You cannot call `@future` from `@future` or from batch Apex at all** — the limit is 0 in both contexts, 50 from a Queueable. Any async context may add only one Queueable with `System.enqueueJob`. → [13](13-queueable-apex-and-chaining.md)
- **Async work runs as the user who queued it**, but with no UI to surface the failure — an unhandled exception produces an email to the last person who edited the class, which is nobody's monitoring strategy. → [16](16-transaction-finalizers.md)
- **`Test.startTest()`/`stopTest()` runs queued async work synchronously**, so tests never exercise ordering, delay or concurrency. A passing test proves the code runs, not that the design is sound.
- **Mixed DML rules still apply per transaction** — moving the second half of a save into async is the standard fix, and the async job then has the same restriction internally. → [05](05-dml-database-methods-and-savepoints.md)
- **There is no ordering guarantee between independent async jobs.** Two Queueables enqueued in sequence are not guaranteed to run in that sequence; if order matters, chain them.

## Recall

Q: What do you actually gain by moving work into an async context?
A: A separate transaction with its own governor budget and higher async ceilings — at the cost of atomicity with the user's save and any ability to report back synchronously.

Q: What is the daily async execution limit, and which mechanisms draw on it?
A: 250,000 or 200 × user licences per 24 hours, whichever is greater — shared across `@future`, Queueable, batch chunks and scheduled Apex.

Q: How many unstarted jobs can the Apex flex queue hold?
A: 100 batch jobs in `Holding` status. Past that, `Database.executeBatch` throws a `LimitException` rather than queueing.

Q: Why can't `@future` take an sObject parameter?
A: It only accepts primitives and collections of primitives. Pass IDs and re-query inside the method, which also avoids acting on stale field values.

Q: What do async transactions get that synchronous ones don't?
A: 200 SOQL queries, 25 MB heap and 60,000 ms CPU. The DML statement limit stays at 150.

## Related

- [13 · Queueable Apex & chaining](13-queueable-apex-and-chaining.md) — the default choice, and why `@future` is not
- [01 · Apex language core & governor limits](01-apex-language-core-and-governor-limits.md) — the synchronous limit map these ceilings are measured against
- [04-flow · Flow at scale](../04-flow-and-automation/INDEX.md) — the declarative side of the same deferral decision, including scheduled paths

## Sources

- [Apex Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_apex_developer_guide.pdf) — Salesforce Developers · read 2026-10-28 · heap 10 MB / 25 MB; Elastic Limits for Asynchronous Apex Jobs (Beta): covers Batch, Queueable and future, *"Scheduled jobs remain capped"*, formula `DailyAsyncApexExecutions + min(licensed, 2000000)`, no elastic capacity in non-production orgs; flex queue: *"If the Apex flex queue has the maximum number of 100 jobs, Database.executeBatch throws a LimitException"*; *"Methods declared as future can't be called from a batch Apex class"*
- [Metadata API Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_meta.pdf) — Salesforce Developers · read 2026-10-28 · ApexSettings `enableAsyncApexElasticExecutions` (default `false`, API 67.0) and `asyncApexExecutionsOverride` (non-production only, API 68.0)
- [REST API Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_rest.pdf) — Salesforce Developers · read 2026-10-28 · org limit names `DailyAsyncApexExecutions` and `DailyAsyncApexElasticExecutions`; no `DailyAsyncApexProcessed`
- [Winter '27 Release Architect Highlights](https://www.salesforce.com/blog/winter-27-release-architect-highlights/) — Salesforce Architecture Blog · read 2026-10-28 · Elastic Async Apex Jobs (Beta) *"now covers batch jobs"*; cap is the licensed limit or 2 million, whichever is lower; heap 6 → 10 MB and 12 → 25 MB

## History

- 2026-10-28 · Winter '27 currency check: heap 12/6 → 25/10 MB; elastic limits still Beta, now cover batch, opt-in, 2 million cap; replaced the non-existent `DailyAsyncApexProcessed`; corrected the flex-queue and `@future`-from-batch claims
