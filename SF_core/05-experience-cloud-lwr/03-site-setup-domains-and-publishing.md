# Site Setup, Domains & Publishing

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

**Scope:** Standing a site up and getting it onto a URL people will type — enablement, domains, CDN, statuses and the publish lifecycle. The build model behind publishing is [02](02-lwr-architecture-and-build-model.md); pipeline deployment is [09-devops · 05](../09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md).

## Core idea

Two irreversible things happen before you build anything. **Enabling Digital Experiences fixes your org's site domain name permanently**, and **creating a site fixes its URL prefix and its runtime**. Neither can be changed afterwards, and both end up in every link, bookmark, email template and integration you ever ship. Spend the ten minutes.

After that the model is simple and worth stating plainly because two words get conflated: **publish** makes builder changes live; **activate** makes the site reachable by its members. They are independent, and a site can be published and inactive.

## How it works

- **Setup → Digital Experiences → Settings** enables the feature and takes the org-wide domain (`<name>.my.site.com`). One-time, irreversible, and it is *not* your My Domain name — though it inherits My Domain's fate → [07-security · 20](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md).
- **Each site gets a URL prefix** appended to that domain. Also permanent.
- **Custom domains** are added under **Setup → Domains → Add a Domain**, then mapped to a site under **Custom URLs**. Choose *Serve the domain with the Salesforce CDN* for Experience Cloud; the **Cloudflare** option belongs to Commerce LWR sites and to Experience Delivery, which is **being discontinued in Winter '27** → [02](02-lwr-architecture-and-build-model.md). The default Salesforce CDN path is **Akamai**.
- **Custom domains are production-only** and need Enterprise, Performance or Unlimited — you cannot rehearse them in a Developer Edition org, and sandbox site URLs differ from production by construction.
- **Three statuses**: *Preview* (builder-visible, members can't reach it), *Active* (live to members), *Inactive* (serves the **Service Not Available** page, which is itself customisable).
- **Publish is per-site and ships everything currently saved in the builder** — including another person's in-progress edits. There is no per-change publish.
- **100 sites per org**, counting active, inactive, preview and Visualforce sites together.
- **Guest page views are metered by edition** — an Enterprise-edition site is provisioned against an annual page-view allowance, which is a capacity conversation before launch, not after → [09-devops · 20](../09-devops-sfdx-and-release-management/20-release-management-and-org-upgrades.md).

## 2026 currency

The domain layer moved under everyone's feet in 2026 and Experience Cloud inherits all of it. **Legacy My Domain hostname redirections ended in Spring '26 — a stale hostname now 404s rather than forwarding**, so an old bookmark or an email template with a hardcoded site URL fails silently for the person who clicks it. Separately, **API traffic on instanced hostnames stops being supported around Winter '27**, which reaches any integration pointed at a site. Both are recorded once in [07-security · 20](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md) and [06-integration · 03](../06-integration-and-apis/03-api-endpoints-hostnames-and-edge-network.md); the Experience Cloud angle is simply that **guest pages are the most-linked-to URLs you own**, so they have the longest tail of stale references.

## Gotchas

- **The Digital Experiences domain name cannot be changed.** Neither can a site's URL prefix. Both outlive the project.
- **Publishing is not deploying.** Publish makes builder changes live in *that* org; moving them to another org is Metadata API → [02](02-lwr-architecture-and-build-model.md).
- **Deactivating a site does not unpublish it** — it serves Service Not Available while the built assets remain.
- **A custom domain needs a certificate that matches it**, and the certificate has its own expiry clock that is getting shorter every year → [06-integration · 26](../06-integration-and-apis/26-certificates-mutual-tls-and-the-pki-changes.md).
- **Site URLs differ between sandbox and production**, so anything that hardcodes one breaks on deploy. Use custom labels or custom settings → [01-admin · 10](../01-admin-and-declarative-platform/10-custom-labels-and-translation-workbench.md).
- **Preview status is not private.** It restricts membership access, not secrecy — treat an unlaunched site's guest surface as live → [11](11-public-site-exposure-audit.md).

## Recall

Q: Which two setup decisions in Experience Cloud are permanent?
A: The org's Digital Experiences domain name, and each site's URL prefix — plus the template's runtime, decided at creation.

Q: What is the difference between publishing and activating a site?
A: Publish makes Experience Builder changes live; activate makes the site reachable by members. They are independent.

Q: Which CDN serves an Experience Delivery site?
A: Cloudflare — the default Salesforce CDN path for other Experience Cloud domains is Akamai. Note Experience Delivery itself is being discontinued in Winter '27, so Cloudflare's remaining Experience Cloud case is Commerce LWR.

Q: What happens when a site is set to Inactive?
A: It serves the customisable Service Not Available page; the published assets are unaffected.

Q: Why is the end of My Domain redirections an Experience Cloud problem specifically?
A: Guest site URLs are the most widely linked-to URLs an org owns, so stale hostnames now 404 for external people you cannot reach.

## Related

- [02 · LWR architecture & build model](02-lwr-architecture-and-build-model.md) — why publish is a build step
- [11 · Public site exposure audit](11-public-site-exposure-audit.md) — what to check before a site is reachable
- [07-security · 20 My Domain, enhanced domains & Trusted URLs](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md) — the domain rules this inherits
- [06-integration · 26 Certificates, mutual TLS & the PKI changes](../06-integration-and-apis/26-certificates-mutual-tls-and-the-pki-changes.md) — the certificate clock behind a custom domain
