# Validation Rules & Duplicate Management

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 01

**Scope:** Declarative data-integrity enforcement at save time — validation rules, matching rules and duplicate rules. Their exact save-order positions are owned by [14 · Order of execution](14-order-of-execution-declarative-view.md).

## Core idea

Validation rules and duplicate rules are the platform's two declarative veto points on a save. A validation rule is a formula that returns `TRUE` **when the record is invalid** — the inverted logic is the single most common source of confusion. Duplicate management splits the job in two: a **matching rule** defines what "the same record" means, and a **duplicate rule** decides what to do about a match. Both enforce on every write path, including Data Loader and integrations, which is why they are also the most common reason a bulk load fails halfway through.

## How it works

- **Validation rules fire at save-order step 5**, after before-save flows and before triggers, and before the record reaches the database. Field values set by a before-save flow *are* validated.
- **Error location** is configurable: on a named field (shown inline) or at the top of the page. Field-level placement is invisible to a user whose layout omits that field.
- **Duplicate rules run at step 6**, immediately after validation and still before the insert.
- **Matching rules** are the definition of sameness — exact or fuzzy matching across up to ten fields. Activating one triggers an **asynchronous index build**; the rule does nothing useful until that finishes.
- **Duplicate rule actions** — *Allow* (record saves, optionally with an alert) or *Block* (save is refused). Alerts and reporting are separate toggles from blocking.
- **Bypassing enforcement** has no built-in per-profile switch. The standard pattern is a **custom permission** or a hierarchy custom setting checked in the rule formula — see [09 · Custom Metadata vs Custom Settings](09-custom-metadata-vs-custom-settings.md).

## 2026 currency

Nothing structural has changed in validation rules or duplicate management. What has changed is the alternative: Salesforce now positions **before-save record-triggered Flows** as the default place for cross-field logic that *corrects* data, leaving validation rules for logic that *rejects* it. Flow also gained the ability to throw a custom error, so the two mechanisms overlap more than they used to — see [04-flow](../04-flow-and-automation/INDEX.md).

## Gotchas

- **The formula returns `TRUE` to raise an error.** Writing the condition for "valid" is the classic inversion bug.
- Validation rules fire on Data Loader and API writes. A load of 50,000 rows fails per-row, leaving a partial result unless you planned for it — see [13 · Data import, export & loading tools](13-data-import-export-and-loading-tools.md).
- A rule that does not check `RecordTypeId` fires for every business process on the object, not just the one it was written for.
- Errors attached to a field the user's layout does not show produce an unexplained failure with no visible message.
- `ISNEW()` and `PRIORVALUE()` are unavailable in some contexts; a rule relying on them behaves differently under Flow-driven updates than under manual edits.
- Matching rule activation is **async**. Testing immediately after activating gives a false negative.
- Duplicate rules do not run on every path — lead conversion and some bulk operations bypass them, so they are not a data-integrity guarantee.
- Validation rules do not fire during roll-up recalculation or cascade delete, so a "guaranteed" invariant can still be violated indirectly.

## Recall

Q: Does a validation rule formula return TRUE for valid or invalid data?
A: TRUE means **invalid** — the rule fires and blocks the save.

Q: What is the division of labour between a matching rule and a duplicate rule?
A: The matching rule defines what counts as the same record; the duplicate rule decides what happens on a match — allow, alert, or block.

Q: Where do validation rules and duplicate rules sit relative to each other in the save order?
A: Validation rules at step 5, duplicate rules at step 6 — both before the record is written to the database.

Q: Why might a validation rule error be invisible to a user?
A: The error is attached to a field that the user's page layout does not display.

Q: How do you let a specific group of users bypass a validation rule?
A: There is no built-in switch — check a custom permission or a hierarchy custom setting inside the rule formula.

## Related

- [14 · Order of execution](14-order-of-execution-declarative-view.md) — the authoritative save-order positions
- [04 · Record types & picklist architecture](04-record-types-and-picklist-architecture.md) — why rules must be record-type aware
- [04-flow · INDEX](../04-flow-and-automation/INDEX.md) — before-save flows and Flow custom errors as the modern alternative
