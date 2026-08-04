# Custom LWC in LWR Sites

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

**Scope:** Writing a Lightning web component that survives an LWR site — the target vocabulary, the imports that fail off Lightning Experience, and the SSR rules. Layout components are [04](04-experience-builder-layouts-and-theme-layouts.md); the LWC framework itself is [03-lwc](../03-lwc-and-slds/INDEX.md).

## Core idea

A component is only as portable as its container-dependent imports and its assumptions about *when* it runs. An LWR site breaks both assumptions at once: there is no Lightning Experience shell around it, and under SSR there is no browser at all when the component first renders. Neither failure is loud. A missing container makes a toast vanish silently; a browser assumption under SSR makes the build fail or the page flicker.

The discipline that fixes both is the same one: **decide, per piece of code, whether it must run on the server, the client, or both** — and put it somewhere that matches.

## How it works

```js
// runs on server and client — keep it portable and synchronous
connectedCallback() {
  if (!import.meta.env.SSR) {
    window.addEventListener('resize', this.onResize);   // client-only
  }
}
renderedCallback() { /* safe place for browser APIs and async work */ }
```

- **Four targets matter.** `lightningCommunity__Page` exposes the component to the builder; `lightningCommunity__Default` is what makes its properties editable; `lightningCommunity__Page_Layout` and `lightningCommunity__Theme_Layout` are the structural ones → [04](04-experience-builder-layouts-and-theme-layouts.md).
- **A managed-package LWC is hidden from the Components panel** unless its metadata declares **`lightningCommunity__RelaxedCSP`**.
- **SSR requires portable *and* synchronous code** in `connectedCallback()` and in getters. Async work belongs in `renderedCallback()` or an event handler — never in `connectedCallback()`.
- **`window` and `document` are undefined on the server.** Guard with `import.meta.env.SSR`, or keep the code out of the SSR path entirely.
- **`ShowToastEvent` does not work in LWR sites.** It needs a Lightning Experience container and fails **silently**; use **`lightning/toast`** with **`lightning/toastContainer`** → [03-lwc · 18](../03-lwc-and-slds/18-error-handling-and-user-feedback.md).
- **`NavigationMixin` behaves differently** — LWR routing is the site's own, and page references resolve against site pages, not app pages → [03-lwc · 10](../03-lwc-and-slds/10-navigation-and-page-references.md).
- **Synthetic shadow is unavailable under SSR**, so an SSR component uses native shadow or light DOM, and inherits native shadow's ARIA-by-IDREF restriction → [03-lwc · 17](../03-lwc-and-slds/17-accessibility-and-internationalization.md).
- **`sf lightning dev site` previews the real site locally**, which is the only fast loop available here → [03-lwc · 21](../03-lwc-and-slds/21-local-dev-and-lightning-dev-server.md).

## 2026 currency

The security default that reached Apex at 67.0 matters more here than anywhere else in the vault. **An `@AuraEnabled` method behind a component on a public page is an endpoint a stranger can call**, and a class compiled at 67.0 now enforces object permissions, FLS and sharing by default — which is protection you inherit rather than protection you wrote. The corollary is the dangerous one: **an older Apex class, or one that opts out with `AccessLevel.SYSTEM_MODE`, still runs as the guest user with the model switched off**, and the component around it is not a boundary. This is precisely the shape the 2026 campaign against Experience Cloud sites exploited → [11](11-public-site-exposure-audit.md), [07-security · 14](../07-security-and-sharing/14-code-execution-context-and-security.md).

## Gotchas

- **Toasts fail silently in LWR.** No error, no toast, and it works fine in your dev org's Lightning Experience.
- **Module-scope browser access breaks the build**, not the page — the error arrives at publish and reads like a bundler problem.
- **`renderedCallback()` runs repeatedly.** Guarding client-only work with a flag is not optional there.
- **A hydration mismatch shows as UI shifting**, because the framework silently re-renders to recover. Test with the SSR assertions rather than by eye.
- **Base components are not uniformly SSR-capable.** Experience Delivery has been adding support release by release; check before assuming.
- **An old Apex class behind a guest-facing component bypasses the access model** even though a 67.0 class would not → [07](07-guest-user-security-model.md).

## Recall

Q: Which target makes a component's properties editable in Experience Builder?
A: `lightningCommunity__Default`, declared alongside the target that exposes the component.

Q: Why does `ShowToastEvent` do nothing in an LWR site?
A: It's a bubbling event that needs a Lightning Experience container. Use `lightning/toast` with `lightning/toastContainer`.

Q: What are the two constraints on code that runs during SSR?
A: It must be portable — no browser APIs — and synchronous. So no async work in `connectedCallback()` or getters.

Q: How does a component detect that it's running on the server?
A: The `import.meta.env.SSR` boolean is true during server-side rendering and falsy on the client.

Q: Is a guest-facing `@AuraEnabled` method protected by the component in front of it?
A: No. It's an endpoint; its own checks are the boundary — and a pre-67.0 class isn't enforcing the access model at all.

## Related

- [04 · Experience Builder layouts & theme layouts](04-experience-builder-layouts-and-theme-layouts.md) — the structural targets and slots
- [11 · Public site exposure audit](11-public-site-exposure-audit.md) — what an unguarded guest-facing controller costs
- [03-lwc · 18 Error handling & user feedback](../03-lwc-and-slds/18-error-handling-and-user-feedback.md) — the toast portability rule in full
- [03-lwc · 21 Local dev & the Lightning dev server](../03-lwc-and-slds/21-local-dev-and-lightning-dev-server.md) — `sf lightning dev site`
