---
vault: SF_core
area: 07-security-and-sharing
format: light
level: working
status: open
gaps: 2
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [security]
---
# Trusted URLs & CSP

**One line:** CSP is the browser rule set a page declares in its `Content-Security-Policy` header. **Trusted URLs** is the Setup list that adds your external hosts to the header Salesforce sends.

**Reach for it when:** a Lightning page, an Experience Builder site or a Visualforce page must call, frame, or pull images, fonts, styles or media from a host that is not Salesforce.

> **From my notes.** *"trusted URLs in salesforce setup and its options in detail with there respective use case scenarios? CSP vs Trusted URLs why we have two options."* — **Corrected:** CSP and Trusted URLs are not two options; CSP is the mechanism and Trusted URLs is how you edit Salesforce's CSP header. The real pair is org-wide Trusted URLs for everything except scripts, and each site's **Trusted Sites for Scripts** → [SF_Experience_Cloud · 24](../../SF_Experience_Cloud/24-site-csp-security-level-and-trusted-scripts.md).

## Key points

- **Renamed in Winter '24 (API 59.0).** Up to API 58.0 it was **CSP Trusted Sites**; Permissions-Policy directives arrived with the new name, and the metadata type is still `CspTrustedSite`.
- **Setup → Trusted URLs → New Trusted URL:** API Name, URL, Description, Active, **CSP Context**, then the directive boxes. From API 59.0 at least one box must be ticked.
- **URL rules:** a domain, optional port, `*.example.com` allowed; `https://` for an API, `wss://` for a WebSocket. A malformed URL saved before February 2025 is silently left out of the header.
- **Each ticked box adds the host to one directive:**

| Directive | Allows | Use case |
|---|---|---|
| `connect-src` | `fetch`, XHR and WebSocket calls | an LWC calling a weather API; the Enhanced Chat `scrt2URL` |
| `frame-src` | the host inside an `<iframe>` | a YouTube or Vimeo embed; a payment provider's hosted form |
| `img-src` | images | product photos from a CDN |
| `font-src` | web fonts | `https://fonts.gstatic.com` for Google Fonts |
| `style-src` | external stylesheets | `https://fonts.googleapis.com`, the Google Fonts CSS |
| `media-src` | audio and video | a training MP4 from a CDN |

- **There is no `script-src` box.** The Lightning dev guide: *"You can't load JavaScript resources from a third-party site, even if it's a CSP Trusted Site"* — use a static resource → [03-lwc · 23](../03-lwc-and-slds/23-static-resources-and-third-party-javascript.md).
- **CSP Context sets where the entry applies:** **All** (default), **Lightning Experience pages**, **Experience Builder Sites**, **Visualforce Pages** — the last only for pages with `cspHeader="true"`. Pick the narrowest; the Trailhead's `SCRT_URL` entry uses Experience Builder Sites.
- **Permissions-Policy directives are `camera` and `microphone`.** They act only when Session Settings sends the Permissions-Policy HTTP header and sets that feature to **Trusted URLs Only** (`enablePermissionsPolicy`, `grantCameraAccess = TrustedUrls`).

## Gotchas

- **An entry is org-wide within its context.** Context All relaxes every Lightning page, every site and every opted-in Visualforce page at once → [20](20-my-domain-enhanced-domains-and-trusted-urls.md), [24](24-security-center-and-health-check.md).
- **The `connect-src (scripts)` label means script *interfaces*** — `fetch`, XHR, WebSocket — not loading a script file.
- **`frame-src` is not `frame-ancestors`.** Being framed *by* another site is clickjack protection: Session Settings → **Trusted Domains for Inline Frames** → [20](20-my-domain-enhanced-domains-and-trusted-urls.md).
- **Three lookalike lists:** Apex callouts need Remote Site Settings or a Named Credential → [06 · 17](../06-integration-and-apis/17-named-credentials-and-external-credentials.md); browser calls *into* Salesforce need CORS → [06 · 28](../06-integration-and-apis/28-cors-allowlist.md); redirects need **Trusted URLs for Redirects**.
- **Violations are console-first:** *"Refused to connect because it violates the document's Content Security Policy"*. Setup → **Trusted URL and Browser Policy Violations** keeps 7 days of Lightning Experience only; the **CSP Violation** event type is free → [23](23-event-monitoring-and-transaction-security.md).
- **The Summer '25 release update was canceled** — *Update Your Trusted URLs for the Latest CSP Directives* was never enforced. Session Settings → **Adopt updated CSP directives** still blocks non-compliant frames, images and fonts, and is on by default in orgs created Summer '24 or later.

