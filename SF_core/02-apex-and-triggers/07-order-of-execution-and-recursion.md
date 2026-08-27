# Order of Execution & Recursion

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 03

**Scope:** Where Apex sits in the save order, and how to stop a trigger re-entering itself. The canonical full 20-step order is [01-admin · 14](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md) — **this note conforms to it and does not restate it.**

> **What changed.** Any save-order list beginning "before triggers run first" is wrong. **Before-save record-triggered flows fire at step 3, ahead of every before trigger**, so a flow may already have altered `Trigger.new` by the time your Apex sees it. Workflow Rules and Process Builder, at steps 11 and 13, went **out of support on 31 December 2025 but were not retired** — you cannot build new ones, and in an unmigrated org they still fire between your after-trigger and your after-save flow.

## Core idea

One record save is a fixed twenty-step pipeline, and Apex occupies four of those steps. Knowing which four answers most "why did my trigger see the wrong value?" questions immediately, because the answer is nearly always that the value is produced later in the pipeline than the code reading it. The second half of the topic follows from the first: because a save can *re-enter* the pipeline — a roll-up updating a parent, an after-save flow updating the record again — the same trigger runs more than once in a single transaction. That is normal platform behaviour, not a bug, and the job of a recursion guard is not to prevent it but to make the second pass cheap and idempotent.

## How it works

| Step | What runs | What your Apex can rely on |
|---|---|---|
| 4 | **before triggers** | assign to `Trigger.new` freely; no Id yet on insert |
| 5 | custom validation rules | they validate whatever steps 3 and 4 wrote |
| 7 | record written to the database | Ids now exist; nothing is committed |
| 8 | **after triggers** | Ids available, roll-ups **not** yet recalculated |
| 14 | after-save record-triggered flows | can update the record and re-enter your trigger |
| 16–17 | roll-up summaries recalculate | too late for step 8 to have read them |
| 19 | commit | everything before this can still be discarded |
| 20 | post-commit — email, async jobs | outside the transaction; cannot be rolled back |

- **The window between 7 and 19 is the whole game.** The record is in the database but not committed, so an unhandled exception at step 18 discards the step-7 write entirely.
- **Guard per record, not per invocation.** A `static Boolean hasRun` is the guard most codebases have and it is wrong: the first chunk sets it, and every subsequent record in the transaction is skipped silently. Track the Ids you have processed instead:

```apex
public class OpportunityTriggerHandler {
    private static Set<Id> processed = new Set<Id>();

    public static void afterUpdate(Map<Id, Opportunity> newMap) {
        Map<Id, Opportunity> todo = new Map<Id, Opportunity>(newMap);
        todo.keySet().removeAll(processed);      // skip only what this transaction already did
        if (todo.isEmpty()) { return; }
        processed.addAll(todo.keySet());
        rollUpToAccount(todo.values());
    }
}
```

- **Statics live for the transaction and nothing longer.** Each batch `execute()`, each Queueable and each API call starts with an empty `processed` set — which is correct, because each is a separate transaction with its own budget. → [01](01-apex-language-core-and-governor-limits.md)
- **Recursion has a hard ceiling regardless of your guard**: trigger stack depth is **16**, and exceeding it throws rather than looping forever.

## 2026 currency

All *new* declarative automation now lands at steps 3 and 14, which brackets your Apex on both sides rather than trailing it. The practical effect is that re-entry is *more* likely than under the old model, not less: an after-save flow at step 14 updating the record it was triggered by will run your trigger again, and it is now the ordinary way admins build things. A per-record guard is therefore no longer defensive polish. The debugging nuance: steps 11 and 13 are **not empty** in an org that never migrated — end of support is not retirement — so an unexplained re-entry there is a legacy workflow rule, not a ghost. → [04-flow · 01](../04-flow-and-automation/01-automation-landscape-and-tool-selection.md). The declarative view of the same pipeline is [01-admin · 14](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md).

## Gotchas

- **`static Boolean hasRun` silently drops records.** With more than 200 records, or two unrelated saves in one transaction, everything after the first pass is skipped and nobody notices until the data is wrong.
- **An after trigger reading a roll-up summary gets the stale value** — roll-ups recalculate at steps 16–17, long after step 8.
- **Criteria-based sharing recalculates at step 18**, so a trigger asking whether a user can see the record is asking before the answer exists.
- **A guard set inside a `try` and never released blocks legitimate later work** in the same transaction. Clear it in `finally` if the operation can be retried. → [09](09-exception-handling-and-custom-exceptions.md)
- **Statics are not reverted by a savepoint rollback.** The data goes back; your `processed` set does not. → [05](05-dml-database-methods-and-savepoints.md)
- **The same trigger appearing twice in a debug log is usually correct**, not a defect — a step 14 flow or a step 16 roll-up re-entered the update path.

## Recall

Q: Where do before-save record-triggered flows fire relative to before triggers?
A: Before them — flows at step 3, before triggers at step 4. A flow may have already modified `Trigger.new`.

Q: At which steps is the record written and committed?
A: Written at step 7, committed at step 19. Everything in between is still discardable.

Q: Why is `static Boolean hasRun` the wrong recursion guard?
A: It is per-transaction, not per-record. Once set, every remaining record in the transaction is skipped — including records the trigger has never seen.

Q: What resets a static recursion guard?
A: The transaction boundary. Each batch chunk, Queueable and API call gets a fresh one, which is correct behaviour.

Q: Why does an after trigger see an out-of-date roll-up summary?
A: Roll-up summaries recalculate at steps 16–17, well after after-triggers run at step 8.

## Related

- [01-admin · 14 Order of execution — declarative view](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md) — the canonical full 20-step table this note conforms to
- [06 · Triggers & the handler framework](06-triggers-and-the-handler-framework.md) — the handler class where the guard actually lives
- [01 · Apex language core & governor limits](01-apex-language-core-and-governor-limits.md) — statics, the transaction boundary and the stack-depth ceiling
