# MCP servers & agent-facing APIs

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** Exposing org capability to an AI client over the Model Context Protocol, and the security properties that make it defensible. The agent side — Agentforce, A2A, cross-vendor governance — is [AI_Data](../../AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md).

## Core idea

An MCP server is a **tool catalog with an authentication story**. A client — Claude, ChatGPT, Cursor, a custom agent — connects, discovers the tools the server publishes, and calls them. Salesforce hosts the servers, so there is no infrastructure to run and no bespoke integration to write.

What makes this different from wrapping the REST API yourself is the sentence that matters most in the whole feature: **the tools respect the org's full sharing and security model.** The 67.0 user-mode default is what makes that true rather than aspirational — an Apex action, an autolaunched flow or an Apex REST endpoint invoked as a tool enforces the calling user's object permissions, FLS and sharing by construction. You do not build the security layer; you inherit it.

## How it works

| Standard servers (GA) | What they expose |
|---|---|
| **SObject servers** | sObject CRUD, SOQL, search |
| **Data 360** | Data 360 queries and graph traversal |
| **Tableau** | analytics and visualization |

- **Setup is an External Client App** with the **`mcp_api`** and `refresh_token` scopes. `mcp_api` exists precisely so a client does not need `api`, which would grant the whole Platform API including Metadata and Tooling → [15](15-oauth-flows-and-authorization.md), [16](16-external-client-apps.md).
- **Servers are inactive by default.** An admin activates each one deliberately.
- **Custom servers** are built from **Apex actions** (`@InvocableMethod`), **autolaunched flows**, **Apex REST**, **`@AuraEnabled`** methods, the **Named Query API** (parameterized SOQL as a tool), **Prompt Builder** prompts, whole **Agentforce agents**, and the **API Catalog** → [18](18-apex-rest-and-custom-endpoints.md), [19](19-external-services-openapi-and-the-api-catalog.md).
- **The authorization code flow is enforced — there is no machine-to-machine option.** Every session is tied to a real user who authenticated. There is no service-account MCP client today, and no client credentials path.
- **Tightening happens on the ECA**: pre-authorize by profile or permission set, restrict IP ranges, shorten the refresh-token lifetime (default **one year**), revoke tokens.
- **Everything is logged.** Event Monitoring, filtered on `API_CLIENT_CATEGORY = SALESFORCE_HOSTED_MCP` → [24](24-api-limits-monitoring-and-access-control.md).

## 2026 currency

Standard and custom hosted servers are **GA**; the developer-facing servers around them are not — Salesforce DX MCP and Metadata API Context MCP are **Beta**, Data 360 MCP is **Developer Preview** → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md). The framing to carry into a design conversation is **Headless 360**: every capability reachable as an API, an MCP tool or a CLI command, by a human, an app or an autonomous agent. The honest limitation to state alongside it is the missing M2M flow — an unattended agent needs a user identity, so "the agent runs as a service account" is not currently an available answer.

## Gotchas

- **No machine-to-machine flow.** Anything unattended must borrow a real user's authenticated session, which is a governance question, not a configuration one.
- **Access cannot be scoped to a specific server at the ECA level** — the control granularity is the tool, not the server.
- **A one-year refresh token on a laptop-based MCP client is the actual risk surface.** Shorten it, and revoke on offboarding → [15](15-oauth-flows-and-authorization.md).
- **Servers are inactive by default**, so a correctly configured client fails with nothing wrong at its end.
- **A new external client app takes up to 30 minutes to work** → [16](16-external-client-apps.md).
- **Annotate destructive tools.** A tool that deletes should say so in its hints; a model choosing between similarly-named tools has only the description to go on.
- **An agent retries.** Exposing a non-idempotent action as a tool produces duplicate writes exactly the way retrying middleware does → [23](23-idempotency-retries-and-error-handling.md).

## Recall

Q: What single property makes org-hosted MCP tools safe to expose?
A: They run in the authenticated user's context — object permissions, FLS and sharing all apply, which the 67.0 user-mode default makes the norm rather than an opt-in.

Q: Why does the `mcp_api` scope exist?
A: So an MCP client is not granted `api`, which would carry the whole Platform API surface including Metadata and Tooling.

Q: Can an MCP client authenticate without a user?
A: No. Authorization code flow only — there is no machine-to-machine or service-account option.

Q: What can a custom MCP server's tools be built from?
A: Apex actions, autolaunched flows, Apex REST, `@AuraEnabled` methods, the Named Query API, Prompt Builder prompts, Agentforce agents and the API Catalog.

Q: How is MCP activity audited?
A: Event Monitoring, filtering `API_CLIENT_CATEGORY` on `SALESFORCE_HOSTED_MCP`.

## Related

- [16 · External Client Apps](16-external-client-apps.md) — the prerequisite, not an alternative
- [18 · Apex REST & custom endpoints](18-apex-rest-and-custom-endpoints.md) — the endpoint a tool is often made of
- [19 · External Services, OpenAPI & the API Catalog](19-external-services-openapi-and-the-api-catalog.md) — the registration path from Apex to agent action
- [AI_Data · Agent Fabric & cross-vendor interop](../../AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md) — governing MCP traffic across vendors
