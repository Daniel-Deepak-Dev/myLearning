# RAG on Platform — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is RAG?
A: Retrieval-Augmented Generation: retrieve relevant content, inject it into the prompt, and generate an answer grounded in it — the antidote to hallucination.

Q: What is a retriever, in Salesforce terms?
A: A configured query against a search index or data graph that fetches the most relevant content to ground a prompt — Salesforce's RAG building block.

Q: What is a data graph?
A: A precomputed, denormalized view of related data around a profile, built for millisecond real-time reads by agents and personalization.

Q: What is an Agentforce Data Library?
A: A managed grounding store that indexes Knowledge articles or uploaded files into a vector index and exposes a retriever for RAG.

Q: When should you use a data graph rather than vector search?
A: For structured profile data — "what do we know about this customer". A data graph is precomputed, denormalized, millisecond-fast and exact. Vector search is for unstructured content where you don't know which document holds the answer.

Q: What are the five steps of ADL Connect API provisioning?
A: POST to create the library (returns libraryId) → poll upload-readiness → request a pre-signed S3 URL and PUT the file → POST to indexing → wire the library into the agent's knowledge: block and invoke AnswerQuestionsWithKnowledge.

Q: When is an Agentforce Data Library actually ready to use?
A: When retrieverId goes non-null — NOT when the top-level status flips. Status leads the retriever by 10 to 30 minutes, so polling on status gives you a library that reports ready and then fails to retrieve.

Q: What is the value of rag_feature_config_id?
A: "ARFPC_" + libraryId — not the raw library ID.

Q: What causes a 403 when uploading a file to an Agentforce Data Library?
A: Not forwarding the headers returned with the pre-signed S3 URL verbatim.

Q: Where does sourceType live in the create-library request?
A: Nested under groundingSource — SFDRIVE for files, or KNOWLEDGE / RETRIEVER. Not at the top level.

Q: Why does the ADL Connect API matter architecturally?
A: It is the "grounding as code" half of Headless 360 — RAG configuration stops being click-ops and becomes a scriptable, CI/CD-ready pipeline step.

Q: In what order should you tune RAG quality?
A: Chunking, then choosing the right source (graph vs vector), then top-N, then retriever filters, then citations.

Q: Does a citation mean the answer is correct?
A: No. An agent can cite a chunk it misread. Citations make errors findable, which is most of their value — but cited is not correct.

Q: An agent grounded on a Data Library returns outdated facts. Is that a RAG problem?
A: Not necessarily — grounding can't fix a stale source. If ingestion is behind, retrieval faithfully returns old facts.
