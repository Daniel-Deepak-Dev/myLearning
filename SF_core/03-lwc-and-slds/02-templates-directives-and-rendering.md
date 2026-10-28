---
vault: SF_core
area: 03-lwc-and-slds
format: dense
status: learning
created: 2026-08-02
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 5
tags: [currency-warning]
---
# Templates, Directives & Rendering

**Scope:** What the HTML file can express — conditionals, iteration, expressions — and what it deliberately cannot. Composition directives are [03](03-composition-slots-and-dynamic-components.md); the hooks around a render are [01](01-component-model-and-lifecycle.md).

> **What changed.** Conditionals are **`lwc:if` / `lwc:elseif` / `lwc:else`**, added in **Spring '23**. `if:true` and `if:false` still function and have no announced removal date, but they are no longer recommended and Salesforce intends to remove them — and they evaluate the bound getter **twice** per instance where the new directives evaluate it once.

## Core idea

An LWC template was designed to be underpowered. Below `apiVersion` 66.0 there is no expression language beyond property access, no method calls in the markup, no inline JavaScript — the framework's position is that anything more complicated belongs in a getter, where it can be named and tested. That constraint is the reason most LWC codebases are readable and also the reason nearly every tutorial you find is out of date: the conditional syntax changed in Spring '23, and the *reason* it changed is not cosmetic. `if:true={x}` and `if:false={x}` are two independent bindings, so the getter behind them runs twice per render; `lwc:if`/`lwc:elseif`/`lwc:else` form one chained directive evaluated once. A getter with a side effect or a cost behaves differently under the two.

## How it works

| Directive | Purpose |
|---|---|
| `lwc:if` / `lwc:elseif={p}` / `lwc:else` | chained conditional — must be **immediately adjacent** siblings |
| `for:each={list}` + `for:item="row"` | iteration; requires `key` on the first child element |
| `iterator:it={list}` | iteration exposing `it.value`, `it.index`, `it.first`, `it.last` |
| `key={row.id}` | identity for reconciliation — **not** the loop index |
| `lwc:preserve-comments` | keeps HTML comments in the rendered output |

- **`lwc:elseif` and `lwc:else` must directly follow their sibling.** Whitespace is fine; any element between them is a compile error.
- **`key` must be a stable, unique primitive from your data.** Using the index defeats reconciliation entirely — the framework can no longer tell a reorder from an edit, and component state attaches to the wrong row.
- **Below `apiVersion` 66.0, expressions are property access only.** `{order.total}` is legal; `{order.total * 1.2}`, `{getTotal()}` and `{a && b}` are not. Compute in a getter and bind the getter. At 66.0+ complex template expressions lift this — see below.
- **Event handlers bind by name**: `onclick={handleSave}` — no parentheses, no arguments. Pass data through `data-*` attributes and read `event.target.dataset`.
- **Rendering is batched.** Several mutations in the same tick produce one render pass, so do not reason about the DOM between two assignments.

```html
<template>
    <template lwc:if={hasOrders}>
        <template for:each={orders} for:item="order">
            <li key={order.id}                          <!-- stable id, never the index -->
                data-id={order.id} onclick={handleSelect}>{order.name}</li>
        </template>
    </template>
    <template lwc:elseif={isLoading}><lightning-spinner></lightning-spinner></template>
    <template lwc:else><p>No orders.</p></template>
</template>
```

## 2026 currency

**Complex Template Expressions went GA in Winter '27 (API 68.0)**, after Beta from Spring '26 — so the old *"Do not use … in production"* warning no longer applies. A component with `apiVersion` **66.0 or later** can use a subset of JavaScript inside `{}` — ternaries, optional chaining, comparisons, arrow-function handlers — which removes a great deal of getter boilerplate. Not allowed: `this`, `new`, function declarations, block-bodied arrow functions, assignment outside an arrow function, comments. **Attribute expressions must be quoted** — `class="{…}"` — or you get a compile or runtime error. Expressions re-run on every render, so repeated or array-heavy logic still belongs in a getter. Separately at 67.0, native `<details>` elements support grouping through the `name` attribute, which makes a single-open accordion a zero-JavaScript construct. → [RELEASE-RADAR/developer-tooling-and-apis.md](../../RELEASE-RADAR/developer-tooling-and-apis.md)

