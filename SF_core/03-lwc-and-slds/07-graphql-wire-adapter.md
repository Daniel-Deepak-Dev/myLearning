---
vault: SF_core
area: 03-lwc-and-slds
format: dense
status: learning
created: 2026-08-02
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 6
tags: [currency-new]
---
# GraphQL Wire Adapter

**Scope:** Querying Salesforce data from a component with filters, sorting, pagination and aggregates, without an Apex class. Reading a record you already have the ID for is [06](06-lightning-data-service-and-ui-api-wires.md); the standalone GraphQL API used by external clients belongs to [06-integration](../06-integration-and-apis/INDEX.md).

## Core idea

The `graphql` wire adapter closes the gap that used to force an Apex class for any query with a `WHERE` clause. It is UI API underneath, so it inherits everything LDS gives you — the shared cache, automatic FLS and sharing enforcement, reactivity — and adds rich predicates: filter, sort, group, aggregate, and cursor pagination across multiple objects in a single round trip. The real value is not that GraphQL is a nicer query language. It is that **the Apex class, its test class and its security review all disappear**, and with them the most common way LWC data access goes wrong. What it is not is a general replacement for Apex: the wire only reads (writes are a separate imperative call, below), it only sees what UI API models, and it has no transaction. Salesforce's own guidance is blunt about the middle case — if you already know the record IDs, the plain LDS adapters are more efficient and you should use those.

## How it works

| Piece | Role |
|---|---|
| `import { gql, graphql } from 'lightning/graphql'` | the template tag and the adapter — v2; `lightning/uiGraphQLApi` is v1 |
| `uiapi { query { Account(where: …, first: …) { edges { node { … } } } } }` | the query shape — always `edges` → `node` |
| `first` / `after` + `pageInfo { hasNextPage endCursor }` | Cursor Connections pagination; **default page size 10** |
| `where`, `orderBy` | predicates — `{ Name: { like: "Acme%" } }`, `{ Name: { order: ASC } }` |
| `aggregate` + `groupBy` | `avg`/`sum`/`min`/`max`/`count`, optionally `CUBE` or `ROLLUP` |
| `variables` in the wire config | reactive with the `$` prefix, exactly like any other wire |

- **Every scalar comes back as `{ value, displayValue }`.** `node.Name.value` is the raw value; `displayValue` is the locale- and FLS-formatted one. Forgetting `.value` is the first mistake everyone makes.
- **A query can span unrelated objects.** One `uiapi { query { ... } }` block can ask for Accounts and Cases and Users and returns them in one response — that is the round-trip saving, and it is the case where GraphQL clearly beats both LDS and a single Apex method.
- **Pagination is cursor-based, not offset-based.** You keep `endCursor` from the previous page and pass it as `after`. The **upper-bound `first` must stay constant** for a given paginated collection or the adapter loses track of it.
- **The hard ceiling is 2,000 records** across the paginated collection. Past that the answer is Apex, or a design that does not need 2,000 rows in a browser.
- **Reactivity is by variable, not by string.** Build the query once with `gql`, and re-run it by changing a `$`-prefixed value in `variables` — rebuilding the query string on every keystroke defeats the cache.

```js
import { LightningElement, wire } from 'lwc';
import { gql, graphql } from 'lightning/graphql';

export default class AccountSearch extends LightningElement {
    term = 'Acme%';
    @wire(graphql, { query: gql`
        query find($term: String) {
            uiapi { query { Account(where: { Name: { like: $term } },
                            orderBy: { Name: { order: ASC } }, first: 10) {
                edges { node { Id Name { value } AnnualRevenue { displayValue } } }
                pageInfo { hasNextPage endCursor }
            } } }
        }`, variables: '$vars' })
    result;
    get vars() { return { term: this.term }; }       // reactive getter, not a rebuilt query
}
```

## 2026 currency

