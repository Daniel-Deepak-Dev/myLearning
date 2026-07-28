# AI Theory Essentials

> Track: Core skills · Roadmap: Phase 01 · Weeks 1–4 · Status: 🌱 learning
> Vendor-neutral by design. Platform application lives in [01-data-cloud/](../../01-data-cloud/INDEX.md) and [02-salesforce-ai/](../../02-salesforce-ai/INDEX.md).

**Roadmap scope:** From Microsoft's AI-For-Beginners repo, only lessons 14 (embeddings), 18 (transformers), 20 (LLMs & prompt programming), and 23 (multi-agent systems). Skip CNN/GAN/vision — below your critical path.

## What is it?

The minimum theory that makes platform behaviour *predictable* rather than mysterious. Four ideas:

| Idea | The one-line version |
|---|---|
| **Embeddings** | Text → a vector of meaning. Similar texts land near each other. |
| **Transformers & attention** | For each token, score how relevant every other token is, and blend accordingly. |
| **LLMs & prompting** | Next-token prediction at scale, steerable by context and examples. |
| **Multi-agent systems** | Several agents cooperating on what one can't do well. |

## Why it matters (for the AI-Salesforce architect role)

**Theory earns its place when it changes a decision.** Four places it does:

1. **Embeddings → chunking.** If you understand that an embedding averages the meaning of everything in the chunk, it's obvious why an oversized chunk retrieves badly: the vector is a blur of several topics. That single insight drives most retrieval tuning.
2. **Tokens → cost and context.** Context limits and pricing are both measured in tokens. Grounding decisions are token decisions, and Agentforce bills per action on top.
3. **Hallucination → grounding, not fine-tuning.** Knowing that a model predicts plausible continuations explains why RAG fixes factual errors and fine-tuning doesn't. This is the single most common client misconception.
4. **Multi-agent theory → orchestration.** Orchestrator-worker is the pattern behind both Claude subagents and Agentforce Multi-Agent Orchestration. Learn it once, apply it twice.

## How it works

### Embeddings and why chunking follows from them

An embedding represents the meaning of a **whole chunk** in one vector. Consequences:

- A chunk covering three topics produces a vector near none of them precisely — retrieval degrades
- A chunk too small loses the context that gave it meaning ("it" with no referent)
- Splitting mid-procedure produces two chunks, neither of which answers the question

**Semantic search returns *similar*, not *correct*.** Similarity is a geometric property; correctness isn't. A confidently-retrieved wrong chunk yields a confident wrong answer.

Platform application: [vector DB & unstructured](../../01-data-cloud/07-vector-db-unstructured/notes.md), where custom chunking via Code Extension is how you act on this.

### Prompt injection — the security-relevant one

Because a model can't reliably distinguish *instructions* from *data*, text hidden in a document, email or web page can hijack an agent. This isn't an implementation bug to be patched; it's structural to how LLMs read input.

**Why it matters more in agentic systems than in chatbots:** a chatbot that gets hijacked says something wrong. An agent that gets hijacked *takes an action* — and under multi-agent orchestration and MCP, possibly with no human watching.

Mitigations, layered:

| Layer | Mitigation |
|---|---|
| Platform | Einstein Trust Layer prompt-injection defence |
| Access | Least-privilege running user (user mode at API 67.0) |
| Design | Narrow action scope; no destructive action without confirmation |
| Content | Treat all retrieved content as untrusted input |

That last row is the mental model worth keeping: **retrieved content is data, not instructions** — even when it's phrased as instructions.

### Fine-tuning vs RAG

| | Fine-tuning | RAG |
|---|---|---|
| Changes | Behaviour, style, format | Knowledge available at answer time |
| Cost of update | Retrain | Re-index |
| Fixes hallucination? | **No** | **Yes**, when retrieval is good |

If the agent invents facts about a customer, that's retrieval. Nobody fine-tunes their way out of a grounding problem.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] AI-For-Beginners lessons 14, 18, 20, 23.
- [ ] Embed twenty sentences and inspect which pairs land closest. Intuition for "similar ≠ correct" comes fastest from seeing it.
- [ ] Compare retrieval quality at three chunk sizes on the same corpus — the applied version of lesson 14.
- [ ] Try a prompt-injection string against a test agent and watch the Trust Layer block it.

## Gotchas & sharp edges

- **Similarity ≠ correctness.** The most important sentence in this topic.
- **Fine-tuning doesn't fix hallucination.** Grounding does.
- **Temperature 0 isn't fully deterministic** in practice — don't promise reproducibility you can't demonstrate.
- **Token counts aren't word counts** (~¾ of a word), and they differ by tokenizer.
- **Prompt injection is structural**, not a bug awaiting a patch. Design around it.
- **Retrieved content is untrusted input.** Treat a document that says "ignore previous instructions" as data.
- **Don't over-invest here.** Four lessons is genuinely the right depth for this roadmap; the leverage is in applying them.

## Related topics

- [Vector DB & unstructured](../../01-data-cloud/07-vector-db-unstructured/notes.md) — embeddings and chunking, applied
- [RAG on platform](../../01-data-cloud/08-rag-on-platform/notes.md) — retrieval, applied
- [Einstein Trust Layer](../../02-salesforce-ai/04-einstein-trust-layer/notes.md) — injection defence
- [Multi-agent orchestration](../../02-salesforce-ai/08-multi-agent-orchestration/notes.md) — lesson 23, applied
- [Agentic architecture (Claude track)](../../03-claude-cca/02-agentic-architecture/notes.md)
