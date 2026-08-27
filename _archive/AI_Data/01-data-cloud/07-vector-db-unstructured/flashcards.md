# Vector Database & Unstructured Data — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is a search index in Data 360?
A: Unstructured content (PDFs, transcripts, knowledge) that Data 360 has chunked and embedded so it's semantically searchable.

Q: What is Data 360's vector database?
A: The built-in store of embeddings for unstructured content, powering semantic search and grounded AI answers.

Q: What is chunking and why does it matter?
A: Splitting documents into pieces before embedding. Chunk size, overlap and structure awareness strongly affect retrieval quality — it is usually the single biggest lever on whether RAG works.

Q: What is semantic search?
A: Retrieval by meaning using embedding similarity rather than keyword matching.

Q: Search index vs retriever — what's the difference?
A: The search index is the indexed corpus. The retriever is the configured query against it. They are not interchangeable.

Q: What changed about chunking in Summer '26?
A: Code Extension lets you deploy custom Python scripts implementing custom chunking logic on search index creation. Chunking stopped being a black box.

Q: Name five chunking failure modes.
A: Chunks too large (dilute the embedding, burn tokens); too small (lose context); split mid-procedure (agent answers with half a process); no overlap (misses answers straddling a boundary); ignoring structure (table rows separated from headers).

Q: In what order should you tune retrieval?
A: Chunking → overlap → structure awareness → top-N returned → retriever filters. Everything downstream inherits chunking, and re-indexing after a chunking change is expensive.

Q: What is Intelligent Context, and what is distinctive about it?
A: Low-code automatic extraction of unstructured content (PDFs, tables, images, flowcharts) into grounding data. Distinctively, the same document can be configured to be interpreted from multiple business perspectives.

Q: What is the status of Context Indexing as of 2026-07-28?
A: Open. It was reported in June 2026 as expected to reach GA "later in July 2026", but no confirmation was found — re-check the monthly Data 360 release notes before stating it as GA.

Q: What is the permission split around Code Extension?
A: Developers author the code; users with the Data Cloud Architect permission set run and monitor it. Author is not operator.

Q: Does semantic search return correct results?
A: It returns *similar* results. A confidently-retrieved wrong chunk still produces a wrong answer — similarity is not correctness.

Q: Why is top-N a cost decision, not just a quality one?
A: Every retrieved chunk is tokens in the prompt, and Agentforce bills per action.
