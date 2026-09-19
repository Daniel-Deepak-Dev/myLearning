# Einstein Trust Layer

> Folder: SF_Agentforce · Level: basic · Status: 🌱 4 gaps open
> Created: 2026-08-27 · Updated: 2026-08-27

**One line:** The security layer between Salesforce and the LLM provider. Every Agentforce and Prompt Builder call passes through it.

**Reach for it when:** Someone asks "is our data safe if we send it to an LLM?"

## Key points

- It is **not one feature**. It is a set of guardrails — some run on the way out, some on the way back.
- **Outbound:** secure data retrieval → data masking → prompt-injection defence.
- **Inbound:** demasking → toxicity scoring → zero retention → audit trail.
- **Masking** swaps PII for placeholder tokens before the prompt leaves Salesforce. Demasking swaps them back on the way in.
- **Zero retention** is a separate promise: the provider stores nothing and trains on nothing.
- **Secure data retrieval** fetches grounding data as the running user, so the model only sees what that user could see.
- **Toxicity detection** scores five categories: violence, sexual, profanity, hate, physical.
- **Audit trail** logs the prompt, the safety scores and the raw model output, with timestamps.

> **From my notes.** *"a salesforce based security which prevent LLM from learning ORG data or company information by masking."* — half right, and the wrong half matters. **Masking stops PII leaving.** **Zero retention is what stops the model learning from your data.** Two separate mechanisms; only one is masking.

## Gotchas

- **Masking and zero retention are different promises.** Merging them is the most common Trust Layer mistake.
- **The model never sees the real masked value**, so it cannot reason about it either.
- **Grounding runs as the running user.** A permissions gap becomes a quietly wrong AI answer, not an error.

## Gaps to close

- [ ] Which PII types actually get masked, and is that list configurable?
- [ ] Can any part of the Trust Layer be switched off, or is it always on?
- [ ] Where does the audit trail live, and how long is it kept?
- [ ] When toxicity detection flags a response — is it blocked, or flagged and still delivered?

## Related

- [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md) — every template call passes through this layer
- [Atlas Reasoning Engine](atlas-reasoning-engine.md) — the layer this one wraps
- [SF_core · 31 Apex-grounded prompt templates](../SF_core/02-apex-and-triggers/31-apex-grounded-prompt-templates.md) — where Apex-supplied text becomes an injection surface

## Sources

- [Einstein Trust Layer: Designed for Trust](https://help.salesforce.com/s/articleView?id=ai.generative_ai_trust_arch.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-27 — page is JS-rendered, open it to verify
- [Trust Layer — Agentforce Developer Guide](https://developer.salesforce.com/docs/einstein/genai/guide/trust.html) — Salesforce Developers · via search 2026-08-27 — page is JS-rendered, open it to verify
- [Meet the Einstein Trust Layer](https://trailhead.salesforce.com/content/learn/modules/the-einstein-trust-layer/meet-the-einstein-trust-layer) — Trailhead · via search 2026-08-27 — page is JS-rendered, open it to verify

## History

- 2026-08-27 · created from your Day-3 terms note · corrected the masking-vs-zero-retention claim
