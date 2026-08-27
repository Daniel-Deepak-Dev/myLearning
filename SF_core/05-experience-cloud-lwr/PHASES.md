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
- **02** — unplanned, and the larger of the two: **LWR ≠ enhanced LWR**, different metadata types, and the upgrade Release Update **stopped being enforced in Summer '25** after being scheduled for Spring '26. *(This note's Experience Delivery content was rewritten by phase 19 — see that phase's section.)*
- **07** — as planned, and it held: hardened by default, guest sharing rules only, read-only, no ownership, read/create only.
- **12** — **"no converter exists"** is the correction, and it is inconvenient rather than interesting, which is why it needed writing down.

**🆕 researched before writing:** **01**, **02** (Experience Delivery ~~**is still Beta**~~ — *true when written; **phase 19 found it is being discontinued in Winter '27**, see below* — Summer '24 onward; islands, `lwr:hydrate`, Cloudflare vs Akamai), **05** (`--dxp` hooks, SLDS 2 token removal), **06**, **11**, **12**.

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

**No files added, nothing renumbered — the only phase in the build to do neither.** Area 05 was fully planned by phase 18, so 13–20 landed exactly as listed. The work that mattered was not authoring; it was **the verification pass, which overturned phase 18's headline finding one release after it was recorded.**

**⚠️ corrections as written — three, where the plan anticipated one**

- **18** — as planned, and it held. The deployment trap is **`ExperienceBundle` vs `DigitalExperienceBundle` + `DigitalExperienceConfig`**; phase 18 · **02** owns the distinction, this note owns what it does to a pipeline. The sharper framing carried through: **`ExperienceBundle` does not identify the runtime**, because Aura and non-enhanced LWR both use it. Depends on [09-devops · 05](../09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md).
- **16 — upgraded to ⚠️, and it is the phase's headline.** The plan said *"Carry forward that Experience Delivery is Beta."* **It is being discontinued in Winter '27 and is already closed to new enablement** — orgs that never turned it on have no toggle; those that did run until **October 2026**. The note's entire SSR framing had to be rebuilt around **static build + CDN with no SSR at all**. This is the **sixth** time a plan's own ⚠️ was stale — and the first time the stale correction was **one phase old**, not four.
- **19 — upgraded to ⚠️, two directions on one page**, the same shape as [09-devops · 24](../09-devops-sfdx-and-release-management/24-vscode-code-builder-and-tooling.md). **Messaging for In-App and Web was renamed Enhanced Chat in June 2025** (v2 in Winter '26) — a product-name error the note shipped with. And **legacy Chat / Live Agent genuinely was retired, 14 February 2026** — which the note asserted correctly but undated, the one claim shape this vault demands evidence for.
- **20 — upgraded to ⚠️.** The plan said *"get the current per-edition figures from a source"*; the draft instead told the reader to go look them up, and asserted **overage is "billed, not blocked."** That is wrong: **110% for four consecutive months, or 300% in one month, and Salesforce can disable the sites.** The comfortable version of a limit is the one that gets written down.

**🆕 researched:** **14** (Enhanced CMS — enhanced-LWR-only; **100 active custom content types**, **2,000 workspaces**, collections **50 manual / 250 dynamic** — the second tier was missing), **15** (headless over Connect APIs), **16**, **19**. The finding that most changed a note was **16**'s, and the second was that **Salesforce publishes no Lighthouse budget for Experience Cloud** — the plan asked for concrete budgets "if you can source them", and the sourced answer is that none exist. Logged in [../CURRENCY.md](../CURRENCY.md) as a fourth failure class: **withdrawn from Beta without ever reaching GA.**

**Scope notes the plan left, and what happened to them**
- **15** carries the judgment call as its content, depends on [06-integration · 08 UI API](../06-integration-and-apis/08-ui-api-and-metadata-aware-clients.md), and does **not** restate Headless Identity — [10](10-authentication-self-registration-and-sso.md) owns it. Its sharpest line is that **headless still requires a site**.
- **19** seams into [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md), cross-links the Trust Layer rather than restating it, and treats an embedded agent as **a new line item on [11](11-public-site-exposure-audit.md)**, not a separate subject.
- **20** kept phase 18's **100 sites per org** (counting inactive, preview and Visualforce) and replaced the hedged allowance with the sourced one.

**Seed harvest — none, and that was correct.** [../\_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) line 121 maps only `Exp Cloud Certification Prep` (2022) and a ⛔-skip Visualforce row to this area, both already spent by phase 18. Recording zero here so a later reader does not mistake it for an omission.

## Closing the area

**Area complete.** 20 topics, phases 18–19 — and phase 19 was the last content run in the build. All 215 rows across the nine areas are live links; the final ⬜ in [../PHASES.md](../PHASES.md) is flipped.

> **What this area proved, and it is the reason the standing rules exist.** Phase 18 found that the vault's own INDEX, area plan and `CURRENCY.md` all asserted the same wrong thing about Aura, and concluded: *when a phase overturns a correction, grep the vault for every place it was ever asserted.* Phase 19 had to run exactly that procedure against **phase 18's own finding**, correcting five notes and three plan-level artefacts. **A correction is not a durable fact; it is a dated observation.** Re-check at the source.
