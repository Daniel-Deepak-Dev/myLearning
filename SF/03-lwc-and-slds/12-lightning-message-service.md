# Lightning Message Service

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 06

**Scope:** Talking between components that share no ancestor you control — the message channel, scope, and the subscription lifecycle. Parent/child communication and why pubsub libraries are wrong is [04](04-events-and-component-communication.md); shared *state* rather than messages is [05](05-decorators-and-the-reactivity-model.md).

## Core idea

LMS is the sanctioned answer to "these two components are on the same page and cannot see each other in the DOM". The important design decision is that **the channel is metadata, not code**: a `.messageChannel-meta.xml` file is a deployable, packageable, permission-checkable artifact, which is precisely what a pubsub module never was. That is what makes LMS defensible where the old pattern was not — the set of channels in an org is discoverable, and a channel can be marked `isExposed` or not for other namespaces. The second thing to hold onto is that LMS is genuinely a *last* resort. It is unaddressed broadcast: no delivery guarantee, no ordering, no reply, and every subscriber on the page hears everything. If a `CustomEvent` up one level would do the job, [04](04-events-and-component-communication.md)'s answer is better, and since 67.0 a state manager is often better still.

## How it works

| Piece | Detail |
|---|---|
| `force-app/…/messageChannels/Orders.messageChannel-meta.xml` | `masterLabel`, `isExposed`, `lightningMessageFields` |
| `import CHANNEL from '@salesforce/messageChannel/Orders__c'` | the import — custom channels end `__c` |
| `@wire(MessageContext) messageContext` | required context; **must be wired**, never constructed |
| `publish(messageContext, CHANNEL, payload)` | fire and forget |
| `subscribe(messageContext, CHANNEL, handler, { scope: APPLICATION_SCOPE })` | returns a subscription |
| `unsubscribe(subscription)` | in `disconnectedCallback`, always |

- **Scope is the setting everyone misses.** The default is the *active* navigation context, so a subscriber sitting in an inactive console tab or the utility bar hears nothing. `APPLICATION_SCOPE` widens it to the whole app, and that is usually what a utility-bar component wants.
- **`lightningMessageFields` is documentation, not a schema.** The declared fields do not validate the payload; publishing a different shape succeeds and the subscriber gets whatever you sent.
- **Subscribe in `connectedCallback`, unsubscribe in `disconnectedCallback`.** `connectedCallback` can run more than once, so guard against double-subscribing. → [01](01-component-model-and-lifecycle.md)
- **A publisher that also subscribes hears its own message.** There is no sender exclusion; if that matters, put an identifier in the payload and filter.
- **This is the one channel that crosses technology boundaries.** A message channel is visible to Aura and Visualforce as well, which makes LMS the practical seam during a migration — the only reason those get named in this area.

```js
import { subscribe, unsubscribe, publish, MessageContext, APPLICATION_SCOPE } from 'lightning/messageService';
import ORDERS from '@salesforce/messageChannel/Orders__c';

export default class OrderWatcher extends LightningElement {
    @wire(MessageContext) messageContext;            // wired — never `new`
    sub;

    connectedCallback() {
        this.sub ??= subscribe(this.messageContext, ORDERS,
            (msg) => { this.orderId = msg.orderId; },
            { scope: APPLICATION_SCOPE });           // omit and inactive tabs stay silent
    }
    disconnectedCallback() { unsubscribe(this.sub); this.sub = null; }
}
```

## 2026 currency

LMS has not changed, but its job has narrowed twice. **State Managers went GA at 67.0**, and for the common case people reach for LMS — "several components need to see the same value" — a state manager is the better fit: it holds the value rather than announcing it, so a component that renders *after* the message would have been sent still sees the current state instead of missing it. LMS remains right for genuine **events** ("the user just saved something") and for anything crossing into Aura or Visualforce, which no state manager can do. The second narrowing is [09](09-lightning-web-security.md): under LWS a payload crossing a namespace boundary arrives as a proxy and can unwrap to `null`, so cross-namespace channels should carry primitives or JSON strings. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **No unsubscribe is a leak that survives navigation.** The handler keeps firing against a component that is no longer on screen, usually surfacing as a duplicate action.
- **`MessageContext` obtained any way other than `@wire` does not work** — and the failure is a publish that goes nowhere.
- **Default scope silently excludes inactive console tabs and the utility bar.** The classic "works on my page, not in the console" bug.
- **Custom channel imports must match the file exactly, including `__c`.** A wrong name is a compile error; a wrong *namespace* is a runtime silence.
- **Payloads must be serializable.** No functions, no DOM references, no class instances — and across namespaces, prefer primitives or JSON. → [09](09-lightning-web-security.md)
- **`connectedCallback` running twice double-subscribes**, so every message is handled twice. Guard on the subscription field.
- **LMS is not available in every container.** Lightning Out and standalone apps have no message service, and Experience Cloud has its own rules. → [05-experience](../05-experience-cloud-lwr/INDEX.md)

## Recall

Q: What makes a message channel different from a pubsub module?
A: It is metadata — a deployable, packageable, discoverable artifact with an `isExposed` flag — rather than a shared JavaScript singleton.

Q: What does `APPLICATION_SCOPE` change?
A: It widens the subscription beyond the active navigation context, so components in inactive console tabs and the utility bar receive messages.

Q: Where must `subscribe` and `unsubscribe` go, and why the guard?
A: `connectedCallback` and `disconnectedCallback`. `connectedCallback` can fire more than once, so an unguarded subscribe leads to duplicate handling.

Q: When is a state manager the better choice than LMS at 67.0?
A: When components need to share a *value*. A late-rendering component reads current state, whereas it would simply have missed the message.

Q: What is LMS still uniquely good for?
A: True events, and communication that crosses into Aura or Visualforce during a migration.

## Related

- [04 · Events & component communication](04-events-and-component-communication.md) — the DOM-bound alternatives to try first
- [05 · Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) — State Managers, which displace much of what LMS was used for
- [09 · Lightning Web Security](09-lightning-web-security.md) — why cross-namespace payloads should be primitives
