---
vault: SF_core
area: 08-data-modeling-and-large-data-volumes
format: dense
status: learning
created: 2026-08-03
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 14
---
# Skinny Tables & Support Levers

**Scope:** The end of the read-path argument — what is left after [08](08-indexes-and-query-selectivity.md) selectivity, [09](09-query-plan-and-performance-tuning.md) diagnosis and [10](10-data-skew.md) distribution have all been addressed. These are levers you request, not settings you own.

## Core idea

Salesforce stores standard and custom fields in separate underlying tables, so reading a record that mixes both requires a join. A **skinny table** is a Salesforce-maintained copy of the fields you actually query, in one table, kept in sync automatically. It removes the join and it excludes soft-deleted rows, which is why it can materially speed up reports, list views and SOQL over very large objects.

The honest framing matters more than the mechanism: **you cannot create, view or modify a skinny table.** It is a Salesforce Support request, granted at Salesforce's discretion, and every subsequent change — adding one field to one report — is another request. That makes it a genuine last resort rather than a tuning option, and it is the reason this note sits at the end of the chain rather than the middle.

## How it works

- **Maximum 200 columns**, and the contents are restricted: **no formula fields** (formula is not on the allowed-type list) and **no fields from other objects**. Long text area, multi-select picklist and encrypted data are allowed. Only custom objects and **Account, Contact, Opportunity, Lead and Case** can have one.
- **Kept in sync by the platform.** There is no refresh to schedule and no staleness to manage.
- **It excludes soft-deleted records**, which is a real part of the benefit at volume → [13](13-deletes-recycle-bin-and-physical-deletion.md).
- **Custom indexes come first.** Support will generally expect indexing and query tuning to have been tried; a skinny table is not the opening move.
- **Sandbox behaviour is the detail people get wrong.** Skinny tables **are copied to Full sandboxes**. They are **not** copied to Developer, Developer Pro or Partial sandboxes — Support has to activate them there on request.

**The adjacent Support-only levers**, worth knowing exist so you can ask for the right one:

| Lever | What it does |
|---|---|
| **Custom index** | on a field you cannot make External ID or Unique → [08](08-indexes-and-query-selectivity.md) |
| **Two-column composite index** | for a filter that is only selective in combination |
| **Null-inclusive custom index** | makes `= null` filters selective |
| **Deterministic formula index** | on a single-object, time-invariant formula |
| **Defer sharing calculation** | suspends recalculation during a bulk load → [07-security · 16](../07-security-and-sharing/16-sharing-recalculation-and-performance.md) |
| **Granular locking** | narrows group-membership locks → [07-security · 08](../07-security-and-sharing/08-groups-queues-and-the-grantee-model.md) |

## 2026 currency

The Winter '27 edition of Salesforce's LDV guide (updated 18 September 2026) gives **200 columns**, not the 100 this note quoted from older material. It also lists **Text area (long)** as an allowed type, so the old "no long text" rule was wrong. 🚩 No release note dates the column change. Confirm the ceiling with Support before designing a 150-column table.

## Gotchas

- **Adding a field to a query means re-requesting the skinny table.** Design the field set once, deliberately, or the maintenance cost exceeds the benefit.
- **They do nothing for skew.** Fewer columns read; the same lopsided distribution → [10](10-data-skew.md).
- **They do nothing for a non-selective filter.** A table scan of a skinny table is still a table scan.
- **You cannot verify one exists by looking.** There is no Setup page; the record of what you have is your own Support case history.
- **A Developer sandbox will not reproduce production performance** even after a skinny table is granted in production, unless Support activated it there too.
- **Formula fields being excluded is often the blocker**, because the slow report is usually filtered on exactly the formula that cannot go in.
- **Treat them as a dependency.** An org relying on skinny tables has a performance profile it cannot recreate, migrate or explain without Salesforce.

## Recall

Q: What does a skinny table actually remove?
A: The join between the standard-field and custom-field tables, plus soft-deleted rows — it is one table containing exactly the fields requested.

Q: What is the column limit, and what cannot go in?
A: 200 columns per the Winter '27 LDV guide (older material says 100); no formula fields and no fields from other objects.

Q: How do you create a skinny table?
A: You do not — it is a Salesforce Support request, and you can neither view nor modify the result yourself.

Q: Which sandbox types get skinny tables on refresh?
A: Full sandboxes only. Developer, Developer Pro and Partial need Support to activate them.

Q: Do skinny tables help with data skew?
A: No. They reduce the columns read, not the distribution of records.

## Related

- [08 · Indexes & query selectivity](08-indexes-and-query-selectivity.md) — everything that should be tried first
- [10 · Data skew](10-data-skew.md) — the problem this does not solve
- [13 · Deletes, the Recycle Bin & physical deletion](13-deletes-recycle-bin-and-physical-deletion.md) — the soft-deleted rows a skinny table skips
- [07-security · 16 Sharing recalculation & performance](../07-security-and-sharing/16-sharing-recalculation-and-performance.md) — the other lever you have to ask for

## Sources

- [Best Practices for Deployments with Large Data Volumes (PDF, Winter '27)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_large_data_volumes_bp.pdf) — Salesforce Developers · read 2026-10-28 · *Skinny Tables*: *"a maximum of 200 columns"*; allowed types incl. Text area (long) and multi-select picklist; encrypted data; custom objects plus Account, Contact, Opportunity, Lead, Case; Full sandboxes only
- [Skinny Tables](https://developer.salesforce.com/docs/platform/salesforce-large-data-volumes-bp/guide/ldv-deployments-infrastructure-skinny-tables.html) — Salesforce Developers · via search 2026-10-28 · the HTML edition repeats the 200-column cap

## History

- 2026-10-28 · Winter '27 currency check: column cap 100 → 200; long text area is allowed; supported objects added
