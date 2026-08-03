# Data Architecture Review Checklist

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** The capstone — auditing an unfamiliar org's data layer in about an hour. Every number lives in the note that owns it and is **linked, not restated**, because half-quoting a threshold is how this area's facts go wrong.

## Core idea

A data review is not an inventory. It is a search for the four failures that actually cost money: **queries that stopped being selective**, **writes that contend**, **growth nobody owns**, and **a recovery story that has never been tested**. Everything below is arranged to find those quickly, in the order that surfaces the worst news first.

Run it against a production org, not a sandbox. Sandboxes under-report by construction — volume-driven behaviour, skinny tables and sharing recalculation mode all differ → [20](20-sandboxes-seeding-and-data-mask.md).

## How it works

| Pass | Ask | Where the answer is |
|---|---|---|
| **Size** | Which objects hold >1M rows? What is the storage split and the growth rate? | [06](06-storage-model-and-schema-limits.md), [07](07-large-data-volume-fundamentals.md) |
| **Model** | Master-detail vs lookup, reparenting, roll-ups; any one-way switches already taken? | [02](02-relationships-deep-dive.md), [05](05-person-accounts-and-one-way-modeling-decisions.md) |
| **Keys** | Does every integrated object have a unique External ID? | [03](03-record-ids-external-ids-and-upsert.md) |
| **Reads** | Are the hot queries selective? Run Query Plan on the worst three. | [08](08-indexes-and-query-selectivity.md), [09](09-query-plan-and-performance-tuning.md) |
| **Skew** | Any parent or owner over the threshold? Check the integration user first. | [10](10-data-skew.md) |
| **Writes** | Lock failures in the logs? Loads sorted by parent? Sharing recalc deferred? | [12](12-record-locking-and-concurrency.md), [16](16-bulk-loading-strategy-for-ldv.md) |
| **Deletes** | How much of the row count is soft-deleted and still being scanned? | [13](13-deletes-recycle-bin-and-physical-deletion.md) |
| **Lifecycle** | Is there a written retention policy per object, with an owner and a schedule? | [15](15-archiving-and-retention-strategy.md) |
| **Quality** | Duplicate rate on the core objects; which system masters which field? | [19](19-data-quality-deduplication-and-mdm.md) |
| **Reach** | What is copied in that could be federated — or queried in place? | [17](17-external-objects-vs-replicated-copies.md), [18](18-zero-copy-and-data-360-as-data-tier.md) |
| **Non-prod** | Is production PII sitting unmasked in any sandbox? | [20](20-sandboxes-seeding-and-data-mask.md) |
| **Continuity** | What is the RPO/RTO, who signed it, and when was a restore last rehearsed? | [21](21-backup-restore-and-recovery.md) |
| **Locality** | Which region, and does anything still call an instanced hostname? | [23](23-hyperforce-residency-and-data-locality.md) |

- **The fastest three findings**, in order: an unmasked Full sandbox, an integration user owning millions of records, and a retention policy that does not exist.
- **Ask for the growth *rate*, not the size.** A 4M-row object growing 200k a month is a different conversation from one that stopped growing in 2021.
- **Every "we'll clean it later" is a finding.** Write it down with the date it was said.

## 2026 currency

Four questions belong on a checklist written before 2026 and are missing from every one of them. **Where does the org run** — Hyperforce migration delays ended 1 July 2026 → [23](23-hyperforce-residency-and-data-locality.md). **Is anything still on Salesforce-to-Salesforce**, which stops functioning in Spring '27 → [26](26-cross-org-data-sharing-and-consolidation.md). **Is backup a product or a hope**, given nothing is backed up by default → [21](21-backup-restore-and-recovery.md). And **what would an agent see** — grounding reaches live records, so duplicates and stale rows now produce confident wrong answers rather than untidy reports → [19](19-data-quality-deduplication-and-mdm.md).

## Gotchas

- **Do not restate a threshold from memory.** Standard and custom index selectivity have four numbers and a cap each; quote them from [08](08-indexes-and-query-selectivity.md) or not at all.
- **Query Plan cost is relative to the threshold** — the line is 1.0, and it means non-selective above it → [09](09-query-plan-and-performance-tuning.md).
- **Skinny tables are invisible to you.** You cannot see them in Setup; ask Support or ask the org's history → [11](11-skinny-tables-and-support-levers.md).
- **A clean Recycle Bin does not mean deleted rows are gone** — physical purge lags → [13](13-deletes-recycle-bin-and-physical-deletion.md).
- **"We have backups" usually means the weekly export**, whose files are deleted 48 hours after the email → [21](21-backup-restore-and-recovery.md).
- **Reviewing in a sandbox invalidates half the findings.** Say so in the report rather than caveating each line.
- **The output is a prioritised list with owners**, not a document. A review nobody is assigned to is an inventory again.

## Recall

Q: What four failures is a data architecture review actually hunting for?
A: Non-selective queries, contended writes, unowned growth, and an untested recovery story.

Q: Why must the review run against production?
A: Sandboxes differ in volume, skinny tables and sharing recalculation mode, so volume-driven problems do not reproduce.

Q: What are the three fastest findings in a typical org?
A: An unmasked Full sandbox, an integration user owning millions of records, and a missing retention policy.

Q: Which four questions does a pre-2026 checklist omit?
A: Which region the org runs in, whether anything still uses S2S, whether backup was actually purchased, and what an agent would see.

Q: What form should the output take?
A: A prioritised list of findings with named owners — not a document.

## Related

- [07 · Large data volume fundamentals](07-large-data-volume-fundamentals.md) — the argument this checklist operationalises
- [15 · Archiving & retention strategy](15-archiving-and-retention-strategy.md) — the finding most orgs fail on
- [21 · Backup, restore & recovery](21-backup-restore-and-recovery.md) — the finding with the highest consequence
- [01 · Data model design principles](01-data-model-design-principles.md) — where the review's recommendations land
