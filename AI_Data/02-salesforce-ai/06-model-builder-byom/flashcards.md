# Model Builder & BYOM — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is Model Builder?
A: Tool to register and configure LLMs — Salesforce-hosted or bring-your-own via Bedrock/Vertex — for use across Prompt Builder and Agentforce.

Q: What is BYOM?
A: Bring Your Own Model: connecting an external foundation model (e.g. Claude on Amazon Bedrock) so Salesforce features call it through your own endpoint.

Q: How would you use Claude inside Salesforce today?
A: Register Claude via Amazon Bedrock in Model Builder, then reference it from Prompt Builder templates and agents — with the Trust Layer in between.
