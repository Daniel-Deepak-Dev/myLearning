# Data Skew

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** Lopsided distribution — the pathology that no index fixes. It is the hinge of this area: a **read** problem in [08](08-indexes-and-query-selectivity.md)–[09](09-query-plan-and-performance-tuning.md) and a **write** problem in [12](12-record-locking-and-concurrency.md). Sharing recalculation mechanics belong to [07-security · 16](../07-security-and-sharing/16-sharing-recalculation-and-performance.md).

## Core idea

Skew is not about how many records you have, it is about how unevenly they point. **Salesforce's working threshold is 10,000** — more than 10,000 child records under one parent, or more than 10,000 records of one object owned by one user. Past that, operations that are ordinarily per-record stop being per-record: a single ownership change fans out into hundreds of thousands of sharing recalculations, and a single parent becomes a lock everyone queues behind.

The reason it deserves its own note is that skew is **invisible to every tool in the previous two notes**. The Query Plan looks fine. The index exists and is used. Storage looks normal. What is wrong is the shape of the data, and the only fix is to change the shape.

## How it works

| Type | Shape | What it costs |
|---|---|---|
| **Account (parent-child) skew** | >10,000 children under one Account | sharing recalculation on owner change; lock contention on every child write |
| **Ownership skew** | >10,000 records of one object owned by one user | recalculation cascades through the role hierarchy on every reassignment |
| **Lookup skew** | very many records pointing at one lookup target | pure lock contention — none of master-detail's benefits |

- **Account skew's real cost is the sharing recalculation.** Changing an account's owner forces the platform to re-examine every child record's sharing, walk the role hierarchy and rewrite share rows → [07-security · 16](../07-security-and-sharing/16-sharing-recalculation-and-performance.md).
- **The classic ownership-skew fix is to take the owner out of the role hierarchy.** An integration or "unassigned" user with no role does not trigger hierarchy-based recalculation, which removes most of the cost without redistributing the data.
- **The classic account-skew shape is a bucket record** — `Unassigned`, `Miscellaneous`, `Default Account` — that everything unmatched gets attached to. Spreading across several buckets is a legitimate fix.
- **Lookup skew is the one people miss** because nothing cascades and nothing is shared; it shows up only as `UNABLE_TO_LOCK_ROW` under concurrency → [12](12-record-locking-and-concurrency.md).
- **Detect it with aggregates**, not intuition: `SELECT AccountId, COUNT(Id) FROM Contact GROUP BY AccountId HAVING COUNT(Id) > 10000`, and the equivalent on `OwnerId`.

## Gotchas

- **Skew arrives through integrations, not through users.** A load that assigns every imported record to one API user creates textbook ownership skew on day one.
- **A public sharing model hides ownership skew until the day OWD is tightened.** The recalculation that follows can run for hours or days.
- **Converted Leads and logged Activities accumulate against a few records** — `Task` and `Event` are common skew victims → [04](04-standard-crm-object-map.md).
- **Deleting the skew does not immediately remove it.** Soft-deleted children still sit under the parent until purged → [13](13-deletes-recycle-bin-and-physical-deletion.md).
- **Skinny tables do not help skew at all.** They reduce columns read, not the distribution → [11](11-skinny-tables-and-support-levers.md).
- **10,000 is a working threshold, not a cliff.** Pain starts earlier under heavy concurrency and later on a read-only object; treat it as the number that starts the conversation.
- **Reassigning a skewed owner is itself the expensive operation.** Do it in off-hours, in batches, and after considering the defer-sharing-calculation lever.

## Recall

Q: What is the working threshold for data skew?
A: 10,000 — more than 10,000 child records under one parent, or more than 10,000 records of one object owned by one user.

Q: What are the three types of skew?
A: Account (parent-child) skew, ownership skew, and lookup skew.

Q: What is the standard fix for ownership skew that does not involve moving records?
A: Remove the owning user from the role hierarchy — a user with no role does not trigger hierarchy-based sharing recalculation.

Q: Why is lookup skew easy to miss?
A: Nothing cascades and no sharing is inherited, so it never shows up in a query plan or a sharing report — only as lock contention under concurrency.

Q: How do you actually detect skew?
A: An aggregate query — `GROUP BY` the parent or owner field with `HAVING COUNT(Id) > 10000` — not by inspection.

## Related

- [12 · Record locking & concurrency](12-record-locking-and-concurrency.md) — the write-side consequence, in full
- [09 · Query Plan & performance tuning](09-query-plan-and-performance-tuning.md) — the tool that will *not* show you this
- [02 · Relationships deep dive](02-relationships-deep-dive.md) — why a detail write locks its master
- [07-security · 16 Sharing recalculation & performance](../07-security-and-sharing/16-sharing-recalculation-and-performance.md) — what recalculation costs, and the defer lever
