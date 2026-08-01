# Phases for 06 · Integration & APIs

23 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs after security (phases 10–11).** OAuth, named credentials and API access control all rest on the access model.
> Currency anchor for this area: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

---

## Phase 12 — APIs: REST → legacy streaming · 12 files ⬜

```
01-integration-patterns-and-selection.md
02-api-versions-and-the-retirement-treadmill.md    🆕⚠️
03-rest-api-fundamentals.md
04-soap-api-and-where-it-persists.md
05-composite-batch-and-graph-apis.md
06-bulk-api-2.md                                   ⚠️
07-ui-api-and-metadata-aware-clients.md
08-graphql-api.md                                  🆕
09-pub-sub-api.md                                  🆕⚠️
10-platform-event-design.md
11-change-data-capture.md
12-legacy-streaming-and-outbound-messaging.md      ⚠️
```

**⚠️ corrections to lead with**
- **02** — old API versions are **actively retired**, not merely deprecated. "It works on v39" is a countdown, not a steady state. **Get the current retirement list from a source; do not assert version numbers from memory.**
- **06** — **Bulk API 2.0** is the default. v1's manual batch-splitting model is legacy; PK chunking behaves differently.
- **09** — **Pub/Sub API (gRPC) replaced CometD.** This is the single biggest change in the area.
- **12** — covers what's retired (CometD generic/push topics, outbound messaging's diminishing role) and the migration path. This note exists *to be* the correction; the others just link here.

**🆕 — research before writing:** **02**, **08** (GraphQL API — distinct from the LWC wire adapter in [03-lwc · 07](../03-lwc-and-slds/INDEX.md); this is the external-client surface), **09**.

**Notes on scope**
- **01** is the decision framework the other 22 hang off. Keep it a table.
- **04** — be honest about **where SOAP persists**: Metadata API, some partner tooling. Not "SOAP is dead."
- **05** — the useful content is **transaction boundaries**: what rolls back together in a composite tree vs a graph.

**Seed harvest** ([../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md)) — `SF - Integration Patterns and Practices` (**2026-02**) is likely the most current page in the entire corpus; **read it before writing 01**. `CometD` (2025) → **09**/**12** as the "what changed" hook. `Change data capture` + `lightning/empApi - Change Data Capture` (2023) → **11**. `SOAP API` (2019) → **04**, structure only.

---

## Phase 13 — Auth, external apps & agent-facing integration · 11 files ⬜

```
13-oauth-flows-and-authorization.md                ⚠️
14-external-client-apps.md                         🆕⚠️
15-named-credentials-and-external-credentials.md   ⚠️
16-apex-rest-and-custom-endpoints.md
17-external-services-and-openapi.md
18-salesforce-connect-and-external-objects.md
19-mulesoft-and-api-led-boundaries.md
20-event-relay-and-cloud-eventing.md               🆕
21-idempotency-retries-and-error-handling.md
22-api-limits-monitoring-and-access-control.md
23-mcp-servers-and-agent-facing-apis.md            🆕
```

**⚠️ corrections to lead with**
- **13** — the **username-password OAuth flow is blocked** by default. JWT bearer and client credentials are the server-to-server answers. Tutorials still teach the blocked flow constantly.
- **14** — **External Client Apps supersede Connected Apps** for new integrations. State precisely what still requires a Connected App.
- **15** — the **new** Named Credential model splits External Credential (auth) from Named Credential (endpoint), with named principals. Older guidance describes a single combined object.

**🆕 — research before writing:** **14**, **20** (Event Relay → AWS EventBridge), **23**.

**Notes on scope**
- **16, 23** must reflect **user mode by default** ([02-apex · 10](../02-apex-and-triggers/INDEX.md)) — an agent-callable endpoint enforces the running user unless it opts out. This is the security property that makes org-hosted MCP tools safe; say it once, here.
- **19** — the value is the **boundary judgment** (what belongs off-platform), not MuleSoft product detail.
- **21** — has no Salesforce-specific docs page; it's the distributed-systems layer that integration reviews actually fail on. Worth writing carefully.

**Cross-links** — **23** → [AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md](../../AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md). **18** → [08-data · 13](../08-data-modeling-and-large-data-volumes/INDEX.md).

**Seed harvest** — `Apex REST Callouts` and `Apex Rest Web Services` (2021) → **16**, structure only.
