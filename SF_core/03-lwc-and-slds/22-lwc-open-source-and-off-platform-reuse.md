# LWC Open Source & Off-Platform Reuse

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 07

**Scope:** How far a component travels — to another surface inside the org, and to a stack with no org at all. LWR *sites* are [05-experience](../05-experience-cloud-lwr/INDEX.md); this is the framework and the reuse boundary.

## Core idea

LWC is an open-source web-components framework that Salesforce also happens to run the platform on. `npm install lwc` gets you the real thing — compiler, engine, reactivity, `@api`/`@wire` — with no org, no CLI and no metadata. What you do **not** get is everything the platform layers on top: no `lightning/*` base components, no `@salesforce/*` scoped modules, no Lightning Data Service, no `NavigationMixin`, no Lightning Message Service, no Lightning Web Security. So portability is not a property of how well the component is written. **It is decided entirely by its import list.** A component importing only from `lwc` runs anywhere; one importing `lightning/navigation` and `@salesforce/apex/...` is a platform component that happens to be written in a portable framework. That is the whole calculation, and it is worth making *before* writing something you intend to reuse.

## How it works

| Import | On platform | Off platform |
|---|---|---|
| `lwc` (`LightningElement`, `api`, `wire`, `track`) | ✅ | ✅ |
| `lightning/*` base components | ✅ | ❌ not open source |
| `@salesforce/apex/*`, `/schema/*`, `/label/*`, `/i18n/*` | ✅ | ❌ compiler-resolved, no equivalent |
| `lightning/uiRecordApi` (LDS), `lightning/navigation`, LMS | ✅ | ❌ |
| Plain `fetch`, npm packages, your own modules | ⚠️ CSP / static resources | ✅ |

- **The engine ships as several packages.** `@lwc/engine-dom` renders in a browser, `@lwc/engine-server` and `@lwc/ssr-runtime` render to an HTML string on a server; they expose roughly the same API surface, `LightningElement` included.
- **Off-platform the shadow default flips.** Native shadow DOM is what you get; `@lwc/synthetic-shadow` is an opt-in polyfill — the reverse of Lightning Experience ([13](13-shadow-dom-styling-and-scoped-css.md)).
- **Lightning Web Runtime is the app framework**, and adds server-side rendering with client hydration — markup arrives before the JavaScript has downloaded and executed, then becomes interactive.
- **SLDS styling is separable from the base components.** You can adopt the CSS off-platform; the components that use it are not open source.
- **Design for the boundary deliberately** — keep presentational components pure and push every `@salesforce/*` import into a thin wrapper. That is the same instinct as extracting state ([24](24-lwc-state-managers.md)), for the same reason.

## 2026 currency

The OSS framework is at **`lwc` 9.x** on npm and moves on its own cadence, independent of the platform's API versions — the org is always some way behind, so a feature in the OSS changelog is not necessarily available in a component you deploy. Reach *inside* the platform grew this release: **Summer '26 allows custom LWCs to be embedded directly in Lightning dashboards** as widgets, configured inline in dashboard edit mode. That is the first supported route to a custom visualisation on a dashboard that does not involve a separate page or tab, and it is one more container with its own rules — the same portability question as toasts ([18](18-error-handling-and-user-feedback.md)) and navigation ([10](10-navigation-and-page-references.md)), where `NavigationMixin` is already documented as absent in Lightning Out and standalone apps. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **`lightning-*` base components are not open source.** Off-platform there is no `lightning-datatable` to install — the SLDS look is reproducible, the components are not.
- **`@salesforce/*` imports are resolved by the platform compiler**, not by Node. They are not npm packages and there is nothing to polyfill.
- **The OSS version and the org's API version are unrelated.** An `lwc` 9.x feature may not exist in a deployed component.
- **Shadow behaviour differs between the two worlds** — native off-platform, synthetic on. CSS and ARIA that work in one can fail in the other. → [17](17-accessibility-and-internationalization.md)
- **LWR SSR does not support synthetic shadow at all**, which quietly makes native shadow a prerequisite for server-side rendering.
- **A component built for reuse but importing `NavigationMixin` is not reusable** — it is absent in Lightning Out and standalone apps.
- **"It runs in Jest" is not "it runs off-platform".** Jest stubs `@salesforce/*` and `lightning/*`; a real off-platform build has nothing to stub with.

## Recall

Q: What single thing decides whether an LWC is portable off-platform?
A: Its import list. Only `lwc` itself is universal — `lightning/*` and `@salesforce/*` exist solely on the platform.

Q: Which shadow DOM mode is the default off-platform?
A: Native. `@lwc/synthetic-shadow` is an opt-in polyfill — the opposite of Lightning Experience, where synthetic is the default.

Q: What do `@lwc/engine-dom` and `@lwc/engine-server` do differently?
A: `engine-dom` renders into a browser DOM; `engine-server` (with `@lwc/ssr-runtime`) renders to an HTML string for server-side rendering, then the client hydrates it.

Q: Are the Lightning base components available in LWC OSS?
A: No. The framework is open source; the base component library is not. SLDS *styling* can be adopted separately.

Q: What new on-platform surface did Summer '26 open to custom LWCs?
A: Lightning dashboards — a custom component can be added as a dashboard widget and configured in dashboard edit mode.

## Related

- [13 · Shadow DOM, styling & scoped CSS](13-shadow-dom-styling-and-scoped-css.md) — why the synthetic/native default flip matters
- [10 · Navigation & page references](10-navigation-and-page-references.md) — `NavigationMixin`, the most common portability blocker
- [21 · Local dev & Live Preview](21-local-dev-and-lightning-dev-server.md) — the org-backed loop, and what replaces it when there is no org
- [23 · Static resources & third-party JavaScript](23-static-resources-and-third-party-javascript.md) — how off-platform npm habits have to change on-platform
- [05-experience · LWR sites](../05-experience-cloud-lwr/INDEX.md) — LWR as a Salesforce product rather than a runtime
