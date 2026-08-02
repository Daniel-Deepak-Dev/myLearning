# Phases for 03 · LWC & SLDS

22 topics across 3 runs — **phases 05 and 06 complete**, 14 of 22 written. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> Currency anchor for this area: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md); for **09** specifically, [trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

> **Area constraint.** Aura and Visualforce are **out of scope**. They may be named only in a migration or coexistence sentence — never as an approach. The old notes contain several Aura-flavoured pages ([../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) marks them ⛔); skip those outright.

---

## Phase 05 — LWC entry · 5 files ✅

Shares a run with the Apex closeout — see [02-apex-and-triggers/PHASES.md](../02-apex-and-triggers/PHASES.md).

```
01-component-model-and-lifecycle.md
02-templates-directives-and-rendering.md           ⚠️
03-composition-slots-and-dynamic-components.md
04-events-and-component-communication.md
05-decorators-and-the-reactivity-model.md
```

**⚠️** — **02**: held, with two corrections to the framing. The directives arrived in **Spring '23**, and `if:true`/`if:false` are **not deprecated** — no removal date has been announced, only an intent. Overstating that is a credibility loss. The substantive difference is not syntax: `if:true` and `if:false` are two independent bindings, so the bound getter **evaluates twice** per instance where the `lwc:if` chain evaluates once. That is the sentence the note leads with, because it is the one that changes behaviour rather than style.

**Notes on scope** — all three held.
- **03** — `lwc:ref` (Spring '23), `lwc:spread` (Summer '23), `lwc:component`/`lwc:is` (**Winter '24**). Release stamps added, because the point of the topic is that these post-date the tutorials. Dynamic components in particular are still cited as a reason to keep Aura; since Winter '24 they are not.
- **04** — no pubsub, as planned.
- **05** — `@track` narrowed to deep mutation, as planned. See the 🆕 the plan missed, below.

**🆕 the plan did not flag — LWC State Managers, GA at API 67.0.** `defineState` from `@lwc/state`, with `atom()` / `computed()` / `setAtom()` supplied to a setup function, plus built-in managers such as `lightning/stateManagerRecord`. Computeds recompute lazily and multiple `setAtom` calls in one tick batch into a single notification. This is the first genuinely new answer to cross-component state since LMS and it makes the case for `@track` narrower again — so it went into **05**'s `2026 currency` rather than getting an eleventh file, per standing rule 1. **A dedicated topic is a phase-07 candidate** if the area needs one; it would renumber 06–22, which is why it was not done here.

**Other corrections made while writing**
- **Complex Template Expressions are Beta and documented as *not for production*** — gated on component `apiVersion` **66.0+**. Widely written up in 2026 as though shipped; the docs say "Do not use complex template expressions in production." **02** carries the caveat, not the enthusiasm.
- **Child `renderedCallback` fires *before* the parent's.** The tree constructs top-down and completes bottom-up, which inverts the order most people assume and is the reason parent-level DOM measurement misses child content.
- **LWC Component Preview is GA at 67.0** with faster, more memory-efficient hot module reloading; the VS Code extension was renamed *Local Dev* → **Live Preview**. **This affects the phase-07 seed note below** — the 2024 `Local Dev` page is now named for a thing that has been renamed.
- **At 67.0 LWS blocks the `data:` URI scheme** — use `blob:`. Belongs to **09**, flagged here so phase 06 does not miss it.
- **`<details>` supports `name` grouping at 67.0**, making a single-open accordion zero-JavaScript. In **02**.
- **`errorCallback` is narrower than "error boundary" suggests** — it catches errors in *descendants' lifecycle hooks* only, not in your own hooks, event handlers, or promises. Flagged in **01** so **18** does not have to re-teach it.

**Seed harvest** · *one of three harvested; two were structure-only as predicted*
- **04** — `Events - LWC`, `dispatchEvent (CustomEvent)`, `addEventListener - LWC` (2020, thin). → *structure only, but one line survived as the callout: **name the event for what happened, not for what you want done about it.** `orderselected` leaves the parent free; `refreshtable` has already decided and breaks on reuse.*
- **03** — `Facet (== Slot in LWC)`. → *used as the callout with the correction inline: the analogy holds for the mental model and **breaks on scope** — an Aura facet evaluates in the component's context, slotted LWC content stays in the **parent's**, which is why parent CSS reaches it.*
- **05** — `Wire Methods` (2020). → *nothing usable; **05 carries no `From my notes.` callout.***

---

## Phase 06 — LWC data, security & navigation · 9 files ✅

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
- **09** — **Locker Service was replaced by Lightning Web Security.** Different sandboxing model, different distortions. Any "Locker blocks X" advice needs re-testing under LWS. **Found in phase 05:** at 67.0 LWS also **blocks the `data:` URI scheme** — `blob:` URLs are the replacement. Anything passing a `data:` URL through an event payload or a download link breaks.
- **13** — native shadow DOM vs the synthetic polyfill changes what CSS can reach. Cover `::part` and `:host`.
- **14** — **SLDS 2 / Cosmos.** Overriding SLDS classes was always fragile and is now actively wrong; **styling hooks** are the supported surface.

**🆕 — research before writing**
- **07** GraphQL wire adapter: current pagination/filter/aggregate support, and the honest answer on when it beats an Apex method.
- **09** LWS: the distortion list and the migration-check tooling.
- **14** SLDS 2: what's GA vs still rolling out, and the hook naming scheme.

**Dependency** — **08** must reflect [02-apex · 10 user mode](../02-apex-and-triggers/INDEX.md): a `cacheable=true` method enforces the running user's FLS by default at 67.0. Don't restate the Apex note; link it.

**Seed harvest** — **08**: `Cache issue : refreshApex of wire method & multiple calling of imperative method` is a genuine gotcha worth a callout.

### Retro

**⚠️ corrections — two of three needed correcting themselves**

- **09** — held, but the plan overstated it. **Lightning Locker is not retired.** LWS is the default only for orgs created **Winter '23 and later**, has been GA for all orgs since **Summer '23**, and is a Session Settings checkbox — *Use Lightning Web Security for Lightning web components and Aura components* — that an org can still switch off. "Replaced as the default, not retired" is the accurate sentence, and it is the same credibility problem phase 05 hit with `if:true`. The `data:`/`blob:` find carried over from phase 05 as planned.
- **13** — held. Added the release-accurate framing the plan lacked: **Mixed Shadow Mode is still Beta at 67.0**, synthetic remains the Lightning Experience default, and `shadowSupportMode = 'any'` is **deprecated in favour of `'native'`**. Also recorded that a synthetic parent may contain native children but not the reverse, which is what makes migration leaves-first.
- **14** — **the plan's framing was half wrong and it changed the note.** "Styling hooks are the supported surface" is only true of **global** hooks. **`--slds-c-*` component hooks are not supported in SLDS 2**, and Salesforce's own guidance is that a component depending on them should stay on SLDS 1 for now. `--slds-g-*` is the portable surface.

**🆕 the plan did not flag**

- **SLDS 2 went GA in Winter '26, not Summer '26** (introduced Spring '25). Summer '26's contribution is the **expanded Themes and Branding interface** — typography, shadows, sizing, spacing, illustration colour, with inline preview. On by default for new orgs in the supported editions, opt-in for existing ones.
- **Aura-era design tokens are inert under SLDS 2** — not merely deprecated. **SLDS Linter** and **SLDS Validator** convert them to global hooks; the DX MCP server exposes the same guidance.
- **Dark mode is exclusive to SLDS 2**, enabled per theme with *Let users enable Dark Mode*. An SLDS 1 org must migrate first.
- **GraphQL mutation chaining (Summer '26) landed in the GraphQL *API*, not the wire adapter.** The wire adapter still has **no mutations at all**, so LDS remains the only client-side write path. Features reach the API several releases before the adapter — a "GraphQL API" release note is not evidence the adapter has it.
- **LWS is namespace isolation, not a firewall.** The genuinely blocked set is small (`document.write()`, `Worker()`, `ServiceWorkerContainer`, `window.find()`, XSLT); most symptoms are namespacing or sanitization. Three things routinely blamed on LWS are **not** LWS: external CDN scripts (CSP), `$A`/`Sfdc`/`sforce` (the LWC framework), and `fetch('/aura')` (an internal endpoint).

**Other corrections made while writing**

- **`encodeDefaultFieldValues` is honoured only on `actionName: 'new'`** — silently ignored on `edit`, which is the usual wrong guess. In **10**.
- **`role="outputOnly"` is not enough to return a value to Flow.** Assigning to the `@api` property does nothing; it takes a `FlowAttributeChangeEvent` whose attribute name is an **unchecked string**. In **11**.
- **LMS default scope excludes inactive console tabs and the utility bar** — the "works on my page, not in the console" bug. `APPLICATION_SCOPE` is the fix. In **12**.
- **`fields` vs `optionalFields` differ on no-access**: a field in `fields` the user cannot see errors the *whole* wire. In **06**.

**Seed harvest** · *two harvested, and the Notion connector dropped mid-run*

- **08** — `Cache issue : refreshApex of wire method & multiple calling of imperative method` (2022). → *harvested and it holds up verbatim: **"Refreshing wire method will only call the method using old parameter value, not the updated parameter value."** Stated as the rule it implies — `refreshApex` re-provisions with the config the wire last had, so it is for "the data behind the same question changed", never for "the question changed".*
- **10** — `Navigate to a Record's Create Page with Default Field Values` (2023) plus its sibling `Navigation` page. → *harvested with the correction: the sibling's example is Aura (`<lightning:pageReferenceUtils>`) and **does not port** — in LWC it is a plain import from the `lightning/pageReferenceUtils` module. The part worth keeping is the `GenerateUrl`-into-an-anchor shape, because `Navigate` on a `<div onclick>` produces a destination nobody can middle-click or reach by keyboard.*
- **07, 09, 12, 14 carry no `From my notes.` callout** — confirmed zero seed coverage. No entry anywhere in the inventory for LDS, GraphQL, Locker/LWS, SLDS, or LMS.
- **06, 11, 13 carry none either, for a different reason.** `@Salesforce Modules`, `LWC - Quick Action`, `LWC metadata api file` and `LWC : Query DOM Elements` were **not re-readable** — the Notion connector disconnected part-way through the run. Titles are known, bodies are not, and inventing their content was not an option. **Re-try these three in a later pass.**

**Known debt** — phase-05 files 01, 02, 04 and 05 link forward to topics 06–14 as `[NN](INDEX.md)`, which was correct when those files did not exist. They now do. Left alone under standing rule 1 (no sprawl); worth a one-pass sweep after phase 07 writes 15–22, when the same debt will exist for the rest of the area.

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

**Seed harvest** — `Local Dev` (2024) maps to **21** and may be the most current LWC note in the corpus. Read it before writing — but note it is **named for a thing that has been renamed**: phase 05 found that **LWC Component Preview went GA at 67.0** and the VS Code extension is now **Live Preview**, not Local Dev. Treat the page's terminology as dated even where its workflow is not.
