# 06 · Integration & APIs

Every inbound and outbound path, with the 2024–2026 replacements. **23 topics** · phases [12](PHASES.md), [13](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **Three replacements to internalise:** **Pub/Sub API (gRPC) replaced CometD streaming**; **External Client Apps** supersede Connected Apps for new integrations; **Bulk API 2.0** is the default, v1 is legacy. Also: old API versions are being **actively retired**, so "it works on v39" is a ticking clock, not a stable state.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | Integration patterns & selection | request-reply, fire-and-forget, batch, pub/sub | 12 |
| 02 | API versions & the retirement treadmill 🆕⚠️ | API 67.0 current; legacy versions actively retired | 12 |
| 03 | REST API fundamentals | sObject CRUD, query, describe, limits headers | 12 |
| 04 | SOAP API & where it persists | enterprise vs partner WSDL, Metadata API SOAP | 12 |
| 05 | Composite, Batch & Graph APIs | composite trees, graphs, transaction boundaries | 12 |
| 06 | Bulk API 2.0 ⚠️ | v2 ingest/query jobs; v1 legacy, PK chunking | 12 |
| 07 | UI API & metadata-aware clients | record/layout/lookup endpoints for custom clients | 12 |
| 08 | GraphQL API 🆕 | schema shape, filters, aggregates, cost vs REST | 12 |
| 09 | Pub/Sub API 🆕⚠️ | gRPC replaces CometD; replay IDs, managed subscriptions | 12 |
| 10 | Platform Event design | high-volume events, delivery guarantees, publish behaviour | 12 |
| 11 | Change Data Capture | channels, enrichment fields, downstream replication | 12 |
| 12 | Legacy streaming & outbound messaging ⚠️ | what's retired and the migration path off it | 12 |
| 13 | OAuth flows & authorization ⚠️ | JWT bearer, client credentials; username-password blocked | 13 |
| 14 | External Client Apps 🆕⚠️ | successor to Connected Apps for new integrations | 13 |
| 15 | Named Credentials & External Credentials ⚠️ | principals, per-user auth, legacy vs new model | 13 |
| 16 | Apex REST & custom endpoints | `@RestResource`, versioning, agent-callable endpoints | 13 |
| 17 | External Services & OpenAPI | spec registration, generated invocable actions | 13 |
| 18 | Salesforce Connect & external objects | OData/custom adapters, indirect lookups, limits | 13 |
| 19 | MuleSoft & API-led boundaries | when logic belongs off-platform, layering | 13 |
| 20 | Event Relay & cloud eventing 🆕 | relay to AWS EventBridge, hybrid event architectures | 13 |
| 21 | Idempotency, retries & error handling | dedupe keys, DLQ, replay-safe consumers | 13 |
| 22 | API limits, monitoring & access control | request limits, API Access Control, Event Monitoring | 13 |
| 23 | MCP servers & agent-facing APIs 🆕 | org-hosted MCP tools honouring sharing and user mode | 13 |

## Related

- **13–15** depend on [07-security-and-sharing](../07-security-and-sharing/INDEX.md) — that's why phases 10–11 run first.
- **16, 23** depend on [02-apex · 10 user mode](../02-apex-and-triggers/INDEX.md): an agent-callable endpoint now enforces the running user by default.
- **18** pairs with [08-data · 13 External objects vs replicated copies](../08-data-modeling-and-large-data-volumes/INDEX.md).
- **23** continues in [AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md](../../AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md).
- Currency anchor: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).
