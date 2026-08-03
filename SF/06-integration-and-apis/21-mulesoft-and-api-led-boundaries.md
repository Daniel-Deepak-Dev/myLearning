# MuleSoft & API-led boundaries

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** The judgment call — what belongs on the platform and what belongs off it. Product depth is deliberately out of scope; this is the boundary argument you have to make in a design review. Agent-layer governance is [AI_Data · Agent Fabric](../../AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md).

## Core idea

Salesforce is very good at being a system of record and quite bad at being a system of transit. Every governor limit is a statement that the platform is not where you should do high-volume, long-running, many-system work — and every integration that ignores that ends up as a Queueable chain nobody can debug.

**API-led connectivity** is the vocabulary for drawing that line: three layers, each with a different rate of change. *System* APIs expose a source system faithfully. *Process* APIs compose them into a business capability. *Experience* APIs shape that capability for one consumer. The value of the model is not the diagram — it is that it forces the question *which layer is this logic in*, and orphan logic that answers "all three" is the logic that will not survive a source system being replaced.

## How it works

- **The three layers are about change, not about tiers.** A system API changes when the source system does; a process API changes when the business does; an experience API changes when a UI does. Putting them in one place couples all three clocks.
- **MuleSoft is the product; the boundary is the idea.** The same reasoning applies with any gateway, iPaaS or hand-built service — and applies equally to *not* buying one.
- **Anypoint Exchange is a catalog**, and the reason MuleSoft became the home of Salesforce's agent-governance story: it already knew how to register, govern and observe APIs → [AI_Data · Agent Fabric](../../AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md).
- **On-platform is right when** the logic is Salesforce-only, the volume fits in limits, and the data already lives here.
- **Off-platform is right when** the work fans out to several systems, must survive Salesforce being down, exceeds callout or CPU budgets, or needs orchestration with retries and a dead-letter queue → [23](23-idempotency-retries-and-error-handling.md).

## 2026 currency

Two forces are pulling in opposite directions and both are worth naming. **Headless 360** makes the platform far more reachable — every capability as an API, an MCP tool or a CLI command — which weakens the "we need middleware just to get at it" argument. Meanwhile **agent sprawl** creates a new governance problem at exactly the layer MuleSoft occupies, which is why Agent Fabric exists and why the boundary conversation now includes *which agents may call which tools*, not only which systems may call which APIs. The practical effect on a design review: the question moved from *"can we reach it"* to *"who is allowed to, and can we see that they did"*.

## Gotchas

- **"Use MuleSoft" is not an architecture.** Without the layer question answered, it relocates the mess rather than resolving it.
- **A licence you already own is not a reason.** MuleSoft entitlement is separate from Agentforce, and Agent Fabric's commercials are not public → confirm before scoping.
- **Middleware adds a failure domain.** Two systems that worked become three that can break, and the new one is the one nobody in the Salesforce team can debug at 2 a.m.
- **Point-to-point is defensible at small scale.** Two systems and one interface do not need a layered model; the cost of the model shows up before its benefit does.
- **Orchestration in Apex is the anti-pattern to name.** Chained Queueables coordinating three external systems is middleware written in the wrong language, in a runtime that will kill it.
- **The boundary is not permanent.** Volume grows, and the honest deliverable is the *trigger* for revisiting — a number, not an opinion.

## Recall

Q: What are the three API-led layers, and what distinguishes them?
A: System, process and experience — distinguished by rate of change: the source system, the business, and one consumer's UI.

Q: When does work belong off-platform?
A: When it fans out across systems, must survive Salesforce being unavailable, exceeds callout or CPU budgets, or needs orchestration with retries and a DLQ.

Q: What is the Apex-shaped anti-pattern this topic exists to name?
A: Chained Queueables orchestrating several external systems — middleware written in a runtime with governor limits.

Q: How does Headless 360 change the boundary argument?
A: It removes "we need middleware to reach the platform" as a reason, since every capability is an API, MCP tool or CLI command.

Q: What is the honest deliverable when point-to-point is good enough today?
A: The numeric trigger for revisiting the decision, not a permanent verdict.

## Related

- [01 · Integration patterns & selection](01-integration-patterns-and-selection.md) — the pattern taxonomy this boundary sits on top of
- [23 · Idempotency, retries & error handling](23-idempotency-retries-and-error-handling.md) — the properties middleware is bought for
- [AI_Data · MuleSoft Agent Fabric](../../AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md) — the same playbook applied to agents
- [22 · Event Relay & cloud eventing](22-event-relay-and-cloud-eventing.md) — moving events off-platform without middleware at all