Two things to keep straight, because the release notes blur them. **A component can write through GraphQL.** Since **Spring '26**, `executeMutation` from `lightning/graphql` creates, updates and deletes records. It is imperative only — not a `@wire` — and it returns `errors` (plural) to match the GraphQL spec. `lightning/graphql` (v2, API 65.0+) supersedes `lightning/uiGraphQLApi` (v1), which still works but is deprecated. Second, **features reach the API before the adapter**: Summer '26 **mutation chaining** (`@{ref.Record.FieldName.value}`) is documented for the GraphQL *API*, so a capability listed there is not evidence a component has it. Two standing gaps worth knowing: variables in the `@skip` and `@include` directives are unsupported, and **Mobile Offline still needs v1 `lightning/uiGraphQLApi`**, because v2 does not support offline. → [RELEASE-RADAR/developer-tooling-and-apis.md](../../RELEASE-RADAR/developer-tooling-and-apis.md)

## Gotchas

- **`node.Name` is an object, not a string.** Every field is `{ value, displayValue }`; binding the field directly renders `[object Object]`.
- **Mutations are imperative and do not refresh queries.** `executeMutation` cannot be `@wire`d, and a newly created record stays out of existing query results until you refresh the query. For one record you already have the ID of, `lightning/uiRecordApi` is still the simpler write → [06](06-lightning-data-service-and-ui-api-wires.md)
- **Objects UI API does not support are invisible here**, because this is UI API with a different query language on top.
- **Aggregate queries still obey the 2,000-record ceiling on the underlying rows**, so a `sum` over a large object is not the tool — that is a report or an Apex aggregate query.
- **System-context work is out of reach by design.** If the requirement is "show a count the user cannot see the rows behind", that is Apex without sharing, not this. → [02-apex · 11 sharing keywords](../02-apex-and-triggers/INDEX.md)

## Recall

Q: What does the GraphQL wire adapter give you that the plain LDS adapters do not?
A: Filtering, sorting, grouping, aggregation, cursor pagination, and several unrelated objects in one round trip.

Q: When does Salesforce say to use LDS adapters instead?
A: When you already know the record IDs — the simpler adapters are more efficient for direct retrieval.

Q: How do you read a field value from the response?
A: Through `edges[].node.FieldName.value` — every scalar is wrapped as `{ value, displayValue }`.

Q: What are the pagination defaults and limits?
A: Ten records per page by default, cursor-based via `first`/`after` and `pageInfo.endCursor`, capped at 2,000 records for the collection.

Q: Can a component create, update or delete records through GraphQL?
A: Yes, since Spring '26 — `executeMutation` from `lightning/graphql`, called imperatively, never through `@wire`. Mutation chaining is documented for the GraphQL API, not for this module.

## Related

- [06 · Lightning Data Service & UI API wires](06-lightning-data-service-and-ui-api-wires.md) — the cache this shares, and the record-by-ID write path
- [08 · Apex in LWC — wire vs imperative](08-apex-in-lwc-wire-vs-imperative.md) — where to go when the query needs server logic or system context
- [05 · Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) — `$`-prefixed wire variables and why the getter form matters

## Sources

- [GraphQL Mutations Now Available in LWC: Create, Update, and Delete Records](https://developer.salesforce.com/blogs/2026/05/graphql-mutations-now-available-in-lwc-create-update-and-delete-records) — Salesforce Developers · via search 2026-10-28 · `executeMutation` from `lightning/graphql`, introduced Spring '26; imperative only; created records need a query refresh, deletes do not
- [executeMutation](https://developer.salesforce.com/docs/platform/lwc/guide/reference-graphql-mutation.html) — Salesforce Developers · via search 2026-10-28 · not supported with `@wire`; takes `query`, `variables`, `operationName`; returns `errors`. 🚩 The search did not show a GA or Beta label for this function; the GraphQL API marks mutations GA from v66.0
- [lightning/graphql Wire Adapter (v2)](https://developer.salesforce.com/docs/platform/lwc/guide/reference-lightning-graphql-module.html) — Salesforce Developers · via search 2026-10-28 · v2 supersedes deprecated v1 `lightning/uiGraphQLApi`; first available at API 65.0; v1 is the one that supports Mobile Offline

## History

- 2026-10-28 · Winter '27 currency check: corrected "no mutations" — `executeMutation` (Spring '26) writes from a component; switched the import to v2 `lightning/graphql`