## Gotchas

- **Below `apiVersion` 66.0, `lwc:if` binds a property, not an expression.** `lwc:if={!isReady}` does not work — there is no negation operator. Add an `isNotReady` getter.
- **A falsy check is JavaScript-falsy.** `0`, `''` and `NaN` all render the `lwc:else` branch, which quietly hides legitimate zero values.
- **`key` on the wrong element is a compile error**, and `key` on the *iterated* element rather than the first child inside the template is the usual mistake.
- **`for:item` scoping is per-template.** Nested loops need distinct item names or the inner one shadows the outer.
- **Getters run on every render.** An expensive getter behind a frequently-rendered conditional is a real cost, and it is invisible in the template. → [16 · Performance](16-lwc-performance-and-debugging.md)
- **`data-*` attributes stringify.** A numeric id read back from `dataset` is a `String`, so `===` against a number fails.
- **`event.target` inside a loop may not be the element you bound.** Use `event.currentTarget` when the handler needs the element that carries the `data-*`.
- **Mixing `lwc:if` and the old `if:true` in one template compiles** but makes the evaluation-count difference invisible to whoever reads it next.

## Recall

Q: What replaced `if:true` / `if:false`, and in which release?
A: `lwc:if` / `lwc:elseif` / `lwc:else`, in Spring '23. The old directives still work but are no longer recommended.

Q: What is the concrete technical difference, beyond syntax?
A: `if:true` and `if:false` are separate bindings that each evaluate the getter, so it runs twice; the `lwc:if` chain evaluates it once per instance.

Q: Why must `key` never be the loop index?
A: Reconciliation uses it to identify rows across renders. With an index, a reorder is indistinguishable from an edit and component state attaches to the wrong item.

Q: Can you write `{item.price * quantity}` in a template?
A: Below `apiVersion` 66.0, no — bindings are property access only, so compute it in a getter. At 66.0+ a complex template expression allows it.

Q: What is the status of complex template expressions?
A: GA since Winter '27 (API 68.0), after Beta from Spring '26. They need component `apiVersion` 66.0 or later, and an expression in an attribute must be quoted.

## Related

- [01 · Component model & lifecycle](01-component-model-and-lifecycle.md) — when the render this template produces actually happens
- [05 · Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) — what makes a bound property re-render
- [03 · Composition, slots & dynamic components](03-composition-slots-and-dynamic-components.md) — the directives that place *components* rather than markup

## Sources

- [The Salesforce Developer's Guide to the Winter '27 Release](https://developer.salesforce.com/blogs/2026/10/developers-guide-to-the-winter-27-release) — Salesforce Developers · via search 2026-10-28 · two LWC features GA in Winter '27: complex template expressions and `lwc:external`; `apiVersion` 66.0+; no `this`, `new` or function declarations; quoted attribute expressions
- [Salesforce Winter '27 Release Notes](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.salesforce_release_notes.htm&release=264&type=5) — Salesforce Help · via search 2026-10-28 · the Lightning Components section lists complex template expressions as generally available
- [Template Expressions: Considerations and Limitations](https://developer.salesforce.com/docs/platform/lwc/guide/create-components-html-expressions-considerations.html) — Salesforce Developers · via search 2026-10-28 · the disallowed constructs; unquoted attribute expressions cause compile or runtime errors; re-evaluation on every render

## History

- 2026-10-28 · Winter '27 currency check: complex template expressions moved from Beta to GA; property-access-only rules scoped to `apiVersion` below 66.0
