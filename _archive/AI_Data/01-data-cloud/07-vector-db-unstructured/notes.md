# Vector Database & Unstructured Data

> Track: Data 360 · Roadmap: Phase 02 · Weeks 5–8 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/data-360.md](../../05-release-radar/data-360.md)

**Roadmap scope:** Search indexes, chunking, embeddings, and semantic search inside Data 360 — the retrieval layer your AI agents will stand on.

## What is it?

Data 360's built-in **vector database** stores embeddings for unstructured content — PDFs, call transcripts, Knowledge articles — so it can be searched by *meaning* rather than by keyword.

The pipeline:

```
document (PDF, transcript, article)
     │
  CHUNKING          split into pieces  ← the biggest quality lever
     │
  EMBEDDING         each chunk → a vector
     │
  SEARCH INDEX      vectors stored, semantically searchable
     │
  RETRIEVER         a configured query that fetches the top-N relevant chunks
     │
  grounds a prompt / agent answer
```

A **search index** is the indexed corpus. A **retriever** is the configured query against it. Both terms appear on the exam and they aren't interchangeable.

## Why it matters (for the AI-Salesforce architect role)

**Chunking is usually the single biggest lever on retrieval quality — and until Summer '26 it was a black box.**

That's the headline change. **Code Extension** lets you deploy custom **Python** scripts implementing **custom chunking logic** on search index creation. If you do RAG work, this is the most consequential Data 360 feature of the release.

Why chunking matters so much: retrieval returns *chunks*, not documents. If a chunk splits a procedure in half, the agent gets half a procedure and answers confidently from it. If chunks are too large, each one carries irrelevant text that dilutes the embedding and wastes tokens. If they're too small, they lose the context that made them meaningful.

**The classic failure modes:**

| Chunking mistake | What the agent does |
|---|---|
| Chunks too large | Retrieves loosely-relevant text, dilutes the answer, burns tokens |
| Chunks too small | Loses context; "it" no longer has a referent |
| Split mid-procedure | Answers with half a process, confidently |
| No overlap | Misses answers that straddle a boundary |
| Ignoring structure | Table rows separated from headers become meaningless |

Structure-aware chunking — splitting on headings, keeping tables intact, preserving procedure steps together — is what custom chunking is *for*.

### Intelligent Context

The companion capability: **Intelligent Context** automatically extracts and structures unstructured content (PDFs, tables, images, flowcharts) into grounding data through a low-code pipeline.

Its distinctive feature is genuinely interesting: you can configure context so the **same document is interpreted from multiple business perspectives**. One contract can yield a legal view and a commercial view without duplicating the source.

> **Status caution:** *Context Indexing* was reported in June 2026 as expected to reach GA "later in July 2026", but no confirmation was found as of 2026-07-28. Treat its status as open and re-check against the monthly Data 360 release notes. Same for Document AI upgrades and secondary indexes.

## How it works

### Custom chunking via Code Extension

Deploy Python scripts that run in isolated containers on the platform. Two current uses: batch data transformations, and **custom chunking logic on search index creation**.

Workflow: author and debug locally with the [Data Custom Code Python SDK](https://pypi.org/project/salesforce-data-customcode/) plus the Salesforce CLI Code Extension plugin → validate against a sandbox → deploy → run → monitor via the **code extensions log DLO**.

**Note the separation of duties baked into the permission model:** developers author the code; users with the **Data Cloud Architect** permission set run and monitor it. Author ≠ operator. Details in [Data 360 DevOps](../09-data-360-devops/notes.md).

### Tuning retrieval

| Lever | Effect |
|---|---|
| Chunk size | Context per chunk vs. precision |
| Chunk overlap | Catches answers straddling boundaries; costs storage |
| Structure awareness | Keeps tables, headings, procedures coherent |
| Top-N returned | More recall, more tokens, more cost per action |
| Filters on the retriever | Narrows the corpus before similarity ranking |

Tune in that order. Chunking first — everything downstream inherits it, and re-indexing after a chunking change is expensive.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Build a search index over a handful of PDFs and query it with a retriever.
- [ ] **The chunking experiment:** index the same corpus at three chunk sizes and compare retrieval quality on ten fixed questions. This is the lab that teaches RAG.
- [ ] Write a custom chunking Code Extension that splits on document headings rather than fixed length.
- [ ] Deliberately split a procedure mid-way and watch the agent answer with half of it.

## Gotchas & sharp edges

- **Chunking is the biggest lever, and it's the one people skip.** Most "RAG doesn't work" reports are chunking problems.
- **Retrieval returns chunks, not documents.** Design chunks to be independently meaningful.
- **Re-indexing after a chunking change is expensive.** Get it approximately right before indexing a large corpus.
- **Semantic search finds *similar*, not *correct*.** A confidently-retrieved wrong chunk still produces a wrong answer.
- **Top-N is a cost lever** — every retrieved chunk is tokens, and Agentforce bills per action.
- **Context Indexing GA is unconfirmed** as of 2026-07-28. Don't state it as GA to a client without checking.
- **Embedded content inherits no sharing model by itself.** Think about who can retrieve what before indexing sensitive documents.

## Related topics

- [RAG on platform](../08-rag-on-platform/notes.md) — retrievers and Data Libraries end to end
- [Data 360 DevOps](../09-data-360-devops/notes.md) — Code Extension authoring and deployment
- [Insights & segmentation](../05-insights-segmentation/notes.md) — the meaning leg of grounding
- [AI theory: embeddings & chunking](../../00-core-skills/03-ai-theory/notes.md) — the vendor-neutral fundamentals
- [Capstone: RAG assistant](../../04-capstone/02-rag-assistant-crm/notes.md) — build it
