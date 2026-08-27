# API endpoints, hostnames & Edge Network

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** The half of the URL before `/services/` — which hostname a client may call, how it resolves, and the browser-side allowlists that decide whether a request is even attempted. The version path segment is [02](02-api-versions-and-the-retirement-treadmill.md); My Domain as an org-configuration topic is [07-security · 20](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md).

> **What changed.** *"Any Salesforce hostname works, and old ones redirect"* is wrong twice over. **Legacy My Domain hostnames stopped redirecting in Spring '26 — they 404.** And **instanced hostnames (`na45.salesforce.com`, `cs12.salesforce.com`) stop being supported for API traffic with Winter '27**, which reaches sandboxes from **August 2026** and production from **September 2026**. That is weeks away, not a roadmap item.

## Core idea

An integration's endpoint is two independent decisions welded into one string: **which host** identifies the org, and **which API version** fixes the contract. Historically the host was an instance name — `na45`, `eu17`, `cs12` — which leaked physical infrastructure into every client's configuration and broke whenever Salesforce moved the org. My Domain replaced that with a stable, org-owned hostname, and the platform has spent 2024–2026 closing the old path: first by redirecting, then by ending redirection, and now by withdrawing support for instanced URLs entirely. Meanwhile **Edge Network** changes how the correct hostname resolves — terminating connections closer to the caller — without changing the hostname itself.

The reason this deserves its own note is that the failure is **configuration you do not own**: the hardcoded hostname is usually in middleware, an ISV connector or a script, not in Salesforce.

## How it works

| Host form | Example | Status |
|---|---|---|
| **My Domain** | `mycompany.my.salesforce.com` | the correct form for API traffic |
| **Instanced** | `na45.salesforce.com` | **unsupported from Winter '27** |
| **Legacy My Domain** | pre-enhanced-domain hostnames | **404s since Spring '26** — no redirect |
| **Login endpoints** | `login.salesforce.com` / `test.salesforce.com` | valid for the OAuth request itself |

- **Never hardcode the host after login.** The OAuth token response returns **`instance_url`**; use it verbatim for subsequent calls. A client that authenticates correctly and then rebuilds the URL from a stored constant is the exact shape this retirement breaks.
- **`test.salesforce.com` is for sandbox *authentication*.** The `instance_url` that comes back is the sandbox's own My Domain host.
- **Salesforce Edge Network** terminates TLS and routes at points of presence near the caller, cutting round-trip latency. It is a routing layer, not a new address — you still call the My Domain host.
- **Browser-origin calls need two allowlists, and they are not interchangeable.** **CORS** allowlists the *origin calling Salesforce*; **CSP Trusted Sites** allowlists *destinations Salesforce pages may call*. → [03-lwc · 09](../03-lwc-and-slds/09-lightning-web-security.md)
- **CORS does not replace authentication.** An allowlisted origin still needs a valid token; the allowlist only stops the browser from blocking the response.

## 2026 currency

The instanced-URL withdrawal is the live one and its timeline is tight. An opt-in ***Block API traffic that uses an incorrect instanced URL*** switch became available **19 June 2026** so orgs can find offenders early; enforcement follows with **Winter '27**, which deploys to sandboxes from **August 2026** and production from **September 2026**. One documented trap in the opt-in phase: enabling the switch could make **SOAP login URLs called through Visualforce pages return 400 Bad Request** — Salesforce shipped the fix **16–18 June 2026**, so testing is only meaningful after that. Find the callers with the **Hostname Redirects** event type, which is in Event Monitoring's **free** tier → [07-security · 23](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md). Wider domain context: [07-security · 20](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md).

> **From my notes.** *`Salesforce Edge Network`* (2023) treats Edge purely as a latency optimisation to switch on. Still true, and now incomplete: the same years turned hostname choice from a performance question into a **supportability** one. Enabling Edge changes how fast the right hostname resolves; it does nothing for a client still calling `na45`.

## Gotchas

- **`.my.salesforce.com` is not one thing.** Login, API and Experience Cloud hosts differ; copying a browser address bar into an integration config is how the wrong one gets pinned.
- **Sandbox refresh changes the host.** Any config naming a sandbox hostname needs a post-refresh step, and this is where instanced URLs get reintroduced by hand.
- **A 404 reads like "wrong path", not "wrong host"**, so the end of redirections sends investigations to the URI when the hostname is the fault.
- **`instance_url` can change** — org migrations and Hyperforce moves do change it. Storing it once at first login and never refreshing is a slow-motion outage. → [08-data · Hyperforce](../08-data-modeling-and-large-data-volumes/INDEX.md)
- **CSP Trusted Sites failures surface in the browser console, not in Apex.** Nothing server-side reports them, so they get blamed on LWS. → [03-lwc · 09](../03-lwc-and-slds/09-lightning-web-security.md)
- **Hardcoded hostnames are a secure-coding finding**, already on the checklist as item 16. → [07-security · 26](../07-security-and-sharing/26-secure-coding-checklist.md)

## Recall

Q: What happens to a legacy My Domain hostname today?
A: It 404s. Redirections ended in Spring '26 — it does not forward.

Q: When do instanced URLs stop being supported for API traffic, and what is the real date?
A: With Winter '27 — sandboxes from August 2026, production from September 2026.

Q: Where should a client get the host it calls after authenticating?
A: From `instance_url` in the OAuth token response, used verbatim — never from a stored constant.

Q: What is the difference between CORS and CSP Trusted Sites?
A: CORS allowlists origins that call Salesforce; CSP Trusted Sites allowlists destinations Salesforce pages may call. Opposite directions.

Q: Which free log finds integrations still using old hostnames?
A: The Hostname Redirects event type, available without Shield.

## Related

- [02 · API versions & the retirement treadmill](02-api-versions-and-the-retirement-treadmill.md) — the other half of the endpoint, on its own clock
- [04 · REST API fundamentals](04-rest-api-fundamentals.md) — what goes after the host
- [07-security · 20 My Domain & enhanced domains](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md) — the org-configuration side
- [07-security · 26 Secure coding checklist](../07-security-and-sharing/26-secure-coding-checklist.md) — hardcoded hostnames as a review finding
