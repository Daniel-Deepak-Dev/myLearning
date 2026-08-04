# Phases for 05 · Experience Cloud (LWR-first)

18 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs last (phases 18–19) on purpose.** Guest hardening depends on [07-security](../07-security-and-sharing/INDEX.md) (phases 10–11), custom components depend on [03-lwc](../03-lwc-and-slds/INDEX.md) (phases 05–07), and site deployment depends on [09-devops](../09-devops-sfdx-and-release-management/INDEX.md) (phases 16–17). Do not run this area early.

> ⛔ **Aura templates are legacy.** They appear only in **01** (the landscape comparison) and **16** (the deployment difference). Nowhere else.

---

## Phase 18 — LWR sites: architecture → auth · 10 files ⬜

```
01-template-choice-and-site-landscape.md           🆕⚠️
02-lwr-architecture-and-build-model.md             🆕
03-site-setup-domains-and-publishing.md
04-experience-builder-layouts-and-theme-layouts.md
05-branding-sets-design-tokens-and-slds-2.md       🆕
06-custom-lwc-in-lwr-sites.md                      🆕
07-guest-user-security-model.md                    ⚠️
08-licences-and-external-user-types.md
09-sharing-for-external-users.md
10-authentication-self-registration-and-sso.md
```

**⚠️ corrections to lead with**
- **01** — **LWR is the default for new sites; Aura templates are legacy.** Nearly every Experience Cloud tutorial online builds on Aura templates. This note's job is to make that unmistakable and to say what still forces an Aura template, if anything.
- **07** — guest access was **hardened by default**. Guest users can't be record owners, guest sharing rules are the only grant mechanism, and the old permissive defaults are gone. Any pre-2021 guest-access recipe is a security hole.

**🆕 — research before writing:** **01**, **02** (static build, SSR, CDN, hydration), **05**, **06**.

**Notes on scope**
- **02** is the note that makes everything else make sense: **LWR sites are built and served, not rendered per request like Aura.** That single fact explains the caching model, the SEO story and the SSR-safe component rules. Write it first.
- **06** — SSR-safe component rules are the practical trap: a component that touches `window` at module scope breaks the build. Depends on all of [03-lwc](../03-lwc-and-slds/INDEX.md), especially **· 14 SLDS 2**.
- **08** — licence types drive architecture more than anything else here. Get the current external user licence list from a source. **Internal licence gating is now owned by [07-security · 02](../07-security-and-sharing/02-licences-and-what-they-gate.md)** (written in phase 10) — this note owns the external half only, and the two should state the boundary explicitly.
- **09** — sharing sets and share groups are the external-user equivalents of sharing rules. Cross-link [07-security · 06, 09](../07-security-and-sharing/INDEX.md). **Carry forward from phase 10's seed harvest:** *sharing rules and manual sharing do not support high-volume community users*, who have no roles — which is the whole reason sharing sets exist.
- **10** — depends on [06-integration · 15 OAuth](../06-integration-and-apis/15-oauth-flows-and-authorization.md).

**Seed harvest** ([../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md)) — nearly nothing. `Exp Cloud Certification Prep` (2022) is the only relevant page, and the one Experience Cloud database row is a **Visualforce** trick, out of scope. Treat this area as greenfield.

---

## Phase 19 — Site content, headless, performance & agents · 8 files ⬜

```
11-navigation-search-and-audiences.md
12-enhanced-cms-and-content-delivery.md            🆕
13-headless-sites-and-connect-apis.md              🆕
14-site-performance-caching-and-seo.md             🆕
15-mobile-publisher-and-pwa-delivery.md
16-experience-cloud-devops.md                      ⚠️
17-embedded-messaging-and-agents-in-sites.md       🆕
18-site-monitoring-limits-and-scale.md
```

**⚠️** — **16**: **ExperienceBundle vs SiteDotCom** is the deployment trap. The metadata type you get depends on the template, they behave differently in source control, and this breaks pipelines regularly. Depends on [09-devops · 05](../09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md).

**🆕 — research before writing:** **12** (Enhanced CMS — content types, workspaces, channels), **13** (headless over Connect APIs), **14**, **17**.

**Notes on scope**
- **13** depends on [06-integration · 08 UI API](../06-integration-and-apis/08-ui-api-and-metadata-aware-clients.md). The judgment call — when a headless front end is worth abandoning Experience Builder for — is the actual content.
- **14** — LWR's SSR/CDN model is what makes real SEO possible here; this is where **02** pays off. Give concrete Lighthouse budgets if you can source them.
- **17** — seam into [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md). An agent on a **public** site is the highest-risk deployment surface on the platform: unauthenticated input, guest-user context, and a reasoning engine. Cross-link the Trust Layer note rather than restating it, but do not soften the risk.
- **18** — page-view limits and guest throttling are the capacity constraints that surprise people at launch. Get current numbers from a source.

## Closing the area

Phase 19 is the **last content run in the build**. When it lands: flip the final ⬜ in [../PHASES.md](../PHASES.md), and sweep every area `INDEX.md` to confirm all 190 rows are live links.
