# Decorators & the Reactivity Model

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 05

**Scope:** What makes a component re-render — the three decorators, the mutation rules behind them, and where shared state should live instead. Wiring data specifically is [08 · Apex in LWC](08-apex-in-lwc-wire-vs-imperative.md); message-passing is [04](04-events-and-component-communication.md).

## Core idea

Every field on a `LightningElement` is reactive by default — has been since Spring '20 — and the framework re-renders when a field is *reassigned*. That one word carries the whole model. Reassignment is observable; mutation in place is not. `this.rows = [...this.rows, row]` renders; `this.rows.push(row)` does not, and no error tells you so. `@track` exists solely to opt a field into deep observation so that in-place mutation is also seen, which is why it went from mandatory on every field to a narrow tool most components never need — and why tutorials that still decorate every field are teaching a pre-2020 framework. `@api` marks a field or method public; `@wire` binds a field or function to a data source. That is the entire decorator surface.

## How it works

| Decorator | Marks | Note |
|---|---|---|
| `@api` | public property or method | one-way in; the child must never reassign it |
| `@track` | deep reactivity on an object or array | **only** needed for in-place mutation |
| `@wire` | property or function bound to an adapter | reactive to `$`-prefixed parameters |

- **Reassignment is the trigger.** Primitives are covered automatically. For objects and arrays, replace rather than mutate — `this.rows = [...this.rows]` after a change is the idiomatic form and it also makes the change obvious to whoever reads it.
- **`@track` observes nested fields.** With it, `this.filters.status = 'Open'` re-renders; without it, only `this.filters = {...}` does.
- **`@wire` parameters prefixed with `$` are reactive.** `@wire(getRecord, { recordId: '$recordId' })` re-invokes whenever `recordId` changes; without the `$` the value is a literal string.
- **A wired *property* gives you `{ data, error }`**; a wired *function* receives the same object and lets you transform it. Neither can be called imperatively — that needs a separate import. → [08](08-apex-in-lwc-wire-vs-imperative.md)
- **Getters are the computed layer.** They re-evaluate on every render, so keep them cheap and never give them side effects.

```js
import { LightningElement, api, track, wire } from 'lwc';
export default class OrderList extends LightningElement {
    @api recordId;
    @track filters = { status: 'Open' };            // in-place mutation is intended here
    rows = [];

    @wire(getOrders, { accountId: '$recordId' })    // $ makes it reactive
    wiredOrders({ data, error }) { if (data) this.rows = [...data]; }

    addRow(row) { this.rows = [...this.rows, row]; }   // reassign — push() renders nothing
}
```

## 2026 currency

**LWC State Managers are GA at API 67.0, and they change where the answer to "where does this state live?" should point.** `defineState` from `@lwc/state` takes a setup function that receives `atom`, `computed` and `setAtom`: an *atom* is one reactive value, a *computed* derives from atoms and recomputes lazily only when its inputs change, and `setAtom` is the only way to write. The module returns the atoms and computeds it wants to make public, and any component can consume it — so shared state stops being prop-drilled down a tree or announced with events, and becomes a testable module with no component attached. Multiple `setAtom` calls in one tick are batched into a single notification, so the reactivity does not cost render churn. Salesforce also ships built-in managers such as `lightning/stateManagerRecord`. This is the first genuinely new answer to cross-component state since LMS, and it makes the remaining case for `@track` narrower still. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **`push`, `splice`, `sort` and `pop` do not re-render.** Neither does `obj.field = x` on an undecorated object field. The component is correct and the screen is stale.
- **`@track` on a primitive does nothing.** It is not an error and not a no-op worth writing — it just signals a misunderstanding to the next reader.
- **A missing `$` in a wire parameter is silent.** `{ recordId: 'recordId' }` passes the literal string and the wire never refreshes.
- **`@wire` results are immutable.** Mutating `data` throws in strict mode; copy it first — which is why `[...data]` appears in the sample above.
- **A child reassigning its own `@api` property works until the parent re-renders**, then the value is overwritten with no warning. → [04](04-events-and-component-communication.md)
- **Getters run on every render**, so an expensive computation in one is paid repeatedly and is invisible in the template. → [02](02-templates-directives-and-rendering.md)
- **`@wire` cannot be called imperatively or conditionally.** It fires when its parameters resolve; gating it means gating the parameter, not the decorator.
- **State managers are not a replacement for LDS caching.** They hold application state, not record data — `getRecord` still owns the record cache.

## Recall

Q: What actually triggers a re-render in LWC?
A: Reassigning a field. In-place mutation of an object or array is invisible unless the field carries `@track`.

Q: When is `@track` still necessary?
A: Only when you deliberately mutate a nested property of an object or array in place rather than replacing the whole value.

Q: What does the `$` prefix do in a wire configuration?
A: Marks the parameter as reactive — the adapter re-invokes when that component property changes. Without it, the value is a literal.

Q: What are the three building blocks of an LWC State Manager?
A: `atom` (one reactive value), `computed` (lazily derived from atoms), and `setAtom` (the only way to write), all supplied to the `defineState` setup function.

Q: Why can't you mutate the `data` returned by a wire adapter?
A: Wire results are immutable and shared from the cache — copy before changing, or the mutation throws.

## Related

- [04 · Events & component communication](04-events-and-component-communication.md) — the messaging alternative that state managers partly displace
- [02 · Templates, directives & rendering](02-templates-directives-and-rendering.md) — where getters are consumed and re-evaluated
- [08 · Apex in LWC — wire vs imperative](08-apex-in-lwc-wire-vs-imperative.md) — using `@wire` against Apex, and `refreshApex`
