# Phases for 03 · LWC & SLDS

24 topics across 3 runs — **all complete ✅**, 24 of 24 written. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

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

## Phase 07 — LWC quality, modern tooling & reach · 10 files ✅

```
15-lwc-testing-with-jest.md                        ⚠️
16-lwc-performance-and-debugging.md
17-accessibility-and-internationalization.md       ⚠️
18-error-handling-and-user-feedback.md             ⚠️
19-custom-lightning-types-for-agent-output.md      🆕
20-offline-lwc-and-mobile-constraints.md           🆕
21-local-dev-and-lightning-dev-server.md           🆕⚠️
22-lwc-open-source-and-off-platform-reuse.md
23-static-resources-and-third-party-javascript.md  ← added at plan time
24-lwc-state-managers.md                           🆕 ← added at plan time
```

**Two files added before the run, appended rather than inserted** so no existing link breaks.
- **23** closes a hole in the whole area: nothing in 01–22 owned `platformResourceLoader`, CSP Trusted Sites or `lwc:dom="manual"`, and 09 had already recorded that blocked CDN scripts are CSP rather than LWS without anywhere to point at for the right pattern.
- **24** is the topic the phase-05 retro nominated — State Managers, GA at 67.0. A paragraph in 05's currency section undersold the first new answer to cross-component state since LMS.

**A 25 · *LWC host surfaces & the `js-meta.xml` targets contract* was considered and declined** — 11 already owns `.js-meta.xml` as "the contract". The one genuinely new surface, LWC in Lightning dashboards, went into 22.

**🆕 — research before writing**
- **19** Custom Lightning Types — how typed agent action results render on desktop vs mobile. Cross-link [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md); don't duplicate the agent side.
- **20** Offline LWC — offline GraphQL, draft records, and the real constraint list.
- **21** `sf lightning dev app|site` — the hot-reload workflow. Overlaps [09-devops · 24](../09-devops-sfdx-and-release-management/INDEX.md); this note owns the component-authoring angle, that one owns the tooling install.

**Seed harvest** — `Local Dev` (2024) maps to **21** and may be the most current LWC note in the corpus. Read it before writing — but note it is **named for a thing that has been renamed**: phase 05 found that **LWC Component Preview went GA at 67.0** and the VS Code extension is now **Live Preview**, not Local Dev. Treat the page's terminology as dated even where its workflow is not.

### Retro

**⚠️ — the plan added three flags to a file list that shipped with none, and the run added a fourth**

The phase-07 list as written in the master plan carried **no ⚠️ at all**, which was wrong for half of it. Flags added at plan time to **15**, **17** and **21**; **18** earned one during the run.

