# Testing AI Apex & Mocking LLMs

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 23

**Scope:** Why none of [31](31-apex-grounded-prompt-templates.md)–[33](33-models-api-in-apex.md) is testable by reflex, and the one shape that makes them testable. The general mocking toolkit is [21](21-apex-testing-advanced-and-mocking.md); the injection mechanics are [28](28-dependency-injection-and-pluggable-apex.md).

## Core idea

**Every standard Apex mocking route fails on `ConnectApi.EinsteinLLM`, and it is worth being precise about why, because each failure has a different cause.** `HttpCalloutMock` does not apply — a `ConnectApi` call is not an `HttpRequest`. The documented ConnectApi convention of a `setTest`-prefixed registration method (*"A test method name is the regular method name with a `setTest` prefix"*) does not apply either: the 67.0 `EinsteinLLM` reference publishes no such method. And the Stub API cannot reach it, because the method is **static** and sits in a namespace you do not own — two entries on the restriction list in [21](21-apex-testing-advanced-and-mocking.md) at once. That leaves exactly one route, and it is a design decision rather than a test trick: **wrap the AI call behind your own interface and inject it**. This is [28](28-dependency-injection-and-pluggable-apex.md) arriving as a hard precondition rather than a preference — the same argument that note makes about the Stub API, with the escape hatch removed.

## How it works

| Route | Works on AI Apex? |
|---|---|
| `Test.setMock(HttpCalloutMock…)` | **No** for `ConnectApi` — it is not an HTTP callout |
| ConnectApi `setTest*` registration | **No** — `EinsteinLLM` publishes none |
| Stub API (`Test.createStub`) | **No** — the method is static and out-of-namespace |
| Your own interface + injection | **Yes** — the only reliable seam |
| `@IntegrationTest` (Dev Preview) | Live calls, scratch org only → [21](21-apex-testing-advanced-and-mocking.md) |

- **Own the boundary.** One small interface — `generate(String templateName, Map<String,Object> params)` — with a real implementation that calls `ConnectApi` and a fake that returns a canned string. Production code depends on the interface and never names `ConnectApi` directly.
- **Assert on the call, not the completion.** A model is non-deterministic, so asserting on generated text is a flaky test by construction. Assert that the right template was invoked, with the right inputs, and that your code handled the response — record the arguments in the fake and assert those.
- **`isPreview = true` is the one genuine assertion available without a model** → [32](32-invoking-prompt-templates-from-apex.md). It resolves merge fields and grounding and returns, so a test can verify the *prompt* is right even though the answer cannot be.

```apex
public interface LlmGateway { String generate(String template, Map<String, Object> params); }

public with sharing class CaseSummary {
    @TestVisible private static LlmGateway gateway = new EinsteinGateway();  // the seam
    public static String summarise(Id caseId) {
        return gateway.generate('Case_Summary', new Map<String, Object>{ 'id' => caseId });
    }
}

@IsTest
private class CaseSummaryTest {
    private class FakeGateway implements LlmGateway {
        public String lastTemplate;                       // assert on THIS, not on text
        public String generate(String t, Map<String, Object> p) { lastTemplate = t; return 'x'; }
    }
}
```

## Gotchas

- **A green test proves nothing was called.** With the fake injected, no model ever runs — the same failure shape as an undelivered platform-event subscriber passing green → [26](26-testing-platform-events-and-cdc.md). Assert the fake was actually invoked.
- **An unmocked Models API call in a test throws**, because it is a callout underneath and test methods do not support callouts without a registered mock → [19](19-callouts-named-credentials-and-http-in-apex.md).
- **Whether `HttpCalloutMock` reaches `aiplatform.ModelsAPI` is not worth relying on** even if it happens to work, since External Services generates the class — the wrapper is the seam that survives a regeneration *(unverified — confirm in org)*.
- **`@TestVisible` on the injection point is enough**, and is less ceremony than a full factory for a single collaborator. Reach for CMDT binding only when the choice must vary per org → [28](28-dependency-injection-and-pluggable-apex.md).
- **User mode makes the running identity part of the test.** Grounding queries return what *that* user can see, so an AI test without `System.runAs` is testing the admin's answer → [10](10-apex-security-user-mode-and-fls.md), [20](20-apex-testing-fundamentals.md).
- **Tests that do reach a real model are billed** like any other Einstein Request → [33](33-models-api-in-apex.md), which is a second reason `@IntegrationTest` runs in scratch orgs rather than in CI against a sandbox.
- **A fake that always succeeds hides the interesting half.** The Trust Layer can return zero generations; make the fake capable of returning an empty list so the null-handling path is covered.

## Recall

Q: Why can't the Stub API mock `ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate`?
A: The method is static and belongs to a namespace you don't own — both are on the Stub API's restriction list.

Q: What is the documented ConnectApi test convention, and why doesn't it help here?
A: Register test data with a `setTest`-prefixed method matching the real signature. `EinsteinLLM` publishes no `setTest*` methods, so there is nothing to register.

Q: What should an AI Apex test assert on?
A: The call — which template, which inputs, and how the response was handled — not the generated text, which is non-deterministic.

Q: What is the only mocking route that works reliably across all three AI surfaces?
A: Your own interface wrapping the call, injected at a `@TestVisible` seam.

Q: How can a test verify a prompt without spending a model request?
A: Set `isPreview = true`, which resolves the template and grounding and returns the prompt without calling the model.

## Related

- [21 · Apex testing advanced & mocking](21-apex-testing-advanced-and-mocking.md) — the Stub API restriction list this note cashes in, and `@IntegrationTest`
- [28 · Dependency injection & pluggable Apex](28-dependency-injection-and-pluggable-apex.md) — the seam itself; here it is mandatory rather than preferred
- [32 · Invoking prompt templates from Apex](32-invoking-prompt-templates-from-apex.md) — the unmockable class, and `isPreview` as a partial way out
- [26 · Testing platform events & CDC](26-testing-platform-events-and-cdc.md) — the same "passes green, did nothing" trap in a different subsystem
