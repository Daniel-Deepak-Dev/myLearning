# Apex Testing Advanced & Mocking

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 05

**Scope:** Replacing the parts of a transaction a test cannot execute — callouts, slow dependencies, async completion. The data and isolation half is [20](20-apex-testing-fundamentals.md).

## Core idea

A test cannot make a callout, so anything past an HTTP boundary has to be faked. Apex gives you two tools for that and they answer different questions. `HttpCalloutMock` fakes the *wire*: you keep the real service class and hand it a response you chose, which is right when the thing under test is your parsing and error handling. The **Stub API** fakes an *object*: `Test.createStub` builds a runtime subclass of a class you name, and every call to it is routed to your `StubProvider` instead of the real implementation — right when the dependency is expensive, non-deterministic, or simply not the subject. The cost of the Stub API is that it only works on a surface Apex can subclass, and that surface is narrower than most write-ups admit.

## How it works

- **`Test.setMock(HttpCalloutMock.class, new MyMock())`** registers a response generator for the whole test. `Test.setMock(WebServiceMock.class, …)` is the SOAP equivalent. Neither works outside a test context.
- **`Test.createStub(TypeToMock.class, provider)`** returns a stub instance. Your provider implements `System.StubProvider.handleMethodCall(stubbedObject, stubbedMethodName, returnType, listOfParamTypes, listOfParamNames, listOfArgs)` — six arguments, and the method name arrives as a `String`, so a rename breaks the stub silently at runtime rather than at compile time.
- **The stub must be in the same namespace** as the `Test.createStub` call.
- **Async work is asserted after `Test.stopTest()`**, which flushes the queue. Chained Queueables run one level only, so assert on the first job's effects. → [13](13-queueable-apex-and-chaining.md)
- **`Test.isRunningTest()` in production code is an anti-pattern** — it makes the tested path different from the shipped path, which is the one thing a test must not do.

**What the Stub API cannot touch:** static methods (including `@future`), private methods, properties (getters *and* setters), triggers, inner classes, system types, `Batchable` implementations, classes whose only constructor is private, and iterators as a parameter or return type. Between them these rule out most utility classes, so a class has to be designed for stubbing — interface or `virtual`, injected rather than instantiated inline.

```apex
public class QuoteProvider implements System.StubProvider {
    public Object handleMethodCall(Object stub, String method, Type returnType,
                                   List<Type> pTypes, List<String> pNames, List<Object> args) {
        return method == 'getRate' ? 0.15 : null;        // String match — a rename breaks this
    }
}
// PricingService fake = (PricingService) Test.createStub(PricingService.class, new QuoteProvider());
// PricingService must be public virtual or an interface, and in the same namespace.
```

## 2026 currency

**Apex Integration Tests are Developer Preview at 67.0, and they are narrower than the name suggests** — the feature is *Apex Integration Tests for Agentforce and Data 360 Services*, scratch orgs only, enabled with the `ApexIntegrationTests` scratch org feature. `@IntegrationTest` allows **live callouts** and `IntegrationTest.commitTestOnly()` commits data mid-transaction, with a `@TearDown` method for cleanup; they run asynchronously through the Tooling API. The reason it exists is exactly the limitation above: mocking every callout and rolling back all data makes it impossible to assert on a real Agentforce or Data 360 round trip. Separately, **Unified Logic Testing is Beta** — `sf logic run test --test-level RunLocalTests --test-category Apex --test-category Flow` runs both suites in one request, which matters once invocable Apex is the seam between them. → [22](22-invocable-apex-and-agentforce-actions.md), [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **`handleMethodCall` dispatches on a `String` method name.** Renaming the real method leaves the stub compiling and returning `null` for the branch that no longer matches.
- **You cannot stub what you cannot subclass.** A `public with sharing class` with only static methods is untestable through the Stub API — the fix is a design change, not a test trick.
- **Properties are not stubbable**, only methods. A dependency exposing `public Decimal rate { get; set; }` has to become `getRate()` before a stub can intervene.
- **A mock registered with `Test.setMock` applies to every callout in the test**, so a method making two different calls needs the mock to branch on `request.getEndpoint()`.
- **`Test.stopTest()` runs one level of a Queueable chain.** Asserting on the third link's side effects will pass for the wrong reason or not at all.
- **A stub does not enforce sharing or user mode differently** — it replaces the implementation entirely, so security assertions belong on the real class under `System.runAs`. → [20](20-apex-testing-fundamentals.md)
- **Integration tests are not a general escape from mocking.** Developer Preview means no production orgs and no upgrade guarantees.

## Recall

Q: When would you reach for the Stub API instead of `HttpCalloutMock`?
A: When the thing to replace is a dependency *object* rather than an HTTP response — an expensive, non-deterministic or out-of-scope collaborator.

Q: Name three things the Stub API cannot mock.
A: Any three of: static methods, private methods, properties, triggers, inner classes, system types, `Batchable` classes, classes with only a private constructor.

Q: What are the six parameters of `handleMethodCall`?
A: The stubbed object, the method name as a `String`, the return `Type`, the parameter types, the parameter names, and the runtime arguments.

Q: How do you assert on asynchronous work in a test?
A: Call `Test.stopTest()` to flush the queue, then assert. Only one level of a Queueable chain runs.

Q: What are Apex Integration Tests at 67.0, and what is the catch?
A: Developer Preview, Agentforce and Data 360 only, scratch orgs only — `@IntegrationTest` permits live callouts and `IntegrationTest.commitTestOnly()`, with `@TearDown` for cleanup.

## Related

- [20 · Apex testing fundamentals](20-apex-testing-fundamentals.md) — isolation, `@TestSetup` and the limit resets these tests still obey
- [19 · Callouts, Named Credentials & HTTP](19-callouts-named-credentials-and-http-in-apex.md) — the real callout a mock stands in for
- [22 · Invocable Apex & Agentforce actions](22-invocable-apex-and-agentforce-actions.md) — the seam Unified Logic Testing exists to cover