- **15** — held, and it is two stale answers rather than one. `registerApexTestWireAdapter` / `registerLdsTestWireAdapter` / `registerTestWireAdapter` are the **Spring '21-and-earlier** pattern; the docs' exact words are that the code *"still works, but it isn't recommended."* Not deprecated, not broken — superseded, and the distinction matters for the same credibility reason `if:true` did in phase 05. Second half: `sfdx force:lightning:lwc:test:run` went with `sfdx` v1.
- **17** — held, and the doc-backed framing is stronger than the one the plan proposed. The plan led with "LWC v4 dropped the global ARIA property polyfill", which is an **OSS** changelog fact and not something the platform docs state. The platform docs *do* say, plainly: *"In native shadow DOM, you can't link IDs and ARIA attributes between elements in separate templates."* That is the correction the note leads with, because it also explains the delayed fuse — synthetic shadow flattens IDs, so `aria-labelledby` written in 2021 works until the component goes native.
- **21** — held, and the topic's own filename is the artefact. Three names, three products: `sfdx force:lightning:lwc:start` (retired, off-org, mock-backed) → *Lightning Preview* / *Local Dev* (2024, org-backed) → **Live Preview** (the extension) with **LWC Component Preview** GA at 67.0.
- **18 — a fourth ⚠️ nobody flagged.** *"Fire `ShowToastEvent`"* is no longer portable: it is **not supported in LWR Experience Cloud sites or standalone apps**, where it fails silently because there is no container to catch the event. **`lightning/toast` + `lightning/toastContainer` (Winter '24)** is the portable answer. This is the same shape as `NavigationMixin`'s absence off-platform — a component is only as reusable as its container-dependent imports.

**🆕 the plan did not flag**

- **The plan was wrong about the Custom Lightning Types binding.** It said the renderer LWC uses a **`sourceType`**; the docs use **`targetType`**, with `lightning__AgentforceOutput` for a renderer and `lightning__AgentforceInput` for an editor. The `sourceType` claim came from a search snippet and did not survive the primary source. **Third phase running that a 🆕 item in the plan needed correcting** — 05 hit it, 06 hit it twice, and it should now be treated as the expected outcome rather than a surprise.
- **Custom Lightning Types are registered per channel**, and this is the part every write-up omits: `lightningDesktopGenAi`, `enhancedWebChat`, `lightningMobileGenAi`, `experienceBuilder` are separate folders with **no inheritance**. A renderer that works on the desktop agent is simply absent in Enhanced Chat v2.
- **`lightning/accApi` (Summer '26)** runs the other direction — an ordinary LWC can drive the Agentforce side panel with `open(botId)` / `close()` / `execute(utterance, botId)`. Folded into **19**; the agent side stays in `AI_Data/`.
- **State Managers share through *context*, not through the page.** `fromContext` resolves to the nearest ancestor that instantiated the manager, so two sibling subtrees get two independent states and anything outside the provider's subtree gets nothing. That is the line between **24** and **12**, and it is why LMS is not obsolete.
- **`@lwc/state` is at `0.x` on npm while the platform feature is GA.** Platform GA and package maturity are not the same claim.
- **`lwc` OSS is at 9.x** and moves on its own cadence — an OSS changelog entry is not evidence a deployed component can use it. Checked against the registry rather than recalled.
- **Offline is harsher than "some things are slower".** **Apex does not run offline at all** — neither `@wire`d nor imperative — and triggers, validation rules and flows fire at *sync*, so an offline save can be rejected hours later. Also: Mobile Offline needs **`lightning/uiGraphQLApi`**, not `lightning/graphql`, and that module supports neither optional fields nor dynamic query construction.
- **Summer '26 LWC items absent from the plan, each given a home instead of a file** — LWC in Lightning dashboards → **22**; dynamic list components / virtualization, Developer Preview → **16**; lazy-loading wire adapters → **16**.

**Other corrections made while writing**

- **`force:refreshView` does not port**, and the area was teaching two of the three refresh APIs without ever saying which to pick. **16** now owns the decision: `refreshApex` (same question, new data) vs `notifyRecordUpdateAvailable` (LDS was bypassed) vs `RefreshEvent` from `lightning/refresh` (refresh a whole view, including components you don't own — and descendants must register their own callback, a parent is **not** responsible for them).
- **`aria-*` on a custom element lands on the host**, not on anything in its template — the most common wrong assumption in hand-rolled LWC accessibility.
- **`reduceErrors` is not a platform module.** There is no official import; every codebase copies its own and they drift.
- **`lwc:dom="manual"` costs more than it looks.** Its content is outside reactivity, outside accessibility management **and** outside template sanitization — so it is an XSS surface, not just an escape hatch.

**Seed harvest** · *the Notion connector held this time — all four phase-06 casualties were re-read*

- **21** — `Local Dev` (2024). → *harvested. All four steps still describe the workflow, with two corrections: the `@salesforce/plugin-lightning-dev` install is usually unnecessary now (it ships with the CLI), and `sf lightning dev app` was the only command then — for authoring one component the answer is now **`sf lightning dev component`**, which is what GA'd at 67.0. Confirmed as the most current page in the corpus.*
- **17** — `@salesforce modules or Importing SF values`. → *harvested. The whole import surface in one component — `@salesforce/i18n/lang|locale|currency|timeZone`, `label/c.*`, `resourceUrl`, `user/Id`, `user/isGuest`, `client/formFactor` — fed to `Intl.*`. Corrected inline: its `js-meta.xml` says `<apiVersion>47.0</apiVersion>`, and `lightning-formatted-*` now beats hand-rolled `Intl`.*
- **15** — `LWC : Query DOM Elements` (2023). → *harvested, re-aimed. The page is about `lwc:ref`, which is **03**'s territory, but its findings are testing rules: refs are not emitted into the DOM, so a Jest test can never select by one — anything a test must find needs a `data-*` attribute. Duplicate ref names resolving to the last one, and the absence of a `querySelectorAll` equivalent, both still hold.*
- **`@Salesforce Modules` (2020) was re-read and is structure-only** — a bookmark and an inline sub-topics database, no prose. The 2022 sibling above is the one with content. **`LWC metadata api file` (2019)** maps to **11**, out of phase; read, not used.
- **16, 18, 19, 20, 22, 23, 24 carry no `From my notes.` callout** — confirmed zero seed coverage for performance, error handling, Agentforce rendering, offline, OSS, static resources and state management. Consistent with the inventory: the corpus is 2019–2021 component mechanics, and none of these existed as concerns in it.

**Debt cleared** — the forward-link sweep the phase-06 retro asked for is **done**. 16 links across 8 files (01, 02, 03, 04, 05, 08, 10, 14) that pointed at `INDEX.md` as a placeholder now point at real files; anchor text was already correct, only hrefs changed. Every relative link in the area resolves.

**Area closed.** 24 of 24 topics written. Nothing outstanding except the standing invitation to re-read `LWC - Quick Action` against **11** if that note is ever revised.
