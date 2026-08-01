# Invocable Apex & Agentforce Actions

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 05

**Scope:** The `@InvocableMethod` contract as Apex — signature rules, bulk semantics, and the constructor requirement that breaks existing actions. The *agent* side (writing descriptions, action selection, MCP exposure) lives in [AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) and is not repeated here.

## Core idea

`@InvocableMethod` is how Apex offers itself to callers that cannot write Apex — Flow, the REST Actions API, Agentforce, and a hosted MCP server. One annotation turns a static method into a declarative building block, which is why it has become the standard seam between code and everything else on the platform. The contract is deliberately rigid, and every part of that rigidity is about the caller being a *bulk* caller: the input is a list, the output is a list, and the platform expects them to correspond. The two things that catch people out are both structural — the method's shape is constrained far more than an ordinary Apex method, and the *input class* has an instantiation requirement that Apex itself never imposes.

## How it works

| Rule | Detail |
|---|---|
| Per class | **Exactly one** `@InvocableMethod` — and the class must be an **outer** class |
| Modifiers | `static` and `public` or `global` |
| Parameters | **At most one**, and it must be a `List<>` |
| Return | a `List<>`, or `void` |
| Companion annotations | only `@Deprecated` may be combined with it |
| Input class | needs a **visible no-argument constructor** |

- **Supported payload types** are narrower than Apex generally: a list of a primitive, of an sObject, of the generic `List<sObject>`, or of a **user-defined type whose fields carry `@InvocableVariable`** — plus lists of lists of those. → [23](23-userdefinedtype-and-typed-interop.md)
- **Bulk is the contract, not an optimisation.** Flow may hand you many rows in one call. The returned list must align with the input list by size and order, so a method that returns a single-element list for a 200-element input silently mismaps results.
- **`@InvocableVariable(label='' description='' required=true)`** exposes a field. Only `public` and `global` fields can carry it.
- **The descriptions are the API.** For an agent, `description` is what the reasoning engine reads to decide whether to call the action at all — treat it as prompt text, not documentation. → [AI_Data · custom agent actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md)

```apex
public with sharing class IssueRefund {                  // outer class, one invocable
    public class Input {
        public Input() {}                                // REQUIRED — see below
        @InvocableVariable(label='Order ID' required=true) public Id orderId;
    }
    public class Output { @InvocableVariable public Boolean refunded; }

    @InvocableMethod(label='Issue Refund' description='Refunds a paid order. Not for exchanges.')
    public static List<Output> run(List<Input> inputs) {  // list in, list out, same order
        List<Output> results = new List<Output>();
        for (Input i : inputs) { results.add(refundOne(i.orderId)); }
        return results;
    }
}
```

## 2026 currency

**The no-argument constructor requirement starts at API 66.0, and the Release Update auto-enforces it in Summer '26** — worth stating precisely, because it is widely written up as a 67.0 change. Any custom Apex type used as an invocable action parameter must expose a visible no-arg constructor: `public` outside a managed package, **`global`** when the class is invoked from outside its own package. The trap is plain object-oriented behaviour meeting a platform assumption — *declaring any constructor with arguments removes the compiler-generated default one*, so a class that has worked for years starts failing to instantiate the moment the platform stops guessing what to pass it. Symptom: a runtime failure in Flow or an agent action, not a compile error. Also GA at 67.0: invocable actions gained **custom property editors, definable picklists and custom headers** in the Flow action configuration UI. → [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md)

> **From my notes.** The old `Apex Invocable method in Flow` page has four correct bullets and puts everything else in an embedded video that no longer resolves — so it is structure only. The one thing it never said is the thing that matters now: **the input class is instantiated by the platform, not by you.**

## Gotchas

- **Adding a parameterised constructor to an existing input class breaks it.** There is no compile-time warning; the action fails at runtime. Add `public Input() {}` back explicitly.
- **`global` is required for cross-package invocation**, and `public` is not a near-enough substitute — a managed-package action called from a subscriber org needs the global form.
- **One invocable per class** means a service with three operations needs three classes, or one class with a mode variable — the latter usually reads worse to an agent.
- **Inner classes are fine for the payload, not for the method.** The annotated method's class must be an outer class.
- **The method runs in user mode at 67.0** like everything else, so an action that worked for an admin can return partial data for an agent's running user. → [10](10-apex-security-user-mode-and-fls.md)
- **`@InvocableVariable` ignores private fields silently** — no error, the variable simply never appears in Flow Builder.
- **A `void` invocable returns nothing to the caller**, which for an agent means it has no way to confirm the work happened. Return a status structure instead.

## Recall

Q: What are the four hard signature rules for an `@InvocableMethod`?
A: One per class, on an outer class; `static` and `public`/`global`; at most one parameter and it must be a `List<>`; the return must be a `List<>` or `void`.

Q: From which API version must invocable input classes have a visible no-arg constructor, and when is it enforced?
A: API 66.0 onward, with the Release Update auto-activating in Summer '26. `public` normally, `global` for cross-package calls.

Q: Why does an input class that has worked for years suddenly fail?
A: Someone added a constructor with arguments, which removed the compiler-generated no-arg constructor the platform now needs to instantiate it.

Q: What does the returned list have to guarantee?
A: Alignment with the input list by size and order — Flow calls in bulk and maps results positionally.

Q: Which part of an invocable action does an Agentforce agent actually read when deciding to call it?
A: The `label` and `description` on the method and its `@InvocableVariable` fields — not the code.

## Related

- [23 · `UserDefinedType` & typed interop](23-userdefinedtype-and-typed-interop.md) — what a typed payload can legally contain
- [10 · Apex security: user mode & FLS](10-apex-security-user-mode-and-fls.md) — the running-user semantics an action inherits at 67.0
- [AI_Data · custom agent actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) — description writing, action selection and exposure as an MCP tool