## Gaps to close

- [ ] The Metadata API guide warns to keep the CSP header under 12 KB and reports trouble near 16 KB — is there a hard cap on Trusted URL entries, and what fails first?
- [ ] With **Adopt updated CSP directives** off, which `frame-src`, `img-src` and `font-src` requests are only reported as violations rather than blocked?

## Hands-on

- [ ] **SF-TURL-01** · 25 min · Build an LWC that `fetch`es a public JSON API with no Trusted URL, then add the host with `connect-src` only. **Proves:** the block is CSP — copy the console error verbatim — and one directive fixes it.
- [ ] **SF-TURL-02** · 15 min · Give a CDN host all six directives, then call `loadScript` with a script URL on it. **Proves:** there is no `script-src` route in Lightning; the static resource is the only way.
- [ ] **SF-TURL-03** · 15 min · Set the SF-TURL-01 entry to context **Experience Builder Sites** and reload the LWC in Lightning Experience. **Proves:** context is a real boundary — the same call is blocked again.
- [ ] **SF-TURL-04** · 15 min · Trigger one blocked request in Lightning Experience (SF-TURL-01 before the fix) and one on an Experience Builder site, then open **Trusted URL and Browser Policy Violations**. **Proves:** the list keeps the Lightning one and not the site one. **Needs:** an Experience Builder site.

## Related

- [20 · My Domain, enhanced domains & Trusted URLs](20-my-domain-enhanced-domains-and-trusted-urls.md) — the hostnames behind the header, clickjack protection and Trusted Domains for Inline Frames
- [06-integration · 28 CORS allowlist](../06-integration-and-apis/28-cors-allowlist.md) — the opposite direction: who may call Salesforce from a browser
- [06-integration · 17 Named credentials & external credentials](../06-integration-and-apis/17-named-credentials-and-external-credentials.md) — server-side callouts, which CSP never sees
- [03-lwc · 23 Static resources & third-party JavaScript](../03-lwc-and-slds/23-static-resources-and-third-party-javascript.md) — where a script goes when Trusted URLs cannot take it
- [03-lwc · 09 Lightning Web Security](../03-lwc-and-slds/09-lightning-web-security.md) — the other front-end guard, routinely blamed for CSP blocks
- [23 · Event monitoring & transaction security](23-event-monitoring-and-transaction-security.md) — the CSP Violation event type in the free tier
- [24 · Security Center & Health Check](24-security-center-and-health-check.md) — where loose and wildcard entries surface
- [SF_Experience_Cloud · 24 Site CSP, security level & trusted scripts](../../SF_Experience_Cloud/24-site-csp-security-level-and-trusted-scripts.md) — the per-site script list and security level that sit on top of this one
- [SF_Experience_Cloud · 19 Embedded messaging & agents in sites](../../SF_Experience_Cloud/19-embedded-messaging-and-agents-in-sites.md) — the chat widget whose `scrt2URL` needs an Experience Builder Sites entry
- [SF_Service · Embedded Service deployments](../../SF_Service/embedded-service-deployments.md) — the deployment and Code Snippet the `scrt2URL` is copied from
- [SF_Experience_Cloud · 25 Enhanced Chat on a site, step by step](../../SF_Experience_Cloud/25-enhanced-chat-on-a-site-step-by-step.md) — where the `scrt2URL` entry sits in the full site setup: step 3 of 6

## Sources

