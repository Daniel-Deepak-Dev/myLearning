# Skinny Tables & Support Levers

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** The end of the read-path argument — what is left after [08](08-indexes-and-query-selectivity.md) selectivity, [09](09-query-plan-and-performance-tuning.md) diagnosis and [10](10-data-skew.md) distribution have all been addressed. These are levers you request, not settings you own.

## Core idea

Salesforce stores standard and custom fields in separate underlying tables, so reading a record that mixes both requires a join. A **skinny table** is a Salesforce-maintained copy of the fields you actually query, in one table, kept in sync automatically. It removes the join and it excludes soft-deleted rows, which is why it can materially speed up reports, list views and SOQL over very large objects.

The honest framing matters more than the mechanism: **you cannot create, view or modify a skinny table.** It is a Salesforce Support request, granted at Salesforce's discretion, and every subsequent change — adding one field to one report — is another request. That makes it a genuine last resort rather than a tuning option, and it is the reason this note sits at the end of the chain rather than the middle.

## How it works

- **Maximum 100 columns**, and the contents are restricted: **no formula fields**, no fields from other objects via lookup, no large CLOB/long-text fields. If it could be in a skinny table, it would not be skinny.
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
A: 100 columns; no formula fields, no fields from other objects, no large text/CLOB fields.

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
