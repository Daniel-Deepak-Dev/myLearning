# Zero Copy & BYOL Federation

> Track: Data 360 · Roadmap: Phase 02 · Weeks 5–8 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/data-360.md](../../05-release-radar/data-360.md)

**Roadmap scope:** Querying Snowflake, BigQuery, or Databricks in place without duplicating data — and when zero copy beats ingestion (and vice versa).

## What is it?

**Zero copy / BYOL** ("bring your own lake") is federation: Data 360 queries data **where it lives** — Snowflake, BigQuery, Databricks, Amazon Redshift and others — with no physical movement, no duplication, and no reconciliation jobs.

The data stays in the source. Data 360 gets a queryable view of it.

**In the vocabulary clients and exam questions use, zero copy means no ETL.** That's how the question actually arrives — *"can we do this without building an ETL pipeline?"* — so keep the word attached to the concept.

## Why it matters (for the AI-Salesforce architect role)

**Zero copy is how Data 360 reaches enterprise data without an enterprise data migration** — which is usually the thing that kills the project timeline. It's one of the three legs of grounding at scale: reach without copying.

**But the status table below is the actually useful content**, because "is this GA?" is what decides whether a capability goes in a delivery plan or stays in a demo.

### Summer '26 status — read this literally

| Capability | Status |
|---|---|
| **AWS Glue Data Catalog** federation | **GA** |
| **Microsoft Fabric OneLake** federation | **Beta** |
| **Databricks** file federation — identity-provider (IdP) authentication | Summer '26 |
| Accelerated Data Ingest (the copy-based alternative) | **GA** |

**AWS Glue at GA is proposal-safe.** You can commit to it.

**Fabric OneLake is Beta — read the label literally.** Fine to prototype and demo; it carries no support commitment and **must not become load-bearing in a delivery plan**. This is the single most practical distinction in this topic, and getting it wrong is the kind of mistake that surfaces three months into a project.

**The Databricks IdP change is a security-review unlock.** "Can we govern this connection centrally?" is the question that stalls zero-copy projects — not the technology. Central IdP auth is often what gets a connection approved.

## How it works

### Zero copy vs ingestion — the decision

| Choose **zero copy** when | Choose **ingestion** when |
|---|---|
| The data is large and expensive to duplicate | You need Data 360 features on it — identity resolution, segmentation performance |
| It's already governed where it lives | The source can't serve interactive queries |
| Freshness matters and the source is current | You need predictable query latency |
| Compliance forbids copying it | It's needed for real-time agent grounding |

**Name the right-hand column properly:** ingestion *is* the classic **ETL/ELT** path — extract from the source, load into Data 360, transform there. Zero copy is the absence of that pipeline, not a faster version of it. See [ETL/ELT trade-offs, vendor-neutral](../../00-core-skills/04-data-engineering/notes.md).

**The trap in both directions:** teams federate everything to avoid duplication and then discover identity resolution and segmentation need the data locally; or they ingest everything and pay to store what a query could have reached.

### Query performance is the source's problem

With zero copy, **query performance depends on the source system**. If Snowflake is slow or under-provisioned at query time, Data 360 is slow — and so is any agent grounded on it. That's a genuine operational dependency, and it belongs in a design conversation with whoever owns the warehouse, not discovered later.

### Where it fits in grounding

Zero copy is the **reach** leg of the three-legged grounding model:

- **Intelligent Context** → unstructured content
- **Semantic layer** → agreed meaning
- **Zero copy** → reach without copying

An agent answer is only as trustworthy as the weakest of the three.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Set up one federated connection (Snowflake or BigQuery trial) and query it from Data 360 — scoped out in [lab-99](../10-lab-environment/labs/lab-99-parked-external-sources.md), parked until an account exists.
- [ ] Compare query latency federated vs. ingested for the same dataset. The number is the argument.
- [ ] Try running identity resolution against federated data and note where the constraints appear.
- [ ] Write down, for one real dataset, which of the two you'd choose and why. That paragraph is the deliverable clients actually value.

## Gotchas & sharp edges

- **Fabric OneLake is Beta.** No support commitment. Prototype only — never load-bearing in a plan.
- **Query performance is inherited from the source.** A slow warehouse means a slow agent.
- **Not every Data 360 feature works identically on federated data.** Check identity resolution and segmentation behaviour before designing around it.
- **Federated ≠ free.** You're not paying Data 360 storage, but you are paying source-side compute on every query.
- **Zero copy doesn't solve freshness by itself.** It removes pipeline lag, but if the *source* is stale, so are you.
- **Central IdP auth is often the unblocker**, not a technical feature — the Databricks change matters because security review is where these projects stall.
- **"Zero copy" is a marketing-friendly term** that clients sometimes hear as "no cost" or "no work". Set expectations early.

## Related topics

- [Ingestion](../02-ingestion/notes.md) — the copy-based alternative, incl. Accelerated Data Ingest
- [Orientation](../01-orientation/notes.md) — the three ways data gets in
- [Insights & segmentation](../05-insights-segmentation/notes.md) — the meaning leg of grounding
- [Vector DB & unstructured](../07-vector-db-unstructured/notes.md) — the unstructured leg
- [Release radar: Data 360](../../05-release-radar/data-360.md) — the federation status table with sources
