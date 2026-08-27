# Navigation & Page References

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 06

**Scope:** Sending the user somewhere — the navigation service, the page reference vocabulary, and console tab control. Navigation *within* a Flow screen is [11](11-lwc-in-flow-screens-and-quick-actions.md); Experience Cloud routing and named pages are [05-experience](../05-experience-cloud-lwr/INDEX.md).

## Core idea

A component never builds a URL. It describes a **destination** as a plain object — a page reference — and hands it to the navigation service, which resolves it for wherever the component happens to be running. The same `standard__recordPage` reference becomes a record page in Lightning Experience, a subtab in a console app, a screen in the mobile app, and a site route in Experience Cloud, without the component knowing which. That is the whole argument for the indirection, and it is why hand-assembling `/lightning/r/Account/{id}/view` is a real defect rather than a style preference: it hard-codes one of those contexts and breaks silently in the others. The mixin is a superclass, not a decorator — `extends NavigationMixin(LightningElement)` — and it gives you exactly two methods: go there, or give me a URL for there.

## How it works

| Page reference `type` | Reaches |
|---|---|
| `standard__recordPage` | a record — `attributes: { recordId, objectApiName, actionName: 'view' \| 'edit' }` |
| `standard__objectPage` | list view or **new-record** page — `actionName: 'home' \| 'list' \| 'new'` |
| `standard__navItemPage` | a custom tab, by `apiName` |
| `standard__webPage` | an external URL, via `attributes: { url }` |
| `standard__component` | an Aura component exposed for navigation — the coexistence escape hatch |
| `comm__namedPage` / `standard__managedContentPage` | Experience Cloud pages |

- **`Navigate` and `GenerateUrl` are the only two methods.** `this[NavigationMixin.Navigate](ref, replace)` goes; `this[NavigationMixin.GenerateUrl](ref)` returns a **promise** of a URL for an `<a href>` — which matters for middle-click, "open in new tab" and accessibility.
- **`state` carries query parameters and everything in it must be a string.** Custom keys must be prefixed `c__`; unprefixed ones are reserved and silently dropped.
- **Prefill uses `encodeDefaultFieldValues`.** Import it from `lightning/pageReferenceUtils`, pass the result as `state.defaultFieldValues`, and it is honoured **only** on the `new` action — set it anywhere else and nothing happens, with no error.
- **`CurrentPageReference` is the read side.** `@wire(CurrentPageReference)` gives the component the reference it was rendered under, which is how you read `c__` parameters back out.
- **Console tabs need a different API.** Navigation opens a subtab; renaming, focusing or closing tabs is `lightning/platformWorkspaceApi` (`openTab`, `focusTab`, `setTabLabel`, `IsConsoleNavigation`), and calling it outside a console app is a no-op you must guard.

```js
import { NavigationMixin } from 'lightning/navigation';
import { encodeDefaultFieldValues } from 'lightning/pageReferenceUtils';

export default class NewCaseButton extends NavigationMixin(LightningElement) {
    @api recordId;
    handleClick() {
        this[NavigationMixin.Navigate]({
            type: 'standard__objectPage',
            attributes: { objectApiName: 'Case', actionName: 'new' },   // prefill ONLY works here
            state: { defaultFieldValues: encodeDefaultFieldValues({ AccountId: this.recordId,
                                                                    Subject: 'Follow-up' }) }
        });
    }
}
```

> **From my notes.** The old `Navigate to a Record's Create Page with Default Field Values` page pairs with a `Navigation` page whose example is `<lightning:pageReferenceUtils aura:id="pageRefUtils"/>` feeding `<a href="{!v.url}">`. **The technique survives; the implementation is Aura and does not port.** In LWC there is no component to drop in — `encodeDefaultFieldValues` is a plain import from the `lightning/pageReferenceUtils` *module*. The half of that note still worth keeping is the `GenerateUrl`-into-an-anchor shape, because it is the part people skip: `Navigate` on a `<div onclick>` gives you a destination no one can middle-click, bookmark, or reach with a keyboard.

## Gotchas

- **`state` values must be strings.** A number or boolean is coerced or dropped, and a record ID read back from `CurrentPageReference` is always a string.
- **Custom `state` keys without the `c__` prefix disappear**, silently.
- **`defaultFieldValues` is ignored outside `actionName: 'new'`** — including on `edit`, which is the usual wrong guess.
- **`GenerateUrl` returns a promise**, so the URL is not available during the first render; bind a tracked field set from `.then()`.
- **The mixin is not available everywhere.** It works in Lightning Experience, the mobile app and Experience Cloud sites, and not in Lightning Out or standalone apps — a component reused off-platform needs a fallback. → [22 · LWC OSS](22-lwc-open-source-and-off-platform-reuse.md)
- **Navigating to the page you are already on does not remount the component.** `CurrentPageReference` updates and the component re-renders — a `connectedCallback`-only refresh never fires. → [01](01-component-model-and-lifecycle.md)
- **`standard__webPage` to an internal path defeats the point.** If the destination is in the org, there is a typed page reference for it.

## Recall

Q: Why is building a URL string instead of a page reference a defect?
A: The navigation service resolves one reference differently per context — Lightning Experience, console, mobile, Experience Cloud. A literal URL hard-codes one and breaks in the rest.

Q: What are the two methods the navigation mixin provides?
A: `NavigationMixin.Navigate` to go somewhere, and `NavigationMixin.GenerateUrl` to get a promise of a URL for an anchor.

Q: How do you prefill fields on a new-record page, and where does it work?
A: `encodeDefaultFieldValues` from `lightning/pageReferenceUtils`, passed as `state.defaultFieldValues` — honoured only on `standard__objectPage` with `actionName: 'new'`.

Q: What is the rule for custom query parameters in `state`?
A: They must be strings and must be prefixed `c__`, or they are dropped without an error.

Q: What handles console tab behaviour, given navigation only opens subtabs?
A: `lightning/platformWorkspaceApi` — `openTab`, `focusTab`, `setTabLabel`, guarded by `IsConsoleNavigation`.

## Related

- [11 · LWC in Flow screens & quick actions](11-lwc-in-flow-screens-and-quick-actions.md) — the other way a component gets launched, and why navigation from one is different
- [01 · Component model & lifecycle](01-component-model-and-lifecycle.md) — why re-navigating does not re-run `connectedCallback`
- [06 · Lightning Data Service & UI API wires](06-lightning-data-service-and-ui-api-wires.md) — creating the record in place instead of navigating to a create page
