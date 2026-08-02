# Templates, Directives & Rendering

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 05

**Scope:** What the HTML file can express — conditionals, iteration, expressions — and what it deliberately cannot. Composition directives are [03](03-composition-slots-and-dynamic-components.md); the hooks around a render are [01](01-component-model-and-lifecycle.md).

> **What changed.** Conditionals are **`lwc:if` / `lwc:elseif` / `lwc:else`**, added in **Spring '23**. `if:true` and `if:false` still function and have no announced removal date, but they are no longer recommended and Salesforce intends to remove them — and they evaluate the bound getter **twice** per instance where the new directives evaluate it once.

## Core idea

An LWC template is intentionally underpowered. There is no expression language beyond property access, no method calls in the markup, no inline JavaScript — the framework's position is that anything more complicated belongs in a getter, where it can be named and tested. That constraint is the reason most LWC codebases are readable and also the reason nearly every tutorial you find is out of date: the conditional syntax changed in Spring '23, and the *reason* it changed is not cosmetic. `if:true={x}` and `if:false={x}` are two independent bindings, so the getter behind them runs twice per render; `lwc:if`/`lwc:elseif`/`lwc:else` form one chained directive evaluated once. A getter with a side effect or a cost behaves differently under the two.

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
- **Expressions are property access only.** `{order.total}` is legal; `{order.total * 1.2}`, `{getTotal()}` and `{a && b}` are not. Compute in a getter and bind the getter.
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

**Complex Template Expressions are Beta and explicitly not for production.** Setting a component's `apiVersion` to **66.0 or later** unlocks a substantial subset of JavaScript inside `{}` — ternaries, optional chaining, comparisons, inline handlers — which removes a great deal of getter boilerplate and is being written up widely as though it had shipped. The documentation's own wording is *"Do not use complex template expressions in production"*, and Beta Services Terms apply, so the honest position for now is: know it exists, know the apiVersion gate, keep the getters. Separately at 67.0, native `<details>` elements support grouping through the `name` attribute, which makes a single-open accordion a zero-JavaScript construct. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **`lwc:if` binds a property, not an expression.** `lwc:if={!isReady}` does not work — there is no negation operator. Add an `isNotReady` getter.
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
A: No — bindings are property access only. Compute it in a getter.

Q: What is the status of complex template expressions?
A: Beta, gated on component `apiVersion` 66.0 or later, and documented as not for production use.

## Related

- [01 · Component model & lifecycle](01-component-model-and-lifecycle.md) — when the render this template produces actually happens
- [05 · Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) — what makes a bound property re-render
- [03 · Composition, slots & dynamic components](03-composition-slots-and-dynamic-components.md) — the directives that place *components* rather than markup
