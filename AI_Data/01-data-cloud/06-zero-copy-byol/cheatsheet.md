# Zero Copy & BYOL Federation — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Query Snowflake / BigQuery / Databricks / Redshift **in place** — no movement, no duplication, no reconciliation jobs — at the cost of inheriting the source's query performance.

## Key terms
| Term | Definition |
|---|---|
| Zero copy / BYOL | Federation: bring your own lake, query where the data lives. |
| AWS Glue federation | **GA** — proposal-safe. |
| Fabric OneLake federation | **Beta** — prototype only, no support commitment. |
| Databricks IdP auth | Summer '26 — the security-review unlock, not a feature win. |

## Rules of thumb

- **Zero copy** when data is large, already governed elsewhere, freshness matters, or compliance forbids copying.
- **Ingest** when you need Data 360 features on it (identity resolution, segmentation performance), predictable latency, or real-time agent grounding.
- Read Beta labels **literally**: GA goes in the delivery plan, Beta goes in the demo.
- Discuss query performance with whoever owns the warehouse — it becomes your agent's latency.

## Exam traps / common confusions

- **Federated ≠ free.** No Data 360 storage cost, but source-side compute on every query.
- **Zero copy doesn't fix freshness** — it removes pipeline lag, but a stale source is still stale.
- Not every Data 360 feature behaves identically on federated data — check identity resolution and segmentation first.
- Clients hear "zero copy" as "no cost / no work". Set expectations early.

## Minimal example

The decision, in one pass:

```
Is it needed for identity resolution or fast segmentation?  → INGEST
Is it huge, governed elsewhere, or copy-prohibited?         → ZERO COPY
Does an agent ground on it in real time?                    → INGEST (accelerated)
Only occasional analytical reach?                           → ZERO COPY

Then check status: AWS Glue = GA ✓   Fabric OneLake = Beta ✗
```
