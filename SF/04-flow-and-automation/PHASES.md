# Phases for 04 · Flow & Automation

21 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs after Apex (phases 03–07)** because Flow notes reference governor limits and invocable Apex signatures. Don't reorder.

---

## Phase 08 — Flow fundamentals → Apex interop · 11 files ⬜

```
01-automation-landscape-and-tool-selection.md      ⚠️
02-flow-anatomy-and-builder-basics.md
03-record-triggered-flows.md
04-screen-flows-and-ux-design.md
05-reactive-screen-flows.md                        🆕
06-scheduled-and-autolaunched-flows.md
07-platform-event-and-async-path-flows.md
08-subflows-and-modular-flow-design.md
09-collections-loops-and-the-transform-element.md  🆕
10-fault-paths-and-custom-errors.md
11-flow-and-apex-interop.md
```

**⚠️** — **01**: **Workflow Rules and Process Builder are retired.** The classic three-way decision tree is obsolete; the real decision is *which kind of Flow*, and *Flow vs Apex*. Give an honest Flow-vs-Apex boundary — that's the question people actually have.

**🆕 — research before writing**
- **05** Reactive screen flows — what reactivity is supported across which components today.
- **09** The **Transform element** — it replaces the loop-and-assign pattern for collection mapping. Confirm current capability.

**Notes on scope**
- **03** — before-save vs after-save is the single highest-value distinction in this area. Before-save record-triggered flows are the fastest automation on the platform and now run **ahead of before triggers** in the save order.
- **10** — cover the **custom error element**, not just fault connectors.
- **11** — `@InvocableMethod` contract, generic sObject inputs, and typed UDTs. Cross-link [02-apex · 22–23](../02-apex-and-triggers/INDEX.md) rather than restating.

**Seed harvest** ([../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md)) — `Sub Flow` → **08**. `Apex Invocable method in Flow` → **11**: four correct bullets (`@InvocableVariable` for multiple params, only accepts `List`, input size must equal output size); the rest of that page is an unwatched video and an unchecked to-do list. `Flow Invocable Methods and Variable` (2025) → **11**, likely the most current of the three.

---

## Phase 09 — Flow at scale · 10 files ⬜

```
12-flow-limits-and-bulkification.md                ⚠️
13-flow-testing-and-debugging.md                   (GA Spring '23)
14-flow-orchestrator.md                            (GA Spring '22)
15-approval-orchestration.md                       🆕⚠️
16-migrate-to-flow-and-legacy-retirement.md        🆕⚠️
17-flow-for-external-and-guest-users.md
18-data-cloud-triggered-flows-and-data-actions.md  🆕
19-flows-as-agentforce-actions.md                  🆕
20-flow-deployment-versioning-and-governance.md
21-ai-assisted-flow-authoring.md                   🆕
```

**⚠️ corrections to lead with**
- **12** — Flow is **not** exempt from governor limits. It shares the Apex transaction budget, and DML inside a loop is the classic production failure. Anyone treating Flow as "clicks, so no limits" is wrong.
- **15** — Approval Orchestration is the modern path; classic approval processes are in maintenance. **State the status precisely from a source — do not invent a retirement date.**
- **16** — the Migrate to Flow tool and the retirement timeline; cover the conversion traps, not just the happy path.

**🆕 — research before writing:** **15**, **16**, **18**, **19**, **21**. All post-2024.

**Cross-links, don't duplicate**
- **17** → [05-experience-cloud · 07 Guest user security](../05-experience-cloud-lwr/INDEX.md) (written later, phase 18 — this note owns the run-as context, that one owns site hardening).
- **18** → [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md).
- **19, 21** → [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md). **19** should reuse the description-as-contract framing already written there.
- **15** → [01-admin · 12](../01-admin-and-declarative-platform/INDEX.md), written in phase 02.

**Seed harvest** — `Flow Updates` (2025) → **16** or **21**; check what it actually covers first.
