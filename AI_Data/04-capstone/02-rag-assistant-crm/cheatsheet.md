# Capstone: RAG Assistant over CRM Data — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Build on Agentforce Data Libraries + the ADL Connect API, then prove you moved answer accuracy by **changing chunking** — measured against a fixed question set.

## Key terms
| Term | Definition |
|---|---|
| Agentforce Data Library | Managed grounding store + retriever over Knowledge or uploaded files. |
| ADL Connect API (Beta) | Scriptable, CI-ready provisioning — "grounding as code". |
| Code Extension | Python custom chunking on index creation. The real quality lever. |
| Custom Scorer | Graded evaluation of live sessions, deployable as metadata. |

## Rules of thumb

- **Write the 20–30 question evaluation set before building anything.** No baseline, no claim.
- Quality levers in order: chunking → source choice → freshness → top-N → prompt wording (last).
- Split chunks on **structure** (headings, procedure steps, table boundaries), not fixed length.
- Structured question → data graph. Unstructured → vector search.
- Scope narrowly: "support questions on one product line, citing the runbook section" beats "answers about customers".

## Exam traps / common confusions

- **Ready = `retrieverId` non-null**, not `status` — a 10–30 minute lag that looks like a broken retriever.
- **`rag_feature_config_id` = `"ARFPC_" + libraryId`**; `sourceType` nests under `groundingSource`.
- Forward S3 pre-signed headers **verbatim** or 403.
- **Cited ≠ correct** — verify citations actually support the claim.
- Re-indexing is expensive; test chunking on a small corpus first.

## Minimal example

The result that makes this a portfolio piece:

```
fixed question set (n=25, known answers)
   ├─ default chunking      → baseline accuracy
   └─ structure-aware chunk → measured accuracy
                              (Code Extension, split on headings)

"Improved accuracy from X to Y by changing chunking strategy,
 measured against a fixed question set."
```
