# 03 · Core Platform

Scenario questions on Apex, sharing and integration — the platform underneath the AI work, and the area where a Salesforce developer's existing depth is the differentiator. Source knowledge: [SF/](../../SF/README.md).

> ⚠️ **Two decade-old answers became wrong, and both are load-bearing here.** *"A user's record access is the union of everything that grants it"* became incomplete at **Winter '22** — restriction rules subtract. And *"automation runs as an administrator, so the access model is a UI concern"* is wrong in both directions at **67.0**: Apex now defaults to user mode and `with sharing`, while Flow's triggered types did not move. The same logic is now **more permissive built in Flow than in Apex**.

| Set | Scenarios it drills | Level |
|---|---|---|
| [01 · Apex, triggers & limits](01-apex-triggers-and-limits.md) | A per-transaction recursion guard silently dropping records · a stale roll-up and a before-save flow ⚠️ · a bulk map lookup returning null because of sharing 🆕 · data skew behind a clean query plan | medium → complex |
| [02 · Sharing & security](02-sharing-and-security.md) | The same requirement in Apex and in Flow ⚠️🆕 · a sharing audit reporting access the user does not have · async sharing recalculation and the test that will fail 🆕 · an agent's running user and `without sharing` | medium → complex |
| [03 · Integration & async](03-integration-and-async.md) | "Can we use Pub/Sub?" as a pattern question · *Publish Immediately* surviving a rollback · a retrying partner and 240 duplicate orders · "async gets fresh limits" in a pull request 🆕 | medium → complex |

**12 scenarios.** The recurring shape: code that passes every test and is wrong at volume, or under a different user, or on the second delivery.

## The five highest-value things to be able to say

1. **Guard per record, not per invocation.** A `static Boolean hasRun` is the guard most codebases have and it is wrong — the first chunk sets it and every later record is skipped silently. Track processed Ids.
2. **The value is produced later in the pipeline than the code reading it.** That one sentence answers most "why did my trigger see the wrong value?" questions. Roll-ups recalculate at steps 16–17; before-save flows fire at step 3, ahead of every before trigger.
3. **Whose access is being enforced here, and is it being enforced at all?** The only question worth asking of any component. Contexts do not agree with each other, and an agent adds no boundary of its own — it inherits its running user's access exactly.
4. **A timeout is not a failure**, and every event bus here is **at-least-once**. Correctness comes from the receiver. A sender that retries is behaving correctly; a receiver that cannot recognise a repeat is the defect.
5. **Going async gets you another transaction, not more budget.** The enqueuing transaction still has to finish inside its own limits, and the daily async ceiling is shared across every mechanism.

## The tools that will not show you the problem

Worth knowing as a set, because each one produces a confident all-clear on a real defect:

| Tool | What it misses |
|---|---|
| **Query Plan** | Data skew. The index exists, is used, and is selective — the problem is the shape of the data |
| **Sharing audit** | Restriction rules. Share rows exist and the user still gets nothing back |
| **A passing Apex test** | Async sharing recalculation, which the platform chooses by volume — and async ordering, since `stopTest()` runs queued work synchronously |
| **Code coverage** | Batch size. A guard correct for one record and wrong for 201 shows 100% |

## Related

- [SF/](../../SF/README.md) — the source notes every answer links into, and [SF/CURRENCY.md](../../SF/CURRENCY.md) for what invalidates older tutorials
- [SF/07-security-and-sharing/](../../SF/07-security-and-sharing/INDEX.md) · [SF/02-apex-and-triggers/](../../SF/02-apex-and-triggers/INDEX.md) · [SF/06-integration-and-apis/](../../SF/06-integration-and-apis/INDEX.md) — the three areas these sets draw on most
- [04-cross-domain/](../04-cross-domain/INDEX.md) — where platform limits collide with Agentforce and Data 360
