# Triggers & the Handler Framework

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 03

**Scope:** The trigger as a dispatch point, its context variables, and the handler class that holds the actual logic. Where it fires in the save order and how to stop it re-entering is [07](07-order-of-execution-and-recursion.md).

## Core idea

A trigger is not a place to write code. It is a **binding** between a save event and the code that handles it, and every durable convention in Apex follows from treating it that way: one trigger per object, no logic inside it, all work delegated to a handler class. The reasons are concrete. Salesforce does not guarantee the execution order of multiple triggers on the same object, so two triggers means non-deterministic behaviour. A trigger cannot be unit-tested in isolation, cannot be called from a Queueable or a test factory, and at 67.0 cannot declare a sharing or access mode at all. A handler class can do all of those. The trigger's whole job is to answer "which context is this?" and hand off.

## How it works

- **The dispatch is the trigger.** `Trigger.operationType` returns a `System.TriggerOperation` enum, which makes the whole body a `switch`:

```apex
trigger AccountTrigger on Account (before insert, before update, after insert, after update) {
    switch on Trigger.operationType {
        when BEFORE_INSERT { AccountTriggerHandler.beforeInsert(Trigger.new); }
        when BEFORE_UPDATE { AccountTriggerHandler.beforeUpdate(Trigger.new, Trigger.oldMap); }
        when AFTER_INSERT  { AccountTriggerHandler.afterInsert(Trigger.newMap); }
        when AFTER_UPDATE  { AccountTriggerHandler.afterUpdate(Trigger.newMap, Trigger.oldMap); }
    }
}
```

- **Which context variables exist depends on the event**, and getting this wrong is a null dereference rather than a compile error:

| Context | `Trigger.new` | `Trigger.old` | `newMap` | `oldMap` |
|---|---|---|---|---|
| before insert | editable | — | — | — |
| after insert | read-only | — | ✅ | — |
| before update | editable | ✅ | ✅ | ✅ |
| after update | read-only | ✅ | ✅ | ✅ |
| before / after delete | — | ✅ | — | ✅ |
| after undelete | read-only | — | ✅ | — |

- **Before for the record itself, after for everything else.** Setting a field on the saving record belongs in `before` — assign to `Trigger.new` and the platform persists it with no extra DML. Anything needing the record's Id, or touching a *different* object, belongs in `after`.
- **`addError()` is the trigger's veto.** Called on a record it blocks that row with a field-level or record-level message; under `allOrNone = false` the rest of the batch still commits. That is what makes "prevent delete when children exist" a query in `before delete` plus an `addError()` on the offenders.

> **From my notes.** From the old trigger-factory page, three "Manthras" worth keeping: **all SOQL happens in the bulk phase, never inside the record loop; all DML happens once, at the end; the trigger itself holds no logic.** Every one of those still holds. The `ITrigger` / `TriggerFactory` scaffolding they arrived wrapped in does not — it is ~2013 code, predates `Trigger.operationType`, and hand-rolls the dispatch a `switch` now does in six lines. Keep the discipline, drop the framework.

## 2026 currency

**Triggers always run in system mode at 67.0 and can no longer declare sharing or access modes at all.** The ambiguity is gone — no more wondering what a keyword-less trigger inherits — but the consequence is sharper than it looks: a trigger is now definitively the wrong place for security-sensitive logic, because it has no way to express an access decision. Push that work into the handler class, which *does* default to `with sharing` at 67.0 and can opt into `AccessLevel.SYSTEM_MODE` per operation where it genuinely needs to. This is the position taken in [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md); notes here must not contradict it.

## Gotchas

- **Assigning to `Trigger.new` in an `after` context throws.** The records are read-only once they are in the database.
- **`Trigger.newMap` is null in `before insert`** — the Ids do not exist yet. `Trigger.new` is null in delete contexts and `Trigger.old` is null in insert.
- **`Trigger.old` and both maps are always read-only**, in every context, including `before update`.
- **The trigger fires once per 200 records, not once per save.** A 10,000-row load invokes it 50 times, and each invocation is a fresh chunk. → [07](07-order-of-execution-and-recursion.md)
- **Two triggers on one object have undefined relative order** — the only reason the one-trigger rule is a rule rather than a preference.
- **`addError()` in a `before` trigger prevents the save; in an `after` trigger it rolls back the already-written row.** Both work; the second is more expensive.
- **A trigger cannot be given a sharing keyword at 67.0** — it is a compile error, not a silently ignored declaration.

## Recall

Q: Why one trigger per object?
A: Salesforce does not guarantee the execution order of multiple triggers on the same object, so more than one makes behaviour non-deterministic.

Q: What execution mode do triggers run in at 67.0?
A: Always system mode, with no ability to declare sharing or access modes — so security-sensitive logic belongs in the handler class.

Q: Where do you set a field on the record being saved, and why?
A: In a `before` trigger, by assigning to `Trigger.new`. The platform persists it with no additional DML and no re-entry into the save order.

Q: Which context variables are unavailable in `before insert`?
A: `Trigger.newMap`, `Trigger.old` and `Trigger.oldMap` — there are no Ids yet and no prior version of the record.

Q: How many records does one trigger invocation see?
A: At most 200. Larger operations invoke the trigger repeatedly, in chunks.

## Related

- [07 · Order of execution & recursion](07-order-of-execution-and-recursion.md) — when this fires relative to everything else, and how to stop it firing twice
- [08 · Bulkification patterns](08-bulkification-patterns.md) — what the handler must do with a 200-record list
- [27 · Apex Enterprise Patterns & layered design](27-apex-enterprise-patterns-and-layered-design.md) — what replaces the retired `TriggerFactory` scaffolding once one handler class stops being enough
- [04-flow · INDEX](../04-flow-and-automation/INDEX.md) — the before-save flow that is often the cheaper answer to a same-record field update
