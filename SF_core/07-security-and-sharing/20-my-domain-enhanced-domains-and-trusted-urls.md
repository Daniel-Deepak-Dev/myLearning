# My Domain, Enhanced Domains & Trusted URLs

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 11

**Scope:** The org's own hostnames — how they are shaped, what stopped redirecting, and what the browser is allowed to load once a page is served from them. The LWS half of front-end security is [03-lwc · 09](../03-lwc-and-slds/09-lightning-web-security.md); this note owns the domain and CSP configuration behind it.

> **What changed.** *"Old URLs still redirect, so we can migrate the hardcoded ones later"* is wrong as of Spring '26. **Redirections for legacy My Domain hostnames ended in production** — an old link now fails outright rather than quietly forwarding. The API half is still in flight: an opt-in *Block API traffic that uses an incorrect instanced URL* switch became available **19 June 2026**, and support for incorrect instanced URLs ends in **Winter '27**.

## Core idea

Enhanced domains put your My Domain name into **every** URL the org serves — Lightning pages, Experience Cloud sites, Salesforce Sites, Visualforce, content files — instead of leaving some on shared instance hostnames like `na139.salesforce.com`. The driver was never branding: shared hostnames mean shared cookies, and browsers spent 2020–2024 removing the third-party-cookie behaviour that made them work. So this is a compliance-with-the-browser change, and the platform has been walking it forward through a redirect grace period that has now closed for the UI and is closing for the API. Everything that ever hardcoded a Salesforce URL is in scope: integrations, bookmarks, email templates, allowlists, documentation.

## How it works

| Surface | Shape under enhanced domains |
|---|---|
| Lightning & Setup | `MyDomainName.lightning.force.com` |
| Salesforce Sites / Experience Cloud | `MyDomainName.my.site.com` (plus any custom domain) |
| Content files | `MyDomainName.file.force.com` |
| API endpoints | `MyDomainName.my.salesforce.com` |
| Sandboxes | the My Domain name carries the sandbox name — which is why refreshes break allowlists |

- **Trusted URLs is the renamed CSP Trusted Sites**, and it is what lets a page load scripts, images, fonts, frames or make requests to a host other than Salesforce. Each entry chooses which CSP directives it relaxes.
- **A blocked external script is a CSP failure, not an LWS failure.** Phase 06 established this distinction and it is the single commonest misdiagnosis in LWC work — the fix is a Trusted URL entry, not a Session Settings checkbox. → [03-lwc · 09](../03-lwc-and-slds/09-lightning-web-security.md)
- **Clickjacking protection lives beside it** in Session Settings, and its defaults now block framing Salesforce pages in external sites — deliberate, and a frequent Experience Cloud embedding surprise.
- **Login discovery, SP-initiated SSO and multiple IdPs all depend on My Domain.** → [19](19-sso-saml-oidc-and-identity.md)
- **Instanced URLs are the remaining exposure.** An integration pinned to `na139.salesforce.com` or an instance-specific API host still works today, will fail on the opt-in switch, and stops being supported in Winter '27. Test with the switch on before the release forces it.

## 2026 currency

The redirect grace period is the story. Legacy hostname redirections **stopped in production and demo orgs in Spring '26**, so the failure mode changed from invisible-but-working to a hard 404 or blocked request — which is better for security and worse for anyone who deferred the audit. Since **19 June 2026** you can turn on *Block API traffic that uses an incorrect instanced URL* in the Redirections section of the My Domain Setup page to surface remaining offenders on your own schedule; **Winter '27 ends support** for that traffic regardless. Find them with Login History and API request logs rather than by grepping the codebase — most hardcoded URLs live in middleware and third-party configuration you do not own. → [23](23-event-monitoring-and-transaction-security.md)

## Gotchas

- **The failure is now silent-then-total.** Nothing degrades: a legacy URL returns 404 or is blocked, so an integration that "worked last week" stops entirely.
- **Email templates and Knowledge articles are full of hardcoded URLs** and neither shows up in a deployment diff.
- **Sandbox My Domain names change on refresh**, so every allowlist, IdP entity ID and CORS entry pointing at a sandbox is refresh-fragile. → [09-devops · 06](../09-devops-sfdx-and-release-management/06-source-tracking-and-sandbox-workflow.md)
- **CORS allowlist and Trusted URLs are different lists** solving different halves — CORS governs who may call Salesforce; Trusted URLs govern what a Salesforce page may load.
- **A Trusted URL entry is an org-wide relaxation of CSP.** Adding a wildcard host to make one component work weakens every page, and it is a Health Check item. → [24](24-security-center-and-health-check.md)
- **Guest-accessible Experience Cloud pages inherit all of it**, which is why the domain configuration is a guest-hardening concern too. → [05-experience-cloud · INDEX](../05-experience-cloud-lwr/INDEX.md)
- **Enabling enhanced domains is not reversible on a whim** — plan it as a release, with the allowlist inventory done first.

## Recall

Q: What changed about legacy My Domain hostnames in Spring '26?
A: Redirections ended in production. Old URLs now fail — 404 or blocked — instead of forwarding.

Q: What is the remaining instanced-URL timeline?
A: An opt-in *Block API traffic that uses an incorrect instanced URL* switch from 19 June 2026, and end of support in Winter '27.

Q: Why do enhanced domains exist at all?
A: Shared instance hostnames depend on third-party cookie behaviour browsers have removed. Putting the org's name in every URL removes that dependency.

Q: An LWC cannot load a script from an external CDN. Which setting is responsible?
A: Trusted URLs (CSP) — not Lightning Web Security. LWS is namespace isolation and does not block CDNs.

Q: What is the difference between the CORS allowlist and Trusted URLs?
A: CORS controls which external origins may call Salesforce. Trusted URLs control which external hosts a Salesforce-served page may load from or call.

## Related

- [19 · SSO, SAML, OIDC & identity](19-sso-saml-oidc-and-identity.md) — My Domain as the prerequisite for SP-initiated SSO
- [03-lwc · 09 Lightning Web Security](../03-lwc-and-slds/09-lightning-web-security.md) — what LWS does and does not block, and why CSP gets the blame
- [24 · Security Center & Health Check](24-security-center-and-health-check.md) — where loose Trusted URL entries surface
- [26 · Secure coding checklist](26-secure-coding-checklist.md) — the grep list, including hardcoded instance URLs
