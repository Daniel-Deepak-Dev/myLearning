# Model Builder & BYOM — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is Model Builder?
A: Tool to register and configure LLMs — Salesforce-hosted or bring-your-own via Bedrock/Vertex — for use across Prompt Builder and Agentforce.

Q: What is BYOM?
A: Bring Your Own Model: connecting an external foundation model (e.g. Claude on Amazon Bedrock) so Salesforce features call it through your own endpoint and your own provider contract.

Q: How would you use Claude inside Salesforce today?
A: Claude on Amazon Bedrock is supported first-party by the Atlas Reasoning Engine, so select it directly — with the Trust Layer in between. Build a BYOM integration only if you need your own endpoint for contract, residency or fine-tuning reasons.

Q: Which model providers does the Atlas Reasoning Engine support?
A: Anthropic (Claude on Amazon Bedrock), OpenAI, and Google Gemini.

Q: At what three levels can the model be selected?
A: Org default in Setup, per agent (pinned inside its Agent Script), and per prompt template in Prompt Builder.

Q: What changed about model choice when Agent Script arrived?
A: It moved from effectively one org-wide setting to a per-agent decision with real cost and latency consequences — a genuine architecture lever.

Q: Name four reasons that genuinely justify BYOM.
A: An existing enterprise agreement or negotiated rate, data-residency requirements, a fine-tuned or domain-specific model you already run, and a regulatory need for your own provider contract and audit path.

Q: What is the key Trust Layer caveat with BYOM?
A: Verify which protections still apply end-to-end. Zero retention in particular then depends on your contract with your provider, not Salesforce's — do not assume the guarantee transfers.

Q: Which step of a BYOM setup usually consumes the time?
A: Request/response payload mapping. Provider API shapes differ, and mismatches surface as runtime errors rather than validation failures.

Q: Two paths using the "same" prompt behave differently. What do you check first?
A: Which model each actually used — org default, agent pin, and template setting can all differ.

Q: An agent invents facts about a customer. Is a better model or fine-tuning the fix?
A: Neither. That is a grounding and retrieval problem — fix it with retrievers and Data Libraries, not by changing or fine-tuning the model.
