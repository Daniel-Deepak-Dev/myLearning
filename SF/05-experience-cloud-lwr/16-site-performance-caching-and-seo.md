# Site Performance, Caching & SEO 🆕

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 19

**Scope:** Why LWR sites are fast, how the caching layers stack, and what makes real SEO possible — the payoff of the build-and-serve architecture from [02](02-lwr-architecture-and-build-model.md). Where LWR genuinely differs from Aura is the whole point of this note.

## Core idea

LWR sites are **built and served, not rendered per request**. At publish time the platform compiles the site to static assets and pushes them to the Salesforce **CDN**; a page load hits the edge, not the app server. On top of that sits **server-side rendering (SSR)** — but read the currency note first: on this platform SSR is delivered by **Experience Delivery, which is still Beta**, not a GA guarantee. When it applies, HTML is produced server-side before hydration, so first paint is real content and a crawler sees rendered markup. Aura sites, by contrast, render client-side per request — slow first paint, poor crawlability. Everything here is a consequence of "static build + (beta) SSR + CDN"; if a claim doesn't trace back to that, distrust it.

## How it works

| Layer | What it caches | Scope |
|---|---|---|
| CDN edge | static assets, public pages | anonymous / guest |
| SSR output (Experience Delivery, **Beta**) | pre-rendered HTML | public pages |
| Browser | assets, hydrated state | per visitor |

- **SSR is for public, unauthenticated pages.** Authenticated, personalized pages can't share an edge cache the same way.
- **SEO essentials LWR gives you:** an auto-generated **sitemap**, clean URLs, and per-page meta / Open Graph settable in Experience Builder — plus server-rendered HTML *where Experience Delivery is enabled*.
- **Publish is the cache boundary.** Content goes live at publish, when the static build regenerates — not instantly on save.
- **Measure with Lighthouse** (performance, a11y, SEO, PWA). Aim for first contentful paint well under 1s on public pages; treat regressions as build problems.

## 2026 currency

The critical carry-forward from [02](02-lwr-architecture-and-build-model.md): **Experience Delivery (the SSR/edge-render path) is Beta**, GA-undated, and has been since Summer '24 — a performance or SEO plan that assumes SSR is on by default is wrong. Static build + CDN is the reliable baseline; SSR is an opt-in beta on top. Detail: [AI_Data/05-release-radar/README.md](../../AI_Data/05-release-radar/README.md).

## Gotchas

- **Don't assume SSR is on.** Experience Delivery is Beta and per-site — a public page may be client-rendered, which quietly guts its SEO.
- **SSR-safe components only.** A component touching `window`/`document` at module scope breaks the build; use `import.meta.env.SSR` to guard → [06](06-custom-lwc-in-lwr-sites.md).
- **Authenticated pages don't get the edge cache.** Benchmark the public path, not a logged-in page, before judging the site slow.
- **Stale content after publish** is usually CDN propagation lag, not a data bug.
- **Client-only rendering kills SEO.** A page that builds its content purely in JS after load hands the crawler an empty shell.
- **Meta tags are per-page and manual** — an unset title/description ships a generic one; SEO reviews catch this late.

## Recall

Q: What single architectural fact explains LWR's caching, SEO and SSR-safe rules?
A: LWR sites are built and served as static assets from a CDN (with optional SSR for public pages), not rendered per request like Aura.

Q: What is the status of SSR / Experience Delivery on LWR, and why does it matter?
A: It's still **Beta** and GA-undated — so a performance/SEO plan must not assume SSR is on by default; static build + CDN is the reliable baseline.

Q: What breaks server-side rendering (and the build) in a custom component?
A: Touching `window`/`document` at module scope — guard browser-only code with `import.meta.env.SSR` and defer it to a lifecycle hook.

Q: What does LWR give you for SEO regardless of SSR?
A: An auto-generated sitemap, clean URLs, and per-page meta/Open Graph tags; server-rendered HTML additionally requires Experience Delivery.

Q: When does a content change actually reach visitors?
A: At publish, when the static build regenerates and propagates to the CDN — not on save.

## Related

- [02 · LWR architecture & build model](02-lwr-architecture-and-build-model.md) — build-and-serve and the Beta status of Experience Delivery
- [06 · Custom LWC in LWR sites](06-custom-lwc-in-lwr-sites.md) — the SSR-safe component rules performance depends on
- [15 · Headless sites & Connect APIs](15-headless-sites-and-connect-apis.md) — where you take over SSR/SEO yourself
