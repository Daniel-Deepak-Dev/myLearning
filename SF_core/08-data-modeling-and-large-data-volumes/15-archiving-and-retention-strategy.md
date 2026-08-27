# Archiving & Retention Strategy

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** The policy layer — what to keep, for how long, and on which tier. The big-object *mechanism* is [14](14-big-objects-and-the-archive-tier.md); the legal drivers are [07-security · 25](../07-security-and-sharing/25-privacy-consent-and-data-protection.md).

## Core idea

Archiving is not a storage exercise. It is a decision about **which questions you will still need to answer in five years, and how fast**. Once you can state that, the tier picks itself — data you must query interactively stays live, data you must be *able* to produce stays on a cheap tier, and data you are obliged to destroy has a deletion date rather than an archive date.

The mistake that makes archiving projects fail is treating it as a one-off cleanup. Retention is a **standing policy attached to an object**, running on a schedule, with an owner. A cleanup buys you eighteen months; a policy is the thing that keeps the org sized.

## How it works

| Tier | Query story | Costs | Use when |
|---|---|---|---|
| Live object | full SOQL, reports, automation | data storage + every index | still transacted on |
| **Big object** | index-prefix only, no reports | separate allocation | keyed lookup, write-once → [14](14-big-objects-and-the-archive-tier.md) |
| **Salesforce Archive** | archived-record UI, unarchive on demand | licensed product | policy-driven retention with an audit trail |
| **Data 360 / lake** | SQL, analytics, agent grounding | consumption | analysis and AI, not transactions → [18](18-zero-copy-and-data-360-as-data-tier.md) |
| Deleted | none | none | the retention clock expired |

- **Salesforce Archive** (from the Own acquisition) is the productized answer: **archive policies** define what leaves the live object and when, with end-to-end visibility and one-click unarchive. Part of it ships as a **managed package**, and it is licensed — design the policy so it survives without the product.
- **Retention policy and purge policy are different things.** A retention policy deletes archived records when their period expires. A **purge policy deletes ad hoc, outside that period** — which is how a right-to-be-forgotten request is served against archived data.
- **Standard objects have their own retention primitive:** `HistoryRetentionPolicy` under Field Audit Trail, which is the same idea applied to field history → [07-security · 22](../07-security-and-sharing/22-field-audit-trail-and-data-retention.md).
- **Deleting is a tier.** The Recycle Bin means "archived" rows keep costing until physically purged → [13](13-deletes-recycle-bin-and-physical-deletion.md).
- **Design the archive around the retrieval question**, exactly as you design a big-object index — because on most tiers that is the only question you can ask.

## 2026 currency

The category changed owner. Salesforce **acquired Own Company** (announced September 2024), and Own's tools are now Salesforce products: **Backup & Recovery, Archive, Seed and Discover**. *Archive* is the one that lands here, and it moves the default answer from "build it on big objects yourself" — which is what every pre-2024 guide describes — to "buy the policy engine, or knowingly build one". The other two land on [21](21-backup-restore-and-recovery.md) and [20](20-sandboxes-seeding-and-data-mask.md).

The second shift is the destination. Archiving used to mean *out of the org*; increasingly it means *into [Data 360](18-zero-copy-and-data-360-as-data-tier.md)*, where the data stays analysable and can ground an agent. Note the trade in both directions: a big object cannot be reported on, and a federated table cannot be transacted on.

## Gotchas

- **Editing a retention period applies retroactively** to everything already archived through that policy. The documented workaround is to deactivate the old policy and create a new one.
- **Purge policies are capped at 1,000,000 records per day.** A large erasure obligation is a multi-day job, so a 30-day regulatory clock is tighter than it looks.
- **Pre-2023 archive tutorials lead with a retired query mechanism.** Big objects are current; the query path named in those guides is not → [14](14-big-objects-and-the-archive-tier.md).
- **Archiving does not shrink storage until the source rows are physically deleted** — soft-deleted rows still count → [13](13-deletes-recycle-bin-and-physical-deletion.md).
- **Nothing archives a relationship.** Children whose parent left the live object become orphans unless the policy walks the graph in order.
- **Retention obligations point both ways.** Privacy says delete; financial regulation says keep for ten years. The archive is how you hold both → [07-security · 25](../07-security-and-sharing/25-privacy-consent-and-data-protection.md).
- **An archived record is invisible to automation, sharing and reports.** Anything that quietly assumed a full history — a roll-up, a report, an agent's grounding set — changes answer the day the policy runs.

## Recall

Q: What is the difference between a retention policy and a purge policy in Salesforce Archive?
A: Retention deletes archived records when their period expires; purge deletes ad hoc **outside** that period, which is how right-to-be-forgotten is served.

Q: What happens if you shorten the retention period on an existing archive policy?
A: It applies retroactively to every record already archived through it. Deactivate and create a new policy instead.

Q: What is the daily ceiling on purge?
A: 1,000,000 records per day.

Q: Which tier do you choose for data that must be analysable and able to ground an agent?
A: Data 360 or a federated lake — not a big object, which supports neither reporting nor arbitrary filters.

Q: Why does archiving often fail to reduce storage?
A: The source rows are only soft-deleted, and soft-deleted rows keep consuming storage and query time until they are physically purged.

## Related

- [14 · Big objects & the archive tier](14-big-objects-and-the-archive-tier.md) — the mechanism this note sets policy for
- [13 · Deletes, the Recycle Bin & physical deletion](13-deletes-recycle-bin-and-physical-deletion.md) — why archiving alone frees nothing
- [21 · Backup, restore & recovery](21-backup-restore-and-recovery.md) — the other half of the Own suite, and a different problem
- [07-security · 22 Field Audit Trail & data retention](../07-security-and-sharing/22-field-audit-trail-and-data-retention.md) — retention expressed as a policy object
