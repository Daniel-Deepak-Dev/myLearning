# Apex in LWC — Wire vs Imperative

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 06

**Scope:** Calling Apex from a component — the two call styles, the `cacheable` contract, and refreshing stale data. What the Apex method itself must do about security is [02-apex · 10](../02-apex-and-triggers/INDEX.md) and is not restated here.

## Core idea

An `@AuraEnabled` method reaches a component two ways, and the choice is decided by one question: **does this run because data changed, or because a user did something?** `@wire` is declarative and reactive — it fires when its parameters resolve, re-fires when a `$`-prefixed parameter changes, and you cannot call it, order it or await it. Imperative import is a plain function returning a promise — you call it in a handler, you control when, and nothing is cached. The trap is treating them as interchangeable styles for the same job. They are not: `@wire` requires `cacheable=true`, and `cacheable=true` is a promise that the method **does not mutate anything**, because the framework will serve its result from a client cache without asking the server again. A `cacheable=true` method that performs DML is not a performance choice, it is a correctness bug that appears intermittently.

## How it works

| | `@wire` | imperative |
|---|---|---|
| Apex requirement | **`cacheable=true` mandatory** | any `@AuraEnabled` method |
| Trigger | parameters resolve or change | you call it |
| Result | `{ data, error }`, immutable | a promise you own |
| Caching | client-side, shared | none |
| DML allowed | **no** | yes |
| Refresh | `refreshApex(this.wiredResult)` | call it again |

- **Keep the whole wired result, not just its data.** `refreshApex` needs the provisioned object — `wired({ data, error })` throws it away, so assign the argument to a field (`this._wired = value`) and pass *that*.
- **Errors arrive in different shapes.** A wire error lands in `error`; an imperative error lands in `.catch()`. Both are the same nested `body.message` structure, which is why every codebase grows a `reduceErrors` helper. → [18 · Error handling](18-error-handling-and-user-feedback.md)
- **`cacheable=true` methods run in the user's context by default at 67.0.** The FLS and sharing story is the Apex note's, not this one's — link it rather than re-teaching it: [02-apex · 10 user mode](../02-apex-and-triggers/INDEX.md).
- **`notifyRecordUpdateAvailable` refreshes *LDS*, `refreshApex` refreshes *your wire*.** They are not substitutes. If the Apex method returns records that LDS also caches, you often need both.
- **Imperative calls are unbounded.** Nothing stops a click handler firing four calls before the first returns; debounce, or disable the control while a call is in flight.

```js
import { LightningElement, api, wire } from 'lwc';
import { refreshApex } from '@salesforce/apex';
import getOrders from '@salesforce/apex/OrderController.getOrders';

export default class OrderPanel extends LightningElement {
    @api recordId;
    orders; _wired;                                  // keep the provisioned value, not just data

    @wire(getOrders, { accountId: '$recordId' })     // $ = reactive; re-fires on change
    handle(value) { this._wired = value; this.orders = value.data; }

    async handleSaved() { await refreshApex(this._wired); }   // re-runs with its LAST config
}
```

> **From my notes.** From `Cache issue : refreshApex of wire method & multiple calling of imperative method`: **"Refreshing wire method will only call the method using old parameter value, not the updated parameter value."** Still exactly right, and worth stating as the rule it implies — `refreshApex` re-provisions the wire with **the configuration it was last provisioned with**. It is for *"the data behind the same question changed"*, not for *"the question changed"*. Changing the question means changing the reactive `$` parameter, which re-invokes the wire on its own; calling `refreshApex` after a parameter change re-fetches the previous parameter's result and looks like a caching bug.

## 2026 currency

**The security default under every one of these calls flipped at 67.0**, and it surfaces in the component rather than in Apex. SOQL and DML now run in **user mode** by default, and a keyword-less class defaults to **`with sharing`** — so a `cacheable=true` method that used to return everything may now return fewer rows, or fewer fields, for exactly the users whose profiles were never tested. The failure is rarely an exception; it is a wire that resolves successfully with `data` missing a field, which reads as a UI bug. The rule that follows is worth internalising: **an LWC cannot be the security boundary**, because the method is callable by anyone who can reach the component. All of the mechanism — `AccessLevel`, `WITH USER_MODE`, `stripInaccessible`, the sharing keywords — belongs to [02-apex · 10 user mode](../02-apex-and-triggers/INDEX.md) and is deliberately not restated here. → [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md)

## Gotchas

- **`@wire` against a method without `cacheable=true` fails at runtime**, with an error that names caching rather than the method.
- **`cacheable=true` plus DML is a heisenbug.** The first call works; later calls serve from cache and the DML silently never happens.
- **`refreshApex` on a bare `data` value does nothing useful.** It needs the full provisioned object the wire handed you.
- **A wire cannot be awaited, gated or ordered.** "Load A then B" is an imperative pattern; expressing it with two wires produces a race.
- **Imperative calls bypass the cache entirely**, so a component that "just switched to imperative to fix a refresh problem" has also given up request de-duplication across the page.
- **`@AuraEnabled` methods must be `public static`** (or `global static` in a package) — an instance method is invisible with no deploy error.
- **Every `@AuraEnabled` method is an API endpoint for anyone who can see the component.** Its own permission checks are the security boundary; the component is not. → [07-security](../07-security-and-sharing/INDEX.md)

## Recall

Q: What does `cacheable=true` promise, and what breaks if the promise is false?
A: That the method mutates nothing. If it performs DML, later calls are served from the client cache and the DML silently stops happening.

Q: Why must you store the whole wired value rather than just `data`?
A: `refreshApex` takes the provisioned object the wire supplied; `data` alone cannot be refreshed.

Q: What does `refreshApex` do when the wire's parameter has changed since it was provisioned?
A: It re-runs with the **old** configuration. A changed parameter re-invokes the wire by itself — `refreshApex` is for the same question, not a new one.

Q: When is imperative Apex the right call rather than a wire?
A: When the call is user-initiated, needs ordering or awaiting, or performs DML.

Q: Which refresh do you use for records LDS also caches?
A: `notifyRecordUpdateAvailable` for the LDS copy and `refreshApex` for your own wire — often both.

## Related

- [06 · Lightning Data Service & UI API wires](06-lightning-data-service-and-ui-api-wires.md) — the no-Apex path, and `notifyRecordUpdateAvailable`
- [07 · GraphQL wire adapter](07-graphql-wire-adapter.md) — filtered reads that no longer need an Apex class at all
- [05 · Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) — `$` reactivity and why wire results are immutable
