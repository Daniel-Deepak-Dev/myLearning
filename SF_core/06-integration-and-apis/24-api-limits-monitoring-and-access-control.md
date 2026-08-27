# API limits, monitoring & access control

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** The org's API allowance, who is allowed to spend it, and how to see what did. This is the note [01](01-integration-patterns-and-selection.md), [04](04-rest-api-fundamentals.md), [06](06-composite-batch-and-graph-apis.md), [07](07-bulk-api-2.md) and [12](12-platform-event-design.md) all defer to.

## Core idea

The API allowance is **per org, per rolling 24 hours**, sized by edition and licence count — not per user and not per integration. That makes it a shared resource with no internal accounting: one badly written client can exhaust it for everyone, and the symptom is that *other* integrations start failing.

Access control is the other half. Authentication says who you are ([15](15-oauth-flows-and-authorization.md)); this decides which apps may connect at all, from where, and what the org can prove about it afterwards.

## How it works

- **`REQUEST_LIMIT_EXCEEDED` is the org-wide 24-hour allowance.** Bulk API 2.0 has its own separate allowance, which is a reason to move volume there rather than an excuse to ignore the limit.
- **`Sforce-Limit-Info` comes back on every REST response** — `api-usage=12345/100000`. A client that reads it can throttle itself; almost none do.
- **`/services/data/vXX.0/limits`** and `System.OrgLimits.getMap()` in Apex expose every allowance, including `DailyApiRequests`.
- **Concurrency is a separate ceiling.** Long-running synchronous requests are capped concurrently, so a slow query issued in parallel blocks the org while the 24-hour count still looks healthy.
- **API Access Control** (Setup) turns the org into an **allowlist**: only installed and approved connected apps and external client apps may call the API. It is off by default, and turning it on breaks every unapproved client immediately — which is the point, and the reason to inventory first.
- **The identity spending the allowance is a design choice.** A free **Salesforce Integration** licence — API-only, no UI login — keeps integration traffic attributable and out of a named employee's account → [15](15-oauth-flows-and-authorization.md).

## 2026 currency

Two changes and one new audit surface. **Connect REST API moved off its per-user/per-app/per-hour throttle** onto the org's 24-hour Platform API limit — only Chatter-requiring requests keep an hourly cap, and the same applies to Connect in Apex, so designs built around the old ceiling can be simplified → [09](09-metadata-tooling-and-connect-apis.md). **Event Monitoring has a free tier** in Enterprise, Unlimited and Performance orgs — about seven log types at one day of retention, including **API Total Usage** and **Hostname Redirects**, the latter being exactly the inventory tool for integrations still calling instanced hostnames before the Winter '27 deadline → [03](03-api-endpoints-hostnames-and-edge-network.md), [02](02-api-versions-and-the-retirement-treadmill.md). And hosted MCP traffic is auditable: filter Event Monitoring on **`API_CLIENT_CATEGORY = SALESFORCE_HOSTED_MCP`** → [25](25-mcp-servers-and-agent-facing-apis.md).

## Gotchas

- **The limit is rolling, not midnight-reset.** A load that ran at 3 a.m. is still counted at 2 a.m. the next day, so "it resets overnight" is wrong by hours.
- **Exceeding it takes down the integrations that behaved.** The failure lands on whoever calls next, not on the client that spent the allowance.
- **`API Total Usage` at one day of retention is not a trend.** Free-tier logs must be extracted daily to be useful for capacity planning.
- **Turning on API Access Control without an inventory is an outage.** Start from Connected Apps OAuth Usage → [16](16-external-client-apps.md).
- **Named users spending the allowance hide the culprit.** Traffic attributed to an admin's account is indistinguishable from that admin working.
- **A composite call is one API request, not 25.** Counting requests at the wrong granularity produces capacity plans that are wrong by an order of magnitude → [06](06-composite-batch-and-graph-apis.md).

## Recall

Q: What is the scope and period of the main API allowance?
A: Per org, per rolling 24 hours, sized by edition and licence count.

Q: Which response header lets a client self-throttle?
A: `Sforce-Limit-Info`, e.g. `api-usage=12345/100000`.

Q: What does API Access Control do?
A: Restricts API access to installed and approved apps — an org-wide allowlist, off by default.

Q: Which free Event Monitoring log type finds integrations still on instanced hostnames?
A: Hostname Redirects.

Q: How do you audit hosted MCP traffic?
A: Event Monitoring, filtering on `API_CLIENT_CATEGORY = SALESFORCE_HOSTED_MCP`.

## Related

- [15 · OAuth flows & authorization](15-oauth-flows-and-authorization.md) — the identity spending the allowance
- [16 · External Client Apps](16-external-client-apps.md) — what the allowlist allows
- [23 · Idempotency, retries & error handling](23-idempotency-retries-and-error-handling.md) — which limit errors are worth retrying
- [07-security · 23 Event Monitoring & Transaction Security](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md) — the monitoring platform itself
