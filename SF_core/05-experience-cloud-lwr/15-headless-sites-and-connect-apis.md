# Headless Sites & Connect APIs

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 19

**Scope:** Building a front end in your own stack (React, Next.js, a native app) while Salesforce serves data and content over APIs — and the judgment call of when that's worth abandoning Experience Builder. Auth is **not** restated here: Headless Identity lives in [10](10-authentication-self-registration-and-sso.md).

## Core idea

"Headless" means the presentation layer is decoupled from Salesforce: you own the UI, hosted anywhere, and call Salesforce as a set of services — **UI API / Connect REST API** for records and CMS, GraphQL/REST for data, and the Headless Identity APIs from [10](10-authentication-self-registration-and-sso.md) for auth. The counter-intuitive part: **you still need an Experience Cloud site**. Headless Identity endpoints are exposed *through* a site, and licensing and guest context still flow from it, so headless isn't "no site" — it's "a site with no Experience Builder pages." You reach for it when the brand demands a bespoke UX, when the front end is a mobile/native app, or when a design system can't live inside Experience Builder's component model. You stay in Experience Builder when time-to-launch and admin maintainability beat pixel control — which is most of the time.

## How it works

- **Content & data:** Connect REST API delivers CMS (Enhanced CMS Workspaces resources); **UI API** delivers records with layout metadata; GraphQL/REST for bulk querying → [06-integration · 08 UI API](../06-integration-and-apis/08-ui-api-and-metadata-aware-clients.md).
- **Auth is a cross-reference, not a topic here.** The front end is an OAuth client (PKCE for public, or a private client) and runs Headless Login/Registration/Passwordless from [10](10-authentication-self-registration-and-sso.md); tokens gate every data call.
- **Hybrid is allowed.** A site can be mostly Experience Builder with a headless section, or fully headless — the license and guest model are identical.
- **The judgment call is the content of this note:** headless trades platform-managed rendering, caching and SEO for total UX control. Only take that trade when UX control genuinely outweighs the loss.

## 2026 currency

Under the **Headless 360** theme every capability is reachable as an API, which is what makes a fully decoupled customer site practical → [AI_Data · Headless 360](../../AI_Data/05-release-radar/developer-tooling-and-apis.md). The trade sharpened in Summer '26: LWR's own rendering advantage shrank when **Experience Delivery was slated for discontinuation**, so "we lose SSR by going headless" is no longer the argument against it — an LWR site has no server-side rendering to lose → [16](16-site-performance-caching-and-seo.md). What you still take on is caching and sitemaps.

## Gotchas

- **Headless still requires a site.** Provision an Experience Cloud site even if it renders zero Experience Builder pages — Headless Identity and the guest/licensing context are exposed through it.
- **You lose the platform's build, CDN and sitemap** — not its SSR, which is going away anyway ([16](16-site-performance-caching-and-seo.md)). Caching, sitemaps and meta tags become yours. The upside is that you can add real SSR in your own stack, which the platform no longer offers.
- **Guest data exposure moves to your API calls.** Any endpoint a public front end calls runs as the guest user — the exposure audit applies unchanged, [11](11-public-site-exposure-audit.md).
- **API limits are the org's aggregate**, consumed by every headless request; a chatty front end can exhaust them, [20](20-site-monitoring-limits-and-scale.md).
- **CORS and Trusted URLs** must include the front end's origin, or browser calls silently fail.
- **License still applies.** Headless users consume the same external identity/customer licenses — headless is a UI choice, not a licensing dodge, [08](08-licences-and-external-user-types.md).

## Recall

Q: Does a headless implementation still require an Experience Cloud site?
A: Yes — Headless Identity APIs and the guest/licensing context are exposed through a site even when no Experience Builder pages are rendered.

Q: Where is Headless Identity covered, and should this note restate it?
A: In [10 · Authentication](10-authentication-self-registration-and-sso.md) — this note cross-links it rather than restating the login/registration/passwordless flows.

Q: What do you give up by going headless that Experience Builder gave you for free?
A: The static build, the CDN, the auto-generated sitemap and per-page meta — you own caching and SEO yourself. Not SSR: with Experience Delivery being discontinued, the platform has none to give up, so a headless stack is now the *only* way to get server-side rendering.

Q: What is the main judgment call for choosing headless?
A: Bespoke UX / native app / external design system versus Experience Builder's faster launch and admin maintainability — pick headless only when UX control genuinely outweighs those.

Q: As which user do a public headless front end's data calls execute?
A: The guest user — so the guest exposure audit and sharing rules govern every exposed endpoint.

## Related

- [10 · Authentication, self-registration & SSO](10-authentication-self-registration-and-sso.md) — where Headless Identity is actually taught
- [16 · Site performance, caching & SEO](16-site-performance-caching-and-seo.md) — what you inherit responsibility for when you leave Experience Builder, and why there is no SSR to lose
- [06-integration · 08 UI API](../06-integration-and-apis/08-ui-api-and-metadata-aware-clients.md) — the metadata-aware data API the front end calls
