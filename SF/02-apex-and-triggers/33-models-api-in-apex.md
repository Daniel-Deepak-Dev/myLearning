# Models API in Apex

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 23

**Scope:** The `aiplatform.ModelsAPI` class — calling a model directly from Apex with no prompt template in the way. Going *through* a template is [32](32-invoking-prompt-templates-from-apex.md); choosing or registering the model itself is [AI_Data/02-salesforce-ai/06-model-builder-byom/notes.md](../../AI_Data/02-salesforce-ai/06-model-builder-byom/notes.md).

## Core idea

`aiplatform.ModelsAPI` is the lowest level the platform offers: a prompt in, a completion out, no template metadata involved. It still runs through the Einstein Trust Layer, so masking, zero retention and the audit trail survive, but everything a prompt template gave you for free — the admin-editable wording, the grounding, the versioning — is now your Apex's problem. **The class is generated from an External Services definition rather than hand-designed**, which explains its whole shape: a `_Request`/`_Response`/`_ResponseException` triad per method, a `Code200` property standing in for an HTTP status, and a `body` you populate separately from the request wrapper. It is also, unlike `ConnectApi`, **instantiated** — the methods are instance methods on a `new aiplatform.ModelsAPI()`.

## How it works

| Method | Body type | Read the result from |
|---|---|---|
| `createGenerations` | `ModelsAPI_GenerationRequest` | `Code200.generation.generatedText` |
| `createChatGenerations` | `ModelsAPI_ChatGenerationsRequest` | `Code200.generationDetails.generations` |
| `createEmbeddings` | `ModelsAPI_EmbeddingRequest` | `Code200.embeddings` |
| `submitFeedback` | `ModelsAPI_FeedbackRequest` | — |

- **The model is a string API name** on the request wrapper, e.g. `sfdc_ai__DefaultOpenAIGPT4OmniMini`, so switching models is configuration rather than a code change.
- **Chat messages are role-tagged objects**: a `List<ModelsAPI_ChatMessageRequest>`, each with `content` and a `role` of `system` or `user`. That list is the entire conversation — the API is stateless and remembers nothing between calls.
- **Each method throws its own exception type**, `createChatGenerations_ResponseException` and friends, carrying `responseCode`. There is no common base to catch.

```apex
aiplatform.ModelsAPI.createChatGenerations_Request req =
    new aiplatform.ModelsAPI.createChatGenerations_Request();
req.modelName = 'sfdc_ai__DefaultOpenAIGPT4OmniMini';      // config, not code
aiplatform.ModelsAPI_ChatGenerationsRequest body = new aiplatform.ModelsAPI_ChatGenerationsRequest();
aiplatform.ModelsAPI_ChatMessageRequest msg = new aiplatform.ModelsAPI_ChatMessageRequest();
msg.role = 'user';                                          // 'system' or 'user'
msg.content = 'Summarise this case in two sentences.';
body.messages = new List<aiplatform.ModelsAPI_ChatMessageRequest>{ msg };
req.body = body;                                            // body is set separately

try {
    aiplatform.ModelsAPI api = new aiplatform.ModelsAPI();  // NOT static
    System.debug(api.createChatGenerations(req).Code200.generationDetails.generations);
} catch (aiplatform.ModelsAPI.createChatGenerations_ResponseException e) {
    System.debug(e.responseCode);                           // one exception type per method
}
```

## 2026 currency

**Every Models API request is billed.** The documentation is explicit that requests "are subject to Salesforce's usage and billing rates for **Einstein Requests**", which makes this the rare Apex class where a `for` loop has a line-item cost — a design consideration, not just a governor one. Rate-card and credit detail deliberately stays out of this vault; the entitlement story lives with the licence notes → [07-security · 02](../07-security-and-sharing/02-licences-and-what-they-gate.md) and [AI_Data · Model Builder & BYOM](../../AI_Data/02-salesforce-ai/06-model-builder-byom/notes.md). The second thing to know is architectural rather than new: because the class is generated from **External Services**, its calls are **Apex callouts** and consume the same per-transaction budget as every `HttpRequest` you make → [19](19-callouts-named-credentials-and-http-in-apex.md).

## Gotchas

- **It spends the callout budget.** Model calls count against the 100 callouts per transaction shared with all other HTTP, and against the callout timeout — so a model call per record in a trigger is a design error twice over.
- **`ModelsAPI` is instantiated, not static**, unlike `ConnectApi.EinsteinLLM`. `aiplatform.ModelsAPI.createChatGenerations(req)` does not compile.
- **`req.body` is a separate assignment.** Building the body and forgetting to attach it to the request wrapper is the most common first failure, and it fails at runtime.
- **There is no shared exception base** — each method has its own `_ResponseException`, so a generic handler needs `catch (Exception e)` and loses `responseCode`.
- **No template means no grounding and no admin edit path.** The prompt is a string literal in Apex, so changing wording is a deploy. If a human should own the words, use [32](32-invoking-prompt-templates-from-apex.md).
- **`createEmbeddings` returns a vector Apex has nowhere to put.** There is no native vector type or similarity operator; storage and search belong in Data 360, not in a `List<Double>` on an sObject.
- **The call is stateless.** Multi-turn behaviour means resending the whole message list every time, and that resend is billed and counts toward the model's context limit.

## Recall

Q: What namespace and class expose the Models API to Apex, and are the methods static?
A: `aiplatform.ModelsAPI` — and no, they are instance methods; you call them on `new aiplatform.ModelsAPI()`.

Q: Why does the class have that `_Request` / `_Response` / `_ResponseException` shape?
A: It is generated from an External Services definition rather than hand-written, which also explains `Code200` and the separately-assigned `body`.

Q: What are the four methods?
A: `createGenerations`, `createChatGenerations`, `createEmbeddings` and `submitFeedback`.

Q: Which two budgets does a Models API call spend?
A: The Apex callout limit, because it is a callout underneath, and Einstein Requests, because every request is billed.

Q: When should you reach for a prompt template instead of this class?
A: When the wording should be editable by an admin, or when you need grounding and versioning — a template keeps those in metadata; here the prompt is a literal in Apex.

## Related

- [32 · Invoking prompt templates from Apex](32-invoking-prompt-templates-from-apex.md) — the same destination with metadata and grounding in front of it
- [19 · Callouts, Named Credentials & HTTP](19-callouts-named-credentials-and-http-in-apex.md) — the callout budget these calls draw down
- [34 · Testing AI Apex & mocking LLMs](34-testing-ai-apex-and-mocking-llms.md) — how to test a class that bills per call
- [AI_Data · Model Builder & BYOM](../../AI_Data/02-salesforce-ai/06-model-builder-byom/notes.md) — where model API names come from and when a custom model is justified
