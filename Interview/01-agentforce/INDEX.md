# 01 · Agentforce

Scenario questions on agents in production — where they fail, why the failure looks like something else, and what a client's security team and CFO actually ask. Source knowledge: [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md).

> ⚠️ **Every answer here assumes Agent Script.** The *New Agent* button stopped opening the topic-and-instruction builder the week of **July 13, 2026**. An answer that walks an interviewer through topics and instructions as the current authoring model is describing a retired product — and most online prep material still does.

| Set | Scenarios it drills | Level |
|---|---|---|
| [01 · Grounding & retrieval](01-grounding-and-retrieval.md) | Data graph vs vector search for structured data · the `status`/`retrieverId` race 🆕 · when RAG structurally cannot answer · triaging "it hallucinates" on a client call | medium → complex |
| [02 · Actions & orchestration](02-actions-and-orchestration.md) | Non-idempotent actions under a retrying agent · the API 67.0 breaking changes ⚠️ · intermittent mis-routing as a specification bug 🆕 · reusing Apex REST and `@AuraEnabled` as actions 🆕 | medium → complex |
| [03 · Trust, testing & lifecycle](03-trust-testing-and-lifecycle.md) | Masking vs answer quality, and what BYOM really moves · answering "you can't test it" 🆕 · stored prompt injection through a case field · buy vs build against Help Agent | medium → complex |

**12 scenarios.** The recurring shape: three of these are data or specification failures that present as model failures. If an answer reaches for a bigger model, it is usually wrong.

## The four highest-value things to be able to say

1. **Descriptions are executable configuration.** The reasoning engine never reads your Apex — it reads the action and subagent descriptions. Mis-selection and mis-routing are specification bugs, and debugging starts there.
2. **Stale grounding is the #1 root cause of "the agent was wrong."** It is misdiagnosed as a model problem almost every time. The signature is fluent, specific and obsolete.
3. **The Trust Layer governs the model interaction, not the agent's scope.** It does not stop a badly-scoped action, and it does not fix an over-permissioned running user.
4. **Agent behaviour is testable as of Summer '26** — five layers, two of them new. Being able to name what each layer catches, *and* where it falls short, is the architect-level differentiator.

## Related

- [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md) — the source notes every answer links into
- [AI_Data/02-salesforce-ai/_labs/](../../AI_Data/02-salesforce-ai/_labs/README.md) — the lab ladder. A scenario you have *run* answers differently from one you have read
- [_cert-agentforce-specialist/](../../AI_Data/02-salesforce-ai/_cert-agentforce-specialist/exam-guide.md) — exam prep, a different exercise: certification tests recall, these test reasoning
- [04-cross-domain/](../04-cross-domain/INDEX.md) — where these collide with Data 360 and the core platform
