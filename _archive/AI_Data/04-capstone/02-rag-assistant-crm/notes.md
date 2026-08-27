# Capstone: RAG Assistant over CRM Data

> Track: Capstone · Roadmap: Phase 05 · Weeks 21–26 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/agentforce-platform.md](../../05-release-radar/agentforce-platform.md)

**Roadmap scope:** Data 360 vector search + Claude: grounded answers over cases, knowledge, and account history, with citations back to records.

> **What changed in Summer '26:** don't hand-roll retrieval. **Agentforce Data Libraries** plus the **ADL Connect API (Beta)** give you a managed, scriptable RAG pipeline, and **Code Extension** finally exposes the chunking logic that actually determines quality. Build on those, and spend your effort on the levers that matter.

## What is it?

An assistant that answers questions about customers by retrieving from CRM content and citing its sources — built on the platform's productized RAG rather than assembled from parts.

**Scope it narrowly.** "Answers questions about customers" is not a project. "Answers support questions about a specific product line, citing the runbook section used" is. A narrow scope is what makes evaluation possible, and evaluation is what makes this a portfolio piece.

## Why it matters (for the AI-Salesforce architect role)

**This project is where you demonstrate that you know retrieval quality is an engineering problem, not a prompt problem.**

Most people building a RAG demo tune the prompt. The levers that actually move quality, in order:

| Lever | Why it dominates |
|---|---|
| **Chunking** | Retrieval returns chunks, not documents. A chunk that splits a procedure yields half an answer. |
| **Source choice** | Data graph for structured, vector search for unstructured. Wrong choice = slow, fuzzy, expensive. |
| **Freshness** | Grounding faithfully returns stale facts if ingestion is behind. |
| **Top-N** | Recall vs. tokens vs. cost per action. |
| Prompt wording | Real, but last. |

**The demonstrable claim:** *"I improved answer accuracy from X to Y by changing chunking strategy, measured against a fixed question set."* That sentence, with real numbers behind it, is worth more than any amount of demo polish.

## How it works

### Build order

1. **Fix the question set first** — 20–30 real questions with known-correct answers. Do this *before* building anything. Without it you have no way to tell whether a change helped, and you'll end up tuning on vibes.
2. **Provision an Agentforce Data Library via the ADL Connect API**, not the UI. Scriptable provisioning is the "grounding as code" story, and it's a differentiator.
3. **Index with default chunking.** Measure against the question set. This is your baseline.
4. **Write a custom chunking Code Extension** — split on document structure (headings, procedure steps, table boundaries) rather than fixed length. Re-index. Measure again.
5. **Add citations** back to source records.
6. **Evaluate with Custom Scorers** — e.g. "did it cite a source", "did it decline when it didn't know".
7. **Compare a data graph** for a structured question and note latency and exactness against vector search.

The delta between steps 3 and 4 is your headline result.

### The five-step ADL provisioning flow

Base: `/services/data/v67.0/einstein/data-libraries`

1. `POST /` → returns `libraryId` (note: `sourceType` is nested under `groundingSource`)
2. `GET /{id}/upload-readiness` → poll
3. `POST /{id}/file-upload-urls` → pre-signed S3 URL, then `PUT` the file (**forward headers verbatim** or 403)
4. `POST /{id}/indexing` → chunk, embed, build retriever
5. Wire into the agent's `knowledge:` block → invoke `AnswerQuestionsWithKnowledge`

**Ready means `retrieverId` is non-null** — *not* when `status` flips. Status leads by 10–30 minutes.

### Where Claude fits

Two legitimate designs, and choosing deliberately is part of the project:

- **In-platform** — the agent runs on Agentforce, grounded by the Data Library, with Claude selected as the model. Trust Layer applies throughout.
- **External** — Claude (Desktop/Code/API) reaches the org through a hosted MCP server and calls a retriever. Better for showing the Claude track; check what Trust Layer coverage still applies.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Write the 20–30 question evaluation set **before** anything else.
- [ ] Script the full five-step ADL provisioning flow.
- [ ] Measure baseline accuracy with default chunking.
- [ ] Write a structure-aware chunking Code Extension, re-index, re-measure.
- [ ] Add citations; verify each one actually supports the claim.
- [ ] Deploy a Custom Scorer for "cited a source" and run it against live sessions.

## Gotchas & sharp edges

- **No question set = no project.** You cannot claim improvement without a fixed baseline.
- **Poll `retrieverId`, not `status`** — 10–30 minute lag, and the failure looks like a broken retriever.
- **`rag_feature_config_id` = `"ARFPC_" + libraryId`.**
- **Forward the S3 pre-signed headers verbatim**, or 403.
- **Re-indexing is expensive.** Test chunking strategies on a small corpus first.
- **Cited ≠ correct.** An agent can cite a chunk it misread. Verify citations support the claim — this is a great thing to demonstrate catching.
- **Use a data graph for structured questions.** Semantic search over structured data is slower, fuzzier and costlier.
- **Stale ingestion defeats good retrieval.** Check freshness before blaming the pipeline.
- **ADL Connect API is Beta** — fine to build on, not to promise contractually.

## Related topics

- [RAG on platform](../../01-data-cloud/08-rag-on-platform/notes.md) — the full pipeline
- [Vector DB & unstructured](../../01-data-cloud/07-vector-db-unstructured/notes.md) — chunking depth
- [Data 360 DevOps](../../01-data-cloud/09-data-360-devops/notes.md) — Code Extension workflow
- [Observability & testing](../../02-salesforce-ai/09-observability-and-testing/notes.md) — Custom Scorers
- [Capstone: MCP server](../01-mcp-server-salesforce/notes.md) — if Claude connects externally
- [Write-up & pitch](../04-writeup/notes.md) — where the before/after numbers go
