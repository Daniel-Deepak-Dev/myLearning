# 00 · Core Skills

Vendor-neutral foundations everything else stands on. Roadmap tag: **Core** (slate).

> Kept deliberately vendor-neutral — but each topic notes the one place Summer '26 made it directly relevant to Salesforce work.

| Topic | What it covers | Quick recall |
|---|---|---|
| [SQL Fluency](01-sql/notes.md) | Joins, CTEs, window functions, aggregation — and **SQL from Apex** against Data 360, new in Summer '26 | [cheatsheet](01-sql/cheatsheet.md) · [flashcards](01-sql/flashcards.md) |
| [Python for Data Work](02-python-for-data/notes.md) | pandas, JSON, REST — and **Code Extension**, which made Python a first-class Data 360 runtime | [cheatsheet](02-python-for-data/cheatsheet.md) · [flashcards](02-python-for-data/flashcards.md) |
| [AI Theory Essentials](03-ai-theory/notes.md) | Embeddings, transformers, LLMs & prompting, multi-agent systems (AI-For-Beginners L14/18/20/23) — plus prompt injection | [cheatsheet](03-ai-theory/cheatsheet.md) · [flashcards](03-ai-theory/flashcards.md) |
| [Data Engineering & Pipeline Patterns](04-data-engineering/notes.md) | ETL vs ELT, orchestration, idempotency, data quality — and why agents made **freshness a correctness property** | [cheatsheet](04-data-engineering/cheatsheet.md) · [flashcards](04-data-engineering/flashcards.md) |

## The four ideas that pay off most downstream

1. **Window functions** → calculated insights are built from them.
2. **Embeddings average a whole chunk** → this is *why* chunking dominates retrieval quality.
3. **Idempotency** → agents retry after timeouts, so every agent-triggered write needs it.
4. **Hallucination is fixed by grounding, not fine-tuning** → the most common client misconception.
