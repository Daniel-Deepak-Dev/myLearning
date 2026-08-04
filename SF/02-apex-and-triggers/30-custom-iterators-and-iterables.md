# Custom Iterators & Iterables

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 21

**Scope:** Writing `Iterator<T>` and `Iterable<T>` by hand, and the one place the platform genuinely asks for them — a Batch `start()` whose scope is not a query. Batch mechanics and scope sizing are [14](14-batch-apex-and-stateful-processing.md).

## Core idea

Every Apex list is already iterable, so writing an iterator is never about looping over a collection you have. It is about producing elements **you do not have yet**: pages of a paginated API, lines of a file being decoded, a synthetic range, a merge of two sorted sources. The two interfaces divide that work cleanly and are constantly confused. `Iterator<T>` is the cursor — it holds the position and answers `hasNext()`/`next()`. `Iterable<T>` is the *factory* for cursors — its single `iterator()` method hands out a fresh one. The distinction has a practical edge: only `Iterable` can be used in a `for` loop or returned from `Database.Batchable.start()`, and only because it can produce a new cursor on demand. An `Iterator` used directly is single-use, and reusing one is a silently empty loop rather than an error.

## How it works

- **`Iterator<T>`** requires exactly two methods: `Boolean hasNext()` and `T next()`.
- **`Iterable<T>`** requires exactly one: `Iterator<T> iterator()`.
- **A class may implement both**, returning `this` from `iterator()` — convenient, and the direct cause of the single-use trap below.

```apex
public class CountdownIterable implements Iterator<Integer>, Iterable<Integer> {
    private Integer current;
    public CountdownIterable(Integer from) { this.current = from; }
    public Iterator<Integer> iterator()  { return new CountdownIterable(current); } // fresh cursor
    public Boolean hasNext()             { return current > 0; }
    public Integer next() {
        if (!hasNext()) throw new NoSuchElementException('Exhausted');
        return current--;
    }
}

for (Integer i : new CountdownIterable(3)) { System.debug(i); }   // 3, 2, 1
```

- **The real use is Batch Apex over a non-query scope.** `start()` may return a `Database.QueryLocator` *or* an `Iterable<SObject>`, and the second is how you batch over something SOQL cannot express — an aggregated result set, a decoded file, a remote API's pages.
- **That choice costs three orders of magnitude of scale.** `QueryLocator` supports **50 million** records; the `Iterable` path is bounded by the ordinary query row limit at **50,000**, because the collection is built inside a normal transaction. Reach for `Iterable` when the scope is not queryable, never as a way to handle more data → [14](14-batch-apex-and-stateful-processing.md).

## Gotchas

- **`next()` must throw when exhausted**, conventionally `NoSuchElementException`. Returning `null` instead turns a bounded loop into an infinite one if `hasNext()` is also wrong.
- **Returning `this` from `iterator()` makes the object single-use.** The second `for` loop over it starts from the already-exhausted position and executes zero times — no exception, no warning. Return a fresh instance.
- **A stateful iterator inside a `Database.Stateful` batch is serialized between chunks**, so any non-serializable member — an open `JSONParser`, an `HttpResponse` — breaks the job at the first chunk boundary → [14](14-batch-apex-and-stateful-processing.md).
- **Work done in `hasNext()` runs inside the caller's governor limits.** An implementation that performs a callout or a query per element is a limit exception waiting for a large input, and the cost is invisible at the call site.
- **Iterators as a parameter or return type are on the Stub API's cannot-touch list**, so an interface exposing one cannot be mocked with `Test.createStub()` — it has to be faked with a real implementation → [21](21-apex-testing-advanced-and-mocking.md).
- **`Iterable<T>` in a `for` loop calls `iterator()` once**, at the top. Mutating the underlying source mid-loop is undefined rather than detected.
- **Neither interface gives you `remove()`.** Apex's `Iterator` has only the two methods; there is no mutation half of the protocol.

## Recall

Q: What is the difference between `Iterator<T>` and `Iterable<T>`?
A: `Iterator` is the cursor — `hasNext()`/`next()`, holding position. `Iterable` is the factory that produces a fresh cursor from `iterator()`. Only `Iterable` works in a `for` loop or a Batch `start()`.

Q: Why is returning `this` from `iterator()` a trap?
A: The object becomes single-use. A second loop resumes from the exhausted position and runs zero times, silently, with no exception.

Q: When does Batch Apex need a custom `Iterable`?
A: When the scope cannot be expressed as SOQL — aggregated results, a decoded file, pages from an external API.

Q: What does choosing `Iterable` over `QueryLocator` in `start()` cost?
A: Scale. `QueryLocator` handles 50 million records; the `Iterable` path is capped at the 50,000-row query limit because it is assembled in a normal transaction.

Q: Why can an iterator-returning interface not be mocked with the Stub API?
A: Iterators as a parameter or return type are explicitly excluded by the Stub API, so `Test.createStub()` cannot produce one — you need a real fake implementation.

## Related

- [14 · Batch Apex & stateful processing](14-batch-apex-and-stateful-processing.md) — the `start()` contract, `QueryLocator` vs `Iterable`, and `Database.Stateful` serialization
- [21 · Apex testing advanced & mocking](21-apex-testing-advanced-and-mocking.md) — the Stub API exclusion list that makes iterator-shaped APIs awkward to test
- [01 · Apex language core & governor limits](01-apex-language-core-and-governor-limits.md) — why work hidden inside `hasNext()` is charged to the caller
- [17 · `Database.Cursor` & large result sets](17-database-cursor-and-large-result-sets.md) — the platform's own cursor, for the query case a custom iterator should not try to solve
