# Data Modeling: DSO → DLO → DMO — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Raw source shape (DSO) → persisted lake table (DLO) → canonical model (DMO) — and the DLO→DMO harmonization step is what every downstream feature inherits.

## Key terms
| Term | Definition |
|---|---|
| DSO | Raw data exactly as it arrives, before mapping. |
| DLO | The persisted lake table from a data stream. Still source-shaped. **Not a Platform object.** |
| DMO | Standardized canonical object DLOs map into. Cross-source consistent. |
| `SET OPTIONS` | SOQL clause (Summer '26) for dataspace + null handling. Goes at the **very end**. |
| Dataspace | Logical partition. **Required for DLO queries.** |

## Rules of thumb

- Prefer **standard DMOs** over custom ones — a custom DMO per source recreates the silos you're removing.
- Map what's used. Unmapped DLO fields still cost storage and add nothing downstream.
- Choose the primary key deliberately: identity resolution consumes it, and changing it later is painful.
- Decide null-vs-empty-string handling on purpose; don't inherit the default by accident.

## Exam traps / common confusions

- **Omit the dataspace on a DLO query → zero records, silently.** No error. Most expensive gotcha in the topic.
- `honorEmptyStrings = false` (the default) collapses `NULL` and `''` the way Platform objects do — lake data often doesn't mean it that way.
- **DLOs don't share Platform object semantics.** Don't carry assumptions across.
- **SQL from Apex** (Summer '26) handles joins/aggregations/window functions SOQL can't — same dataspace trap applies.
- Mapping mistakes propagate into identity resolution, insights, segments and every agent answer.

## Minimal example

```sql
SELECT Id, Email__c
FROM   Contact_Home__dlm
WHERE  Email__c != NULL
SET OPTIONS dataspace = 'MarketingDS', honorEmptyStrings = true
--          ^^^^^^^^^ omit this on a DLO → 0 rows, no error
--   and the whole clause must be LAST
```
