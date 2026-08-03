# 08 · Data Modeling & Large Data Volumes

Model it well, then keep it fast past 10M rows. **26 topics** · phases [14](PHASES.md), [15](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> 📌 **Movable block.** Nothing downstream depends on this area, so phases 14–15 can run any time after phase 02 if you want the data layer early.

**How to read 06–14.** They are two arguments, not nine notes. **Reads:** volume degrades ([07](07-large-data-volume-fundamentals.md)) → because queries stop being selective ([08](08-indexes-and-query-selectivity.md)) → which you diagnose with Query Plan ([09](09-query-plan-and-performance-tuning.md)) → skew is the pathology no index fixes ([10](10-data-skew.md)) → skinny tables are the last resort ([11](11-skinny-tables-and-support-levers.md)). **Writes:** locking ([12](12-record-locking-and-concurrency.md)) → deletion, which is not what it looks like ([13](13-deletes-recycle-bin-and-physical-deletion.md)) → the tier below ([14](14-big-objects-and-the-archive-tier.md)). **[10](10-data-skew.md) is the hinge** — it appears in both.

**How to read 15–26.** Physics gives way to **operations**, in three runs. **Lifecycle:** what you keep ([15](15-archiving-and-retention-strategy.md)) → how it gets in ([16](16-bulk-loading-strategy-for-ldv.md)) → the project that puts it there ([25](25-data-migration-and-cutover.md)) → how good it is ([19](19-data-quality-deduplication-and-mdm.md)). **Reach:** copy or federate ([17](17-external-objects-vs-replicated-copies.md)) → the 2026 third option ([18](18-zero-copy-and-data-360-as-data-tier.md)) → across orgs ([26](26-cross-org-data-sharing-and-consolidation.md)). **Continuity:** non-production data ([20](20-sandboxes-seeding-and-data-mask.md)) → getting it back ([21](21-backup-restore-and-recovery.md)) → where it physically runs ([23](23-hyperforce-residency-and-data-locality.md)). [24](24-data-architecture-review-checklist.md) audits all of it.

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
| 15 | [Archiving & retention strategy](15-archiving-and-retention-strategy.md) 🆕 | **Salesforce Archive**, retention vs purge, the 1M/day cap | 15 |
| 16 | [Bulk loading strategy for LDV](16-bulk-loading-strategy-for-ldv.md) ⚠️ | **PK chunking is a v1 header**, defer sharing, load order | 15 |
| 17 | [External objects vs replicated copies](17-external-objects-vs-replicated-copies.md) ⚠️ | **Hyperforce removed the OData ceilings**; indirect lookups | 15 |
| 18 | [Zero-copy & Data 360 as data tier](18-zero-copy-and-data-360-as-data-tier.md) 🆕 | query vs **File Federation on Iceberg**; when it's a latency trap | 15 |
| 19 | [Data quality, deduplication & MDM](19-data-quality-deduplication-and-mdm.md) | merging is destructive; survivorship; the four MDM styles | 15 |
| 20 | [Sandboxes, seeding & Data Mask](20-sandboxes-seeding-and-data-mask.md) 🆕 | **Data Mask & Seed**; 200 MB → production, 1 → 29 days | 15 |
| 21 | [Backup, restore & recovery](21-backup-restore-and-recovery.md) ⚠️ | **the $10,000 service still exists**; nothing is backed up by default | 15 |
| 22 | [Multi-currency, multi-language & locale](22-multi-currency-multi-language-and-locale.md) | irreversible; dated rates are Opportunity-only | 15 |
| 23 | [Hyperforce, residency & data locality](23-hyperforce-residency-and-data-locality.md) 🆕⚠️ | **delays ended 1 Jul 2026**; JPG not SVG previews | 15 |
| 24 | [Data architecture review checklist](24-data-architecture-review-checklist.md) | the hour-long audit, linking every number rather than restating it | 15 |
| 25 | [Data migration & cutover](25-data-migration-and-cutover.md) | external-ID keying, dry run, reconciliation, rollback, freeze | 15 |
| 26 | [Cross-org data sharing & consolidation](26-cross-org-data-sharing-and-consolidation.md) ⚠️🆕 | **S2S retires Spring '27**; Data Cloud One; org merges | 15 |

## Related

- **[10](10-data-skew.md)** pairs with [07-security · 16 Sharing recalculation](../07-security-and-sharing/16-sharing-recalculation-and-performance.md) — ownership skew is a sharing problem first, and that note (phase 11) owns the recalculation mechanics.
- **[12](12-record-locking-and-concurrency.md)** is where three earlier notes were already pointing — [01-admin · 13](../01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md), [06-integration · 07](../06-integration-and-apis/07-bulk-api-2.md) and [06-integration · 23](../06-integration-and-apis/23-idempotency-retries-and-error-handling.md) all deferred lock contention to this area.
- **[14](14-big-objects-and-the-archive-tier.md)** is the storage behind [07-security · 22 Field Audit Trail](../07-security-and-sharing/22-field-audit-trail-and-data-retention.md) — `FieldHistoryArchive` is one, and archive queries obey big-object index rules.
- **[16](16-bulk-loading-strategy-for-ldv.md)** depends on [06-integration · 07 Bulk API 2.0](../06-integration-and-apis/07-bulk-api-2.md).
- **[17](17-external-objects-vs-replicated-copies.md)** pairs with [06-integration · 20 Salesforce Connect](../06-integration-and-apis/20-salesforce-connect-and-external-objects.md).
- **[18](18-zero-copy-and-data-360-as-data-tier.md)** is the seam into [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md) — zero-copy federation is a Data 360 topic seen from the core-platform side, and that vault owns the connector status table.
- **[20](20-sandboxes-seeding-and-data-mask.md)** overlaps [09-devops · 06 Source tracking & sandbox workflow](../09-devops-sfdx-and-release-management/INDEX.md) — this note owns the *data*, that one owns source tracking.
- **[23](23-hyperforce-residency-and-data-locality.md)** pairs with [09-devops · 21](../09-devops-sfdx-and-release-management/INDEX.md) — same platform shift, data side vs ops side.
- **[25](25-data-migration-and-cutover.md)** and **[26](26-cross-org-data-sharing-and-consolidation.md)** were added in phase 15; see [PHASES.md](PHASES.md) for why.

## Seed notes

[_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) maps three pages here, all inspected in phase 14 and all consumed by it: `QUERY PLAN` (2025) → [09](09-query-plan-and-performance-tuning.md), current but wrong about how custom indexes are created; `Optimization work` (2023) → [08](08-indexes-and-query-selectivity.md), a non-indexable ultimate-parent formula; `Lead Broker Field Migration` (2023) → [02](02-relationships-deep-dive.md), really a deployment checklist whose surviving lesson is that renaming a relationship breaks report types. **Phase 15 harvested nothing** — the corpus contains no page on retention, backup, federation, sandboxes or residency.
