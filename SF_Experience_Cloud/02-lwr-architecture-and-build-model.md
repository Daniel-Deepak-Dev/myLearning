---
vault: SF_Experience_Cloud
format: dense
status: learning
created: 2026-08-04
updated: 2026-09-20
currency: "Summer '26 (API 67.0)"
phase: 18
tags: [currency-new, currency-warning]
---
# LWR Architecture & Build Model

**Scope:** The one fact that makes the rest of this area make sense — an LWR site is **built and served**, not rendered per request. Templates are [01](01-template-choice-and-site-landscape.md); the operational side of publishing is [03](03-site-setup-domains-and-publishing.md).

> **What changed, twice.** *"LWR is one thing"* is wrong: there is **LWR** and **enhanced LWR**, and they use different metadata types — `ExperienceBundle` versus `DigitalExperienceBundle` + `DigitalExperienceConfig`. And the *Upgrade to Enhanced LWR Sites* Release Update, **available Spring '25 and scheduled for enforcement in Spring '26, stopped being enforced from Summer '25** — Salesforce now recommends it rather than requiring it. So an inherited org can sit on non-enhanced LWR indefinitely, and any 2025 note promising a forced upgrade is stale.

## Core idea

Aura renders a page by shipping a framework to the browser and assembling components at runtime, per visitor, per request. **LWR compiles the site at publish time** into static, immutable, cacheable assets and serves those from a CDN. Everything downstream follows from that single difference: pages can be cached for guests, the first paint doesn't wait on a framework boot, a URL can return real HTML to a crawler, and *nothing you change is live until you publish*.

It also explains the constraints. A build step cannot run your browser code, so a component that touches `window` while the module loads breaks the build rather than the page → [07](07-guest-user-security-model.md) is the security half, [06](06-custom-lwc-in-lwr-sites.md) the authoring half. And immutable assets mean the deployment unit is the site, which is why enhanced LWR's **partial deployment** is a headline feature rather than plumbing.

## How it works

| | LWR (non-enhanced) | Enhanced LWR |
|---|---|---|
| Metadata | `ExperienceBundle` | `DigitalExperienceBundle` + `DigitalExperienceConfig` |
| Deployment | whole site | **partial deployment** |
| CMS | classic workspaces | **enhanced workspaces & channels**, variations, collections |
| Visibility rules | component-level | **expression-based visibility** |
| Data 360 | — | site can be connected as a source |

- **Publish is a build.** Preview reflects the builder; the live site reflects the last publish. Two people editing and one publishing ships both sets of changes.
- **Upgrade path is one-way**, from Experience Builder → *Settings* → *Updates* → **Upgrade**. Treat it as a migration with a regression test, not a checkbox.
- **Experience Delivery was the *hosting* tier, not SSR itself, and it is discontinued as of Winter '27.** It never left Beta. It applied to **Build Your Own (LWR)** in Enterprise, Performance and Unlimited — never Developer Edition — and served through **Cloudflare** rather than the default **Akamai** → [03](03-site-setup-domains-and-publishing.md). **Republishing a site that still sits on it migrates that site to standard LWR infrastructure automatically.** A site left unpublished keeps serving, but its performance degrades over time.
- **SSR did not leave with it.** Server-side rendering on **islands architecture** is a standard LWR Experience Cloud capability, and it is **on by default on the standard pages of Build Your Own (LWR)**. The gate is the **theme layout**: a page is server-rendered only if its theme layout declares the `lightning__ServerRenderable` capability — a custom theme layout that omits it makes the whole route client-rendered → [04](04-experience-builder-layouts-and-theme-layouts.md).
- **Components opt in by capability, not by directive.** `lightning__ServerRenderable` server-renders a component that will never change after render; `lightning__ServerRenderableWithHydration` server-renders it and then hydrates it into an interactive island. Everything unmarked stays client-rendered.
- **Synthetic shadow DOM is not supported under SSR.** SSR components use native shadow or light DOM → [03-lwc · 13](../SF_core/03-lwc-and-slds/13-shadow-dom-styling-and-scoped-css.md).
- **500 routes per site** is the hard structural ceiling on how many unique URLs the build can produce.

