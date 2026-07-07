# Context Management & Reliability — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is the context window?
A: The maximum tokens a model can consider at once — the hard budget every agent design must manage.

Q: What is prompt caching?
A: Reusing a cached prompt prefix (system prompt, documents, tools) across calls to cut latency and cost dramatically.

Q: What is compaction?
A: Summarizing earlier conversation/tool history to reclaim context window space in long-running agent sessions.
