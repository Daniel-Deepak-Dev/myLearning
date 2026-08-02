# LWC Testing with Jest

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 07

**Scope:** Unit-testing a component bundle off-platform with Jest — mounting, querying, mocking wires and Apex. Apex test classes are [02-apex · 20](../02-apex-and-triggers/INDEX.md); this runs in Node, not in the org.

> **What changed.** Two of the three things older tutorials teach are stale. **Registering a wire adapter — `registerApexTestWireAdapter`, `registerLdsTestWireAdapter`, `registerTestWireAdapter` — is the Spring '21-and-earlier pattern**; the docs say that code "still works, but it isn't recommended." You now **import the adapter the component imports and call `.emit()` on it directly.** And `sfdx force:lightning:lwc:test:run` went with `sfdx` v1 — the runner is `npm run test:unit`.

## Core idea

A Jest test mounts a component into a jsdom document, drives it, and asserts on the rendered DOM. Nothing about it touches an org: there is no Apex, no records, no session — every `@salesforce/*` import is replaced by a stub before the test runs. That is the whole trade. Tests are fast and run in CI with no scratch org, and in exchange they can only prove *client* behaviour: given this data, does the component render and dispatch what it should. The two things people get wrong are both consequences of that. Base components are **stubs**, so asserting on the inside of a `lightning-input` asserts on a fake; and re-rendering is **asynchronous**, so an assertion written immediately after a property assignment reads the previous DOM.

## How it works

- **The bundle owns its tests.** `force-app/main/default/lwc/myCmp/__tests__/myCmp.test.js`. Jest config comes from `@salesforce/sfdx-lwc-jest/config`, and the run is `npm run test:unit` — `test:unit:watch` and `test:unit:coverage` are scaffolded too.
- **Mount with `createElement`, and always clean up.** jsdom persists between tests in a file; a component left in `document.body` leaks into the next test.
- **Query through `shadowRoot`.** `element.shadowRoot.querySelector('[data-id="total"]')` — inside the component it is `this.template`, from the test it is `shadowRoot`.
- **Await a microtask before asserting.** `await Promise.resolve()` flushes the render; there is no `waitFor` built in.
- **Wire:** import the same adapter module the component imports, then `adapter.emit(mockData)` or `adapter.error()`. sfdx-lwc-jest auto-mocks it — no registration call.
- **Imperative Apex:** `jest.mock('@salesforce/apex/X.y', () => ({ default: jest.fn() }), { virtual: true })`. The `virtual: true` is not optional; the module does not exist on disk.

```js
import { createElement } from 'lwc';
import MyCmp from 'c/myCmp';
import getRecord from '@salesforce/apex/AcctCtrl.getRecord';   // the wire adapter itself

jest.mock('@salesforce/apex/AcctCtrl.getRecord', () => ({ default: { emit: jest.fn() } }), { virtual: true });

describe('c-my-cmp', () => {
    afterEach(() => { while (document.body.firstChild) document.body.removeChild(document.body.firstChild); });

    it('renders the account name', async () => {
        const el = createElement('c-my-cmp', { is: MyCmp });
        document.body.appendChild(el);
        getRecord.emit({ Name: 'Acme' });
        await Promise.resolve();                                 // flush the re-render
        expect(el.shadowRoot.querySelector('[data-id="name"]').textContent).toBe('Acme');
    });
});
```

> **From my notes.** `LWC : Query DOM Elements` (2023) records that `lwc:ref` "cannot see them declared in DOM after rendering output in browser" and "is not a class name so cannot use queryselector to get the element." Still true, and it is a **testing** rule as much as a runtime one: `this.refs` exists only inside the component, so a Jest test can never select by it. Give anything a test must find a `data-*` attribute. The note's other finding holds too — duplicate `lwc:ref` names resolve to the **last** one, and `this.refs` has no `querySelectorAll` equivalent.

## 2026 currency

The **direct-emit wire pattern has been the recommendation since Spring '21**, but the `register*TestWireAdapter` form is what nearly every blog post and older Trailhead screenshot shows, so expect to meet it in an existing codebase — it is not broken, just superseded. The runner moved with the CLI: `sfdx force:lightning:lwc:test:*` belongs to `sfdx` v1 and is gone → [09-devops · 01](../09-devops-sfdx-and-release-management/INDEX.md). Newer surfaces are only partly testable this way — a component written against **State Managers** ([24](24-lwc-state-managers.md)) is tested by exercising the state module directly, which is most of the argument for extracting state in the first place.

## Gotchas

- **Jest coverage is not org coverage.** It counts toward nothing at deployment; only Apex coverage gates a production release.
- **Base components are stubs.** `lightning-button` renders an empty custom element — you can assert it exists and read its properties, never its internals or its rendered label.
- **jsdom has no layout.** `offsetWidth`, `getBoundingClientRect()` and anything scroll-related return zero; visual and responsive behaviour is untestable here.
- **A missing `afterEach` cleanup is the classic flaky-test cause** — the previous test's component is still mounted and its selectors match first.
- **`{ virtual: true }` is required on every `@salesforce/*` `jest.mock`**, because Jest cannot resolve a module that has no file.
- **`element.shadowRoot` is `null` before `appendChild`** — the component is not rendered until it is in the document.
- **Synthetic shadow does not apply in Jest.** Tests query real shadow roots, so a selector that works in a test can still fail in the org, and the reverse.

## Recall

Q: What replaced `registerApexTestWireAdapter` and when?
A: Since Spring '21, import the wire adapter the component imports and call `.emit(data)` / `.error()` on it directly. The old registration still works but is not recommended.

Q: Why does an assertion straight after setting a property fail?
A: Re-rendering is asynchronous. Await a microtask — `await Promise.resolve()` — before reading the DOM.

Q: What does `{ virtual: true }` do in a `jest.mock` of an `@salesforce/*` module?
A: It tells Jest to mock a module that has no file on disk. `@salesforce/apex/*`, `@salesforce/schema/*` and friends are resolved by the compiler, not by Node.

Q: Can a Jest test assert on the label rendered inside `lightning-button`?
A: No. Base components are stubbed — assert the element exists and check its `label` property instead.

Q: Why can't a test select an element by its `lwc:ref`?
A: Refs are not emitted into the DOM; `this.refs` is internal to the component. Use a `data-*` attribute.

## Related

- [08 · Apex in LWC — wire vs imperative](08-apex-in-lwc-wire-vs-imperative.md) — the two call shapes each test differently
- [16 · Performance & debugging](16-lwc-performance-and-debugging.md) — what to do when the behaviour is right but the render count isn't
- [21 · Local dev & Live Preview](21-local-dev-and-lightning-dev-server.md) — the other half of the feedback loop, in a real browser
- [09-devops · CI/CD](../09-devops-sfdx-and-release-management/INDEX.md) — running `test:unit` in a pipeline
