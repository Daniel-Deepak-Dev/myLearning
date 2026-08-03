# Phases for 08 · Data Modeling & Large Data Volumes

24 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> 📌 **Movable block.** Nothing downstream depends on this area. Phase 15 can run any time you want the data layer finished.

---

## Phase 14 — Data modeling & LDV performance · 14 files ✅

```
01-data-model-design-principles.md
02-relationships-deep-dive.md
03-record-ids-external-ids-and-upsert.md
04-standard-crm-object-map.md
05-person-accounts-and-one-way-modeling-decisions.md    ← added
06-storage-model-and-schema-limits.md                   ← added
07-large-data-volume-fundamentals.md
08-indexes-and-query-selectivity.md
09-query-plan-and-performance-tuning.md
10-data-skew.md
11-skinny-tables-and-support-levers.md
12-record-locking-and-concurrency.md                    ← added
13-deletes-recycle-bin-and-physical-deletion.md         ← added
14-big-objects-and-the-archive-tier.md          ⚠️      ← renamed
```

### What the plan got wrong

**"No 🆕 or ⚠️ in this run — it's stable platform physics."** That sentence was in this file, and it was false. The planned `10-big-objects-and-async-soql.md` named a feature **retired in Summer '23**. Help article **000394892** is explicit: *"You must use the Bulk API or batch Apex to query or report on custom Big Objects after your org gets upgraded to the Summer '23 release."* Big objects are **not** retired — only the query mechanism. The file was renamed and now opens with the correction.

**This inverts the vault's usual failure mode**, which is why it earned a rule rather than just a fix. The nine corrections logged in [../CURRENCY.md](../CURRENCY.md) were all *"called dead but actually alive"*; phase 13's was a correct retirement carrying a wrong date. This is the first **"assumed alive, actually dead"** — and the standing greps only ever guarded one direction.

### Why four files were added

- **12** was not optional. Three shipped notes already forward-linked to this area for lock contention — [01-admin · 13](../01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md), [06-integration · 07](../06-integration-and-apis/07-bulk-api-2.md), [06-integration · 23](../06-integration-and-apis/23-idempotency-retries-and-error-handling.md) — and no planned file owned it. The area was carrying a promise it could not keep.
- **13** is the missing half of LDV: every plan designs the load and none designs the delete, so orgs accumulate soft-deleted rows that are invisible to users and fully visible to the optimizer.
- **06** and **05** cover the two questions asked in every real design review — what does this cost, and which switches cannot be undone.

### Renumbering — free again, for the third time

Area 08 had **no files**, and all ~25 inbound links pointed at `INDEX.md`. Five named a file by number, but only in link **text**, and the approved link sweep touched those files anyway. So the area was renumbered into learning order rather than appended to, as in phases 10 and 12 — the opposite call from phase 13, which appended because real numbered targets existed. **Phase 15 shifted 11–20 → 15–24.**

### Seed harvest — all three pages inspected

- `QUERY PLAN` (**2025**) → **09**. ✅ Genuinely current, and its worked example (TableScan 1.5 → Index 0.5) is correct. **One error corrected:** it says custom indexes are created *"by requesting Salesforce Support or enabling them in Setup"* — there is no Setup screen for custom indexes. It also never states that **1.0 is the threshold**, which is the only number you actually use.
- `Optimization work` (2023) → **08**, not 09/10 as planned. Its content is a single **ultimate-parent formula field**, eleven nested `IF`s walking an Account hierarchy — cross-object, therefore **non-deterministic and permanently non-indexable**, and sitting at both the 10-relationship traversal ceiling and the 10-unique-relationships-per-object ceiling. Kept as the worked example of why materialising beats computing at read time.
- `Lead Broker Field Migration` (2023) → **02**. Not a data-migration note at all: a deployment checklist about report types and fields missing between sandboxes. Its durable lesson is that **a relationship's API name is schema, and report types are built on relationship paths**, so renaming one commits you to a report-type deployment. Its natural long-term home is area 09.

---

## Phase 15 — Retention, federation & data operations · 10 files ⬜

```
15-archiving-and-retention-strategy.md             🆕
16-bulk-loading-strategy-for-ldv.md                ⚠️
17-external-objects-vs-replicated-copies.md
18-zero-copy-and-data-360-as-data-tier.md          🆕
19-data-quality-deduplication-and-mdm.md
20-sandboxes-seeding-and-data-mask.md
21-backup-restore-and-recovery.md                  ⚠️
22-multi-currency-multi-language-and-locale.md
23-hyperforce-residency-and-data-locality.md       🆕
24-data-architecture-review-checklist.md
```

**⚠️ corrections to lead with**
- **16** — Bulk API 2.0, and the **operational levers** most guides omit: defer sharing calculation, load order by dependency, PK chunking for extraction (a **v1** header — see [06-integration · 07](../06-integration-and-apis/07-bulk-api-2.md)). Lock contention is already owned by [12](12-record-locking-and-concurrency.md); link, don't restate.
- **21** — **there is no free recovery service.** Salesforce's paid data recovery was discontinued and then reintroduced as a product. Design RPO/RTO deliberately; "Salesforce backs it up" is not a plan.

**🆕 — research before writing:** **15** (native archiving + offload to Data 360), **18** (zero-copy), **23** (Hyperforce residency).

> **Re-verify the corrections themselves, not only what they correct.** Phases 10, 11 and 14 each found the *plan's own framing* stale. For **21** in particular, confirm the current state of Salesforce's backup and recovery products against Help before writing a word — this is precisely the shape of claim that goes out of date quietly.

**Notes on scope**
- **18** is the seam into [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md) — same topic from the core-platform side. The useful content is **when federation genuinely fits vs when it's a latency trap**. Link across; don't restate Data 360 architecture.
- **17 and 18 overlap deliberately**: 17 is the classic Salesforce Connect trade-off, 18 is the 2026 answer. Write 17 first, then let 18 update it. Note that Salesforce Connect's per-hour ceilings are **gone on Hyperforce** — phase 13 found that, and it changes the copy-or-federate maths.
- **15** must not duplicate [14](14-big-objects-and-the-archive-tier.md). That note owns the big-object **mechanism**; 15 owns **policy** — what to archive, when, and to which tier.
- **20** overlaps [09-devops · 06](../09-devops-sfdx-and-release-management/INDEX.md); this note owns **data** (seeding, masking policy), that one owns **source tracking**.
- **24** is the capstone — a review checklist, not prose. It should let you audit an unfamiliar org in an hour, and it should reuse the numbers already published in [06](06-storage-model-and-schema-limits.md), [08](08-indexes-and-query-selectivity.md), [10](10-data-skew.md) and [12](12-record-locking-and-concurrency.md) rather than restating them.
