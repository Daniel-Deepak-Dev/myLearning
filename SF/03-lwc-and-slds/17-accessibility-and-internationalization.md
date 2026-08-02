# Accessibility & Internationalization

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 07

**Scope:** Making a component usable by assistive technology and correct in another locale. Colour and contrast belong to [14](14-slds-2-and-styling-hooks.md); this covers semantics, focus, labels and formatting.

> **What changed.** The standard ARIA advice — "give the label an `id` and point `aria-labelledby` at it" — **does not work across a shadow boundary.** The docs are explicit: *"In native shadow DOM, you can't link IDs and ARIA attributes between elements in separate templates."* Worse, it often *appears* to work today, because synthetic shadow flattens IDs into one document — so an `aria-labelledby` written in 2021 silently breaks the day the component moves to native shadow ([13](13-shadow-dom-styling-and-scoped-css.md)). Prefer `aria-label`, or put both elements in the same root with light DOM.

## Core idea

Accessibility in LWC is mostly a question of *not fighting the base components*. `lightning-input`, `lightning-combobox` and the rest already wire `label`, `aria-describedby` on validation errors, and state attributes like `aria-hidden` as they change — a hand-rolled `<input>` starts from nothing and has to reproduce all of it. So the first rule is to use the base component and pass `label`, not to build the control and bolt ARIA on afterwards. Where you genuinely must build it, the shadow boundary is the constraint that makes web ARIA advice unreliable: anything that works by pointing an `id` at another element stops at the boundary. Internationalization has the opposite shape — the platform hands you the user's locale, currency, time zone and language as importable values, and the failure mode is ignoring them and hard-coding, not misusing them.

## How it works

- **`label` is not decoration.** On a base component it produces a properly associated label; `variant="label-hidden"` keeps it for screen readers while hiding it visually. That is the supported way to have an unlabelled-looking field.
- **`aria-*` on a custom element lands on the host**, not on anything inside it. `<c-my-input aria-label="Amount">` labels the wrapper — the inner `<input>` is unaffected.
- **Focus is a method, not an attribute.** Base components expose `focus()`; call it in `renderedCallback` guarded by a flag, since that hook runs on every render.
- **Locale arrives as imports, not as an API call** — `@salesforce/i18n/lang`, `/locale`, `/currency`, `/timeZone`, plus `/dir` for right-to-left. Feed them to `Intl.*`, or skip the work and use `lightning-formatted-number` / `lightning-formatted-date-time`, which already do.
- **All user-facing text goes through `@salesforce/label/c.myLabel`.** Custom Labels are the translatable surface; a string literal in a template cannot be translated by anyone.
- **Test with the keyboard first.** Tab through the component. If focus disappears, gets trapped, or lands somewhere invisible, no ARIA attribute will fix it.

> **From my notes.** `@salesforce modules or Importing SF values` collects the whole import surface in one component — `@salesforce/i18n/lang|locale|currency|timeZone`, `@salesforce/label/c.testCustomLabel`, `@salesforce/resourceUrl/...`, `@salesforce/user/Id`, `@salesforce/user/isGuest`, `@salesforce/client/formFactor` — and feeds them to `Intl.NumberFormat` and `Intl.DateTimeFormat`. **The pattern holds; the note is stale in two places.** Its `js-meta.xml` declares `<apiVersion>47.0</apiVersion>`, and `@salesforce/user/isGuest` reads very differently now that guest access is hardened → [05-experience · guest hardening](../05-experience-cloud-lwr/INDEX.md). Reach for `lightning-formatted-*` before hand-rolling `Intl` — the note pre-dates that being the easier answer.

## 2026 currency

The accessibility story is now coupled to the styling one. **SLDS 2 dark mode** means a hard-coded colour is an accessibility defect and not merely an aesthetic one — a fixed white background under a dark theme produces text that fails contrast outright, which is the practical reason global styling hooks are mandatory rather than tidy ([14](14-slds-2-and-styling-hooks.md)). The **Mixed Shadow Mode** migration is the other live risk: `shadowSupportMode = 'native'` is exactly the change that exposes every IDREF-based ARIA relationship written under synthetic shadow, and since migration runs leaves-first, it surfaces one component at a time rather than all at once.

## Gotchas

- **`aria-labelledby` and `aria-activedescendant` cannot cross a shadow root.** Use `aria-label`, or light DOM to put both elements in one root.
- **Synthetic shadow hides this bug.** IDs are flattened into one document, so the broken pattern works until the component goes native.
- **`placeholder` is not a label.** It disappears on input and several screen readers ignore it.
- **`lwc:dom="manual"` content is invisible to the framework** — nothing manages its ARIA or focus. → [23](23-static-resources-and-third-party-javascript.md)
- **`role` and `tabindex` on a `<div>` are a rebuild, not a shortcut.** A clickable div needs role, tabindex, Enter *and* Space handling, and a focus ring.
- **Hard-coded date and number formats break silently for other locales** — `MM/DD/YYYY` is simply wrong in most of the world, and nobody in the office will notice.
- **A hard-coded string in a template cannot be translated.** Custom Labels are the only translatable surface.
- **Time zone is per user, not per org.** `@salesforce/i18n/timeZone` is the running user's, which is the value a formatted date must use.

## Recall

Q: Why is `aria-labelledby` unreliable in LWC?
A: It works by IDREF, and IDs do not resolve across a shadow boundary. It appears to work under synthetic shadow because IDs are flattened, then breaks under native shadow.

Q: What does `variant="label-hidden"` do, and why is it better than omitting the label?
A: It hides the label visually while keeping it associated for assistive technology. Omitting the label leaves the control unnamed.

Q: Where does `<c-my-cmp aria-label="Total">` actually apply?
A: To the host element only. It does not reach any element inside the component's template.

Q: How does a component get the running user's locale and currency?
A: Import them — `@salesforce/i18n/locale`, `@salesforce/i18n/currency`, `@salesforce/i18n/timeZone`, `@salesforce/i18n/lang` — or let `lightning-formatted-*` apply them.

Q: What makes a hard-coded hex colour an accessibility problem rather than a styling one?
A: Under SLDS 2 dark mode the surrounding theme changes and the fixed colour does not, producing text that fails contrast.

## Related

- [13 · Shadow DOM, styling & scoped CSS](13-shadow-dom-styling-and-scoped-css.md) — why IDREFs stop at the boundary, and what Mixed Shadow Mode changes
- [14 · SLDS 2 & styling hooks](14-slds-2-and-styling-hooks.md) — theme-aware colour, and why dark mode makes contrast a code concern
- [18 · Error handling & user feedback](18-error-handling-and-user-feedback.md) — errors announced to assistive technology, not just displayed
- [23 · Static resources & third-party JavaScript](23-static-resources-and-third-party-javascript.md) — `@salesforce/resourceUrl`, and the a11y cost of manual DOM
