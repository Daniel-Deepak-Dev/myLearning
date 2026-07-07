# Einstein Trust Layer — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is the Einstein Trust Layer?
A: The security layer between Salesforce and LLM providers: data masking, secure retrieval, zero retention, toxicity scoring, and an audit trail.

Q: What is zero data retention?
A: Guarantee that model providers processing prompts via the Trust Layer don't store them or use them for training.

Q: How does data masking work?
A: PII in the prompt is replaced with placeholder tokens before it leaves Salesforce; real values are re-inserted into the response.

Q: Name the five Trust Layer capabilities worth reciting to a client.
A: Data masking, secure data retrieval, zero retention, toxicity scoring, audit trail.
