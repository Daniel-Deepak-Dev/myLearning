# Data Modeling: DSO → DLO → DMO

> Track: Data 360 · Roadmap: Phase 02 · Weeks 5–8 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/data-360.md](../../05-release-radar/data-360.md)

**Roadmap scope:** How raw source objects land as lake objects and get mapped to the standard data model. This mapping discipline is the heart of the Consultant exam.

## What is it?

Three stages, and the exam cares that you can tell them apart precisely:

| Stage | What it is | Shape |
|---|---|---|
| **DSO** — Data Source Object | Raw data exactly as it arrives from the source, before any mapping | Source's shape |
| **DLO** — Data Lake Object | The stored table in the lake created from a data stream | Source's shape, persisted |
| **DMO** — Data Model Object | A standardized object in the canonical model that DLOs map into | Salesforce's shape |

**Harmonization** is the DLO → DMO mapping step: "email" from five systems becomes one consistent attribute on one DMO.

```
source system
    │
  DSO      raw, as it arrives
    │      (data stream)
  DLO      persisted in the lake, still source-shaped
    │      ← HARMONIZATION happens here
  DMO      canonical model — cross-source consistent
    │
    └──► identity resolution → insights → segments → agent grounding
```

## Why it matters (for the AI-Salesforce architect role)

**Everything downstream inherits this mapping.** Identity resolution matches on DMO fields. Calculated insights compute over DMOs. Segments filter DMOs. Agents ground on them. A mapping mistake doesn't stay local — it propagates into every answer the agent gives, and it's expensive to unwind once segments and insights are built on top.

This is why the Consultant exam weights it heavily, and why "just map it and fix it later" is the wrong instinct here specifically.

**The 2026 addition:** DLOs became directly queryable from SOQL and from Apex. That's a real capability increase, and it comes with a trap that costs people an afternoon — covered below.

## How it works

### `SET OPTIONS` — new in Summer '26

A new [`SET OPTIONS` clause](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_select_set_options.htm) lets a SOQL query specify a Data 360 **dataspace** and control `NULL` / empty-string handling. **The clause goes at the very end of the query.**

Two rules that will bite you:

**1. Dataspace is required for DLO queries.** Omit it and the query **silently returns zero records** — not an error, not a warning. Zero rows looks exactly like "no matching data", so you'll debug your `WHERE` clause for an hour before suspecting the dataspace.

**2. `honorEmptyStrings = true` makes Data 360 treat `NULL` and `''` as distinct values.** The default (`false`) collapses them the way Salesforce Platform objects do.

That second one is the deeper lesson: **DLOs don't share Platform object semantics.** They're lake tables. `SET OPTIONS` is the seam where that difference becomes explicit, and the empty-string default is a classic source of wrong-but-plausible results — queries that return rows, just not the right ones.

### SQL from Apex

Summer '26 also added **running SQL from Apex** against Data 360. This removes a genuine impedance mismatch: SOQL can't express the joins, aggregations and window functions that lakehouse work needs, and the previous alternative was HTTP callouts to the Direct API.

An Apex-backed Agentforce action can now compute a rolling aggregate or a multi-table join in a single query. **Same trap applies** — specify the dataspace for DLO queries or get zero records, silently.

### Modeling decisions that matter

| Decision | Guidance |
|---|---|
| Map to a standard DMO or create a custom one? | Prefer standard — cross-source consistency is the whole point, and standard DMOs carry downstream behaviour |
| Which field is the primary key? | Gets used by identity resolution; changing it later is painful |
| How much to map? | Map what's used. Unmapped DLO fields still cost storage but add no downstream value |
| Nulls vs empty strings | Decide deliberately and set `honorEmptyStrings` accordingly — don't inherit the default by accident |

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Map one DLO to a standard DMO end to end, then query the DMO.
- [ ] **The trap lab:** run a SOQL query against a DLO *without* `SET OPTIONS`, observe zero records with no error, then add the dataspace and watch it work. Fifteen minutes that saves an afternoon later.
- [ ] Run the same query with `honorEmptyStrings` true and false against data containing both `NULL` and `''`. Compare row counts.
- [ ] Write one Apex method that runs SQL against Data 360 and returns an aggregate.

## Gotchas & sharp edges

- **Missing dataspace on a DLO query returns zero records silently.** No error. This is the single most expensive gotcha in the topic.
- **`SET OPTIONS` goes at the very end of the query** — not after the `FROM`, not before `ORDER BY`.
- **`NULL` and `''` collapse by default.** Platform objects behave that way; lake data often doesn't mean it that way.
- **DLOs are not Platform objects.** Don't carry over assumptions about semantics, indexing or behaviour.
- **Mapping mistakes propagate.** Identity resolution, insights, segments and agent answers all inherit them.
- **Don't create custom DMOs reflexively.** Standard DMOs exist so that cross-source consistency is possible; a custom DMO per source recreates the silos you were removing.
- **Unmapped fields still cost storage.** Ingesting everything "just in case" has a bill attached.

## Related topics

- [Ingestion](../02-ingestion/notes.md) — how data reaches the DLO
- [Identity resolution](../04-identity-resolution/notes.md) — what consumes your DMO mapping
- [Insights & segmentation](../05-insights-segmentation/notes.md) — computed over DMOs
- [Data 360 DevOps](../09-data-360-devops/notes.md) — promoting model changes between orgs
- [SQL fluency](../../00-core-skills/01-sql/notes.md) — the joins and window functions SQL-from-Apex unlocks
- [Release radar: Data 360](../../05-release-radar/data-360.md) — `SET OPTIONS` entry with sources
