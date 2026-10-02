---
vault: SF_Data_360
format: light
level: working
status: open
gaps: 2
labs: 3
created: 2026-10-02
updated: 2026-10-02
currency: "Summer '26 (API 67.0)"
---
# Vector Search & RAG

**One line:** Data 360 chunks and embeds unstructured content into a **search index**; a **retriever** queries that index to ground a prompt template or an agent. That is retrieval-augmented generation (RAG).

**Reach for it when:** an agent must answer from documents (Knowledge, PDFs, transcripts), or a RAG answer is confidently wrong.

## Key points

- **The pipeline:** document → **chunking** → **embedding** → **search index** → **retriever** → prompt. A search index is the indexed corpus; a retriever is the configured query against it. They are not the same thing.
- **Three index types:** keyword, vector and **hybrid**. A hybrid index builds both, queries both (semantic and lexical), then merges and ranks the results.
- **Chunking is usually the biggest quality lever.** Retrieval returns chunks, not documents. A chunk split mid-procedure gives the agent half a procedure.
- **Custom chunking (Summer '26):** with **Code Extension**, a deployed **Python** function can be chosen as the chunking strategy in a search index's Advanced Setup → [DevOps](data-360-devops.md).
- **Retrievers ground prompt templates.** They supply relevant, specialised content at run time → [SF_Agentforce · Grounding a prompt template](../SF_Agentforce/grounding-a-prompt-template.md).
- **Unstructured files arrive as a UDLO mapped to a UDMO** (unstructured data lake object → unstructured data model object). From a blob store, Data 360 doesn't import the files; the UDMO references them, and the search index is built on it.
- **Structured questions want a data graph, not vector search.** For "what do we know about this customer", a precomputed data graph answers in milliseconds, exactly. Semantic search over structured data is slower and fuzzier.
- **A data graph combines related DMO data into one JSON blob.** A **standard** data graph refreshes with a delay of minutes to hours. A **real-time** data graph refreshes continuously and is read in milliseconds.

## Gotchas

- **Most "RAG doesn't work" reports are chunking problems**, and chunking is the step people skip.
- **Re-indexing after a chunking change is expensive.** Get chunking roughly right before indexing a large corpus.
- **Semantic search finds similar, not correct.** A confidently retrieved wrong chunk still produces a wrong answer.
- **Top-N is a cost lever.** Every retrieved chunk is tokens in every call.
- **Indexed content needs an access decision first.** Think about who may retrieve what before you index sensitive documents.
- **Retrieval can't fix a stale source.** If ingestion is behind, the index faithfully returns old facts.
- **Changing a DLO's data space filter doesn't update an existing search index.** The index keeps what it indexed under the old filter, even rows that no longer qualify.

## Gaps to close

- [ ] Re-read Vector Search, Retrieve Data and the search index type pages in full once the doc domains are reachable. This note was built from search extracts.
- [ ] Which out-of-the-box chunking strategies and embedding models are available at API 67.0, and what are their defaults?

## Hands-on

- [ ] **D360-RAG-01** · 30 min · Create a vector search index over a few Knowledge articles, then test its retriever with three questions. **Proves:** what comes back is chunks; read them before reading the answer.
- [ ] **D360-RAG-02** · 25 min · Rebuild the same corpus as a hybrid index and ask a question that hinges on an exact product code. **Proves:** lexical matching catches what similarity misses.
- [ ] **D360-RAG-03** · 20 min · Add an article whose key step spans a long table, then ask about that step. **Proves:** chunk boundaries decide what the agent sees.

## Related

- [Ingestion & Data Streams](ingestion-and-data-streams.md) — freshness of what gets indexed
- [Identity Resolution](identity-resolution.md) — real-time resolution feeds the data graphs structured grounding uses
- [Data 360 DevOps](data-360-devops.md) — Code Extension, the route to custom chunking
- [SF_Agentforce · Grounding a prompt template](../SF_Agentforce/grounding-a-prompt-template.md) — where a retriever plugs into a template
- [Interview · Grounding & retrieval](../Interview/01-agentforce/01-grounding-and-retrieval.md) — the structured-data-behind-semantic-search scenario

## Sources

- [Vector Search](https://help.salesforce.com/s/articleView?language=en_US&id=data.c360_a_search_index_vector_index.htm&type=5) — Salesforce Help · via search 2026-10-02 · chunk unstructured data in DMOs and UDMOs before embedding
- [Retrieve Data](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-02 · retrievers augment prompt templates with grounding
- [Use Search for AI, Automation, and Analytics](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_ground_ai.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-02 · hybrid search merges vector and keyword results
- [Data 360 Architecture](https://architect.salesforce.com/docs/architect/fundamentals/guide/data-360-architecture) — Salesforce Architects · via search 2026-10-02 · keyword, vector and hybrid indexing; chunking and embedding pipelines
- [Use Custom Functions in Data 360](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/use-custom-function.html) — Salesforce Developers · via search 2026-10-02 · a deployed function as the chunking strategy
- [Unstructured Data in Data Cloud](https://trailhead.salesforce.com/content/learn/projects/unstructured-data-in-data-cloud/get-started-with-unstructured-data-in-data-cloud) — Trailhead · via search 2026-10-02 · UDLO mapped to UDMO; blob-store files referenced, not imported
- [Data Graphs](https://help.salesforce.com/s/articleView?language=en_US&id=data.c360_a_data_graphs.htm&type=5) — Salesforce Help · via search 2026-10-02 · standard vs real-time data graphs; one JSON blob
- [Search Index Reference](https://help.salesforce.com/s/articleView?language=en_US&id=data.c360_a_search_index_reference.htm&type=5) — Salesforce Help · via search 2026-10-02 · a changed data space filter doesn't update the index

## History

- 2026-10-02 · created — facts carried over from the archived roadmap notes and confirmed against Salesforce search extracts
- 2026-10-02 · updated — UDLO/UDMO, standard vs real-time data graphs, and the data space filter gotcha, for the terminology flashcards
