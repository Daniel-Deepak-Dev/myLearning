---
vault: SF_Experience_Cloud
format: dense
status: learning
created: 2026-08-04
updated: 2026-09-20
currency: "Summer '26 (API 67.0)"
phase: 19
tags: [currency-new, currency-warning]
---
# Site Performance, Caching & SEO

**Scope:** Why LWR sites are fast, how the caching layers stack, and what makes real SEO possible — the payoff of the build-and-serve architecture from [02](02-lwr-architecture-and-build-model.md). Where LWR genuinely differs from Aura is the whole point of this note.

> **What changed — and this note's own second draft was the bigger error.** Almost every LWR performance article treats **Experience Delivery** as the SSR tier you switch on. It is **discontinued as of Winter '27**, and republishing an affected site migrates it to standard LWR infrastructure. The overcorrection — the one this note previously made — is concluding that LWR therefore has no server-side rendering. **It does.** Islands SSR is a standard LWR Experience Cloud capability, on by default on the standard pages of Build Your Own (LWR). What was withdrawn was the Cloudflare-backed **hosting** tier, not the rendering model → [02](02-lwr-architecture-and-build-model.md).

## Core idea

LWR sites are **built and served, not rendered per request**. At publish time the platform compiles the site to static assets and pushes them to the Salesforce **CDN**; a page load hits the edge, not the app server. On top of that, **pages whose theme layout declares `lightning__ServerRenderable` are rendered to HTML on the server**, and only the components that asked for hydration become interactive islands. So a crawler on a default Build Your Own (LWR) page receives real HTML, not an empty shell. Aura sites, by contrast, render client-side per request with no static build at all — which is the gap that makes LWR the only runtime with a serious SEO story. Everything here is a consequence of "built ahead of time, served from the edge"; if a claim doesn't trace back to that, distrust it.

## How it works

| Layer | What it caches | Scope |
|---|---|---|
| CDN edge | static assets, public pages | anonymous / guest |
| Server-side render (islands) | HTML produced ahead of the browser | per page, via the theme layout's `lightning__ServerRenderable` |
| Browser | assets, hydrated state | per visitor |

- **The edge cache is for public, unauthenticated pages.** Authenticated, personalized pages can't share it the same way.
- **SEO essentials LWR gives you:** server-rendered HTML on SSR-enabled pages, an auto-generated **sitemap**, clean URLs, and per-page meta / Open Graph settable in Experience Builder.
- **A custom theme layout is the usual way a site loses SSR.** Omit `lightning__ServerRenderable` from it and every page using it goes client-rendered — no error, just a worse crawl → [04](04-experience-builder-layouts-and-theme-layouts.md).
- **Publish is the cache boundary.** Content goes live at publish, when the static build regenerates — not instantly on save.
- **Measure with Lighthouse** (performance, a11y, SEO). **Salesforce publishes no Lighthouse budget for Experience Cloud** — the only first-party performance figure was the "subsecond page loads" claim attached to Experience Delivery, which has been withdrawn. Set your own budget from a measured baseline of the site's own public pages and gate regressions against it; a number quoted from a blog is not a target.

## 2026 currency

The critical carry-forward from [02](02-lwr-architecture-and-build-model.md): **Experience Delivery is discontinued as of Winter '27.** It was Beta from Summer '24 and never flipped, and a republish moves an affected site onto standard LWR infrastructure. What it took with it was the Cloudflare edge tier and the subsecond-page-load marketing claim — **not** server-side rendering, which remains a capability of standard LWR. The useful lesson is about reading a withdrawal precisely: the first draft of this note under-read it and planned around SSR as a toggle; the second over-read it and declared SSR dead. **Name the thing that was withdrawn, not the category it sat in.**

## Gotchas

- **Don't plan around *Experience Delivery*** — it is gone. Do plan around SSR, which is not.
- **Verify SSR is actually on for your pages** rather than assuming the template default survived. A custom theme layout is the common way it quietly turns off.
- **SSR-safe component discipline is not optional.** Module-scope `window`/`document` access breaks a server-rendered page; guard it with `import.meta.env.SSR` → [06](06-custom-lwc-in-lwr-sites.md).
- **Authenticated pages don't get the edge cache.** Benchmark the public path, not a logged-in page, before judging the site slow.
- **Stale content after publish** is usually CDN propagation lag, not a data bug.
- **Client-only rendering kills SEO.** A page that builds its content purely in JS after load hands the crawler an empty shell.
- **Meta tags are per-page and manual** — an unset title/description ships a generic one; SEO reviews catch this late.
- **The sitemap and "clean URLs" claims above are untested on a multilingual site.** Whether the sitemap emits per-language URLs, whether anything emits `hreflang`, and whether the edge caches a page once or once per language are all open → [21](21-multilingual-sites-and-translation.md).

## Recall

Q: What single architectural fact explains LWR's caching, SEO and SSR-safe rules?
A: LWR sites are built and served from a CDN, not rendered per request like Aura.

Q: What is the status of Experience Delivery, and what did it actually take with it?
A: **Discontinued as of Winter '27**; republishing migrates the site to standard LWR infrastructure. It was the Cloudflare hosting and edge tier — it did *not* take server-side rendering, which remains a standard LWR capability.

Q: What breaks server-side rendering (and the build) in a custom component?
A: Touching `window`/`document` at module scope — guard browser-only code with `import.meta.env.SSR` and defer it to a lifecycle hook.

Q: What does LWR give you for SEO?
A: Server-rendered HTML on SSR-enabled pages, an auto-generated sitemap, clean URLs, and per-page meta/Open Graph tags.

Q: When does a content change actually reach visitors?
A: At publish, when the static build regenerates and propagates to the CDN — not on save.

## Related

- [02 · LWR architecture & build model](02-lwr-architecture-and-build-model.md) — build-and-serve, the SSR capabilities, and Experience Delivery's withdrawal
- [06 · Custom LWC in LWR sites](06-custom-lwc-in-lwr-sites.md) — the SSR-safe component rules performance depends on
- [15 · Headless sites & Connect APIs](15-headless-sites-and-connect-apis.md) — where you take over SSR/SEO yourself
- [21 · Multilingual sites & site translation](21-multilingual-sites-and-translation.md) — carries the open questions a second language puts to this note's caching and sitemap story
