# GraphQL API

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** The standalone GraphQL endpoint for **external clients**. The in-component wire adapter is a different, narrower thing — [03-lwc · 07](../03-lwc-and-slds/07-graphql-wire-adapter.md) — and the two diverge on features, so keep them apart.

## Core idea

REST returns whatever a resource returns; the client discards the rest and makes another call for what was missing. GraphQL inverts that: the client declares the exact shape it wants — fields, related records, several unrelated objects — and receives precisely that in one round trip. For a mobile or headless client on a slow connection, that is the difference between six requests and one.

The Salesforce implementation is built **on UI API**, which has a consequence people miss: it inherits UI API's semantics, so FLS and sharing are applied and the schema exposed is the org's own, generated from its metadata. It is not a generic database query language bolted onto Salesforce — it is a query language over the same metadata-aware layer as [08](08-ui-api-and-metadata-aware-clients.md).

## How it works

- **One endpoint, one verb:** `POST /services/data/v67.0/graphql`. Versioning still lives in the path → [02](02-api-versions-and-the-retirement-treadmill.md).
- **The schema is your org's**, discoverable by introspection — so a client tool can autocomplete against custom objects and fields with no configuration.
- **Records come back through a connection shape** — `edges` → `node` → field → `value` — which is verbose to read but is what carries pagination cursors and per-field metadata.
- **Filtering, sorting, pagination and aggregates** are all query arguments rather than separate resources.
- **Several unrelated objects in one query** is the headline capability, and the one that replaces a composite request for read-heavy work → [06](06-composite-batch-and-graph-apis.md).
- **`X-Chatter-Entity-Encoding: false`** is required for correct encoding of returned text.
- **Authentication is ordinary OAuth**, and Salesforce's guidance is to use an External Client App for production clients → [16](INDEX.md).

## 2026 currency

**Mutation chaining is the Summer '26 addition, and it landed in the API — not in the LWC wire adapter.** A mutation can now reference **any field** returned by an earlier operation in the same request, not merely its record ID: `@{ref.Record.FieldName.value}` for a field value, `@{ref.Record.Id}` (shorthand `@{ref}`) for the ID. That is a **larger referencing model than composite's `referenceId`**, which only ever exposed the ID — so linked-record creation now fits in one GraphQL round trip.

The split with the wire adapter is the thing to carry: **the adapter still has no mutations at 67.0**, so inside a component LDS remains the only create/update/delete path, and capability generally reaches the API several releases before the adapter. Reading a 2026 blog post about GraphQL mutations and expecting them in an LWC is the predictable mistake. → [03-lwc · 07](../03-lwc-and-slds/07-graphql-wire-adapter.md)

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

Q: Can an LWC use GraphQL mutations at 67.0?
A: No. The wire adapter still has no mutations; LDS remains the only client-side write path in a component.

Q: Where does a field's scalar value sit in a response?
A: Under `edges` → `node` → field → `value`.

## Related

- [03-lwc · 07 GraphQL wire adapter](../03-lwc-and-slds/07-graphql-wire-adapter.md) — the in-component counterpart, and what it still lacks
- [08 · UI API](08-ui-api-and-metadata-aware-clients.md) — the layer this is built on
- [06 · Composite, Batch & Graph APIs](06-composite-batch-and-graph-apis.md) — the REST way to do one round trip
- [04 · REST API fundamentals](04-rest-api-fundamentals.md) — where SOQL still wins
