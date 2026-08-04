# 05 · Experience Cloud (LWR-first)

Public, partner and customer sites built **LWR-first**. **20 topics** · phases [18](PHASES.md), [19](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **The area's own headline was half wrong, and phase 18 corrected it.** LWR is the strategic runtime and where every new capability lands — but **only two templates are LWR**, *Build Your Own (LWR)* and *Microsite (LWR)*. **Customer Service, Partner Central, Customer Account Portal, Help Center and Build Your Own are Aura templates, still creatable at 67.0, still receiving Summer '26 features, with no announced retirement date.** This area teaches LWR because that is where the platform is going; it does **not** claim Aura is dead, and a migration business case built on that claim is built on sand → [01](01-template-choice-and-site-landscape.md), [12](12-aura-to-lwr-migration-and-coexistence.md).

> ⚠️ **"LWR" is two products.** LWR and **enhanced LWR** use different metadata types, and the *Upgrade to Enhanced LWR Sites* Release Update — scheduled for enforcement in Spring '26 — **has not been enforced since Summer '25** → [02](02-lwr-architecture-and-build-model.md).

> ⚠️ Runs **late** (phases 18–19) on purpose: guest-user hardening depends on [07-security-and-sharing](../07-security-and-sharing/INDEX.md), and site deployment depends on [09-devops](../09-devops-sfdx-and-release-management/INDEX.md).

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | [Template choice & site landscape](01-template-choice-and-site-landscape.md) 🆕⚠️ | **two LWR templates, five Aura ones, none retired** | 18 |
| 02 | [LWR architecture & build model](02-lwr-architecture-and-build-model.md) 🆕⚠️ | built not rendered; enhanced LWR; Experience Delivery **Beta** | 18 |
| 03 | [Site setup, domains & publishing](03-site-setup-domains-and-publishing.md) | irreversible names, Salesforce CDN vs Cloudflare, publish ≠ activate | 18 |
| 04 | [Experience Builder layouts & theme layouts](04-experience-builder-layouts-and-theme-layouts.md) | theme vs page layout, slots, the LWR targets | 18 |
| 05 | [Branding sets, design tokens & SLDS 2](05-branding-sets-design-tokens-and-slds-2.md) 🆕 | `--dxp` hooks, branding sets, **tokens inert under SLDS 2** | 18 |
| 06 | [Custom LWC in LWR sites](06-custom-lwc-in-lwr-sites.md) 🆕 | targets, `import.meta.env.SSR`, toasts fail silently | 18 |
| 07 | [Guest user security model](07-guest-user-security-model.md) ⚠️ | guest sharing rules only, read-only, no ownership, read/create only | 18 |
| 08 | [Licences & external user types](08-licences-and-external-user-types.md) | high-volume vs role-based; member vs login billing | 18 |
| 09 | [Sharing for external users](09-sharing-for-external-users.md) | sharing sets, share groups, super user access | 18 |
| 10 | [Authentication, self-registration & SSO](10-authentication-self-registration-and-sso.md) | Login & Registration, JIT, login flows, Headless Identity | 18 |
| 11 | [Public site exposure audit](11-public-site-exposure-audit.md) 🆕⚠️ | **the 7 Mar 2026 advisory**; the eight-item guest audit | 18 |
| 12 | [Aura to LWR: migration & coexistence](12-aura-to-lwr-migration-and-coexistence.md) 🆕⚠️ | **no converter exists**; rebuild and cut over, or don't | 18 |
| 13 | Navigation, search & audiences | nav menus, search config, audience targeting | 19 |
| 14 | Enhanced CMS & content delivery 🆕 | content types, workspaces, channels | 19 |
| 15 | Headless sites & Connect APIs 🆕 | decoupled front ends over Connect/Headless APIs | 19 |
| 16 | Site performance, caching & SEO 🆕 | SSR caching, Lighthouse budgets, LWR SEO | 19 |
| 17 | Mobile Publisher & PWA delivery | branded apps, PWA option, review pipeline | 19 |
| 18 | Experience Cloud DevOps ⚠️ | ExperienceBundle vs DigitalExperienceBundle, deployment gotchas | 19 |
| 19 | Embedded messaging & agents in sites 🆕 | embedded service deployment, agent on public sites | 19 |
| 20 | Site monitoring, limits & scale | page view limits, guest throttling, capacity planning | 19 |

## Related

- **06** depends on all of [03-lwc-and-slds](../03-lwc-and-slds/INDEX.md), especially **· 14 SLDS 2**, **· 18 toasts** and **· 13 shadow DOM**.
- **07, 09, 11** are the site-facing projection of [07-security · 06 OWD](../07-security-and-sharing/06-org-wide-defaults-and-record-access.md) and **· 14 execution context**.
- **10** depends on [06-integration · 15 OAuth flows](../06-integration-and-apis/15-oauth-flows-and-authorization.md) and [07-security · 19 SSO](../07-security-and-sharing/19-sso-saml-oidc-and-identity.md).
- **15** depends on [06-integration · 08 UI API](../06-integration-and-apis/08-ui-api-and-metadata-aware-clients.md).
- **18** depends on [09-devops · 05 Metadata API](../09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md) — and on **02**, which owns the two bundle types.
- **19** is a seam into [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md).
- **11 is the note the other eleven exist to make possible.** A site is a data surface before it is a user experience, and the March 2026 campaign is the reason that sentence is in an INDEX rather than a footnote.
