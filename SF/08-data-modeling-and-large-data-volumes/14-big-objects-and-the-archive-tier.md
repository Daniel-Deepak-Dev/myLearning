# Big Objects & the Archive Tier

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** The storage tier beneath standard and custom objects — what it is for, and the one design decision you cannot take back. Retention *policy* and the offload to Data 360 are phase 15.

> **What changed.** *"Query big objects with Async SOQL"* has been wrong since **Summer '23**. **Async SOQL is retired** — Salesforce's guidance is explicit: use **Bulk API query or Batch Apex** to query or report on custom big objects. **Big objects themselves are not retired** and are current at 67.0; only the query mechanism went.

## Core idea

A big object holds enormous volumes of data — hundreds of millions of rows and beyond — outside the normal record store, and it buys that scale by **giving almost everything else up**. No triggers, no flows, no validation rules, no sharing rules, no standard Salesforce app UI, and no arbitrary `WHERE` clause. It is a write-once, read-by-key archive, and it is only the right answer when the access pattern genuinely looks like that.

The decision that defines a big object is its **composite index**, and it is fixed at deployment. You cannot alter it, extend it or drop it afterwards — changing your mind means creating a new big object and migrating. That makes it the most consequential single design choice in this area, and the reason to design the index around **the question you will ask most often** rather than around what the data looks like.

## How it works

- **The index is the primary key.** 1–5 custom fields, **total length ≤ 100 characters**, no URL or Long Text Area fields, at least one custom field. **Immutable after deployment.**
- **Queries must filter on index fields in the order defined** — a prefix match, with the permitted operators depending on a field's position. There is no arbitrary filtering, so a field outside the index is effectively unqueryable.
- **Field types are limited:** Text, Number, DateTime, Lookup, Email, Phone, URL, Long Text Area. **No picklists, formulas or checkboxes.**
- **Writing is `Database.insertImmediate()`**, and it behaves unlike DML in two ways: it **commits outside the transaction and cannot be rolled back**, and it is really an **upsert on the index** — reinserting the same index values with different data updates the row. `Database.deleteImmediate()` is the counterpart.
- **Two kinds exist.** *Standard* big objects ship with features — `FieldHistoryArchive` behind Field Audit Trail is one → [07-security · 22](../07-security-and-sharing/22-field-audit-trail-and-data-retention.md). *Custom* ones you define and deploy through the Metadata API.
- **Storage is a separate allocation** — about **1 million records per org**, extendable — so archiving into a big object genuinely relieves data storage → [06](06-storage-model-and-schema-limits.md).
- **Bulk API 2.0 is the loading path** for volume → [06-integration · 07](../06-integration-and-apis/07-bulk-api-2.md).

## 2026 currency

The Async SOQL retirement above is the correction that matters, and it is old enough that most surviving tutorials predate it — Async SOQL was the *headline* feature of big objects when they went GA in Winter '18, so material written before Summer '23 leads with it. Read **Bulk API query or Batch Apex** wherever a guide says Async SOQL. Big objects remain current at API 67.0, and Salesforce continues to publish new patterns for them — the June 2026 *Big Objects Playbook* on payload capture and replay is the current worked example. Deeper integration between big objects and Data 360 is where the tier is heading; phase 15 owns that comparison.

## Gotchas

- **The index cannot be changed.** Not extended, not reordered, not dropped. Getting it wrong means a new object and a migration.
- **Design the index around the query, not the data.** The field you filter on most goes first.
- **`insertImmediate` cannot be rolled back**, so a partial failure inside a larger transaction leaves committed archive rows behind.
- **No triggers or flows means no derived data.** Everything you will ever need must be written at archive time.
- **Reporting is not direct.** Standard reports do not run over custom big objects; you extract via Bulk API, Batch Apex or CRM Analytics.
- **Archived history is frequently missed by backup tooling** — verify rather than assume → [07-security · 22](../07-security-and-sharing/22-field-audit-trail-and-data-retention.md).
- **A big object is not a cheap custom object.** If the data needs editing, sharing or automation, it is the wrong tier.

## Recall

Q: How do you query a custom big object at Summer '26?
A: Bulk API query or Batch Apex. Async SOQL was retired in Summer '23.

Q: Were big objects retired along with Async SOQL?
A: No. Big objects are current at API 67.0; only the query mechanism was withdrawn.

Q: What are the constraints on a big object's index?
A: 1–5 custom fields, 100 characters total, no URL or Long Text Area fields — and it is immutable once deployed.

Q: How does `Database.insertImmediate()` differ from ordinary DML?
A: It commits outside the transaction and cannot be rolled back, and it upserts on the index rather than always inserting.

Q: Why can you not filter a big object on an arbitrary field?
A: Queries must match the composite index in the order it was defined, so any field outside the index is effectively unqueryable.

## Related

- [13 · Deletes, the Recycle Bin & physical deletion](13-deletes-recycle-bin-and-physical-deletion.md) — the alternative to archiving: actually removing the rows
- [06 · Storage model & schema limits](06-storage-model-and-schema-limits.md) — the separate allocation this tier draws on
- [07-security · 22 Field Audit Trail & data retention](../07-security-and-sharing/22-field-audit-trail-and-data-retention.md) — `FieldHistoryArchive`, a standard big object in the wild
- [06-integration · 07 Bulk API 2.0](../06-integration-and-apis/07-bulk-api-2.md) — the load and extract path
