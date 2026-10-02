# SF_Data_360

> **Start at [../HOME.md](../HOME.md)** — what to study next, rebuilt from the notes.

Data 360 only. Ingestion, data model objects, identity resolution, segments, zero-copy, vector search, RAG.

Data 360 is the current name. Data Cloud is the old one. The platform underneath lives in [SF_core/](../SF_core/README.md).

> Currency: **Summer '26 (API 67.0)** · what changed: [RELEASE-RADAR/data-360.md](../RELEASE-RADAR/data-360.md)

## Learning path

Read top to bottom. `#` is display order only — filenames carry no number, so reordering costs one row edit.

**8 topics** · 15 gaps open · 0 complete · newest 2026-10-02 · oldest 2026-10-02

**25 hands-on labs · ~9 h.** This file is the reading order. When the goal is to *do* something, open [PRACTICE.md](PRACTICE.md) instead.

> **Sourcing.** These notes were written on 2026-10-02 while help.salesforce.com, developer.salesforce.com and trailhead.salesforce.com were blocked from the authoring session. Facts come from the archived roadmap notes and were confirmed against Salesforce search extracts (`via search` in each note's Sources). Every note keeps one gap: re-read the full pages.

| # | Topic | One line | Level | Status | Pre | Created | Updated |
|---|---|---|---|---|---|---|---|
| 1 | [Lab Environment](lab-environment.md) | What a Developer Edition can do, and which orgs can feed it | basic | 🌱 1 open | — | 2026-10-02 | 2026-10-02 |
| 2 | [Ingestion & Data Streams](ingestion-and-data-streams.md) | Connector → data stream → DLO; freshness is decided per stream | basic | 🌱 2 open | 1 | 2026-10-02 | 2026-10-02 |
| 3 | [Data Model: DSO, DLO & DMO](data-model-dso-dlo-dmo.md) | Raw → lake → canonical model, data spaces and the zero-row trap | basic | 🌱 2 open | 2 | 2026-10-02 | 2026-10-02 |
| 4 | [Identity Resolution](identity-resolution.md) | Match rules, reconciliation rules, and why over-matching is the dangerous direction | working | 🌱 2 open | 3 | 2026-10-02 | 2026-10-02 |
| 5 | [Calculated Insights & Segmentation](calculated-insights-and-segmentation.md) | Metrics over profiles, segments, activation targets | working | 🌱 2 open | 4 | 2026-10-02 | 2026-10-02 |
| 6 | [Zero Copy & BYOL](zero-copy-and-byol.md) | Live Query, Accelerated Query, File Federation — and reading GA vs Beta literally | working | 🌱 2 open | 2 | 2026-10-02 | 2026-10-02 |
| 7 | [Vector Search & RAG](vector-search-and-rag.md) | Chunk → embed → index → retriever, and when a data graph beats it | working | 🌱 2 open | 3 | 2026-10-02 | 2026-10-02 |
| 8 | [Data 360 DevOps](data-360-devops.md) | DevOps vs standard data kits, metadata-only sandboxes, Code Extension | basic | 🌱 2 open | 3 | 2026-10-02 | 2026-10-02 |

## Seams into SF_core

| Topic | SF_core note |
|---|---|
| Data 360 as a data tier, zero-copy | [08-data · 18 Zero-copy & Data 360 as data tier](../SF_core/08-data-modeling-and-large-data-volumes/18-zero-copy-and-data-360-as-data-tier.md) |
| Data-Cloud-triggered flows, data actions | [04-flow · 22 Data Cloud-triggered flows & data actions](../SF_core/04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md) |
| Identity resolution vs CRM dedup | [08-data · 19 Data quality, deduplication & MDM](../SF_core/08-data-modeling-and-large-data-volumes/19-data-quality-deduplication-and-mdm.md) |
| Query language for the platform side | [10-soql-and-sosl · INDEX](../SF_core/10-soql-and-sosl/INDEX.md) |
| Ingestion over the API | [06-integration-and-apis · INDEX](../SF_core/06-integration-and-apis/INDEX.md) |

## Seams into SF_Agentforce

| Topic | Note |
|---|---|
| Grounding a prompt on Data 360 | [SF_Agentforce · Grounding a Prompt Template](../SF_Agentforce/grounding-a-prompt-template.md) |

## Backlog — referenced elsewhere, not yet fed

Other notes in the repo link here for these topics. The count is how many places expect them, so it doubles as a priority order.

Nothing outstanding. All eight backlog topics got a note on 2026-10-02; their old row counts were how the reading order above was chosen.

## Unfiled

[_inbox.md](_inbox.md) — anything captured that does not have a home yet.
