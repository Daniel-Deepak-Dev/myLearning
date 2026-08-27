# Bulk Loading Strategy for LDV

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** Making a large load finish — the levers, in the order you reach for them. The API surface is [06-integration · 07](../06-integration-and-apis/07-bulk-api-2.md); lock contention is [12](12-record-locking-and-concurrency.md); a one-off migration is [25](25-data-migration-and-cutover.md).

> **What changed.** *"Tune the batch size and switch on PK chunking"* is **Bulk API v1** advice. In **Bulk API 2.0 you set neither** — Salesforce chunks server-side, and the `Sforce-Enable-PKChunking` header does nothing at all. It remains a real and useful header for **v1 extraction**, which is the only place to keep using it.

## Core idea

Throughput is almost never limited by the API. It is limited by **what the platform does per row** — recalculating sharing, maintaining indexes, firing automation, and taking locks on shared parents. A load of 20 million rows into an object with no automation and no sharing complexity is fast on any API; the same load into a skewed, trigger-heavy object is slow on all of them.

So the strategy is subtractive. Work out what the platform is doing per row that you do not need during the load, switch it off, load, and switch it back on. Everything below is one of those switches.

## How it works

- **Defer sharing calculation.** With the `Defer Sharing Calculation` permission you suspend group membership and sharing rule recalculation for the duration of the load and resume it afterwards, once — instead of per batch → [07-security · 16](../07-security-and-sharing/16-sharing-recalculation-and-performance.md).
- **Load in dependency order** — parents before children, and lookups before the records that point at them. Anything else forces a second update pass.
- **Sort the file by parent Id.** Two batches touching the same parent contend for its lock; grouping children by parent keeps each lock inside one batch → [12](12-record-locking-and-concurrency.md).
- **Serial vs parallel.** Bulk 2.0 processes in parallel by default. If you are seeing `UNABLE_TO_LOCK_ROW`, serial is the fix that costs throughput but finishes.
- **Suppress what you can, and know what you cannot.** Triggers and flows can be bypassed by a custom-permission or custom-setting switch; **validation rules and duplicate rules cannot be turned off for API writes** and fire on every row → [01-admin · 08](../01-admin-and-declarative-platform/08-validation-rules-and-duplicate-management.md).
- **Use external IDs to upsert** rather than query-then-update — one round trip, and no ID mapping table to maintain → [03](03-record-ids-external-ids-and-upsert.md).
- **Deleting is a load too.** `hardDelete` skips the Recycle Bin and is the only delete that frees storage immediately → [13](13-deletes-recycle-bin-and-physical-deletion.md).

## 2026 currency

Bulk API 2.0 is where capability lands and where a new load should start; **v1 is legacy but not retired**, and PK chunking is the one reason to still reach for it. Two things worth re-checking on an inherited integration: whether it is pinned to a **retired API version**, which now returns **410 GONE** rather than degrading → [06-integration · 02](../06-integration-and-apis/02-api-versions-and-the-retirement-treadmill.md), and whether it still uses an **instanced hostname**, which stops being supported shortly after Winter '27 → [06-integration · 03](../06-integration-and-apis/03-api-endpoints-hostnames-and-edge-network.md). A load that has run nightly for six years is exactly the thing nobody has re-pointed.

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
A: For extraction using PK chunking — the one capability 2.0 does not expose.

## Related

- [12 · Record locking & concurrency](12-record-locking-and-concurrency.md) — the failure mode most loads actually hit
- [25 · Data migration & cutover](25-data-migration-and-cutover.md) — these levers inside a one-off migration project
- [06-integration · 07 Bulk API 2.0](../06-integration-and-apis/07-bulk-api-2.md) — the API surface and job lifecycle
- [07-security · 16 Sharing recalculation & performance](../07-security-and-sharing/16-sharing-recalculation-and-performance.md) — what deferral actually defers
