# Phases for 03 · LWC & SLDS

22 topics across 3 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Area constraint.** Aura and Visualforce are **out of scope**. They may be named only in a migration or coexistence sentence — never as an approach. The old notes contain several Aura-flavoured pages ([../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) marks them ⛔); skip those outright.

---

## Phase 05 — LWC entry · 5 files ⬜

Shares a run with the Apex closeout — see [02-apex-and-triggers/PHASES.md](../02-apex-and-triggers/PHASES.md).

```
01-component-model-and-lifecycle.md
02-templates-directives-and-rendering.md           ⚠️
03-composition-slots-and-dynamic-components.md
04-events-and-component-communication.md
05-decorators-and-the-reactivity-model.md
```

**⚠️** — **02**: conditionals are **`lwc:if` / `lwc:elseif` / `lwc:else`**. `if:true` / `if:false` are the old form and appear in nearly every tutorial. Lead with the correction.

**Notes on scope**
- **03** — include `lwc:ref`, `lwc:spread` and `lwc:component` (dynamic components). These post-date most published material.
- **04** — **no pubsub library.** That pattern was an Aura-era workaround; use CustomEvent up, `@api` down, and LMS across the DOM (topic 12).
- **05** — `@track` is only needed for deep mutation of objects/arrays now. Plenty of tutorials still put it on every field.

**Seed harvest** — `Events - LWC`, `dispatchEvent (CustomEvent)`, `addEventListener - LWC` map to **04**; `Facet (== Slot in LWC)` to **03**; `Wire Methods` to **05**. All 2020–2021, thin. Structure only.

---

## Phase 06 — LWC data, security & navigation · 9 files ⬜

```
06-lightning-data-service-and-ui-api-wires.md
07-graphql-wire-adapter.md                         🆕
08-apex-in-lwc-wire-vs-imperative.md
09-lightning-web-security.md                       🆕⚠️
10-navigation-and-page-references.md
11-lwc-in-flow-screens-and-quick-actions.md
12-lightning-message-service.md
13-shadow-dom-styling-and-scoped-css.md            ⚠️
14-slds-2-and-styling-hooks.md                     🆕⚠️
```

**⚠️ corrections to lead with**
- **09** — **Locker Service was replaced by Lightning Web Security.** Different sandboxing model, different distortions. Any "Locker blocks X" advice needs re-testing under LWS.
- **13** — native shadow DOM vs the synthetic polyfill changes what CSS can reach. Cover `::part` and `:host`.
- **14** — **SLDS 2 / Cosmos.** Overriding SLDS classes was always fragile and is now actively wrong; **styling hooks** are the supported surface.

**🆕 — research before writing**
- **07** GraphQL wire adapter: current pagination/filter/aggregate support, and the honest answer on when it beats an Apex method.
- **09** LWS: the distortion list and the migration-check tooling.
- **14** SLDS 2: what's GA vs still rolling out, and the hook naming scheme.

**Dependency** — **08** must reflect [02-apex · 10 user mode](../02-apex-and-triggers/INDEX.md): a `cacheable=true` method enforces the running user's FLS by default at 67.0. Don't restate the Apex note; link it.

**Seed harvest** — **08**: `Cache issue : refreshApex of wire method & multiple calling of imperative method` is a genuine gotcha worth a callout.

---

## Phase 07 — LWC quality, modern tooling & reach · 8 files ⬜

```
15-lwc-testing-with-jest.md
16-lwc-performance-and-debugging.md
17-accessibility-and-internationalization.md
18-error-handling-and-user-feedback.md
19-custom-lightning-types-for-agent-output.md      🆕
20-offline-lwc-and-mobile-constraints.md           🆕
21-local-dev-and-lightning-dev-server.md           🆕
22-lwc-open-source-and-off-platform-reuse.md
```

**🆕 — research before writing**
- **19** Custom Lightning Types — how typed agent action results render on desktop vs mobile. Cross-link [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md); don't duplicate the agent side.
- **20** Offline LWC — offline GraphQL, draft records, and the real constraint list.
- **21** `sf lightning dev app|site` — the hot-reload workflow. Overlaps [09-devops · 22](../09-devops-sfdx-and-release-management/INDEX.md); this note owns the component-authoring angle, that one owns the tooling install.

**Seed harvest** — `Local Dev` (2024) maps to **21** and may be the most current LWC note in the corpus. Read it before writing.
