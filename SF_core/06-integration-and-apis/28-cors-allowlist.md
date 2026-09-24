---
vault: SF_core
area: 06-integration-and-apis
format: light
level: basic
status: open
gaps: 3
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [integration, security]
---
# CORS Allowlist

**One line:** The org's list of browser origins whose JavaScript may call Salesforce APIs and read the response. You manage it in Setup → **CORS**.

**Reach for it when:** JavaScript on a page Salesforce does not serve — your website, a single-page app, a browser extension — calls a Salesforce API, and the console says the request was blocked by CORS policy.

> **From my notes.** *"CORS - what is it?"* — Cross-Origin Resource Sharing: the browser rule that lets script on one origin read a response from another origin, when that server agrees. In Salesforce it lists who may call **into** the org — the opposite direction to the Trusted URLs entry the same Trailhead step made.

## Key points

- **The default is the same-origin policy:** page script may only read responses from its own origin — scheme + host + port. So `https://shop.example.com` and `https://acme.my.salesforce.com` are two origins.
- **CORS is the server saying yes:** the browser sends `Origin`, the server answers with `Access-Control-Allow-Origin`. A request that is not "simple" — a `PATCH`, an `Authorization` header — first sends a **preflight** `OPTIONS`.
- **Add an origin:** Setup → **CORS** → **New** → **Origin URL Pattern**. A listed origin is echoed back in `Access-Control-Allow-Origin`; an unlisted one gets **403** per Help but **404** per the Metadata API guide 🚩.
- **Pattern rules:** `https://` plus a domain and optional port — the exceptions are `http://localhost` and, from API 53.0, `chrome-extension://` and `moz-extension://` IDs. `*` goes only in front of a second-level domain (`https://*.example.com`), and an IP is a separate entry from its domain.
- **What honours it:** REST API, Apex REST, Bulk API and Bulk API 2.0, Connect REST API, User Interface API, CRM Analytics REST API and Lightning Out. Help says it applies on your My Domain URL and `api.salesforce.com`.
- **OAuth endpoints need a second switch:** *"CORS doesn't support requests for unauthenticated resources, including OAuth endpoints."* Tick **Enable CORS for OAuth endpoints** under **Cross-Origin Resource Sharing (CORS) Policy Settings** → Edit, on the same page.
- **It deploys:** metadata `CorsWhitelistOrigin` (API 32.0+, one field `urlPattern`); the API object is `CorsWhitelistEntry`.

## The two directions

| | CORS allowlist | Trusted URLs |
|---|---|---|
| Question | may this outside page call Salesforce? | may this Salesforce page load or call that host? |
| The entry is | the calling page's origin | the destination host |
| Header the browser reads | `Access-Control-Allow-Origin` | `Content-Security-Policy` |

## Gotchas

- **CORS is not authentication.** An allowlisted origin still needs a valid access token; the allowlist only lets the browser hand the response to the script.
- **No browser, no CORS.** curl, Apex, middleware and the Postman desktop app never see it, so "it works in Postman" proves nothing — only the Postman *web* app needs an entry.
- **Paste an origin, not a page** — browsers send `Origin` without a path, so the path on an All Sites URL is at best ignored 🚩. A sandbox refresh renames the host, so sandbox entries break → [07-security · 20](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md).
- **Lightning apps are checked on the server too** — the Winter '22 release update *Enforce CORS Allowlist for Lightning Apps* moved the check there. Blocks are logged as the **CORS Violation Record** event type, in the free tier → [07-security · 23](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md).

## Gaps to close

- [ ] Which OAuth endpoints does **Enable CORS for OAuth endpoints** open, and must the calling origin also be in the allowlist?
- [ ] Does the allowlist cover API calls made on an Experience Cloud site's own domain, or only My Domain and `api.salesforce.com`?
- [ ] Which APIs did Winter '25's *Enforce the CORS Allowlist on More Salesforce APIs* add, and is the list above now complete?

## Confirm in org

- 🚩 Does Enhanced Web Chat — on an external website or an Experience Cloud site — need a CORS entry, or does the deployment's Domain field cover it, given Help's chat CORS page was written for legacy Embedded Chat? — delete the Trailhead's entry, start a chat, read the console.

## Hands-on

- [ ] **SF-CORS-01** · 20 min · Serve a page from `http://localhost:8080` that `fetch`es `https://<MyDomain>.my.salesforce.com/services/data/v67.0/limits` with a bearer token, before and after allowlisting the origin. **Proves:** without the entry the browser blocks it — copy the console error verbatim — while curl gets the same data. **Needs:** a local static server, an access token.
- [ ] **SF-CORS-02** · 10 min · With the origin allowlisted, send the same `fetch` with no token. **Proves:** the allowlist grants no access — the call still fails; record whether the script sees a 401 or a CORS error.
- [ ] **SF-CORS-03** · 15 min · Call from an origin that is not listed, read the status in the Network tab, then query the CORS Violation Record event log. **Settles:** the 403-or-404 🚩, and whether the block is logged. **Needs:** event log file access.
- [ ] **SF-CORS-04** · 20 min · Delete the site-URL CORS entry from the Trailhead org, then start a chat on the site. **Settles:** whether Enhanced Chat on a site needs a CORS entry. **Needs:** the Knowledge & Enhanced Chat project org.

