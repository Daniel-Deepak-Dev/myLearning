---
vault: SF_core
area: 08-data-modeling-and-large-data-volumes
format: dense
status: learning
created: 2026-08-03
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 14
---
# Deletes, the Recycle Bin & Physical Deletion

**Scope:** What "deleted" means at volume, and why removing rows does not immediately remove their cost. DML semantics are [02-apex · 05](../02-apex-and-triggers/05-dml-database-methods-and-savepoints.md); archiving strategy is phase 15.

## Core idea

A Salesforce `delete` is a **soft delete**. The row is flagged, hidden from queries, reports and list views, and moved to the Recycle Bin — but it is still in the table. It no longer counts against storage, which is why the cost is easy to miss: **it still has to be excluded from every query that scans that table**. Deleting fifty million rows does not make the object faster; until they are physically purged it makes it very slightly slower.

This is the half of large-data-volume work that plans routinely omit. Loading strategy gets designed carefully and deletion gets treated as an afterthought, so orgs accumulate a hidden tier of rows that are invisible to users and fully visible to the query optimizer. **Physical deletion is a separate, deliberate, privileged operation**, and at volume it has to be planned like a load.

## How it works

- **Soft delete → Recycle Bin → physical delete.** After **15 days** rows are *scheduled* for hard deletion, and Salesforce does not guarantee when the purge actually runs. Emptying the bin is the only way to make it happen now.
- **The bin has no item limit and does not count against storage.** So nothing purges early, and the storage figure is no clue to how many deleted rows are still in the table.
- **`/queryAll` and `ALL ROWS` are the only ways to see soft-deleted rows.** Ordinary `/query` and SOQL exclude them silently, which makes "the record vanished" reports hard to reproduce → [06-integration · 04](../06-integration-and-apis/04-rest-api-fundamentals.md).
- **`Database.emptyRecycleBin(records)`** purges immediately, and is the standard companion to a `delete` inside a batch job's `execute` method.
- **Bulk API `hardDelete`** bypasses the bin entirely and needs the **`Bulk API Hard Delete`** permission — worth treating as privileged, because there is no undo → [06-integration · 07](../06-integration-and-apis/07-bulk-api-2.md).
- **Deletes fire triggers, flows and cascade rules** and are therefore *slower per record than inserts*. Master-detail cascade multiplies the work invisibly → [02](02-relationships-deep-dive.md).
- **Skinny tables exclude soft-deleted rows**, which is a real part of why they help → [11](11-skinny-tables-and-support-levers.md).

## 2026 currency

The Winter '27 edition of Salesforce's LDV guide (updated 18 September 2026) states both facts above: Recycle Bin items **don't count against storage**, and the bin has **no item limit**. This note used to say the opposite on both. The guide also recommends **Bulk API 2.0 hard delete** for large deletes. 🚩 No release note dates the change, and older pages still describe a capped bin, so check before quoting it about an old org.

## Gotchas

- **"We deleted the data and it is still slow" is the signature symptom.** The rows are in the bin; the storage figure dropped but the table did not shrink.
- **Storage and performance free up at different times.** Soft-deleted rows stop counting against storage, but they keep slowing scans until purged. A mass delete answers a storage alarm, not a slow report → [06](06-storage-model-and-schema-limits.md).
- **Hard delete is irreversible.** No Recycle Bin, no undelete, no support recovery — and there is no free recovery service to fall back on (phase 15 owns that argument).
- **Deleting a parent cascades to children regardless of sharing**, so a delete job's real row count can be far larger than its input file → [02](02-relationships-deep-dive.md).
- **Deleting at volume causes lock contention** exactly like loading at volume, and takes the same fixes → [12](12-record-locking-and-concurrency.md).
- **`undelete` restores children too**, which surprises people who deleted a parent to remove the children.
- **A deleted *field* or *object* is also soft**, holding its allocation for 15 days → [06](06-storage-model-and-schema-limits.md).

## Recall

Q: Why does deleting millions of rows fail to speed up queries on that object?
A: The rows are soft-deleted and still in the table until physically purged, so they still have to be excluded from every scan.

Q: How long do records stay in the Recycle Bin?
A: 15 days, then they are scheduled for hard deletion at a time Salesforce does not guarantee. Current docs give the bin no item limit, so there is no early purge.

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

## Sources

- [Best Practices for Deployments with Large Data Volumes (PDF, Winter '27)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_large_data_volumes_bp.pdf) — Salesforce Developers · read 2026-10-28 · *Deleting Data*: *"items in the Recycle Bin don't count against an org's storage usage. There isn't a limit on the number of deleted items that the Recycle Bin can hold"*; 15 days then scheduled, no guaranteed time; Bulk API 2.0 hard delete recommended
- [Manage the Recycle Bin in Lightning Experience](https://help.salesforce.com/s/articleView?id=sf.recycle_bin_manage.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-28 · same two statements; purge time not guaranteed
- [Bulk API 2.0 and Bulk API Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_asynch.pdf) — Salesforce Developers · read 2026-10-28 · `hardDelete` skips the Recycle Bin; `Bulk API Hard Delete` is off by default

## History

- 2026-10-28 · Winter '27 currency check: Recycle Bin rows no longer described as counting against storage or as size-capped; purge time not guaranteed
