# Custom Lightning Types for Agent Output

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 07

**Scope:** Replacing an Agentforce action's default input form and output text with your own LWC. The agent, the topic and the action's Apex live in [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md); this is the rendering contract only.

## Core idea

An agent action returns structured data, and by default the agent flattens it into prose or a generic key-value block. A **Custom Lightning Type** is the metadata that says "when a value of this shape appears, render it with *this* component instead." It is declarative binding, not a callback: you register a type, optionally register a **renderer** LWC for output and an **editor** LWC for input, and the agent runtime instantiates them where it would have drawn its default. That matters because the interesting agent actions return things prose is bad at — a list of flights, an availability grid, a form with dependent picklists — and because an editor override is the only way to collect *validated, structured* input rather than hoping the user phrases it well. The component itself is an ordinary LWC. What is new is the metadata folder and two `js-meta.xml` targets.

## How it works

- **Type metadata lives in `lightningTypes/`,** one folder per type, with a required **`schema.json`** describing the data shape — it mirrors the Apex class whose `@InvocableVariable` properties the action returns.
- **Channel subfolders hold the overrides**, because the same type renders differently per surface: `lightningDesktopGenAi` (Agentforce in Lightning Experience), `enhancedWebChat` (Agentforce Service, Enhanced Chat v2), `lightningMobileGenAi` (mobile agents), `experienceBuilder`.
- **`renderer.json` overrides output; `editor.json` overrides input.** The **`$`** key binds a component to the whole type; the **`collection`** key binds one component to render an entire list at once rather than repeating a single-item renderer.
- **The `js-meta.xml` target is the binding, and it is directional** — `lightning__AgentforceOutput` for a renderer, `lightning__AgentforceInput` for an editor.
- **Data arrives on an `@api value` property**, usually with a getter/setter so the component can normalise it; an editor reports changes back by dispatching a bubbling **`valuechange`** event.
- **Deploy it as metadata.** The `lightningTypes` folder is source-tracked and packaged like any other directory → [09-devops · 2GP](../09-devops-sfdx-and-release-management/INDEX.md).

```
force-app/main/default/
  lightningTypes/
    flightResponse/
      schema.json                      ← required: the data shape
      lightningDesktopGenAi/
        renderer.json                  ← "$": bind a component to the whole type
        editor.json                    ← optional, for input
  lwc/flightDetails/                   ← target: lightning__AgentforceOutput
  lwc/flightRequestFilter/             ← target: lightning__AgentforceInput
```

## 2026 currency

Custom Lightning Types are the supported seam between LWC and Agentforce, and the **per-channel folder structure is the part most write-ups omit** — a renderer registered only under `lightningDesktopGenAi` does nothing in Enhanced Chat v2 or on mobile, which reads as "it works on my machine" and is really "it works on my channel." Summer '26 adds traffic in the other direction: the **`lightning/accApi`** module lets an ordinary LWC drive the Agentforce side panel with `open(botId)`, `close()` and `execute(utterance, botId)` — so a record-page component can hand the agent a question rather than waiting to be asked. Custom Lightning Types decide how agent output *looks*; `accApi` decides when the agent *appears*. → [AI_Data/05-release-radar/](../../AI_Data/05-release-radar/README.md)

## Gotchas

- **A renderer registered on one channel is absent on the others.** Desktop, Enhanced Chat v2, mobile and Experience Builder each need their own folder — there is no inheritance.
- **`schema.json` is required even when you only want a renderer.** Without a registered type there is nothing to bind to.
- **The target is directional.** An output component with `lightning__AgentforceInput` will not render as a renderer, and the failure is silence, not an error.
- **`collection` and `$` solve different problems.** Overriding `$` and letting the runtime repeat it gives you N cards; a `collection` renderer draws the whole list once — the only way to build a table or a grid.
- **The LWC never talks to the LLM.** It receives already-produced data on `value`; anything it needs that the action did not return has to be added to the action, not fetched ad hoc.
- **An editor's `valuechange` must bubble**, or the agent runtime never sees the value and the action runs with the default.
- **Chat surfaces are narrow and often dark.** A renderer built at record-page width and SLDS 1 colours is unreadable in a side panel → [14](14-slds-2-and-styling-hooks.md).

## Recall

Q: What are the three metadata files in a Custom Lightning Type, and which is mandatory?
A: `schema.json` (required — the data shape), `renderer.json` (optional — output UI) and `editor.json` (optional — input UI).

Q: Why does a working renderer sometimes not appear in Enhanced Chat v2?
A: Overrides are registered per channel folder — `lightningDesktopGenAi`, `enhancedWebChat`, `lightningMobileGenAi`, `experienceBuilder`. Registering one does not cover the rest.

Q: Which `js-meta.xml` targets do the renderer and editor components use?
A: `lightning__AgentforceOutput` for the renderer, `lightning__AgentforceInput` for the editor.

Q: What is the difference between the `$` key and the `collection` key in `renderer.json`?
A: `$` binds a component to a single instance of the type; `collection` binds one component to render the entire list in one pass.

Q: What does `lightning/accApi` add, and how is it different from a Custom Lightning Type?
A: It lets an LWC control the Agentforce side panel — `open()`, `close()`, `execute(utterance)`. Custom Lightning Types shape what the agent renders; `accApi` drives when the agent runs.

## Related

- [11 · LWC in Flow screens & quick actions](11-lwc-in-flow-screens-and-quick-actions.md) — the same "the `js-meta.xml` target is the contract" pattern on a different host
- [14 · SLDS 2 & styling hooks](14-slds-2-and-styling-hooks.md) — theme-aware styling, which a chat-panel renderer needs more than a record page does
- [22 · LWC OSS & off-platform reuse](22-lwc-open-source-and-off-platform-reuse.md) — how far a component like this travels
- [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md) — agent actions, topics and the invocable side of the contract
- [04-flow · Flows as agent actions](../04-flow-and-automation/INDEX.md) — the other way an action gets built
