# SF_Experience_Cloud — Experience Cloud (LWR-first)

> **Start at [../HOME.md](../HOME.md)** — what to study next, rebuilt from the notes.

Public, partner and customer sites built **LWR-first**. **24 topics** · phases [18](PHASES.md), [19](PHASES.md), plus fed topics appended beyond them.

> Currency: **Summer '26 (API 67.0)** · [flag legend](../SF_core/README.md#flag-legend) · [what changed](../SF_core/CURRENCY.md) · [how to write here](AGENTS.md)

> **This vault was `SF_core/05-experience-cloud-lwr/` until 2026-09-19.** It is now a root-level vault beside [SF_core/](../SF_core/README.md), [SF_Agentforce/](../SF_Agentforce/INDEX.md), [SF_Data_360/](../SF_Data_360/INDEX.md) and — since 2026-09-24 — [SF_Service/](../SF_Service/INDEX.md). Filenames and numbering are unchanged. The build record stays in [../SF_core/PHASES.md](../SF_core/PHASES.md) and the currency rows stay in [../SF_core/CURRENCY.md](../SF_core/CURRENCY.md) — one ledger for the whole platform.

> ⚠️ **The area's own headline was half wrong, and phase 18 corrected it.** LWR is the strategic runtime and where every new capability lands — but **only two templates are LWR**, *Build Your Own (LWR)* and *Microsite (LWR)*. **Customer Service, Partner Central, Customer Account Portal, Help Center and Build Your Own are Aura templates, still creatable at 67.0, still receiving Summer '26 features, with no announced retirement date.** This vault teaches LWR because that is where the platform is going; it does **not** claim Aura is dead, and a migration business case built on that claim is built on sand → [01](01-template-choice-and-site-landscape.md), [12](12-aura-to-lwr-migration-and-coexistence.md).

> ⚠️ **"LWR" is two products.** LWR and **enhanced LWR** use different metadata types, and the *Upgrade to Enhanced LWR Sites* Release Update — scheduled for enforcement in Spring '26 — **has not been enforced since Summer '25** → [02](02-lwr-architecture-and-build-model.md).

> ⚠️ **Experience Delivery is discontinued as of Winter '27 — but SSR is not gone.** Experience Delivery was the Cloudflare-backed *hosting* tier: Beta from Summer '24, never flipped, and republishing an affected site migrates it to standard LWR infrastructure. **Islands server-side rendering survived it** and is a standard LWR capability, on by default on Build Your Own (LWR) standard pages, gated per page by `lightning__ServerRenderable` on the theme layout. Phase 18 called the feature "still Beta"; phase 19 read the withdrawal too broadly and declared SSR dead. **Both were wrong — name the thing that was withdrawn, not the category it sat in** → [02](02-lwr-architecture-and-build-model.md), [16](16-site-performance-caching-and-seo.md).

> ⚠️ Runs **late** (phases 18–19) on purpose: guest-user hardening depends on [07-security-and-sharing](../SF_core/07-security-and-sharing/INDEX.md), and site deployment depends on [09-devops](../SF_core/09-devops-sfdx-and-release-management/INDEX.md).

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | [Template choice & site landscape](01-template-choice-and-site-landscape.md) 🆕⚠️ | **two LWR templates, five Aura ones, none retired** | 18 |
| 02 | [LWR architecture & build model](02-lwr-architecture-and-build-model.md) 🆕⚠️ | built not rendered; enhanced LWR; Experience Delivery **discontinued Winter '27**, islands SSR survives it | 18 |
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
| 13 | [Navigation, search & audiences](13-navigation-search-and-audiences.md) | nav menus, search config, audience targeting | 19 |
| 14 | [Enhanced CMS & content delivery](14-enhanced-cms-and-content-delivery.md) 🆕 | content types, workspaces, channels, enhanced-LWR-only | 19 |
| 15 | [Headless sites & Connect APIs](15-headless-sites-and-connect-apis.md) 🆕 | decoupled front ends over Connect/Headless APIs | 19 |
| 16 | [Site performance, caching & SEO](16-site-performance-caching-and-seo.md) 🆕⚠️ | **no SSR to plan for** — static build + CDN is the whole story | 19 |
| 17 | [Mobile Publisher & PWA delivery](17-mobile-publisher-and-pwa-delivery.md) | branded apps, PWA option, review pipeline | 19 |
| 18 | [Experience Cloud DevOps](18-experience-cloud-devops.md) ⚠️ | ExperienceBundle vs DigitalExperienceBundle, deployment gotchas | 19 |
| 19 | [Embedded messaging & agents in sites](19-embedded-messaging-and-agents-in-sites.md) 🆕⚠️ | **Enhanced Chat** (renamed 2025); legacy Chat **retired 14 Feb 2026**; agent on public sites | 19 |
| 20 | [Site monitoring, limits & scale](20-site-monitoring-limits-and-scale.md) ⚠️ | **overage disables sites**, not just bills; EE 500k/mo, UE/PE 1M/mo | 19 |
| 21 | [Multilingual sites & site translation](21-multilingual-sites-and-translation.md) | three translation surfaces; **40 languages**; CMS variants; the per-language URL question | — |
| 22 | [Site accessibility & conformance](22-site-accessibility-and-conformance.md) 🆕⚠️ | **the ACR is not your site's claim**; EAA 28 Jun 2025, EN 301 549 v3.2.1 = WCAG 2.1 AA | — |
| 23 | [Topics & Knowledge on sites](23-topics-and-knowledge-on-sites.md) | navigational, featured and content topics; Article Management; what really makes an article visible | — |
| 24 | [Site CSP, security level & trusted scripts](24-site-csp-security-level-and-trusted-scripts.md) | Strict vs Relaxed CSP; Trusted Sites for Scripts per site; how it stacks on org Trusted URLs | — |

## Related

- **06** depends on all of [03-lwc-and-slds](../SF_core/03-lwc-and-slds/INDEX.md), especially **· 14 SLDS 2**, **· 18 toasts** and **· 13 shadow DOM**.
- **07, 09, 11** are the site-facing projection of [07-security · 06 OWD](../SF_core/07-security-and-sharing/06-org-wide-defaults-and-record-access.md) and **· 14 execution context**.
- **10** depends on [06-integration · 15 OAuth flows](../SF_core/06-integration-and-apis/15-oauth-flows-and-authorization.md) and [07-security · 19 SSO](../SF_core/07-security-and-sharing/19-sso-saml-oidc-and-identity.md).
- **15** depends on [06-integration · 08 UI API](../SF_core/06-integration-and-apis/08-ui-api-and-metadata-aware-clients.md).
- **18** depends on [09-devops · 05 Metadata API](../SF_core/09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md) — and on **02**, which owns the two bundle types.
- **19** is a seam into [SF_Agentforce/](../SF_Agentforce/INDEX.md).
- **11 is the note the other eleven exist to make possible.** A site is a data surface before it is a user experience, and the March 2026 campaign is the reason that sentence is in an INDEX rather than a footnote.
