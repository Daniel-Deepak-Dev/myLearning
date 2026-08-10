# Ingestion

> Track: Data 360 · Roadmap: Phase 01 · Weeks 1–4 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/data-360.md](../../05-release-radar/data-360.md)

**Roadmap scope:** Data streams, connectors (CRM, Marketing Cloud, S3, web SDK), batch vs streaming ingestion, refresh schedules.

## What is it?

**Ingestion** is step 1 of the Data 360 flow: getting data in. The unit of configuration is a **data stream** — a feed from a connector on a batch or streaming schedule, landing data as a **DLO** (Data Lake Object).

### The three ways data gets in

| Method | How it works | Trade-off |
|---|---|---|
| **Ingestion** (data streams) | Data is copied into Data 360 | Full control, full cost, freshness depends on schedule |
| **Zero-copy federation** | Query it where it lives (Snowflake, BigQuery, Databricks, Redshift) | No duplication, but query performance depends on the source |
| **Accelerated Data Ingest** | Real-time CRM data with no pipeline lag | **GA** in Summer '26 — the default for CRM going forward |

Choosing between these is the first real architecture decision in a Data 360 project. See [zero copy & BYOL](../06-zero-copy-byol/notes.md) for the federation side.

### Common connectors

CRM (core org), Marketing Cloud, Amazon S3, Web/Mobile SDK, plus federation connectors for the major lakehouses.

## Why it matters (for the AI-Salesforce architect role)

**Accelerated Data Ingest is the most under-appreciated feature in Summer '26, and it deserves a paragraph of its own.**

Scheduled ingestion meant Data 360's copy of a Case or Opportunity always lagged the live CRM record. That's tolerable for analytics — a churn dashboard doesn't care about the last four hours. It is **fatal for agents**, which then answer confidently from stale state.

That failure has a distinctive signature: the agent is fluent, specific, and wrong, and everyone blames the model. It isn't the model. It's that the agent was told the case was open when it closed twenty minutes ago.

Accelerated Data Ingest (GA) removes it for CRM data. It also removes the workaround people reached for — bypassing Data 360 and calling CRM directly from an action — which cost you the unified profile and its governance, and quietly reintroduced the sharing problems Data 360 was solving.

**The architect's rule:** if an agent grounds on it, it needs to be real-time. If a dashboard reads it, scheduled is fine. Decide per data stream, not per project.

## How it works

### Batch vs streaming vs accelerated

| | Batch | Streaming | Accelerated |
|---|---|---|---|
| Latency | Scheduled (minutes–hours) | Near-real-time | Real-time |
| Typical source | Nightly CRM sync, S3 drops | Web/mobile SDK, engagement events | CRM objects |
| Cost profile | Cheapest per row | Higher | — |
| Good for | Analytics, historical loads | Behavioural signals | **Agent grounding** |

### Refresh schedules and the design question

Every data stream has a refresh schedule, and every schedule is a **freshness-versus-cost decision**. The questions worth asking for each stream:

1. Does an *agent* read this? → real-time
2. Does a *segment* use it for activation? → match the activation cadence
3. Does only a *dashboard* read it? → scheduled is fine
4. Is it historical/immutable? → one-time load

Most projects over-refresh everything by default, which costs money, or under-refresh the one stream an agent depends on, which produces the failure above.

### Where ingestion sits

```
source system
    │
  connector          ← CRM, Marketing Cloud, S3, web SDK
    │
 data stream         ← batch | streaming | accelerated
    │
   DLO               ← lands here, source-shaped
    │
  mapping            → DMO (canonical model)
```

Ingestion's job ends at the DLO. Everything after that is [data modeling](../03-data-modeling-dso-dlo-dmo/notes.md).

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Configure a CRM data stream and watch the DLO populate — [lab-01](../10-lab-environment/labs/lab-01-home-org-crm-connector.md), then [lab-02](../10-lab-environment/labs/lab-02-external-org-connection.md) for an org that isn't the home org.
- [ ] Set up a batch stream and a streaming stream, then compare observed latency — [lab-03](../10-lab-environment/labs/lab-03-ingestion-api-any-org.md) does both over the Ingestion API.
- [ ] **The instructive lab:** ground an agent on a scheduled stream, change the source record, and ask the agent about it before the refresh. Watch it answer confidently and wrongly. That's the failure mode, made visible.
- [ ] Audit an org's streams and mark each one agent-facing or analytics-facing.

## Gotchas & sharp edges

- **Stale grounding is the #1 "the agent was wrong" root cause** — and it's misdiagnosed as a model problem almost every time.
- **Don't bypass Data 360 to get freshness.** Calling CRM directly from an action loses the unified profile and its governance. Accelerated Data Ingest exists precisely so you don't have to.
- **Refresh schedule is a cost lever.** Over-refreshing everything is a common and invisible waste.
- **Ingestion ≠ modeling.** Landing data in a DLO does nothing useful until it's mapped to a DMO. New starters routinely think they're done at ingestion.
- **Ingested ≠ resolved.** Two records for the same person stay two profiles until identity resolution runs. See [identity resolution](../04-identity-resolution/notes.md).
- **Watch the volume-to-profile relationship.** Under profile-based pricing you're billed on unified profiles, not rows — but sloppy ingestion of duplicate-heavy sources inflates the profile count downstream.

## Related topics

- [Orientation](../01-orientation/notes.md) — where ingestion sits in the five-step flow
- [Data modeling DSO → DLO → DMO](../03-data-modeling-dso-dlo-dmo/notes.md) — what happens next
- [Zero copy & BYOL](../06-zero-copy-byol/notes.md) — the alternative to copying
- [Identity resolution](../04-identity-resolution/notes.md) — turning ingested rows into profiles
- [Data engineering patterns](../../00-core-skills/04-data-engineering/notes.md) — batch vs streaming, vendor-neutral
