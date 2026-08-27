# ApexGuru & Performance Review

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 17

**Scope:** Finding the Apex that is actually slow in *this* org, and the entitlement wall in front of that. Static rules are [16](16-code-analyzer-v5.md); the language-level tuning is [02-apex · 24](../02-apex-and-triggers/24-apex-performance-and-profiling.md).

## Core idea

Static analysis flags what *looks* expensive. ApexGuru flags what *is* expensive, because it reads your org's **runtime metrics** — real execution counts, real CPU time, real query costs — and ranks anti-patterns by the harm they are doing rather than by rule severity. A SOQL-in-a-loop in a class that runs twice a month and one in a trigger that runs 400,000 times a day are the same finding to PMD and completely different problems to a release manager.

It is packaged as a feature of **Scale Center**, Salesforce's performance-monitoring product, and that packaging is the first thing to know about it — see the entitlement gotcha below, because it decides whether this note is actionable for a given client at all.

## How it works

- **Enable it once:** Setup → **Scale Center** → **ApexGuru** tab → accept the agreement. **Reports appear within about 24 hours**, not immediately, because it needs a window of runtime telemetry first.
- **It reports insights, not violations** — hotspots ranked by observed impact, each with the anti-pattern named and a suggested remediation.
- **The catalogue is the expensive-at-scale list**: SOQL and DML inside loops, redundant or repeated SOQL, unselective queries, unnecessary work in a trigger path.
- **Test Case Insights** surfaces inefficient *tests* — the ones quietly adding minutes to every validation and therefore to every release window → [15](15-apex-test-strategy-in-ci.md).
- **Analysis runs through the Einstein Trust Layer** with masking and zero data retention, using a Salesforce-owned model. That is the answer to the security question a client will ask before enabling it.
- **It is also an MCP tool.** The **Salesforce DX MCP Server (Beta)** exposes ApexGuru, so a coding agent in the editor can review a class against the org's own runtime data → [22](22-agentforce-dx-and-ai-assisted-development.md).

## 2026 currency

The MCP surface is the change worth noticing, and it is a change of *workflow* rather than of capability. ApexGuru has been GA since **February 2024**; what 2026 added is reaching it from the inner loop — the developer sees the org's runtime verdict while writing the class, instead of a release manager seeing it in a report six weeks later. Pair it with the two Summer '26 facts that move Apex cost around: **user-mode SOQL evaluates sharing**, so a query's cost now depends on who runs it, and **elastic async limits (Beta)** convert some runaway-chain failures into throttling, which turns a loud error into a quiet delay → [02-apex · 24](../02-apex-and-triggers/24-apex-performance-and-profiling.md).

## Gotchas

- **Most orgs cannot use it, and this is the headline.** It comes with **Scale Center** — Unlimited Edition production orgs and full-copy sandboxes, Signature Success customers, and Scale Test customers. It is **not supported on Government Cloud Plus.** Confirm entitlement before you put it in a proposal.
- **It analyses production traffic**, so a finding in a sandbox with no load is meaningless. The sandbox use is validating a fix, not finding the problem.
- **Nothing appears on day one.** The 24-hour delay is routinely mistaken for a failed enablement.
- **Ranked by impact means quiet code stays invisible** — a genuinely awful class that barely executes will never surface here. Static analysis still owns that half → [16](16-code-analyzer-v5.md).
- **Suggested remediations are suggestions.** They are generated against the pattern, not against your business logic, and a bulkification rewrite can change transaction semantics.
- **It sees Apex.** A slow Flow, an unselective report or a badly-shaped object are elsewhere → [04-flow · 13](../04-flow-and-automation/13-flow-limits-and-bulkification.md), [08-data · 09](../08-data-modeling-and-large-data-volumes/09-query-plan-and-performance-tuning.md).
- **"Insight closed" is not "regression prevented."** Nothing stops the pattern coming back next sprint unless the equivalent static rule is also in the gate.

## Recall

Q: What does ApexGuru have that a static analyser structurally cannot?
A: Your org's runtime metrics — so findings are ranked by observed execution cost, not by rule severity.

Q: Which orgs actually have it?
A: Scale Center customers — UE production and full-copy sandboxes, Signature Success and Scale Test — and **not** Government Cloud Plus.

Q: Why is there nothing to look at right after enabling it?
A: It needs a telemetry window; reports appear within roughly 24 hours.

Q: What do Test Case Insights identify, and why does a release manager care?
A: Inefficient Apex tests — they lengthen every validation, and validation is the release window.

Q: How is it reached from an editor in 2026?
A: Through the Salesforce DX MCP Server (Beta), which exposes ApexGuru as a tool to a coding agent.

## Related

- [16 · Code Analyzer v5](16-code-analyzer-v5.md) — the static half, which catches what never runs
- [15 · Apex test strategy in CI](15-apex-test-strategy-in-ci.md) — where Test Case Insights get spent
- [02-apex · 24 Apex performance & profiling](../02-apex-and-triggers/24-apex-performance-and-profiling.md) — the limits and language-level tuning behind each finding
- [21 · Observability, logging & prod debugging](21-observability-logging-and-prod-debugging.md) — what to do when the problem is not in Apex at all
