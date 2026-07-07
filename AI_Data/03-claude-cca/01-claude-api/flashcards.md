# Claude API — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is tool use (function calling)?
A: The model requests a structured call to a tool you defined; your code executes it and returns the result for the model to continue with.

Q: What is structured output?
A: Constraining a model's response to a JSON schema so downstream code can parse it reliably.

Q: What is a JSON schema used for in the API?
A: A contract describing required fields, types, and constraints — used to define tools and validate structured output.

Q: What is a system prompt?
A: Instructions set before any user message that define the model's role, rules, and output expectations.

Q: What is extended thinking?
A: A mode where Claude reasons step-by-step in a visible scratchpad before its final answer — better on hard problems.
