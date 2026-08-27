# Reactive Screen Flows

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** Making one screen recalculate without a Next click — **reactive components** and **Screen Actions**, which are two different mechanisms people conflate. Screen composition is [04](04-screen-flows-and-ux-design.md).

## Core idea

Reactivity is the capability that changed screen-flow design most, and it arrived in two halves that solve different problems. **Reactive components** let one component on a screen read another's current value — a picklist filters a Data Table, a formula recomputes a total — all client-side, with no server round trip and no navigation. That covers everything you can *calculate* from what is already on screen. It does not cover anything you have to *fetch*, which is why the second half exists: **Screen Actions** run an autolaunched flow from a screen while the user is still on it, so a search box can query records, a callout can validate an address, and the results land back on the same screen. Together they close a gap that used to be filled by a screen boundary, and every design pattern that inserts a screen "so the next one can see the value" is now obsolete.

## How it works

| Mechanism | GA | What it does |
|---|---|---|
| **Reactive components** | **Winter '24** (Beta Summer '23) | one component reads another's live value; formulas recompute client-side |
| **Action Buttons** | **Winter '25** | run an autolaunched flow on click, stay on the screen |
| **Screen Actions** | **Summer '25** (Beta Spring '25) | run an autolaunched flow on *change* or on load, no click |

- **Flow API version must be 59.0 or later.** The stopgap setting that back-ported reactivity to API 57.0/58.0 — *Enable Reactive Components for Screen Flows running API Version 57.0 and 58.0* — **expired in Winter '25** and is gone.
- **Every reactive pair has a source and a target.** The source exposes a value; the target binds to it. Types must match, and a formula is the standard way to convert.
- **A Screen Action fires on input change by default.** Since Summer '25 you can also run it on screen load and gate it with filter conditions, which is what makes it usable in practice.
- **A custom LWC is a reactive *source* only if it dispatches `FlowAttributeChangeEvent`.** Assigning to the `@api` property is not enough — same rule as any Flow output. → [03-lwc · 11](../03-lwc-and-slds/11-lwc-in-flow-screens-and-quick-actions.md)
- **Typical uses**: dependent picklists from records, running totals over a Data Table, duplicate detection while typing, address validation via an HTTP callout → [12](12-http-callout-and-external-services-in-flow.md).

## 2026 currency

Reactivity is mature rather than new — the interesting fact is what it retired. Screen Actions completed the arc in Summer '25, and Salesforce's own framing is that it was the last missing piece: reactive components could recalculate but never fetch. Four constraints are still live at 67.0 and none of them is signposted in the builder: **cross-object formulas are not reactive**, **formulas are capped at 3,900 characters**, **a reactive change does not fire validation** on the components it updates, and reactivity is a property of *specific* components rather than all of them, so the supported list has to be checked per component rather than assumed. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **A cross-object formula silently does not react.** It evaluates once and then never updates, which reads as a caching bug and is not one.
- **Reactive updates bypass validation.** A component whose value was set reactively can hold a value its own validation would have rejected.
- **A flow below API 59.0 is simply not reactive**, and the back-port setting that used to rescue it expired in Winter '25.
- **Type mismatch between source and target fails at design time**, not at run time — which is the good case, but it surprises people expecting implicit conversion.
- **A custom LWC that only assigns to its `@api` property is not a reactive source.** It needs `FlowAttributeChangeEvent`, and the attribute name is an unchecked string.
- **Screen Actions run a whole autolaunched flow**, so they spend SOQL and DML from the same transaction budget — on every keystroke-triggered fire if you do not gate them with conditions.
- **Not every stock component is reactive.** Reactivity was rolled out component by component; check the current list rather than assuming.

## Recall

Q: In which release did reactive screen components go GA, and what API version do they require?
A: Winter '24 (Beta in Summer '23), and the flow must run on API version 59.0 or later.

Q: What is the difference between reactive components and Screen Actions?
A: Reactive components recalculate client-side from values already on the screen; Screen Actions run an autolaunched flow to fetch or do something, then return to the same screen.

Q: When did Screen Actions go GA, and what did Summer '25 add?
A: Summer '25, after a Spring '25 beta. Summer '25 added run-on-load and filter conditions controlling when the action fires.

Q: Name two reactivity limits the builder does not warn you about.
A: Cross-object formulas are not reactive, and a reactive change does not fire validation. Formulas are also capped at 3,900 characters.

Q: What must a custom LWC do to act as a reactive source?
A: Dispatch `FlowAttributeChangeEvent` from `lightning/flowSupport`. Assigning to the `@api` property does nothing.

## Related

- [04 · Screen flows & UX design](04-screen-flows-and-ux-design.md) — screen composition, and why fewer screens is now the goal
- [03-lwc · 11 LWC in Flow screens](../03-lwc-and-slds/11-lwc-in-flow-screens-and-quick-actions.md) — the `FlowAttributeChangeEvent` contract on the component side
- [12 · HTTP callout & External Services](12-http-callout-and-external-services-in-flow.md) — what a Screen Action calls when the answer is outside Salesforce
