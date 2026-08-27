# Exception Handling & Custom Exceptions

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 03

**Scope:** What Apex throws, what you are allowed to catch, and how to fail in a way someone can act on. Per-row DML errors are [05](05-dml-database-methods-and-savepoints.md); async retry and finalizers are phase 04.

## Core idea

Apex gives you two distinct ways to reject something and they are not interchangeable. **`throw`** abandons the transaction and hands the decision upward — right when the caller is code that can choose what to do. **`addError()`** rejects one record while the rest of the batch proceeds — right when the caller is a user or a bulk load and "this row is invalid" is the whole message. Choosing wrongly is how a 5,000-record import dies on row 12. Underneath both sits one hard boundary: governor limits throw `LimitException`, and no `catch` block in the language will stop it. Every recovery strategy in Apex is therefore built *before* the failure — checking limits, sizing batches, sending errors somewhere that survives a rollback.

## How it works

| Exception | Thrown when | Catchable |
|---|---|---|
| `DmlException` | a DML statement fails any row | ✅ |
| `QueryException` | a query returns 0 or 2+ rows into one sObject; FLS violation in user mode | ✅ |
| `NullPointerException` | dereferencing null | ✅ |
| `CalloutException` | HTTP failure, or a callout attempted after DML | ✅ |
| `LimitException` | any governor limit is breached | ❌ **never** |

- **A custom exception is one line and needs no constructor.** `extends Exception` inherits four of them — no-arg, message, message-and-cause, cause — and the class name **must** end in `Exception` or it will not compile.
- **`throw` in a service class, `addError()` at a record boundary:**

```apex
public class OrderSyncException extends Exception {}   // no constructor required

// Record boundary: reject this row, let the rest of the batch through
for (Order o : Trigger.new) {
    if (o.Total__c > creditLimits.get(o.AccountId)) {
        o.addError(Label.Order_Exceeds_Credit_Limit);
    }
}

// Service boundary: the caller decides what a failed sync means
if (res.getStatusCode() != 200) {
    throw new OrderSyncException('Sync failed ' + res.getStatusCode() + ': ' + res.getStatus());
}
```

- **Log the type, not just the message.** `e.getTypeName()`, `e.getMessage()`, `e.getLineNumber()` and `e.getStackTraceString()` together are the difference between a diagnosable log and a string that says "Attempt to de-reference a null object".
- **`finally` runs whether or not the exception was caught**, which makes it the right home for releasing a flag or resetting a static guard. → [07](07-order-of-execution-and-recursion.md)
- **Errors logged by inserting a record vanish with the rollback that caused them.** Publishing a platform event with `PublishImmediately` behaviour survives, because it commits independently of the transaction — the mechanics are phase 04.

## 2026 currency

User mode makes `QueryException` an ordinary runtime outcome rather than a sign of a bug. A field the running user cannot read now throws instead of returning null, and the same applies to writes — so exception handling has quietly become part of the access model, not just the error path. One detail is a genuine improvement worth exploiting: `WITH USER_MODE` reports **every** FLS violation on the query, not only the first, so the exception message is a complete list of what the user is missing rather than a one-at-a-time guessing game. Read them off the `QueryException` and log the lot. See [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **`catch (Exception e)` does not catch `LimitException`.** There is no syntax that does. Check `Limits` before the work instead. → [01](01-apex-language-core-and-governor-limits.md)
- **Catching an exception does not undo the DML already committed in that transaction.** Only a `Savepoint` rollback does. → [05](05-dml-database-methods-and-savepoints.md)
- **An exception thrown in an `after` trigger discards the whole save**, including the write that already happened at step 7 of the save order.
- **A custom exception class whose name doesn't end in `Exception` is a compile error**, with a message that does not obviously say so.
- **`addError()` on a scalar field cannot be safe-navigated** — `o.Name?.addError(…)` will not compile. Call it on the sObject, or on the field directly. → [02](02-modern-apex-syntax.md)
- **An empty `catch` block is the one unforgivable pattern.** It converts a failure into wrong data, and Code Analyzer flags it precisely because it is invisible afterwards.
- **`getMessage()` on a `DmlException` describes only the first failed row.** For the full picture use `getNumDml()` and `getDmlMessage(i)`, or switch to `Database.insert(list, false)` and read the results.

## Recall

Q: When do you use `addError()` rather than `throw`?
A: At a record boundary, when rejecting one row and letting the rest of the batch commit is the correct behaviour. `throw` abandons the whole transaction.

Q: Can you catch a governor limit failure?
A: No. `LimitException` is uncatchable by any `catch` clause — the only defence is checking `Limits` before doing the work.

Q: How much code does a custom exception need?
A: One line: `public class MyException extends Exception {}`. It inherits four constructors, and the name must end in `Exception`.

Q: Why does inserting an error-log record inside a `catch` block often produce no log?
A: If the transaction rolls back, so does the log insert. Publish a platform event with immediate publish behaviour instead.

Q: What is the user-mode improvement to FLS error reporting?
A: `WITH USER_MODE` reports every field-level security violation on the query, not just the first one.

## Related

- [05 · DML, Database methods & savepoints](05-dml-database-methods-and-savepoints.md) — per-row errors as the alternative to an exception, and the only real undo
- [06 · Triggers & the handler framework](06-triggers-and-the-handler-framework.md) — where `addError()` belongs and what it does in each context
- [01-admin · 08 Validation rules & duplicate management](../01-admin-and-declarative-platform/08-validation-rules-and-duplicate-management.md) — the declarative form of the same record-level rejection