## 2026 currency

Two things worth carrying, and both are the same lesson from opposite ends. **Experience Delivery arrived in Summer '24, never left Beta, and is discontinued as of Winter '27** — a Beta that shipped improvements for two years was still withdrawn, so "we'll turn on Experience Delivery" is a plan with no feature behind it. And the **enhanced-LWR Release Update was de-enforced**: an announced enforcement that did not happen. Neither a promised arrival nor a promised deadline is a fact — verify both against Setup and the current doc before quoting either.

**Read the withdrawal narrowly, though.** Experience Delivery was the Cloudflare-backed hosting and edge tier. **Islands SSR is a separate thing and it survives** on standard LWR infrastructure, gated by the `lightning__ServerRenderable` capability on the theme layout. "Experience Delivery is gone, therefore LWR has no SSR" is the overcorrection — and it is the one this vault made in its own first draft.

## Gotchas

- **Non-enhanced LWR and Aura share a metadata type.** `ExperienceBundle` in a repo does not tell you the runtime — check the template → [12](12-aura-to-lwr-migration-and-coexistence.md).
- **Nothing ships without a publish**, including CMS content changes routed through the site.
- **Do not design around Experience Delivery.** It is gone as of Winter '27, and it never ran on Developer Edition, so no scratch-org demo ever proved it. **Do not conclude that SSR went with it** — islands SSR is still there, on standard infrastructure.
- **A custom theme layout silently switches SSR off for every page that uses it** unless it declares `lightning__ServerRenderable`. The page still works; it just becomes client-rendered, and nothing warns you → [04](04-experience-builder-layouts-and-theme-layouts.md).
- **`import.meta.env.SSR` guards code, it does not make it portable.** Module-scope browser access still breaks the build → [06](06-custom-lwc-in-lwr-sites.md).
- **A hydration mismatch is a UI defect, not a warning to ignore** — the framework recovers by re-rendering, which is the flicker your stakeholder screenshots.
- **Upgrading to enhanced LWR changes what the pipeline retrieves.** Plan the DevOps change with the upgrade, not after it → [09-devops · 05](../SF_core/09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md).

## Recall

Q: What single fact explains LWR's caching, SEO and component rules?
A: An LWR site is built at publish time into static, immutable, cacheable assets and served from a CDN — it is not rendered per request.

Q: Which metadata types distinguish enhanced LWR from non-enhanced?
A: Enhanced uses `DigitalExperienceBundle` and `DigitalExperienceConfig`; non-enhanced LWR — like Aura — uses `ExperienceBundle`.

Q: Is the Upgrade to Enhanced LWR Sites Release Update enforced?
A: No. Available Spring '25 and scheduled for Spring '26, but not enforced since Summer '25 — it is a recommendation.

Q: What is the status and scope of Experience Delivery?
A: **Discontinued as of Winter '27.** It was the Cloudflare-backed hosting tier — Beta from Summer '24, Build Your Own (LWR) only, Enterprise/Performance/Unlimited, no Developer Edition. Republishing migrates a site to standard LWR infrastructure.

Q: Did SSR go away with Experience Delivery?
A: No. Islands SSR is a standard LWR Experience Cloud capability and is on by default on Build Your Own (LWR) standard pages. Experience Delivery was the hosting tier, not the rendering model.

Q: What switches SSR on for an LWR page, and what turns it off by accident?
A: The theme layout's `lightning__ServerRenderable` capability. A custom theme layout that omits it makes the entire route client-rendered, silently.

## Related

- [06 · Custom LWC in LWR sites](06-custom-lwc-in-lwr-sites.md) — the SSR-safe authoring rules this model imposes
- [03 · Site setup, domains & publishing](03-site-setup-domains-and-publishing.md) — the CDN and publish mechanics in operational terms
- [03-lwc · 13 Shadow DOM, styling & scoped CSS](../SF_core/03-lwc-and-slds/13-shadow-dom-styling-and-scoped-css.md) — why SSR forces native shadow or light DOM
- [09-devops · 05 Metadata API & deployment mechanics](../SF_core/09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md) — the two bundle types in a pipeline
