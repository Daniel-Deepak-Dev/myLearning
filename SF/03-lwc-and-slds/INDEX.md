# 03 · LWC & SLDS

LWC as the **only** UI framework in this vault. **22 topics** · phases [05](PHASES.md) — **complete ✅**, [06](PHASES.md), [07](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⛔ **Aura and Visualforce are out of scope by design.** They appear only where a note must explain a migration path or a coexistence rule — never as a recommended approach.

> ⚠️ **Two things most tutorials get wrong now:** **Locker Service was replaced by Lightning Web Security (LWS)**, and template conditionals are **`lwc:if`/`lwc:elseif`/`lwc:else`**, not `if:true`/`if:false`.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | [Component model & lifecycle](01-component-model-and-lifecycle.md) | bundle anatomy, hook order, child `renderedCallback` fires **first** | 05 |
| 02 | [Templates, directives & rendering](02-templates-directives-and-rendering.md) ⚠️ | `lwc:if/elseif/else` (Spring '23) — `if:true` evaluates the getter **twice** | 05 |
| 03 | [Composition, slots & dynamic components](03-composition-slots-and-dynamic-components.md) | `@api`, slots, `lwc:ref`, `lwc:spread`, `lwc:component` (Winter '24) | 05 |
| 04 | [Events & component communication](04-events-and-component-communication.md) | CustomEvent, `bubbles`/`composed`, retargeting, **no pubsub library** | 05 |
| 05 | [Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) | reassign don't mutate; **State Managers GA at 67.0** | 05 |
| 06 | Lightning Data Service & UI API wires | getRecord, RecordForm vs RecordEditForm, cache behaviour | 06 |
| 07 | GraphQL wire adapter 🆕 | pagination, filtering, aggregates, when it beats Apex | 06 |
| 08 | Apex in LWC — wire vs imperative | `cacheable=true` rules, `refreshApex`, notifyRecordUpdate | 06 |
| 09 | Lightning Web Security 🆕⚠️ | LWS replaced Locker; sandboxing, distortions, migration checks | 06 |
| 10 | Navigation & page references | NavigationMixin, page reference types, console tabs | 06 |
| 11 | LWC in Flow screens & quick actions | flow-target attributes, headless screen actions | 06 |
| 12 | Lightning Message Service | message channels, scope, cross-DOM communication | 06 |
| 13 | Shadow DOM, styling & scoped CSS ⚠️ | native vs synthetic shadow, `::part`, `:host` | 06 |
| 14 | SLDS 2 & styling hooks 🆕⚠️ | SLDS 2 / Cosmos theming; hooks instead of class overrides | 06 |
| 15 | LWC testing with Jest | `sf-lwc-jest`, wire adapter stubs, DOM assertions | 07 |
| 16 | LWC performance & debugging | render thrash, lazy loading, Lightning inspector | 07 |
| 17 | Accessibility & internationalization | a11y patterns, `@salesforce/i18n`, label imports | 07 |
| 18 | Error handling & user feedback | reduceErrors pattern, ShowToastEvent, error boundaries | 07 |
| 19 | Custom Lightning Types for agent output 🆕 | typed action results rendering on desktop and mobile | 07 |
| 20 | Offline LWC & mobile constraints 🆕 | offline GraphQL, draft records, mobile-first limits | 07 |
| 21 | Local dev & Lightning Dev Server 🆕 | `sf lightning dev app\|site`, hot reload workflow | 07 |
| 22 | LWC Open Source & off-platform reuse | LWC OSS, sharing components beyond the org | 07 |

## Related

- **05 carries the State Manager story** — `defineState` from `@lwc/state` (`atom` / `computed` / `setAtom`) went **GA at API 67.0** and moves shared state out of components entirely. It is folded into 05's currency section rather than given its own file; **a dedicated topic is a phase-07 candidate.**
- **02's Beta caveat matters.** Complex template expressions need component `apiVersion` 66.0+ and are documented as **not for production** — most 2026 write-ups omit that.
- **08** depends on [02-apex · 10 user mode](../02-apex-and-triggers/INDEX.md) — a `cacheable=true` method now enforces the running user's FLS by default.
- **11** pairs with [04-flow · 04 Screen flows](../04-flow-and-automation/INDEX.md).
- **19** feeds [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md) — how agent action output renders.
- **21** overlaps [09-devops · 22 VS Code & tooling](../09-devops-sfdx-and-release-management/INDEX.md).
