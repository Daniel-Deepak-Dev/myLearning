# PRACTICE — SF_Data_360

> The file you open when the goal is **do something**. Reading lives in [INDEX.md](INDEX.md).
>
> **Three rules.** One item under ▶ Next · max 3 in flight · every lab has a time box.
>
> If you catch yourself reading instead of running, you are in the wrong file.

**25 labs · ~9 h total.** Nothing here runs over 45 minutes. If one overruns it was too big — split it into `NNa` / `NNb` rather than letting it become the lab you never start.

Each lab's full wording lives in its own note, as a `- [ ]` line under `## Hands-on`. **Tick it there when it is done** — labs are ticked, not deleted, because work you actually did is a record. That tick is the whole record: [Done](#done) is rebuilt from it.

## A lab is not finished until you have written down what broke

That is the point of the **Done** table's last column. Copy the error string **verbatim** — not paraphrased, not summarised. In six months the notes will have been rewritten and the release will have moved, but an exact error string is still what you type into a search box.

If a lab produced no failure at all, say so — `no failure; worked first time` is a real result and tells you the lab was too gentle.

## Order

The queue is **unblocked-first**, not INDEX order:

- **#1–19** need only a **Developer Edition with Data 360**. Keep test data to a few hundred records: a Developer Edition has 10 GB and no scheduled refreshes, so you run streams and rulesets by hand. **#5** is the only one needing a **second Developer Edition** as a CRM source.
- **#20–22** need **Code Extension tooling** (the Python SDK and CLI plugin) or a **Data 360 sandbox**.
- **#23–25** need a **Snowflake or BigQuery trial** for zero copy, or are a writing exercise.

---

## ▶ Next

**D360-LAB-01 · 15 min · [Lab Environment](lab-environment.md)**

Open Data 360 Setup, and record the data space count, storage used and the limits page. Every later count is compared against this baseline.

---

## In flight — max 3

| Lab | Box | Started | Blocked on |
|---|---|---|---|
| — | — | — | — |

---

## Queue

| # | Lab | Topic | Box | Proves | Needs |
|---|---|---|---|---|---|
| 1 | D360-LAB-01 | [Lab Environment](lab-environment.md) | 15 min | The baseline before any lab | — |
| 2 | D360-INGEST-01 | [Ingestion](ingestion-and-data-streams.md) | 20 min | A green status is not a row count | — |
| 3 | D360-MODEL-01 | [Data Model](data-model-dso-dlo-dmo.md) | 20 min | An unmapped field reads as null | needs #2 |
| 4 | D360-MODEL-02 | [Data Model](data-model-dso-dlo-dmo.md) | 15 min | No dataspace, zero rows, no error | needs #2 |
| 5 | D360-LAB-02 | [Lab Environment](lab-environment.md) | 30 min | The source org needs no Data 360 licence | second Developer Edition |
| 6 | D360-LAB-03 | [Lab Environment](lab-environment.md) | 15 min | Permission failures look like missing data | needs #5 |
| 7 | D360-INGEST-02 | [Ingestion](ingestion-and-data-streams.md) | 30 min | Bulk and streaming feed one stream | — |
| 8 | D360-INGEST-03 | [Ingestion](ingestion-and-data-streams.md) | 15 min | The 200 KB streaming limit | needs #7 |
| 9 | D360-MODEL-03 | [Data Model](data-model-dso-dlo-dmo.md) | 15 min | `NULL` and `''` collapse by default | needs #7 |
| 10 | D360-IDR-01 | [Identity Resolution](identity-resolution.md) | 30 min | The profile-to-source baseline | needs #3, #7 |
| 11 | D360-IDR-02 | [Identity Resolution](identity-resolution.md) | 20 min | The household merge looks like success | needs #10 |
| 12 | D360-IDR-03 | [Identity Resolution](identity-resolution.md) | 20 min | Reconciliation is per field | needs #10 |
| 13 | D360-SEG-01 | [Insights & Segmentation](calculated-insights-and-segmentation.md) | 30 min | Validate an insight with raw SQL | needs #10 |
| 14 | D360-SEG-02 | [Insights & Segmentation](calculated-insights-and-segmentation.md) | 20 min | Segment, activation and target are separate | needs #13 |
| 15 | D360-SEG-03 | [Insights & Segmentation](calculated-insights-and-segmentation.md) | 25 min | RFM tiers move with the population | needs #10 |
| 16 | D360-INGEST-04 | [Ingestion](ingestion-and-data-streams.md) | 20 min | Freshness belongs to the stream | needs #2, Prompt Builder |
| 17 | D360-RAG-01 | [Vector Search & RAG](vector-search-and-rag.md) | 30 min | Retrieval returns chunks | Knowledge articles |
| 18 | D360-RAG-02 | [Vector Search & RAG](vector-search-and-rag.md) | 25 min | Hybrid catches exact codes | needs #17 |
| 19 | D360-RAG-03 | [Vector Search & RAG](vector-search-and-rag.md) | 20 min | Chunk boundaries decide the answer | needs #17 |
| 20 | D360-OPS-03 | [DevOps](data-360-devops.md) | 30 min | Author is not operator | Python SDK + CLI plugin |
| 21 | D360-OPS-01 | [DevOps](data-360-devops.md) | 30 min | What a data kit carries, and what it doesn't | Data 360 sandbox |
| 22 | D360-OPS-02 | [DevOps](data-360-devops.md) | 15 min | Sandbox connections arrive Inactive | needs #21 |
| 23 | D360-ZC-01 | [Zero Copy](zero-copy-and-byol.md) | 30 min | Federated data never lands in a DLO | warehouse trial |
| 24 | D360-ZC-02 | [Zero Copy](zero-copy-and-byol.md) | 20 min | Acceleration trades freshness for speed | needs #23 |
| 25 | D360-ZC-03 | [Zero Copy](zero-copy-and-byol.md) | 15 min | Defend zero copy vs ingestion per feature | — |

---

## Done

**Generated from the ticked labs — do not add rows by hand.** Tick `- [x]` in the
note and run `python scripts/vault.py fix`; the row appears here. The `What broke`
cell is yours: fill it in and it is preserved on every rebuild.

| Lab | Date | What broke — verbatim |
|---|---|---|
| — | — | — |

---

## Parked

Nothing yet. Park a lab here rather than leaving it in the queue when it is blocked on something outside your control — a licence, a Beta, a region restriction — and say what would unblock it.
