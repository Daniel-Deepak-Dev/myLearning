# Agentic Architecture & Orchestration — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is the agentic loop?
A: Reason → act (call a tool) → observe the result → repeat until the goal is met.

Q: What is the orchestrator-worker pattern?
A: A lead agent decomposes a task, delegates slices to specialized subagents, then synthesizes their results.

Q: What is a subagent, and why give it a separate context window?
A: A worker agent running in its own context, handling a delegated task without polluting the lead agent's context.

Q: When should you NOT delegate to subagents?
A: When the task fits one context window, when workers would need shared state they can't see, or when coordination overhead exceeds the benefit.
