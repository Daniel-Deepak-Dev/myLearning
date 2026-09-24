---
vault: SF_Experience_Cloud
format: light
level: working
status: open
gaps: 2
org_checks: 3
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [security]
---
# Site CSP: Security Level & Trusted Sites for Scripts

**One line:** Each Experience Builder site sets its own script policy — a **Security Level** and a **Trusted Sites for Scripts** list — on top of the org's Trusted URLs, which cover everything that is not a script.

**Reach for it when:** a head-markup tag or third-party library will not run on a site, or you must decide whether a site may run inline code at all.

> **From my notes.** *"CSP vs Trusted URLs why we have two options."* — On a site the two lists split by resource type. JavaScript hosts go in the site's **Trusted Sites for Scripts**; images, styles, fonts, media, frames and `fetch` targets go in org **Trusted URLs** → [SF_core · 07 · 27](../SF_core/07-security-and-sharing/27-trusted-urls-and-csp.md).

## Key points

- **Where it lives:** Experience Builder → Settings → **Security & Privacy**. The level and the script list are **per site**; *"you must allowlist each resource separately per site"*.
- **New sites default to Strict CSP** (since Spring '19). Help: it *"blocks the execution of all inline scripts and all requests for remote JavaScript files"*, still shows non-script resources from allowed hosts, and turns Lightning Locker on.
- **Relaxed CSP: Permit Access to Inline Scripts and Allowed Hosts** lets inline scripts run and loads remote JavaScript from hosts on the site's list. So a library in Settings → Advanced → **Edit Head Markup** needs Relaxed CSP plus a script-list entry; on LWR, wrap it in `<x-oasis-script>` to reach inside shadow DOM.
- **How the lists stack** (Help, *Where to Allowlist Third-Party Hosts*):

| Resource on the page | Where you allow the host | Reaches |
|---|---|---|
| `<script src>`, head-markup library | **Trusted Sites for Scripts**, with Relaxed CSP | this site |
| inline `<script>` | **Relaxed CSP** — no host to list | this site |
| `fetch`, WebSocket, the chat `scrt2URL` → [19](19-embedded-messaging-and-agents-in-sites.md) | **Trusted URLs**, `connect-src` | every site, if the context is Experience Builder Sites |
| image, font, stylesheet, media, iframe | **Trusted URLs**, the matching directive | every site, or the whole org on context All |

- **LWS and Locker differ by runtime.** An LWR site runs its own LWS instance, and the org's Session Settings LWS checkbox has no effect on it. On an Aura site, turning the site's Locker off turns off LWS too when the org uses LWS.
- **Locker off means packaged components must opt in** — Aura `lightningcommunity:allowInRelaxedCSP`, LWC `lightningCommunity__RelaxedCSP` → [06](06-custom-lwc-in-lwr-sites.md).

## Gotchas

- **An Experience Builder Sites entry reaches every site in the org.** There is no per-site Trusted URL, so least privilege stops at the context.
- **A third level is gone.** *Allow Inline Scripts and Script Access to Any Third-party Host* was removed in Spring '22, so a how-to that names it is stale.
- **Site violations show only in the browser console.** Setup's **Trusted URL and Browser Policy Violations** list holds Lightning Experience pages only.
- **Aura head markup bypasses Locker** — Locker isolates components, *"but not from the head markup"* — so the security level, not Locker, is what limits it.

## Gaps to close

- [ ] Does Strict CSP honour **Trusted Sites for Scripts** at all? Help says it blocks "all requests for remote JavaScript files", yet the list appears after either level.
- [ ] Can Lightning Locker be turned off on Strict CSP? The Experience Cloud Developer Guide says both "select Relaxed CSP" to reach the setting and "turn off Lightning Locker from the Relaxed CSP or Strict CSP security levels".

## Confirm in org

- 🚩 Does Relaxed CSP put `'unsafe-inline'` and `'unsafe-eval'` into the site's `script-src`? — DevTools → Network → the document's `Content-Security-Policy` header, Strict vs Relaxed.
- 🚩 Which of the six directives does the `scrt2URL` entry need? The Trailhead ticks all six — untick all but `connect-src`, publish, start a chat.
- 🚩 Does a security-level or script-list change reach the live site before you publish? — change it, reload the live URL, then publish and reload.

## Hands-on

- [ ] **EC-CSP-01** · 20 min · On a Strict CSP site, put `<script>console.log('head')</script>` in head markup, publish and reload; then switch to Relaxed CSP and publish again. **Proves:** Strict blocks inline script — copy the console error verbatim — and Relaxed runs it.
- [ ] **EC-CSP-02** · 20 min · On Relaxed CSP, load a CDN library from head markup with the host in org Trusted URLs (all six) but not in Trusted Sites for Scripts; then add it there. **Proves:** a Trusted URL cannot carry a script; only the site list can.
- [ ] **EC-CSP-03** · 20 min · On the Trailhead site, untick every directive on the `SCRT_URL` entry except `connect-src`, publish and start a chat; then untick `connect-src` too. **Settles:** which directives the chat needs. **Needs:** the Knowledge & Enhanced Chat project org.
- [ ] **EC-CSP-04** · 15 min · With EC-CSP-02 working, switch back to Strict CSP without touching the list, publish and reload. **Proves:** the entries survive the switch — and shows whether Strict still loads them.

## Related

- [SF_core · 07-security · 27 Trusted URLs & CSP](../SF_core/07-security-and-sharing/27-trusted-urls-and-csp.md) — the org half: the six directives, CSP Context and Permissions-Policy
- [SF_core · 06-integration · 28 CORS allowlist](../SF_core/06-integration-and-apis/28-cors-allowlist.md) — the CORS entry the same Trailhead step added, and the open question of whether chat needs it
- [06 · Custom LWC in LWR sites](06-custom-lwc-in-lwr-sites.md) — `lightningCommunity__RelaxedCSP`, the capability a packaged LWC needs on a Locker-off site
- [19 · Embedded messaging & agents in sites](19-embedded-messaging-and-agents-in-sites.md) — the chat widget whose `scrt2URL` needs the Trusted URL
- [05 · Branding sets, design tokens & SLDS 2](05-branding-sets-design-tokens-and-slds-2.md) — external fonts and imagery, which need Trusted URLs rather than the script list
- [03 · Site setup, domains & publishing](03-site-setup-domains-and-publishing.md) — publish vs activate, and the publish the last org check is about

## Sources

- [Where to Allowlist Third-Party Hosts for Experience Builder Sites](https://help.salesforce.com/s/articleView?id=experience.networks_security_csp_allow.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · scripts per site in **Security & Privacy**; non-scripts in Trusted URLs; *"you must allowlist each resource separately per site"*
- [Select a Security Level in Experience Builder Sites](https://help.salesforce.com/s/articleView?id=experience.networks_security_csp_scriptlevel.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Strict default since Spring '19; the removed third level; *"these allowed sites remain"*; activate or deactivate entries
- [CSP and Lightning Locker in Experience Builder Sites](https://help.salesforce.com/s/articleView?id=experience.networks_security_csp_overview.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · what Strict and Relaxed allow; Locker on by default
- [CSP and Lightning Locker Design Considerations](https://help.salesforce.com/s/articleView?id=experience.networks_security_csp_tips.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · non-script resources allowlisted at every level
- [Experience Cloud Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/communities_dev.pdf) — Salesforce Developers · read 2026-09-24 · *Develop Secure Sites: CSP, LWS, and Lightning Locker*; the two contradictory Locker sentences; head markup bypasses Locker; `allowInRelaxedCSP` and `lightningCommunity__RelaxedCSP` — a Winter '27 build; nothing used here is new in 68.0
- [LWR Sites for Experience Cloud (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/exp_cloud_lwr.pdf) — Salesforce Developers · read 2026-09-24 · **Relaxed CSP: Permit Access to Inline Scripts and Allowed Hosts**; `<x-oasis-script>`; *"switch to Relaxed CSP and to allowlist the remote host"*; the site's own LWS instance — a Winter '27 build
- [Manage Trusted URL and Browser Policy Violations](https://help.salesforce.com/s/articleView?id=xcloud.security_trusted_urls_csp_violations.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · CSP violations *"always related to a Lightning Experience page"*
- [Configure a Web Deployment](https://trailhead.salesforce.com/content/learn/projects/build-a-community-with-knowledge-and-chat/enable-and-configure-lightning-knowledge) — Trailhead project unit · read 2026-09-24 · the `SCRT_URL` Trusted URL in **Experience Builder Sites** with all six directives; no script-list step

## History

- 2026-09-24 · created from your Trailhead feed (Knowledge & Enhanced Chat site project)
