# Calculated Insights & Segmentation — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Insights compute metrics on a schedule, segments slice audiences from them, activation publishes to targets — and the **semantic layer** is what stops an agent inventing its own definition of "churn".

## Key terms
| Term | Definition |
|---|---|
| Calculated Insight | Scheduled metric over DMOs, SQL-like definition (LTV, engagement, churn risk). |
| RFM | Recency / Frequency / Monetary — the other canonical insight. Emits a **tier label**, not a number. |
| Segment | Audience slice from profiles + attributes + insights. The unit you activate. |
| Tableau Semantics | The semantic layer — standardizes what a metric *means*, in business language. |
| OSI | Vendor-neutral YAML standard for semantic models. Core spec finalized Feb 2026. |

## Rules of thumb

- **Insight defines how a number is computed; the semantic layer defines what it means.** Agents need both.
- Prefer grounding an agent on an **insight** over raw records for analytical questions — fewer tokens, governed meaning, no model-computed arithmetic.
- Match segment refresh to the **activation cadence**, not to "as often as possible".
- The three legs of grounding: Intelligent Context (unstructured) + semantic layer (meaning) + zero-copy (reach). Weakest one caps trust.

## Exam traps / common confusions

- **Agents never ask what a metric means** — ambiguity yields confident wrong numbers.
- Insights run **on a schedule**, so an agent can ground on a stale metric.
- Insights compute **per unified profile** — fragmented profiles produce wrong metrics; the bug is upstream in identity resolution.
- **RFM ranks are relative** — quintiles re-cut every run, so a tier can change because the population moved, not the customer.
- **SQL from Apex** (Summer '26) carries the same dataspace trap: omit it on a DLO query → zero records, silently.
- A metric with two definitions is a **governance** problem; the semantic layer surfaces it, it doesn't decide.

## Minimal example

```
Calculated Insight  "LTV_90d"
   SUM(order.amount) OVER (PARTITION BY profileId
                           ORDER BY orderDate
                           ROWS BETWEEN 90 PRECEDING AND CURRENT ROW)
        ↓
Segment  "High Value, No Purchase 30d"   → activate to Marketing Cloud
        ↓
Agent grounding: "is this customer high value?"
   answers from the COMPANY's definition, not its own
```
