# Events & Component Communication

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 05

**Scope:** Getting a message from one component to another — up, down, and across an unrelated part of the page. Sharing *state* rather than sending messages is [05](05-decorators-and-the-reactivity-model.md).

## Core idea

LWC has exactly three sanctioned channels and choosing between them is a question about the DOM, not about preference. **Down** the tree, a parent sets an `@api` property or calls an `@api` method. **Up** the tree, a child dispatches a `CustomEvent` and the parent listens for it. **Across** unrelated branches — two components on a page that share no ancestor you control — Lightning Message Service carries a message over a channel. What is *not* on the list is a pubsub module. That pattern exists in thousands of LWC repositories because it was the only cross-DOM option before LMS shipped; it is an Aura-era workaround, it has no scope control, and it leaks subscriptions across navigation. If a codebase still has one, replacing it is the migration, not a refactor.

## How it works

| Direction | Mechanism | Constraint |
|---|---|---|
| Parent → child | `@api` property or method | child must not reassign its own `@api` field |
| Child → parent | `dispatchEvent(new CustomEvent(...))` | crosses one shadow boundary by default |
| Anywhere ↔ anywhere | Lightning Message Service | needs a `messageChannel` metadata file → [12](12-lightning-message-service.md) |

- **Event names are lowercase with no spaces, hyphens or camel case.** `orderselected`, not `orderSelected` — the HTML attribute is `onorderselected`, and camel case simply never fires.
- **`bubbles` and `composed` are both `false` by default**, which is the right default: the event reaches the parent's listener on the child element and stops. Setting both `true` makes an event traverse the entire DOM and every shadow boundary — powerful, and almost always the wrong instinct.
- **Retargeting means the listener sees the host, not the inner element.** Once an event crosses a shadow boundary, `event.target` is rewritten to the component that emitted it, so the parent cannot reach into the child's internals.
- **Put primitives in `detail`.** Passing an object hands the receiver a live reference to the child's state, and the receiver can mutate it — a real defect in shadow DOM, and constrained further under Lightning Web Security. → [09 · LWS](09-lightning-web-security.md)
- **Never dispatch from the constructor.** No one is listening yet; `connectedCallback` is the earliest useful point.

```js
// child — announce, don't command
this.dispatchEvent(new CustomEvent('orderselected', {
    detail: { orderId: this.order.id }              // a primitive, not this.order
}));                                                 // bubbles/composed default to false
```

```html
<!-- parent -->
<c-order-row onorderselected={handleOrderSelected}></c-order-row>
```

## 2026 currency

The mechanics are stable; what has changed is that the workarounds are now clearly wrong rather than merely dated. **Lightning Message Service is the supported cross-DOM channel** and has been for several releases, so a pubsub module is a finding in a code review. **Lightning Web Security replaced Locker Service**, and the distortion list around event payloads differs — advice of the form "Locker blocks passing X in `detail`" needs re-testing rather than trusting. At 67.0 LWS also blocks the `data:` URI scheme, so an event payload carrying a `data:` URL for a download or preview needs a `blob:` URL instead. All of that is [09](09-lightning-web-security.md)'s subject; this note just stops short of repeating it.

> **From my notes.** `Events - LWC`, `dispatchEvent (CustomEvent)` and `addEventListener - LWC` are all 2020 pages and thin, but one line in them is still the most useful sentence on the topic: **name the event for what happened, not for what you want done about it.** `orderselected` leaves the parent free to decide; `refreshtable` has already decided for it, and breaks the second time the component is reused.

## Gotchas

- **A camel-case event name silently never fires.** There is no warning — `onorderSelected` is just an unknown attribute.
- **`bubbles: true` without `composed: true` stops at the shadow boundary**, which produces an event that works in Jest and not in the org.
- **`composed: true` on a bubbling event reaches the whole document.** Two instances of the component on one page will both trigger every listener.
- **`event.target` is retargeted after crossing a boundary.** Reading `event.target.dataset` in a grandparent gives the host element's dataset, not the button's.
- **An object in `detail` is passed by reference.** The receiver can mutate the sender's state; send an id or a copy.
- **Listeners added with `addEventListener` in `connectedCallback` must be removed in `disconnectedCallback`** — and `connectedCallback` can fire more than once. → [01](01-component-model-and-lifecycle.md)
- **LMS subscriptions survive navigation** unless unsubscribed, which is how a "phantom" duplicate handler appears after a few page changes.
- **Slotted content dispatches into the parent's scope**, so a listener on the child never sees it. → [03](03-composition-slots-and-dynamic-components.md)

## Recall

Q: What are the three sanctioned communication channels, and which is not on the list?
A: `@api` down, `CustomEvent` up, Lightning Message Service across. A pubsub library is not — it is an Aura-era workaround superseded by LMS.

Q: What are the default values of `bubbles` and `composed`, and why do they matter?
A: Both `false`. The event reaches the immediate parent and stops; setting both `true` sends it across the entire DOM and every shadow boundary.

Q: Why must event names be all lowercase?
A: The template binds them as HTML attributes (`onorderselected`). A camel-case name never matches and the handler silently never runs.

Q: What is retargeting?
A: When an event crosses a shadow boundary, `event.target` is rewritten to the emitting component's host, so listeners cannot reach the internal element.

Q: Why should `detail` carry primitives?
A: An object is passed by reference, letting the receiver mutate the sender's state — and payload handling is further constrained under Lightning Web Security.

## Related

- [05 · Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) — when shared state beats sending messages at all
- [03 · Composition, slots & dynamic components](03-composition-slots-and-dynamic-components.md) — `@api` as the downward half of the contract
- [12 · Lightning Message Service](12-lightning-message-service.md) — the cross-DOM channel, with scope and channel metadata
