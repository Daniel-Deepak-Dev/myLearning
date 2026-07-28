# Capstone: RAG Assistant over CRM Data — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What should you build before writing any code on this project?
A: A fixed evaluation set of 20–30 real questions with known-correct answers. Without a baseline you can't tell whether a change helped, and you end up tuning on vibes.

Q: What changed about this project's approach in Summer '26?
A: Don't hand-roll retrieval. Agentforce Data Libraries plus the ADL Connect API give a managed, scriptable RAG pipeline, and Code Extension exposes the chunking logic that actually determines quality.

Q: Rank the levers on RAG answer quality.
A: Chunking, then source choice (data graph vs vector search), then data freshness, then top-N, then prompt wording last.

Q: Why does chunking dominate retrieval quality?
A: Retrieval returns chunks, not documents. A chunk that splits a procedure yields half an answer, delivered confidently.

Q: What is the demonstrable claim this project should produce?
A: "I improved answer accuracy from X to Y by changing chunking strategy, measured against a fixed question set" — with real numbers behind it.

Q: When is an Agentforce Data Library ready to use?
A: When retrieverId goes non-null — not when the top-level status flips. Status leads by 10 to 30 minutes.

Q: What is rag_feature_config_id?
A: "ARFPC_" + libraryId, not the raw library ID.

Q: What causes a 403 when uploading a file during ADL provisioning?
A: Not forwarding the headers returned with the pre-signed S3 URL verbatim.

Q: What are the two legitimate designs for where Claude sits in this project?
A: In-platform — the agent runs on Agentforce grounded by the Data Library with Claude as the selected model, Trust Layer throughout. Or external — Claude reaches the org through a hosted MCP server and calls a retriever, in which case check what Trust Layer coverage still applies.

Q: How should this project be scoped?
A: Narrowly. "Answers support questions about a specific product line, citing the runbook section used" is a project; "answers questions about customers" is not. Narrow scope is what makes evaluation possible.

Q: Does a citation prove the answer is right?
A: No — an agent can cite a chunk it misread. Verifying that citations actually support the claim is itself a good thing to demonstrate.

Q: Should you split chunks by length or by structure?
A: By structure — headings, procedure steps, table boundaries. That is what custom chunking via Code Extension is for.
