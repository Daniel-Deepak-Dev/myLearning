# Calculated Insights & Segmentation

> Track: Data 360 · Roadmap: Phase 02 · Weeks 5–8 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/data-360.md](../../05-release-radar/data-360.md)

**Roadmap scope:** Build metrics (LTV, engagement scores) with SQL-like expressions, slice audiences into segments, and activate them to targets.

## What is it?

Three chained concepts:

| Concept | What it is |
|---|---|
| **Calculated Insight** | A metric computed over Data 360 data on a schedule, defined with a SQL-like expression — lifetime value, engagement score, churn risk |
| **Segment** | An audience slice built from profiles, attributes and insights — the unit you activate |
| **Activation** | Publishing a segment or data to a target where action happens: Marketing Cloud, ad platforms, CRM |

Insights feed segments; segments get activated. In 2026, a fourth consumer joined: **agents ground on insights too.**

## Why it matters (for the AI-Salesforce architect role)

**The semantic layer is the 2026 story here, and it's the part worth understanding properly.**

When a human reads a dashboard labelled "churn rate", they bring context: they know which definition the company uses, or they know to ask. **An agent doesn't ask.** Given an ambiguous metric, it produces a confident number computed from whichever definition it happened to find — or one it inferred.

**Tableau Semantics** is Salesforce's semantic layer: it standardizes metric definitions and translates data into business language, so an agent asked *"what was churn last quarter"* returns the company's definition of churn rather than inventing one.

Related and worth knowing by name: **OSI**, a vendor-neutral, YAML-based open-source standard for interoperable semantic models, metrics and relationships. Core spec finalized **February 2026**. It matters because semantic definitions becoming portable is the same portability move as Agent Script compiling to JSON.

**The architect's framing:** a calculated insight defines *how* a number is computed. The semantic layer defines *what the number means* and makes that meaning available to a machine. Agents need both. This is one of the clearest places where the data track directly determines AI answer quality.

### The three legs of enterprise grounding

Worth memorizing as a set, because an agent answer is only as trustworthy as the weakest of them:

| Leg | Provides | Covered in |
|---|---|---|
| **Intelligent Context** | Unstructured content as grounding data | [Vector DB & unstructured](../07-vector-db-unstructured/notes.md) |
| **Semantic layer** | Agreed meaning | This topic |
| **Zero-copy federation** | Reach without copying | [Zero copy & BYOL](../06-zero-copy-byol/notes.md) |

## How it works

### Calculated insights

Defined with SQL-like expressions over DMOs, computed on a schedule, and stored as attributes available to segments, activations and agents.

Because they're SQL-like, this is where your [SQL fluency](../../00-core-skills/01-sql/notes.md) pays off directly — aggregations, window functions and CTEs are the working vocabulary.

**Summer '26 addition:** you can now **run SQL from Apex** against Data 360. That means an Apex-backed agent action can compute a rolling aggregate or a multi-table join inline, rather than depending on a pre-computed insight refreshed on a schedule. Note the same dataspace trap as everywhere else — omit it on a DLO query and you get zero records, silently.

### Segmentation

Segments filter on profile attributes, insights and behavioural data. Two design questions govern them:

1. **Refresh cadence** — how fresh does the membership need to be? Match it to the activation cadence, not to "as often as possible".
2. **Publish schedule** — activation targets have their own rhythms; over-publishing costs without benefit.

### Insights as agent grounding

An agent grounded on calculated insights answers questions like *"is this customer high value?"* using the company's actual definition of high value. This is often a better grounding source than raw records — it's pre-aggregated, governed and cheap to include in a prompt.

**Prefer an insight over raw record grounding when the question is analytical.** Fewer tokens, governed meaning, and no chance the model computes its own aggregate wrongly.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Write a calculated insight for lifetime value using a window function.
- [ ] Build a segment on that insight and activate it to a target.
- [ ] **The semantic-layer lab:** ask an agent a metric question ("what was churn last quarter") before and after defining the metric in the semantic layer. The before-answer is the whole argument for the feature.
- [ ] Write an Apex method that runs SQL from Apex for an aggregate an agent action needs live.

## Gotchas & sharp edges

- **Agents don't ask what a metric means.** Ambiguous definitions produce confident wrong numbers. This is the failure the semantic layer exists to prevent.
- **Insights run on a schedule.** An agent may ground on a stale insight — the same freshness problem as [ingestion](../02-ingestion/notes.md), one layer up.
- **Segment refresh is a cost lever.** Match cadence to activation, not to "as often as possible".
- **Over-publishing to activation targets costs without benefit.** Check the target's own rhythm.
- **SQL from Apex has the dataspace trap** — omit it on a DLO query and get zero records with no error.
- **Insights compute per unified profile**, so fragmented profiles produce wrong metrics. The error originates in [identity resolution](../04-identity-resolution/notes.md).
- **A metric with two definitions in two systems is a governance problem, not a tooling one.** The semantic layer makes the disagreement visible; it doesn't decide for you.

## Related topics

- [Identity resolution](../04-identity-resolution/notes.md) — insights compute per unified profile
- [Data modeling](../03-data-modeling-dso-dlo-dmo/notes.md) — insights are defined over DMOs
- [Zero copy & BYOL](../06-zero-copy-byol/notes.md) — the reach leg of grounding
- [Vector DB & unstructured](../07-vector-db-unstructured/notes.md) — the unstructured leg
- [SQL fluency](../../00-core-skills/01-sql/notes.md) — the expression language
- [Release radar: Data 360](../../05-release-radar/data-360.md) — semantic layer and SQL-from-Apex entries
