# Sandboxes, Seeding & Data Mask

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** The **data** in non-production orgs — which sandbox holds what, how it gets there, and how it stops being real. Source tracking and the development workflow are [09-devops](../09-devops-sfdx-and-release-management/INDEX.md).

## Core idea

A sandbox is a metadata copy with a **data policy attached**, and the data policy is the part teams skip. Two failures follow from skipping it: developers testing against 12 records and shipping code that dies at 12 million, and production PII sitting unmasked in five environments with no owner.

Both are decisions, not accidents. Choosing a sandbox tier is choosing how much data you get and how often you can refresh it; everything after that is deliberately putting data in (**seeding**) and deliberately taking the truth out of it (**masking**).

## How it works

| Type | Data | Storage | Refresh |
|---|---|---|---|
| Developer | metadata only | 200 MB | 1 day |
| Developer Pro | metadata only | 1 GB | 1 day |
| Partial Copy | sample via **sandbox template** | 5 GB | 5 days |
| Full | everything | production-equivalent | **29 days** |

- **The refresh interval is the real constraint.** A Full sandbox is the only place LDV behaviour reproduces, and you get it roughly monthly — so a performance test is scheduled work, not something you retry.
- **Sandbox templates** choose which objects a Partial Copy or Full sandbox brings, and are how you get a useful subset instead of an arbitrary one.
- **Data Mask runs after the refresh, in the sandbox**, and offers anonymize, pseudonymize, pattern-based replacement and delete, per field. It is **irreversible by design** — that is the point.
- **Seeding is the opposite operation**: pushing a curated, relationship-preserving dataset into an environment that has none.
- **Usernames are rewritten** on refresh and email deliverability is restricted, which is a data-safety feature, not a bug to work around.
- **Skinny tables are copied to Full sandboxes only** — Developer, Developer Pro and Partial need Support to activate them, which is why production performance will not reproduce → [11](11-skinny-tables-and-support-levers.md).

## 2026 currency

The product is now **Data Mask & Seed**, and the "& Seed" half is the new part: **seeding templates**, **synthetic test data generation**, and seeding into **Developer, Developer Pro, Partial and Full** sandboxes — so a Developer sandbox with realistic data is finally an option. The refreshed masking experience **preserves field-value distributions**, which matters more than it sounds: masking that flattens a picklist's distribution silently invalidates every performance and reporting test run against it.

Alongside it, the **Own acquisition** brought **Seed** into the Salesforce portfolio, so an org may have two overlapping seeding tools with different licensing. Establish which one is in play before writing a runbook step. Own's **Archive** and **Backup & Recovery** are the same story on [15](15-archiving-and-retention-strategy.md) and [21](21-backup-restore-and-recovery.md).

## Gotchas

- **A Full sandbox refresh copies real PII by default**, and nobody owns the follow-up. Automate masking as part of the refresh → [07-security · 25](../07-security-and-sharing/25-privacy-consent-and-data-protection.md).
- **Masking is irreversible.** Run it against the wrong environment and the only recovery is another refresh — which costs you the 29-day window.
- **Partial Copy is a sample, not a scale model.** It reproduces shape, never volume; selectivity and skew problems do not appear in it → [08](08-indexes-and-query-selectivity.md), [10](10-data-skew.md).
- **Seeded data with broken relationships is worse than no data** — orphaned children make automation behave in ways production never will.
- **Sandbox storage is a hard ceiling.** A 5 GB Partial Copy silently truncates what the template asked for.
- **Automation fires during seeding** unless you suppress it, so a seed load is a bulk load with all the same levers → [16](16-bulk-loading-strategy-for-ldv.md).
- **Async sharing recalculation makes small sandboxes unrepresentative** of production behaviour — the platform picks sync or async by data volume → [07-security · 16](../07-security-and-sharing/16-sharing-recalculation-and-performance.md).

## Recall

Q: Which sandbox types can be refreshed daily, and which is limited to 29 days?
A: Developer and Developer Pro refresh daily, Partial Copy every 5 days, Full every 29 days.

Q: Why is a Partial Copy sandbox useless for LDV testing?
A: It caps at 5 GB and copies a sample — volume-driven behaviour like selectivity, skew and async sharing recalculation never appears.

Q: What does the current masking experience preserve, and why does it matter?
A: Field-value distributions — masking that flattens them invalidates performance and reporting tests run against the sandbox.

Q: What is the standard answer to production PII in sandboxes?
A: Data Mask, run as an automated step in the refresh process rather than as a manual follow-up.

Q: Which two overlapping seeding tools might an org have in 2026?
A: Data Mask & Seed, and Own **Seed** — different licensing, same job.

## Related

- [16 · Bulk loading strategy for LDV](16-bulk-loading-strategy-for-ldv.md) — seeding is a bulk load and hits the same levers
- [11 · Skinny tables & support levers](11-skinny-tables-and-support-levers.md) — why Full sandboxes perform differently from the rest
- [07-security · 25 Privacy, consent & data protection](../07-security-and-sharing/25-privacy-consent-and-data-protection.md) — the obligation behind masking
- [09-devops · INDEX](../09-devops-sfdx-and-release-management/INDEX.md) — source tracking and the sandbox's role in the pipeline
