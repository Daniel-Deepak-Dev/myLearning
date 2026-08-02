# Flow & Apex Interop

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** The seam in both directions — Flow calling Apex, and Apex calling Flow — from the **flow author's** side. The `@InvocableMethod` signature contract itself is [02-apex · 22](../02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md) and is not restated here.

## Core idea

The boundary runs both ways and the two directions are asymmetric enough to be worth separating. **Flow → Apex** is the common one: an `@InvocableMethod` appears in the Action element's palette, takes a list in and hands a list back, and from the flow's point of view it is an ordinary action with typed parameters. **Apex → Flow** is the direction most developers forget exists: `Flow.Interview` starts an autolaunched flow from code, passing a `Map<String, Object>` of inputs and reading outputs back by name. The thing that governs both is **what can cross the boundary**, and the answer is narrower than either language suggests. Flow has no Map type and no notion of an interface; Apex has no equivalent of a flow resource. The types that survive the crossing are primitives, sObjects, collections of those, and Apex classes whose fields are annotated to be visible.

## How it works

| Direction | Mechanism | Notes |
|---|---|---|
| Flow → Apex | `@InvocableMethod` on an Action element | one list in, one list out, **same size and order** |
| Flow → Apex | **Apex-defined variable** | an Apex class with `@AuraEnabled` fields, usable as a flow resource |
| Apex → Flow | `Flow.Interview.createInterview(name, inputs)` | **autolaunched and user-provisioning flows only** |
| Apex → Flow | `Flow.Interview.MyFlowName` | the statically-typed form of the same thing |

- **`@InvocableVariable` carries more than a label.** `required=true`, `defaultValue` and `placeholderText` all shape what the flow author sees, and `description` is what an Agentforce agent reads. → [02-apex · 22](../02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md)
- **Bulk is the contract.** Flow may hand the action many rows in one call, and the returned list must align by size and order. → [09](09-collections-loops-and-the-transform-element.md)
- **`Flow.Interview` outputs come back as `Object`** from `getVariableValue('name')`, and the variable must be flagged *Available for output*. → [02](02-flow-anatomy-and-builder-basics.md)
- **The invocable input class needs a visible no-arg constructor** from API 66.0, enforced by a Release Update in Summer '26. It fails at run time in Flow, never at compile time.
- **An Apex-defined variable is a different annotation from an invocable one** — `@AuraEnabled` for flow resources and LWC, `@InvocableVariable` for action parameters. A class often needs both. → [02-apex · 23](../02-apex-and-triggers/23-userdefinedtype-and-typed-interop.md)

## 2026 currency

Summer '26 reworked the surface a flow author actually touches. Action parameters gained **Formula Mode**, so a value can be computed inline instead of via a formula resource, and **Transform Mode**, so a collection can be reshaped inside the action's property panel rather than in a separate Transform element → [09](09-collections-loops-and-the-transform-element.md). **Apex-defined inputs can now have their fields set directly** in the panel instead of being assembled by an Assignment first. And the *Include* toggle on optional Apex action inputs is gone — **required parameters are marked with a red asterisk** and everything else is simply optional, which removes a genuinely confusing control. None of this changes the Apex side of the contract; it changes how much scaffolding the flow needs around it.

> **From my notes.** A 2025 page on invocable variables ends with one line that is worth more than the sample code above it: *"InvocableVariable fields do not support type of `Map<String,Decimal>`."* True, and true of every map — **Flow has no Map data type at all**, so no `Map<>` crosses the boundary in either direction regardless of its value type. A separate 2023 page on `Flow.Interview` carries the other half: that route works **only for autolaunched and user-provisioning flows**, so Apex cannot start a screen flow or a record-triggered one.

## Gotchas

- **No `Map<>` crosses the boundary, ever.** Not as an invocable variable, not as an Apex-defined field. Use parallel collections or a wrapper class with named fields.
- **`Flow.Interview` cannot start a screen flow**, a record-triggered flow or a scheduled one — autolaunched and user-provisioning only.
- **Adding a constructor with arguments to an invocable input class breaks it at run time**, because it removes the compiler-generated no-arg constructor the platform needs.
- **`@InvocableVariable` ignores private fields silently.** The variable simply never appears in Flow Builder — no error.
- **An invocable action returning a single-element list for a 200-element input mismaps results** rather than failing.
- **`getVariableValue` returns `Object`** and needs casting; a wrong cast is a run-time failure with an unhelpful message.
- **The action runs in user mode at 67.0** like the rest of Apex, so an action that worked for an admin can return partial data for another running user. → [02-apex · 10](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)
- **An invocable action inside a Loop is called once per iteration**, defeating the bulk contract it was designed around.

## Recall

Q: Which flow types can Apex start with `Flow.Interview`?
A: Autolaunched and user-provisioning flows only — not screen, record-triggered or scheduled flows.

Q: Why can't a `Map<String, Decimal>` be an `@InvocableVariable`?
A: Because Flow has no Map data type at all. No map of any value type crosses the boundary in either direction.

Q: Which annotation makes an Apex class usable as a *flow resource*, as opposed to an action parameter?
A: `@AuraEnabled` on its fields. `@InvocableVariable` is for action parameters, and a class often needs both.

Q: What does an invocable action have to guarantee about its return value?
A: Alignment with the input list by size and order — Flow calls in bulk and maps results positionally.

Q: What did Summer '26 change about configuring an Apex action in Flow?
A: Formula Mode and Transform Mode in the property panel, direct field-setting for Apex-defined inputs, and the *Include* toggle replaced by red asterisks on required parameters.

## Related

- [02-apex · 22 Invocable Apex & Agentforce actions](../02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md) — the signature rules and the API 66.0 constructor requirement
- [02-apex · 23 `UserDefinedType` & typed interop](../02-apex-and-triggers/23-userdefinedtype-and-typed-interop.md) — which annotation does what, and why a class often needs two
- [12 · HTTP callout & External Services](12-http-callout-and-external-services-in-flow.md) — the case where Flow no longer needs Apex at all
