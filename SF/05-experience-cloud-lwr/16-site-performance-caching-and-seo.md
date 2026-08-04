# Site Performance, Caching & SEO

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 19

**Scope:** Why LWR sites are fast, how the caching layers stack, and what makes real SEO possible — the payoff of the build-and-serve architecture from [02](02-lwr-architecture-and-build-model.md). Where LWR genuinely differs from Aura is the whole point of this note.

> **What changed.** Almost every LWR performance article — including this note's own first draft — treats **Experience Delivery** as the SSR tier you switch on. **It is being discontinued in Winter '27, and it is already closed to new enablement**: if your org never turned it on, there is no toggle. Orgs that did have until **October 2026**. So the honest baseline is **static build + CDN with no SSR**, and any SEO plan that assumed server-rendered HTML needs rebuilding around prerendered static output instead.

## Core idea

LWR sites are **built and served, not rendered per request**. At publish time the platform compiles the site to static assets and pushes them to the Salesforce **CDN**; a page load hits the edge, not the app server. **That is the whole performance story now** — the SSR tier on top of it, Experience Delivery, is being withdrawn and cannot be newly enabled, so for any site you build today HTML is *not* produced server-side and a crawler receives the built static shell plus client-side hydration. Aura sites, by contrast, render client-side per request with no static build at all — which is why LWR still wins on first paint and crawlability without SSR. Everything here is a consequence of "static build + CDN"; if a claim doesn't trace back to that, distrust it.

## How it works

| Layer | What it caches | Scope |
|---|---|---|
| CDN edge | static assets, public pages | anonymous / guest |
| SSR output (Experience Delivery) | pre-rendered HTML | **withdrawn — Winter '27, no new enablement** |
| Browser | assets, hydrated state | per visitor |

- **The edge cache is for public, unauthenticated pages.** Authenticated, personalized pages can't share it the same way.
- **SEO essentials LWR gives you without SSR:** an auto-generated **sitemap**, clean URLs, and per-page meta / Open Graph settable in Experience Builder. These are the whole toolkit now — treat them as such rather than as a supplement to server rendering.
- **Publish is the cache boundary.** Content goes live at publish, when the static build regenerates — not instantly on save.
- **Measure with Lighthouse** (performance, a11y, SEO). **Salesforce publishes no Lighthouse budget for Experience Cloud** — the only first-party performance figure was the "subsecond page loads" claim attached to Experience Delivery, which is being withdrawn. Set your own budget from a measured baseline of the site's own public pages and gate regressions against it; a number quoted from a blog is not a target.

## 2026 currency

The critical carry-forward from [02](02-lwr-architecture-and-build-model.md): **Experience Delivery is being discontinued in Winter '27** and is **already closed to new enablement**; orgs already on it have until **October 2026**. It was Beta from Summer '24 and never flipped. A performance or SEO plan that assumes SSR is available — never mind on by default — is wrong twice over. **Static build + CDN is not the baseline under SSR any more; it is the whole thing.**

## Gotchas

- **Don't plan around SSR at all.** Experience Delivery cannot be newly enabled and ends in Winter '27 — assume public pages are client-hydrated and budget the SEO work accordingly.
- **SSR-safe component discipline still pays.** Guarding module-scope `window`/`document` access with `import.meta.env.SSR` keeps components portable and prerender-friendly even with Experience Delivery gone → [06](06-custom-lwc-in-lwr-sites.md).
- **Authenticated pages don't get the edge cache.** Benchmark the public path, not a logged-in page, before judging the site slow.
- **Stale content after publish** is usually CDN propagation lag, not a data bug.
- **Client-only rendering kills SEO.** A page that builds its content purely in JS after load hands the crawler an empty shell.
- **Meta tags are per-page and manual** — an unset title/description ships a generic one; SEO reviews catch this late.

## Recall

Q: What single architectural fact explains LWR's caching, SEO and SSR-safe rules?
A: LWR sites are built and served as static assets from a CDN, not rendered per request like Aura.

Q: What is the status of SSR / Experience Delivery on LWR, and why does it matter?
A: **Being discontinued in Winter '27 and already closed to new enablement** (existing orgs until October 2026). It was Beta from Summer '24 and never flipped — so SSR is not something you can plan to switch on, and static build + CDN is the entire performance story.

Q: What breaks server-side rendering (and the build) in a custom component?
A: Touching `window`/`document` at module scope — guard browser-only code with `import.meta.env.SSR` and defer it to a lifecycle hook.

Q: What does LWR give you for SEO regardless of SSR?
A: An auto-generated sitemap, clean URLs, and per-page meta/Open Graph tags — which, with Experience Delivery withdrawn, is the complete first-party SEO toolkit.

Q: When does a content change actually reach visitors?
A: At publish, when the static build regenerates and propagates to the CDN — not on save.

## Related

- [02 · LWR architecture & build model](02-lwr-architecture-and-build-model.md) — build-and-serve, and Experience Delivery's withdrawal
- [06 · Custom LWC in LWR sites](06-custom-lwc-in-lwr-sites.md) — the SSR-safe component rules performance depends on
- [15 · Headless sites & Connect APIs](15-headless-sites-and-connect-apis.md) — where you take over SSR/SEO yourself
