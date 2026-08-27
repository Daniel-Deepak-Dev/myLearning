# Phases for 08 · Data Modeling & Large Data Volumes

26 topics across 2 runs — **area complete.** Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> 📌 **Movable block.** Nothing downstream depended on this area, which is why it ran out of numeric order.

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

## Phase 15 — Retention, federation & data operations · 12 files ✅

```
15-archiving-and-retention-strategy.md             🆕
16-bulk-loading-strategy-for-ldv.md                ⚠️
17-external-objects-vs-replicated-copies.md        ⚠️     ← flag added
18-zero-copy-and-data-360-as-data-tier.md          🆕
19-data-quality-deduplication-and-mdm.md
20-sandboxes-seeding-and-data-mask.md              🆕     ← flag added
21-backup-restore-and-recovery.md                  ⚠️
22-multi-currency-multi-language-and-locale.md
23-hyperforce-residency-and-data-locality.md       🆕⚠️   ← flag added
24-data-architecture-review-checklist.md
25-data-migration-and-cutover.md                          ← added
26-cross-org-data-sharing-and-consolidation.md     ⚠️🆕   ← added
```

### What the plan got wrong — five findings

The area file told this phase to **re-verify the corrections themselves, not only what they correct**. That instruction paid for itself: the phase's headline ⚠️ was wrong, and three more topics had moved under it.

**1. The ⚠️ for 21 conflated a service with a product, and called a live service dead.** The plan said *"there is no free recovery service — Salesforce's paid data recovery was discontinued and then reintroduced as a product."* Two lineages:

- The **Data Recovery Service** — Support-requested, retired 31 Jul 2020, **reinstated 2021, still available in 2026**: **$10,000**, **6–8 weeks**, **data only, no metadata**, returned as **CSV you re-import yourself**, ~3 months of history, no guarantee. It came back as a *service*, not a product.
- The **products** — *Backup and Restore* (2021) → renamed **Salesforce Backup** → and after the **Own Company acquisition** (announced Sept 2024), **Salesforce Backup & Recover** (formerly Own Recover / OwnBackup), with **Backup & Recover Next** announced as its successor.

The durable point survives — *"Salesforce backs it up" is not a plan* — but the note now states the service **exists**, and is priced, slow and data-only. That is the stronger argument for designing RPO/RTO, not the weaker one.

**2. The Own acquisition reshaped three planned topics at once.** Help **004634031** (11 Jul 2026) names the suite: **Backup & Recovery, Archive, Seed, Discover** — landing on **15**, **20** and **21** simultaneously. Any of the three written without it reproduces the 2023 answer.

**3. "Native archiving" is now a named product with policy semantics.** **Salesforce Archive** has **archive policies** and a **retention vs purge** distinction: retention deletes on expiry, **purge deletes ad hoc outside the retention period** — which is how right-to-be-forgotten is served. **Purge is capped at 1,000,000 records/day**, and **editing a retention period applies retroactively** to everything already archived through that policy. It is licensed and partly a managed package, so **15** gives a policy that works with or without it.

**4. Topic 23 needed a ⚠️, because the date had already passed.** Salesforce Help: *"Starting July 1, 2026, it is no longer possible to delay upgrades to Hyperforce."* Five weeks before the phase ran. Concrete developer-visible consequence: **file previews are generated as JPG, not SVG**, regardless of preference — pre-migration SVGs survive, new uploads do not.

**5. Topic 18 is two features at different maturities, under a renamed product.** *Query federation* and **File Federation** (Apache Iceberg, read at the storage layer with Data 360's own compute — **no external compute bill**) are separate; AWS Glue is GA while Fabric OneLake is Beta, and [AI_Data](../../AI_Data/01-data-cloud/06-zero-copy-byol/notes.md) owns that table. **Data Cloud was renamed Data 360 on 14 Oct 2025**, so every older source uses the old name.

### The retirement nobody had recorded

**Salesforce-to-Salesforce is genuinely dying** (Help **005103355**): no new enablement from **Spring '26**, **support ended Summer '26**, **fully retired and non-functional in Spring '27**. Replacements named by Salesforce: Partner Cloud, Data Cloud One, MuleSoft Anypoint, MuleSoft for Flow.

This is the **second** "old *and* dead" finding in the build, after phase 14's Async SOQL — and the vault had no note on S2S at all, so nothing was wrong, only missing. It is the reason **26** exists rather than a paragraph in 17.

### Why two files were added, and why they were appended

- **25** — [16](16-bulk-loading-strategy-for-ldv.md) owns the *levers*; nothing owned the *project*. Profiling, external-ID keying, dependency sequencing, dry run, reconciliation, rollback and the cutover freeze are a different discipline from job configuration, and it is the work most often actually asked for.
- **26** — carries the S2S deadline, plus the cross-org adapter's Summer '26 named credential support and the consolidation-is-three-projects argument.

**Appended as 25–26, not renumbered.** Unlike phase 14, this area now has real inbound references by number: [06-integration · INDEX](../06-integration-and-apis/INDEX.md) names **· 17**, [06-integration · 13](../06-integration-and-apis/13-change-data-capture.md) names **· 18**, and [09-devops · INDEX](../09-devops-sfdx-and-release-management/INDEX.md) and its `PHASES.md` name **· 23**. Renumbering would have broken four references to buy nothing — the same call phase 13 made, and the opposite of phase 14's.

### Seed harvest — nothing to harvest

[../\_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) maps three pages to this area and **phase 14 consumed all three**. The corpus contains no page on retention, backup, federation, sandboxes, migration or residency, so this run has **no `> **From my notes.**` callouts** — stated here so the absence reads as a fact rather than an omission.

### Scope boundaries held

- **15** owns retention *policy*; [14](14-big-objects-and-the-archive-tier.md) keeps the big-object *mechanism*.
- **17** owns the copy-or-federate *decision*; [06-integration · 20](../06-integration-and-apis/20-salesforce-connect-and-external-objects.md) keeps adapters and relationships.
- **18** links to [AI_Data](../../AI_Data/01-data-cloud/06-zero-copy-byol/notes.md) for connector status rather than restating it.
- **19** links to [01-admin · 08](../01-admin-and-declarative-platform/08-validation-rules-and-duplicate-management.md) for matching/duplicate rule mechanics.
- **20** owns sandbox *data*; [09-devops](../09-devops-sfdx-and-release-management/INDEX.md) keeps source tracking.
- **24** links every threshold to the note that owns it — no number is restated, because half-quoting is how this area's facts go wrong.
