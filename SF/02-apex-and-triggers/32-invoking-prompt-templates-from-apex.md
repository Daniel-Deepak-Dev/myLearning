# Invoking Prompt Templates from Apex

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 23

**Scope:** `ConnectApi.EinsteinLLM` — Apex as the *caller* of a prompt template, the inverse of [31](31-apex-grounded-prompt-templates.md). Calling a model with no template at all is [33](33-models-api-in-apex.md); what makes a template good is [AI_Data/02-salesforce-ai/03-prompt-builder/notes.md](../../AI_Data/02-salesforce-ai/03-prompt-builder/notes.md).

## Core idea

A prompt template is a piece of metadata, so Apex can run one on demand rather than waiting for a user to click Draft with Einstein. `ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate(devName, input)` takes the template's name and a bag of inputs, resolves the merge fields and grounding, sends the result to the model, and hands back both the **resolved prompt** and the **generations**. Keeping the prompt in metadata is the point: an admin edits wording in Prompt Builder without a deploy, and the Trust Layer's masking, grounding and audit trail apply because the call went through the platform's prompt path rather than a raw HTTP callout. The cost is that the coupling is a **string** — the template name — and the input object is far less optional than it looks.

## How it works

| Property of `EinsteinPromptTemplateGenerationsInput` | Type | |
|---|---|---|
| `inputParams` | `Map<String, ConnectApi.WrappedValue>` | **required** — keys are `Input:<param>` |
| `additionalConfig` | `ConnectApi.EinsteinLlmAdditionalConfigInput` | **required** — carries `applicationName` |
| `isPreview` | `Boolean` | **required** — `true` resolves *without* calling the model |
| `citationMode`, `outputLanguage`, `tags` | `String` / `String` / `WrappedValue` | optional, added 61.0–62.0 |

- **Three of the six properties are mandatory**, which is the first surprise — it reads like a config object and behaves like a constructor. Omitting `additionalConfig` fails at runtime.
- **Every input value is double-wrapped**: the record goes into a `Map<String,Object>` as `'id' => recordId`, that map goes into a `ConnectApi.WrappedValue`, and the wrapped value goes into `inputParams` under a key like `Input:Contact`.
- **The response carries both halves** — `.prompt` is the fully resolved text that was sent, `.generations[0].text` is what came back. Logging `.prompt` is the only honest way to debug a bad answer.

```apex
ConnectApi.WrappedValue contact = new ConnectApi.WrappedValue();
contact.value = new Map<String, Object>{ 'id' => contactId };      // wrap #1

ConnectApi.EinsteinPromptTemplateGenerationsInput in =
    new ConnectApi.EinsteinPromptTemplateGenerationsInput();
in.inputParams = new Map<String, ConnectApi.WrappedValue>{
    'Input:Contact' => contact };                                  // wrap #2
in.additionalConfig = new ConnectApi.EinsteinLlmAdditionalConfigInput();
in.additionalConfig.applicationName = 'PromptTemplateGenerationsInvocable';  // exact
in.isPreview = false;                                              // true = no LLM call

ConnectApi.EinsteinPromptTemplateGenerationsRepresentation out =
    ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate('Draft_Follow_Up', in);
String answer = out.generations[0].text;
```

## 2026 currency

**The 67.0 `ConnectApi.EinsteinLLM` reference lists exactly two static methods** — `generateMessagesForPromptTemplate` (**API 60.0**) and `getPromptTemplates` (**API 62.0**). The raw `generateMessages`/`EinsteinLLMGenerationsInput` path that most 2024 write-ups lead with is **not among them**, so treat any tutorial built on it as unusable and reach for [33](33-models-api-in-apex.md) when you genuinely want a model without a template *(the class reference carries no deprecation notice, so this is an absence rather than a documented retirement — confirm in org)*. `getPromptTemplates` is the useful newer half: it lists templates by type, related entity and active state, which is what lets Apex pick a template at runtime instead of hardcoding a dev name.

## Gotchas

- **A `ConnectApi` call is not an `HttpCalloutMock` callout.** The usual mocking reflex does nothing here, and `EinsteinLLM` publishes no `setTest*` methods either — this is the single biggest practical problem with the class → [34](34-testing-ai-apex-and-mocking-llms.md).
- **`applicationName` is a magic string.** The documented value is `PromptTemplateGenerationsInvocable` across every template type; it is not a label you invent.
- **The template dev name is a string dependency.** Renaming the template in Prompt Builder deploys cleanly and breaks Apex at runtime — same failure shape as `Type.forName()` → [28](28-dependency-injection-and-pluggable-apex.md).
- **`isPreview = true` is the cheap path** — it resolves merge fields and grounding and returns without spending a model request. Use it to test resolution and to show a user what will be sent.
- **`inputParams` keys are prefixed `Input:`** and must match the template's parameter names exactly; a wrong key silently resolves to nothing rather than throwing.
- **This is a synchronous call to a slow dependency.** Doing it inside a trigger puts model latency inside the user's save → run it from Queueable → [13](13-queueable-apex-and-chaining.md).
- **`generations` is a list and can be empty** when the Trust Layer blocks a response; indexing `[0]` unguarded is a `ListException` in production.

## Recall

Q: Which method invokes a prompt template from Apex, and what does it return?
A: `ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate(devName, input)`, returning an `EinsteinPromptTemplateGenerationsRepresentation` that carries both the resolved `prompt` and the `generations`.

Q: Which three properties of the input class are required?
A: `inputParams`, `additionalConfig` (with `applicationName`) and `isPreview`.

Q: What does `isPreview = true` do?
A: Resolves the template — merge fields and grounding — and returns without sending anything to the model.

Q: How is a record passed as an input parameter?
A: Double-wrapped: `Map<String,Object>{ 'id' => recordId }` inside a `ConnectApi.WrappedValue`, stored in `inputParams` under an `Input:<name>` key.

Q: Why is a 2024 tutorial using `ConnectApi.EinsteinLLM.generateMessages` a dead end?
A: The 67.0 class reference lists only `generateMessagesForPromptTemplate` and `getPromptTemplates`; the raw-generation method is gone from the documented surface.

## Related

- [31 · Apex-grounded prompt templates](31-apex-grounded-prompt-templates.md) — the inverse direction, where Apex feeds the template instead of calling it
- [33 · Models API in Apex](33-models-api-in-apex.md) — when you want a model and no template at all
- [34 · Testing AI Apex & mocking LLMs](34-testing-ai-apex-and-mocking-llms.md) — why this class cannot be mocked and what to do instead
- [AI_Data · Einstein Trust Layer](../../AI_Data/02-salesforce-ai/04-einstein-trust-layer/notes.md) — the masking, grounding and audit this path buys you over a raw callout
