# Mobile Publisher & PWA Delivery

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 19

**Scope:** Turning an Experience Cloud site into a branded mobile experience — a native app via Mobile Publisher, or a progressive web app — and the review/publishing pipeline each implies. Licences underneath the app are [08](08-licences-and-external-user-types.md).

## Core idea

Two paths put an Experience Cloud site on a phone. **Mobile Publisher** wraps the site as a genuine native iOS/Android app — your icon, your name, your listing in the App Store and Google Play — with push notifications, biometric login and native device features the browser can't reach. It's a Salesforce add-on, **licensed per app**, and the app is submitted through *your* Apple and Google developer accounts. **PWA** delivery instead serves the site as an installable web app — no store listing, no native shell, updates ship the instant you publish. The choice is a trade: Mobile Publisher buys store presence, push and native APIs at the cost of a review pipeline and per-release resubmission; PWA buys instant updates and zero store friction at the cost of native reach and discoverability.

## How it works

- **Mobile Publisher pipeline:** a **Listing Wizard** collects branding assets, builds separate iOS and Android artifacts, supports beta/test distribution, then submits to each store. Apple and Google require different listing metadata — you populate both.
- **Review is Apple's/Google's, not Salesforce's.** A rejected build is a store decision; build in lead time before launch.
- **Per-release resubmission:** a native binary change goes back through review; content and site changes published to the underlying site appear without resubmission (the app loads the live site).
- **PWA** needs a manifest and HTTPS; the LWR site already serves over the CDN, so "installable web app" is largely a configuration + icon exercise → [16](16-site-performance-caching-and-seo.md).
- **Auth on mobile** reuses the same OAuth/Headless Identity model from [10](10-authentication-self-registration-and-sso.md); biometric unlock is a Mobile Publisher feature on top.

## Gotchas

- **Per-app licensing.** Mobile Publisher is licensed per branded app — a partner portal and a customer portal are two apps, two licenses.
- **You own the developer accounts.** Salesforce doesn't publish for you; App Store/Play memberships, certificates and store fees are yours.
- **Store review can reject** for reasons unrelated to Salesforce (thin content, login walls, guideline nuances) — a portal that's "just a website" risks rejection.
- **Binary vs content changes differ.** Branding/native changes need resubmission; site content published to the live site does not — teams conflate these and over-resubmit.
- **PWA has no App Store discoverability** and weaker native integration — fine for internal/known-audience portals, weak for consumer acquisition.
- **iOS and Android diverge** — features and review outcomes can differ per platform; test both, don't assume parity.

## Recall

Q: What does Mobile Publisher produce, and how is it licensed?
A: A branded native iOS/Android app with its own store listing, push and biometric login — licensed per app, submitted through your own Apple/Google developer accounts.

Q: Which changes to a Mobile Publisher app require store resubmission, and which don't?
A: Native/branding (binary) changes require resubmission; content published to the underlying live site appears without it, since the app loads the live site.

Q: What's the core trade between Mobile Publisher and a PWA?
A: Native app buys store presence, push and device APIs at the cost of review and resubmission; PWA buys instant updates and no store friction at the cost of native reach and discoverability.

Q: Who reviews and approves a Mobile Publisher app?
A: Apple and Google — it's a store review, not a Salesforce approval, so build in lead time and rejection risk.

Q: Why might a simple portal be rejected from the App Store?
A: Store guidelines can reject thin "just a website" apps or login-walled content lacking native value.

## Related

- [10 · Authentication, self-registration & SSO](10-authentication-self-registration-and-sso.md) — the auth model both delivery paths reuse
- [16 · Site performance, caching & SEO](16-site-performance-caching-and-seo.md) — PWA installability builds on the LWR CDN delivery
- [08 · Licences & external user types](08-licences-and-external-user-types.md) — how mobile users are licensed underneath the app license
