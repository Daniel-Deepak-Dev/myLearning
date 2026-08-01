# Composition, Slots & Dynamic Components

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 05

**Scope:** Putting components inside components — public API, content projection, references, and instantiating a component whose type you don't know until runtime. Talking *between* them is [04](04-events-and-component-communication.md).

## Core idea

Composition in LWC has two shapes and they answer different questions. `@api` properties are for *data* a parent supplies; **slots** are for *markup* a parent supplies, which is how you write a container that knows about layout and nothing about content. Beyond those, three directives have arrived since most published LWC material was written and they close the gaps that used to force ugly workarounds: `lwc:ref` replaces `querySelector` for elements you own, `lwc:spread` passes a whole object of properties instead of enumerating them, and `lwc:component` with `lwc:is` instantiates a component chosen at runtime — the thing that previously required Aura or a chain of conditionals.

## How it works

| Directive | Since | What it does |
|---|---|---|
| `lwc:ref="name"` | Spring '23 | names an element; read it as `this.refs.name` |
| `lwc:spread={obj}` | Summer '23 | binds every key of an object as a property |
| `lwc:component` + `lwc:is={ctor}` | Winter '24 | renders a constructor resolved at runtime |

- **`@api` is the public contract**, on properties and on methods. A parent calls a child's `@api` method through a reference; the child never reaches upward. Public properties are one-way — a child must not reassign its own `@api` field.
- **Slots project the parent's markup into the child's template.** `<slot></slot>` is the default; `<slot name="footer">` is addressed with `slot="footer"` on the supplied element.
- **Slotted content belongs to the parent, not the child.** It is styled by the parent's CSS and its events fire in the parent's scope — the single most surprising thing about slots. → [13 · Shadow DOM & styling](INDEX.md)
- **`lwc:spread` spreads top-level keys only.** Nested objects are passed as-is, and it does not bind event handlers.
- **Dynamic components need a real constructor.** Resolve it with a dynamic `import()`, then assign — `lwc:is` takes the constructor, not a string name.

```html
<!-- container.html -->
<div class="card">
    <slot name="header">Fallback header</slot>
    <c-order-row lwc:ref="firstRow" lwc:spread={rowProps}></c-order-row>
    <lwc:component lwc:is={rowCtor}></lwc:component>
</div>
```

```js
const { default: ctor } = await import('c/orderRowCompact');   // resolve, then assign
this.rowCtor = ctor;
this.refs.firstRow.focus();                                    // @api method on the child
```

## 2026 currency

Nothing in this topic changed at 67.0 — the currency risk is the opposite one. All three directives post-date the bulk of published LWC tutorials, so the material you find still solves these problems the old way: `this.template.querySelector` for references, one attribute per property, and a stack of `lwc:if` branches standing in for a dynamic component. Dynamic components in particular were an Aura capability for years, and their absence from LWC is still cited as a reason to keep Aura in a codebase; since Winter '24 it is not one. Composition patterns for Flow screens and quick actions are [11](INDEX.md); the styling consequences of slots and shadow boundaries are [13](INDEX.md).

> **From my notes.** The old `Facet (== Slot in LWC)` page maps the Aura *facet* idea onto LWC slots. The analogy holds for the mental model and breaks on scope: an Aura facet is evaluated in the *component's* context, whereas slotted LWC content stays in the **parent's** — which is why parent CSS reaches it and the child's does not.

## Gotchas

- **`this.refs` is undefined before the first render.** It is populated for `renderedCallback` onward — never the constructor.
- **`lwc:ref` inside a `for:each` does not give you a list.** Refs must be unique; iterate with `querySelectorAll` instead.
- **A child must never reassign its own `@api` property.** It works until the parent re-renders and silently overwrites it; expose an event instead. → [04](04-events-and-component-communication.md)
- **Slot fallback content renders only when nothing is passed** — passing an empty element counts as passing something.
- **Named slots are not validated.** A typo in `slot="fotter"` drops the content with no error.
- **`lwc:spread` does not bind handlers.** `{ onclick: this.handle }` in the spread object will not wire an event.
- **`lwc:is` must receive a constructor.** Assigning a module name string renders nothing and logs nothing useful.
- **Dynamically imported components must still be deployable and referenced statically enough to be packaged** — a name built from string concatenation at runtime will not resolve.

## Recall

Q: What is the difference between passing data with `@api` and passing markup with a slot?
A: `@api` supplies values the child renders itself; a slot lets the parent supply the markup, which stays in the parent's styling and event scope.

Q: When is `this.refs` available?
A: From `renderedCallback` onward — never in the constructor, and not in `connectedCallback`.

Q: Which release made dynamic components possible in LWC, and what is the syntax?
A: Winter '24 — `<lwc:component lwc:is={ctor}>`, where `ctor` is a constructor resolved by a dynamic `import()`.

Q: What does `lwc:spread` *not* do?
A: Spread nested objects, or bind event handlers — it assigns top-level keys as properties only.

Q: Why does parent CSS reach slotted content?
A: Slotted markup belongs to the parent's template and only renders inside the child; it never enters the child's scope.

## Related

- [04 · Events & component communication](04-events-and-component-communication.md) — how a child tells its parent something changed
- [01 · Component model & lifecycle](01-component-model-and-lifecycle.md) — why refs and children are absent early in the cycle
- [13 · Shadow DOM, styling & scoped CSS](INDEX.md) — what a shadow boundary does to slotted content
