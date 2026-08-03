# Data Migration & Cutover

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** The shape of a one-off migration project, from profiling the source to the weekend it goes live. The loading *levers* are [16](16-bulk-loading-strategy-for-ldv.md); the tools are [01-admin · 13](../01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md).

## Core idea

A migration is not a big load. It is a **reconciliation project with a load in the middle**, and the load is the part least likely to fail. What fails is that nobody can prove the 4.2 million rows in the new org are the same 4.2 million rows that were in the old system, so go-live becomes an argument instead of a decision.

Everything below exists to make that provable. The single highest-leverage decision is to **carry the legacy key into Salesforce as a unique External ID on every object**. It makes loads idempotent, makes a failed run safe to re-run, makes reconciliation a join rather than a spreadsheet, and gives you the only practical rollback you will have → [03](03-record-ids-external-ids-and-upsert.md).

## How it works

- **Profile before mapping.** Row counts, null rates, distinct values, orphan rates, date ranges. Mapping decisions made without these numbers get revisited during the cutover weekend.
- **Sequence by dependency.** Parents before children, lookups before referrers. Self-lookups and circular references need two passes: insert, then update the reference.
- **Suppress what you can; plan around what you cannot.** Triggers and flows take a bypass switch; **validation and duplicate rules fire on every API row regardless**, so budget for a rejects file and a retry loop → [16](16-bulk-loading-strategy-for-ldv.md).
- **Spread ownership deliberately.** Loading every record to one integration user manufactures ownership skew on day one → [10](10-data-skew.md).
- **Dry-run at full volume in a Full sandbox.** It is the only environment where the timings are real, and the measured duration is what the cutover plan is built from → [20](20-sandboxes-seeding-and-data-mask.md).
- **Reconcile on numbers, not vibes:** row counts per object, sums of the amounts finance cares about, orphan counts, and a sampled field-level diff. Sign-off is against that report.
- **Cutover is a sequence with a freeze in it** — freeze the source, load the delta, verify, switch users over, and know who is allowed to write during the window.
- **Stabilise afterwards:** re-enable automation, backfill everything the bypass skipped (roll-ups, derived flags, history), resume sharing recalculation, and hold a hypercare period.

## 2026 currency

Two platform defaults have moved under older migration runbooks. **Apex runs in user mode at API 67.0**, so a migration utility class that used to see everything now sees what its running user sees — and it fails by processing a subset, not by throwing → [02-apex · 14](../02-apex-and-triggers/14-batch-apex-and-stateful-processing.md). And the **asynchronous sharing recalculation** Release Update means post-load assertions about share rows may not be true immediately, which breaks verification scripts that check access straight after a load → [07-security · 16](../07-security-and-sharing/16-sharing-recalculation-and-performance.md). Both are silent failures, which is the worst kind to meet at 2 a.m. on a Sunday.

## Gotchas

- **Rollback has to be designed in.** Stamp every migrated record with a batch identifier; without it, "undo the load" means finding the rows first.
- **A hard delete is the only rollback that frees storage**, and soft-deleted rows keep degrading queries meanwhile → [13](13-deletes-recycle-bin-and-physical-deletion.md).
- **Throughput does not extrapolate linearly.** The second 10 million rows are slower than the first — indexes, sharing and skew all grow.
- **Date and number parsing follows the running user's locale**, which is how 03/04 becomes the wrong month in production → [22](22-multi-currency-multi-language-and-locale.md).
- **Migrating "everything" is a decision nobody made.** Legacy data you never intended to keep arrives with a retention obligation attached → [15](15-archiving-and-retention-strategy.md).
- **Deduplicate before the load, not after.** Merging in Salesforce is destructive and reparents children; filtering a source file is neither → [19](19-data-quality-deduplication-and-mdm.md).
- **The delta window is where migrations actually go wrong** — records edited in the source after the main extract and before the freeze.

## Recall

Q: What is the single most valuable structural decision in a Salesforce migration?
A: Carrying the legacy key into a unique External ID on every object — it makes loads idempotent, re-runnable, reconcilable and reversible.

Q: Which save-time rules cannot be suppressed for a migration load?
A: Validation rules and duplicate rules — they fire on every API-written row.

Q: Why must the dry run happen in a Full sandbox?
A: It is the only environment with production-scale data, so it is the only place the timings and LDV behaviour are real.

Q: What does reconciliation actually consist of?
A: Row counts per object, sums of business-critical amounts, orphan counts and a sampled field-level diff — the report that sign-off is given against.

Q: What has to happen after the load that the load itself skipped?
A: Backfilling everything the automation bypass suppressed — roll-ups, derived fields, history — plus resuming sharing recalculation.

## Related

- [16 · Bulk loading strategy for LDV](16-bulk-loading-strategy-for-ldv.md) — the levers this project pulls
- [19 · Data quality, deduplication & MDM](19-data-quality-deduplication-and-mdm.md) — clean before you load, not after
- [26 · Cross-org data sharing & consolidation](26-cross-org-data-sharing-and-consolidation.md) — the same project when the source is another Salesforce org
- [01-admin · 13 Data import, export & loading tools](../01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md) — what you actually run the load with
