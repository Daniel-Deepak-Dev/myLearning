---
vault: SF_core
area: 02-apex-and-triggers
format: dense
status: learning
created: 2026-08-02
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 5
---
# Apex Testing Advanced & Mocking

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

**Apex Integration Tests arrived as Developer Preview at 67.0 and are still Developer Preview at 68.0** — scratch orgs only, enabled with the `ApexIntegrationTests` scratch org feature, never in production, sandboxes or deployments. At 67.0 they were scoped to Agentforce and Data 360; **Winter '27 widened them to real HTTP endpoints** and added `@BeforeClass` for shared setup data. `@IntegrationTest` allows **live callouts** and `IntegrationTest.commitTestOnly()` commits data mid-transaction, with a `@TearDown` method for cleanup; they run asynchronously, one per org at a time, under async limits, and earn no coverage. A registered `HttpCalloutMock` still wins over the real endpoint. The reason it exists is exactly the limitation above: mocking every callout and rolling back all data makes it impossible to assert on a real round trip. Separately, **Unified Logic Testing is Beta** — `sf logic run test --test-level RunLocalTests --test-category Apex --test-category Flow` runs both suites in one request, which matters once invocable Apex is the seam between them. → [22](22-invocable-apex-and-agentforce-actions.md), [RELEASE-RADAR/developer-tooling-and-apis.md](../../RELEASE-RADAR/developer-tooling-and-apis.md)

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

Q: What are Apex Integration Tests at 68.0, and what is the catch?
A: Still Developer Preview and scratch orgs only. Since Winter '27 they reach real HTTP endpoints as well as Agentforce and Data 360. `@IntegrationTest` permits live callouts and `IntegrationTest.commitTestOnly()`, with `@BeforeClass` for setup and `@TearDown` for cleanup.

## Related

- [28 · Dependency injection & pluggable Apex](28-dependency-injection-and-pluggable-apex.md) — the design change the restriction list above forces: a class that instantiates collaborators inline exposes no seam the Stub API can reach

- [20 · Apex testing fundamentals](20-apex-testing-fundamentals.md) — isolation, `@TestSetup` and the limit resets these tests still obey
- [19 · Callouts, Named Credentials & HTTP](19-callouts-named-credentials-and-http-in-apex.md) — the real callout a mock stands in for
- [22 · Invocable Apex & Agentforce actions](22-invocable-apex-and-agentforce-actions.md) — the seam Unified Logic Testing exists to cover
- [26 · Testing platform events & CDC](26-testing-platform-events-and-cdc.md) — `Test.getEventBus().deliver()` and stepping through a retry sequence

## Sources

- [Apex Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_apex_developer_guide.pdf) — Salesforce Developers · read 2026-10-28 · Apex Integration Tests (Developer Preview): *"real interactions between your Salesforce org and external services, including Agentforce and Data 360, as well as HTTP endpoints"*; `@BeforeClass` (Developer Preview); scratch orgs only, *"aren't available in production orgs, sandboxes, or during metadata deployments"*; one test per org at a time; async limits; no coverage; a registered `HttpCalloutMock` takes precedence
- [Test External Services and HTTP Callouts in Apex Integration Tests (Developer Preview)](https://help.salesforce.com/s/articleView?id=release-notes.rn_apex_integration_tests.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-28 · Winter '27 release note: real HTTP endpoints without mocks; new `@BeforeClass`
- [The Salesforce Developer's Guide to the Winter '27 Release](https://developer.salesforce.com/blogs/2026/10/developers-guide-to-the-winter-27-release) — Salesforce Developers Blog · via search 2026-10-28 · lists Apex integration tests as Developer Preview in Winter '27

## History

- 2026-10-28 · Winter '27 currency check: Integration Tests still Developer Preview at 68.0 but no longer Agentforce/Data 360 only — real HTTP endpoints and `@BeforeClass` added; Recall answer updated
