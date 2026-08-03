# Storage Model & Schema Limits

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** What a record, a field and an object actually cost against the org's allocations. Storage as a *performance* problem starts at [07](07-large-data-volume-fundamentals.md); reclaiming it is [13](13-deletes-recycle-bin-and-physical-deletion.md).

## Core idea

Salesforce does not bill storage by how much data a record contains. **Most records count as roughly 2 KB each regardless of how many fields are populated** — a record with four fields and a record with four hundred cost the same. That single fact inverts the instinct brought from other databases: adding fields is cheap against *storage* and expensive against everything else, while adding **rows** is the only thing that moves the storage needle.

The second thing to hold is that there is no single "storage". **Data, file and big-object storage are three separate allocations**, they are consumed by different things, and exhausting one says nothing about the others. An org can be at 98% on files and 12% on data, and the symptom — "we're out of space" — points at the wrong fix.

## How it works

| Allocation | Consumed by | Notes |
|---|---|---|
| **Data storage** | records, at ~2 KB each | per-edition base plus a per-user increment |
| **File storage** | attachments, Files, images, documents | far larger base; separate ceiling |
| **Big object storage** | big object rows | **1 million records** allocated per org, extendable → [14](14-big-objects-and-the-archive-tier.md) |

- **Read the org's real numbers, never a blog's.** Setup → **Storage Usage** shows current consumption by object; the allocation itself varies by edition and purchased capacity. `/limits` gives the API view → [06-integration · 24](../06-integration-and-apis/INDEX.md).
- **Some records are not 2 KB.** Person accounts consume two records ([05](05-person-accounts-and-one-way-modeling-decisions.md)); Campaign records and email messages are larger; big-object rows are counted separately altogether.
- **Field and object allocations are per-edition and per-object**, and they are what actually bind in a mature org — not storage. Custom fields per object, relationship fields per object (**40**), roll-up summaries (**25**, raisable to **40**), external IDs (**25**, shared with `Unique`).
- **Schema changes at volume are not instant.** Adding an indexed field or a required field to a table with tens of millions of rows is a background operation, and adding a field with a default value rewrites rows.
- **Custom metadata and custom settings are not record storage.** Configuration modelled as records is the commonest self-inflicted storage cost → [01-admin · 09](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md).

## Gotchas

- **A deleted field keeps consuming its allocation for 15 days**, and so does a deleted object. An org that is at the field limit cannot free space by deleting and immediately re-creating — it must purge first.
- **Deleting records does not free storage immediately.** They sit in the Recycle Bin and still count → [13](13-deletes-recycle-bin-and-physical-deletion.md).
- **Storage exhaustion blocks writes across the org**, not just on the offending object, and it surfaces as failing integrations rather than an admin warning.
- **Sandboxes have their own, much smaller allocations.** A Developer sandbox that will not take a data load is usually hitting storage, not a governor limit.
- **Field history and audit rows are records too.** Turning history tracking on for twenty fields on a high-volume object is a storage decision → [07-security · 22](../07-security-and-sharing/22-field-audit-trail-and-data-retention.md).
- **"Add a field" is cheap for storage and expensive for everything else** — describe payloads, page load, API response size, and every `SELECT FIELDS(ALL)`.
- **Buying storage is often cheaper than an archiving project**, and that comparison is rarely made explicitly. Do the arithmetic before designing an archive → [15](INDEX.md) *(phase 15)*.

## Recall

Q: How much data storage does a record with 400 populated fields consume compared with one that has 4?
A: The same — roughly 2 KB. Storage is counted per record, not per byte of content.

Q: What are the three separate storage allocations?
A: Data storage (records), file storage (attachments and Files), and big object storage — with about 1 million big object records allocated per org.

Q: Why can an org at its custom-field limit not free a slot by deleting a field?
A: A deleted field still consumes its allocation for 15 days until it is purged.

Q: What is the first place to look for an org's actual storage position?
A: Setup → Storage Usage, which breaks consumption down by object. Allocations vary by edition and purchased capacity, so a published figure is not evidence.

Q: Which allocation usually binds first in a mature org?
A: Not storage — the per-object field, relationship and roll-up allocations.

## Related

- [07 · Large data volume fundamentals](07-large-data-volume-fundamentals.md) — when row count stops being a billing question and becomes a performance one
- [13 · Deletes, the Recycle Bin & physical deletion](13-deletes-recycle-bin-and-physical-deletion.md) — how storage is actually reclaimed
- [14 · Big objects & the archive tier](14-big-objects-and-the-archive-tier.md) — the separate allocation, and what belongs in it
- [01-admin · 09 Custom metadata vs custom settings](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md) — configuration that should never be record storage
