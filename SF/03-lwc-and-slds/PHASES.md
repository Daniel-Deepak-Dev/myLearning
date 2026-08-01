# Phases for 03 · LWC & SLDS

22 topics across 3 runs — **phase 05 complete**, 5 of 22 written. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

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
- **09** — **Locker Service was replaced by Lightning Web Security.** Different sandboxing model, different distortions. Any "Locker blocks X" advice needs re-testing under LWS. **Found in phase 05:** at 67.0 LWS also **blocks the `data:` URI scheme** — `blob:` URLs are the replacement. Anything passing a `data:` URL through an event payload or a download link breaks.
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

**Seed harvest** — `Local Dev` (2024) maps to **21** and may be the most current LWC note in the corpus. Read it before writing — but note it is **named for a thing that has been renamed**: phase 05 found that **LWC Component Preview went GA at 67.0** and the VS Code extension is now **Live Preview**, not Local Dev. Treat the page's terminology as dated even where its workflow is not.
