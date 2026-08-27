# Scheduled Apex & CRON

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 04

**Scope:** Running Apex on a clock — the `Schedulable` interface, CRON expressions, and managing the jobs once they exist. What the scheduled job then starts is usually [14](14-batch-apex-and-stateful-processing.md) or [13](13-queueable-apex-and-chaining.md).

## Core idea

`Schedulable` is a trigger with a clock instead of a record. The interface is one method, the scheduling is one call, and almost every mistake in the topic comes from forgetting that the scheduled class runs under **synchronous** governor limits: it is an entry point, not a worker. The correct shape is therefore always the same — `execute()` decides *what* to run and hands it to a batch or a Queueable, which is where the real limits live. The second half of the topic is operational rather than syntactic. A schedule is a persistent object in the org with a name, an owner, a timezone and a next-fire time; it outlives the developer who created it, it cannot be edited in place, and it will block a deployment of the class it points at.

## How it works

| # | CRON field | Values |
|---|---|---|
| 1 | Seconds | `0–59` |
| 2 | Minutes | `0–59` |
| 3 | Hours | `0–23` |
| 4 | Day of month | `1–31`, `L` (last), `W` (nearest weekday) |
| 5 | Month | `1–12` or `JAN`–`DEC` |
| 6 | Day of week | `1–7` or `SUN`–`SAT`, `L`, `#` (nth) |
| 7 | Year *(optional)* | `1970–2099` |

- **Exactly one of day-of-month and day-of-week must be `?`.** Specifying both is an error, because they are two ways of answering the same question.
- **`/` means increment, and it is how you get below the UI's hourly minimum.** `0 0/15 * * * ?` is "the first minute and every fifteenth thereafter" — the Setup scheduler cannot express it; `System.schedule` can.
- **`System.scheduleBatch(batchable, name, minutesFromNow)` is the one-shot variant** — no CRON, runs once, deletes itself afterwards. Ideal for "start this in five minutes" from a trigger or a finish method.
- **`CronTrigger` and `CronJobDetail` are the state.** Query `NextFireTime`, `PreviousFireTime`, `State`, `TimesTriggered` and `CronExpression`, joined to `CronJobDetail` for the job's name — that is your scheduled-job monitoring page.

```apex
public class NightlyArchive implements Schedulable {
    public void execute(SchedulableContext sc) {
        Database.executeBatch(new ArchiveOrders(), 200);  // start the work, never do it here
    }
}
// 02:00 every day             0 0 2 * * ?
// every 15 minutes            0 0/15 * * * ?
// 09:00, last Friday of month 0 0 9 ? * 6L
String jobId = System.schedule('Nightly archive', '0 0 2 * * ?', new NightlyArchive());
System.abortJob(jobId);        // a schedule cannot be edited — abort and re-create
```

## 2026 currency

Nothing in the scheduling mechanism itself changed at 67.0, but what runs *under* it did. A scheduled class runs as the user who scheduled it, and at 67.0 its SOQL and DML default to that user's access — so a job scheduled years ago by an admin who has since been deactivated or had permissions reduced does less than it used to, silently, the first time its class is recompiled at 67.0. Auditing `CronTrigger.OwnerId` against still-active, still-privileged users is a genuinely new piece of housekeeping. The access-mode mechanics are [10](10-apex-security-user-mode-and-fls.md); the release detail is [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **A pending scheduled job blocks deployment of its class.** The error is *"This schedulable class has jobs pending or in progress"*, and the only fix is to abort the job, deploy, and reschedule — which needs to be in the release runbook, not discovered at 23:50.
- **Synchronous callouts are not allowed from `execute()`.** Hand the work to a `Queueable implements Database.AllowsCallouts` instead. → [13](13-queueable-apex-and-chaining.md)
- **100 scheduled Apex jobs is the ceiling**, and scheduling from a trigger is the classic way to reach it — every save adds another job that nothing removes.
- **The schedule uses the scheduling user's timezone**, so a job set to 02:00 moves an hour twice a year and can run twice or not at all on the changeover night.
- **The scheduled time is when the job is *queued*, not when it runs.** Under load the platform starts it late, so two jobs 60 seconds apart are not guaranteed to execute in that order.
- **A `Schedulable` that does the work itself gets synchronous limits** — 100 SOQL queries, 6 MB heap, 10,000 ms CPU. The batch it should have started would have had none of those problems.
- **Aborting a job deletes its `CronTrigger` row**, so the run history goes with it. Log elsewhere if you need to prove a job ran.

## Recall

Q: How many fields does a Salesforce CRON expression have, and what is the first one?
A: Seven, the last optional — Seconds, Minutes, Hours, Day-of-month, Month, Day-of-week, Year. It starts with Seconds, not Minutes.

Q: Why must one of day-of-month and day-of-week be `?`
A: They are two ways of specifying the same day; setting both is contradictory, so the platform requires one to be explicitly unspecified.

Q: What should a `Schedulable.execute()` method actually contain?
A: A handoff — `Database.executeBatch` or `System.enqueueJob`. It runs under synchronous limits and no callouts are permitted from it.

Q: How do you change the time an existing scheduled job runs?
A: You cannot edit it. Abort with `System.abortJob(id)` and schedule a new one.

Q: What breaks a deployment that touches a scheduled class?
A: A pending or in-progress job on that class. Abort it, deploy, then reschedule.

## Related

- [14 · Batch Apex & stateful processing](14-batch-apex-and-stateful-processing.md) — what a scheduled job almost always starts
- [12 · Async Apex overview & choosing](12-async-apex-overview-and-choosing.md) — the shared async limits every scheduled run draws on
- [04-flow · Flow at scale](../04-flow-and-automation/INDEX.md) — scheduled-triggered flows, the declarative alternative for simple clock-driven work
