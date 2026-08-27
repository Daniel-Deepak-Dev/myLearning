# Apex Enterprise Patterns & Layered Design

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 21

**Scope:** The architecture *above* the handler class — Selector, Domain, Service and Unit of Work, and when the ceremony is worth it. The trigger-to-handler binding itself is [06](06-triggers-and-the-handler-framework.md); making the layers mockable is [28](28-dependency-injection-and-pluggable-apex.md).

## Core idea

[06](06-triggers-and-the-handler-framework.md) gets logic out of the trigger and into a handler. That is one move, and it stops working at about the point a second team touches the org: handlers grow to a thousand lines, the same query is written eleven different ways, and nothing can be unit-tested without inserting records. **Enterprise Patterns are the next factoring — separate code by *what kind of thing it is* rather than by which trigger called it.** Queries live in a Selector, per-record behaviour in a Domain, cross-object orchestration in a Service, and every DML statement in a Unit of Work that commits once at the end. The payoff is not elegance; it is that each layer has one reason to change and can be replaced by a mock. The cost is real and is discussed below.

## How it works

| Layer | Owns | Shape |
|---|---|---|
| **Selector** | every SOQL against one SObject | `AccountsSelector.selectById(Set<Id>)` — field list in one place |
| **Domain** | validation and defaulting for one SObject | `Accounts extends fflib_SObjectDomain` — `onValidate()`, `onBeforeInsert()` |
| **Service** | a use case spanning objects | `OpportunityService.closeAndInvoice(…)` — static, coarse-grained |
| **Unit of Work** | all DML, ordered by dependency | `registerNew` / `registerDirty` / `registerRelationship` → one `commitWork()` |

- **The Unit of Work is the layer that pays for itself first.** You register work against it and it resolves insert order from a declared `List<SObjectType>`, sets the child's lookup after the parent gets its Id, and issues **one DML statement per object type** inside a single savepoint. That is the whole "insert parents, collect Ids, stitch children, insert children" ritual deleted → [05](05-dml-database-methods-and-savepoints.md).
- **The Application factory is what makes the rest testable.** One class maps each layer to its implementation, and tests swap in mocks without touching the code under test → [28](28-dependency-injection-and-pluggable-apex.md).

```apex
fflib_ISObjectUnitOfWork uow = Application.UnitOfWork.newInstance();
Account a = new Account(Name = 'Acme');
uow.registerNew(a);
// child's AccountId is filled in after the parent inserts — no second pass
uow.registerRelationship(new Contact(LastName = 'Roe'), Contact.AccountId, a);
uow.commitWork();   // ordered DML, one statement per type, one savepoint
```

- **fflib is community open source, not a Salesforce product.** It lives in the `apex-enterprise-patterns` GitHub org and began as FinancialForce's Apex Commons. Salesforce publicises the *patterns*; it ships and supports none of this code. A hand-rolled Selector and Unit of Work are entirely legitimate — the pattern is the durable part, the library is one implementation you now own and must upgrade yourself.

## 2026 currency

**The 67.0 security flip inverts what a Selector's access options are for.** fflib Selectors carry `enforceFLS` / `enforceCRUD` toggles, and every tutorial written before 2026 turns them *on* — because Apex ran in system mode by default and elevated access was what you got unless you asked otherwise. At 67.0 the default is user mode, so a Selector's job is now the opposite: it is the one place that might legitimately need `AccessLevel.SYSTEM_MODE`, and that elevation should be deliberate, named and rare. A Selector base class carrying an unexamined "enforce security" flag inherited from a 2019 fork is now the surprising path, not the safe one. Audit the base class before trusting the subclasses. → [10](10-apex-security-user-mode-and-fls.md), [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md)

## Gotchas

- **The patterns are overhead below a threshold.** Four layers and a factory to update one field is worse than a handler method. They pay off on multi-team orgs, long-lived code and heavy test suites — roughly, when more than one person is changing the same object's logic.
- **`commitWork()` runs in one transaction, so one bad record rolls back everything registered.** That is usually what you want and is exactly wrong for partial-success batch processing → [05](05-dml-database-methods-and-savepoints.md).
- **A Unit of Work does not lift DML governor limits.** It reduces *statements* by grouping per type; the 10,000-row DML limit is unchanged.
- **`registerRelationship` only resolves parents registered in the same Unit of Work.** An existing record's Id must be set directly — a silent no-op otherwise.
- **Selector field lists grow until every query is `SELECT` everything.** One oversized field list shared by twenty callers is a heap and CPU problem that no single caller looks responsible for.
- **Domain classes bind to a trigger via the library's own dispatcher**, which is a *second* framework layered on the one-trigger-per-object rule from [06](06-triggers-and-the-handler-framework.md). Pick one dispatcher; running both is how ordering becomes non-deterministic again.
- **Adopting fflib means owning a dependency with no Salesforce support path.** Budget for reading its source when something breaks.

## Recall

Q: What does a Unit of Work do that hand-written DML does not?
A: It orders inserts by declared dependency, resolves parent Ids into child lookups via `registerRelationship`, and issues one DML statement per object type inside a single `commitWork()`.

Q: Is fflib a Salesforce product?
A: No. It is community-maintained open source in the `apex-enterprise-patterns` GitHub org, originally FinancialForce's Apex Commons. Salesforce promotes the patterns but ships and supports none of the code.

Q: How did the 67.0 security default change the Selector layer?
A: Apex now defaults to user mode, so a Selector's `enforceFLS`/`enforceCRUD` flags no longer describe the safe path — the notable case is now deliberate elevation to `AccessLevel.SYSTEM_MODE`.

Q: When are these patterns the wrong choice?
A: On small, single-team orgs. Four layers plus a factory to set one field costs more than it returns; the break-even is roughly when several people change the same object's logic.

Q: Which layer owns SOQL, and why does that matter?
A: The Selector. Centralising the field list and filters stops the same query being rewritten per caller and gives one place to change access level or add an index-friendly filter.

## Related

- [06 · Triggers & the handler framework](06-triggers-and-the-handler-framework.md) — the layer below; its "no logic in the trigger" rule is what these patterns extend
- [28 · Dependency injection & pluggable Apex](28-dependency-injection-and-pluggable-apex.md) — the Application factory generalised, and why layering without injection is untestable
- [05 · DML, Database methods & savepoints](05-dml-database-methods-and-savepoints.md) — what `commitWork()` is doing underneath, and what a rollback does not restore
- [10 · Apex security: user mode & FLS](10-apex-security-user-mode-and-fls.md) — the 67.0 default the Selector layer has to be re-read against
