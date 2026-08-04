# Phases for 05 · Experience Cloud (LWR-first)

20 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs last (phases 18–19) on purpose.** Guest hardening depends on [07-security](../07-security-and-sharing/INDEX.md) (phases 10–11), custom components depend on [03-lwc](../03-lwc-and-slds/INDEX.md) (phases 05–07), and site deployment depends on [09-devops](../09-devops-sfdx-and-release-management/INDEX.md) (phases 16–17). Do not run this area early.

> ⛔ **The Aura scope rule from the original plan was withdrawn in phase 18.** It read: *"Aura templates are legacy. They appear only in 01 and 16."* Research contradicted the premise — **five of the seven current templates are Aura, none is retired, and Summer '26 shipped features to them** — so Aura now appears wherever a decision genuinely turns on it: **01** (the landscape), **04** (the layout component model), **12** (migration) and **18** (the deployment difference). It is still not taught as a build target.

---

## Phase 18 — LWR sites: architecture → auth · 12 files ✅

```
01-template-choice-and-site-landscape.md           🆕⚠️
02-lwr-architecture-and-build-model.md             🆕⚠️
03-site-setup-domains-and-publishing.md
04-experience-builder-layouts-and-theme-layouts.md
05-branding-sets-design-tokens-and-slds-2.md       🆕
06-custom-lwc-in-lwr-sites.md                      🆕
07-guest-user-security-model.md                    ⚠️
08-licences-and-external-user-types.md
09-sharing-for-external-users.md
10-authentication-self-registration-and-sso.md
11-public-site-exposure-audit.md                   🆕⚠️  ← added, beyond plan
12-aura-to-lwr-migration-and-coexistence.md        🆕⚠️  ← added, beyond plan
```

**Rule 1 exceeded deliberately — two files added and appended, not inserted.** Area 05 had no files, but eight notes in areas 01, 03, 04, 06 and 07 already name **05 · 07**, **· 08**, **· 09**, **· 10** and **· 13** by number. Appending as **11–12** left every one of those correct except the phase-19 headless reference, which moved 13 → 15. Same call phases 13 and 15 made, for the same reason. Phase 19 shifted to **13–20**.

**What the two additions are for**
- **11** — the plan gave guest security one file, **07**, and treated it as a design topic. The 7 March 2026 Salesforce advisory makes it an operational one: the *model* has been enforced since 2021 and the *configurations* are what failed. Splitting the runbook out of the model was the only way to keep both under the line cap and to give the audit somewhere to live.
- **12** — the plan's own scope rule forbade this note, on a premise the research disproved. "How do we get off Aura" is the first question any inherited Experience Cloud estate asks, and the honest answer — *no converter exists, and you may not want to* — had nowhere to live.

**⚠️ corrections that landed, and how they differ from the plan's**
- **01** — the plan's ⚠️ was *"LWR is the default; Aura templates are legacy"* and asked what still forces Aura. **The answer is: most purpose-built templates.** Only Build Your Own (LWR) and Microsite (LWR) are LWR. **This is the fifth phase where the plan's own correction was the stale thing** — see [../CURRENCY.md](../CURRENCY.md).
- **02** — unplanned, and the larger of the two: **LWR ≠ enhanced LWR**, different metadata types, and the upgrade Release Update **stopped being enforced in Summer '25** after being scheduled for Spring '26.
- **07** — as planned, and it held: hardened by default, guest sharing rules only, read-only, no ownership, read/create only.
- **12** — **"no converter exists"** is the correction, and it is inconvenient rather than interesting, which is why it needed writing down.

**🆕 researched before writing:** **01**, **02** (Experience Delivery **is still Beta**, Summer '24 onward; islands, `lwr:hydrate`, Cloudflare vs Akamai), **05** (`--dxp` hooks, SLDS 2 token removal), **06**, **11**, **12**.

**Seed harvest** ([../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md)) — as predicted, nearly nothing. `Exp Cloud Certification Prep` (2022) is the only relevant page and the one Experience Cloud database row is a **Visualforce** trick, out of scope. The one genuinely useful line came second-hand, via phase 10's harvest: *sharing rules and manual sharing do not support high-volume community users* — quoted in **09**, where it belongs.

---

## Phase 19 — Site content, headless, performance & agents · 8 files ✅

```
13-navigation-search-and-audiences.md
14-enhanced-cms-and-content-delivery.md            🆕
15-headless-sites-and-connect-apis.md              🆕
16-site-performance-caching-and-seo.md             🆕
17-mobile-publisher-and-pwa-delivery.md
18-experience-cloud-devops.md                      ⚠️
19-embedded-messaging-and-agents-in-sites.md       🆕
20-site-monitoring-limits-and-scale.md
```

**⚠️** — **18**: the deployment trap is **`ExperienceBundle` vs `DigitalExperienceBundle` + `DigitalExperienceConfig`**, and phase 18 · **02** already owns the distinction — this note owns what it does to a pipeline. Note the sharper framing phase 18 found: **`ExperienceBundle` does not identify the runtime**, because Aura sites and non-enhanced LWR sites both use it. Depends on [09-devops · 05](../09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md).

**🆕 — research before writing:** **14** (Enhanced CMS — content types, workspaces, channels; note these are **enhanced-LWR-only**), **15** (headless over Connect APIs), **16**, **19**.

**Notes on scope**
- **15** depends on [06-integration · 08 UI API](../06-integration-and-apis/08-ui-api-and-metadata-aware-clients.md). The judgment call — when a headless front end is worth abandoning Experience Builder for — is the actual content. **Headless Identity is already covered in [10](10-authentication-self-registration-and-sso.md)**; do not restate it.
- **16** — LWR's SSR/CDN model is what makes real SEO possible, and this is where **02** pays off. **Carry forward that Experience Delivery is Beta** — a performance note that assumes it is GA is wrong. Give concrete Lighthouse budgets if you can source them.
- **19** — seam into [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md). An agent on a **public** site is the highest-risk deployment surface on the platform: unauthenticated input, guest-user context, and a reasoning engine. Cross-link the Trust Layer note rather than restating it, and cross-link **[11](11-public-site-exposure-audit.md)** — an agent is a new item on that audit, not a separate subject.
- **20** — page-view limits and guest throttling are the capacity constraints that surprise people at launch. Phase 18 sourced two numbers to build on: **100 sites per org** (counting inactive, preview and Visualforce sites) and an edition-scaled annual guest page-view allowance. Get the current per-edition figures from a source.

## Closing the area

Phase 19 is the **last content run in the build**. When it lands: flip the final ⬜ in [../PHASES.md](../PHASES.md), and sweep every area `INDEX.md` to confirm all 215 rows are live links.
