# Apex Performance & Profiling

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 05

**Scope:** Finding out *where* a transaction spends itself, and what to do about it. The limit table itself is [01](01-apex-language-core-and-governor-limits.md); making the underlying query selective is an [08-data · 09](../08-data-modeling-and-large-data-volumes/09-query-plan-and-performance-tuning.md) problem.

## Core idea

Two limits actually end transactions in practice: **CPU time** (10,000 ms sync / 60,000 ms async) and **heap** (6 MB / 12 MB). Everything else — queries, DML statements, rows — is usually a bulkification defect you already know how to fix, and it fails loudly with a limit name attached. CPU and heap fail differently: they are cumulative across everything in the save order, so the class that throws is frequently not the class that spent the budget. That makes profiling a question of *attribution* rather than optimisation, and the tool for attribution is the debug log, read with the right log levels and with an understanding of what the numbers at the bottom actually count.

## How it works

- **`Limits` is the in-transaction instrument.** `Limits.getCpuTime()`, `getHeapSize()`, `getQueries()`, `getDmlRows()` — and the `getLimit*()` counterparts for the ceiling. Logging the delta around a suspect block attributes cost far faster than reading a whole log.
- **`System.OrgLimits.getMap()`** answers the *daily* question instead: async executions, API requests, storage. Different problem, different tool.
- **Log levels matter more than log size.** `PROFILING` and `FINEST` on Apex Code generate the cumulative-time lines you want; `DEBUG` on everything just fills the buffer.
- **The `CUMULATIVE_PROFILING` and `LIMIT_USAGE_FOR_NS` blocks at the end of a log** are the summary — SOQL, DML, CPU and heap per namespace. Read those first, then work backwards.
- **CPU time excludes waiting.** Callouts, database time and DML processing do not count; your loops and collection work do. A transaction that takes 40 seconds of wall clock can use 300 ms of CPU. → [01](01-apex-language-core-and-governor-limits.md)
- **Heap measures what is still reachable.** A list you have finished with holds its memory until the reference leaves scope, which is why a SOQL for-loop beats a query into a variable.

```apex
Long cpu0 = Limits.getCpuTime();
Integer heap0 = Limits.getHeapSize();
enrich(scope);                                            // the suspect
System.debug(LoggingLevel.ERROR, 'enrich: '
    + (Limits.getCpuTime() - cpu0) + 'ms, '
    + (Limits.getHeapSize() - heap0) + ' bytes');         // ERROR so it survives a low log level
```

## 2026 currency

Nothing about the limits themselves changed at 67.0, but two things around them did. **Elastic async limits are Beta**, which converts a class of failure into a slowdown — a runaway chain that used to stop with a `LimitException` now gets throttled, so the symptom moves from an error email to a queue that drains late. → [12](12-async-apex-overview-and-choosing.md). And **the security flip changes what a query costs**: user-mode SOQL evaluates sharing, so a query that was cheap for an admin is not necessarily cheap for a portal user, and the row count it returns may differ too. → [10](10-apex-security-user-mode-and-fls.md). For static analysis rather than runtime profiling, **ApexGuru** and **Code Analyzer v5** are the current tooling — covered in [09-devops](../09-devops-sfdx-and-release-management/INDEX.md) rather than here.

## Gotchas

- **The class that throws is rarely the class that spent the budget.** CPU and heap accumulate across the whole save order, so a trigger failing at 10,000 ms may be paying for a flow that ran before it. → [07](07-order-of-execution-and-recursion.md)
- **Debug logs are truncated when they exceed the size cap**, and the truncation removes the *middle* — the summary at the end survives, the detail you wanted may not.
- **Turning on a trace flag changes the timing you are measuring.** Logging at `FINEST` adds real overhead; confirm a fix with the log off.
- **`System.debug` costs CPU even when the log level would discard it**, because the arguments are still evaluated — string concatenation inside a loop is a measurable expense.
- **A nested loop over two collections is the classic CPU killer**, not the queries. Build a `Map` and index into it.
- **Sorting and `String` manipulation dominate more often than expected.** `List.sort()` on a large list with a `Comparable` implementation runs your Apex once per comparison.
- **Heap is not released by `clear()` on a list you still reference.** Null the reference, or scope it tighter.
- **Async does not reset heap for a chained job's caller** — each transaction gets its own budget, which is precisely the reason to chain. → [13](13-queueable-apex-and-chaining.md)

## Recall

Q: Which two governor limits actually end most real transactions?
A: CPU time (10,000 ms sync / 60,000 ms async) and heap (6 MB / 12 MB). The rest usually signal a bulkification defect.

Q: Does a slow callout push you toward the CPU limit?
A: No — callout, database and DML processing time are excluded. CPU time measures your own code's execution.

Q: What is the fastest way to attribute cost to a specific block of code?
A: Capture `Limits.getCpuTime()` and `Limits.getHeapSize()` before and after it and log the delta, rather than reading a whole debug log.

Q: Why can a query that performed well for an admin be slower at 67.0?
A: User-mode SOQL evaluates sharing for the running user, changing both the cost and the rows returned.

Q: What does `System.OrgLimits.getMap()` tell you that `Limits` does not?
A: Daily, org-wide consumption — async executions, API calls, storage — rather than the current transaction's usage.

## Related

- [01 · Apex language core & governor limits](01-apex-language-core-and-governor-limits.md) — the full per-transaction limit table
- [08 · Bulkification patterns](08-bulkification-patterns.md) — the fix for almost every limit that is not CPU or heap
- [08-data · 09 Query Plan & performance tuning](../08-data-modeling-and-large-data-volumes/09-query-plan-and-performance-tuning.md) — where slow queries are actually diagnosed and solved
