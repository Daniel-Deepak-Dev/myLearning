# Template-Triggered Prompt Flows

> Folder: SF_Agentforce · Level: working · Status: 🌱 4 gaps open
> Created: 2026-08-27 · Updated: 2026-08-27

**One line:** A flow type whose only job is to gather data and hand it to a prompt template as text.

**Reach for it when:** A merge field cannot reach the data — you need a query, a loop, or formatting before the model sees it.

## Key points

- A **distinct flow type**, chosen at creation — not record-triggered, not autolaunched. Its output reaches the template as `{!$Flow:Flow_API_Name.Prompt}`.
- **It must be activated before it appears** in the Prompt Template workspace. A draft is invisible — and silently so.
- The input choice — **Manual** or **Automatic** — is also set at creation and decides where the data comes from.

| | Manual Inputs | Automatic Inputs |
|---|---|---|
| Driven by | The user, at run time | The system, from the record |
| Feels like | A modal asking for text | A button that just works |
| Use for | Ad-hoc context in the user's head | Data already in the org |
| Example | A `User_Instructions` variable: *"warm tone, emphasise the new nav UI"* | Account ID passed in; the flow runs Get Records for open Cases |

> **From my notes.** *"Automatic Inputs take template type as input to match the flow availability only for the specific prompt template."* — right instinct. Automatic scopes the flow to one template type; Manual leaves it general.

## Gotchas

- **Getting the input type wrong means rebuilding the flow.** Set at creation, like the flow type itself.
- **The flow returns text, not structure.** Whatever you build gets flattened into the prompt as a string.

## Gaps to close

- [ ] 🚩 Exactly which template types accept a flow — docs show Field Generation, Sales Email and reusable flows, but not the full list. Confirm in org.
- [ ] What happens when the flow faults mid-run — does the prompt fail, or resolve with empty text?
- [ ] Does the flow run as the requesting user, or in system mode?
- [ ] Can one flow serve several templates, and what does the reusable-flow pattern require?

## Related

- [Prompt Template Types](prompt-template-types.md) — the type an Automatic-input flow binds itself to
- [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md) — merge fields, the simpler alternative
- [SF_core · 04-flow · 23 Flows as Agentforce actions](../SF_core/04-flow-and-automation/23-flows-as-agentforce-actions.md) — a **different** thing: autolaunched flows an agent calls as an action

## Sources

- [Template-Triggered Prompt Flows](https://help.salesforce.com/s/articleView?id=platform.flow_concepts_trigger_prompt_template_capability.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-27 — page is JS-rendered, open it to verify
- [Add a Flow to Your Prompt Template](https://trailhead.salesforce.com/content/learn/projects/quick-start-create-prompt-builder-flex-template/add-a-flow-to-your-prompt-template) — Trailhead · read 2026-08-27

## History

- 2026-08-27 · created from your Day-5 notes · your two scenarios kept as the Manual/Automatic examples
