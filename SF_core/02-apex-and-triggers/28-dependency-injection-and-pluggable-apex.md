# Dependency Injection & Pluggable Apex

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 21

**Scope:** Getting collaborators *into* a class rather than letting it build its own — interfaces, factories, `Type.forName()` and custom metadata binding. What you do with the seam in tests is [21](21-apex-testing-advanced-and-mocking.md); the layered architecture it serves is [27](27-apex-enterprise-patterns-and-layered-design.md).

## Core idea

Apex has no DI container and no annotation that wires anything. Injection here means one plain discipline: **a class declares what it needs as an interface and receives it, instead of writing `new` in the middle of its own logic.** The reason this is not a style preference is [21](21-apex-testing-advanced-and-mocking.md) — the Stub API cannot stub static methods, private methods, properties, inner classes, `Batchable` implementations, or classes whose only constructor is private. A class that instantiates its collaborators inline exposes no seam the Stub API can reach, so it is **untestable by construction**, and no amount of test writing fixes it afterwards. Injection is the design decision that makes mocking possible at all. The second payoff arrives later: once the dependency is named rather than hard-coded, it can be chosen at runtime from configuration.

## How it works

- **Constructor injection is the default form.** Take the interface as a parameter, keep a `private final` field, and provide a no-arg constructor that supplies the real implementation so ordinary callers are unaffected.
- **A factory centralises the choice.** One class decides which implementation each interface gets, and tests override it. This is exactly what fflib's `Application` class is → [27](27-apex-enterprise-patterns-and-layered-design.md).
- **`Type.forName()` turns a string into a class**, which is what lets the choice live outside the code:

```apex
public interface TaxCalculator { Decimal calculate(Decimal amount); }

public class InvoiceService {
    private final TaxCalculator calc;
    public InvoiceService() { this(TaxFactory.get()); }        // production path
    public InvoiceService(TaxCalculator calc) { this.calc = calc; }  // the test seam
}

// TaxFactory.get(), reading the implementation name from custom metadata:
Tax_Setting__mdt s = Tax_Setting__mdt.getInstance('Default');
Type t = Type.forName(s.Implementation_Class__c);
return (TaxCalculator) t.newInstance();
```

- **Custom metadata binding is the idiomatic Salesforce answer** to "different implementation per org". The class name is a CMDT field, so a managed package or a per-region org swaps behaviour with a deploy of *data*, not code — and CMDT costs no SOQL query → [01-admin · 09](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md).
- **`System.Callable` is the cross-package seam.** A single `call(String action, Map<String, Object> args)` method lets one package invoke another it cannot compile against. Loose to the point of untyped — reach for it at package boundaries, not inside one codebase.

## 2026 currency

Nothing about injection itself changed at 67.0, but the **user-mode default changes what a swapped implementation can quietly do**. An implementation class named in custom metadata is chosen at runtime and inherits the sharing behaviour of its own declaration — and a keyword-less class now defaults to `with sharing`. So a pluggable implementation written before 2026 and assumed to run elevated will silently return fewer rows rather than throwing. The class name in a CMDT row is effectively a security-relevant setting: it decides which code runs, and nothing about the record tells a reviewer that. → [10](10-apex-security-user-mode-and-fls.md), [11](11-sharing-keywords-and-apex-managed-sharing.md)

## Gotchas

- **`Type.forName()` returns `null` for an unknown class — it does not throw.** The failure surfaces as a `NullPointerException` on the following `newInstance()`, pointing at the wrong line.
- **`Type.forName()` is namespace-sensitive.** In a managed package use the two-argument form, `Type.forName(namespace, className)`; the one-argument form resolves against the caller's namespace and fails cross-package.
- **`newInstance()` requires a public, visible, no-argument constructor** — the same rule that bites invocable classes at API 66.0, from the same cause: declaring any constructor with arguments removes the compiler-generated default → [22](22-invocable-apex-and-agentforce-actions.md).
- **String-based binding fails at runtime, never at compile time.** Renaming or deleting the implementation class deploys cleanly and breaks in production; the CMDT row is a deployable dependency with no compiler protection.
- **A `private final` field assigned in the constructor is the point.** Injecting through a public setter leaves the collaborator swappable after construction, which is a different and worse thing.
- **Interfaces are not free.** One interface per collaborator is worth it; an interface per class is ceremony that makes navigation harder and buys nothing.
- **`System.Callable` discards all type safety** — arguments and return value are `Object`. Use it where compile-time coupling is impossible, not as a general decoupling tool.

## Recall

Q: Why is dependency injection a testing prerequisite in Apex rather than a style choice?
A: The Stub API cannot stub static or private methods, properties, inner classes, `Batchable` classes or private-constructor-only classes. A class that writes `new` inline exposes no seam it can reach, so it is untestable by construction.

Q: What does `Type.forName()` do when the class name is wrong?
A: It returns `null` rather than throwing, so the error appears as a `NullPointerException` at the subsequent `newInstance()` call.

Q: How do you make an implementation swappable per org without a code deploy?
A: Store the class name in a custom metadata record and resolve it with `Type.forName().newInstance()`. CMDT is deployable, packageable, and costs no SOQL query.

Q: What constructor does `newInstance()` require?
A: A visible no-argument constructor. Declaring any constructor with arguments removes the compiler-generated default one, and the call then fails at runtime.

Q: When is `System.Callable` the right seam?
A: Across package boundaries, where one package cannot compile against the other. Its single untyped `call(String, Map<String, Object>)` signature is too loose for use inside a single codebase.

## Related

- [21 · Apex testing advanced & mocking](21-apex-testing-advanced-and-mocking.md) — the Stub API restriction list that makes injection mandatory rather than optional
- [27 · Apex Enterprise Patterns & layered design](27-apex-enterprise-patterns-and-layered-design.md) — the Application factory is this pattern applied to four layers at once
- [22 · Invocable Apex & Agentforce actions](22-invocable-apex-and-agentforce-actions.md) — the same no-arg constructor rule, enforced by the platform instead of by your factory
- [01-admin · 09 Custom Metadata vs Custom Settings](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md) — why CMDT is the right store for a binding record
