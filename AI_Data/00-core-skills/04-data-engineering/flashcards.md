# Data Engineering & Pipeline Patterns — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: ETL vs ELT?
A: Transform before loading (ETL) vs load raw then transform inside the warehouse (ELT — the modern default).

Q: What makes a pipeline idempotent, and why does it matter?
A: Re-running it produces the same result — essential for safe retries after failures.

Q: What is data lineage?
A: Tracking where data came from and how it was transformed — key for trust, debugging, and compliance.

Q: What is a semantic layer?
A: A governed layer of business definitions (what counts as "revenue") sitting between raw data and consumers, human or AI.
