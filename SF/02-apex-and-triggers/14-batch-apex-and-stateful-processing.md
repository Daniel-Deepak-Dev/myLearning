# Batch Apex & Stateful Processing

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 04

**Scope:** Processing a record set larger than one transaction can hold — the three-method contract, scope sizing, carrying state across chunks and surviving partial failure. Paging a large result set *inside* one transaction is [17](17-database-cursor-and-large-result-sets.md) instead.

## Core idea

Batch Apex splits one logical job across many transactions so that no single one has to fit inside a governor limit. The contract is three methods and one idea: `start()` describes the whole set, `execute()` is called repeatedly with a slice of it, and `finish()` runs once at the end. Each `execute()` is a genuinely separate transaction with a fresh budget, which is what makes 50 million records tractable — and also what makes the design work harder than it looks, because *separate transaction* means separate rollback. A chunk that fails takes only itself down. The job continues, completes, and reports success with an error count buried in `AsyncApexJob`, so "did the batch run" and "did the batch work" are two different questions.

## How it works

| Piece | Runs | Notes |
|---|---|---|
| `start(bc)` | once | returns `Database.QueryLocator` (up to **50 M** rows) or `Iterable<sObject>` (capped at 50,000) |
| `execute(bc, scope)` | once per chunk | own transaction, own limits; `scope` is 1–2000 records, default 200 |
| `finish(bc)` | once | own transaction — send the summary, or chain the next batch |
| `Database.Stateful` | — | **instance** members persist across chunks; statics still reset |
| `Database.RaisesPlatformEvents` | — | publishes a `BatchApexErrorEvent` per failed chunk |

- **`Database.executeBatch(job, scopeSize)` is the only tuning knob that matters.** Lower it when each record is expensive (callouts, deep queries, heavy triggers); raise it when the work is cheap and the per-transaction overhead dominates.
- **Five batch jobs can be queued or active at once.** Further submissions go to `Holding` status — up to 100 — rather than throwing, which is a queue you can silently fill.
- **`BatchApexErrorEvent` is how you find out about a failed chunk without reading a log.** Declare `Database.RaisesPlatformEvents`, write a trigger on the event, and each failure arrives with the job ID, the exception and the chunk's record IDs. `Database.AllowsCallouts` is the other marker interface worth knowing — it permits HTTP from `execute()`. → [18](18-platform-events-and-cdc-in-apex.md)

```apex
public class ArchiveOrders implements Database.Batchable<sObject>, Database.Stateful,
                                      Database.RaisesPlatformEvents {
    public Integer archived = 0;              // survives every chunk; a static would not

    public Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id FROM Order WHERE Status = 'Closed' AND CloseDate < LAST_N_YEARS:2
            WITH SYSTEM_MODE                  // nightly job — no running user to defer to
        ]);
    }
    public void execute(Database.BatchableContext bc, List<Order> scope) {
        archived += archive(scope).size();
    }
    public void finish(Database.BatchableContext bc) { summarise(archived); }
}
```

> **From my notes.** The most useful measurement I ever took: iterating 450 records through a **SOQL for-loop** held heap flat at roughly **1050 → 1200 bytes**, while assigning the same query to a `List` pushed it **1050 → 20000**. The mechanism is that a SOQL for-loop pulls records in internal batches of 200 and lets the previous batch become garbage, so only one batch is live at a time; a list holds every record at once. Still true, and still the cheapest heap fix there is — with one qualification the note did not make: inside a batch `execute()` the scope list is already bounded, so the trick applies to any *additional* query you run in that method, not to the scope itself.

## 2026 currency

Batch is not exempt from the 67.0 security flip. The `QueryLocator` built in `start()` runs in **user mode** by default like everything else, which for a nightly job running as a low-privilege automation user means the scope quietly shrinks rather than erroring — the job succeeds, having processed a subset. Decide the mode explicitly in `start()` (`WITH SYSTEM_MODE`, or the `AccessLevel` argument on `Database.getQueryLocatorWithBinds`) and treat an unqualified locator in a scheduled job as a review finding. Background: [10](10-apex-security-user-mode-and-fls.md) and [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **`Database.Stateful` preserves instance members only.** Static variables reset with every chunk — the single most common reason a "running total" comes out equal to the last chunk's count.
- **A failed chunk does not fail the job.** The job reaches `Completed` with `NumberOfErrors` greater than zero, so monitoring that checks `Status` alone reports success on a half-finished run.
- **Chunk order is not guaranteed** and neither is parallelism. Anything that depends on chunk *n* finishing before chunk *n+1* needs chaining, not batching.
- **`Iterable<sObject>` in `start()` throws away the 50-million ceiling** — it is evaluated as an ordinary query and hits the 50,000-row limit. Use it only for genuinely computed sets.
- **Scope size and trigger batch size are different numbers.** A scope of 2000 still fires triggers in chunks of 200, so a DML in `execute()` runs the trigger ten times with the trigger's own limits in play.
- **State carried in `Database.Stateful` is serialized between chunks**, so a growing `Map` in state costs heap in every transaction and eventually kills the job that was supposed to avoid heap problems.
- **A batch whose `execute()` updates records its own locator selected** can reprocess or skip rows — the locator is a cursor over live data, not a snapshot.

## Recall

Q: How many records can `start()` return, and what changes that number?
A: 50 million from a `Database.QueryLocator`. Returning an `Iterable<sObject>` drops it to the ordinary 50,000-row query limit.

Q: What exactly does `Database.Stateful` preserve?
A: Instance member variables across `execute()` calls. Static variables still reset at every transaction boundary.

Q: How do you learn that a chunk failed without reading debug logs?
A: Implement `Database.RaisesPlatformEvents` and write a trigger on `BatchApexErrorEvent` — each failure carries the job ID, exception and the chunk's record IDs.

Q: How many batch jobs can be queued or active at once?
A: Five. Additional submissions sit in `Holding` status, up to 100, rather than throwing.

Q: Why does a nightly batch suddenly process fewer records at API 67.0?
A: Its `QueryLocator` defaults to user mode, so the scope is filtered by the running user's access. Declare `WITH SYSTEM_MODE` if the job is meant to see everything.

## Related

- [17 · `Database.Cursor` & large result sets](17-database-cursor-and-large-result-sets.md) — the same problem solved inside a single transaction
- [12 · Async Apex overview & choosing](12-async-apex-overview-and-choosing.md) — when the record set is not actually the reason to go async
- [08-data · 08 Indexes & query selectivity](../08-data-modeling-and-large-data-volumes/08-indexes-and-query-selectivity.md) — making the `QueryLocator` selective at the volumes that make batch necessary
- [30 · Custom iterators & iterables](30-custom-iterators-and-iterables.md) — writing the `Iterable` that `start()` accepts when the scope is not a query, and the 50 K ceiling that comes with it
