# Prompt Templates as Agent Actions

> Folder: SF_Agentforce · Level: working · Status: 🌱 4 gaps open
> Created: 2026-08-28 · Updated: 2026-08-28

**One line:** How a prompt template stops being something a user clicks and becomes something an agent decides to call.

**Reach for it when:** You have a working template and want an agent to use it in conversation.

## Key points

- **Flex is the type for this.** Its **5 declared inputs** of mixed types are what let an agent supply context that is not a record on screen. 🚩 No source confirms whether the other five types can be exposed → [Grounding a Prompt Template](grounding-a-prompt-template.md).
- The wiring is two steps, in two places:

| Step | Where | What |
|---|---|---|
| 1 | Agent Assets → **New Agent Action** | Reference type **Prompt Template**, pick the template, write the instructions |
| 2 | Agent Builder → your **topic** → Actions | Add the action so the agent can reach it |

- **The instructions you write in step 1 are the specification, not documentation.** Atlas reads them to decide whether to call this action at all → [Atlas Reasoning Engine](atlas-reasoning-engine.md).
- **The agent must pass inputs in the format the template declares.** A mismatch is a runtime failure, not a build-time one.

## Gotchas

- **A vague action description is a bug.** It produces intermittent non-calling that looks like a model problem and is a specification problem.
- **The template must be activated first.** An inactive one is invisible here, exactly as it is to Flow and Apex → [Versions & Access](prompt-template-versions-and-access.md).

## Gaps to close

- [ ] 🚩 Can any type other than Flex be exposed as an agent action?
- [ ] Does the action pin a template **version**, or always follow the active one?
- [ ] What does the agent see when the template returns an empty response?
- [ ] How does a prompt-template action compare to an Apex one on credit cost and latency?

## Related

- [Prompt Template Types](prompt-template-types.md) — why Flex is the one that fits here
- [Prompt Template Versions & Access](prompt-template-versions-and-access.md) — activation, which gates this entirely
- [Atlas Reasoning Engine](atlas-reasoning-engine.md) — the caller that reads your instructions and decides
- [SF_core · 22 Invocable Apex & Agentforce actions](../SF_core/02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md) — the coded action, same description-as-contract rule
- [SF_core · 04-flow · 23 Flows as Agentforce actions](../SF_core/04-flow-and-automation/23-flows-as-agentforce-actions.md) — the declarative action, autolaunched only

## Sources

- [Exercise 5: Extend Agents with Prompt Template Actions](https://developer.salesforce.com/workshops/agentforce-workshop/agents/5-prompt-template-actions) — Salesforce Developers · read 2026-08-28 · the two-step wiring
- [Your Guide to Building a Flex Template for Agentforce](https://www.salesforceben.com/your-guide-to-building-a-flex-template-for-agentforce/) — third party 🚩 · via search 2026-08-28 · the 5-input figure

## History

- 2026-08-28 · created from the agent-action question left open by [Prompt Template Types](prompt-template-types.md)
