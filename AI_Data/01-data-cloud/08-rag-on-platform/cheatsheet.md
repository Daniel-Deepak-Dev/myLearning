# RAG on Platform — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Salesforce's productized RAG: Agentforce Data Libraries and retrievers ground agent answers in Data 360 content — and since Summer '26 the whole lifecycle is scriptable via the ADL Connect API.

## Key terms
| Term | Definition |
|---|---|
| Agentforce Data Library (ADL) | Managed grounding store over Knowledge or uploaded files; exposes a retriever. |
| Retriever | Configured query against a search index or data graph. |
| Data graph | Precomputed denormalized profile view — **millisecond** reads. Use for structured data. |
| ADL Connect API | Beta. Makes grounding configuration a pipeline step, not click-ops. |

## Rules of thumb

- **Structured question → data graph. Unstructured → vector search.** Semantic search over structured data is slower, fuzzier and costlier.
- Quality levers in order: chunking → right source → top-N → filters → citations.
- Citations make errors *findable* — that's most of their value, and what earns client trust.
- Grounding can't fix stale ingestion; retrieval faithfully returns old facts.

## Exam traps / common confusions

- **Poll `retrieverId` non-null, not `status`** — status leads the retriever by **10–30 minutes**.
- **`rag_feature_config_id` = `"ARFPC_" + libraryId`**, not the raw ID.
- `sourceType` is nested under `groundingSource` (`SFDRIVE` / `KNOWLEDGE` / `RETRIEVER`), not top-level.
- Forward the S3 pre-signed headers **verbatim** or you get a 403.
- **Cited ≠ correct.** An agent can cite a chunk it misread.

## Minimal example

ADL Connect API, five steps — base `/services/data/v67.0/einstein/data-libraries`:

```
1. POST  /                          → libraryId
2. GET   /{id}/upload-readiness     → poll
3. POST  /{id}/file-upload-urls     → pre-signed S3 URL, then PUT (headers verbatim!)
4. POST  /{id}/indexing             → chunk + embed + build retriever
5. wire into .agent  knowledge:     → AnswerQuestionsWithKnowledge

READY = retrieverId non-null.  NOT status.
```
