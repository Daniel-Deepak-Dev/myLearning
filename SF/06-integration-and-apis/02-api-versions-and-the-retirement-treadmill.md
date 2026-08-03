# API versions & the retirement treadmill

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** What an API version number commits you to, and the retirement cycle running underneath every integration in the org. The endpoint *host* is [03](03-api-endpoints-hostnames-and-edge-network.md); per-version feature detail belongs to each API's own note.

> **What changed.** *"Old API versions are deprecated"* understates it. They are **actively retired**, and a retired version does not degrade — it returns **HTTP 410 GONE** and the integration stops. Versions **21.0–30.0** were deprecated in Summer '22 and **retired in Summer '25**. "It works on v39" is a position on a countdown, not a steady state.

## Core idea

Salesforce versions its APIs so that an integration written against v40.0 keeps behaving like v40.0 after the org upgrades three times a year — the contract is pinned in the URL path, not in the org. That guarantee is what makes the platform safely upgradable, and it is also what lets thousands of integrations quietly rot: nothing forces a client forward, so nothing moves it, until the version underneath it is withdrawn. The treadmill is the consequence. Salesforce commits to supporting a version for a minimum window, announces deprecation, then announces retirement with a date — and on that date the endpoint returns 410 rather than falling back to a newer version.

The architect's job is therefore inventory, not memorisation: knowing **which versions your org is actually being called on** matters more than knowing any published list.

## How it works

| State | What it means | What a caller sees |
|---|---|---|
| **Current** | the version shipping with the release — **67.0** at Summer '26 | normal |
| **Supported** | older, still fully served, behaviour frozen at its own semantics | normal |
| **Deprecated** | announced as going away; still served | normal, plus a countdown |
| **Retired** | withdrawn | **HTTP 410 GONE** |

- **The version lives in the path** — `/services/data/v67.0/…` — and in SOAP, in the endpoint URL and WSDL. Nothing about the org's release changes it.
- **Apex classes and triggers carry their own version too**, set per file, which is how a 2019 class keeps its 2019 behaviour after the org reaches 67.0. → [09](09-metadata-tooling-and-connect-apis.md)
- **Retirement is announced, dated, and published** on Salesforce's *Product & Feature Retirements* list. That list — not recall — is the source.
- **Find your real exposure in the org, not in a spreadsheet.** The **API Total Usage** event type reports the API version of inbound calls, and it is one of the log types available **without Shield** → [07-security · 23](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md).

## 2026 currency

**One wave is complete and no next wave is announced.** Versions **21.0–30.0** are retired as of Summer '25; the floor is **31.0**. Projections that 31.0–39.0 follow in a particular release circulate widely and **none of them is an announcement** — do not repeat a date the retirements list does not carry. The dated item that *does* exist is narrower and easy to confuse with it: **SOAP `login()` is being retired for API versions 31.0–64.0 in Summer '27** — that is **one call** being withdrawn across a range of versions, **not those versions being retired**. Both facts and their sourcing live in [../CURRENCY.md](../CURRENCY.md). → [05](05-soap-api-and-where-it-persists.md)

## Gotchas

- **The failure is total, not gradual.** 410 GONE means the nightly job that ran for nine years stops on a Tuesday. There is no degraded mode and no automatic upgrade to a supported version.
- **Packaged and vendor integrations are the real exposure**, because you cannot edit them. Inventory ISV connectors before your own code.
- **Old Data Loader builds pin an old version.** A desktop tool nobody thinks of as an integration is exactly what a retirement wave breaks. → [01-admin · 13](../01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md)
- **Bumping the version is not free.** Behaviour genuinely differs between versions — that is the entire point of pinning — so a bump is a change requiring regression testing, not a find-and-replace.
- **`/services/data/` with no version returns the version list**, which is the cheapest way to see what an org will currently serve.
- **Do not conflate a *version* retirement with a *feature* retirement.** SOAP `login()`, the username-password OAuth flow and instanced URLs are each on their own clock. → [03](03-api-endpoints-hostnames-and-edge-network.md), [15](INDEX.md)

## Recall

Q: What does a retired API version return?
A: HTTP 410 GONE. It does not fall back to a supported version.

Q: Which versions are retired, and when did it happen?
A: 21.0–30.0 — deprecated Summer '22, retired Summer '25. The supported floor is 31.0.

Q: When is the next retirement wave?
A: No next wave is announced. Circulating projections about 31.0–39.0 are speculation, not a published date.

Q: How is the SOAP `login()` retirement different from a version retirement?
A: It withdraws one call across API versions 31.0–64.0 in Summer '27. Those versions themselves are not being retired.

Q: How do you find which API versions an org is actually called on?
A: The API Total Usage event type in Event Monitoring — available without Shield.

## Related

- [03 · API endpoints, hostnames & Edge Network](03-api-endpoints-hostnames-and-edge-network.md) — the other half of the URL, and its own end-of-support clock
- [05 · SOAP API & where it persists](05-soap-api-and-where-it-persists.md) — where the `login()` retirement bites
- [../CURRENCY.md](../CURRENCY.md) — the dated retirement rows and their sourcing
- [07-security · 23 Event Monitoring](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md) — where API Total Usage lives
