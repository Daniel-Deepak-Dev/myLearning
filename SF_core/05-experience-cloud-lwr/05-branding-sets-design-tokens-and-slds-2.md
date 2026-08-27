# Branding Sets, Design Tokens & SLDS 2

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

**Scope:** Making a site look like the brand rather than like Salesforce — the LWR styling hook system, branding sets, and where SLDS 2 lands. The org-wide SLDS 2 story is [03-lwc · 14](../03-lwc-and-slds/14-slds-2-and-styling-hooks.md); this note owns the site-specific layer.

## Core idea

LWR branding is a **cascade of CSS custom properties**, not a stylesheet you override. Experience Builder's Theme panel writes values into `--dxp-*` custom properties; those map down onto the lower-level component hooks; components consume them. Set one `--dxp` hook and dozens of components change together — which is the entire design intent, and the reason hand-written CSS overriding a component's internals is the wrong instinct here.

Everything else is packaging around that. A **branding set** is a named collection of those values, and a site can hold several and switch between them — the mechanism behind seasonal skins, sub-brands and audience-specific looks without a second site.

## How it works

- **`--dxp-*` is LWR's own reduced hook vocabulary.** It sits above SLDS's component hooks deliberately: fewer knobs, broader effect. `--dxp-g-root` is the one to know — it maps to the Theme panel's background colour selector.
- **The Theme panel is the no-code face of the same properties.** Every control in it writes one or more of these values; nothing is available there that is not expressible as a hook.
- **Branding sets are per-site and switchable**, and are the right answer whenever someone asks for "the same site but in the partner colours".
- **Custom CSS goes in the site's CSS editor or in a component's own stylesheet**, and should set custom properties rather than target another component's internals — which shadow DOM will stop you doing anyway → [03-lwc · 13](../03-lwc-and-slds/13-shadow-dom-styling-and-scoped-css.md).
- **Fonts, spacing and imagery ride the same route.** Static assets referenced from CSS come from static resources or CMS, and their cache headers matter for guests → [03-lwc · 23](../03-lwc-and-slds/23-static-resources-and-third-party-javascript.md).

## 2026 currency

**SLDS 2 replaces design tokens with global styling hooks, and this is where an Experience Cloud site feels it first.** Aura-era standard design tokens still work in SLDS 1 themes and are **not included in SLDS 2 themes** — a site branded through tokens looks unstyled rather than differently styled after the switch. Carry two rules across from [03-lwc · 14](../03-lwc-and-slds/14-slds-2-and-styling-hooks.md) unchanged: **`--slds-g-*` global hooks work in both versions and are the portable surface**, and **component-level `--slds-c-*` hooks are not supported in SLDS 2**, so a component that depends on them should stay on SLDS 1 for now. SLDS 2 and the Cosmos theme have been GA since Winter '26, and **dark mode is exclusive to SLDS 2** — which is the first branding request that forces the decision rather than deferring it.

## Gotchas

- **Design tokens are inert under SLDS 2**, so a token-branded site degrades silently. SLDS Linter and SLDS Validator are the conversion tools.
- **`--dxp` and `--slds` are two levels of the same cascade, not alternatives.** Reach for `--dxp` first; drop to `--slds-g-*` only when the coarse hook doesn't reach.
- **A branding set changes values, not structure.** Anything hardcoded in a custom component's CSS ignores it entirely — which is how one component stays blue forever.
- **Theme-panel changes are not live until publish**, like everything else in the builder → [03](03-site-setup-domains-and-publishing.md).
- **Shadow DOM blocks descendant selectors into another component**, so "just override the class" is not available. Custom properties pierce; selectors don't.
- **Dark mode is an SLDS 2 decision, not a toggle** — asking for it commits the site to the new styling model and the `--slds-c-*` carve-out above.

## Recall

Q: What is the `--dxp-*` custom property system for?
A: LWR's reduced set of styling hooks that map onto lower-level component hooks, so one value brands many components at once.

Q: What happened to standard design tokens under SLDS 2?
A: They aren't included — SLDS 2 replaces them with global styling hooks, so token-branded sites lose their branding rather than change it.

Q: Which styling hooks are portable across SLDS 1 and SLDS 2?
A: The global `--slds-g-*` hooks. Component-level `--slds-c-*` hooks are not supported in SLDS 2.

Q: What is a branding set?
A: A named, switchable collection of a site's branding property values — the mechanism for sub-brands and seasonal skins within one site.

Q: Why can't you brand a component by overriding its CSS classes?
A: Shadow DOM scopes styles, so selectors don't reach in. Custom properties do, which is why the whole system is built on them.

## Related

- [03-lwc · 14 SLDS 2 & styling hooks](../03-lwc-and-slds/14-slds-2-and-styling-hooks.md) — the platform-wide version of the SLDS 2 rules cited here
- [04 · Experience Builder layouts & theme layouts](04-experience-builder-layouts-and-theme-layouts.md) — the chrome these values paint
- [03-lwc · 13 Shadow DOM, styling & scoped CSS](../03-lwc-and-slds/13-shadow-dom-styling-and-scoped-css.md) — why custom properties are the only styling surface that crosses a boundary
- [03-lwc · 23 Static resources & third-party JavaScript](../03-lwc-and-slds/23-static-resources-and-third-party-javascript.md) — fonts and imagery, and the guest caching rule
