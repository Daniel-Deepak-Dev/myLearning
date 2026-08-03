# Flow Anatomy & Builder Basics

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** The vocabulary every other note in this area assumes — elements, resources, the canvas, versioning. Type-specific behaviour lives in [03](03-record-triggered-flows.md)–[07](07-platform-event-and-async-path-flows.md).

## Core idea

A flow is two things that beginners conflate: **elements**, which are steps on the canvas and consume limits, and **resources**, which are named values that do not. Almost every performance conversation in this area reduces to that split — a formula resource is free, a Get Records element is a SOQL query. The second structural idea is **versioning**: a flow is a container of numbered versions of which exactly one may be active, and an active version is immutable. You do not edit a running flow; you open it, which silently creates a new draft version, and activating that draft deactivates its predecessor. Understanding those two facts prevents most of the "why did my change not take effect?" and "why did this blow the SOQL limit?" confusion.

## How it works

| Category | Elements | Costs a limit? |
|---|---|---|
| **Interaction** | Screen, Action, Subflow | Action and Subflow can |
| **Logic** | Assignment, Decision, Loop, Collection Sort/Filter, Transform | no — but a Loop *around* a Data element does |
| **Data** | Get / Create / Update / Delete Records | **yes** — SOQL or DML every time |

- **Resources are values, not steps:** variable, collection variable, record variable, formula, constant, text template, choice, choice set, stage. They are evaluated where used and cost nothing.
- **A variable's `Available for input` / `Available for output` flags are its public contract.** Nothing outside the flow can see a variable that has neither. → [08](08-subflows-and-modular-flow-design.md)
- **Auto-layout is the default canvas** and enforces a single connected path; free-form is still available and is what older screenshots show. You can switch a flow between them.
- **`$Record`, `$User`, `$Setup`, `$Permission`, `$Organization`, `$Api`, `$Flow`** are global variables. `$Flow.CurrentDateTime`, `$Flow.InterviewGuid` and `$Flow.FaultMessage` are the ones you reach for.
- **One active version.** Deploying an inactive version to production changes nothing until something activates it. → [24 · Deployment & versioning](24-flow-deployment-versioning-and-governance.md)

## 2026 currency

Summer '26 is a builder-usability release rather than a capability one, and two items change how you write logic. **Decision elements gained roughly twenty date operators** — `Is Today`, `Is Tomorrow`, `Is Yesterday`, `Is This Month`, `Is Anniversary of Today`, `Last N Days`, `Next N Months` — which retire a pile of formula resources that existed only to compare dates. The catch worth remembering: **they do not support DateTime fields**, only Date. Alongside that, the **validation panel was redesigned** into cards and now stays closed by default, **fault paths, Decisions and Loops all collapse on the canvas**, and static resource images can be browsed and uploaded without leaving the builder. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

> **From my notes.** The old `Flow Builder` page is a sixteen-item agenda with **one box ticked**, which makes it an accurate record of what was hard in 2023 rather than a note. Two lines have aged into the answer: *"use flow to make a callout"* sat unchecked because the feature was still in beta — it is GA now → [12](12-http-callout-and-external-services-in-flow.md) — and *"`$Record` vs `$Record__Prior`"* was written as a question with no answer under it → [03](03-record-triggered-flows.md).

## Gotchas

- **Opening an active flow creates a new draft version.** Your edits are not live until you activate, and activating deactivates the version that was running.
- **You cannot edit an active version in place**, which is also why "just tweak it in production" is not available.
- **A Get Records inside a Loop is one SOQL query per iteration.** This is the single most common way a flow dies. → [09](09-collections-loops-and-the-transform-element.md)
- **A variable with neither input nor output flag is invisible outside the flow** — the usual cause of a subflow that "returns nothing".
- **Formula resources are validated at save, not at design time**, so a bad cross-object reference surfaces late.
- **The new date operators silently exclude DateTime fields.** A `CreatedDate` comparison still needs a formula.
- **Flow has no Map data type.** Anything shaped like a dictionary has to be a collection plus a loop, or Apex. → [11](11-flow-and-apex-interop.md)

## Recall

Q: What is the difference between an element and a resource?
A: An element is a step on the canvas and can consume governor limits; a resource is a named value that is evaluated where used and costs nothing.

Q: How many versions of a flow can be active at once?
A: Exactly one. Opening the active version creates a new draft, and activating that draft deactivates the previous one.

Q: Which three element categories exist, and which always costs a limit?
A: Interaction, Logic and Data. Data elements — Get, Create, Update, Delete — always cost a SOQL query or a DML statement.

Q: What makes a flow variable visible to a caller?
A: The `Available for input` and `Available for output` flags. Without them the variable is private to the flow.

Q: What is the catch with Summer '26's new Decision date operators?
A: They work on Date fields only — DateTime is not supported, so datetime comparisons still need a formula.

## Related

- [03 · Record-triggered flows](03-record-triggered-flows.md) — the first flow type to build with this vocabulary
- [09 · Collections, loops & the Transform element](09-collections-loops-and-the-transform-element.md) — why the element/resource split decides performance
- [08 · Subflows & modular flow design](08-subflows-and-modular-flow-design.md) — where the input/output flags become a real contract
