---
vault: SF_Data_360
format: light
level: working
status: open
gaps: 2
labs: 3
created: 2026-10-02
updated: 2026-10-02
currency: "Summer '26 (API 67.0)"
---
# Zero Copy & BYOL

**One line:** Data 360 reads data where it already lives (Snowflake, BigQuery, Redshift, Databricks, an Iceberg lake) instead of copying it in. "Bring your own lake."

**Reach for it when:** the data is large, already governed elsewhere, or the client's answer to "can we copy it?" is no.

## Key points

- **Zero copy means no ETL pipeline.** That is how the requirement usually arrives: "can we do this without building a pipeline?" It works both ways: Data 360 can also share its data out to those platforms.
- **Live Query** pushes the query to the source's engine and returns only the result. Good for interactive analysis and live dashboards.
- **Accelerated Query** keeps a cached local copy of a federated query, refreshed every **15 minutes to 7 days**. You trade freshness for speed.
- **File Federation** reads the source's **storage layer** (S3, Iceberg, BigQuery, Redshift) with Data 360's own compute. It suits large historical datasets and generally costs less.
- **Read the release labels literally (Summer '26).** **AWS Glue Data Catalog** federation is **GA**: proposal-safe. **Microsoft Fabric OneLake** federation is **Beta**: prototype only, never load-bearing in a dated plan.
- **Zero copy is the reach leg of grounding.** It lets an agent see warehouse data, but reach is not the same as every Data 360 feature working on that data.

## Gotchas

- **Query performance is inherited from the source.** If the warehouse is busy on Monday mornings, the segment and the agent are slow on Monday mornings. That is not a Salesforce case to escalate.
- **"Zero copy" is not "zero cost".** It removes Data 360 storage. Live Query still spends warehouse compute on every query.
- **Not every feature behaves the same on federated data.** Check identity resolution and segmentation per feature before designing on them; don't assume either "it all works" or "nothing works".
- **Federation removes pipeline lag, not staleness.** If the source loads nightly, so are you.
- **A Beta connector that works in the demo is still Beta.** The label is about support and stability, not whether it runs today.

## Gaps to close

- [ ] Re-read Data 360 Interoperability and the AWS Glue and Microsoft connector pages in full once the doc domains are reachable. This note was built from search extracts.
- [ ] Which Data 360 features (identity resolution, calculated insights, segmentation) are supported on federated DLOs at API 67.0?

## Hands-on

- [ ] **D360-ZC-01** · 30 min · In a Snowflake or BigQuery trial, set up one federated data stream and query it from Data 360. **Proves:** the data never lands in a DLO; note where the query runs. **Needs:** a warehouse trial account.
- [ ] **D360-ZC-02** · 20 min · Run the same query with Live Query and with Accelerated Query at a 15-minute refresh, changing a source row in between. **Proves:** acceleration trades freshness for speed. **Needs:** #1.
- [ ] **D360-ZC-03** · 15 min · For one real dataset you know, write down zero copy or ingestion, and why, in five lines. **Proves:** you can defend the choice per feature, not as a slogan.

## Related

- [Ingestion & Data Streams](ingestion-and-data-streams.md) — the copy-based alternative
- [Vector Search & RAG](vector-search-and-rag.md) — what agents ground on once the data is reachable
- [SF_core · 08-data · 18 Zero-copy & Data 360 as a data tier](../SF_core/08-data-modeling-and-large-data-volumes/18-zero-copy-and-data-360-as-data-tier.md) — the same choice seen from the core platform: when Data 360 is the right tier for CRM data
- [Interview · Zero copy & activation](../Interview/02-data-360/03-zero-copy-and-activation.md) — the federated-everything, Beta-in-a-proposal and slow-Monday scenarios
- [RELEASE-RADAR · Data 360](../RELEASE-RADAR/data-360.md) — the Summer '26 federation status changes

## Sources

- [Data 360 Interoperability](https://architect.salesforce.com/docs/architect/decision-guides/guide/data-360-interoperability.html) — Salesforce Architects · via search 2026-10-02 · Live Query, Accelerated Query (15 min to 7 days), File Federation
- [Data 360 — Summer '26 release notes](https://help.salesforce.com/s/articleView?id=release-notes.rn_c360_truth.htm&language=en_US&release=262&type=5) — Salesforce Help · via search 2026-10-02 · AWS Glue federation GA; Microsoft Fabric OneLake federation Beta
- [AWS Glue Data Catalog Connector](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsglue-connector.html) — Salesforce Developers · via search 2026-10-02
- [Microsoft Integration](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoft-integration.html) — Salesforce Developers · via search 2026-10-02 · the OneLake connector federates using zero copy
- [From Hype to Reality: 4 Things I Learned Implementing Zero Copy with Data 360](https://www.salesforce.com/blog/4-lessons-implementing-zero-copy-data360/) — Salesforce blog · via search 2026-10-02

## History

- 2026-10-02 · created — facts carried over from the archived roadmap notes and confirmed against Salesforce search extracts
