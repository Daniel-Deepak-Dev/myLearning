# Record Locking & Concurrency

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** Why concurrent writes fail at volume, and how to make them stop. The read-path chain ends at [11](11-skinny-tables-and-support-levers.md); this opens the write path. `FOR UPDATE` syntax is [10-soql · 01](../10-soql-and-sosl/01-query-anatomy-and-the-soql-model.md); retry policy is [06-integration · 23](../06-integration-and-apis/23-idempotency-retries-and-error-handling.md).

## Core idea

`UNABLE_TO_LOCK_ROW` is the write path's version of a non-selective query: an error that looks random, is not, and gets worse exactly as volume and concurrency rise. A transaction that wants to write a record takes an exclusive lock on it. If another transaction already holds that lock, the second waits — and after **10 seconds** it gives up and fails the whole transaction.

The part that surprises people is **which** records get locked. Writing a child record locks its **parent**. So two processes updating two entirely different Opportunities on the same Account are not independent: they serialise behind one Account row. This is why lock contention is a *data-shape* problem and why it belongs next to skew rather than in the Apex area — the fix is almost never in the code that failed.

## How it works

- **The wait is 10 seconds**, then the transaction fails. It is not a queue you can lengthen.
- **Master-detail writes lock the master.** Required lookups behave the same way. An optional lookup does not lock its target on every write, but a lookup with millions of children pointing at one record still concentrates contention → [02](02-relationships-deep-dive.md).
- **Bulk API processes batches in parallel by default.** Two parallel batches containing children of the same parent will collide, which is why the same file succeeds when loaded one way and fails another.
- **The three standard fixes, in order of preference:**
  1. **Sort the load file by parent Id**, so records sharing a parent land in the same chunk rather than being split across parallel batches.
  2. **Reduce the batch size**, shortening how long each lock is held.
  3. **Switch to serial mode**, which trades throughput for the guarantee that only one batch runs at a time.
- **`FOR UPDATE` holds its locks until the transaction ends** — there is no early release, so a long transaction that locks early converts other users' saves into failures → [10-soql · 01](../10-soql-and-sosl/01-query-anatomy-and-the-soql-model.md).
- **Group membership has its own lock**, on the group maintenance tables, and **granular locking** is the lever that narrows it → [07-security · 08](../07-security-and-sharing/08-groups-queues-and-the-grantee-model.md).
- **`UNABLE_TO_LOCK_ROW` is retryable**, unlike a validation error — but retrying harder without changing the shape just moves the failure → [06-integration · 23](../06-integration-and-apis/23-idempotency-retries-and-error-handling.md).

## Gotchas

- **It reproduces only under concurrency**, so it passes every test and fails in production at month end.
- **An approval process locks the record while it is in flight**, and automation editing it mid-approval hits exactly this error → [01-admin · 12](../01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md).
- **Ownership changes lock widely.** Reassigning a skewed owner touches every child record's sharing and is the single most contention-heavy routine operation → [10](10-data-skew.md).
- **Lock late and commit fast.** DML at the end of the transaction, callouts and slow work before it, never between the lock and the commit.
- **Serial mode is not a fix, it is a fallback.** If a load only completes serially, the data shape is the actual problem.
- **Two integrations writing the same objects on the same schedule will find each other.** Stagger them; concurrency you did not design is still concurrency.
- **A trigger that updates a parent on every child insert manufactures contention** even when the load file is sorted correctly.

## Recall

Q: How long does a transaction wait for a locked row before failing?
A: 10 seconds, then the whole transaction fails with `UNABLE_TO_LOCK_ROW`.

Q: Why do two updates to different child records collide?
A: Writing a detail record takes a lock on its master, so siblings serialise behind the same parent row.

Q: What is the preferred fix for lock contention in a bulk load, before reducing batch size or going serial?
A: Sort the file by parent Id so records sharing a parent are not split across parallel batches.

Q: Is `UNABLE_TO_LOCK_ROW` worth retrying?
A: Yes — it is transient and retryable. But retrying without changing the data shape or the load order only defers the failure.

Q: How long does `FOR UPDATE` hold its locks?
A: Until the transaction ends. There is no early release, so long transactions turn into other users' lock errors.

## Related

- [10 · Data skew](10-data-skew.md) — the distribution that makes contention inevitable
- [02 · Relationships deep dive](02-relationships-deep-dive.md) — why the parent gets locked at all
- [06-integration · 07 Bulk API 2.0](../06-integration-and-apis/07-bulk-api-2.md) — parallel batches, serial mode and where the sort happens
- [07-security · 08 Groups, queues & the grantee model](../07-security-and-sharing/08-groups-queues-and-the-grantee-model.md) — granular locking, the membership-side lever
