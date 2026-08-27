# GraphQL Wire Adapter

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 06

**Scope:** Querying Salesforce data from a component with filters, sorting, pagination and aggregates, without an Apex class. Reading a record you already have the ID for is [06](06-lightning-data-service-and-ui-api-wires.md); the standalone GraphQL API used by external clients belongs to [06-integration](../06-integration-and-apis/INDEX.md).

## Core idea

The `graphql` wire adapter closes the gap that used to force an Apex class for any query with a `WHERE` clause. It is UI API underneath, so it inherits everything LDS gives you — the shared cache, automatic FLS and sharing enforcement, reactivity — and adds rich predicates: filter, sort, group, aggregate, and cursor pagination across multiple objects in a single round trip. The real value is not that GraphQL is a nicer query language. It is that **the Apex class, its test class and its security review all disappear**, and with them the most common way LWC data access goes wrong. What it is not is a general replacement for Apex: it reads, it does not write, it only sees what UI API models, and it has no transaction. Salesforce's own guidance is blunt about the middle case — if you already know the record IDs, the plain LDS adapters are more efficient and you should use those.

## How it works

| Piece | Role |
|---|---|
| `import { gql, graphql } from 'lightning/uiGraphQLApi'` | the template tag and the adapter |
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
import { gql, graphql } from 'lightning/uiGraphQLApi';

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

Two things to keep straight, because the release notes blur them. **Mutation chaining shipped in Summer '26 for the GraphQL *API*, not for the wire adapter** — an operation can now reference any field returned by an earlier operation in the same request via `@{ref.Record.FieldName.value}`, which is genuinely useful for server-to-server work and does nothing for a component, because the wire adapter still supports no mutations at all. Writes from a component remain LDS's job. Second, **features reach the API before the adapter**, sometimes by several releases, so a capability documented under "GraphQL API" is not evidence the wire adapter has it. Two standing gaps worth knowing: variables in the `@skip` and `@include` directives are unsupported, and **Mobile Offline needs the imperative `lightning/uiGraphQLApi` module rather than the wire adapter**. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **`node.Name` is an object, not a string.** Every field is `{ value, displayValue }`; binding the field directly renders `[object Object]`.
- **No mutations.** Create, update and delete go through `lightning/uiRecordApi`. → [06](06-lightning-data-service-and-ui-api-wires.md)
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

Q: Did Summer '26 mutation chaining give components the ability to write via GraphQL?
A: No — chaining is a GraphQL API feature. The wire adapter still has no mutations; writes stay in LDS.

## Related

- [06 · Lightning Data Service & UI API wires](06-lightning-data-service-and-ui-api-wires.md) — the cache this shares, and the only client-side write path
- [08 · Apex in LWC — wire vs imperative](08-apex-in-lwc-wire-vs-imperative.md) — where to go when the query needs server logic or system context
- [05 · Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) — `$`-prefixed wire variables and why the getter form matters
