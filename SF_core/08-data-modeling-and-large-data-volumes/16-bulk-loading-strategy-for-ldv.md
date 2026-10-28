---
vault: SF_core
area: 08-data-modeling-and-large-data-volumes
format: dense
status: learning
created: 2026-08-03
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 15
tags: [currency-warning]
---
# Bulk Loading Strategy for LDV

**Scope:** Making a large load finish — the levers, in the order you reach for them. The API surface is [06-integration · 07](../06-integration-and-apis/07-bulk-api-2.md); lock contention is [12](12-record-locking-and-concurrency.md); a one-off migration is [25](25-data-migration-and-cutover.md).

> **What changed.** *"Tune the batch size and switch on PK chunking"* is **Bulk API v1** advice. In **Bulk API 2.0 you set neither** — Salesforce chunks server-side, and the `Sforce-Enable-PKChunking` header does nothing at all. It remains a real and useful header for **v1 extraction**, which is the only place to keep using it.

## Core idea

Throughput is almost never limited by the API. It is limited by **what the platform does per row** — recalculating sharing, maintaining indexes, firing automation, and taking locks on shared parents. A load of 20 million rows into an object with no automation and no sharing complexity is fast on any API; the same load into a skewed, trigger-heavy object is slow on all of them.

So the strategy is subtractive. Work out what the platform is doing per row that you do not need during the load, switch it off, load, and switch it back on. Everything below is one of those switches.

## How it works

- **Defer sharing calculation.** With the `Defer Sharing Calculation` permission you suspend group membership and sharing rule recalculation for the duration of the load and resume it afterwards, once — instead of per batch → [07-security · 16](../07-security-and-sharing/16-sharing-recalculation-and-performance.md).
- **Load in dependency order** — parents before children, and lookups before the records that point at them. Anything else forces a second update pass.
- **Sort the file by parent Id.** Two batches touching the same parent contend for its lock; grouping children by parent keeps each lock inside one batch → [12](12-record-locking-and-concurrency.md).
- **Serial vs parallel.** Bulk 2.0 runs **parallel only** — its `concurrencyMode` field is documented as *"for future use"*. If sorting by parent does not stop `UNABLE_TO_LOCK_ROW`, serial mode is a **Bulk API v1** option (in Data Loader, *Enable serial mode for Bulk API* with *Use Bulk API* ticked). It costs throughput but finishes.
- **Suppress what you can, and know what you cannot.** Triggers and flows can be bypassed by a custom-permission or custom-setting switch; **validation rules and duplicate rules cannot be turned off for API writes** and fire on every row → [01-admin · 08](../01-admin-and-declarative-platform/08-validation-rules-and-duplicate-management.md).
- **Use external IDs to upsert** rather than query-then-update — one round trip, and no ID mapping table to maintain → [03](03-record-ids-external-ids-and-upsert.md).
- **Deleting is a load too.** `hardDelete` skips the Recycle Bin, so the rows leave the table at once instead of slowing scans until the purge. Salesforce recommends the **Bulk API 2.0** hard delete for large volumes → [13](13-deletes-recycle-bin-and-physical-deletion.md).

## 2026 currency

Bulk API 2.0 is where capability lands and where a new load should start; **v1 is legacy but not retired**, and PK chunking and serial mode are the two reasons to still reach for it. Two things worth re-checking on an inherited integration: whether it is pinned to a **retired API version**, which now returns **410 GONE** rather than degrading → [06-integration · 02](../06-integration-and-apis/02-api-versions-and-the-retirement-treadmill.md). **Versions 31.0–40.0 are next**: unsupported from **Summer '27**, retired in **Summer '28**, after which Bulk API answers `400 InvalidVersion`. And whether it still uses an **instanced hostname**: the *Update Instanced URLs in API Traffic* Release Update was postponed again, to **Spring '27** → [06-integration · 03](../06-integration-and-apis/03-api-endpoints-hostnames-and-edge-network.md). A load that has run nightly for six years is exactly the thing nobody has re-pointed.

