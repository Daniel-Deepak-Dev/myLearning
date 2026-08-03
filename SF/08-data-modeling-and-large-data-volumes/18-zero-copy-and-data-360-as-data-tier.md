# Zero-Copy & Data 360 as a Data Tier

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** Data 360 seen from the *core platform* — when it is the right tier for CRM data and when federation is a latency trap. Its architecture, connectors and GA status table live in [AI_Data · Zero Copy & BYOL](../../AI_Data/01-data-cloud/06-zero-copy-byol/notes.md); this note does not restate them.

## Core idea

Every previous note in this area assumed data belongs either in a Salesforce object or in someone else's system. **Data 360** (formerly Data Cloud — renamed October 2025) is a third place: a lakehouse tier that sits beside the org, can hold CRM data without holding it *in* the org, and — the part that matters here — can **query data where it already lies** instead of moving it.

For a data architect the interesting consequence is that "the org is too big" now has an answer that is neither archiving nor deleting. Cold CRM data can live in a lake and stay analysable and groundable, which a big object cannot manage → [14](14-big-objects-and-the-archive-tier.md). The cost is that it stops being transactional: no triggers, no sharing rules, no record page.

## How it works

- **Two federation modes, not one.** *Query federation* pushes a query into Snowflake, BigQuery, Redshift or Databricks; **File Federation** reads **Apache Iceberg** tables directly at the storage layer via an Iceberg REST catalog, using Data 360's own compute — so there is **no warehouse cluster to run and no external compute bill**.
- **The status of each connector is the design decision.** AWS Glue Data Catalog is GA; Microsoft Fabric OneLake is Beta. Read the labels literally and check the current table before committing → [AI_Data](../../AI_Data/01-data-cloud/06-zero-copy-byol/notes.md).
- **It goes both ways.** External lakes can query unified Data 360 tables, so "federate into Salesforce" and "expose Salesforce to the lake" are the same connection.
- **Data 360 ships monthly**, not on the three-release cadence — a currency assumption that holds everywhere else in this vault fails here.
- **Ingestion is still a thing**, and sometimes the right one; the copy-based alternative is Accelerated Data Ingest.
- **The core-platform bridges are ordinary integration**: Change Data Capture outbound → [06-integration · 13](../06-integration-and-apis/13-change-data-capture.md), and Data 360-triggered flows inbound → [04-flow · 22](../04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md).

## 2026 currency

Zero copy is the reason a 2022 answer to "should we replicate this warehouse into Salesforce?" is now usually wrong: the honest answer is often *neither replicate nor federate into the org — query it in Data 360*. Two 2026 facts anchor that. **File Federation on Iceberg is GA on AWS Glue**, which removes the "who pays for the warehouse compute" objection that stalled these projects. And the product is **Data 360**; every source older than October 2025 calls it Data Cloud, and *Data Cloud One* — the multi-org sharing feature — keeps the old word deliberately → [26](26-cross-org-data-sharing-and-consolidation.md).

## Gotchas

- **Federated query performance is inherited from the source.** A slow warehouse means a slow segment, and a slow agent grounded on it.
- **"Zero copy" is not "zero cost".** You skip storage and pay source-side compute per query — except on File Federation, where the compute is Data 360's.
- **Not every Data 360 feature behaves identically on federated data.** Verify identity resolution and segmentation before designing on them.
- **Federation removes pipeline lag, not staleness.** If the source is a nightly batch, so are you.
- **A federated table is not a record.** No sharing model, no automation, no record page — do not solve a CRM requirement with it.
- **Archiving into Data 360 does not shrink the org** until the source rows are physically deleted → [13](13-deletes-recycle-bin-and-physical-deletion.md).
- **Foundations auto-provisions Data 360** and starts a credit meter, so an org may already have this tier without anyone choosing it → [01-admin · 18](../01-admin-and-declarative-platform/18-salesforce-foundations-and-org-strategy.md).

## Recall

Q: What are the two zero-copy federation modes and how do they differ in cost?
A: Query federation pushes queries into the warehouse and you pay its compute; File Federation reads Iceberg tables at the storage layer with Data 360's own compute, so there is no external compute bill.

Q: What is Data 360's release cadence?
A: Monthly, not the three seasonal releases — currency has to be checked separately from the platform.

Q: Why is a federated table a poor answer to a CRM requirement?
A: It has no sharing model, no automation and no record page; it is analysable, not transactable.

Q: What does zero copy *not* fix?
A: Staleness at the source, and per-query latency — it removes the pipeline, not the dependency.

Q: What was Data 360 called before October 2025?
A: Data Cloud. Sources older than that use the old name throughout.

## Related

- [17 · External objects vs replicated copies](17-external-objects-vs-replicated-copies.md) — the same decision before this tier existed
- [15 · Archiving & retention strategy](15-archiving-and-retention-strategy.md) — Data 360 as an archive destination
- [AI_Data · Zero Copy & BYOL](../../AI_Data/01-data-cloud/06-zero-copy-byol/notes.md) — connectors, GA status and the grounding story
- [04-flow · 22 Data Cloud-triggered flows](../04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md) — reacting to the tier from the core platform
