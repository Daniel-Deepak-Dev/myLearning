---
vault: SF_core
area: 06-integration-and-apis
format: dense
status: learning
created: 2026-08-03
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 12
tags: [currency-new]
---
# GraphQL API

**Scope:** The standalone GraphQL endpoint for **external clients**. The in-component wire adapter is a different, narrower thing — [03-lwc · 07](../03-lwc-and-slds/07-graphql-wire-adapter.md) — and the two diverge on features, so keep them apart.

## Core idea

REST returns whatever a resource returns; the client discards the rest and makes another call for what was missing. GraphQL inverts that: the client declares the exact shape it wants — fields, related records, several unrelated objects — and receives precisely that in one round trip. For a mobile or headless client on a slow connection, that is the difference between six requests and one.

The Salesforce implementation is built **on UI API**, which has a consequence people miss: it inherits UI API's semantics, so FLS and sharing are applied and the schema exposed is the org's own, generated from its metadata. It is not a generic database query language bolted onto Salesforce — it is a query language over the same metadata-aware layer as [08](08-ui-api-and-metadata-aware-clients.md).

## How it works

- **One endpoint, one verb:** `POST /services/data/v68.0/graphql`. Versioning still lives in the path → [02](02-api-versions-and-the-retirement-treadmill.md).
- **The schema is your org's**, discoverable by introspection — so a client tool can autocomplete against custom objects and fields with no configuration.
- **Records come back through a connection shape** — `edges` → `node` → field → `value` — which is verbose to read but is what carries pagination cursors and per-field metadata.
- **Filtering, sorting, pagination and aggregates** are all query arguments rather than separate resources.
- **Several unrelated objects in one query** is the headline capability, and the one that replaces a composite request for read-heavy work → [06](06-composite-batch-and-graph-apis.md).
- **`X-Chatter-Entity-Encoding: false`** is required for correct encoding of returned text.
- **Authentication is ordinary OAuth**, and Salesforce's guidance is to use an External Client App for production clients → [16](INDEX.md).

## 2026 currency

**Mutation chaining is the Summer '26 addition, and it landed in the API — not in the LWC wire adapter.** A mutation can now reference **any field** returned by an earlier operation in the same request, not merely its record ID: `@{ref.Record.FieldName.value}` for a field value, `@{ref.Record.Id}` (shorthand `@{ref}`) for the ID. That is a **larger referencing model than composite's `referenceId`**, which only ever exposed the ID — so linked-record creation now fits in one GraphQL round trip.

The split with the component side is the thing to carry, and this note had it wrong until 2026-10-28. **A component can write through GraphQL**: since **Spring '26**, `executeMutation` from `lightning/graphql` creates, updates and deletes records. It is imperative only — the `@wire` adapter itself still has no mutations. What holds is that capability reaches the API before the component: mutation **chaining** is documented for the API, so do not assume it inside `executeMutation`. → [03-lwc · 07](../03-lwc-and-slds/07-graphql-wire-adapter.md)

**Winter '27 added a guest-access switch.** Admins now control unauthenticated guest access to the GraphQL endpoint from Setup → **API Access Control**. It is **off by default** in new orgs and in orgs with no guest GraphQL use since March 2026; orgs that had guest traffic keep it. A guest call with the switch off gets an error.

## Gotchas

- **It is not a shortcut past the access model.** FLS, sharing and object permissions all apply; an inaccessible field is absent from the response, exactly as in UI API. → [07-security · 13](../07-security-and-sharing/13-field-level-security-and-visibility-layers.md)
- **The `edges`/`node`/`value` nesting is easy to mis-parse.** A field's scalar lives at `…node.Field.value`, not at `…node.Field`.
- **Object coverage inherits UI API's limits**, so an object REST exposes may simply not be in the schema.
- **One query can be expensive.** "One round trip" is not "one cheap query" — a deeply nested request does real work server-side and still consumes API budget.
- **Not every SOQL construct has a GraphQL equivalent.** Complex aggregate and semi-join shapes still belong in SOQL over REST. → [04](04-rest-api-fundamentals.md)
- **`lightning/uiGraphQLApi` is the Mobile Offline module** and is *not* this API, nor the standard adapter — it supports neither optional fields nor dynamic queries. → [03-lwc · 20](../03-lwc-and-slds/20-offline-lwc-and-mobile-constraints.md)

## Recall

Q: What is the Salesforce GraphQL API built on, and why does it matter?
A: UI API — so it inherits FLS, sharing and the org's own metadata-generated schema.

Q: What arrived in Summer '26, and where exactly?
A: Mutation chaining, in the **API**. A mutation can reference any field from an earlier operation via `@{ref.Record.FieldName.value}`.

Q: How does that compare with composite's referencing?
A: It is larger — composite's `referenceId` exposes only the ID of an earlier subrequest.

Q: Can an LWC use GraphQL mutations?
A: Yes, since Spring '26 — imperatively, through `executeMutation` from `lightning/graphql`. The `@wire` adapter itself still reads only.

Q: Where does a field's scalar value sit in a response?
A: Under `edges` → `node` → field → `value`.

## Related

- [03-lwc · 07 GraphQL wire adapter](../03-lwc-and-slds/07-graphql-wire-adapter.md) — the in-component counterpart, and what it still lacks
- [08 · UI API](08-ui-api-and-metadata-aware-clients.md) — the layer this is built on
- [06 · Composite, Batch & Graph APIs](06-composite-batch-and-graph-apis.md) — the REST way to do one round trip
- [04 · REST API fundamentals](04-rest-api-fundamentals.md) — where SOQL still wins

## Sources

- [GraphQL API (Winter '27 release notes)](https://help.salesforce.com/s/articleView?id=release-notes.rn_api_graphql.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-28 · guest-user access control under API Access Control; off by default in new orgs and orgs with no guest GraphQL access since March 2026; existing access kept. 🚩 The developer guide says API 68.0, one status-code page says 67.0
- [(2026年8月) Salesforceの運用に関する重要なお知らせ](https://successjp.salesforce.com/article/NAI-001321) — Salesforce Japan Success Navi, 24 Aug 2026 · read 2026-10-28 · release note added: admins can control guest user access to the GraphQL API
- [GraphQL Mutations Now Available in LWC: Create, Update, and Delete Records](https://developer.salesforce.com/blogs/2026/05/graphql-mutations-now-available-in-lwc-create-update-and-delete-records) — Salesforce Developers · via search 2026-10-28 · `executeMutation` from `lightning/graphql`, introduced Spring '26, imperative only. 🚩 No GA or Beta label seen for the function

## History

- 2026-10-28 · Winter '27 currency check: corrected "LWC has no GraphQL mutations" (`executeMutation`, Spring '26); added the Winter '27 guest-access switch
