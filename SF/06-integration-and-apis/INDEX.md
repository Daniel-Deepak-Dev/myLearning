# 06 · Integration & APIs

Every inbound and outbound path, with the 2024–2026 replacements. **26 topics** · phases [12](PHASES.md), [13](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **Three changes to internalise, stated at their real strength.** **Bulk API 2.0** is the default; v1 is legacy but callable. **External Client Apps** supersede Connected Apps for new integrations — connected-app *creation* is Support-gated since Spring '26, while existing ones keep working ([16](16-external-client-apps.md)). **Pub/Sub API is the recommended transport for new event subscribers** — but it **retired nothing**: Streaming API, CometD and Bayeux have **no published end-of-life**, and only *PushTopic* and *generic* events carry the docs' *(Legacy)* label ([14](14-legacy-streaming-and-outbound-messaging.md)).
>
> 🕐 **The dated ones — four clocks, all running.** **Instanced hostnames (`na45.salesforce.com`) stop being supported for API traffic with Winter '27** — sandboxes from **August 2026**, production from **September 2026** ([03](03-api-endpoints-hostnames-and-edge-network.md)). The **OAuth username-password flow retires in Winter '27** and **SOAP `login()` for API 31.0–64.0 in Summer '27** ([15](15-oauth-flows-and-authorization.md), [05](05-soap-api-and-where-it-persists.md)). **Maximum certificate validity drops to 100 days on 15 March 2027** and 47 days in 2029 ([26](26-certificates-mutual-tls-and-the-pki-changes.md)). And a retired API version returns **HTTP 410 GONE** rather than degrading ([02](02-api-versions-and-the-retirement-treadmill.md)).

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | [Integration patterns & selection](01-integration-patterns-and-selection.md) | request-reply, fire-and-forget, batch, pub/sub | 12 |
| 02 | [API versions & the retirement treadmill](02-api-versions-and-the-retirement-treadmill.md) 🆕⚠️ | API 67.0 current; retired versions return 410 GONE | 12 |
| 03 | [API endpoints, hostnames & Edge Network](03-api-endpoints-hostnames-and-edge-network.md) 🆕⚠️ | My Domain hosts, instanced-URL end of support, CORS/CSP | 12 |
| 04 | [REST API fundamentals](04-rest-api-fundamentals.md) | sObject CRUD, query, describe, limits headers | 12 |
| 05 | [SOAP API & where it persists](05-soap-api-and-where-it-persists.md) | enterprise vs partner WSDL; `login()` retiring, API is not | 12 |
| 06 | [Composite, Batch & Graph APIs](06-composite-batch-and-graph-apis.md) | 25 subrequests, 500-node graphs, transaction boundaries | 12 |
| 07 | [Bulk API 2.0](07-bulk-api-2.md) ⚠️ | v2 ingest/query jobs; v1 legacy, PK chunking differs | 12 |
| 08 | [UI API & metadata-aware clients](08-ui-api-and-metadata-aware-clients.md) | record/layout/lookup endpoints; 67.0 CSRF resource | 12 |
| 09 | [Metadata, Tooling & Connect APIs](09-metadata-tooling-and-connect-apis.md) 🆕 | the org-administration surface every pipeline runs on | 12 |
| 10 | [GraphQL API](10-graphql-api.md) 🆕 | schema shape, filters, aggregates, 67.0 mutation chaining | 12 |
| 11 | [Pub/Sub API](11-pub-sub-api.md) 🆕⚠️ | gRPC, Avro, replay IDs, flow control, managed subscriptions | 12 |
| 12 | [Platform Event design](12-platform-event-design.md) | payload as contract, publish behaviour, delivery guarantees | 12 |
| 13 | [Change Data Capture](13-change-data-capture.md) | channels, `ChangeEventHeader`, enrichment fields | 12 |
| 14 | [Legacy streaming & outbound messaging](14-legacy-streaming-and-outbound-messaging.md) ⚠️ | what is actually legacy, what is not, and the migration path | 12 |
| 15 | [OAuth flows & authorization](15-oauth-flows-and-authorization.md) ⚠️ | JWT bearer, client credentials, `mcp_api`; username-password retiring | 13 |
| 16 | [External Client Apps](16-external-client-apps.md) 🆕⚠️ | successor to Connected Apps; creation Support-gated since Spring '26 | 13 |
| 17 | [Named Credentials & External Credentials](17-named-credentials-and-external-credentials.md) ⚠️ | principals, per-user auth, legacy deprecated with **no date** | 13 |
| 18 | [Apex REST & custom endpoints](18-apex-rest-and-custom-endpoints.md) | `@RestResource`, versioning, user mode, agent-callable endpoints | 13 |
| 19 | [External Services, OpenAPI & the API Catalog](19-external-services-openapi-and-the-api-catalog.md) | spec registration outbound; Apex REST → agent action inbound | 13 |
| 20 | [Salesforce Connect & external objects](20-salesforce-connect-and-external-objects.md) | OData/custom adapters, indirect lookups, limits lifted on Hyperforce | 13 |
| 21 | [MuleSoft & API-led boundaries](21-mulesoft-and-api-led-boundaries.md) | when logic belongs off-platform, layering | 13 |
| 22 | [Event Relay & cloud eventing](22-event-relay-and-cloud-eventing.md) 🆕 | relay to Amazon EventBridge — the only destination | 13 |
| 23 | [Idempotency, retries & error handling](23-idempotency-retries-and-error-handling.md) | dedupe keys, DLQ, replay-safe consumers | 13 |
| 24 | [API limits, monitoring & access control](24-api-limits-monitoring-and-access-control.md) | request limits, API Access Control, Event Monitoring | 13 |
| 25 | [MCP servers & agent-facing APIs](25-mcp-servers-and-agent-facing-apis.md) 🆕 | org-hosted MCP tools honouring sharing and user mode; **no M2M flow** | 13 |
| 26 | [Certificates, mutual TLS & the PKI changes](26-certificates-mutual-tls-and-the-pki-changes.md) 🆕⚠️ | dual-use roots banned, validity 200 → 100 → 47 days, stop pinning | 13 |

## Related

- **15–17, 26** depend on [07-security-and-sharing](../07-security-and-sharing/INDEX.md) — that's why phases 10–11 run first.
- **18, 25** depend on [02-apex · 10 user mode](../02-apex-and-triggers/INDEX.md): an agent-callable endpoint now enforces the running user by default.
- **16 → 25** is a hard dependency, not a cross-reference: an external client app is the only documented way to connect an MCP client.
- **18 → 19 → 25** is one pipeline: an Apex REST class becomes an OpenAPI document, a catalog entry, then an agent action or MCP tool.
- **09** underpins [09-devops](../09-devops-sfdx-and-release-management/INDEX.md) — every pipeline is a Metadata API client.
- **20** pairs with [08-data · 17 External objects vs replicated copies](../08-data-modeling-and-large-data-volumes/17-external-objects-vs-replicated-copies.md) — this note owns the adapters, that one owns the copy-or-federate decision.
- **25** continues in [AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md](../../AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md).
- Currency anchor: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).
