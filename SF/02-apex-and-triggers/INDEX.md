# 02 · Apex & Triggers

Expert Apex, including the **API 67.0 security rewrite that invalidates most published examples**. **24 topics** · phases [03](PHASES.md), [04](PHASES.md), [05](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **Three defaults flipped at 67.0** and they touch nearly every note in this area: SOQL/DML default to **user mode**; a keyword-less class defaults to **`with sharing`**; **`WITH SECURITY_ENFORCED` no longer compiles**. The anchor for all three is [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md) — notes here must not contradict it.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | Apex language core & governor limits | types, collections, per-transaction limit map | 03 |
| 02 | Modern Apex syntax 🆕 | null coalescing `??`, safe navigation `?.`, switch | 03 |
| 03 | SOQL fundamentals & relationship queries | parent/child traversal, aggregates, date literals | 03 |
| 04 | Advanced SOQL, SOSL & dynamic queries | TYPEOF, FOR UPDATE, bind vars, injection defence | 03 |
| 05 | DML, Database methods & savepoints | allOrNone, SaveResult handling, rollback semantics | 03 |
| 06 | Triggers & the handler framework | one trigger per object, context vars, dispatcher pattern | 03 |
| 07 | Order of execution & recursion ⚠️ | full save order incl. flows; static recursion guards | 03 |
| 08 | Bulkification patterns | maps/sets, no SOQL-DML in loops, 200-record chunks | 03 |
| 09 | Exception handling & custom exceptions | catch scope, `addError`, partial-success design | 03 |
| 10 | Apex security: user mode & FLS 🆕⚠️ | user mode is the 67.0 default; `WITH SECURITY_ENFORCED` retired | 04 |
| 11 | Sharing keywords & Apex managed sharing 🆕⚠️ | keyword-less classes now `with sharing`; triggers always system mode | 04 |
| 12 | Async Apex overview & choosing | future vs queueable vs batch vs events | 04 |
| 13 | Queueable Apex & chaining ⚠️ | replaces `@future`; delay, depth, allowCallouts | 04 |
| 14 | Batch Apex & stateful processing | scope sizing, `Database.Stateful`, failure isolation | 04 |
| 15 | Scheduled Apex & CRON | Schedulable, CRON syntax, scheduling from Apex | 04 |
| 16 | Transaction Finalizers *(GA Winter '22)* | post-Queueable hook, retry/alert on uncatchable failures | 04 |
| 17 | `Database.Cursor` & large result sets 🆕 | cursor pagination, heap avoidance, vs QueryLocator | 04 |
| 18 | Platform Events & CDC in Apex | publish behaviours, event triggers, replay handling | 04 |
| 19 | Callouts, Named Credentials & HTTP ⚠️ | callout limits, new-style named credentials, no hardcoded endpoints | 04 |
| 20 | Apex testing fundamentals ⚠️ | `@TestSetup`, data factory, never `SeeAllData=true` | 05 |
| 21 | Apex testing advanced & mocking | HttpCalloutMock, Stub API, `Assert` class, async assertions | 05 |
| 22 | Invocable Apex & Agentforce actions 🆕 | `@InvocableMethod` contract, mandatory no-arg constructor at 67.0 | 05 |
| 23 | `UserDefinedType` & typed interop 🆕 | typed payloads across Apex, Flow and agent actions | 05 |
| 24 | Apex performance & profiling | CPU/heap hotspots, query cost, debug log reading | 05 |

## Related

- **07** is the code-side twin of [01-admin · 14 Order of execution](../01-admin-and-declarative-platform/INDEX.md).
- **10–11** are the Apex projection of [07-security-and-sharing](../07-security-and-sharing/INDEX.md) — read together.
- **19** continues in [06-integration-and-apis · 15 Named credentials](../06-integration-and-apis/INDEX.md).
- **22–23** are the bridge into [AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) — that note already carries the 67.0 action-contract facts.
