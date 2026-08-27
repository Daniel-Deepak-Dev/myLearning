# Component Model & Lifecycle

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 05

**Scope:** What a component *is* on disk, and the order the platform calls into it. What the template can express is [02](02-templates-directives-and-rendering.md); what makes it re-render is [05](05-decorators-and-the-reactivity-model.md).

## Core idea

A Lightning web component is a folder whose contents share its name — an HTML template, a JavaScript class extending `LightningElement`, and a `.js-meta.xml` configuration file, with optional CSS and SVG alongside. The class is a standard ES module and the framework is a thin layer over web components, which is the whole design argument: the parts you already know are the parts the platform does not reimplement. What the platform *does* own is the render cycle. You never call `render()`; you mutate a field and the framework decides when to re-render, batching the work. Almost every lifecycle bug traces back to fighting that — reaching for the DOM before it exists, or mutating state in the hook that runs after rendering and re-triggering it.

## How it works

| Hook | Fires | Use it for |
|---|---|---|
| `constructor()` | once, first | field initialisation only — **no DOM, no `@api` values yet** |
| `connectedCallback()` | on insertion, **can repeat** | subscriptions, imperative Apex, reading `@api` props |
| `render()` | before each render | returning a *different* template; rarely overridden |
| `renderedCallback()` | after **every** render | DOM measurement, third-party library init |
| `disconnectedCallback()` | on removal | unsubscribe, clear intervals, remove listeners |
| `errorCallback(error, stack)` | on a descendant's error | error boundaries |

- **Parents and children interleave.** A parent constructs, connects and renders before its children exist; then each child constructs, connects and renders. **Child `renderedCallback` fires before the parent's** — the tree completes bottom-up.
- **The metadata file decides where it can live.** `apiVersion`, `isExposed`, `targets` and `targetConfigs` in `.js-meta.xml` are what make a component available to App Builder, a Flow screen or a quick action.
- **Naming is mechanical.** Folder `myOrderList` → module `c/myOrderList` → markup `<c-my-order-list>`. Camel case becomes kebab case, and the folder name cannot contain a hyphen.
- **`this.template.querySelector` is the escape hatch, not the habit.** For a known element, [03](03-composition-slots-and-dynamic-components.md)'s `lwc:ref` is cheaper and does not break under shadow DOM.

```js
import { LightningElement, api } from 'lwc';
export default class OrderPanel extends LightningElement {
    @api recordId;                       // undefined in the constructor; set before connectedCallback
    #initialised = false;                // guard — renderedCallback runs after EVERY render

    renderedCallback() {
        if (this.#initialised) return;
        this.#initialised = true;
        this.refs?.chart && this.drawChart();
    }
    disconnectedCallback() { this.subscription?.unsubscribe(); }
}
```

## 2026 currency

**LWC Component Preview is GA at 67.0** — a single component renders in the browser or in VS Code without a full page reload, which changes the lifecycle debugging loop from *deploy, navigate, refresh* to something closer to a normal front-end workflow. 67.0 also makes hot module reloading faster and more memory-efficient, and the VS Code extension has been renamed from *Local Dev* to *Live Preview*. The install and CLI side of that belongs to [21 · Local dev & Lightning Dev Server](21-local-dev-and-lightning-dev-server.md); this note only cares that previewing a component in isolation is now a supported way to watch its hooks fire. Release context: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

## Gotchas

- **`@api` properties are not set in the constructor.** Reading `this.recordId` there gives `undefined`; the first hook that can see it is `connectedCallback`.
- **There is no DOM in the constructor either** — `this.template.querySelector` returns `null`, and adding attributes to the host element throws.
- **`connectedCallback` can fire more than once.** Moving a component in the DOM disconnects and reconnects it, so a subscription made there needs a matching teardown, not a one-time flag.
- **Mutating reactive state in `renderedCallback` without a guard is an infinite render loop** — the single most common LWC defect.
- **`errorCallback` only catches errors thrown in a descendant's lifecycle hooks.** Errors in your own hooks, in event handlers, or inside a promise are not caught. → [18 · Error handling](18-error-handling-and-user-feedback.md)
- **`disconnectedCallback` is not guaranteed on page unload.** It is a DOM-removal hook, not a destructor; do not rely on it to flush anything important.
- **The constructor must call `super()` first** and must not touch `this` before it.
- **A missing `isExposed` in the metadata file is silent.** The component deploys cleanly and simply never appears in App Builder.

## Recall

Q: Which three files does every LWC bundle require?
A: The HTML template, the JavaScript class extending `LightningElement`, and `.js-meta.xml` — all sharing the folder's name.

Q: In what order do a parent and its child complete rendering?
A: The parent constructs, connects and renders first, then the child does — but the **child's** `renderedCallback` fires before the parent's.

Q: Why is reading an `@api` property in the constructor a bug?
A: Public properties are assigned by the framework after construction; the earliest reliable read is `connectedCallback`.

Q: What guard does `renderedCallback` almost always need, and why?
A: A one-time flag or condition — it runs after every render, so mutating reactive state inside it re-triggers itself.

Q: What is GA for LWC development at 67.0?
A: Component Preview — rendering a single component in the browser or VS Code without a full page reload, with faster hot module reloading.

## Related

- [02 · Templates, directives & rendering](02-templates-directives-and-rendering.md) — what the template can express between renders
- [05 · Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) — what actually triggers the render cycle
- [03 · Composition, slots & dynamic components](03-composition-slots-and-dynamic-components.md) — `lwc:ref` instead of `querySelector`
