# Transaction Finalizers

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 04

**Scope:** The post-transaction hook on a Queueable — what runs after the job has already failed. The job itself is [13](13-queueable-apex-and-chaining.md); the batch equivalent is `BatchApexErrorEvent` in [14](14-batch-apex-and-stateful-processing.md).

## Core idea

Some Apex failures cannot be caught. A `LimitException` — CPU timeout, heap exhaustion, too many queries — unwinds the transaction past every `catch` block you wrote, which means the standard advice to "log the error and alert" is unimplementable exactly when it matters most. A transaction finalizer closes that hole. It is a separate object attached to a Queueable job, and the platform runs it in a **new transaction** after the job's transaction has ended, whatever ended it. It gets told which job it is finalising, whether that job succeeded, and the exception if it did not — and it gets a fresh governor budget to act on that, including a callout and exactly one enqueue. That last allowance is what makes it a retry mechanism and not just a logger.

## How it works

| `FinalizerContext` method | Returns |
|---|---|
| `getAsyncApexJobId()` | the `AsyncApexJob` ID of the parent Queueable |
| `getRequestId()` | the request ID, shared with the parent's debug log — the join key |
| `getResult()` | `ParentJobResult.SUCCESS` or `ParentJobResult.UNHANDLED_EXCEPTION` |
| `getException()` | the exception that ended the job, or null on success |

- **Attach it from inside the Queueable's `execute()`** with `System.attachFinalizer(f)`. One per job; a second attach throws.
- **It runs regardless of outcome**, so `getResult()` is the first line of any real implementation — a finalizer that logs unconditionally logs every success too.
- **It may enqueue a single async job** — Queueable, `@future` or batch. Re-enqueuing the parent is the retry pattern, and a failed Queueable can be retried **five times** this way before the chaining limit stops it.
- **Callouts are allowed**, which makes paging an external alerting system a legitimate use rather than a workaround. Limits are otherwise **synchronous** caps, with three exceptions that use the asynchronous ones: total heap size, maximum enqueued jobs, and `@future` method limits.

```apex
public class ReconcileFinalizer implements Finalizer {
    private final List<Id> pending;
    private final Integer attempt;
    public ReconcileFinalizer(List<Id> pending, Integer attempt) {
        this.pending = pending;  this.attempt = attempt;
    }
    public void execute(FinalizerContext ctx) {
        if (ctx.getResult() == ParentJobResult.SUCCESS) { return; }
        insert new Job_Failure__c(Job__c     = ctx.getAsyncApexJobId(),
                                  Request__c = ctx.getRequestId(),
                                  Error__c   = ctx.getException().getMessage(),
                                  Attempt__c = attempt);
        if (attempt < 5) {                                    // the one enqueue we are allowed
            System.enqueueJob(new ReconcileJob(pending, attempt + 1));
        }
    }
}
```

## 2026 currency

Two 67.0 changes land on this pattern from opposite directions. The finalizer's own DML now runs in **user mode** like everything else, so a failure logger writing to an audit object as an under-privileged automation user throws inside the finalizer — and there is no second finalizer to record *that*. Give the logging object's write permission to whoever the job runs as, or elevate the insert deliberately. Meanwhile, **elastic async limits (Beta)** mean a job that would have failed on the daily enqueue ceiling now gets throttled instead, so a retry chain that used to terminate loudly can keep quietly re-arming itself. Cap attempts in your own state; do not rely on a limit to do it. Sources: [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md) and [developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

## Gotchas

- **Queueable only.** Batch, scheduled and `@future` jobs cannot attach a finalizer — batch uses `Database.RaisesPlatformEvents` and a `BatchApexErrorEvent` trigger instead.
- **`attachFinalizer` must be called inside `execute()`.** Attaching from the constructor or from the enqueuing transaction does not register anything.
- **It is not a `catch` block.** It runs *after* the transaction ended, so it cannot suppress the rollback or repair data mid-flight — the parent's DML is already gone.
- **Nothing catches a failing finalizer.** There is no finalizer for a finalizer, so an exception inside it loses the log and the retry together. Keep it small and defensive.
- **Re-query nothing you can carry.** The finalizer starts from committed state, so the IDs and context it needs must be member variables set before the parent job ran.
- **The retry count is yours to keep.** The platform does not count attempts; five is only the point at which chaining stops, not a counter you can read.
- **A finalizer that always enqueues is an infinite chain** — the `getResult()` guard is load-bearing, not defensive style.

## Recall

Q: What problem do transaction finalizers solve that a `try`/`catch` cannot?
A: Uncatchable failures — a `LimitException` unwinds past every catch block, so the finalizer is the only code that still runs after a CPU or heap blowout.

Q: Where must `System.attachFinalizer()` be called?
A: Inside the Queueable's `execute()` method. One finalizer per job; a second attach throws.

Q: What does `FinalizerContext.getResult()` return?
A: `ParentJobResult.SUCCESS` or `ParentJobResult.UNHANDLED_EXCEPTION` — the finalizer runs on both, so this is the first thing to check.

Q: How many jobs can a finalizer enqueue, and how many times can it retry the parent?
A: One async job per finalizer, and a failed Queueable can be retried five times this way before the chaining limit ends it.

Q: Which async types support finalizers?
A: Queueable only. Batch reports failures through `BatchApexErrorEvent`; `@future` and scheduled Apex have no equivalent hook.

## Related

- [13 · Queueable Apex & chaining](13-queueable-apex-and-chaining.md) — the job a finalizer attaches to, and the chain it can restart
- [09 · Exception handling & custom exceptions](09-exception-handling-and-custom-exceptions.md) — where the catchable half of failure handling lives
- [18 · Platform Events & CDC in Apex](18-platform-events-and-cdc-in-apex.md) — `BatchApexErrorEvent`, the same idea for batch jobs
