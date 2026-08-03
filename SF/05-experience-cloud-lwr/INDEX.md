# 05 · Experience Cloud (LWR-first)

Public, partner and customer sites built **LWR-first**. **18 topics** · phases [18](PHASES.md), [19](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **LWR is the default template for new sites; Aura templates are legacy.** Almost every Experience Cloud tutorial online builds on Aura templates. Treat them as read-only history — this area teaches LWR and covers Aura only as a migration concern.

> ⚠️ Runs **late** (phases 18–19) on purpose: guest-user hardening depends on [07-security-and-sharing](../07-security-and-sharing/INDEX.md), and site deployment depends on [09-devops](../09-devops-sfdx-and-release-management/INDEX.md).

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | Template choice & site landscape 🆕⚠️ | LWR is the default; Aura templates legacy | 18 |
| 02 | LWR architecture & build model 🆕 | static build, SSR, CDN, hydration | 18 |
| 03 | Site setup, domains & publishing | custom domains, publish pipeline, environments | 18 |
| 04 | Experience Builder layouts & theme layouts | sections, regions, theme layout components | 18 |
| 05 | Branding sets, design tokens & SLDS 2 🆕 | tokens, branding sets, Cosmos alignment | 18 |
| 06 | Custom LWC in LWR sites 🆕 | site targets, property editors, SSR-safe component rules | 18 |
| 07 | Guest user security model ⚠️ | guest sharing rules, hardening defaults, no owner access | 18 |
| 08 | Licences & external user types | customer/partner/external identity, login-based licensing | 18 |
| 09 | Sharing for external users | sharing sets, share groups, super user access | 18 |
| 10 | Authentication, self-registration & SSO | login flows, social sign-on, headless identity | 18 |
| 11 | Navigation, search & audiences | nav menus, search config, audience targeting | 19 |
| 12 | Enhanced CMS & content delivery 🆕 | content types, workspaces, channels | 19 |
| 13 | Headless sites & Connect APIs 🆕 | decoupled front ends over Connect/Headless APIs | 19 |
| 14 | Site performance, caching & SEO 🆕 | SSR caching, Lighthouse budgets, LWR SEO | 19 |
| 15 | Mobile Publisher & PWA delivery | branded apps, PWA option, review pipeline | 19 |
| 16 | Experience Cloud DevOps ⚠️ | ExperienceBundle vs SiteDotCom, deployment gotchas | 19 |
| 17 | Embedded messaging & agents in sites 🆕 | embedded service deployment, agent on public sites | 19 |
| 18 | Site monitoring, limits & scale | page view limits, guest throttling, capacity planning | 19 |

## Related

- **06** depends on all of [03-lwc-and-slds](../03-lwc-and-slds/INDEX.md), especially **· 14 SLDS 2**.
- **07, 09** are the site-facing projection of [07-security-and-sharing · 06 OWD](../07-security-and-sharing/INDEX.md) and **· 14 execution context**.
- **10** depends on [06-integration · 13 OAuth flows](../06-integration-and-apis/INDEX.md).
- **13** depends on [06-integration · 07 UI API](../06-integration-and-apis/INDEX.md).
- **16** depends on [09-devops · 05 Metadata API](../09-devops-sfdx-and-release-management/INDEX.md).
- **17** is a seam into [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md).
