# `Database.Cursor` & Large Result Sets

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 04

**Scope:** Walking a result set too large to hold, without the ceremony of a batch class. The batch alternative is [14](14-batch-apex-and-stateful-processing.md); the chain that usually carries a cursor is [13](13-queueable-apex-and-chaining.md).

## Core idea

A cursor is a server-side handle to a query's results that you page through yourself. `Database.getCursor()` runs the query and hands back an object with two useful methods — `getNumRecords()` and `fetch(position, count)` — and that object can be stored in a Queueable's member variables and survive into the next transaction. That is the whole value: chunking under your own control, in ordinary Apex, without writing a `Database.Batchable`. It fills the gap between "this fits in a list" and "this needs a batch job", and it is the right answer when the *processing* is naturally sequential or resumable but the record count is too high for one transaction. What a cursor is emphatically **not** is a way around the per-transaction row limit — that misreading is the main trap in the topic.

## How it works

| | plain `[SELECT …]` | `Database.QueryLocator` | `Database.Cursor` |
|---|---|---|---|
| Usable where | anywhere | batch `start()` | anywhere, across transactions |
| Total rows | 50,000 per transaction | 50 M per job | 50 M per cursor |
| Chunking | none | platform, via scope size | yours, via `fetch(position, count)` |
| Lifetime | the statement | the job | **2 days** |
| Query cost | 1 | 1 | **1 per `fetch()`** |

- **Creation takes an access level.** `Database.getCursor(soql, accessLevel)` and `Database.getCursorWithBinds(soql, binds, accessLevel)` — user mode by default at 67.0, like every other query. → [10](10-apex-security-user-mode-and-fls.md)
- **Cursors are stateless and offset-based.** The set of record IDs is fixed when the cursor is created; `fetch()` just reads from an offset, so nothing is held open between calls.
- **The pagination variant is a different object for a different job.** `Database.getPaginationCursor()` returns a `PaginationCursor` whose `fetchPage(start, pageSize)` yields a `Database.CursorFetchResult` with `getRecords()`, `getDeletedRows()`, `getNextIndex()` and `isDone()` — it skips deleted rows so page sizes stay stable for a UI, at the cost of a 100,000-row ceiling per instance.
- **Two exception types, and the difference matters.** `System.TransientCursorException` means retry; `System.FatalCursorException` does not.

```apex
public class ContactSweep implements Queueable {
    private final Database.Cursor cursor;              // survives the transaction; 2-day lifetime
    private final Integer position;
    public ContactSweep(Database.Cursor c, Integer p) { cursor = c; position = p; }

    public void execute(QueueableContext ctx) {
        List<Contact> scope = (List<Contact>) cursor.fetch(position, 200);  // 1 query, 200 rows
        process(scope);
        if (position + 200 < cursor.getNumRecords()) {
            System.enqueueJob(new ContactSweep(cursor, position + 200));    // resume, don't restart
        }
    }
}
// Database.getCursor('SELECT Id, Email FROM Contact WHERE …', AccessLevel.USER_MODE)
```

## 2026 currency

Cursors are **GA and have been since Summer '24 (API 61.0)** — worth saying plainly, because they are new enough to be absent from most tutorials and old enough that treating them as a Summer '26 feature will date you. What 67.0 added is the same thing it added everywhere: the query behind a cursor runs in user mode unless you pass `AccessLevel.SYSTEM_MODE`, so a sweep job written before the flip processes fewer records rather than failing. The org-level ceilings — **10,000 standard cursors and 200,000 pagination cursors per 24 hours** — are the numbers to design against; they are generous for background work and tight for anything created per page view. Release context: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

## Gotchas

- **`fetch()` costs a SOQL query, and the rows it returns count against the query row limit.** A cursor does not escape 50,000 rows per transaction — it escapes *heap*, and lets you resume in the next transaction. Reading it as a row-limit bypass is the standard mistake.
- **100 `fetch()` calls per transaction**, shared between standard and pagination cursors. At 200 records a fetch that is 20,000 rows before the row limit bites anyway.
- **Cursors expire after two days**, results included. A chain that stalls over a long weekend fails on its next fetch, not at creation.
- **The record set is frozen at creation.** Rows deleted afterwards leave gaps in a standard cursor's pages — that is precisely what `PaginationCursor` and `getDeletedRows()` exist to smooth over.
- **Catching both cursor exceptions the same way loses work.** `TransientCursorException` should be retried; `FatalCursorException` should not be.
- **Nothing tracks `position` for you.** It is zero-based, it lives in your Queueable's state, and an off-by-one either skips a page or reprocesses one forever.
- **A cursor per user request is a daily-limit incident waiting to happen** at 10,000 per org per day — cursors are for jobs, pagination cursors are for pages.

## Recall

Q: What is the practical difference between a cursor and a `Database.QueryLocator`?
A: A locator only works inside a batch class and the platform chunks it; a cursor works in ordinary Apex, is paged by your own `fetch(position, count)`, and lives for two days across transactions.

Q: Does a cursor let you exceed 50,000 query rows in one transaction?
A: No. Each `fetch()` counts as a query and its rows count against the row limit. Cursors save heap and allow resumption, not row budget.

Q: How long does a cursor and its results remain available?
A: Two days.

Q: When would you use `Database.getPaginationCursor` instead of `Database.getCursor`?
A: For UI paging — it skips deleted rows so page sizes stay consistent, and exposes `isDone()` and `getNextIndex()`. It is capped at 100,000 rows per instance.

Q: Which cursor exception is worth retrying?
A: `System.TransientCursorException`. `System.FatalCursorException` is not retryable.

## Related

- [14 · Batch Apex & stateful processing](14-batch-apex-and-stateful-processing.md) — the alternative when 50 M rows and platform-managed chunking are what you want
- [13 · Queueable Apex & chaining](13-queueable-apex-and-chaining.md) — the chain that carries a cursor's position between transactions
- [08-data · LDV performance](../08-data-modeling-and-large-data-volumes/INDEX.md) — making the underlying query selective enough that paging it is worth doing