## Gotchas

- **`Sforce-Enable-PKChunking` in a 2.0 client is silently ignored.** No error, no chunking, no clue.
- **Validation and duplicate rules cannot be switched off for a load.** Plan for per-row failures and a retry file rather than a clean run.
- **A "successful" load with automation bypassed leaves derived data missing** — roll-ups, formula-driven flags and history all need a deliberate backfill pass.
- **Deferring sharing calculation defers the cost, it does not remove it.** Resuming on a 50-million-row object is itself a long job; schedule it.
- **Ownership skew is created by loads.** Assigning every migrated record to one integration user is the classic way to manufacture it → [10](10-data-skew.md).
- **The 10-second lock wait is per transaction, not per row.** One contended parent fails the whole batch → [12](12-record-locking-and-concurrency.md).
- **Data Loader does not default to Bulk API 2.0** — both bulk options are opt-in checkboxes → [01-admin · 13](../01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md).

## Recall

Q: What does `Sforce-Enable-PKChunking` do in Bulk API 2.0?
A: Nothing. It is a v1 header; 2.0 chunks server-side and exposes no batch-size or chunking control.

Q: Which two save-time rules cannot be disabled for an API load?
A: Validation rules and duplicate rules — they fire on every row regardless of the write path.

Q: Why sort a load file by parent Id?
A: To keep all children of a parent inside one batch, so batches do not contend for the same parent lock.

Q: What does the Defer Sharing Calculation permission buy you?
A: It suspends group membership and sharing rule recalculation during the load so it runs once afterwards rather than continuously.

Q: When is Bulk API v1 still the right choice?
A: For extraction using PK chunking, and for a load that only finishes in serial mode — two capabilities 2.0 does not expose.

## Related

- [12 · Record locking & concurrency](12-record-locking-and-concurrency.md) — the failure mode most loads actually hit
- [25 · Data migration & cutover](25-data-migration-and-cutover.md) — these levers inside a one-off migration project
- [06-integration · 07 Bulk API 2.0](../06-integration-and-apis/07-bulk-api-2.md) — the API surface and job lifecycle
- [07-security · 16 Sharing recalculation & performance](../07-security-and-sharing/16-sharing-recalculation-and-performance.md) — what deferral actually defers

## Sources

- [Bulk API 2.0 and Bulk API Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_asynch.pdf) — Salesforce Developers · read 2026-10-28 · `concurrencyMode` *"For future use … Currently only parallel mode"*; versions 31.0–40.0 *"Deprecated and unsupported from Summer '27. Retired from Summer '28"*
- [Salesforce Platform API Versions 31.0 through 40.0 Retirement](https://help.salesforce.com/s/articleView?id=005321531&language=en_US&type=1) — Salesforce Help · via search 2026-10-28 · after retirement REST returns `410 GONE`, SOAP `500 UNSUPPORTED_API_VERSION`, Bulk API `400 InvalidVersion`
- [Data Loader Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_data_loader.pdf) — Salesforce Developers · read 2026-10-28 · *Enable serial mode for Bulk API* applies *"If Use Bulk API is selected"*
- [Best Practices for Deployments with Large Data Volumes (PDF, Winter '27)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_large_data_volumes_bp.pdf) — Salesforce Developers · read 2026-10-28 · *"use the Bulk API 2.0's hard delete function to delete large data volumes"*
- [Update Instanced URLs in API Traffic (Release Update)](https://help.salesforce.com/s/articleView?id=release-notes.rn_update_instanced_urls_in_api_traffic.htm&language=en_US&release=262&type=5) — Salesforce Help · via search 2026-10-28 · scheduled for Spring '26, postponed; listed under *Scheduled to Be Enforced in Spring '27* on the Winter '27 Release Updates page

## History

- 2026-10-28 · Winter '27 currency check: API 31.0–40.0 retirement dates; instanced-URL enforcement now Spring '27; Bulk 2.0 has no serial mode; hard delete described by query cost, not storage
