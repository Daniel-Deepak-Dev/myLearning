# Ingestion — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Data streams pull from connectors on a batch, streaming or **accelerated** schedule and land data as DLOs — and the schedule you pick decides whether an agent grounded on it will be right.

## Key terms
| Term | Definition |
|---|---|
| Data stream | A configured ingestion feed from a connector on a batch or streaming schedule. |
| Accelerated Data Ingest | Real-time CRM data, no pipeline lag. **GA** Summer '26. |
| DLO | Where ingested data lands, still source-shaped. Ingestion's job ends here. |
| Connector | CRM, Marketing Cloud, S3, Web/Mobile SDK, plus lakehouse federation. |

## Rules of thumb

- **If an agent grounds on it, it needs real-time.** If only a dashboard reads it, scheduled is fine. Decide per stream, not per project.
- Never bypass Data 360 to get freshness — calling CRM directly from an action loses the unified profile and its governance.
- Refresh schedule is a **cost lever**; over-refreshing everything is invisible waste.
- Three ways in: ingest (copy), zero-copy federation (query in place), accelerated (real-time CRM).

## Exam traps / common confusions

- **Ingestion ≠ modeling.** Data in a DLO does nothing until it's mapped to a DMO.
- **Ingested ≠ resolved.** Two records for one person stay two profiles until identity resolution runs.
- Stale grounding is the **#1 root cause** of "the agent was wrong" — and is misdiagnosed as a model problem nearly every time.
- Billing is on **unified profiles**, not ingested rows — but duplicate-heavy ingestion inflates profiles downstream.

## Minimal example

Freshness decision, per stream:

```
Does an AGENT read it?        → accelerated / real-time
Does a SEGMENT activate it?   → match the activation cadence
Does only a DASHBOARD read it?→ scheduled batch
Historical / immutable?       → one-time load
```
