# JSON, Serialization & Untyped Data

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 21

**Scope:** Turning Apex objects into JSON and back — the four `JSON` entry points, streaming with `JSONParser`/`JSONGenerator`, and traversing a response whose shape you do not control. The HTTP that carries it is [19](19-callouts-named-credentials-and-http-in-apex.md); the annotations that make a class a typed payload are [23](23-userdefinedtype-and-typed-interop.md).

## Core idea

`JSON.serialize()` and `JSON.deserialize()` cover most of the work, and the interesting decisions are all about **how much you are willing to assume about the other side's payload**. Deserializing into an Apex class is the strongest assumption: you get type safety and a compile-time contract, and you get a runtime exception the day the provider adds a field or a field name collides with an Apex reserved word. Deserializing untyped gives up type safety and gives back tolerance — a `Map<String, Object>` accepts anything and defers every failure to the moment you cast. Neither is correct in general. The choice is a statement about whose schema changes you expect to survive, and the streaming classes exist for the case where the payload is too large to hold in heap at all.

## How it works

| Call | Returns | Use when |
|---|---|---|
| `JSON.serialize(obj)` | `String` | writing a request body; second arg `suppressApexObjectNulls` drops null fields |
| `JSON.deserialize(str, Type)` | typed object | you own or trust the schema; **unknown fields are ignored** |
| `JSON.deserializeStrict(str, Type)` | typed object | contract enforcement — **throws on any unknown field** |
| `JSON.deserializeUntyped(str)` | `Object` (really `Map<String, Object>`) | shape is unknown, variable, or uses reserved words |

- **Untyped traversal is a cast at every level**, and each level is a place the provider can break you:

```apex
Map<String, Object> root = (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
List<Object> items = (List<Object>) root.get('results');
for (Object o : items) {
    Map<String, Object> item = (Map<String, Object>) o;
    // numbers arrive as Integer, Long, Double or Decimal depending on the literal
    Decimal amount = (Decimal) item.get('amount');
}
```

- **`JSONGenerator` and `JSONParser` stream** — `writeStartObject()`/`writeStringField()` and `nextToken()`/`getText()` — so neither the whole string nor the whole object graph needs to exist at once. This is the heap answer for a large payload → [24](24-apex-performance-and-profiling.md).
- **`@JsonAccess`** (class-level) controls whether a type may be serialized or deserialized across namespaces — the packaging concern, not a formatting one.

> **Watch the seam with `String.template()`.** Multiline strings make an inline JSON body readable, and `String.template()` fills its placeholders — but it renders a `Datetime` in **GMT** as `yyyy-MM-dd HH:mm:ss`, which is neither `String.valueOf()`'s output nor ISO-8601. Hand-building a JSON body that way produces a timestamp the receiver may silently misread. `JSON.serialize()` on a real object does not have this problem. → [02](02-modern-apex-syntax.md)

## Gotchas

- **Apex reserved words cannot be field names, so a payload containing `currency`, `limit`, `group` or `class` cannot be deserialized into a typed class at all** — the class simply cannot declare the member. This is the single commonest reason to fall back to `deserializeUntyped`.
- **`deserialize()` silently ignores unknown fields; `deserializeStrict()` throws on them.** Strict is right for a contract you control and wrong for a third-party API that adds fields without telling you.
- **Untyped numbers are not one type.** `1` deserializes to `Integer`, a large value to `Long`, `1.5` to `Double` — casting straight to `Decimal` throws on some inputs and not others, so the bug depends on the data.
- **Serializing an SObject emits only the fields that were queried or set.** A field absent from the `SELECT` list is absent from the JSON rather than null, and a round trip therefore silently narrows the record.
- **`serialize()` on an object graph with a cycle throws.** Parent-child references that point both ways need one side marked `transient`.
- **`transient` fields are skipped by serialization *and* excluded from view state** — one keyword, two effects, and forgetting the first is how a value survives locally and vanishes over the wire.
- **The whole serialized string counts against heap** (6 MB synchronous, 12 MB async). A response that fits the callout size limit can still fail on heap once it is a `String` and an object graph simultaneously → [01](01-apex-language-core-and-governor-limits.md).

## Recall

Q: Why can a valid JSON payload be impossible to deserialize into a typed Apex class?
A: If a field name is an Apex reserved word — `currency`, `limit`, `group`, `class` — the class cannot declare that member. `deserializeUntyped` is the fallback.

Q: What is the difference between `deserialize` and `deserializeStrict`?
A: `deserialize` ignores fields the target type does not declare; `deserializeStrict` throws on any unknown field. Strict suits an owned contract, lenient suits a third-party API.

Q: What type does an untyped JSON number become?
A: It depends on the literal — `Integer`, `Long`, `Double` or `Decimal`. Casting blindly to one of them fails on some inputs and not others.

Q: When would you use `JSONGenerator` instead of `JSON.serialize`?
A: When the payload is large enough that holding both the object graph and the resulting string in heap is the binding limit. The generator streams and never materialises both.

Q: What happens to fields you did not query when you serialize an SObject?
A: They are omitted from the JSON entirely rather than serialized as null, so a query-serialize-deserialize round trip silently drops them.

## Related

- [19 · Callouts, Named Credentials & HTTP in Apex](19-callouts-named-credentials-and-http-in-apex.md) — where these payloads come from and the limits on the request itself
- [23 · `UserDefinedType` & typed interop](23-userdefinedtype-and-typed-interop.md) — `@AuraEnabled` and `@InvocableVariable`, the annotations that make a class a payload for Flow, LWC and agents
- [02 · Modern Apex syntax](02-modern-apex-syntax.md) — multiline strings and `String.template()`, including the GMT `Datetime` trap above
- [06-integration · 18 Apex REST & custom endpoints](../06-integration-and-apis/18-apex-rest-and-custom-endpoints.md) — the inbound direction, where the platform does the binding for you
