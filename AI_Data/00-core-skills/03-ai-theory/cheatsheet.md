# AI Theory Essentials — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Embeddings, attention, LLM prompting and multi-agent systems — the minimum theory that makes platform behaviour predictable instead of mysterious.

## Key terms
| Term | Definition |
|---|---|
| Embedding | A vector representing the meaning of a **whole chunk**. Similar texts land near each other. |
| Attention | For each token, score how relevant every other token is, then blend. |
| Prompt injection | Hidden instructions in data hijack an agent. **Structural, not a bug.** |
| Token | ~¾ of an English word. Context limits *and* pricing are measured in these. |

## Rules of thumb

- **Similarity ≠ correctness.** The most important sentence in this topic.
- An embedding averages the chunk's meaning → an oversized chunk retrieves badly. That one insight drives most retrieval tuning.
- **Hallucination is fixed by grounding, not fine-tuning.** Fine-tuning changes behaviour; RAG changes knowledge.
- **Treat retrieved content as untrusted input** — data, not instructions, even when phrased as instructions.

## Exam traps / common confusions

- Fine-tuning does **not** fix factual errors about your data.
- Temperature 0 isn't fully deterministic in practice — don't promise reproducibility.
- Token counts ≠ word counts, and differ by tokenizer.
- A hijacked chatbot says something wrong; a hijacked **agent takes an action** — possibly unwatched.

## Minimal example

Why chunk size is an embeddings problem, not a formatting one:

```
chunk covering 3 topics  → one vector, near none of them precisely
chunk too small          → "it" has no referent
split mid-procedure      → 2 chunks, neither answers the question

⇒ the vector IS the retrieval quality
```
