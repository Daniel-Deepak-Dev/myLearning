# Aura to LWR: Migration & Coexistence

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

**Scope:** What "move our site to LWR" actually costs, and how to decide whether to. The runtime comparison is [01](01-template-choice-and-site-landscape.md); the build model that makes the two incompatible is [02](02-lwr-architecture-and-build-model.md). Added in phase 18, beyond the original plan.

> **What changed.** *"Migrate to LWR before Aura is retired"* has a false premise and a false verb. **Aura templates are not retired and have no announced end-of-life** — Salesforce shipped features to them in Summer '26 → [01](01-template-choice-and-site-landscape.md). And **there is no migration.** No converter exists, in either direction. What is on offer is a **rebuild in a new site followed by a cutover**, typically weeks to months depending on complexity, and it should be scoped and justified as a project rather than accepted as maintenance.

## Core idea

The two runtimes share a builder and almost nothing else. Aura components cannot run in LWR; standard Aura site components frequently have no LWR equivalent; theme layouts and page layouts are a different component model → [04](04-experience-builder-layouts-and-theme-layouts.md); and the site's own metadata type may differ → [02](02-lwr-architecture-and-build-model.md). Nothing about the existing site is portable except business logic that already lives in Apex, and content that already lives in CMS.

So the honest decision is not *when* but *whether*, and it turns on one question: **does this site have a reason to be fast and findable?** A public, guest-heavy, SEO-relevant site gets a real return from LWR's build-and-cache model. An authenticated internal-ish partner portal behind a login, running happily on Partner Central, mostly does not — and rebuilding it buys a maintenance burden and a feature regression.

## How it works

- **Build in a new site; never convert in place.** The existing site keeps serving throughout, and the two coexist in the same org until cutover.
- **Work from a component inventory, not a page list.** For each component: does an LWR equivalent exist, must it be rewritten as LWC, or does the requirement go away?
- **Apex is the part that survives.** Controllers and services carry across — but re-check them against the 67.0 user-mode default and against guest exposure before reusing them → [06](06-custom-lwc-in-lwr-sites.md), [11](11-public-site-exposure-audit.md).
- **CSS does not survive.** Aura-era design tokens are inert under SLDS 2, and LWR brands through `--dxp` hooks → [05](05-branding-sets-design-tokens-and-slds-2.md).
- **Budget for the known gaps** — no generic record pages, a 500-route cap, thinner Chatter and CMS component coverage, and out-of-the-box Aura components with no counterpart → [01](01-template-choice-and-site-landscape.md).
- **Cutover is a URL problem.** The new site needs the old site's custom domain and URL paths, and anything indexed or bookmarked under the old ones must be redirected deliberately — the platform will not do it for you → [03](03-site-setup-domains-and-publishing.md).
- **Two sites means two guest users.** Audit both during the overlap, and retire the old site rather than leaving it inactive-but-published → [11](11-public-site-exposure-audit.md).

## Gotchas

- **"Aura is being retired" is the premise that gets these projects funded, and it is false.** Justify on performance, SEO or roadmap access instead — the case is real without the fiction.
- **The org may already be on LWR without being on *enhanced* LWR**, which is a much smaller upgrade and often the actual answer → [02](02-lwr-architecture-and-build-model.md).
- **Copying Aura sources into the existing project is the standard mistake.** A separate project keeps the running site clean.
- **Feature parity is not the goal and pretending otherwise sinks the project.** Decide up front what is not coming across.
- **SEO regresses at cutover unless redirects are planned**, and a public site's search ranking is often the reason for the move in the first place.
- **A B2B Commerce store has its own documented Aura-to-LWR path** and is not this project — do not generalise between them.

## Recall

Q: Is there a supported converter from an Aura Experience Cloud site to LWR?
A: No. The path is a rebuild in a new site followed by a cutover; the runtimes share only the builder.

Q: What is the false premise behind most Aura-to-LWR migration business cases?
A: That Aura templates are retired or dated. They aren't — they have no announced end-of-life and still received features in Summer '26.

Q: What actually carries across from the old site?
A: Apex logic and CMS content. Components, layouts and CSS do not.

Q: Which kind of site gets a genuine return from LWR?
A: A public, guest-heavy, SEO-relevant one, where the build-and-cache model pays. A logged-in partner portal on Partner Central usually doesn't.

Q: What is the commonly missed cutover risk?
A: URLs — the new site must take over the custom domain and paths, and old indexed or bookmarked links need deliberate redirection.

## Related

- [01 · Template choice & site landscape](01-template-choice-and-site-landscape.md) — the runtime trade this decision reopens
- [02 · LWR architecture & build model](02-lwr-architecture-and-build-model.md) — including the smaller LWR → enhanced LWR upgrade
- [03 · Site setup, domains & publishing](03-site-setup-domains-and-publishing.md) — the domain and URL mechanics of a cutover
- [11 · Public site exposure audit](11-public-site-exposure-audit.md) — two live sites means two guest surfaces
