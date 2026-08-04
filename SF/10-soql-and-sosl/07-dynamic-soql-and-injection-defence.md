# Dynamic SOQL & Injection Defence

> Area: 10-soql-and-sosl · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 22

**Scope:** Building a query string at runtime and the security consequences of doing so — binds, escaping, and identifier allowlisting. The Apex API surface (`Database.queryWithBinds`, `AccessLevel`, describe calls) is [02-apex · 04](../02-apex-and-triggers/04-advanced-soql-sosl-and-dynamic-queries.md).

## Core idea

A static SOQL literal is checked by the compiler: field names, object names and types are all validated before deployment. **The moment a query becomes a string, every one of those guarantees is gone** and a new one is introduced — user input can now change the query's *structure*, not just its values. That is SOQL injection, and the reason it is worth its own note is that the standard mitigation people reach for, `String.escapeSingleQuotes()`, defends exactly one of the two attack surfaces. Values can be made safe with binds. **Identifiers — object names, field names, `ORDER BY` targets, `LIMIT` — cannot be bound at all**, and the only defence for those is an allowlist. A dynamic query builder that escapes its values and concatenates its column names is the common shape and is still vulnerable.

## How it works

- **Bind variables are the complete defence for values**, and the modern form takes them from a map rather than resolving against enclosing Apex locals:

```apex
Map<String, Object> binds = new Map<String, Object>{ 'name' => userInput };
List<Account> safe = Database.queryWithBinds(
    'SELECT Id, Name FROM Account WHERE Name = :name', binds, AccessLevel.USER_MODE);
```

- **Identifiers need an allowlist, not escaping.** Validate the requested field against a set you control — ideally derived from a describe call so it reflects the real schema:

```apex
Set<String> allowed = Schema.SObjectType.Account.fields.getMap().keySet();
if (!allowed.contains(sortField.toLowerCase())) throw new QueryException('bad field');
```

- **`String.escapeSingleQuotes()` escapes quote characters and nothing else.** It is the right tool only where a bind is genuinely impossible and the value is still a *value*.
- **The three things an attacker changes** are the filter (`' OR Name != '`), the object, and the clause structure — appending `LIMIT`, `ORDER BY`, or a second condition. Binds close the first; only allowlisting closes the others.

## 2026 currency

**Dynamic queries default to user mode at 67.0.** `Database.query()` and `Database.queryWithBinds()` now enforce the running user's FLS and sharing unless `AccessLevel.SYSTEM_MODE` is passed deliberately — which materially reduces the blast radius of an injection, because injected SQL now runs as the attacker rather than as the system. **It does not make injection safe**: an attacker can still widen a filter to everything they are personally entitled to see, which in a community or partner context is often the point. `WITH SECURITY_ENFORCED` **no longer compiles**, so any dynamic query string still assembling it is dead code. Two Winter '25 quality-of-life changes are worth knowing because they remove long-standing debugging pain: **invalid dynamic SOQL now returns specific error messages** instead of a generic parse failure, and **negative currency values are supported** in dynamic and API-issued queries. → [02-apex · 10](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)

## Gotchas

- **`String.escapeSingleQuotes()` is not an injection defence for identifiers.** An injected field name, object name, `LIMIT` or `ORDER BY` passes straight through untouched.
- **A bind cannot substitute an identifier.** Object and field names must be assembled from values you control — there is no parameterised form.
- **User mode limits the damage; it does not prevent the attack.** The injected query runs with the attacker's own access, which for an authenticated portal user may still be a great deal of data.
- **Allowlisting against a hardcoded list drifts from the schema.** Deriving it from `getMap()` costs CPU but cannot go stale → [02-apex · 04](../02-apex-and-triggers/04-advanced-soql-sosl-and-dynamic-queries.md).
- **`Database.query()` with a literal string is still dynamic.** It is not compile-checked even when nothing is concatenated into it, so a typo deploys and fails at runtime.
- **`queryWithBinds` resolves binds by map key, not by Apex variable name** — a key present in the string but missing from the map throws at runtime rather than binding null.
- **Building a query in a loop is a governor-limit bug waiting to happen**, and dynamic construction makes it much easier to write by accident.

## Recall

Q: Why is `String.escapeSingleQuotes()` an incomplete injection defence?
A: It only handles quote characters in values. Injected object names, field names, `LIMIT` and `ORDER BY` clauses pass through untouched and need an allowlist instead.

Q: What can a bind variable not do?
A: Substitute an identifier. Object names, field names and clause keywords cannot be bound and must be assembled from controlled values.

Q: How did the 67.0 user-mode default change the risk of SOQL injection?
A: It reduces the blast radius — injected queries run with the attacker's own FLS and sharing rather than as the system. It does not prevent the attack.

Q: Where does `Database.queryWithBinds` take its bind values from?
A: A `Map<String, Object>` keyed by bind name, rather than resolving `:variable` against Apex locals — which removes the old enclosing-scope surprise.

Q: What is the safest source for an identifier allowlist?
A: A describe call such as `Schema.SObjectType.X.fields.getMap()`, so the allowlist reflects the real schema instead of drifting from a hardcoded list.

## Related

- [02-apex · 04 Dynamic SOQL, SOSL & describe in Apex](../02-apex-and-triggers/04-advanced-soql-sosl-and-dynamic-queries.md) — the Apex API surface, `AccessLevel`, and schema describe including the `validFor` bitmap
- [02 · Filtering, operators & literals](02-filtering-operators-and-literals.md) — what the assembled `WHERE` clause can contain
- [02-apex · 10 Apex security: user mode & FLS](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) — the default that changed what an injected query can reach
- [07-security · 26 Secure coding checklist](../07-security-and-sharing/26-secure-coding-checklist.md) — injection as one control inside the wider review
