# Phases for 08 · Data Modeling & Large Data Volumes

20 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> 📌 **Movable block.** Nothing downstream depends on this area. Phases 14–15 can run any time after phase 02 if you want the data layer early.

---

## Phase 14 — Data modeling & LDV performance · 10 files ⬜

```
01-data-model-design-principles.md
02-relationships-deep-dive.md
03-record-ids-external-ids-and-upsert.md
04-standard-crm-object-map.md
05-large-data-volume-fundamentals.md
06-indexes-and-query-selectivity.md
07-query-plan-and-performance-tuning.md
08-data-skew.md
09-skinny-tables-and-support-levers.md
10-big-objects-and-async-soql.md
```

No 🆕 or ⚠️ in this run — it's stable platform physics. That makes it the **best candidate to run early** if you want a quick win.

**Notes on scope**
- **02** — the real content is the **consequences**: cascade delete, reparenting rules, roll-up availability, and the sharing implications of master-detail. Not the definition list.
- **05–09 are one argument in five parts.** Write them as a chain: the platform degrades → because queries stop being selective → which you diagnose with Query Plan → skew is the specific pathology → skinny tables are the last resort. If they read as five independent notes, the phase failed.
- **06** — give the **actual selectivity thresholds** (the percentage-of-rows rules for standard vs custom indexes). That number is the whole reason the topic exists.
- **08** — give the **actual record counts** where ownership, lookup and account skew start to hurt.
- **09** — be honest: skinny tables are a **support request**, not a self-service feature, and they come with real constraints.

**Seed harvest** ([../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md)) — `QUERY PLAN` (2025) → **07**, one of the few current pages in the corpus. `Optimization work` (2023) → **07**/**08**.

---

## Phase 15 — Retention, federation & data operations · 10 files ⬜

```
11-archiving-and-retention-strategy.md             🆕
12-bulk-loading-strategy-for-ldv.md                ⚠️
13-external-objects-vs-replicated-copies.md
14-zero-copy-and-data-360-as-data-tier.md          🆕
15-data-quality-deduplication-and-mdm.md
16-sandboxes-seeding-and-data-mask.md
17-backup-restore-and-recovery.md                  ⚠️
18-multi-currency-multi-language-and-locale.md
19-hyperforce-residency-and-data-locality.md       🆕
20-data-architecture-review-checklist.md
```

**⚠️ corrections to lead with**
- **12** — Bulk API 2.0, and the **operational levers** most guides omit: defer sharing calculation, load order by dependency, PK chunking for extraction.
- **17** — **there is no free recovery service.** Salesforce's paid data recovery was discontinued and then reintroduced as a product. Design RPO/RTO deliberately; "Salesforce backs it up" is not a plan.

**🆕 — research before writing:** **11** (native archiving + offload to Data 360), **14** (zero-copy), **19** (Hyperforce residency).

**Notes on scope**
- **14** is the seam into [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md) — same topic from the core-platform side. The useful content is **when federation genuinely fits vs when it's a latency trap**. Link across; don't restate Data 360 architecture.
- **13 and 14 overlap deliberately**: 13 is the classic Salesforce Connect trade-off, 14 is the 2026 answer. Write 13 first, then let 14 update it.
- **16** overlaps [09-devops · 06](../09-devops-sfdx-and-release-management/INDEX.md); this note owns **data** (seeding, masking policy), that one owns **source tracking**.
- **20** is the capstone — a review checklist, not prose. It should let you audit an unfamiliar org in an hour.
