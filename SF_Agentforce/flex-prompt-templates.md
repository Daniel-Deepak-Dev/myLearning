---
vault: SF_Agentforce
format: light
level: working
status: open
gaps: 3
org_checks: 2
labs: 3
created: 2026-08-30
updated: 2026-08-30
---
# Flex Prompt Templates

**One line:** The prompt template type with no entry point of its own — you declare the inputs, and you supply the caller.

**Reach for it when:** The generated text does not belong in the email composer, a record field, or a record-page panel.

## Key points

- **Every other type owns a surface.** Sales Email owns the email composer, Field Generation a field, Record Summary a record-page panel — they ship wired to it → [Prompt Template Types](prompt-template-types.md).
- **Flex owns none, by design.** The rule: *if you can point at the button Salesforce already built for it, use that type. If you cannot, it is Flex.*
- **You declare the inputs — up to 5 resources**, each with a Name, an API Name and a Source Type: **Object**, **Free Text** or **File**. A File input makes the template multimodal (image, PDF).
- **Arbitrary inputs are the whole point.** They let a caller with no record on screen pass context — which is why an agent action needs Flex. **All four callers need the template activated**; a draft is invisible, and silently so.

## The four callers

| Caller | How it calls | Typical use |
|---|---|---|
| **Agentforce** | agent action, `GenAiFunction` → [Agent Actions](prompt-templates-as-agent-actions.md) | the agent decides to call it mid-conversation |
| **Flow** | Actions element → category **Prompt Template** → [SF_core · 04-flow · 28](../SF_core/04-flow-and-automation/28-calling-prompt-templates-from-flow.md) | screen flow behind a quick action; scheduled; record-triggered |
| **Apex / LWC** | `ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate`, inputs keyed `Input:<APIName>` → [SF_core · 02-apex · 32](../SF_core/02-apex-and-triggers/32-invoking-prompt-templates-from-apex.md) | custom UI, batch, queueable |
| **REST** | `POST /einstein/prompt-templates/<devName>/generations` | an external system asking Salesforce for text |

> **From my notes.** You had Flex, template-triggered prompt flows and **Add Prompt Instructions** in one list and could not place Flex. They are two opposite directions — the first gotcha below is the whole answer.

## Gotchas

- **Flow and a template point both ways, and the names do not help.** A **template-triggered prompt flow** feeds text *into* the template while it resolves (`Add Prompt Instructions` → `{!$Flow:….Prompt}`). An ordinary flow *calls* an activated template as an action and reads the generation back → [Template-Triggered Prompt Flows](template-triggered-prompt-flows.md).
- **A Flex *template* has nothing to do with *Flex Credits*.** Same word, unrelated meanings — the credits are the Agentforce billing unit, and they are what the repo mostly talks about.
- **No surface of its own also means no default error path.** Whatever calls it owns the failure message, and renaming the template's API name breaks all four callers at runtime — every one holds it as a string.

## Gaps to close

- [ ] Does the resource picker offer any source type beyond Object, Free Text and File at Summer '26?
- [ ] Is the 5-resource cap separate from the 5-Flow / 5-Apex grounding caps, or one shared budget?
- [ ] Which models accept File inputs, and what file types and sizes are allowed?

## Confirm in org

- 🚩 Does the Flow **Prompt Template** action category list every activated template, or only Flex ones?
- 🚩 Whose permissions resolve the grounding when a Flex template is invoked over REST — the integration user's?

## Hands-on

- [ ] **AF-FLEX-01** · 25 min · Build a Flex template with two resources — an Object and a Free Text — then call it from a screen flow behind a quick action. **Proves:** Flex has no surface of its own; the entry point is the one you supply.
- [ ] **AF-FLEX-02** · 10 min · Deactivate that template, then reopen the flow's Actions list and look for it. **Proves:** activation is what publishes the invocable action — a draft is invisible to every caller.
- [ ] **AF-FLEX-03** · 15 min · Add a sixth resource to a Flex template. **Proves:** the 5-resource cap is real — copy the error string verbatim.

## Related

- [Prompt Template Types](prompt-template-types.md) — the five types that do own a surface, and what each grounds on
- [Prompt Templates as Agent Actions](prompt-templates-as-agent-actions.md) — the Agentforce caller, in full
- [Template-Triggered Prompt Flows](template-triggered-prompt-flows.md) — the **other** direction: a flow feeding the template
- [Grounding a Prompt Template](grounding-a-prompt-template.md) — declared inputs are not grounding; these are the six sources that are
- [Prompt Template Versions & Access](prompt-template-versions-and-access.md) — the activation gate every caller hits
- [SF_core · 04-flow · 28 Calling a prompt template from Flow](../SF_core/04-flow-and-automation/28-calling-prompt-templates-from-flow.md) — the Flow caller, in full
- [SF_core · 02-apex · 32 Invoking prompt templates from Apex](../SF_core/02-apex-and-triggers/32-invoking-prompt-templates-from-apex.md) — the Apex caller, and the `Input:` key convention

## Sources

- [Flex Prompt Templates in Action](https://help.salesforce.com/s/articleView?id=sf.prompt_builder_templates_in_action_flex.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-30 · *"Flex templates don't have predefined entry points"*, and the Apex / Flow / REST / Agentforce list — page is JS-rendered, open it to verify
- [Build a Flex Prompt Template](https://trailhead.salesforce.com/content/learn/projects/quick-start-create-prompt-builder-flex-template/build-a-flex-prompt-template) — Trailhead · read 2026-08-30 · *"you can add up to five resources"*, and the Name / API Name / Source Type / Object dialog
- [Invoke Prompt Templates from Flow, Apex, or the REST API](https://developer.salesforce.com/blogs/2024/04/invoke-prompt-templates-from-flow-apex-or-the-rest-api) — Salesforce Developers, **April 2024** · read 2026-08-30 · the Prompt Template action category, the `Input:` keys, the REST path
- [Unlock Multi-Modal AI with File Inputs in Prompt Builder](https://developer.salesforce.com/blogs/2025/05/unlock-multi-modal-ai-with-file-inputs-in-prompt-builder) — Salesforce Developers, May 2025 · via search 2026-08-30 · File inputs, and the PDF/image use cases
- [Exercise 4: Create a Flex Template](https://developer.salesforce.com/workshops/agentforce-workshop/prompt-builder/4-flex-template) — Salesforce Developers · read 2026-08-30 · the creation dialog and the Preview panel

## History

- 2026-08-30 · created from your Flex / template-triggered-prompt-flow notes · splits out the *where do I use Flex* answer that [Prompt Template Types](prompt-template-types.md) only gestured at
