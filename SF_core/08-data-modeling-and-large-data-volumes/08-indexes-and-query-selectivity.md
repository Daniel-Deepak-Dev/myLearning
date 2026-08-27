# Indexes & Query Selectivity

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** Which fields are indexed, what "selective" means numerically, and what silently disables an index. Diagnosing a specific query is [09](09-query-plan-and-performance-tuning.md); SOQL syntax is [10-soql · 01](../10-soql-and-sosl/01-query-anatomy-and-the-soql-model.md).

## Core idea

A query is **selective** when its `WHERE` clause narrows the table enough that using an index beats scanning it. Salesforce's optimizer decides this per query, per execution, against published thresholds expressed as a **percentage of rows** — and that is the detail that makes selectivity a moving target. Nobody changes the query; the table grows past the threshold and the optimizer quietly stops using the index.

Two consequences follow. First, selectivity is a property of the **filter**, not of the fields you select or of how the query is written. Second, an index you cannot reach is worth nothing: a large share of real-world slow queries are on indexed fields, filtered in a way that disqualifies the index.

## How it works

**The thresholds — the whole reason this topic exists.** Both tiers and the cap, or the number is wrong:

| Index type | First 1M rows | Beyond 1M | Hard cap |
|---|---|---|---|
| **Standard** | 30% | 15% | **1,000,000** targeted records |
| **Custom** | 10% | 5% | **333,333** targeted records |

- **Standard indexes come free** on `Id`, `Name`, `OwnerId`, `CreatedDate`, `LastModifiedDate`, `SystemModstamp`, `RecordTypeId`, and every lookup and master-detail field. `Email` is indexed on Contact and Lead.
- **Two self-service routes to a custom index**, and both are side effects: marking a field **External ID** or **Unique** → [03](03-record-ids-external-ids-and-upsert.md). Everything else goes through **Salesforce Support**, including two-column composite indexes and null-inclusive indexes.
- **A deterministic formula field can be indexed by Support** — but only if it references fields on **one object**, uses no dynamic functions (`TODAY`, `NOW`), no `Id`, no `TEXT()` on a picklist, and no owner, autonumber or division fields. Anything cross-object or time-varying is **non-deterministic and can never be indexed.**
- **Custom indexes exclude nulls by default.** Filtering `WHERE Field__c = null` is therefore non-selective unless Support has enabled a null-inclusive index.

**What disables an index** — the list worth memorising: `!=`, `NOT`, `NOT IN`, `LIKE` with a **leading** wildcard, comparisons against `null`, `OR` where **any** branch is non-indexed, and filters on text areas, long text or multi-select picklists.

> **From my notes.** `Optimization work` (2023) is a single artefact: an "ultimate parent" formula field, eleven nested `IF`s walking `Parent.Parent.Parent…` up an Account hierarchy. It is a textbook demonstration of this note's argument, and worth keeping for exactly that reason. **It can never be indexed** — it is cross-object, therefore non-deterministic — so every report grouped or filtered on ultimate parent is non-selective by construction. It also sits at **two** documented ceilings simultaneously: cross-object formulas traverse at most **10 relationships**, and an object allows only **10 unique relationships** across all its formulas ([01-admin · 07](../01-admin-and-declarative-platform/07-formula-fields-and-roll-up-summaries.md)). The fix at volume is to stop computing it at read time — **materialise the ultimate parent into a real indexed field** maintained by a record-triggered flow or batch job. Same answer, and it can be filtered.

## Gotchas

- **Growth alone breaks a selective query.** Nothing changed in the code; the table crossed 333,333 matching rows.
- **One `OR` branch on a non-indexed field discards the index for the whole query.** Split into two queries, or index the other field.
- **`!=` and `NOT IN` are never selective.** Rewrite as a positive filter wherever the domain allows it.
- **The cap is on *targeted* records, not on the object.** A 100M-row object filtered down to 300,000 is selective on a custom index; the same object filtered to 400,000 is not.
- **Sharing can be the leading operation** rather than your filter, which usually means a small result set for a user with narrow access — fast for them and slow for an admin.
- **An index on a field nobody filters on is dead weight**, and marking fields `Unique` "just in case" changes upsert semantics as a side effect.
- **Selectivity is per query, not per field.** The same indexed field is selective in one query and not in another.

## Recall

Q: What are the selectivity thresholds for standard and custom indexes?
A: Standard — 30% of the first million rows, 15% beyond, capped at 1,000,000 targeted records. Custom — 10% then 5%, capped at 333,333.

Q: What are the only two ways to get a custom index without contacting Support?
A: Mark the field as an External ID, or mark it Unique. Both create the index as a side effect.

Q: Can a formula field be indexed?
A: Only a deterministic one — single object, no dynamic date functions, no `Id`, no owner or autonumber fields — and only by Support. Cross-object formulas never can.

Q: Why does one `OR` branch on an unindexed field matter?
A: It disqualifies the index for the entire query, so the whole thing becomes a table scan.

Q: A query was fast last year and is slow now with no code change. What most likely happened?
A: The object grew, so the filter now targets more rows than the threshold allows and the optimizer stopped using the index.

## Related

- [09 · Query Plan & performance tuning](09-query-plan-and-performance-tuning.md) — proving which of these applies to a specific query
- [03 · Record IDs, external IDs & upsert](03-record-ids-external-ids-and-upsert.md) — the index an external ID creates for free
- [10 · Data skew](10-data-skew.md) — the distribution problem no index solves
- [01-admin · 07 Formula fields & roll-up summaries](../01-admin-and-declarative-platform/07-formula-fields-and-roll-up-summaries.md) — the formula limits the seed note collides with
