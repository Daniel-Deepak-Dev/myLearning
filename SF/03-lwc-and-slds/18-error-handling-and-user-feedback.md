# Error Handling & User Feedback

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 07

**Scope:** Getting an error from wherever it was thrown to something the user can act on. Where errors *originate* is [08](08-apex-in-lwc-wire-vs-imperative.md) and [06](06-lightning-data-service-and-ui-api-wires.md); this is what you do with them.

> **What changed.** "Fire `ShowToastEvent` and you're done" is no longer portable. **`ShowToastEvent` is not supported in LWR Experience Cloud sites or standalone apps** — it is an event that needs a Lightning Experience container to catch it, and where there is none it fails silently. Since **Winter '24** the portable answer is the **`lightning/toast`** module with **`lightning/toastContainer`**, which the site itself hosts.

## Core idea

An LWC has three separate failure surfaces and they do not share a shape. A **wire** error arrives as data — the `{ data, error }` object simply carries `error` instead — and never throws. An **imperative** call rejects, so it lands in `.catch()`. A **rendering or lifecycle** failure in a descendant hits `errorCallback`. Nothing unifies them, which is why practically every real codebase ends up with a `reduceErrors` helper: the same logical failure reaches you as `error.body.message`, as an array of `body[].message`, as `body.pageErrors` and `body.fieldErrors` from LDS, or as a bare string, depending only on which path it took. The second half of the job is the part that gets skipped — deciding what the user is supposed to *do*. A toast that says "An error occurred" is indistinguishable from the page being broken.

## How it works

| Failure | Where it surfaces | Shape |
|---|---|---|
| `@wire` (Apex or LDS) | the `error` property | `error.body.message`, sometimes `body[].message` |
| Imperative Apex | `.catch(e => …)` | same body, wrapped in a rejection |
| `lightning-record-edit-form` | `onerror` handler, `lightning-messages` | `detail.message` + `detail.output.fieldErrors` |
| Descendant lifecycle hook | `errorCallback(error, stack)` | a real `Error` |
| Field validation | `setCustomValidity` + `reportValidity` | inline, on the field |

- **Throw `AuraHandledException` from Apex.** It is the difference between the user reading *"This account is locked for editing"* and reading a class name and line number. An unhandled exception leaks implementation detail to the client.
- **`errorCallback` is narrower than "error boundary".** It catches errors thrown in a **descendant's lifecycle hooks** — not your own hooks, not event handlers, not anything inside a promise. → [01](01-component-model-and-lifecycle.md)
- **Modals instead of `window.*`.** `lightning/alert`, `lightning/confirm` and `lightning/prompt` are promise-based and render as real modals; `window.confirm()` is blocked or unreliable depending on the container.
- **Put the error where the user is looking.** Field-level errors belong on the field, form errors in `lightning-messages`, and only genuinely page-level events belong in a toast.
- **Never catch and drop.** A bare `.catch(() => {})` produces the worst outcome available: the button does nothing and the console is clean.

```js
import { LightningElement } from 'lwc';
import Toast from 'lightning/toast';               // portable — works in LWR sites too

export default class Saver extends LightningElement {
    async handleSave() {
        try {
            await saveRecord({ recordId: this.recordId });
            Toast.show({ label: 'Saved', variant: 'success' }, this);
        } catch (e) {
            this.errorMessage = reduceErrors(e).join(', ');   // render it inline, not only as a toast
        }
    }
}
```

## 2026 currency

The split is the thing to carry forward: **`ShowToastEvent` for Lightning Experience, `lightning/toast` + `lightning/toastContainer` for LWR sites** — and if a component is meant to run in both, the second is the one to write. This is the same portability question that decides `NavigationMixin` ([10](10-navigation-and-page-references.md)) and base-component availability off-platform ([22](22-lwc-open-source-and-off-platform-reuse.md)): a component is only as reusable as the container-dependent modules it imports. Guest-user contexts sharpen it further, because an error message is an information-disclosure surface there → [05-experience · guest hardening](../05-experience-cloud-lwr/INDEX.md).

## Gotchas

- **`ShowToastEvent` fails silently in an LWR site.** No error, no toast — the event has nobody to bubble to.
- **A wire error does not throw**, so `try/catch` around a wire does nothing. Check the `error` property.
- **`errorCallback` will not catch your own `connectedCallback` throwing**, nor anything in a promise or an event handler.
- **Without `AuraHandledException` the user sees the raw exception**, class name and all — a leak as much as a UX failure.
- **`reduceErrors` is a copied helper, not a platform module.** There is no `import { reduceErrors }` from anything official; every codebase has its own, and they drift.
- **Toasts auto-dismiss and are easy to miss** — mode `sticky` exists for errors the user must actually read.
- **A toast is not announced reliably to assistive technology.** An error the user must act on belongs in the DOM. → [17](17-accessibility-and-internationalization.md)
- **`error.body` can be an array.** Handling only the object shape works until the first multi-error response.

## Recall

Q: Why does `ShowToastEvent` do nothing in an LWR Experience Cloud site?
A: It is a bubbling event that requires a Lightning Experience container to handle it. LWR has none, so it fails silently. Use `lightning/toast` with `lightning/toastContainer` instead.

Q: How does a wire error reach you, and why doesn't `try/catch` help?
A: It arrives as the `error` property of the `{ data, error }` object. The wire never throws, so there is nothing for `catch` to intercept.

Q: What exactly does `errorCallback` catch?
A: Errors thrown in a **descendant's** lifecycle hooks. Not your own hooks, not event handlers, not promise rejections.

Q: What does `AuraHandledException` buy you?
A: A controlled message in `error.body.message` instead of the raw exception, which otherwise exposes the Apex class and line number to the browser.

Q: Why does every project have its own `reduceErrors`?
A: Because there is no platform-provided one, and the same failure arrives as `body.message`, `body[].message`, `body.pageErrors`/`fieldErrors`, or a plain string depending on the call path.

## Related

- [01 · Component model & lifecycle](01-component-model-and-lifecycle.md) — `errorCallback` and where it sits in the hook order
- [08 · Apex in LWC — wire vs imperative](08-apex-in-lwc-wire-vs-imperative.md) — the two shapes an Apex failure arrives in
- [16 · Performance & debugging](16-lwc-performance-and-debugging.md) — when "nothing happens" is a swallowed error
- [17 · Accessibility & internationalization](17-accessibility-and-internationalization.md) — announcing an error rather than only showing it
- [02-apex · Exceptions](../02-apex-and-triggers/INDEX.md) — throwing `AuraHandledException` from the server side
