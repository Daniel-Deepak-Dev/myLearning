---
vault: SF_Data_360
format: light
level: basic
status: open
gaps: 2
labs: 4
created: 2026-10-02
updated: 2026-10-02
currency: "Summer '26 (API 67.0)"
---
# Ingestion & Data Streams

**One line:** How data gets into Data 360 (formerly Data Cloud): a connector feeds a **data stream**, which lands the data as a **data lake object** (DLO).

**Reach for it when:** you are choosing how fresh each source must be, or a "the agent was wrong" ticket turns out to be stale data.

## Key points

- **The data stream is the unit of ingestion.** One stream per object per connection. It lands rows in a DLO, still in the source's shape → [Data model](data-model-dso-dlo-dmo.md).
- **Three ways in.** Copy it with a data stream; query it in place with zero copy → [Zero copy](zero-copy-and-byol.md); or, for CRM data, **Accelerated Data Ingest** (real time, no pipeline delay, **GA in Summer '26**).
- **The Salesforce CRM connector refreshes on its own.** An incremental refresh runs about every **10 minutes** after a full refresh. Periodic full refresh is **off by default** in new streams.
- **Batch vs streaming.** Batch mode checks the source every **10–15 minutes**; streaming mode reflects changes as soon as they are made.
- **The Ingestion API is the universal fallback** — REST from any system or org. **Streaming** pattern: JSON micro-batches, max **200 KB** per request, processed about every **3 minutes**. **Bulk** pattern: CSV files up to **150 MB**.
- **An Ingestion API schema is an OpenAPI 3.0.x file** (`.yml` / `.yaml`). The schema defines the objects, and therefore the DLOs.
- **One stream can take both patterns.** Streaming and bulk can feed the same data stream.
- **Freshness is decided per stream, not per project.** If an agent reads a stream, it needs to be real time. If only a dashboard reads it, a schedule is fine.

## Gotchas

- **Stale grounding is the commonest "the agent was wrong" root cause**, and it is usually blamed on the model. The agent answers fluently from a record that changed an hour ago.
- **Don't bypass Data 360 for freshness.** Calling CRM directly from an agent action loses the unified profile and its governance. Accelerated Data Ingest exists so you don't have to.
- **Over-refreshing every stream is invisible spend.** The opposite mistake is under-refreshing the one stream an agent depends on.
- **Ingested is not modelled, and modelled is not resolved.** A DLO does nothing until it is mapped to a DMO. Two records for one person stay two profiles until identity resolution runs → [Identity resolution](identity-resolution.md).
- **A stream can report Success with 0 rows.** Check the row count in the refresh history, not the green status.

## Gaps to close

- [ ] Re-read the Data Streams, Data Stream Schedule and Ingestion API pages in full once help.salesforce.com is reachable. This note was built from search extracts.
- [ ] Which objects and orgs does Accelerated Data Ingest cover, and does it replace the CRM connector's 10-minute incremental refresh?

## Hands-on

- [ ] **D360-INGEST-01** · 20 min · Create a CRM data stream on Contact in the home org, then read the refresh history. **Proves:** a stream lands rows in a DLO, and the history shows the row count. A green status alone shows nothing.
- [ ] **D360-INGEST-02** · 30 min · Set up an Ingestion API connector with a two-object OpenAPI schema, then push one record with the streaming pattern and one CSV with bulk. **Proves:** both patterns land in the same stream; time how long the streaming record takes to appear.
- [ ] **D360-INGEST-03** · 15 min · Send a streaming payload over 200 KB. **Proves:** the size limit is enforced at the API. Copy the error body verbatim.
- [ ] **D360-INGEST-04** · 20 min · Ground a prompt on a Contact field, change the field in CRM, then ask straight away and again after the next refresh. **Proves:** freshness is a property of the stream, not of the model.

## Related

- [Data Model: DSO, DLO & DMO](data-model-dso-dlo-dmo.md) — what happens to the DLO next
- [Zero Copy & BYOL](zero-copy-and-byol.md) — the alternative to copying
- [Lab Environment](lab-environment.md) — which orgs you can connect, and the Developer Edition limits
- [SF_core · 06-integration · 07 Bulk API 2.0](../SF_core/06-integration-and-apis/07-bulk-api-2.md) — the platform bulk pattern the Ingestion API's bulk mode resembles
- [RELEASE-RADAR · Data 360](../RELEASE-RADAR/data-360.md) — the Summer '26 ingest status changes

## Sources

- [Ingestion API](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-ingestion-api.html) — Salesforce Developers · via search 2026-10-02 · bulk and streaming patterns; one data stream per object per connection; 150 MB CSV, 200 KB JSON
- [Requirements for Ingestion API Schema File](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-ingestion-api-schema-req.html) — Salesforce Developers · via search 2026-10-02 · OpenAPI 3.0.x, `.yml` / `.yaml`
- [Streaming Ingestion](https://developer.salesforce.com/docs/data/data-cloud-int/references/data-cloud-ingestionapi-ref/c360-a-api-streaming-ingestion.html) — Salesforce Developers · via search 2026-10-02 · fire-and-forget micro-batches, processed about every 3 minutes
- [Data Stream Schedule in Data 360](https://help.salesforce.com/s/articleView?id=sf.c360_a_data_stream_schedule.htm&language=en_US) — Salesforce Help · via search 2026-10-02 · incremental refresh every 10 minutes; periodic full refresh off by default in new streams
- [CRM Connector Streaming](https://help.salesforce.com/s/articleView?id=data.c360_a_crm_connector_streaming.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-02 · batch every 10–15 minutes vs streaming
- [Data 360 — Summer '26 release notes](https://help.salesforce.com/s/articleView?id=release-notes.rn_c360_truth.htm&language=en_US&release=262&type=5) — Salesforce Help · via search 2026-10-02 · Accelerated Data Ingest *"now Generally Available"*

## History

- 2026-10-02 · created — first Data 360 note; facts carried over from the archived roadmap notes and confirmed against Salesforce search extracts, because help.salesforce.com was blocked from this session
