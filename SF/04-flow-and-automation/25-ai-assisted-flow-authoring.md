# AI-Assisted Flow Authoring

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** Agentforce for Flow — generating, editing and describing flows in natural language, and what to check before trusting the result. Diagnosing a broken flow with AI is [15](15-flow-testing-and-debugging.md).

## Core idea

"Describe your flow and Salesforce builds it" is one headline covering three separate capabilities, and they carry different amounts of risk. **Flow generation** turns a prompt into a structured draft of a record-triggered, scheduled, screen or autolaunched flow — the highest-leverage and the least trustworthy, because a plausible flow and a correct flow look identical on a canvas. **Natural-language editing** changes an *existing* screen flow from the Agentforce panel: add a component, remove a step, modify an action, without hand-editing the logic. **Flow summarisation** reads a finished flow and writes a description of it, then pushes that text into the flow's description metadata in one click. The last one is the quiet winner. It attacks the documentation deficit that makes every other governance problem worse, and it costs nothing to be wrong about — unlike a generated flow, which costs a data-quality incident.

## How it works

| Capability | What it does | Status |
|---|---|---|
| **Flow Generation V2** | prompt → structured draft flow | **GA** |
| **Natural-language screen flow editing** | add / remove / modify screen and action elements | **GA — Summer '26** |
| **Flow summarisation ("Describe")** | canvas → description, written to flow metadata | GA |
| **Troubleshoot Flow Errors** | diagnoses design-time and runtime failures, can apply a fix | **Beta** → [15](15-flow-testing-and-debugging.md) |

- **All of it requires Einstein generative AI and Agentforce provisioning.** Being on 67.0 does not mean you have it.
- **Generation is a draft, not a build.** It produces elements and connectors; it does not produce a design decision.
- **Review the trigger type first.** A generated record-triggered flow is usually *after-save*, and a field update on the triggering record belongs *before-save*. → [03](03-record-triggered-flows.md)
- **Generated flows rarely have fault paths**, and a flow with no fault path fails to an email nobody reads. → [10](10-fault-paths-and-custom-errors.md)
- **A generated description is prose, not a specification** — which matters specifically for an autolaunched flow exposed as an agent action, where the description *is* the contract another model reads. → [23](23-flows-as-agentforce-actions.md)

## 2026 currency

This surface arrived quickly and is still moving: generation matured through Winter '26 and Spring '26, and **Summer '26 extended natural-language editing to screen flows**, which had been the gap — you could generate a screen flow but not iterate on one conversationally. Salesforce's own engineering write-up on building the feature is worth reading for the framing rather than the numbers: the win it claims is authoring *time*, and nothing in it claims correctness. That is the right way to hold the whole category. The practical case where it genuinely changes a project's economics is post-migration consolidation — a pile of one-to-one converted Workflow Rules is exactly the tedious, well-specified, low-ambiguity editing this is good at. → [18](18-migrate-to-flow-and-legacy-retirement.md), [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md)

## Gotchas

- **A plausible flow and a correct flow look the same.** Reviewing generated output is the job, not a formality.
- **Check before-save versus after-save every time.** This is the most common and most expensive generated-flow mistake. → [13](13-flow-limits-and-bulkification.md)
- **Generators do not think about bulk.** A Get or Update inside a loop is idiomatic-looking and wrong at 200 records.
- **Fault paths are almost never generated.** Add them.
- **Entry criteria are often missing or too broad**, so the flow starts on every save and pays to start.
- **It does not know your org's conventions** — naming, ownership, the existing flow that already does half of this. Sprawl is easier to create than ever. → [24](24-flow-deployment-versioning-and-governance.md)
- **A generated description on an agent action is read by a model as a contract.** Edit it deliberately; do not ship the first draft. → [23](23-flows-as-agentforce-actions.md)
- **Run context is never part of the prompt.** Generated flows inherit the defaults, which for the triggered types means system context without sharing. → [19](19-flow-run-context-and-sharing.md)

## Recall

Q: What are the three AI authoring capabilities and which is the safest?
A: Generation, natural-language editing, and summarisation. Summarisation — it documents rather than builds.

Q: What did Summer '26 add?
A: Natural-language editing of **existing screen flows** from the Agentforce panel, closing the gap between generating one and iterating on it.

Q: What is the first thing to check on a generated record-triggered flow?
A: Whether it should be before-save. Generators default to after-save, which costs a DML statement for a field update on the triggering record.

Q: Which two things do generated flows almost always lack?
A: Fault paths and tight entry criteria.

Q: Why does a generated description deserve editing on an agent action specifically?
A: Because there the description is the interface the reasoning engine reads to decide whether and how to call the flow.

## Related

- [23 · Flows as Agentforce actions](23-flows-as-agentforce-actions.md) — where a generated description stops being documentation
- [15 · Flow testing & debugging](15-flow-testing-and-debugging.md) — Troubleshoot Flow Errors with Agentforce, the Beta half of this story
- [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md) — the agent platform these features are built on
