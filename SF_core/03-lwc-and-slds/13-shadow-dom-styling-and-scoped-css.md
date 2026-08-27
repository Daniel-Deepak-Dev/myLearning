# Shadow DOM, Styling & Scoped CSS

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 06

**Scope:** The boundary around a component's DOM and CSS — what it blocks, what crosses it, and how the on-platform version differs from the browser's. Which design tokens to set once you know what can reach in is [14](14-slds-2-and-styling-hooks.md).

> **What changed.** On-platform, LWC has always rendered through a **synthetic shadow polyfill**, not the browser's real shadow DOM — so advice written about "shadow DOM" from a web-components blog describes behaviour you may not have. Native shadow is opt-in per component through **Mixed Shadow Mode (still Beta)** via `static shadowSupportMode = 'native'`; the older `'any'` value is **deprecated and superseded by `'native'`**. The two modes differ in what CSS reaches in, what `querySelector` can find, and whether `::part` works at all.

## Core idea

The boundary does two jobs and it is worth separating them, because components fail at one or the other for different reasons. **For CSS**, it stops a parent's styles from reaching a child's internals — which is what makes base components upgradeable, and also what makes "just override the class" fail. **For JavaScript**, it partitions the DOM: `this.template.querySelector` searches your shadow tree, `this.querySelector` searches slotted content that belongs to the parent, and neither is `document.querySelector`. Synthetic shadow approximates all of this with attribute scoping rather than a real boundary, so it is leakier by construction: global stylesheets like SLDS apply inside components, which is convenient and is exactly the leak native shadow closes. That is the migration tension in one sentence — native is faster and correct, and turning it on can restyle a page that was quietly depending on the leak.

## How it works

| Mode | Set by | Behaviour |
|---|---|---|
| Synthetic (default in Lightning Experience) | nothing — it is the default | attribute-scoped, global styles leak in |
| Native | `static shadowSupportMode = 'native'` | real boundary, `::part` works, ~faster |
| Light DOM | `static renderMode = 'light'` + `<template lwc:render-mode="light">` | no boundary at all |

- **`:host` targets the component's own element** and works in both modes — it is where a component sets its own defaults, and where you declare the custom properties it exposes.
- **CSS custom properties cross every boundary, in both modes.** That is not an accident and it is the whole basis of the styling-hook contract in [14](14-slds-2-and-styling-hooks.md): properties inherit, so they are the one supported channel into a component's internals.
- **`::part` only works in native shadow**, and only for elements the child explicitly marked with a `part` attribute. Under synthetic it does nothing, silently — a very common wasted afternoon.
- **A synthetic parent may contain native children; the reverse is not supported.** Migration therefore proceeds leaves-first, which is what makes Mixed Shadow Mode a gradual path rather than a switch.
- **Light DOM is the escape hatch with a cost.** It exists for third-party libraries that need to walk the DOM, for global styling, and for SSR in LWR — and it gives up encapsulation for every consumer of the component, permanently.

```css
/* the component's own stylesheet — scoped automatically, no BEM prefixing needed */
:host {
    --my-panel-accent: var(--slds-g-color-accent-container-1, #0176d3);  /* inheritable in */
    display: block;
}
:host(.compact) .row { padding: 0; }        /* :host() filters on the host's own classes */
.row { border-left: 3px solid var(--my-panel-accent); }
```

## 2026 currency

Mixed Shadow Mode has been **Beta for several releases and is still Beta at 67.0**, which is the honest headline: Salesforce has stated the intent to migrate off the synthetic polyfill and eventually remove it — removing it would roughly halve LWC's JavaScript payload, and native components already benchmark meaningfully faster — but that migration is not finished and native is not the platform default. What this means practically is that a component authored today should be written so it *would* survive native shadow: no reliance on global stylesheet leakage, no `document.querySelector` into another component, styling exposed as custom properties rather than overridable classes. LWR server-side rendering is the one place the choice is already forced — **synthetic shadow is not supported there**, so SSR components use native shadow or light DOM. → [05-experience · LWR](../05-experience-cloud-lwr/INDEX.md)

## Gotchas

- **`this.template.querySelector` in the constructor returns `null`.** There is no rendered DOM yet. → [01](01-component-model-and-lifecycle.md)
- **`this.querySelector` and `this.template.querySelector` search different trees** — slotted content belongs to the parent, so it is the former.
- **`::part` under synthetic shadow fails silently.** No error, no style, and no clue in devtools that the mode is why.
- **Turning on native shadow can restyle the component** wherever it was inheriting from a global stylesheet it never declared a dependency on.
- **`shadowSupportMode = 'any'` is deprecated** — use `'native'`. Existing code with `'any'` still works and is not a good example to copy.
- **Styles injected into markup you built by hand are not scoped** unless the container carries `lwc:dom="manual"`.
- **Light DOM is not reversible in practice.** Consumers style its internals, and taking encapsulation back breaks them.
- **You cannot style a base component's internals from outside**, in either mode. If there is no styling hook for it, that is the answer, not a challenge. → [14](14-slds-2-and-styling-hooks.md)

## Recall

Q: What renders LWC in Lightning Experience by default, and why does it matter?
A: A synthetic shadow polyfill, not native shadow DOM. It is attribute-scoped and leakier — global stylesheets reach inside components.

Q: How do you opt a component into native shadow, and what is the deprecated form?
A: `static shadowSupportMode = 'native'` under Mixed Shadow Mode (Beta). The older `'any'` value is deprecated.

Q: Which direction does mixed-mode nesting work?
A: A synthetic parent can contain native children; a native parent cannot contain synthetic children — so migration goes leaves-first.

Q: What is the one thing that crosses the shadow boundary in both modes?
A: CSS custom properties. They inherit, which is why styling hooks are the supported customization channel.

Q: Where does `::part` work?
A: Native shadow only, and only on elements the child marked with a `part` attribute. Under synthetic it does nothing.

## Related

- [14 · SLDS 2 & styling hooks](14-slds-2-and-styling-hooks.md) — the custom properties that are meant to cross this boundary
- [03 · Composition, slots & dynamic components](03-composition-slots-and-dynamic-components.md) — slotted content stays in the parent's scope, which is why parent CSS reaches it
- [01 · Component model & lifecycle](01-component-model-and-lifecycle.md) — when the shadow tree exists and `querySelector` becomes safe
