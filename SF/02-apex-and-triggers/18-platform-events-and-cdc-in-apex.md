# Platform Events & CDC in Apex

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 04

**Scope:** Publishing and subscribing from Apex — publish behaviours, event triggers, retries and Change Data Capture. The transport, external subscribers and event design belong to [06-integration](../06-integration-and-apis/INDEX.md); this is the in-org half.

## Core idea

A platform event is a message with no addressee. Apex publishes it, the event bus keeps it, and whoever has subscribed receives it in *their* transaction — which makes it the only decoupling primitive on the platform where the publisher genuinely does not know or care who is listening. That independence is the feature and the cost: you get fan-out, replay and a subscriber that can be added without touching the publisher, and you give up the transaction, the ordering guarantee across event types, and any synchronous way to know the work succeeded. Change Data Capture is the same machinery with the events generated for you — every insert, update, delete and undelete on a selected object becomes a message on `AccountChangeEvent` and friends, with a header describing what happened.

## How it works

| | Publish Immediately | Publish After Commit |
|---|---|---|
| Sent when | `EventBus.publish()` runs | the transaction commits |
| Rolled back with the transaction | **no** | yes |
| Fits | telemetry, audit, "we attempted this" | "this happened" — downstream work |

- **`EventBus.publish(events)` returns `Database.SaveResult[]`**, positional like any DML result. It consumes a DML statement, so publishing inside a loop burns the 150-statement limit exactly the way `insert` does. → [08](08-bulkification-patterns.md)
- **Subscribe with an `after insert` trigger on the event object.** No other trigger event exists. The trigger receives up to **2,000 event messages** per execution and runs in its own transaction with its own limits — synchronous ones, despite being asynchronous work.
- **The subscriber runs as the Automated Process user** unless you override it with `PlatformEventSubscriberConfig`, which also controls which user's debug logs the execution lands in.
- **Two retry strategies, and you pick one per trigger.** Throwing `EventBus.RetryableException` replays the whole batch; `EventBus.TriggerContext.currentContext().setResumeCheckpoint(replayId)` instead marks the last message you finished, so a retry after an uncaught exception resumes from there rather than reprocessing.
- **CDC gives you a `ChangeEventHeader`** on every message: `changeType` (`CREATE`/`UPDATE`/`DELETE`/`UNDELETE`), `recordIds`, `changedFields`, `commitUser`, `commitTimestamp` and `transactionKey` — the last of which is how you reassemble one user action from several event messages.

```apex
trigger OrderSyncEvent on Order_Sync__e (after insert) {
    EventBus.TriggerContext ctx = EventBus.TriggerContext.currentContext();
    for (Order_Sync__e e : Trigger.new) {
        try {
            handle(e);
        } catch (CalloutException ex) {
            if (ctx.retries < 4) {                  // 10 runs total is the platform's ceiling
                throw new EventBus.RetryableException(ex.getMessage());
            }
            logDeadLetter(e, ex);                   // give up deliberately, keep the evidence
        }
    }
}
```

## 2026 currency

Two things to keep straight. First, **external** subscribers no longer use the legacy streaming transport — that migration is real and consequential, but it belongs to [06-integration](../06-integration-and-apis/INDEX.md) and changes nothing about an Apex trigger subscriber, which has always been in-process. Second, the 67.0 rule that **triggers always run in system mode** applies here too: an event trigger cannot declare sharing or an access mode, so it sees everything regardless of what the Automated Process user could see on its own. That removes a class of confusion and adds a responsibility — any filtering an event subscriber ought to do is now unambiguously your code's job. → [11](11-sharing-keywords-and-apex-managed-sharing.md), and [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **The `ReplayId` does not exist yet in the publishing transaction.** The bus assigns it after publish, so the `SaveResult` cannot hand you a handle to the message you just sent.
- **Publish Immediately events survive a rolled-back transaction.** That is the point of the setting, and it is also how a "record created" event gets emitted for a record that was never created.
- **`UserInfo.getUserId()` in an event trigger is the Automated Process user**, not whoever caused the change. Carry the actor on the payload, or read `ChangeEventHeader.commitUser` for CDC.
- **After ten runs — one attempt plus nine retries — the trigger enters an error state and stops processing new events entirely.** The failure mode is a silently dead subscriber, not an infinite loop, and it stays dead until the class is fixed and saved.
- **High-volume events are retained for 72 hours.** A subscriber down longer than that has lost the messages, permanently and without notification.
- **A CDC delete gives you `recordIds` and nothing else.** The field values are gone by the time the event arrives, so anything you need at delete time must be captured before it.
- **Event triggers get synchronous governor limits** — 100 SOQL queries and 10,000 ms CPU for up to 2,000 messages. Bulkify the subscriber exactly as hard as a record trigger.

## Recall

Q: Which trigger events can you use to subscribe to a platform event in Apex?
A: `after insert` only, and the trigger receives up to 2,000 messages per execution in its own transaction.

Q: What is the difference between Publish Immediately and Publish After Commit?
A: Publish Immediately sends the event when `EventBus.publish()` runs and it is not rolled back with the transaction; Publish After Commit sends it only if the transaction commits.

Q: How many times will a platform event trigger run before it gives up?
A: Ten — the initial run plus nine retries. It then moves to an error state and stops processing new events until the code is fixed and saved.

Q: Which user does an event trigger run as?
A: The Automated Process user, unless overridden with `PlatformEventSubscriberConfig`.

Q: What does `setResumeCheckpoint()` do that `EventBus.RetryableException` does not?
A: It records the last message successfully processed, so a retry resumes from that point instead of replaying the entire batch.

## Related

- [14 · Batch Apex & stateful processing](14-batch-apex-and-stateful-processing.md) — `BatchApexErrorEvent`, the same subscription pattern applied to job failures
- [06-integration · Platform events & Pub/Sub API](../06-integration-and-apis/INDEX.md) — event design, external subscribers and the transport this note deliberately skips
- [09 · Exception handling & custom exceptions](09-exception-handling-and-custom-exceptions.md) — where the dead-letter record belongs once retries are exhausted
- [26 · Testing platform events & CDC](26-testing-platform-events-and-cdc.md) — forcing delivery, and why an untested subscriber passes green
- [06-integration · 27 Event bus allocations, limits & monitoring](../06-integration-and-apis/27-event-bus-allocations-limits-and-monitoring.md) — `EventBusSubscriber` health and parallel subscriptions at 67.0
