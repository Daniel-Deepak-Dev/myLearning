# Queueable Apex & Chaining

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 04

**Scope:** The default async mechanism — typed state, delay, chaining and duplicate suppression. Choosing between it and the alternatives is [12](12-async-apex-overview-and-choosing.md); recovering from its failures is [16](16-transaction-finalizers.md).

> **What changed.** `@future` is legacy. It is not deprecated and existing methods still run, but it has no capability Queueable lacks and several Queueable has gained since — a job ID, typed member variables, chaining, a configurable delay, duplicate detection and finalizers. New async work has no reason to start there.

## Core idea

A Queueable is an object you hand to the platform to run later, and *object* is the operative word: it is a class with constructor arguments and member variables, so the state it needs travels with it. That single difference is why it displaced `@future`, whose primitives-only signature forced every job to re-query its own inputs and made passing a computed decision impossible. The second difference is that `System.enqueueJob` returns an ID, which turns "did it work" from an inbox question into a SOQL query. Everything else — the delay, the stack-depth introspection, the duplicate signature — exists to manage the one genuinely dangerous property of the mechanism: a job that enqueues its successor is a loop with no compiler-visible exit.

## How it works

| | `@future` | Queueable |
|---|---|---|
| Signature | `static void`, primitives only | `execute(QueueableContext)`, any member type |
| State | must be re-queried inside | carried in member variables |
| Handle | none | job ID returned by `enqueueJob` |
| Chaining | none | one child job per parent |
| Delay | none | 0–10 minutes |
| Callouts | `@future(callout=true)` | `implements Database.AllowsCallouts` |
| Recovery hook | none | `System.attachFinalizer` |

- **Three enqueue signatures.** `System.enqueueJob(job)`, `System.enqueueJob(job, delayInMinutes)` for 0–10 minutes, and `System.enqueueJob(job, asyncOptions)` for everything else. An org-wide default delay of 1–600 seconds can also be set in Setup, and an explicit delay argument overrides it.
- **`AsyncOptions` carries three things**: `MinimumQueueableDelayInMinutes`, `MaximumQueueableStackDepth`, and `DuplicateSignature`.
- **Duplicate suppression is built in.** Build a signature with `QueueableDuplicateSignature.Builder` — `addId()`, `addInteger()`, `addString()`, then `build()` — put it on `AsyncOptions.DuplicateSignature`, and a second enqueue with the same signature throws `DuplicateMessageException` instead of running the work twice.
- **`AsyncInfo` lets a job ask where it is**: `getCurrentQueueableStackDepth()`, `getMaximumQueueableStackDepth()`, `hasMaxStackDepth()`. Use the first as the chain's exit condition, not a static counter — statics do not survive the transaction boundary. → [07](07-order-of-execution-and-recursion.md)

```apex
public class ReconcileJob implements Queueable, Database.AllowsCallouts {
    private final List<Id> pending;                       // typed state — the @future problem, gone
    public ReconcileJob(List<Id> pending) { this.pending = pending; }

    public void execute(QueueableContext ctx) {
        System.attachFinalizer(new ReconcileFinalizer(pending));
        List<Id> remaining = reconcileFirstChunk(pending);          // does a callout
        if (!remaining.isEmpty() && AsyncInfo.getCurrentQueueableStackDepth() < 5) {
            System.enqueueJob(new ReconcileJob(remaining), 1);       // resume in ~1 minute
        }
    }
}
```

## 2026 currency

**Elastic limits for async jobs are Beta at 67.0** — Queueable and `@future` enqueues are accepted up to twice the licensed daily limit and the overflow is throttled rather than rejected. For chaining code this is a meaningful change of failure mode: a runaway chain used to stop with a `LimitException` at some point in the day, and now it slows down instead, which is harder to notice. Read `DailyAsyncApexElasticExecutions` and `DailyAsyncApexProcessed` from `System.OrgLimits.getMap()` if a job needs to back off on its own. Detail and Beta caveats: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

## Gotchas

- **One child job per parent.** A chain is a line, not a tree — a job that tries to enqueue two successors throws, so fan-out has to happen from the synchronous transaction or from a batch.
- **50 enqueues per synchronous transaction, one from an async context.** A trigger looping over 200 records and enqueuing per record hits the first limit at 50 and takes the whole save down with it.
- **Chain depth is capped at 5 in Developer and Trial orgs only.** Production has no documented ceiling, so a defective exit condition does not fail in the sandbox where you would notice — it fails as a consumed daily async limit in production.
- **Member variables are serialized when the job is enqueued.** Holding a non-serializable member — an open `Database.QueryLocator`, an `HttpResponse` — throws at enqueue time, not at execute time.
- **`Test.startTest()`/`stopTest()` runs one level of chain and no more**, and the delay argument is ignored entirely in tests. Chained-job behaviour is effectively untestable; assert on the first job's effects.
- **`DuplicateMessageException` is thrown at the enqueue site**, in the caller's transaction. If duplicate suppression is a normal condition rather than a defect, catch it — otherwise it takes down the save that tried to queue the work.
- **A Queueable that fails leaves no user-visible trace.** The only signal is a `Failed` row in `AsyncApexJob` and an email to whoever last edited the class. → [16](16-transaction-finalizers.md)

## Recall

Q: Why did Queueable displace `@future`?
A: It carries typed state in member variables instead of primitives only, returns a job ID you can query, supports chaining, delay, duplicate detection and finalizers.

Q: How many child jobs can a running Queueable enqueue?
A: One. Chains are linear; fan-out has to come from a synchronous transaction or a batch.

Q: How do you stop a self-chaining job from looping forever?
A: Exit on `AsyncInfo.getCurrentQueueableStackDepth()`, not on a static counter — statics reset at every transaction boundary.

Q: What happens when a Queueable is enqueued twice with the same `DuplicateSignature`?
A: The second `System.enqueueJob` throws `DuplicateMessageException` in the calling transaction; the job does not run twice.

Q: What is the maximum delay you can pass to `System.enqueueJob`?
A: 10 minutes — and the delay is ignored during Apex tests.

## Related

- [12 · Async Apex overview & choosing](12-async-apex-overview-and-choosing.md) — when a Queueable is the wrong shape for the work
- [16 · Transaction Finalizers](16-transaction-finalizers.md) — the only hook that survives an uncatchable failure in a Queueable
- [19 · Callouts, Named Credentials & HTTP](19-callouts-named-credentials-and-http-in-apex.md) — what `Database.AllowsCallouts` actually unlocks, and its limits
