# LWC State Managers

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 07

**Scope:** `defineState` from `@lwc/state` — shared reactive state as a module instead of as events. Component-local reactivity is [05](05-decorators-and-the-reactivity-model.md); the page-wide message bus is [12](12-lightning-message-service.md).

## Core idea

Until this release, two components that needed the same data had three options and all of them were bad past a certain size: pass it down through every intermediate component, bounce it up and back down as events ([04](04-events-and-component-communication.md)), or publish it on a message channel and let every subscriber keep its own copy ([12](12-lightning-message-service.md)). A **state manager** is a fourth answer — a plain JavaScript module that owns a slice of state and the functions that change it, which components subscribe to rather than copy. State lives outside the component tree, so it survives re-render, and it is a module, so it can be unit-tested without mounting anything ([15](15-lwc-testing-with-jest.md)). The mental shift is that the state is the thing with an API and components are its consumers, rather than one component being the owner and everyone else asking it politely.

## How it works

- **`defineState` takes a setup function** and returns a factory. The setup function receives its building blocks as its first argument and any initial values after that.
- **Three primitives.** `atom(value)` is a reactive cell; `computed([deps], fn)` is a **lazily evaluated** derivation that recalculates only when its inputs change; `setAtom(atom, value)` is the only way to write.
- **The setup function returns the public API** — which atoms and computeds are readable, and which functions may mutate. Anything not returned is private.
- **Instantiating makes a component the provider** for its entire subtree: `form = formStateManager();`
- **Descendants reach up with `fromContext`** — `form = fromContext(formStateManager)` — and read through `.value`, e.g. `this.form.value.hasUnsavedChanges`.
- **Writes batch.** Multiple `setAtom` calls in the same tick collapse into a single notification cycle, so a multi-field update re-renders once.
- **Built-ins wrap Lightning Data Service.** `lightning/stateManagerRecord` (via `createRecordStateManager()`) and siblings for object info, layouts and related lists → [06](06-lightning-data-service-and-ui-api-wires.md).

```js
// counterState.js
import { defineState } from '@lwc/state';

export const createCounter = defineState(({ atom, computed, setAtom }, initialCount = 0) => {
    const count = atom(initialCount);
    const doubled = computed([count], (countValue) => countValue * 2);
    const increment = () => setAtom(count, count.value + 1);
    return { count, doubled, increment };          // only these are public
});

// child component — reaches up to whichever ancestor instantiated it
import { fromContext } from '@lwc/state';
counter = fromContext(createCounter);
get total() { return this.counter.value.doubled; }
```

## 2026 currency

**State Managers went GA at API 67.0 (Summer '26)** — the first genuinely new answer to cross-component state since Lightning Message Service, and the reason `@track` keeps getting narrower ([05](05-decorators-and-the-reactivity-model.md)). The distinction to hold is **context versus bus**. A state manager is shared through the DOM hierarchy: `fromContext` finds the *nearest ancestor* that instantiated it, so two sibling subtrees get two independent instances, and a component outside the provider's subtree gets nothing. LMS is genuinely page-wide, crosses into the utility bar and console tabs with `APPLICATION_SCOPE`, and reaches components in trees you do not control. They solve adjacent problems and neither replaces the other. Note the version skew worth knowing about: the **platform feature is GA while the `@lwc/state` npm package is still `0.x`** — off-platform it is not on the same footing ([22](22-lwc-open-source-and-off-platform-reuse.md)).

## Gotchas

- **Context follows the DOM, not the page.** A component that is not a descendant of the provider gets no state — this is the "it works on the record page, not in the utility bar" bug, and LMS is the fix. → [12](12-lightning-message-service.md)
- **Two ancestors instantiating the same manager create two independent states.** Instantiate once, as high as the sharing needs to reach.
- **Read through `.value`.** `this.form.hasUnsavedChanges` is `undefined`; `this.form.value.hasUnsavedChanges` is the value.
- **`setAtom` is the only write path.** Assigning to an atom directly does not notify anything, and fails quietly.
- **Computeds are lazy.** A computed nothing reads is never evaluated — fine, until you put a side effect in one.
- **State outside the component outlives the component.** Nothing resets on disconnect; a stale value from a previous record is a real defect unless the manager is reset deliberately.
- **It is not a persistence layer.** State managers hold client state — LDS remains the only client-side write path to records. → [06](06-lightning-data-service-and-ui-api-wires.md)
- **The npm package is pre-1.0** even though the platform feature is GA; do not assume off-platform parity.

## Recall

Q: What are the three primitives a `defineState` setup function receives?
A: `atom` (a reactive cell), `computed` (a lazy derivation over declared dependencies) and `setAtom` (the only write path).

Q: How does a descendant component get the ancestor's state manager instance?
A: `fromContext(theStateManager)` — it walks up the DOM to the nearest ancestor that instantiated it.

Q: What is the difference between a state manager and Lightning Message Service?
A: A state manager shares state through the DOM hierarchy and holds a single source of truth. LMS is a page-wide bus that carries messages, not state, and reaches components outside your subtree.

Q: Why does a multi-field update re-render only once?
A: `setAtom` calls within the same tick are batched into a single notification cycle.

Q: What happens if two ancestors each instantiate the same state manager?
A: Each subtree gets its own independent instance. `fromContext` resolves to the nearest provider, not to a global.

## Related

- [05 · Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) — where component-local reactivity ends and this begins
- [12 · Lightning Message Service](12-lightning-message-service.md) — the bus, and why it is still needed for cross-tree communication
- [04 · Events & component communication](04-events-and-component-communication.md) — the pattern this replaces for deep hierarchies
- [15 · LWC testing with Jest](15-lwc-testing-with-jest.md) — a state module is testable without mounting a component
- [22 · LWC OSS & off-platform reuse](22-lwc-open-source-and-off-platform-reuse.md) — `@lwc/state` off the platform
