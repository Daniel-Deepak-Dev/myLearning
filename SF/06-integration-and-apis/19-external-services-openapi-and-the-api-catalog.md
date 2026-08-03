# External Services, OpenAPI & the API Catalog

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** Turning an API specification into something Salesforce can call or expose — outbound via External Services, inbound via the API Catalog. Flow's HTTP Callout is [04-flow · 12](../04-flow-and-automation/12-http-callout-and-external-services-in-flow.md); the endpoints being described are [18](18-apex-rest-and-custom-endpoints.md).

## Core idea

Both halves of this topic do the same trick in opposite directions: **a schema document becomes callable metadata.** External Services takes someone else's OpenAPI spec and generates Apex classes plus an org-wide invocable action, so a flow can call a third-party API without code. The API Catalog takes *your* Apex REST classes, generates OpenAPI documents for them, and registers those so an agent can call them.

The point of both is that the spec is the contract. Nothing is hand-written, so the action and the API cannot drift — and when they do drift, you re-register rather than debug.

## How it works

**Outbound — External Services**

- Register a **named credential** ([17](17-named-credentials-and-external-credentials.md)) plus an OpenAPI spec. **OpenAPI 2.0 and 3.0** are supported; parameters, requests and responses become the action's inputs and outputs.
- Registration generates an **`ExternalServiceRegistration`**, Apex classes and an invocable action available to **every** flow and to Agentforce.
- Flow's **HTTP Callout** is this machinery with a friendlier front end: it infers the schema from **one pasted sample response**, which is its main weakness — a field absent from the sample does not exist to the action.

**Inbound — the API Catalog**

- Deploy an Apex class that defines a REST resource and its **OpenAPI document and metadata are added to the API Catalog**; the methods become available as agent actions.
- **Extension fields in the OpenAPI document control that exposure** — the API's owner decides how it is presented to agents, rather than someone reconstructing it in Agent Studio.
- A **topic** can be declared in the OpenAPI document via MuleSoft Topic Center and is created in Agentforce on registration.
- The catalog is also a documented tool source for **custom MCP servers** → [25](25-mcp-servers-and-agent-facing-apis.md).

## 2026 currency

The inbound half is new and it is the piece that makes phase 13's agent story coherent: **Apex REST → OpenAPI document → API Catalog → agent action or MCP tool**, with the 67.0 user-mode default carrying the security all the way through. Generation of the OpenAPI document is AI-assisted through the Agentforce Vibes extension and parts of the pipeline are still **Beta** — check status before designing on it. Outbound, External Services is stable and unglamorous; its 2026 relevance is that it is how a *flow* reaches a third-party API, which is why [04-flow · 12](../04-flow-and-automation/12-http-callout-and-external-services-in-flow.md) exists.

## Gotchas

- **A schema inferred from one sample is a schema with holes.** Anything the sample omitted — an optional field, an error shape, a nullable — is invisible to the generated action forever.
- **Re-registering does not silently update consumers.** Flows bound to the old action keep the old shape, so a changed spec means finding every consumer.
- **OpenAPI support is a subset.** Deeply nested schemas, `oneOf`/`anyOf` and unusual types fail at registration with messages that name the JSON path and not the problem.
- **The named credential must exist first.** External Services has no place to put an endpoint or a secret of its own.
- **An operation exposed to agents is an operation exposed to anyone the agent serves.** Extension fields are a publishing decision, not a security control — permissions still come from Apex Class Access and user mode.
- **Beta means Beta.** Do not put an AI-generated OpenAPI document into a production contract without reading it line by line.

## Recall

Q: What does registering an External Service generate?
A: An `ExternalServiceRegistration`, Apex classes, and an invocable action available to every flow and to Agentforce.

Q: What is the weakness of Flow HTTP Callout's schema handling?
A: It infers the response schema from a single pasted sample, so anything absent from that sample does not exist to the action.

Q: What happens to an Apex REST class's OpenAPI document when you deploy it?
A: It is added to the API Catalog and its methods become available as agent actions.

Q: What controls how a catalogued API is presented to agents?
A: Extension fields in the OpenAPI document, set by the API's owner.

Q: Which OpenAPI versions does External Services support?
A: 2.0 and 3.0.

## Related

- [18 · Apex REST & custom endpoints](18-apex-rest-and-custom-endpoints.md) — where a catalogued API comes from
- [25 · MCP servers & agent-facing APIs](25-mcp-servers-and-agent-facing-apis.md) — the catalog as a tool source
- [17 · Named Credentials & External Credentials](17-named-credentials-and-external-credentials.md) — the prerequisite for any outbound registration
- [04-flow · 12 HTTP Callout & External Services in Flow](../04-flow-and-automation/12-http-callout-and-external-services-in-flow.md) — the same machinery, from Flow Builder