## Related

- [03 · API endpoints, hostnames & Edge Network](03-api-endpoints-hostnames-and-edge-network.md) — the host a browser call goes to, and the one-line CORS-vs-CSP rule this note expands
- [07-security · 27 Trusted URLs & CSP](../07-security-and-sharing/27-trusted-urls-and-csp.md) — the opposite direction: what a Salesforce page may load or call
- [15 · OAuth flows & authorization](15-oauth-flows-and-authorization.md) — where the token comes from; CORS never replaces it
- [18 · Apex REST & custom endpoints](18-apex-rest-and-custom-endpoints.md) — a custom endpoint a browser can call once its origin is listed
- [07-security · 23 Event monitoring & transaction security](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md) — the CORS Violation Record event type, in the free tier
- [SF_Service · Enhanced Chat setup chain](../../SF_Service/enhanced-chat-setup-chain.md) — carries the same CORS question as a gap; SF-CORS-04 answers it for both notes
- [SF_Service · Embedded Service deployments](../../SF_Service/embedded-service-deployments.md) — the deployment whose Domain field may or may not make the Trailhead's CORS entry redundant
- [SF_Experience_Cloud · 19 Embedded messaging & agents in sites](../../SF_Experience_Cloud/19-embedded-messaging-and-agents-in-sites.md) — the site-side chat step the Trailhead's CORS entry was added for
- [SF_Experience_Cloud · 24 Site CSP, security level & trusted scripts](../../SF_Experience_Cloud/24-site-csp-security-level-and-trusted-scripts.md) — the site half of the Trailhead's security step, and where its script hosts go

## Sources

- [Configure Salesforce CORS Allowlist](https://help.salesforce.com/s/articleView?language=en_US&id=sf.extend_code_cors.htm&type=5) — Salesforce Help · via search 2026-09-24 · supported technologies; pattern rules; 403; My Domain URL and `api.salesforce.com`; *"CORS doesn't support requests for unauthenticated resources, including OAuth endpoints"*
- [Enable CORS for OAuth Endpoints](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_endpoints_cors.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · the **Cross-Origin Resource Sharing (CORS) Policy Settings** checkbox
- [Metadata API Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_meta.pdf) — Salesforce Developers · read 2026-09-24 · `CorsWhitelistOrigin`: API 32.0, `urlPattern`, extensions from API 53, IP entries, *"returns HTTP status code 404"* — a Winter '27 build; nothing used here is new in 68.0
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `CorsWhitelistEntry` — a Winter '27 build
- [REST API Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_rest.pdf) — Salesforce Developers · read 2026-09-24 · CORS for supported APIs, Apex REST and Lightning Out
- [User Interface API Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_ui.pdf) — Salesforce Developers · read 2026-09-24 · the Postman web app *"requires a CORS configuration in Salesforce"*
- [Enforce the CORS Allowlist on More Salesforce APIs](https://help.salesforce.com/s/articleView?id=release-notes.rn_api_cors_allowlist.htm&language=en_US&release=252&type=5) — Winter '25 release notes · via search 2026-09-24 · title only; the body did not load — behind gap 3
- [Enforce CORS Allowlist for Lightning Apps (Release Update)](https://help.salesforce.com/s/articleView?id=release-notes.rn_lc_cors_allowlist_ru.htm&language=en_US&release=234&type=5) — Winter '22 release notes · via search 2026-09-24 · enforced on the server, not only in the browser
- [CORS Violation Record Event Type](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_eventlogfile_cors_violation.htm) — Salesforce Developers · via search 2026-09-24
- [Working with CORS and CSP to Call APIs from LWC](https://developer.salesforce.com/blogs/2022/03/working-with-cors-and-csp-to-call-apis-from-lwc) — Salesforce Developers Blog, March 2022 · via search 2026-09-24 · preflight; `Origin` vs `Access-Control-Allow-Origin`; *"Access has been blocked by CORS policy"*
- [Add Your Website to the CORS Allowlist](https://help.salesforce.com/s/articleView?id=service.embedded_chat_cors_allowlist.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · the legacy Embedded Chat page behind the first org check
- [Configure a Web Deployment](https://trailhead.salesforce.com/content/learn/projects/build-a-community-with-knowledge-and-chat/enable-and-configure-lightning-knowledge) — Trailhead project unit · read 2026-09-24 · **Set Security Protocols**: All Sites → copy the site URL → CORS → New → paste → Save

## History

- 2026-09-24 · created from your Trailhead feed (Knowledge & Enhanced Chat site project)
