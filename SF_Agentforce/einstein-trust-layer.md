---
vault: SF_Agentforce
format: light
level: basic
status: complete
org_checks: 1
labs: 4
created: 2026-08-27
updated: 2026-08-28
---
# Einstein Trust Layer

**One line:** The security layer between Salesforce and the LLM provider. Every Agentforce and Prompt Builder call passes through it.

**Reach for it when:** Someone asks "is our data safe if we send it to an LLM?"

## Key points

- It is **not one feature**. It is a set of guardrails — some run on the way out, some on the way back.
- **Outbound:** secure data retrieval → data masking → prompt-injection defence. **Inbound:** demasking → toxicity scoring → zero retention → audit trail.
- **Masking** swaps PII for a placeholder before the prompt leaves Salesforce, and swaps it back on the way in. The placeholder is **type plus a counter** — the first name detected becomes `PERSON_0`, the next `PERSON_1`.
- **Masked by default: Name, Email Address, Phone Number, Credit Card, US SSN.** Each entity type toggles independently.
- **It can be switched off.** Setup → Einstein Setup → **Einstein Trust Layer** holds the master masking toggle and the per-entity table.
- **Zero retention** is a separate promise: the provider stores nothing and trains on nothing.
- **Secure data retrieval** fetches grounding data as the running user, so the model only sees what that user could see.
- **Toxicity detection** scores five categories — violence, sexual, profanity, hate, physical — into one **0–1** score.
- **The audit trail lands in Data 360**, as DMOs: `GenAIGatewayRequest__dlm`, `GenAIGatewayResponse__dlm`, `GenAIContentQuality__dlm`, `GenAIFeedback__dlm`.

> **From my notes.** *"a salesforce based security which prevent LLM from learning ORG data or company information by masking."* — half right, and the wrong half matters. **Masking stops PII leaving.** **Zero retention is what stops the model learning from your data.** Two separate mechanisms; only one is masking.

## Gotchas

- **Masking and zero retention are different promises.** Merging them is the most common Trust Layer mistake.
- **Toxicity scoring does not block.** The score is returned *alongside* the response — acting on it is the calling app's job, not the platform's.
- **Turning masking on caps the context window at 65,536 tokens.** That is the price of the safety.
- **Detection is pattern-based and validates format**, so a credit card number failing its checksum is not masked — and the model never sees the real value of one that is.
- **Grounding runs as the running user.** A permissions gap becomes a quietly wrong AI answer, not an error.

## Confirm in org

- 🚩 How long audit data is kept in Data 360. No retention period is stated on any page reachable here.

## Hands-on

- [ ] **AF-TRUST-01** · 25 min · Run a template on a Contact, then read `GenAIGatewayRequest__dlm`. **Proves:** the model saw `PERSON_0`, not the name. **Needs:** Data 360.
- [ ] **AF-TRUST-02** · 15 min · Turn masking off for one entity type only, re-run, re-read the request. **Proves:** the toggle really is per entity. **Needs:** Data 360.
- [ ] **AF-TRUST-03** · 20 min · Push a masked prompt past 65,536 tokens. **Proves:** the *"Prompt size exceeds the token limit when PII is enabled"* error — copy it verbatim.
- [ ] **AF-TRUST-04** · 20 min · Query the audit DMOs for the oldest record still present. **Settles:** how long audit data is kept 🚩. **Needs:** Data 360.

## Related

- [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md) — every template call passes through this layer
- [Atlas Reasoning Engine](atlas-reasoning-engine.md) — the layer this one wraps
- [Grounding a Prompt Template](grounding-a-prompt-template.md) — what gets assembled *before* this layer sees it, and why masking can push it over a ceiling
- [SF_core · 31 Apex-grounded prompt templates](../SF_core/02-apex-and-triggers/31-apex-grounded-prompt-templates.md) — where Apex-supplied text becomes an injection surface

## Sources

- [Configure LLM Data Masking Policies](https://trailhead.salesforce.com/content/learn/modules/llm-data-masking-in-the-einstein-trust-layer/configure-llm-data-masking-policies) — Trailhead · read 2026-08-28 · default entities, per-entity toggle, Setup path
- [Data Masking — Agentforce Developer Guide](https://developer.salesforce.com/docs/ai/agentforce/guide/models-api-data-masking.html) — Salesforce Developers · read 2026-08-28 · masking is optional; the 65,536-token cap
- [Follow the Response Journey](https://trailhead.salesforce.com/content/learn/modules/the-einstein-trust-layer/follow-the-response-journey) — Trailhead · read 2026-08-28 · toxicity is scored, not blocked
- [The Einstein Audit and Feedback Data Model in Data Cloud](https://developer.salesforce.com/blogs/2024/07/the-einstein-audit-and-feedback-data-model-in-data-cloud) — Salesforce Developers · read 2026-08-28 · the DMO names

## History

- 2026-08-27 · created from your Day-3 terms note · corrected the masking-vs-zero-retention claim
- 2026-08-28 · masking made concrete — default entities, per-entity toggle, `PERSON_0` token shape, 65,536-token cap, checksum validation; toxicity confirmed advisory, not blocking; audit trail located in Data 360 DMOs
