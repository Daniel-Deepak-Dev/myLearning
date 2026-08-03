# 08 · Data Modeling & Large Data Volumes

Model it well, then keep it fast past 10M rows. **24 topics** · phases [14](PHASES.md), [15](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> 📌 **Movable block.** Nothing downstream depends on this area, so phases 14–15 can run any time after phase 02 if you want the data layer early.

**How to read 06–14.** They are two arguments, not nine notes. **Reads:** volume degrades ([07](07-large-data-volume-fundamentals.md)) → because queries stop being selective ([08](08-indexes-and-query-selectivity.md)) → which you diagnose with Query Plan ([09](09-query-plan-and-performance-tuning.md)) → skew is the pathology no index fixes ([10](10-data-skew.md)) → skinny tables are the last resort ([11](11-skinny-tables-and-support-levers.md)). **Writes:** locking ([12](12-record-locking-and-concurrency.md)) → deletion, which is not what it looks like ([13](13-deletes-recycle-bin-and-physical-deletion.md)) → the tier below ([14](14-big-objects-and-the-archive-tier.md)). **[10](10-data-skew.md) is the hinge** — it appears in both.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | [Data model design principles](01-data-model-design-principles.md) | standard-first, normalization vs reporting pressure | 14 |
| 02 | [Relationships deep dive](02-relationships-deep-dive.md) | cascade, reparenting, roll-up availability, sharing consequences | 14 |
| 03 | [Record IDs, external IDs & upsert](03-record-ids-external-ids-and-upsert.md) | 15 vs 18 char, the 25-field ceiling, upsert matching | 14 |
| 04 | [Standard CRM object map](04-standard-crm-object-map.md) | core object graph, the pricing chain, polymorphic keys | 14 |
| 05 | [Person Accounts & one-way modeling decisions](05-person-accounts-and-one-way-modeling-decisions.md) | no disable path, two records per person, the wider family | 14 |
| 06 | [Storage model & schema limits](06-storage-model-and-schema-limits.md) | ~2 KB per record, three allocations, what actually binds | 14 |
| 07 | [Large data volume fundamentals](07-large-data-volume-fundamentals.md) | where the platform degrades and why | 14 |
| 08 | [Indexes & query selectivity](08-indexes-and-query-selectivity.md) | standard/custom indexes, **30/15 and 10/5 thresholds** | 14 |
| 09 | [Query Plan & performance tuning](09-query-plan-and-performance-tuning.md) | **cost > 1.0 is non-selective**, leading operation types | 14 |
| 10 | [Data skew](10-data-skew.md) | account, ownership and lookup skew; the 10,000 threshold | 14 |
| 11 | [Skinny tables & support levers](11-skinny-tables-and-support-levers.md) | 100 columns, no formulas, Support-only | 14 |
| 12 | [Record locking & concurrency](12-record-locking-and-concurrency.md) | the 10-second wait, parent locks, sort by parent Id | 14 |
| 13 | [Deletes, the Recycle Bin & physical deletion](13-deletes-recycle-bin-and-physical-deletion.md) | soft delete still costs; hard delete and purge | 14 |
| 14 | [Big objects & the archive tier](14-big-objects-and-the-archive-tier.md) ⚠️ | **Async SOQL retired Summer '23**; immutable index | 14 |
| 15 | Archiving & retention strategy 🆕 | native archiving, offload to Data 360, policy design | 15 |
| 16 | Bulk loading strategy for LDV ⚠️ | Bulk API 2.0, PK chunking, defer sharing, load order | 15 |
| 17 | External objects vs replicated copies | federation trade-offs, indirect lookups | 15 |
| 18 | Zero-copy & Data 360 as data tier 🆕 | federate instead of migrate; when it actually fits | 15 |
| 19 | Data quality, deduplication & MDM | matching rules, golden record, survivorship | 15 |
| 20 | Sandboxes, seeding & Data Mask | sandbox types, seeding templates, masking policy | 15 |
| 21 | Backup, restore & recovery ⚠️ | no free recovery service; RPO/RTO design | 15 |
| 22 | Multi-currency, multi-language & locale | dated exchange rates, translation and locale effects | 15 |
| 23 | Hyperforce, residency & data locality 🆕 | regions, migration effects, latency and compliance | 15 |
| 24 | Data architecture review checklist | sizing, skew, growth, archival, cert-aligned recap | 15 |

## Related

- **[10](10-data-skew.md)** pairs with [07-security · 16 Sharing recalculation](../07-security-and-sharing/16-sharing-recalculation-and-performance.md) — ownership skew is a sharing problem first, and that note (phase 11) owns the recalculation mechanics.
- **[12](12-record-locking-and-concurrency.md)** is where three earlier notes were already pointing — [01-admin · 13](../01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md), [06-integration · 07](../06-integration-and-apis/07-bulk-api-2.md) and [06-integration · 23](../06-integration-and-apis/23-idempotency-retries-and-error-handling.md) all deferred lock contention to this area.
- **[14](14-big-objects-and-the-archive-tier.md)** is the storage behind [07-security · 22 Field Audit Trail](../07-security-and-sharing/22-field-audit-trail-and-data-retention.md) — `FieldHistoryArchive` is one, and archive queries obey big-object index rules.
- **16** depends on [06-integration · 07 Bulk API 2.0](../06-integration-and-apis/07-bulk-api-2.md).
- **17** pairs with [06-integration · 20 Salesforce Connect](../06-integration-and-apis/20-salesforce-connect-and-external-objects.md).
- **18** is the seam into [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md) — zero-copy federation is a Data 360 topic seen from the core-platform side.
- **20** overlaps [09-devops · 06 Source tracking & sandbox workflow](../09-devops-sfdx-and-release-management/INDEX.md).

## Seed notes

[_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) maps three pages here, all inspected in phase 14: `QUERY PLAN` (2025) → [09](09-query-plan-and-performance-tuning.md), current but wrong about how custom indexes are created; `Optimization work` (2023) → [08](08-indexes-and-query-selectivity.md), a non-indexable ultimate-parent formula; `Lead Broker Field Migration` (2023) → [02](02-relationships-deep-dive.md), really a deployment checklist whose surviving lesson is that renaming a relationship breaks report types.
