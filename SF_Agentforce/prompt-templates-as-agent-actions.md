---
vault: SF_Agentforce
format: light
level: working
status: complete
org_checks: 3
labs: 4
created: 2026-08-28
updated: 2026-08-30
---
# Prompt Templates as Agent Actions

**One line:** How a prompt template stops being something a user clicks and becomes something an agent decides to call.

**Reach for it when:** You have a working template and want an agent to use it in conversation.

## Key points

- **Flex is the type for this.** Its **5 declared inputs** of mixed types are what let an agent supply context that is not a record on screen.
- The wiring is two steps, in two places:

| Step | Where | What |
|---|---|---|
| 1 | Agent Assets → **New Agent Action** | Reference type **Prompt Template**, pick the template, write the instructions |
| 2 | Agent Builder → your **topic** → Actions | Add the action so the agent can reach it |

- **The instructions you write in step 1 are the specification, not documentation.** Atlas reads them to decide whether to call this action at all → [Atlas Reasoning Engine](atlas-reasoning-engine.md).
- **The agent must pass inputs in the format the template declares.** A mismatch is a runtime failure, not a build-time one.
- As metadata the action is a **`GenAiFunction`**: `invocationTargetType` = `generatePromptResponse`, `invocationTarget` = the template. The topic is a **`GenAiPlugin`**, and `pluginField` points back at it.
- **The action does not pin a version.** `GenAiFunction` has no version field at all — it names the template and gets whatever version is active → [Metadata & Deployment](prompt-template-metadata-and-deployment.md).
- **Billing is per action, not per conversation.** A standard action is **20 credits, about $0.10**, the same rate whether it runs Apex or a prompt template. A five-action resolution costs five times a demo's one.

## Gotchas

- **A vague action description is a bug.** It produces intermittent non-calling that looks like a model problem and is a specification problem.
- **The template must be activated first.** An inactive one is invisible here, exactly as it is to Flow and Apex → [Versions & Access](prompt-template-versions-and-access.md).
- **Activating a new version silently changes agent behaviour.** Because nothing is pinned, an edit meant for a Setup user reaches every agent calling the template. Check **Prompt Template References** — it lists the flows and agents depending on it — before you activate.

## Confirm in org

- 🚩 Can any type other than Flex be exposed as an agent action? No source confirms or denies it.
- 🚩 What does the agent see when the template returns an empty response — an error, or an empty string it narrates around?
- 🚩 Does the template's own LLM generation bill on top of the 20-credit action, or is it included? The credit table does not split them.

## Hands-on

- [ ] **AF-ACT-01** · 30 min · Wire a Flex template as an agent action and call it in conversation. **Proves:** the two-step wiring — the action first, then the topic.
- [ ] **AF-ACT-02** · 25 min · Write a deliberately vague action instruction, watch the agent fail to call it, then rewrite it as an API contract. **Proves:** the instruction is the specification, not documentation.
- [ ] **AF-ACT-03** · 20 min · Activate a new template version while an agent is using the action. **Proves:** nothing is pinned — agent behaviour changes with no change to the agent.
- [ ] **AF-ACT-04** · 15 min · Try to expose a non-Flex template as an agent action. **Settles:** whether any type but Flex works 🚩.

## Related

- [Flex Prompt Templates](flex-prompt-templates.md) — the type in full, and the three other callers an agent competes with
- [Prompt Template Types](prompt-template-types.md) — why Flex is the one that fits here
- [Prompt Template Versions & Access](prompt-template-versions-and-access.md) — activation, which gates this entirely
- [Prompt Template Metadata & Deployment](prompt-template-metadata-and-deployment.md) — the version this action resolves to, and how it travels
- [Atlas Reasoning Engine](atlas-reasoning-engine.md) — the caller that reads your instructions and decides
- [SF_core · 22 Invocable Apex & Agentforce actions](../SF_core/02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md) — the coded action, same description-as-contract rule
- [SF_core · 04-flow · 23 Flows as Agentforce actions](../SF_core/04-flow-and-automation/23-flows-as-agentforce-actions.md) — the declarative action, autolaunched only

## Sources

- [Exercise 5: Extend Agents with Prompt Template Actions](https://developer.salesforce.com/workshops/agentforce-workshop/agents/5-prompt-template-actions) — Salesforce Developers · read 2026-08-28 · the two-step wiring
- [GenAiFunction](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaifunction.htm) — Metadata API Developer Guide · read 2026-08-28 · the field list, and the absence of a version field
- [Flex Credits](../RELEASE-RADAR/pricing-and-certification.md) — RELEASE-RADAR · 2026-07-26 · 20 credits per standard action
- [Your Guide to Building a Flex Template for Agentforce](https://www.salesforceben.com/your-guide-to-building-a-flex-template-for-agentforce/) — third party 🚩 · via search 2026-08-28 · the 5-input figure

## History

- 2026-08-28 · created from the agent-action question left open by [Prompt Template Types](prompt-template-types.md)
- 2026-08-28 · added the `GenAiFunction` / `GenAiPlugin` shape, confirmed the action follows the active version rather than pinning one, and priced an action at 20 credits
- 2026-08-30 · linked to the new [Flex Prompt Templates](flex-prompt-templates.md) note, which now owns the type itself
