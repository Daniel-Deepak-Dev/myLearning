# Site Monitoring, Limits & Scale

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 19

**Scope:** The capacity constraints that surprise teams at launch — page-view allowances, site counts, guest throttling, API limits — and how to watch a live site. Closes the Experience Cloud area.

> **What changed — or rather, what was never true.** *"Page-view overage is just a bill"* is the comfortable version and it is wrong. Sustained overage **disables sites**: exceed **110% of the allowance for four consecutive calendar months** and Salesforce can disable your sites until the next month or until you buy more; hit **300% in a single month** and they can be disabled immediately. Overage is billable *and* enforceable, so a viral launch is an availability risk, not only a budget one.

## Core idea

Experience Cloud meters on **page views**, not users, and that's the number that surprises people. The allowance is **per edition and monthly**: **Enterprise 500,000 page views/month** — the "6 million a year" figure people quote is the same number annualised — and **Unlimited and Performance 1,000,000/month**. Exceeding it is not a pure billing event: see the correction above. There's also a ceiling most people never hit until they do: an org is capped at **100 sites**, and that count includes **inactive, preview and Visualforce** sites, so old experiments count against it. Layered on top are the org's **aggregate API limits** (shared across all integrations, not per user) and **guest-user throttling** to blunt scraping. Scale planning is therefore: how many page views will public traffic generate, how many API calls will authenticated/headless clients make, and where the guest throttles bite.

## How it works

- **Page views are the currency, and the allowance is monthly.** **EE 500,000/month; UE and PE 1,000,000/month.** Quote the edition with the number or the figure means nothing — and check the current *Salesforce Sites Usage and Billing* doc, because these move.
- **Bandwidth is a second, separate meter:** **40 GB per rolling 24 hours** per production site (EE/PE/UE), **1 GB** in sandboxes, **500 MB** in Developer Edition.
- **100 sites per org**, counting inactive/preview/Visualforce — audit and retire dead sites before assuming headroom.
- **API limits are org-aggregate.** Every headless/API call counts against the same 24-hour org allocation — a chatty front end competes with integrations, [15](15-headless-sites-and-connect-apis.md).
- **Guest throttling** caps request rates and can disable guest API access entirely (site setting + guest profile `API Enabled`) — the anti-scraping lever, [11](11-public-site-exposure-audit.md).
- **Monitoring surfaces:** the site's usage dashboards, Event Monitoring for page-view/login events, and the CDN/cache behaviour from [16](16-site-performance-caching-and-seo.md) for what's actually reaching the app server.

## Gotchas

- **Page-view overage can take the site down.** 110% for four consecutive months, or 300% in one month, and Salesforce can disable your sites. Model expected traffic before go-live and watch the meter after — this is the gotcha most launch plans get backwards.
- **Never quote a page-view number without its edition.** EE and UE differ by 2×, and half-quoting it is how a capacity plan ends up sized for the wrong org.
- **The 100-site cap counts the dead.** Inactive, preview and Visualforce sites all count — a "we have room" assumption is often wrong.
- **API limits are shared org-wide.** A headless site can starve unrelated integrations; budget them together.
- **Caching changes cost, not counting.** Edge-cached pages spare the app server, but page-view *counting* still applies — caching doesn't make views free.
- **Guest API can be turned off** and often should be — it's both a scrape vector and a limit drain, [11](11-public-site-exposure-audit.md).
- **Per-edition numbers change** — never quote a page-view figure without checking the current usage-limits doc for that edition.

## Recall

Q: What does an Experience Cloud site primarily meter on, and at what allowance?
A: Page views, monthly and per edition — **Enterprise 500,000/month**, **Unlimited and Performance 1,000,000/month** — not the number of users.

Q: What happens when a site exceeds its page-view allowance?
A: More than a bill. At **110% for four consecutive calendar months**, or **300% in a single month**, Salesforce can **disable the sites** until the next month or until more page views are purchased — so an unmodeled viral launch is an availability risk as well as a cost one.

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
