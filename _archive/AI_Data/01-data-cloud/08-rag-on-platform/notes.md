# RAG on Platform

> Track: Data 360 · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/agentforce-platform.md](../../05-release-radar/agentforce-platform.md)

**Roadmap scope:** Retrievers and search indexes grounding Agentforce answers in Data 360 content — Salesforce's productized RAG pipeline end to end.

## What is it?

**RAG** — Retrieval-Augmented Generation — is the pattern: retrieve relevant content, inject it into the prompt, generate an answer grounded in it. It's the antidote to hallucination, and Salesforce ships it as a product rather than a pattern you assemble.

### The three grounding sources, and when each fits

| Source | Best for | Latency |
|---|---|---|
| **Agentforce Data Library (ADL)** | Documents: Knowledge articles, uploaded files | Index-time cost, fast at query |
| **Retriever over a search index** | Any indexed unstructured corpus | Fast |
| **Data graph** | Structured profile data — precomputed, denormalized | **Millisecond** real-time reads |

**Data graphs are underused.** For "what do we know about this customer", a data graph beats a vector search: it's precomputed, denormalized, millisecond-fast and exact. Vector search is for *unstructured* content where you don't know which document holds the answer. Choosing the wrong one is a common design error — semantic search over structured data is slower, fuzzier and more expensive than a graph lookup.

## Why it matters (for the AI-Salesforce architect role)

**Grounding configuration became code in Summer '26.** The **ADL Connect API (Beta)** makes the whole Data Library lifecycle scriptable and CI/CD-ready — creating one used to be a manual Setup step.

That's the "grounding as code" half of Headless 360: RAG configuration stops being click-ops and becomes a pipeline step, alongside Agent Script compiling to JSON and scorers deploying as metadata. The pattern across the whole release is consistent — every part of an agent becomes a deployable artifact.

## How it works

### The ADL Connect API — five-step provisioning

Base resource: `/services/data/v67.0/einstein/data-libraries`

1. **Create the library** — a single `POST`. Note `sourceType` is *nested* under `groundingSource` (`SFDRIVE` for files, or `KNOWLEDGE` / `RETRIEVER`). The response returns the `libraryId` every later step needs.
2. **Wait for upload readiness** — poll `GET …/{libraryId}/upload-readiness`. Data 360 is provisioning the objects that hold file metadata behind the scenes.
3. **Upload the file** — request a pre-signed S3 URL from `POST …/{libraryId}/file-upload-urls`, then `PUT` the file to that URL. **Forward the returned headers verbatim or S3 rejects it with a 403.**
4. **Index it** — `POST …/{libraryId}/indexing` chunks, embeds and builds the retriever.
5. **Ground the agent** — wire the library into the `.agent` file's `knowledge:` block and invoke `AnswerQuestionsWithKnowledge` from a subagent.

### Two gotchas worth memorizing

**1. Treat the library as ready when `retrieverId` goes non-null — not when the top-level `status` flips.** Status leads the retriever by **10–30 minutes**. Polling on `status` gives you a library that reports ready and then fails to retrieve, which is a maddening bug to diagnose.

**2. `rag_feature_config_id` is `"ARFPC_" + libraryId`**, not the raw ID.

Both of these cost real time if you meet them the hard way. They're the kind of detail that separates someone who has built this from someone who has read about it.

### The end-to-end path

```
documents / Knowledge
      │  ADL Connect API (create → readiness → upload → index)
   DATA LIBRARY  ─ retrieverId non-null = actually ready
      │
   agent's knowledge: block
      │
   subagent invokes AnswerQuestionsWithKnowledge
      │
   retrieved chunks → prompt → Trust Layer → model
      │
   grounded answer + citations
```

### Quality levers, in order

1. **Chunking** — the biggest lever; custom logic via Code Extension. See [vector DB & unstructured](../07-vector-db-unstructured/notes.md).
2. **Right source** — data graph for structured, vector search for unstructured.
3. **Top-N** — recall vs. tokens vs. cost per action.
4. **Retriever filters** — narrow the corpus before ranking.
5. **Citations** — make the answer checkable; this is what earns client trust.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Provision a Data Library through the **API**, not the UI — all five steps.
- [ ] **Poll on `status` first and watch it lie**, then switch to `retrieverId`. Ten minutes that saves an afternoon.
- [ ] Ground an agent on the library and get an answer with citations back to source documents.
- [ ] Answer the same question via a data graph and via vector search; compare latency and exactness.
- [ ] Script the whole provisioning flow so it runs in CI.

## Gotchas & sharp edges

- **`status` leads `retrieverId` by 10–30 minutes.** Poll on `retrieverId` being non-null.
- **`rag_feature_config_id` = `"ARFPC_" + libraryId`**, not the raw ID.
- **Forward the S3 pre-signed headers verbatim** or you get a 403.
- **`sourceType` is nested under `groundingSource`**, not top-level.
- **ADL Connect API is Beta.** Fine to build on; don't make it contractually load-bearing.
- **Use a data graph for structured data.** Semantic search over structured data is slower, fuzzier and costlier than a graph lookup.
- **Grounding doesn't fix a stale source.** If [ingestion](../02-ingestion/notes.md) is behind, retrieval faithfully returns old facts.
- **Citations aren't automatic quality.** An agent can cite a chunk it misread. Cited ≠ correct, though citations make the error findable — which is most of the value.

## Related topics

- [Vector DB & unstructured](../07-vector-db-unstructured/notes.md) — chunking, embeddings, indexes
- [Prompt Builder](../../02-salesforce-ai/03-prompt-builder/notes.md) — retrievers as a grounding source
- [Agent Script](../../02-salesforce-ai/07-agent-script/notes.md) — the `knowledge:` block
- [Ingestion](../02-ingestion/notes.md) — freshness caps grounding quality
- [Capstone: RAG assistant over CRM data](../../04-capstone/02-rag-assistant-crm/notes.md) — build it
- [Release radar: Agentforce platform](../../05-release-radar/agentforce-platform.md) — the ADL Connect API entry
