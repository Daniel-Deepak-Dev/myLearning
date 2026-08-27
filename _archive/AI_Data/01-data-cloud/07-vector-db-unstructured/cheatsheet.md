# Vector Database & Unstructured Data — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Documents are chunked, embedded and stored in Data 360's vector database so a retriever can fetch them by meaning — and **chunking is the biggest lever on whether any of it works**.

## Key terms
| Term | Definition |
|---|---|
| Search index | The indexed corpus — chunked, embedded, semantically searchable. |
| Retriever | The configured *query* against that index. Not the same thing as the index. |
| Chunking | Splitting documents before embedding. Now customizable via Python **Code Extension**. |
| Intelligent Context | Low-code extraction of PDFs/tables/images into grounding data; same doc, multiple business perspectives. |

## Rules of thumb

- Tune in order: **chunking → overlap → structure awareness → top-N → filters.** Everything inherits chunking, and re-indexing is expensive.
- Design chunks to be **independently meaningful** — retrieval returns chunks, not documents.
- Split on structure (headings, table boundaries, procedure steps), not fixed length.
- Top-N is a cost lever: every retrieved chunk is tokens, billed per action.

## Exam traps / common confusions

- **Search index ≠ retriever.** Index = the corpus; retriever = the query against it.
- **Semantic search finds *similar*, not *correct*.** A confidently-retrieved wrong chunk yields a wrong answer.
- **Context Indexing GA is unconfirmed** as of 2026-07-28 — don't state it as GA without checking the monthly notes.
- Code Extension has an **author ≠ operator** split: developers write it, Data Cloud Architect perm set runs and monitors it.
- Embedded content carries no sharing model by itself — decide who can retrieve what before indexing sensitive docs.

## Minimal example

Chunking failure modes, memorized as a set:

```
too large      → dilutes embedding, burns tokens
too small      → loses context, "it" has no referent
mid-procedure  → agent answers with half a process, confidently
no overlap     → misses answers straddling a boundary
ignores tables → rows separated from headers = meaningless
```
