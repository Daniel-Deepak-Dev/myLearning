# Template Choice & Site Landscape

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

**Scope:** The first irreversible decision on an Experience Cloud project — which runtime and template. What LWR buys and what it costs. The build model itself is [02](02-lwr-architecture-and-build-model.md); moving an existing Aura site is [12](12-aura-to-lwr-migration-and-coexistence.md).

> **What changed — and the correction is smaller than the internet's version.** *"Aura templates are retired, LWR is the default"* is **half wrong in a way that costs a scoping call**. LWR is the strategic runtime and where new capability lands. But **only two templates are LWR** — *Build Your Own (LWR)* and *Microsite (LWR)*. **Customer Service, Partner Central, Customer Account Portal, Help Center and Build Your Own are Aura templates, still creatable at 67.0, with no announced retirement date.** Choosing LWR for a service portal does not mean picking a different template; it means building from a blank canvas what Customer Service hands you free.

## Core idea

Experience Cloud is one product over three runtimes: **Aura**, **LWR**, and the legacy *Salesforce Tabs + Visualforce*. The template you pick at creation fixes the runtime **permanently** — there is no in-place converter, in either direction. So this is not a styling choice made in week one and revisited later; it decides your component library, your deployment metadata, your performance ceiling and your rebuild cost.

The honest framing is a trade, not an upgrade. LWR is faster, is where Salesforce is investing, and is the only runtime with a real SEO and CDN story. Aura is feature-rich out of the box and has purpose-built templates for the two commonest asks on the platform — a customer self-service portal and a partner portal. **LWR's advantage is the floor; Aura's advantage is the ceiling you get for free.**

## How it works

| Template | Runtime | Built for |
|---|---|---|
| **Build Your Own (LWR)** | LWR | blank canvas — the do-it-all LWR template |
| **Microsite (LWR)** | LWR | small, mostly unauthenticated marketing/landing sites |
| Customer Service | Aura | self-service: Knowledge, Cases, Chatter, search |
| Partner Central | Aura | channel sales — leads, opportunities, PRM |
| Customer Account Portal | Aura | account self-service, invoices, records |
| Help Center | Aura | public Knowledge search for guests |
| Build Your Own (Aura) | Aura | blank canvas on the Aura runtime |
| Salesforce Tabs + Visualforce | legacy | pre-template sites; not a new-build option |

- **The runtime decides the component library.** LWR runs **Lightning web components only** — an Aura component cannot run there at all, and many standard Aura site components have no LWR equivalent.
- **LWR has no generic record pages.** Record components live on object-specific pages; you cannot drop record detail onto an arbitrary site page the way Aura allows. This is the structural gap people meet in week two.
- **LWR sites cap at 500 routes** (unique URLs), which is a real ceiling for catalogue-shaped or Knowledge-shaped sites.
- **Chatter and parts of the CMS component set are thinner on LWR.** Summer '26 did move both forward — Chatter can be turned on in new orgs for Aura *and* LWR sites, and AI-assisted Self-Service components ship for both — but parity is not the assumption to plan against.
- **Guest-heavy and public means LWR**, because caching and SSR are only possible on a runtime that builds pages ahead of time → [02](02-lwr-architecture-and-build-model.md).

## 2026 currency

Summer '26's Experience Cloud items are additive rather than directional: 10 GB file uploads (was 2 GB) on Aura **and** LWR, AI-assisted Self-Service components on **both** runtimes, malware scanning for Salesforce Files GA, and Chatter enablement in new orgs. Read that list the right way — **Salesforce is still shipping to Aura sites in 2026**, which is the strongest available evidence against "Aura is retired". What is true is the asymmetry: enhanced CMS and Data 360 site integration are LWR-only, so the gap widens in one direction only. **Note that SSR is no longer part of that asymmetry** — Experience Delivery is being discontinued in Winter '27 and is closed to new enablement → [02](02-lwr-architecture-and-build-model.md), so the LWR case now rests on the static build, the CDN and where new capability lands.

## Gotchas

- **Template choice is permanent.** Changing runtime is a rebuild in a new site, then a cutover → [12](12-aura-to-lwr-migration-and-coexistence.md).
- **"LWR is the default" is a strategy statement, not a Setup fact** — the template gallery still offers more Aura templates than LWR ones.
- **Picking Build Your Own (LWR) for a service portal buys you a blank page.** Knowledge, case deflection, search and the Chatter feed are what Customer Service was giving you.
- **Microsite (LWR) is designed for unauthenticated visitors** — reaching for it because it sounds lightweight, then adding login, is the wrong starting point.
- **A managed-package LWC is hidden in Experience Builder** unless its metadata declares `lightningCommunity__RelaxedCSP` → [06](06-custom-lwc-in-lwr-sites.md).
- **The 100-site org cap counts everything** — active, inactive, preview and Visualforce sites → [03](03-site-setup-domains-and-publishing.md).

## Recall

Q: Which Experience Cloud templates are LWR-based?
A: Only two — Build Your Own (LWR) and Microsite (LWR). Customer Service, Partner Central, Customer Account Portal, Help Center and Build Your Own are Aura.

Q: Have Aura templates been retired?
A: No. They are legacy in direction only — still creatable at 67.0, still receiving Summer '26 features, with no announced retirement date.

Q: What does choosing LWR cost you on a self-service portal project?
A: Everything Customer Service gave you for free — Knowledge, case deflection, feed and search all become build work on a blank canvas.

Q: Can Aura components run in an LWR site?
A: No. LWR runs Lightning web components only, and there is no compatibility layer.

Q: What is the structural gap in LWR that surprises Aura developers?
A: No generic record pages — record components only work on object-specific pages — plus a 500-route cap per site.

## Related

- [02 · LWR architecture & build model](02-lwr-architecture-and-build-model.md) — why the runtime choice decides caching, SEO and deployment
- [12 · Aura to LWR: migration & coexistence](12-aura-to-lwr-migration-and-coexistence.md) — what "switch to LWR" actually costs
- [03-lwc · 22 LWC OSS & off-platform reuse](../03-lwc-and-slds/22-lwc-open-source-and-off-platform-reuse.md) — LWR as a runtime rather than a product
- [../CURRENCY.md](../CURRENCY.md) — the vault-wide record of what is retired and what only looks it
