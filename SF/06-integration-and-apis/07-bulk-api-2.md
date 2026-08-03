# Bulk API 2.0

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** Moving large record volumes asynchronously — ingest and query jobs, and what changed from v1. Declarative and desktop loading tools are [01-admin · 13](../01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md); LDV design is [08-data](../08-data-modeling-and-large-data-volumes/INDEX.md).

> **What changed.** *"Bulk API means creating a job, splitting your data into batches and polling each one"* describes **v1**. **Bulk API 2.0 is the default**, it batches the data for you, and it is an ordinary REST surface with OAuth. v1 is not retired — but it is where no new capability lands, and **PK chunking works differently enough that v1 advice actively misleads**.

## Core idea

Bulk API exists because synchronous APIs are the wrong shape for large volumes: they hold a connection, they run inside one transaction's limits, and they fail all-or-nothing at exactly the scale where that is most expensive. Bulk is asynchronous by construction — you hand Salesforce a job and a payload, it queues the work, splits it, runs it in parallel across its own infrastructure, and hands back a result set you collect later.

**2.0's contribution is the removal of the client's job.** Under v1 the caller chose batch sizes, submitted each batch, tracked each batch's state and reassembled results — a large amount of code whose only purpose was to guess at Salesforce's internal parallelism. 2.0 deletes all of it. Salesforce's own guidance draws the line at **more than 2,000 records** as a good candidate for Bulk.

## How it works

| Step | Ingest job | Query job |
|---|---|---|
| 1 | `POST /jobs/ingest` — object, operation, `lineEnding` | `POST /jobs/query` with the SOQL |
| 2 | `PUT /jobs/ingest/{id}/batches` — the CSV | — |
| 3 | `PATCH` state to `UploadComplete` | — |
| 4 | poll `GET /jobs/ingest/{id}` for `JobComplete` | poll for `JobComplete` |
| 5 | `successfulResults` / `failedResults` / `unprocessedRecords` | `GET /results`, paged by locator |

- **CSV only**, and `lineEnding` must match the file (`LF` or `CRLF`). A Windows-generated file declared as `LF` fails in a way the error message does not make obvious.
- **Operations include `upsert`** with an external ID field — the same idempotency property as REST, at volume. → [04](04-rest-api-fundamentals.md)
- **Failures are per record, not per job.** A job reaching `JobComplete` says nothing about success; `failedResults` must be read every time.
- **`unprocessedRecords` is a third bucket** and is easy to drop: records that were neither applied nor rejected, and that a correct client resubmits.
- **Bulk still fires triggers, flows and validation rules.** It is not a back door around automation, and per-record automation cost is what actually determines throughput. → [01-admin · order of execution](../01-admin-and-declarative-platform/INDEX.md)
- **Read the org's remaining daily allowance from `/limits`** rather than quoting a number from memory — it varies by edition and by purchased capacity.

## 2026 currency

The v1 → 2.0 shift is complete in the sense that matters: **new capability lands in 2.0 and v1 receives none**. v1 is still callable, so this is a legacy status, not a retirement — audit remaining use under **Setup → Bulk Data Load Jobs**, filtering for **Bulk V1** jobs ([../CURRENCY.md](../CURRENCY.md)). Two adjacent facts stay true and are routinely misremembered: **Data Loader does not default to Bulk API 2.0** — *Use Bulk API* and *Use Bulk API 2.0* are separate opt-in checkboxes ([01-admin · 13](../01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md)) — and **serial mode still exists** for when parallel processing causes lock contention.

> **From my notes.** The seed `Bulk API` page is v1-era throughout: it teaches batch splitting, the 10,000-record batch ceiling and the `Sforce-Enable-PKChunking` header as the standard way to extract large tables. All three are v1 mechanics. **In 2.0 you do not set batch sizes and you do not set that header** — chunking of query jobs is handled server-side. The page's genuinely durable lesson survives: **lock contention, not row count, is what makes a large load slow**, and serial mode is the lever.

## Gotchas

- **`JobComplete` does not mean every record succeeded.** It means processing finished. This is the single most common Bulk defect.
- **`Sforce-Enable-PKChunking` is a Bulk **v1** header.** Copying it into a 2.0 integration does nothing, and the tutorial that told you to is describing another API.
- **Parent-child loads self-inflict lock contention.** Sorting the file by parent ID so one chunk touches one parent is the standard fix; serial mode is the fallback. → [08-data · skew](../08-data-modeling-and-large-data-volumes/INDEX.md)
- **A hard-deleted record bypasses the Recycle Bin** and needs `Bulk API Hard Delete` — a permission worth treating as privileged.
- **Bulk query has no relationship-subquery support** the way REST query does; reshape into separate jobs rather than fighting it.
- **The results endpoints expire.** Collect them; a job whose results were never fetched is unrecoverable work.

## Recall

Q: What is the record threshold Salesforce gives as a good candidate for Bulk?
A: More than 2,000 records in one operation.

Q: What did 2.0 remove from the client's responsibility?
A: Batch splitting, per-batch submission and per-batch tracking — Salesforce batches the payload itself.

Q: Does `JobComplete` mean the load succeeded?
A: No — only that processing finished. `failedResults` and `unprocessedRecords` must both be read.

Q: Which PK chunking advice is wrong for 2.0?
A: The `Sforce-Enable-PKChunking` header — it is a Bulk v1 mechanism and does nothing in 2.0.

Q: Is Bulk API v1 retired?
A: No. It is legacy — still callable, but no new capability lands there.

## Related

- [04 · REST API fundamentals](04-rest-api-fundamentals.md) — the synchronous surface below Bulk's threshold
- [01-admin · 13 Data import, export & loading tools](../01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md) — Data Loader, and its Bulk checkboxes
- [08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md) — skew, selectivity and why large loads are slow
- [24 · API limits, monitoring & access control](INDEX.md) — the daily allowance Bulk draws on
