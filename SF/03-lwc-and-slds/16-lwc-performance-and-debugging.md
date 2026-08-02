# LWC Performance & Debugging

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 07

**Scope:** Why a page feels slow, how to find out, and the three refresh APIs — which one to reach for. Server-side cost is [02-apex · 01](../02-apex-and-triggers/INDEX.md) and [08-data · 07](../08-data-modeling-and-large-data-volumes/INDEX.md); this is the client.

## Core idea

Almost every slow LWC is slow for one of three reasons, and they need different fixes. **Too many round trips** — each `@wire` is a request, and five components each fetching the same record make five of them unless they go through Lightning Data Service, which dedupes and caches ([06](06-lightning-data-service-and-ui-api-wires.md)). **Too much rendering** — reassigning a tracked array re-renders the list, and a getter in a template runs on *every* render, so an expensive one behind a frequently-toggled conditional is a cost you cannot see in the markup ([02](02-templates-directives-and-rendering.md)). **Too much DOM** — a thousand rows is a thousand rows whether the user scrolls to them or not. The debugging problem is that all three present identically as "the page is slow", so the first move is always measurement, not optimisation.

## How it works

| Symptom | Where to look | Usual fix |
|---|---|---|
| Slow first paint | Network tab — count `aura`/`ui-api` calls | Fewer wires; let LDS dedupe; `@AuraEnabled(cacheable=true)` |
| Slow after interaction | Performance profile — long tasks | Stop reassigning whole arrays; move work out of getters |
| Slow with lots of data | Element count in the DOM | Paginate, or virtualize |
| "Nothing happens" | Console + `errorCallback` | An error is being swallowed → [18](18-error-handling-and-user-feedback.md) |

- **Turn on Debug Mode** (Setup → Debug Mode) for your own user before profiling. Without it you are reading minified framework code, and LWC skips some development-time warnings.
- **The three refresh APIs are not interchangeable.** `refreshApex(this.wiredResult)` re-runs an Apex wire *with the config it already had*; `notifyRecordUpdateAvailable(recordIds)` tells LDS a record changed behind its back; `RefreshEvent` from `lightning/refresh` asks the **container** to refresh a whole view, and reaches components you do not own.
- **`RefreshEvent` needs a participating container.** Components register a `refresh()` callback with `lightning/refresh` to join the refresh tree, and a component is **not** responsible for its descendants — each registers itself. Fire it where the container will hear it, or nothing happens and nothing errors.
- **Lazy-render behind `lwc:if`.** Content inside a false branch is never constructed — that is the cheap win `lwc:if` has over CSS `display: none`.
- **Debug the render, not the code.** Chrome DevTools' Performance panel plus `console.count()` in `renderedCallback` answers "how many times did this render" faster than reading the component.

## 2026 currency

Two Summer '26 additions matter here. **Dynamic list components** — `lightning-dynamic-list-container` and `lightning-dynamic-list-item` — bring **virtualization** to base components: only the rows in the viewport are rendered, with focus preserved across recycling, which removes the usual "paginate because the DOM died" workaround for lists in the thousands. They are **Developer Preview**, so they belong in a spike, not in a release. **Lazy-loading wire adapters** defer the fetch until the component is actually visible, which attacks the round-trip problem rather than the render one — the right lever for a tab or accordion whose contents most users never open. Neither replaces measuring first. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **`force:refreshView` does not port.** It is the Aura event; the LWC answer is `RefreshEvent` from `lightning/refresh`, and firing the string name from an LWC does nothing.
- **`refreshApex` re-provisions with the *old* config.** It is for "the data behind the same question changed" — never for "the question changed". → [08](08-apex-in-lwc-wire-vs-imperative.md)
- **Getters run on every render, including ones whose output did not change.** Cache the result in a field if it is expensive.
- **Mutating an array in place does not re-render; reassigning does.** The performance trap is the reverse of the correctness trap — reassigning in a loop re-renders each time. → [05](05-decorators-and-the-reactivity-model.md)
- **`renderedCallback` firing repeatedly is usually self-inflicted** — writing to a reactive field inside it re-triggers it.
- **Child `renderedCallback` fires before the parent's**, so parent-level measurement in `renderedCallback` is not "after everything rendered". → [01](01-component-model-and-lifecycle.md)
- **`cacheable=true` results are cached client-side and can go stale**; that is the feature, and it is why a write path needs an explicit refresh.
- **Debug Mode is per user and slows the page down.** Leaving it on for a production user is itself a performance bug.

## Recall

Q: What are the three refresh APIs and when does each apply?
A: `refreshApex` re-runs an Apex wire with its existing config; `notifyRecordUpdateAvailable` tells LDS a record changed server-side; `RefreshEvent` from `lightning/refresh` asks the container to refresh a whole view including components you don't own.

Q: Why is an expensive getter behind `lwc:if` still a problem?
A: Getters referenced in the template are evaluated on every render, so the cost is paid whenever the component re-renders, not only when the branch is true.

Q: What is the Summer '26 answer to rendering thousands of rows, and what is its status?
A: `lightning-dynamic-list-container` / `lightning-dynamic-list-item`, which virtualize to the viewport and preserve focus. **Developer Preview** — not production.

Q: A component fires `RefreshEvent` and nothing happens. What is the first thing to check?
A: Whether a container that participates in the refresh tree is listening, and whether the components you expect to refresh registered their own `refresh()` callback — descendants are not refreshed automatically.

Q: Why turn on Debug Mode before profiling?
A: Without it the framework is minified and some development-time warnings are suppressed, so the profile and the console are both harder to read.

## Related

- [05 · Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) — what actually triggers a re-render
- [06 · Lightning Data Service](06-lightning-data-service-and-ui-api-wires.md) — the cache that removes duplicate requests for free
- [08 · Apex in LWC](08-apex-in-lwc-wire-vs-imperative.md) — `cacheable=true` and `refreshApex`
- [20 · Offline LWC & mobile constraints](20-offline-lwc-and-mobile-constraints.md) — where every one of these costs is multiplied
- [08-data · Query plan & performance tuning](../08-data-modeling-and-large-data-volumes/INDEX.md) — when the client is fine and the query is not
