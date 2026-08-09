# 01 · Data 360 (formerly Data Cloud)

The data layer: ingest → model → unify → insight → activate. Roadmap tag: **Data Cloud** (cyan).
Cert target: **[Data 360 Consultant](_cert-data-cloud-consultant/exam-guide.md)** (end of Phase 02).

> **Naming.** The product is **Data 360** since Dreamforce 2025, and the certification renamed on 2026-03-27 (exam code `Data-Con-101` unchanged). Folder paths keep the old `data-cloud` names so existing links and the dashboard keep working.
>
> **The 2026 reframe:** Data 360 is no longer just a CDP. It's the **context engine that grounds AI agents** — and it ships **monthly**, not on the seasonal cadence.

| Topic | What it covers | Quick recall |
|---|---|---|
| [Orientation](01-orientation/notes.md) | Lakehouse platform, the Data 360 rename and full lineage, how it sits beside core CRM, **multi-org via Data Cloud One**, the end-to-end flow | [cheatsheet](01-orientation/cheatsheet.md) · [flashcards](01-orientation/flashcards.md) |
| [Ingestion](02-ingestion/notes.md) | Data streams, connectors, batch vs streaming vs **Accelerated Data Ingest (GA)** — and why stale grounding is the #1 agent failure | [cheatsheet](02-ingestion/cheatsheet.md) · [flashcards](02-ingestion/flashcards.md) |
| [Data Modeling: DSO → DLO → DMO](03-data-modeling-dso-dlo-dmo/notes.md) | Raw → lake → canonical model; **`SET OPTIONS`**, dataspaces, SQL from Apex. The heart of the Consultant exam | [cheatsheet](03-data-modeling-dso-dlo-dmo/cheatsheet.md) · [flashcards](03-data-modeling-dso-dlo-dmo/flashcards.md) |
| [Harmonization & Identity Resolution](04-identity-resolution/notes.md) | Match and reconciliation rules — and why profile-based pricing made match quality a recurring cost | [cheatsheet](04-identity-resolution/cheatsheet.md) · [flashcards](04-identity-resolution/flashcards.md) |
| [Calculated Insights & Segmentation](05-insights-segmentation/notes.md) | SQL-like metrics, segments, activation, and the **semantic layer** that stops agents inventing definitions | [cheatsheet](05-insights-segmentation/cheatsheet.md) · [flashcards](05-insights-segmentation/flashcards.md) |
| [Zero Copy & BYOL Federation](06-zero-copy-byol/notes.md) | Querying Snowflake/BigQuery/Databricks in place; AWS Glue **GA** vs Fabric OneLake **Beta** | [cheatsheet](06-zero-copy-byol/cheatsheet.md) · [flashcards](06-zero-copy-byol/flashcards.md) |
| [Vector Database & Unstructured Data](07-vector-db-unstructured/notes.md) | Search indexes, embeddings, **custom chunking via Code Extension**, Intelligent Context | [cheatsheet](07-vector-db-unstructured/cheatsheet.md) · [flashcards](07-vector-db-unstructured/flashcards.md) |
| [RAG on Platform](08-rag-on-platform/notes.md) | Retrievers, data graphs, **Agentforce Data Libraries + the ADL Connect API** — Salesforce's productized RAG | [cheatsheet](08-rag-on-platform/cheatsheet.md) · [flashcards](08-rag-on-platform/flashcards.md) |
| [Data 360 DevOps](09-data-360-devops/notes.md) 🆕 | Python Code Extension, data kits, `@IntegrationTest`, the Data 360 MCP server and its facade-tool pattern | [cheatsheet](09-data-360-devops/cheatsheet.md) · [flashcards](09-data-360-devops/flashcards.md) |

## Cert prep
- [Exam guide breakdown](_cert-data-cloud-consultant/exam-guide.md) — renamed to **Data 360 Consultant**
- [Practice questions](_cert-data-cloud-consultant/practice-questions.md)
- [Weak areas](_cert-data-cloud-consultant/weak-areas.md)

## Staying current
Data 360 ships **monthly**. Check the [monthly release notes](https://help.salesforce.com/s/articleView?id=release-notes.rn_c360_truth.htm&release=262&type=5) and [05-release-radar/data-360.md](../05-release-radar/data-360.md) rather than only the three seasonal releases.
