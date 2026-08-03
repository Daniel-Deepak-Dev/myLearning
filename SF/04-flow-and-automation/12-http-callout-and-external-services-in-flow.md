# HTTP Callout & External Services in Flow

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** Calling a REST API from Flow with no Apex — the HTTP Callout action, what External Services generates underneath, and where the boundary with Apex actually falls. Auth object modelling is [02-apex · 19](../02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md) and [13-integration](../06-integration-and-apis/INDEX.md).

## Core idea

*"Flow can't make callouts, so you need Apex"* stopped being true in Winter '24, and a surprising amount of integration advice has not caught up. The **HTTP Callout** action lets a flow author point at an endpoint, paste a sample response, and get a typed, reusable action back — no class, no test class, no deployment of code. What makes it more than a convenience is what it builds: Flow Builder generates an **External Service registration** and the Apex classes behind it, and the resulting invocable action is visible to every other flow, and to Agentforce, in the org. You are not embedding a callout in one flow; you are registering a capability. The judgement this note owes you is where that stops being enough — and the honest answer is that it stops at anything needing real retry logic, request signing, or a response shape the sample-based generator cannot infer.

## How it works

| Release | What became available |
|---|---|
| Spring '23 | HTTP Callout, **Beta**, `GET` only |
| **Summer '23** | `GET` **GA**, `POST` added |
| **Winter '24** | `POST`, `PUT`, `PATCH`, `DELETE` all **GA** |

- **Prerequisites are an external credential and a named credential**, plus the *Customize Application* permission to build the action. The named credential owns the base URL; the external credential owns the protocol and the principals. → [02-apex · 19](../02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md)
- **The response schema is inferred from a sample.** You paste a real response body and Flow Builder derives the data structure from it — which is fast, and is also the mechanism's main weakness.
- **Flow Builder generates an External Service registration, Apex classes and an invocable action** behind the scenes. The action is org-wide and reusable, not private to the flow that created it.
- **Response values are referenced as `{!ActionName.2XX.…}`**, with the status class in the path — the non-2XX branches are how you detect failure.
- **Nested and repeating JSON is where Transform earns its place** — flattening a callout response into a record collection is one of the cases Transform was built for. → [09](09-collections-loops-and-the-transform-element.md)

## 2026 currency

The capability is stable; what has changed around it is where callouts get *placed*. A record-triggered flow still cannot call out from the save transaction, so the callout belongs on an **asynchronous path** → [07](07-platform-event-and-async-path-flows.md), and since Summer '25 a **Screen Action** can make one while the user is still on the screen → [05](05-reactive-screen-flows.md), which is what makes live address validation and duplicate lookup practical without a component. The other 2026 context is authentication: **legacy named credentials are deprecated**, and the two-object model — external credential plus named credential — is the only one that can express *who* may call out via a permission set. A flow built on a legacy named credential inherits that problem. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **A record-triggered flow cannot call out from the save transaction.** Put it on an async path, or the element is simply unavailable.
- **The schema is inferred from one sample response.** A field absent from your sample does not exist as far as the action is concerned, and an optional field that arrives later is silently dropped.
- **Callouts count against the per-transaction callout limit** — 100 — and the total callout timeout of 120 seconds applies to the transaction, not to each call.
- **There is no retry.** A transient 503 is a fault path, nothing more; anything needing backoff belongs in Apex. → [02-apex · 19](../02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md)
- **You cannot do DML before a callout in the same transaction.** The uncommitted-work rule applies to Flow exactly as it does to Apex.
- **The generated Apex classes are real metadata.** They deploy, they show in the org, and deleting the action without cleaning them up leaves orphans. → [24 · Deployment & versioning](24-flow-deployment-versioning-and-governance.md)
- **Request signing, custom headers per call and multipart bodies are Apex territory.** If the API needs any of them, the declarative route ends.
- **A legacy named credential cannot express per-permission-set access.** Build on external credential + named credential.

## Recall

Q: From which release could a flow make every common HTTP verb call?
A: Winter '24 — `POST`, `PUT`, `PATCH` and `DELETE` all went GA there, after `GET` in Summer '23.

Q: What does Flow Builder actually generate when you create an HTTP Callout action?
A: An External Service registration, Apex classes and an invocable action that is reusable across the whole org.

Q: How is the response structure determined?
A: It is inferred from a sample response body you paste in — so any field missing from that sample does not exist to the action.

Q: Where must a callout go in a record-triggered flow?
A: On an asynchronous path, because the save transaction does not permit callouts.

Q: Name two things that push a callout back into Apex.
A: Retry with backoff, and request signing or custom per-call headers. Complex or variable response shapes are a third.

## Related

- [09 · Collections, loops & the Transform element](09-collections-loops-and-the-transform-element.md) — flattening a nested callout response into records
- [11 · Flow & Apex interop](11-flow-and-apex-interop.md) — the other side of the boundary, for when the declarative route runs out
- [02-apex · 19 Callouts & named credentials](../02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md) — the credential model both routes share, and why the legacy object is deprecated
