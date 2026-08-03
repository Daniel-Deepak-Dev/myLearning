# Backup, Restore & Recovery

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** Getting data back after you break it — the options, what each actually covers, and how to design an RPO/RTO you can defend. Metadata recovery is a pipeline problem → [09-devops](../09-devops-sfdx-and-release-management/INDEX.md).

> **What changed.** Two different things get compressed into one wrong sentence. The **paid Data Recovery Service** was retired in 2020, **reinstated in 2021, and is still available** — but at **$10,000**, **6–8 weeks**, **data only, no metadata**, returned as **CSV files you re-import yourself**. Separately the *product* was renamed twice: *Backup and Restore* → **Salesforce Backup** → and since the **Own acquisition**, **Salesforce Backup & Recover**. Neither is on by default. **Nothing backs your org up unless somebody bought and configured it.**

## Core idea

Salesforce guarantees the **infrastructure** will not lose your data. It does not guarantee your data is *correct*, and almost all real data loss is self-inflicted: a bad deploy, a mis-keyed load, an integration that upserts on the wrong external ID, a mass delete run against the wrong filter. Infrastructure redundancy is no help against any of those, because the platform faithfully replicates the mistake.

So the design question is never "is it backed up" but the two numbers underneath: **RPO** — how much data you can afford to lose, measured in time — and **RTO** — how long you can be down while restoring. Every option below is an answer to those two numbers at a price, and answering them is what turns "we should have backups" into a decision someone can sign.

## How it works

| Option | Covers | RPO | Notes |
|---|---|---|---|
| Recycle Bin | deleted rows | immediate | ~15 days, size-capped → [13](13-deletes-recycle-bin-and-physical-deletion.md) |
| **Data Export Service** | data, as CSV in a zip | 7 or 29 days | **monthly only in PE and DE**; files deleted **48 hours** after the email |
| Full sandbox | data + metadata | up to 29 days | a point-in-time copy you already pay for → [20](20-sandboxes-seeding-and-data-mask.md) |
| Own extraction pipeline | what you built | your choice | Bulk API 2.0 → [06-integration · 07](../06-integration-and-apis/07-bulk-api-2.md) |
| **Salesforce Backup & Recover** | data, metadata, files, attachments, managed packages, sandboxes | daily + on demand | licensed; does not consume the org's API limits |
| Data Recovery Service | data only | ~3 months back | $10,000, 6–8 weeks, CSV, **no guarantee** |

- **Restore is the hard half.** A CSV of Contacts does not restore relationships: record Ids change, lookups break, parents must be loaded first, and reparenting is your job → [25](25-data-migration-and-cutover.md).
- **An untested restore is not a backup.** Rehearse it in a sandbox against a real scenario, and time it — that measured number is your actual RTO.
- **Files, attachments and metadata are three separate scopes.** A tool that covers one is routinely assumed to cover all three.

## 2026 currency

The category consolidated. Salesforce **acquired Own Company** (announced September 2024) and **Salesforce Backup & Recover** — formerly Own Recover / OwnBackup — is the current native offering, with **Backup & Recover Next** announced as its successor. The suite's other members land elsewhere in this area: **Archive** on [15](15-archiving-and-retention-strategy.md), **Seed** on [20](20-sandboxes-seeding-and-data-mask.md). Practical consequence: any material naming *Backup and Restore* is at least two renames old, and the honest summary for a client is that **backup is a purchase decision on this platform, not a default**.

## Gotchas

- **Export zips are deleted 48 hours after the email** (weekends excluded). An export nobody downloads is not a backup.
- **`Weekly Data Export` grants sight of every object and field**, which is why it sits on System Administrator by default — treat it as a privileged permission → [07-security · 15](../07-security-and-sharing/15-auditing-and-troubleshooting-access.md).
- **Big objects and archived field history are routinely outside backup scope.** Verify rather than assume → [14](14-big-objects-and-the-archive-tier.md).
- **A restore fires automation.** Triggers, flows and validation rules run against restored rows unless suppressed → [16](16-bulk-loading-strategy-for-ldv.md).
- **Backups are full of PII** and are in scope for subject-rights erasure like any other copy → [07-security · 25](../07-security-and-sharing/25-privacy-consent-and-data-protection.md).
- **A Full sandbox as a backup costs you the 29-day refresh window** the moment you use it for recovery.
- **The corruption you are restoring from may predate your retention.** A silently wrong integration discovered in week six is not recoverable from a two-week window.

## Recall

Q: Is Salesforce's paid Data Recovery Service still available, and on what terms?
A: Yes — reinstated in 2021. $10,000 flat, 6–8 weeks, data only (no metadata), delivered as CSV, with no guarantee of full recovery.

Q: What is the current native backup product called?
A: **Salesforce Backup & Recover** (formerly Own Recover / OwnBackup). *Backup and Restore* and *Salesforce Backup* are earlier names for that lineage.

Q: What do RPO and RTO mean, and why are they the design question?
A: How much data you can lose (time) and how long you can be down. Every backup option is a price attached to those two numbers.

Q: Why is a CSV export not a restore plan?
A: Record Ids change on reload, so relationships, load order and reparenting all have to be rebuilt — and a restore fires automation while doing it.

Q: How long do Data Export Service files remain available?
A: 48 hours after the notification email, excluding weekends.

## Related

- [13 · Deletes, the Recycle Bin & physical deletion](13-deletes-recycle-bin-and-physical-deletion.md) — the first and cheapest recovery tier
- [25 · Data migration & cutover](25-data-migration-and-cutover.md) — a restore is a migration with a deadline
- [20 · Sandboxes, seeding & Data Mask](20-sandboxes-seeding-and-data-mask.md) — the Full sandbox as an accidental backup
- [15 · Archiving & retention strategy](15-archiving-and-retention-strategy.md) — the other half of the Own suite, solving a different problem