- [Manage Trusted URLs](https://help.salesforce.com/s/articleView?language=en_US&id=sf.security_trusted_urls_manage.htm&type=5) — Salesforce Help · via search 2026-09-24 · the directive boxes, CSP Context options, Permissions-Policy directives, **Trusted URLs Only**; the Console Integration Toolkit sentence *"Otherwise, you can't load JavaScript resources from a third party, even if it's a trusted URL"*
- [Metadata API Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_meta.pdf) — Salesforce Developers · read 2026-09-24 · `CspTrustedSite` (API 39.0; *"In API version 58.0 and earlier … referred to as CSP Trusted Sites"*; context values; URL rules; February 2025 malformed URLs; 12 KB / 16 KB header tip) and `SecuritySettings` (`enablePermissionsPolicy`, `grantCameraAccess`, `grantMicrophoneAccess`: Always / Never / TrustedUrls) — a Winter '27 build; only API 59.0-and-earlier fields are used
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `CspTrustedSite` field meanings; `IsApplicableToConnectSrc` = *"load URLs using script interfaces"*
- [Lightning Aura Components Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/lightning.pdf) — Salesforce Developers · read 2026-09-24 · *Making API Calls from Components*; *"You can't load JavaScript resources from a third-party site, even if it's a CSP Trusted Site"*
- [Write Content Security Policy-Compatible Code](https://trailhead.salesforce.com/content/learn/modules/secure-clientside-development/write-content-security-policy-compatible-code) — Trailhead · read 2026-09-24 · the six directives; JavaScript *"cannot be executed from that URL"*
- [Secure Access to Your Users' Camera and Microphone](https://help.salesforce.com/s/articleView?id=release-notes.rn_security_other_camera_microphone.htm&language=en_US&release=246&type=5) — Winter '24 release notes · via search 2026-09-24
- [Control Access to Browser Features](https://help.salesforce.com/s/articleView?language=en_US&id=sf.security_browser_features.htm&type=5) — Salesforce Help · via search 2026-09-24 · the Permissions-Policy header in Session Settings
- [Update Your Trusted URLs for the Latest CSP Directives (Release Update)](https://help.salesforce.com/s/articleView?id=release-notes.rn_security_other_update_csp_ru.htm&language=en_US&release=256&type=5) — Summer '25 release notes · via search 2026-09-24 · *"This update was canceled and no longer appears in the Release Update page in Setup"*
- [Salesforce Platform: Content Security Policy (CSP) Violations - Release Update Canceled](https://help.salesforce.com/s/articleView?id=002416582&language=en_US&type=1) — Salesforce Help KA 002416582, 7 March 2025 · read 2026-09-24 · *Adopt Updated CSP Directives* canceled; the setting restricts frames, images and fonts
- [Protect Your Org with Updated CSP Directives](https://help.salesforce.com/s/articleView?id=xcloud.security_trusted_urls_csp_directives_updated.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · on by default for orgs created Summer '24 or later
- [Manage Trusted URL and Browser Policy Violations](https://help.salesforce.com/s/articleView?id=xcloud.security_trusted_urls_csp_violations.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · seven days; CSP violations *"always related to a Lightning Experience page"*
- [CSP Violation Event Type](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_eventlogfile_cspviolation.htm) — Salesforce Developers · via search 2026-09-24
- [Specify Trusted Domains for Inline Frames](https://help.salesforce.com/s/articleView?language=en_US&id=xcloud.security_clickjack_specify_iframe_trusted_domains.htm&type=5) — Salesforce Help · via search 2026-09-24 · written into `frame-ancestors`
- [Specify Trusted URLs for Redirections](https://help.salesforce.com/s/articleView?language=en_US&id=xcloud.security_trusted_urls_external_redirections_specify.htm&type=5) — Salesforce Help · via search 2026-09-24 · the **Trusted URLs for Redirects** allowlist
- [Working with CORS and CSP to Call APIs from LWC](https://developer.salesforce.com/blogs/2022/03/working-with-cors-and-csp-to-call-apis-from-lwc) — Salesforce Developers Blog, March 2022 · via search 2026-09-24 · the console error string
- [LWR Sites for Experience Cloud (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/exp_cloud_lwr.pdf) — Salesforce Developers · read 2026-09-24 · Google Fonts needs `fonts.googleapis.com` and `fonts.gstatic.com` as Trusted URLs
- [Configure a Web Deployment](https://trailhead.salesforce.com/content/learn/projects/build-a-community-with-knowledge-and-chat/enable-and-configure-lightning-knowledge) — Trailhead project unit · read 2026-09-24 · `scrt2URL` → New Trusted URL, API Name `SCRT_URL`, CSP Context **Experience Builder Sites**, all six directives

## History

- 2026-09-24 · created from your Trailhead feed (Knowledge & Enhanced Chat site project)
- 2026-09-24 · linked SF_Experience_Cloud · 25, the step-by-step site guide
