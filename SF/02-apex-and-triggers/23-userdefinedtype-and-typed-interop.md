# `UserDefinedType` & Typed Interop

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 05

**Scope:** Carrying a structured payload across a boundary — Apex ↔ Flow, Apex ↔ agent action, Apex ↔ LWC — and the equality contract a custom type owes its collections. The invocable signature rules are [22](22-invocable-apex-and-agentforce-actions.md).

## Core idea

**There is no `System.UserDefinedType` interface.** The title is the phrase the Apex docs use, not a type you implement: *"a list of a user-defined type, containing variables of the supported types"* — meaning an ordinary Apex class you wrote, annotated so a non-Apex caller can see inside it. Worth stating plainly, because the name reads like `Comparable` or `Callable` and sends people looking for an interface that does not exist. What does exist is three separate, unrelated mechanisms that all get called "typed interop", each with its own annotation and its own failure mode: `@InvocableVariable` for Flow and agent actions, `@AuraEnabled` for LWC and Flow variables, and `equals`/`hashCode` for collections. Getting a payload across the platform usually means satisfying two of the three at once.

## How it works

| Surface | Annotation / method | Who instantiates it |
|---|---|---|
| Flow action, agent action, Actions API | `@InvocableVariable` on `public`/`global` fields | **the platform** — hence the no-arg constructor rule |
| Flow *variable* (Apex-Defined Type), LWC payload | `@AuraEnabled` on fields | the platform, from JSON |
| Map key or set element | `public Boolean equals(Object)` + `public Integer hashCode()` | you |

- **An Apex-Defined Type (ADT) is a class with `@AuraEnabled` members** used as a Flow variable's data type. It is how a Flow holds a shape that has no custom object behind it — fields drawn from two objects, or a parsed API response.
- **The same class often needs both annotations.** `@InvocableVariable` makes a field visible to an *action*; `@AuraEnabled` makes it visible to a Flow *variable* and to LWC. They are not interchangeable and neither implies the other.
- **Collections do not use your fields unless you tell them to.** Two instances with identical values are different keys until the class implements both `equals` and `hashCode` — Apex uses them together to decide identity and uniqueness.
- **Serialization is the common denominator.** All three surfaces move the object as data, so anything non-serializable — an open `Database.QueryLocator`, an `HttpResponse` — cannot ride along.

```apex
public class RefundLine {
    public RefundLine() {}                                     // API 66.0 rule → 22
    @InvocableVariable @AuraEnabled public Id orderId;         // action AND Flow/LWC
    @AuraEnabled public Decimal amount;                        // Flow/LWC only

    public Boolean equals(Object o) {                          // without this pair,
        return o instanceof RefundLine                         // two identical lines are
            && ((RefundLine) o).orderId == this.orderId;       // two distinct map keys
    }
    public Integer hashCode() { return orderId == null ? 0 : orderId.hashCode(); }
}
```

## 2026 currency

Two changes worth knowing, neither of them a new type system. **The no-arg constructor rule (API 66.0, Release Update enforced Summer '26) applies to the invocable half of this note** and is the most likely reason a typed payload that worked last year fails now — the platform instantiates your class, so it needs a constructor to call. → [22](22-invocable-apex-and-agentforce-actions.md). Separately, **Flow Data Tables render Apex-Defined Types as of Winter '26**, not just sObjects, which removes the standard workaround of mapping an ADT onto a throwaway custom object purely to display it. Nothing here is a Summer '26 addition: ADTs, `@InvocableVariable` and the `equals`/`hashCode` contract are all long-standing, and their currency risk is the constructor rule rather than the mechanisms themselves. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **Mutating an object after adding it to a map or set makes it unfindable.** The hash was computed at insertion; changing a field the hash depends on strands the entry — it is still in the collection and no lookup will ever return it.
- **Implementing `equals` without `hashCode` is worse than implementing neither.** `==` starts agreeing while map and set lookups keep missing, which produces a bug that reads as random.
- **`@AuraEnabled` and `@InvocableVariable` solve different problems.** A field with only `@AuraEnabled` is invisible in an action's input; a field with only `@InvocableVariable` is invisible to LWC.
- **Private fields are silently skipped** by both annotations — no compile error, the field just never appears.
- **An ADT is matched by shape, not identity, across a subflow boundary.** Renaming a field breaks the binding at runtime with an unhelpful message.
- **Nested types multiply the constructor rule.** A payload class holding another custom class needs the no-arg constructor on *both*.
- **`Id` fields do not round-trip as `String`.** A Flow that writes text into an `Id`-typed `@InvocableVariable` fails on assignment, not on entry.

## Recall

Q: What is `UserDefinedType` in Salesforce Apex?
A: A phrase from the docs for an ordinary Apex class used as a typed payload — not an interface. Nothing implements it.

Q: Which annotation exposes a field to a Flow *action*, and which to a Flow *variable* or LWC?
A: `@InvocableVariable` for the action; `@AuraEnabled` for the Apex-Defined Type used as a variable or LWC payload. A field often needs both.

Q: What must a class implement to work as a map key or set element?
A: `public Boolean equals(Object)` and `public Integer hashCode()` — both, or lookups misbehave.

Q: Why can an object disappear from a set it is demonstrably still in?
A: Its hash was computed on insertion; mutating a field the hash depends on means no lookup can locate it again.

Q: What did Winter '26 change for Apex-Defined Types?
A: Flow Data Tables can render them, not only sObjects — removing the throwaway-custom-object workaround.

## Related

- [22 · Invocable Apex & Agentforce actions](22-invocable-apex-and-agentforce-actions.md) — the signature the typed payload plugs into, and the constructor rule
- [01 · Apex language core & governor limits](01-apex-language-core-and-governor-limits.md) — collection semantics these types have to satisfy
- [AI_Data · custom agent actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) — why a typed return beats prose for an agent, and Custom Lightning Types
