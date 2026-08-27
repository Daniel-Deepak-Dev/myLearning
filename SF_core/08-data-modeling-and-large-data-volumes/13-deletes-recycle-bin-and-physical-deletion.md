# Deletes, the Recycle Bin & Physical Deletion

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** What "deleted" means at volume, and why removing rows does not immediately remove their cost. DML semantics are [02-apex · 05](../02-apex-and-triggers/05-dml-database-methods-and-savepoints.md); archiving strategy is phase 15.

## Core idea

A Salesforce `delete` is a **soft delete**. The row is flagged, hidden from queries, reports and list views, and moved to the Recycle Bin — but it is still in the table. It still occupies storage, and, the part that matters here, **it still has to be excluded from every query that scans that table**. Deleting fifty million rows does not make the object faster; until they are physically purged it makes it very slightly slower.

This is the half of large-data-volume work that plans routinely omit. Loading strategy gets designed carefully and deletion gets treated as an afterthought, so orgs accumulate a hidden tier of rows that are invisible to users and fully visible to the query optimizer. **Physical deletion is a separate, deliberate, privileged operation**, and at volume it has to be planned like a load.

## How it works

- **Soft delete → Recycle Bin → physical delete.** Rows leave the bin after **15 days**, or earlier when it hits its size cap, or when it is emptied explicitly.
- **The Recycle Bin has a size limit**, calculated from the org's data storage. Past it, the oldest entries are purged early — so the 15 days is a maximum, not a guarantee.
- **`/queryAll` and `ALL ROWS` are the only ways to see soft-deleted rows.** Ordinary `/query` and SOQL exclude them silently, which makes "the record vanished" reports hard to reproduce → [06-integration · 04](../06-integration-and-apis/04-rest-api-fundamentals.md).
- **`Database.emptyRecycleBin(records)`** purges immediately, and is the standard companion to a `delete` inside a batch job's `execute` method.
- **Bulk API `hardDelete`** bypasses the bin entirely and needs the **`Bulk API Hard Delete`** permission — worth treating as privileged, because there is no undo → [06-integration · 07](../06-integration-and-apis/07-bulk-api-2.md).
- **Deletes fire triggers, flows and cascade rules** and are therefore *slower per record than inserts*. Master-detail cascade multiplies the work invisibly → [02](02-relationships-deep-dive.md).
- **Skinny tables exclude soft-deleted rows**, which is a real part of why they help → [11](11-skinny-tables-and-support-levers.md).

## Gotchas

- **"We deleted the data and it is still slow" is the signature symptom.** The rows are in the bin; nothing has been reclaimed.
- **Storage does not free up on delete.** It frees on purge, which is why a storage emergency is not solved by a mass delete → [06](06-storage-model-and-schema-limits.md).
- **Hard delete is irreversible.** No Recycle Bin, no undelete, no support recovery — and there is no free recovery service to fall back on (phase 15 owns that argument).
- **Deleting a parent cascades to children regardless of sharing**, so a delete job's real row count can be far larger than its input file → [02](02-relationships-deep-dive.md).
- **Deleting at volume causes lock contention** exactly like loading at volume, and takes the same fixes → [12](12-record-locking-and-concurrency.md).
- **`undelete` restores children too**, which surprises people who deleted a parent to remove the children.
- **A deleted *field* or *object* is also soft**, holding its allocation for 15 days → [06](06-storage-model-and-schema-limits.md).

## Recall

Q: Why does deleting millions of rows fail to speed up queries on that object?
A: The rows are soft-deleted and still in the table until physically purged, so they still have to be excluded from every scan.

Q: How long do records stay in the Recycle Bin?
A: Up to 15 days — less if the bin hits its storage-derived size cap, which purges the oldest entries early.

Q: How do you see soft-deleted records?
A: `ALL ROWS` in SOQL, or the `/queryAll` REST endpoint. Ordinary queries exclude them silently.

Q: What are the two ways to delete physically?
A: `Database.emptyRecycleBin()` after a delete, or Bulk API `hardDelete`, which requires the `Bulk API Hard Delete` permission.

Q: Why can a delete job process far more records than its input file contains?
A: Master-detail cascade delete removes the children too, and it ignores sharing while doing it.

## Related

- [06 · Storage model & schema limits](06-storage-model-and-schema-limits.md) — what is actually reclaimed, and when
- [12 · Record locking & concurrency](12-record-locking-and-concurrency.md) — deleting at volume is a load, with the same contention
- [14 · Big objects & the archive tier](14-big-objects-and-the-archive-tier.md) — where the data goes when it should not simply vanish
- [02-apex · 05 DML, Database methods & savepoints](../02-apex-and-triggers/05-dml-database-methods-and-savepoints.md) — the DML-level view of soft delete
