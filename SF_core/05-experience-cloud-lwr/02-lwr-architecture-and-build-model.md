# LWR Architecture & Build Model

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

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
- **Experience Delivery was the SSR + CDN tier, and it is being discontinued in Winter '27.** It never left Beta. **If you did not already enable it, it is no longer available to turn on**; orgs that did may run it until **October 2026**, and Salesforce recommends disabling it first. It applied to **Build Your Own (LWR)** in Enterprise, Performance and Unlimited — never Developer Edition — served through **Cloudflare** rather than the default **Akamai** → [03](03-site-setup-domains-and-publishing.md).
- **SSR is opt-in per page, not per site**, and uses **islands architecture**: the page renders to HTML on the server and only components marked for hydration (`lwr:hydrate`) become interactive. The rest stays static HTML.
- **Synthetic shadow DOM is not supported under SSR.** SSR components use native shadow or light DOM → [03-lwc · 13](../03-lwc-and-slds/13-shadow-dom-styling-and-scoped-css.md).
- **500 routes per site** is the hard structural ceiling on how many unique URLs the build can produce.

## 2026 currency

Two things worth carrying, and both are the same lesson from opposite ends. **Experience Delivery arrived in Summer '24, never left Beta, and is being discontinued in Winter '27** — new enablement is already closed, existing sites run until **October 2026**. A Beta that ships improvements for two years can still be withdrawn, so "we'll turn on Experience Delivery" is now not a plan with a Beta dependency, it is a plan with no feature behind it. And the **enhanced-LWR Release Update was de-enforced**: an announced enforcement that did not happen. Neither a promised arrival nor a promised deadline is a fact — verify both against Setup and the current doc before quoting either.

## Gotchas

- **Non-enhanced LWR and Aura share a metadata type.** `ExperienceBundle` in a repo does not tell you the runtime — check the template → [12](12-aura-to-lwr-migration-and-coexistence.md).
- **Nothing ships without a publish**, including CMS content changes routed through the site.
- **Do not design around Experience Delivery.** It is closed to new enablement and gone in Winter '27 — any SSR performance story that depends on it needs another answer. It also never ran on Developer Edition, so no scratch-org demo ever proved it.
- **`import.meta.env.SSR` guards code, it does not make it portable.** Module-scope browser access still breaks the build → [06](06-custom-lwc-in-lwr-sites.md).
- **A hydration mismatch is a UI defect, not a warning to ignore** — the framework recovers by re-rendering, which is the flicker your stakeholder screenshots.
- **Upgrading to enhanced LWR changes what the pipeline retrieves.** Plan the DevOps change with the upgrade, not after it → [09-devops · 05](../09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md).

## Recall

Q: What single fact explains LWR's caching, SEO and component rules?
A: An LWR site is built at publish time into static, immutable, cacheable assets and served from a CDN — it is not rendered per request.

Q: Which metadata types distinguish enhanced LWR from non-enhanced?
A: Enhanced uses `DigitalExperienceBundle` and `DigitalExperienceConfig`; non-enhanced LWR — like Aura — uses `ExperienceBundle`.

Q: Is the Upgrade to Enhanced LWR Sites Release Update enforced?
A: No. Available Spring '25 and scheduled for Spring '26, but not enforced since Summer '25 — it is a recommendation.

Q: What is the status and scope of Experience Delivery?
A: **Being discontinued in Winter '27** and already closed to new enablement; existing sites run until October 2026. It was Beta from Summer '24, Build Your Own (LWR) only, Enterprise/Performance/Unlimited, no Developer Edition, served via Cloudflare.

Q: What does islands architecture mean for an SSR page?
A: The page is server-rendered to HTML and only components marked with `lwr:hydrate` become interactive; everything else stays static.

## Related

- [06 · Custom LWC in LWR sites](06-custom-lwc-in-lwr-sites.md) — the SSR-safe authoring rules this model imposes
- [03 · Site setup, domains & publishing](03-site-setup-domains-and-publishing.md) — the CDN and publish mechanics in operational terms
- [03-lwc · 13 Shadow DOM, styling & scoped CSS](../03-lwc-and-slds/13-shadow-dom-styling-and-scoped-css.md) — why SSR forces native shadow or light DOM
- [09-devops · 05 Metadata API & deployment mechanics](../09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md) — the two bundle types in a pipeline
