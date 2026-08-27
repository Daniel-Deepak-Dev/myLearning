# Observability, Logging & Prod Debugging

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 17

**Scope:** Knowing what production did, after it did it. Performance hotspots are [17](17-apexguru-and-performance-review.md); the security-audit view of the same event streams is [07-security · 23](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md).

## Core idea

The constraint that shapes everything here is simple and non-negotiable: **debug logs are a development tool that Salesforce also exposes in production, and they are capped, retrospective and short-lived.** A trace flag captures nothing that happened before you set it, which means the first production incident is always debugged from evidence that does not exist.

So production observability on this platform is a **design decision made in advance**, not a tool you reach for during an incident. It has three layers: a durable custom log your own code writes, the platform's event streams for what your code did not write, and the org's own health telemetry.

## How it works

- **The hard numbers.** Each log is capped at **20 MB**. **System debug logs are retained 24 hours; monitoring debug logs 7 days.** Generate more than **1,000 MB in a 15-minute window** and your **trace flags are disabled** — an email goes to whoever last modified them, and they can be re-enabled after 15 minutes.
- **Trace flags expire**, and they are set per user, per Apex class or per trigger, against a **Debug Level**. Leaving one on a busy integration user is the fastest way to hit the ceiling above.
- **Build a custom logging object or platform event.** The platform-event version is the strong pattern: a `publishImmediate` event **survives the transaction rollback that destroyed the evidence**, which a `Log__c` insert does not → [02-apex · 18](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md).
- **Log a correlation ID** — a UUID minted at the entry point and carried through every callout, async hop and event — or an async chain is unreconstructable → [06-integration · 23](../06-integration-and-apis/23-idempotency-retries-and-error-handling.md).
- **Event Monitoring is the tier above.** Event Log Files give you Apex execution, API calls, report exports and page views after the fact; Real-Time Event Monitoring streams a subset live.
- **Apex Replay Debugger** turns a log into a step-through session in VS Code — free, and the reason to capture a good log rather than a big one.
- **Unhandled exceptions email someone.** Configure that address deliberately; the default sends to the last code modifier, which is not an on-call rota.

## 2026 currency

Two things worth folding in. **Elastic async limits (Beta)** change the shape of async failure: a runaway `Queueable` chain that used to stop with a `LimitException` can now be throttled instead, so the symptom moves from an error email to a queue draining late — which is invisible unless you are already logging enqueue and execution times → [02-apex · 24](../02-apex-and-triggers/24-apex-performance-and-profiling.md). And **agent workloads need their own observability story**: local traces land in `.sfdx/agents/…/traces/`, production goes through the Session Trace Data Model, and neither appears in a debug log → [AI_Data · observability](../../AI_Data/02-salesforce-ai/09-observability-and-testing/notes.md).

## Gotchas

- **The log you need is the one you did not enable.** Trace flags are prospective only — there is no "show me last Tuesday".
- **A 20 MB truncation removes the middle of the log**, which is usually the part you wanted. Narrow the Debug Level instead of turning everything to FINEST.
- **`System.debug()` is evaluated even when logging is off.** String concatenation inside one costs CPU in production for nothing.
- **An empty `catch` block deletes the incident**, not the error → [02-apex · 09](../02-apex-and-triggers/09-exception-handling-and-custom-exceptions.md).
- **`Database.insert(records, false)` returns errors nobody reads.** Partial-success DML is the most common source of silent data loss.
- **Event Log Files are licensed and delayed** — most are hourly or daily, so they answer "what happened" and never "what is happening".
- **Logs contain data.** A custom logging framework that serialises records into a log object has just created an unencrypted copy of the fields you protected → [07-security · 21](../07-security-and-sharing/21-shield-platform-encryption.md).

## Recall

Q: What is the fundamental limitation of debug logs in production?
A: They are prospective — a trace flag captures nothing from before it was set, so the first occurrence of an incident is never logged.

Q: What happens after 1,000 MB of debug logs in a 15-minute window?
A: Trace flags are disabled org-wide and the last modifier is emailed; they can be re-enabled after 15 minutes.

Q: How long do debug logs survive?
A: System debug logs 24 hours, monitoring debug logs 7 days — and each log is capped at 20 MB.

Q: Why log through a platform event rather than a custom object?
A: A `publishImmediate` event survives the rollback that would delete a `Log__c` row, so the failing transaction still leaves evidence.

Q: What makes an async failure reconstructable?
A: A correlation ID minted at the entry point and carried through every callout, queueable and event.

## Related

- [17 · ApexGuru & performance review](17-apexguru-and-performance-review.md) — runtime metrics where this note has runtime evidence
- [07-security · 23 Event Monitoring & Transaction Security](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md) — the same streams read for audit
- [02-apex · 09 Exception handling & custom exceptions](../02-apex-and-triggers/09-exception-handling-and-custom-exceptions.md) — where the evidence is usually destroyed
- [06-integration · 23 Idempotency, retries & error handling](../06-integration-and-apis/23-idempotency-retries-and-error-handling.md) — correlation across system boundaries
