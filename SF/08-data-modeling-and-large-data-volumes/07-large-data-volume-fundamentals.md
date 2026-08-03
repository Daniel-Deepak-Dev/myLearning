# Large Data Volume Fundamentals

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** Where the platform starts to degrade, and *why* — the opening of an argument continued in [08](08-indexes-and-query-selectivity.md)–[11](11-skinny-tables-and-support-levers.md) for reads and [12](12-record-locking-and-concurrency.md)–[13](13-deletes-recycle-bin-and-physical-deletion.md) for writes.

## Core idea

"Large data volume" is not a row count, it is the point at which **the platform stops being able to take shortcuts on your behalf**. Below it, the query optimizer's decisions barely matter because every table scan is cheap. Above it, the same query, the same report and the same trigger behave differently — and the change is not gradual. A query that returns in 200 ms at 500,000 rows can time out at 5 million, because the optimizer crossed a threshold and abandoned the index.

The mechanism underneath is worth stating once, because the rest of this area depends on it. Salesforce is **multi-tenant**: your records share physical tables with other orgs, and every query is silently rewritten to filter by org. The platform therefore leans on indexes far harder than a single-tenant database would, and it protects itself with **hard timeouts and row limits** rather than letting a slow query run long. So at volume the failure mode is not "slow" — it is *refused*.

The third piece is **sharing**. Every query a user runs also has to answer "may this user see this row?", and at volume that check has its own cost and its own tables. Two orgs with identical data can perform differently because one has a private sharing model and 400,000 share rows.

## How it works

- **The commonly cited threshold is a few million rows per object**, but the honest answer is that it depends on selectivity, sharing, skew and field shape. Treat published row counts as a prompt to measure, not as a limit.
- **What degrades, roughly in order:** reports and list views → SOQL in triggers and batch → sharing recalculation → deployments and schema changes → data loads.
- **The optimizer decides per query whether an index is worth using**, against thresholds expressed as a *percentage of rows* ([08](08-indexes-and-query-selectivity.md)). Growth alone can push a previously selective query over the line without anyone changing it.
- **Governor limits are the symptom, not the disease.** 50,000 rows in SOQL, 10 seconds of CPU, query timeouts — these fire because the underlying access was non-selective → [02-apex · 01](../02-apex-and-triggers/01-apex-language-core-and-governor-limits.md).
- **Volume has a write side too**, and it is a different problem: locking and contention rather than selectivity → [12](12-record-locking-and-concurrency.md).
- **Deleted rows count until they are physically purged**, so an org can carry volume it believes it has removed → [13](13-deletes-recycle-bin-and-physical-deletion.md).

## Gotchas

- **Nothing warns you.** There is no notification when an object crosses into LDV territory; the first signal is a user complaint or a failing nightly job.
- **A sandbox proves nothing about volume.** Full sandboxes copy data, all other types do not — so performance testing in a Developer sandbox is testing an empty table.
- **The same query behaves differently for different users.** An admin with `View All Data` skips the sharing check entirely, which is why "it works for me" is not a test result.
- **`SELECT COUNT()` on a huge object is not free**, and neither is an unfiltered list view — both are ordinary non-selective queries.
- **Growth is the variable, not size.** An object at 2M rows growing 4M a year is a more urgent problem than a static object at 20M.
- **Archiving is a design decision made at the start**, not a rescue later. By the time it is needed, the migration is the expensive part → [15](INDEX.md) *(phase 15)*.

## Recall

Q: What actually defines "large data volume"?
A: The point where the platform can no longer take shortcuts — where selectivity, sharing cost and locking begin to decide behaviour. It is not a fixed row count.

Q: Why does Salesforce depend on indexes more heavily than a single-tenant database?
A: It is multi-tenant. Records share physical tables and every query is rewritten to filter by org, so index use is what keeps that filter cheap.

Q: At volume, what is the usual failure mode of a non-selective query?
A: Refusal rather than slowness — a timeout or a governor limit, because the platform protects itself instead of running long.

Q: Why can two orgs with identical data perform differently?
A: Sharing. A private model with large numbers of share rows adds a per-query access check that a public model does not.

Q: Why is testing performance in a Developer sandbox misleading?
A: Only Full sandboxes copy production data. Every other type gives you an empty table and therefore a selective query.

## Related

- [08 · Indexes & query selectivity](08-indexes-and-query-selectivity.md) — the next step in the argument: *why* queries stop being selective
- [12 · Record locking & concurrency](12-record-locking-and-concurrency.md) — the write-side twin of this note
- [06 · Storage model & schema limits](06-storage-model-and-schema-limits.md) — volume as a billing question, before it becomes a performance one
- [07-security · 16 Sharing recalculation & performance](../07-security-and-sharing/16-sharing-recalculation-and-performance.md) — what the sharing check costs to maintain
