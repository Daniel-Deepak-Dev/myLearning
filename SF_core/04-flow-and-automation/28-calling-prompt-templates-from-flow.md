# Calling a Prompt Template from Flow

> Area: 04-flow-and-automation · Level: working · Status: 🌱 3 gaps open
> Currency: **Summer '26 (API 67.0)** · Created: 2026-08-30 · Updated: 2026-08-30

**One line:** An activated prompt template is automatically an invocable action, so any flow can call one and read the generated text back.

**Reach for it when:** You want AI-written text inside automation you already own — a quick action, a scheduled job, a record update — and there is no Salesforce button that already produces it.

## Key points

- **Nothing to register.** Save and activate a template in Prompt Builder and it appears in the **Actions** element; filter the list by the **Prompt Template** category.
- **The inputs are the template's declared resources.** A [Flex template](../../SF_Agentforce/flex-prompt-templates.md) is the only type where you choose what those are, which is why Flex is the type you will nearly always be calling here.
- **Pass a record input as the record, not the Id** — the action expects the object type the template declared.
- **Assign the returned generation to a text variable**, then do the ordinary flow thing with it: write it to a field, put it on a screen, send it.
- **This is the reverse of a template-triggered prompt flow**, which is the flow type you build when the *template* needs data, not when *you* need text.
- **The template's API name is a string dependency.** Renaming it in Prompt Builder deploys cleanly and breaks the flow at run time — the same failure shape as [11 · invocable Apex](11-flow-and-apex-interop.md) losing a method.

## The two directions

| Direction | What you build | Who starts it |
|---|---|---|
| **Flow → template** (grounding) | a **template-triggered prompt flow**, emitting via **Add Prompt Instructions**, read in the template as `{!$Flow:….Prompt}` → [SF_Agentforce](../../SF_Agentforce/template-triggered-prompt-flows.md) | the **template**, while it resolves |
| **Template → flow** (invocation) | any ordinary flow, **Actions** element, **Prompt Template** category | the **flow**, when it reaches the element |

## Gotchas

- **The two directions share a vocabulary and nothing else.** "Prompt flow" is ambiguous in a design review — say which way the data goes.
- **A draft template is invisible here**, and silently so: it simply never appears in the action list. Same activation gate Apex and agent actions hit.
- **A generation can come back empty** when the Trust Layer blocks the response, so a template call needs a fault path and a sensible default → [10 · Fault paths & custom errors](10-fault-paths-and-custom-errors.md).
- **An LLM call is slow.** [02-apex · 32](../02-apex-and-triggers/32-invoking-prompt-templates-from-apex.md) documents the Apex version as a synchronous call to a slow dependency; putting one in a record-triggered flow puts model latency inside the user's save.

## Gaps to close

- [ ] What the action's output variables are actually named, and whether the resolved prompt is returned alongside the generation as it is in Apex.
- [ ] Does the Flow action expose `isPreview` and `additionalConfig`, or only the template's inputs?
- [ ] Does a template invoked from a plain flow — no agent anywhere — draw Flex Credits, and at what rate?

## Confirm in org

- 🚩 Does the **Prompt Template** action category list every activated template, or only Flex ones?
- 🚩 Can a record-triggered flow call it at all, and if so does it run inside the save transaction?

## Hands-on

- [ ] **SF-PTFLOW-01** · 20 min · Activate a Flex template, then call it from a screen flow and display the generation on a screen. **Proves:** activation alone publishes the invocable action — there is no registration step.
- [ ] **SF-PTFLOW-02** · 15 min · Rename the template's API name and rerun the flow. **Proves:** the dependency is a string; it deploys clean and fails at run time.
- [ ] **SF-PTFLOW-03** · 20 min · Build both directions against one template — a template-triggered prompt flow feeding it, and a screen flow calling it. **Proves:** they are different features that happen to share a noun.

## Related

- [SF_Agentforce · Flex Prompt Templates](../../SF_Agentforce/flex-prompt-templates.md) — the type you will be calling, and the other three callers
- [SF_Agentforce · Template-Triggered Prompt Flows](../../SF_Agentforce/template-triggered-prompt-flows.md) — the opposite direction, and the flow type this area does not own
- [23 · Flows as Agentforce actions](23-flows-as-agentforce-actions.md) — a third relationship again: the flow *is* the action an agent calls
- [02-apex · 32 Invoking prompt templates from Apex](../02-apex-and-triggers/32-invoking-prompt-templates-from-apex.md) — the coded equivalent, with the input-wrapping and `isPreview` detail
- [11 · Flow & Apex interop](11-flow-and-apex-interop.md) — the invocable-action machinery this rides on
- [10 · Fault paths & custom errors](10-fault-paths-and-custom-errors.md) — what to do when the generation is empty

## Sources

- [Invoke Prompt Templates from Flow, Apex, or the REST API](https://developer.salesforce.com/blogs/2024/04/invoke-prompt-templates-from-flow-apex-or-the-rest-api) — Salesforce Developers, **April 2024** · read 2026-08-30 · every activated template is an invocable action, filtered by the **Prompt Template** category, with record inputs passed as the related entity
- [Flex Prompt Templates in Action](https://help.salesforce.com/s/articleView?id=sf.prompt_builder_templates_in_action_flex.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-30 · Flow named as one of the four ways a Flex template is applied — page is JS-rendered, open it to verify

## History

- 2026-08-30 · created — the Flow side of prompt templates had no home, so the area covered *flow as an agent action* and *flow feeding a template* but not *flow calling a template*
