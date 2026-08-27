# Flows as Agentforce Actions

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** The Flow builder's side of an agent action — what shape a flow must be, and what the agent actually reads. Agent design, reasoning and the wider action catalogue live in [AI_Data/02-salesforce-ai/05](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md).

## Core idea

An agent action built in Flow is an ordinary autolaunched flow with one unusual property: **its caller cannot read it.** The Atlas reasoning engine never sees your canvas. It sees the action's description, the descriptions of the variables marked *Available for input*, and the descriptions of those marked *Available for output* — and it decides from those alone whether to call this flow and what to pass. That inverts the normal relationship between documentation and code. In every other note in this area the description field is a courtesy; here it is **executable specification**, and the commonest cause of "the agent picked the wrong action" is a vague description rather than a model failure. The second property follows from the first: because the descriptions are the contract, **publishing an action locks the interface**. The logic inside stays editable; the inputs and outputs do not.

## How it works

| Requirement | Detail |
|---|---|
| Flow type | **Autolaunched (no trigger) only** — no screen flows, no record-triggered |
| Inputs | variables with **Available for input** ticked, each with a description |
| Outputs | variables with **Available for output** ticked, each with a description |
| Contract | **locked once the action is published** — logic can change, the interface cannot |
| Complex types | Apex-defined variables need a visible **no-argument constructor** |

- **No screens means no clarifying question inside the flow.** If information is missing, the agent asks for it before invoking — which is exactly what the input descriptions are steering.
- **One action, one job.** An action that does three things forces the reasoning engine to guess which one you meant; three small flows route more reliably than one flexible one.
- **Fail loudly with a usable message.** An agent has to explain the failure to a person, and `$Flow.FaultMessage` is not that message. → [10](10-fault-paths-and-custom-errors.md)
- **The invocable no-arg constructor rule starts at API 66.0**, not 67.0, and it fails at run time inside the agent rather than at compile time. → [02-apex · 22](../02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md)
- **The flow runs in its caller's context** and an agent is not a user in the usual sense — treat access as a deliberate decision, not an inheritance. → [19](19-flow-run-context-and-sharing.md)

## 2026 currency

Summer '26 puts the agent *inside* Flow Builder rather than only alongside it. The **Create Agent element (GA)** builds or deploys an agent straight from the canvas, including small purpose-built agents with their own instructions — so a flow can now create the thing that calls flows. The **Add Prompt Instructions element** gained breadcrumb navigation for nested resource selection, which matters more than it sounds when the prompt is assembled from Apex-defined structures. The wider context is the authoring shift recorded in the AI vault: since **July 2026** new agents are authored in **Agent Script**, not the legacy topic-and-instruction builder, and most tutorials still teach the old model. What has not changed is the part this note owns — the flow is still an autolaunched flow and the description is still the interface. → [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md)

## Gotchas

- **Only autolaunched flows qualify.** A screen flow cannot be an agent action, and neither can a record-triggered one.
- **A variable without *Available for input* is invisible to the agent**, and the failure looks like the agent ignoring instructions.
- **Descriptions are the interface.** "Account Id" is not a description; "the 18-character Id of the account to credit, from the current case" is.
- **Publishing locks the input and output contract.** Design the signature before you build the logic, not after.
- **An unhandled fault reaches a customer as a non-answer.** Catch it and return an output the agent can say out loud. → [10](10-fault-paths-and-custom-errors.md)
- **Flow has no Map type**, so anything map-shaped has to be modelled as a collection of records or an Apex-defined type. → [11](11-flow-and-apex-interop.md)
- **An over-general action is a routing hazard**, not a convenience — it competes with every other action for the same request.
- **Agent invocation is not free.** Each action consumes Flex Credits, so a chatty design is a billing design. → [AI_Data/GLOSSARY.md](../../AI_Data/GLOSSARY.md)

## Recall

Q: Which flow types can be an Agentforce action?
A: Autolaunched (no trigger) only.

Q: What does the reasoning engine actually read when deciding to call your flow?
A: The action description and the descriptions of the input and output variables — never the flow itself.

Q: What is locked when you publish a flow as an agent action?
A: The interface — the input and output variables. The internal logic stays editable.

Q: Why can't an agent action flow ask the user a question mid-flow?
A: It has no screens. The agent gathers inputs before invoking, steered by the input descriptions.

Q: What did the Summer '26 Create Agent element add to Flow Builder?
A: The ability to build or deploy an agent — including a small purpose-built one — directly from the flow canvas.

## Related

- [AI_Data/02-salesforce-ai/05 Custom agent actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) — the full action catalogue and the description-as-specification argument
- [02-apex · 22 Invocable Apex & Agentforce actions](../02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md) — the coded action, and the API 66.0 constructor rule
- [11 · Flow & Apex interop](11-flow-and-apex-interop.md) — the typed-payload boundary an agent action inherits
