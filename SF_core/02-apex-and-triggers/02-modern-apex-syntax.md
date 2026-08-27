# Modern Apex Syntax

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 03

**Scope:** The language additions that post-date most published Apex — safe navigation, null coalescing, `switch`, and the Summer '26 string work. Query and DML idioms are [03](03-soql-fundamentals-and-relationship-queries.md) and [05](05-dml-database-methods-and-savepoints.md).

## Core idea

Apex accreted its modern conveniences slowly, and the practical consequence is that most sample code you will meet — including much of Salesforce's own — is written in a dialect several releases behind the compiler. The additions all attack the same two kinds of noise: **null ceremony** and **string concatenation**. Nothing here changes what Apex can do; it changes how much of a method is plumbing. That matters more than it sounds, because the alternative to a `?.` chain is a nested `if` ladder, and nested `if` ladders are where null-handling bugs live. Learn the GA release of each one — it is the fastest way to date a codebase you have inherited.

## How it works

| Construct | Syntax | GA |
|---|---|---|
| Switch statement | `switch on x { when 'a' {…} when else {…} }` | Summer '18 (43.0) |
| Safe navigation | `a?.b?.c()` | Winter '21 (50.0) |
| Null coalescing | `a ?? b` | Spring '24 (60.0) |
| Multiline string | `'''…'''` | **Summer '26 (67.0)** |
| String template | `'…${key}…'.template(bindMap)` | **Summer '26 (67.0)** |

- **`?.` short-circuits the whole chain.** `o.Account?.Owner?.Email` yields `null` the moment any link is null, instead of throwing. It works on method chains, sObject traversal and inline SOQL results.
- **`??` evaluates its left operand exactly once**, which is the real gain over the `x == null ? getDefault() : x` idiom it replaces — that one evaluated `x` twice, and evaluated it twice *again* every time someone nested it.
- **`switch on` takes `Integer`, `Long`, `String`, `Enum` and sObject types.** No fall-through, no `break`, and `when` accepts a comma-separated list. It is the right shape for trigger context dispatch. → [06](06-triggers-and-the-handler-framework.md)
- **Multiline strings and templates together replace concatenation.** Triple single quotes open and close a literal block; `.template()` fills `${key}` placeholders from a `Map<String, Object>`:

```apex
// 67.0 multiline + named interpolation, with the older two operators in the map
String body = '''
Hi ${name},
Your order shipped on ${shipped}.'''.template(new Map<String, Object>{
    'name'    => c.FirstName ?? 'there',              // 60.0 null coalescing
    'shipped' => o.Account?.LastActivityDate          // 50.0 safe navigation
});
```

## 2026 currency

The 67.0 additions are **multiline strings and `String.template()`**, both GA. They are the first genuine ergonomics change to Apex text handling since the language shipped, and they retire the concatenation chains that email bodies, JSON payloads, HTTP request bodies and dynamic SOQL were all built from. Two details do not survive a casual reading: the newline immediately after the opening `'''` is **trimmed** — so the literal above starts at `Hi`, not a blank line — and `.template()` renders a `Datetime` in **GMT** as `yyyy-MM-dd HH:mm:ss`, which is not what `String.valueOf()` does. Nothing else in the operator set moved; `??`, `?.` and `switch` are all long-standing GA and any "new in Apex" article claiming otherwise is dating itself.

## Gotchas

- **`?.` is banned in more places than people expect** — static member access (`String.format(…)`, `AClass.aStaticMethod()`), namespaces, `Trigger.new`, `{Type}.class`, assignment targets (`foo?.bar = 42`) and SOQL bind variables. All compile errors, so you find out immediately.
- **`c.LastName?.addError('…')` will not compile.** Safe navigation is restricted on scalar sObject fields for `addError()`; call it on the sObject. → [09](09-exception-handling-and-custom-exceptions.md)
- **A `?.` chain that returns null tells you nothing about *which* link was null.** In a validation path that is a debugging cost, not a saving — use it to avoid crashes, not to avoid thinking.
- **Indentation inside a `'''` block is part of the string.** Aligning the literal with your code indents every line of the output.
- **`.template()` has no compile-time key checking.** A typo in `${nmae}` is a runtime `StringException`, not a build failure — the map keys and the placeholders are only matched when the line runs.
- **`switch on` without a `when else` silently does nothing** on an unmatched value. There is no fall-through to save you.
- **`??` is not a null-safe assignment.** `a ?? b` returns a value; it does not write to `a`. Apex has no `??=`.

## Recall

Q: Which two Apex syntax features are new at API 67.0?
A: Multiline strings using `'''` delimiters, and `String.template()` for `${key}` interpolation from a map. Both GA.

Q: What is the advantage of `a ?? b` over `a == null ? b : a`?
A: The left operand is evaluated exactly once. The ternary form evaluates `a` twice, which matters when it is a method call.

Q: Name three places the safe navigation operator will not compile.
A: Any three of: static method or variable access, namespaces, `Trigger.new`, `{Type}.class`, assignment targets, SOQL bind variables.

Q: What happens to the newline directly after an opening `'''`?
A: It is trimmed, so the string starts with the first visible character. The newline before the closing `'''` is *not* trimmed.

Q: How does `String.template()` render a `Datetime`?
A: In GMT, as `yyyy-MM-dd HH:mm:ss` — not the running user's locale. Format it yourself before putting it in the map.

## Related

- [01 · Apex language core & governor limits](01-apex-language-core-and-governor-limits.md) — the type system these operators work over
- [04 · Advanced SOQL, SOSL & dynamic queries](04-advanced-soql-sosl-and-dynamic-queries.md) — where multiline strings stop being cosmetic and make dynamic SOQL readable
- [09 · Exception handling & custom exceptions](09-exception-handling-and-custom-exceptions.md) — what `?.` suppresses, and when you wanted the exception
