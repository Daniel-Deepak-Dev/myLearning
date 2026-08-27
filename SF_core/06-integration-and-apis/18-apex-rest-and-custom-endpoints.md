# Apex REST & custom endpoints

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** Publishing your own inbound HTTP endpoint from Apex, and what it becomes once published. Standard REST is [04](04-rest-api-fundamentals.md); the OpenAPI document and catalog registration are [19](19-external-services-openapi-and-the-api-catalog.md); exposure to agents is [25](25-mcp-servers-and-agent-facing-apis.md).

## Core idea

Standard REST gives a caller sObjects. Apex REST gives them a **verb in your domain language** — `POST /orders/submit` instead of three composite subrequests and a client that knows your schema. That is the real reason to write one: it moves the transaction boundary and the business rules inside the org, so the caller cannot half-complete a workflow.

The cost is that you now own an API contract. A custom endpoint has no version negotiation of its own beyond the URL you chose, no describe call, and no automatic backward compatibility. Everything standard REST gives for free, you re-create by hand.

## How it works

- **`@RestResource(urlMapping='/orders/*')`** on a global class, with `@HttpGet`, `@HttpPost`, `@HttpPatch`, `@HttpPut`, `@HttpDelete` on global static methods — **one method per verb per class**.
- The endpoint lives at **`/services/apexrest/`** plus your mapping, and a wildcard segment is read from `RestContext.request.requestURI`.
- **Parameters bind from the request body by name** for JSON; return a type and the platform serializes it. `RestContext.response` is there when you need to set a status code or write raw bytes.
- **User mode is the default at API 67.0.** The endpoint enforces the calling user's object permissions, FLS and sharing unless the class deliberately opts out — which is what makes a custom endpoint safe to expose to an agent → [02-apex · 10](../02-apex-and-triggers/INDEX.md).
- **Access is granted by permission set**, via *Apex Class Access*. Deploying the class does not publish it to anyone.
- **It is a first-class agent tool source.** Apex REST is one of the documented ways to build a hosted MCP tool, and its operations can become agent actions once catalogued → [19](19-external-services-openapi-and-the-api-catalog.md).

```apex
@RestResource(urlMapping='/orders/*')
global with sharing class OrderApi {
    @HttpPost
    global static Id submit(String accountId, List<LineItem> lines) {
        // runs in user mode at 67.0 — the caller's sharing and FLS apply
        return OrderService.submit(accountId, lines);
    }
}
```

> **From my notes.** The 2021 pages `Apex REST Callouts` and `Apex Rest Web Services` are structure only — annotations and a worked example, no prose. Two things they predate and would now get wrong: the security context is **user mode by default**, so their examples' implicit system-mode assumption is inverted; and a published endpoint is no longer only for middleware — it is a candidate agent action.

## 2026 currency

The interesting change is not in the annotations, which are stable, but in what happens **after** you deploy one. An Apex REST class can have an OpenAPI 3.0 document generated for it, be registered in the **API Catalog**, and have its operations surfaced as **agent actions** or as tools on a **custom MCP server** — all without a line of integration code → [19](19-external-services-openapi-and-the-api-catalog.md), [25](25-mcp-servers-and-agent-facing-apis.md). Combined with the 67.0 user-mode default, that is the whole *Headless 360* premise: the same endpoint serves middleware and an autonomous caller, with sharing enforced identically for both.

## Gotchas

- **`global`, not `public`** — on the class and on every exposed method, or the endpoint silently does not exist.
- **One method per HTTP verb per class.** Two `@HttpPost` methods is a compile error, so overloading a resource means a new class or a dispatch parameter.
- **You own versioning.** There is no `/v67.0/` for `/services/apexrest/`; put the version in the URL mapping from day one or you will break callers to add it later.
- **Unhandled exceptions return HTTP 500 with an Apex stack trace** in the body — a leak and a useless message. Catch and map to real status codes.
- **User mode means partial data, not an error.** A caller without FLS on a field gets the record with the field missing, and a naive client reads it as null.
- **Apex Class Access is the whole authorization.** Granting it via a profile or permission set is what publishes the endpoint — deployment alone reaches nobody.

## Recall

Q: What makes a custom endpoint worth writing instead of using standard REST?
A: It exposes a domain verb and keeps the transaction boundary and business rules inside the org, so a caller cannot half-complete a workflow.

Q: What security context does an Apex REST method run in at API 67.0?
A: User mode by default — the caller's object permissions, FLS and sharing apply unless the class opts out.

Q: What are the two `global` requirements?
A: The class and every exposed method must be `global`, or the endpoint does not exist.

Q: How do you version an Apex REST endpoint?
A: Yourself, in the `urlMapping`. There is no platform version negotiation for `/services/apexrest/`.

Q: What can a deployed Apex REST class become without extra integration code?
A: An OpenAPI document in the API Catalog, an agent action, and a tool on a custom MCP server.

## Related

- [19 · External Services, OpenAPI & the API Catalog](19-external-services-openapi-and-the-api-catalog.md) — what registration turns this into
- [25 · MCP servers & agent-facing APIs](25-mcp-servers-and-agent-facing-apis.md) — the same endpoint, reached by an agent
- [23 · Idempotency, retries & error handling](23-idempotency-retries-and-error-handling.md) — what a caller does when your `POST` times out
- [04 · REST API fundamentals](04-rest-api-fundamentals.md) — the standard surface this sits beside
