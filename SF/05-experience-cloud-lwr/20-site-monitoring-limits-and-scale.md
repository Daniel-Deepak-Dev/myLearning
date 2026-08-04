# Site Monitoring, Limits & Scale

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 19

**Scope:** The capacity constraints that surprise teams at launch — page-view allowances, site counts, guest throttling, API limits — and how to watch a live site. Closes the Experience Cloud area.

## Core idea

Experience Cloud meters on **page views**, not users, and that's the number that surprises people. A site has an **edition-scaled annual guest page-view allowance** (Enterprise is commonly cited around **~6 million/year**, tiered by edition), and overage is **billed, not blocked** — a viral public page can burn the budget fast. There's also a ceiling most people never hit until they do: an org is capped at **100 sites**, and that count includes **inactive, preview and Visualforce** sites, so old experiments count against it. Layered on top are the org's **aggregate API limits** (shared across all integrations, not per user) and **guest-user throttling** to blunt scraping. Scale planning is therefore: how many page views will public traffic generate, how many API calls will authenticated/headless clients make, and where the guest throttles bite.

## How it works

- **Page views are the currency.** Allowances are annual and per edition; overage is charged, not blocked — so cost, not downtime, is the usual failure mode. Confirm current per-edition numbers against the *Experience Cloud Site Usage Limits* doc.
- **100 sites per org**, counting inactive/preview/Visualforce — audit and retire dead sites before assuming headroom.
- **API limits are org-aggregate.** Every headless/API call counts against the same 24-hour org allocation — a chatty front end competes with integrations, [15](15-headless-sites-and-connect-apis.md).
- **Guest throttling** caps request rates and can disable guest API access entirely (site setting + guest profile `API Enabled`) — the anti-scraping lever, [11](11-public-site-exposure-audit.md).
- **Monitoring surfaces:** the site's usage dashboards, Event Monitoring for page-view/login events, and the CDN/cache behaviour from [16](16-site-performance-caching-and-seo.md) for what's actually reaching the app server.

## Gotchas

- **Page-view overage is a bill, not an outage.** A successful public launch can generate a surprise invoice — model expected traffic before go-live.
- **The 100-site cap counts the dead.** Inactive, preview and Visualforce sites all count — a "we have room" assumption is often wrong.
- **API limits are shared org-wide.** A headless site can starve unrelated integrations; budget them together.
- **Caching changes cost, not counting.** Edge-cached pages spare the app server, but page-view *counting* still applies — caching doesn't make views free.
- **Guest API can be turned off** and often should be — it's both a scrape vector and a limit drain, [11](11-public-site-exposure-audit.md).
- **Per-edition numbers change** — never quote a page-view figure without checking the current usage-limits doc for that edition.

## Recall

Q: What does an Experience Cloud site primarily meter on?
A: Page views — an edition-scaled annual guest allowance (Enterprise commonly ~6M/year), not the number of users.

Q: What happens when a site exceeds its page-view allowance?
A: Overage is billed — a cost event, not an outage — which makes an unmodeled viral launch a budget risk.

Q: What's the org-wide site-count cap, and what counts against it?
A: 100 sites per org, including inactive, preview and Visualforce sites — so dead experiments consume headroom.

Q: Are API limits per user or per org?
A: Per org — an aggregate 24-hour allocation shared across every integration and headless client.

Q: What is guest throttling for, and what's the blunt lever?
A: To blunt scraping/abuse — you can rate-limit and fully disable guest API access via the site setting plus the guest profile's `API Enabled` permission.

## Related

- [16 · Site performance, caching & SEO](16-site-performance-caching-and-seo.md) — caching is what keeps page views off the app server
- [15 · Headless sites & Connect APIs](15-headless-sites-and-connect-apis.md) — the biggest consumer of the org's shared API budget
- [11 · Public site exposure audit](11-public-site-exposure-audit.md) — guest throttling and API-off as hardening controls
