# AI Theory Essentials — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is an embedding?
A: A numeric vector representing meaning; similar texts map to nearby vectors, enabling semantic comparison.

Q: What is a token, and roughly how big is one?
A: The unit models read and write — roughly ¾ of an English word. Context limits and API pricing are measured in tokens.

Q: What is a transformer?
A: The neural architecture behind modern LLMs, built on attention — the mechanism that weighs which parts of the input matter for each output token.

Q: What does attention actually do?
A: For each token, it scores how relevant every other token is and blends information accordingly.

Q: Fine-tuning vs RAG — when does each apply?
A: Fine-tuning retrains the model on domain data to shift behavior/style; RAG supplies knowledge at runtime via retrieval. Prefer RAG for knowledge, fine-tuning for behavior.

Q: What is temperature?
A: Sampling randomness: low = deterministic and repeatable, high = varied and creative.

Q: What is inference?
A: Running a trained model to produce output — what you pay for per token on every API call.

Q: What is few-shot prompting?
A: Steering a model with a handful of worked examples in the prompt instead of retraining it.

Q: What is a hallucination and what mitigates it?
A: Confident but false model output; mitigated by grounding/RAG, citations, and validation.

Q: What is a multi-agent system?
A: Multiple AI agents cooperating or competing to solve a task no single agent handles well — the theory behind orchestrator-worker designs.

Q: Why does embedding theory determine chunking strategy?
A: An embedding represents the meaning of the whole chunk in one vector. A chunk covering three topics produces a vector near none of them precisely, so retrieval degrades — the vector is the retrieval quality.

Q: Does semantic search return correct results?
A: It returns similar results. Similarity is a geometric property; correctness isn't. A confidently-retrieved wrong chunk yields a confident wrong answer.

Q: Why is prompt injection structural rather than a bug to be patched?
A: Because a model can't reliably distinguish instructions from data, so text hidden in a document, email or web page can be read as a command.

Q: Why is prompt injection more serious in agentic systems than in chatbots?
A: A hijacked chatbot says something wrong; a hijacked agent takes an action — and under multi-agent orchestration and MCP, possibly with no human watching.

Q: What is the right mental model for retrieved content?
A: Untrusted input. It is data, not instructions — even when it is phrased as instructions.

Q: Is temperature 0 fully deterministic?
A: Not in practice. Don't promise reproducibility you can't demonstrate.
