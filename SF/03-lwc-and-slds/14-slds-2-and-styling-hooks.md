# SLDS 2 & Styling Hooks

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 06

**Scope:** Customising the look of base components and your own — which knobs are supported, and which SLDS version answers. How CSS reaches across a component boundary at all is [13](13-shadow-dom-styling-and-scoped-css.md).

> **What changed.** Overriding an SLDS class or a base component's internal selector was never supported — "SLDS classes and base component internals can change in future releases" — and **SLDS 2 makes it actively breaking**, because the CSS framework was rebuilt to separate structure from theme. Two corrections to how this is usually told: SLDS 2 went **GA in Winter '26**, not Summer '26 (Summer '26's contribution is the expanded Themes and Branding interface), and "use styling hooks instead" is only half the answer — **component hooks (`--slds-c-*`) are not supported in SLDS 2 at all.**

## Core idea

SLDS 2 splits a component's **structure** from its **theme**, and styling hooks are the seam. A hook is a CSS custom property the framework reads at render time, so it crosses the shadow boundary the way nothing else does ([13](13-shadow-dom-styling-and-scoped-css.md)) and it resolves against the org's current theme and colour mode rather than a value you hard-coded. That last part is the reason dark mode is possible at all, and the reason a hex code in a component stylesheet is now a bug with a delayed fuse: it looks fine today and is unreadable the moment a user turns dark mode on. The awkward truth for 2026 is that the hook surface is **not uniform across versions**. Global hooks (`--slds-g-*`) exist in both SLDS 1 and SLDS 2 and are the portable choice. Component hooks (`--slds-c-*`) are an SLDS 1 feature, and Salesforce's own guidance is that a component relying on them should **stay on SLDS 1 for now**.

## How it works

| Surface | Prefix / place | Status |
|---|---|---|
| Global styling hooks | `--slds-g-*` | supported in **both** SLDS 1 and SLDS 2 — the portable surface |
| Component styling hooks | `--slds-c-*` | SLDS 1 only — **not supported in SLDS 2** |
| Design tokens | Aura-era token files | **not supported in SLDS 2** — replace with global hooks |
| Class overrides (`.slds-button { … }`) | anywhere | never supported, breaks on upgrade |
| Themes and Branding | Setup → Themes and Branding | picks SLDS 1 vs SLDS 2 / Cosmos, and dark mode |

- **Set a hook, do not override a class.** Declaring `--slds-c-button-brand-color-background` in your component's CSS changes buttons *inside that component only*; restyling `.slds-button` reaches everything and breaks at the next release.
- **`:host` is where component-level hooks belong**, so the value applies to everything the component renders and inherits down. → [13](13-shadow-dom-styling-and-scoped-css.md)
- **Not every base component exposes hooks.** Toast, Tooltip, Links and Form Elements are documented as unsupported for custom-property styling — for those the answer is genuinely "you cannot", not "find a selector".
- **Turning on SLDS 2 is an org-level theme choice**, not a per-component one: Setup → Themes and Branding → the Salesforce Cosmos theme. New orgs in the supported editions are on it by default; existing orgs opt in.
- **Dark mode only exists in SLDS 2.** An SLDS 1 org must move to SLDS 2 first, then enable it per theme with *Let users enable Dark Mode*.

```css
:host {
    /* global hooks — resolve per theme AND per colour mode, and work in SLDS 1 and 2 */
    --my-card-bg: var(--slds-g-color-surface-container-1);
    --my-card-fg: var(--slds-g-color-on-surface-1);
}
.card { background: var(--my-card-bg); color: var(--my-card-fg); }
/* .slds-card { background: #fff; }   ← never. Unsupported, and dark mode makes it unreadable. */
```

## 2026 currency

**SLDS 2 and the Salesforce Cosmos theme are GA as of Winter '26** across the supported editions — on by default for new orgs, opt-in through Themes and Branding for existing ones — and **Summer '26 expands the no-code side**, with a Themes and Branding interface covering typography, shadows, sizing, spacing and illustration colour, plus an inline preview to check a theme before committing it. The migration story is the part to plan around, not the theming: **Aura-era design tokens do not work in SLDS 2 themes**, and the replacement is global styling hooks. Two tools do that mechanically rather than by grep — the **SLDS Linter** and the **SLDS Validator** find design tokens and unsupported overrides and propose global-hook replacements, and the Salesforce DX MCP server exposes the same SLDS guidance to an AI assistant. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **`--slds-c-*` hooks stop working when the org moves to SLDS 2.** They do not error — the component simply reverts to theme defaults.
- **Hard-coded hex values survive dark mode and ruin it.** A white background with theme-coloured text is the classic result.
- **A hook that does not exist fails silently**, which is why the fallback in `var(--slds-g-…, #0176d3)` is worth writing.
- **Overriding `.slds-*` classes can work for years and then break in one release.** "It works" was never the test; supported was.
- **SLDS 2 is org-wide.** You cannot preview it per component — test in a sandbox with the theme switched.
- **Toast, Tooltip, Links and Form Elements do not accept custom-property styling** at all.
- **Design tokens are not just deprecated, they are inert under SLDS 2** — a token-based stylesheet degrades quietly rather than failing loudly.

## Recall

Q: In which release did SLDS 2 become GA, and what did Summer '26 add?
A: GA in Winter '26. Summer '26 expanded the Themes and Branding interface — typography, shadows, sizing, spacing, illustration colour, with inline preview.

Q: Why is overriding an SLDS class unsupported rather than merely discouraged?
A: SLDS classes and base component internals are implementation detail and can change in any release; SLDS 2's rebuilt CSS framework is exactly that happening.

Q: What is the difference between `--slds-g-*` and `--slds-c-*`?
A: Global hooks work in both SLDS 1 and SLDS 2 and are the portable choice. Component hooks are SLDS 1 only and are not supported in SLDS 2.

Q: What happens to Aura-era design tokens under SLDS 2?
A: They stop working. Global styling hooks replace them, and the SLDS Linter/Validator find and convert them.

Q: What is the prerequisite for dark mode?
A: SLDS 2 — dark mode is exclusive to SLDS 2 themes, enabled per theme in Setup → Themes and Branding.

## Related

- [13 · Shadow DOM, styling & scoped CSS](13-shadow-dom-styling-and-scoped-css.md) — why custom properties are the only thing that reaches inside a component
- [01-admin · Lightning pages](../01-admin-and-declarative-platform/INDEX.md) — Themes and Branding as an admin surface
- [17 · Accessibility & internationalization](17-accessibility-and-internationalization.md) — colour contrast, which theme-aware hooks are meant to preserve
