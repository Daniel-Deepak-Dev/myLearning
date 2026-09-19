# Template-Triggered Prompt Flows

> Folder: SF_Agentforce · Level: working · Status: ✅ complete
> Created: 2026-08-27 · Updated: 2026-08-30

**One line:** A flow type whose only job is to gather data and hand it to a prompt template as text.

**Reach for it when:** A merge field cannot reach the data — you need a query, a loop, or formatting before the model sees it.

## Key points

- A **distinct flow type**, chosen at creation — not record-triggered, not autolaunched. Its output reaches the template as `{!$Flow:Flow_API_Name.Prompt}`.
- **It must be activated before it appears** in the Prompt Template workspace. A draft is invisible — and silently so.
- The flow emits its text through the **Add Prompt Instructions** element. That element is **additive** — use it as many times as you need and the text appends.
- At creation the flow binds to a **capability**, and the binding decides reuse: `PromptTemplateType://einstein_gpt__salesEmail` · `__fieldCompletion` · `__recordSummary` · or `FlexTemplate://<template_API_Name>`.
- **A type binding serves every template of that type. A `FlexTemplate://` binding serves exactly one named template.** That is the whole reusable-flow question — reuse comes from binding to the type, not to the template.
- The input choice — **Manual** or **Automatic** — is also set at creation and decides where the data comes from.

| | Manual Inputs | Automatic Inputs |
|---|---|---|
| Driven by | The user, at run time | The system, from the record |
| Feels like | A modal asking for text | A button that just works |
| Use for | Ad-hoc context in the user's head | Data already in the org |
| Example | A `User_Instructions` variable: *"warm tone, emphasise the new nav UI"* | Account ID passed in; the flow runs Get Records for open Cases |

> **From my notes.** *"Automatic Inputs take template type as input to match the flow availability only for the specific prompt template."* — right instinct. Automatic scopes the flow to one template type; Manual leaves it general.

## Gotchas

- **This is only one of the two directions.** Here the flow feeds the template while it resolves. The other way round, an *activated* template is an invocable action any ordinary flow can call to get text back → [SF_core · 04-flow · 28](../SF_core/04-flow-and-automation/28-calling-prompt-templates-from-flow.md). Both get called "prompt flows" in a design review.
- **Getting the input type wrong means rebuilding the flow.** Set at creation, like the flow type and the capability binding.
- **The flow returns text, not structure.** Whatever you build gets flattened into the prompt as a string.
- **Binding to `FlexTemplate://` locks the flow to that one template.** Renaming the template breaks the binding, with no compile-time warning.

## Confirm in org

- 🚩 Whether those four capability bindings are still the full list at Summer '26. The source is an **April 2024** blog and the set has probably grown.
- 🚩 What happens when the flow faults mid-run — does the prompt fail, or resolve with the text gathered so far? No doc states it.
- 🚩 Whether the flow runs as the requesting user or in system mode. Not documented either way, and it decides whether a Get Records can over-fetch.

## Hands-on

- [ ] **AF-FLOW-01** · 30 min · Build a prompt flow with Automatic inputs and use **Add Prompt Instructions** twice. **Proves:** the element is additive — the second block appends rather than replacing.
- [ ] **AF-FLOW-02** · 10 min · Leave the flow as a draft and go looking for it in the Prompt Template workspace. **Proves:** an inactive flow is invisible, and silently so.
- [ ] **AF-FLOW-03** · 20 min · Force a fault on a Get Records inside the flow. **Settles:** whether the prompt fails or resolves with the text gathered so far 🚩.
- [ ] **AF-FLOW-04** · 20 min · Run the same flow as an admin and as a minimal-permission user. **Settles:** running user or system mode 🚩.

## Related

- [Prompt Template Types](prompt-template-types.md) — the type an Automatic-input flow binds itself to
- [Flex Prompt Templates](flex-prompt-templates.md) — the type a `FlexTemplate://` binding names, and why it needs a caller at all
- [Grounding a Prompt Template](grounding-a-prompt-template.md) — Flow is one of the six grounding sources
- [SF_core · 04-flow · 28 Calling a prompt template from Flow](../SF_core/04-flow-and-automation/28-calling-prompt-templates-from-flow.md) — the **opposite direction**: a flow invoking a template as an action
- [SF_core · 04-flow · 23 Flows as Agentforce actions](../SF_core/04-flow-and-automation/23-flows-as-agentforce-actions.md) — a **different** thing: autolaunched flows an agent calls as an action

## Sources

- [Template-Triggered Prompt Flows](https://help.salesforce.com/s/articleView?id=platform.flow_concepts_trigger_prompt_template_capability.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-27 — page is JS-rendered, open it to verify
- [Ground Your Prompt Templates with Data Using Flow or Apex](https://developer.salesforce.com/blogs/2024/04/ground-your-prompt-templates-with-data-using-flow-or-apex) — Salesforce Developers, **April 2024** · read 2026-08-28 · the four capability bindings
- [Add a Flow to Your Prompt Template](https://trailhead.salesforce.com/content/learn/projects/quick-start-create-prompt-builder-flex-template/add-a-flow-to-your-prompt-template) — Trailhead · read 2026-08-27

## History

- 2026-08-27 · created from your Day-5 notes · your two scenarios kept as the Manual/Automatic examples
- 2026-08-28 · added the four capability bindings, the Add Prompt Instructions element, and the reuse rule — a type binding serves every template of that type, a `FlexTemplate://` binding serves one
- 2026-08-30 · added the two-directions gotcha — this flow feeds a template; an ordinary flow can also *call* one as an invocable action
