# Prompt Engineering & Structured Output — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What are evals?
A: Systematic tests that score prompt or agent output against defined criteria — improving AI systems on evidence instead of vibes.

Q: Why explicit criteria over vague instructions?
A: Models follow concrete, checkable rules far more reliably; vague adjectives ("be concise", "be helpful") drift.

Q: What is a validation loop?
A: Generate → validate the output against a schema or criteria → feed errors back → regenerate until it passes.

Q: What is prompt injection?
A: An attack where malicious instructions hidden in data (an email, a web page) hijack an agent — a core security concern in tool-using systems.
