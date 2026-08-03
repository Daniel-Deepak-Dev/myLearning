# 08 · Data Modeling & Large Data Volumes

Model it well, then keep it fast past 10M rows. **20 topics** · phases [14](PHASES.md), [15](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> 📌 **Movable block.** Nothing downstream depends on this area, so phases 14–15 can run any time after phase 02 if you want the data layer early.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | Data model design principles | standard-first, normalization vs reporting pressure | 14 |
| 02 | Relationships deep dive | master-detail vs lookup, cascade, reparenting, depth limits | 14 |
| 03 | Record IDs, external IDs & upsert | 15 vs 18 char, external ID indexing, upsert semantics | 14 |
| 04 | Standard CRM object map | core object graph, polymorphic keys, who/what | 14 |
| 05 | Large data volume fundamentals | where the platform degrades and why | 14 |
| 06 | Indexes & query selectivity | standard/custom indexes, selectivity thresholds | 14 |
| 07 | Query Plan & performance tuning | Query Plan tool, cardinality, anti-patterns | 14 |
| 08 | Data skew | ownership, lookup and account skew; thresholds and fixes | 14 |
| 09 | Skinny tables & support levers | what they solve, constraints, how to request | 14 |
| 10 | Big objects & Async SOQL | index design, ingestion, retrieval limits | 14 |
| 11 | Archiving & retention strategy 🆕 | native archiving, offload to Data 360, policy design | 15 |
| 12 | Bulk loading strategy for LDV ⚠️ | Bulk API 2.0, PK chunking, defer sharing, load order | 15 |
| 13 | External objects vs replicated copies | federation trade-offs, indirect lookups | 15 |
| 14 | Zero-copy & Data 360 as data tier 🆕 | federate instead of migrate; when it actually fits | 15 |
| 15 | Data quality, deduplication & MDM | matching rules, golden record, survivorship | 15 |
| 16 | Sandboxes, seeding & Data Mask | sandbox types, seeding templates, masking policy | 15 |
| 17 | Backup, restore & recovery ⚠️ | no free recovery service; RPO/RTO design | 15 |
| 18 | Multi-currency, multi-language & locale | dated exchange rates, translation and locale effects | 15 |
| 19 | Hyperforce, residency & data locality 🆕 | regions, migration effects, latency and compliance | 15 |
| 20 | Data architecture review checklist | sizing, skew, growth, archival, cert-aligned recap | 15 |

## Related

- **08** pairs with [07-security · 16 Sharing recalculation](../07-security-and-sharing/INDEX.md) — ownership skew is a sharing problem first.
- **12** depends on [06-integration · 06 Bulk API 2.0](../06-integration-and-apis/INDEX.md).
- **13** pairs with [06-integration · 18 Salesforce Connect](../06-integration-and-apis/INDEX.md).
- **14** is the seam into [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md) — zero-copy federation is a Data 360 topic seen from the core-platform side.
- **16** overlaps [09-devops · 06 Source tracking & sandbox workflow](../09-devops-sfdx-and-release-management/INDEX.md).

## Seed notes

[_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) maps `QUERY PLAN` (2025) and `Optimization work` (2023) here — the only legacy material behind this area.
