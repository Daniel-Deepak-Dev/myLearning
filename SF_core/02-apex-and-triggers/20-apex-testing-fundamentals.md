# Apex Testing Fundamentals

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 05

**Scope:** Isolation, setup, assertions and limit resets — the mechanics of a test that proves something. Faking the boundaries is [21](21-apex-testing-advanced-and-mocking.md); reading what a test measured is [24](24-apex-performance-and-profiling.md).

> **What changed.** `@IsTest(SeeAllData=true)` is not a workaround for awkward test data, it is a defect. Data isolation has been the default since **API 24.0**, and the annotation reintroduces exactly the coupling isolation exists to remove — the test passes in the org it was written in and fails in a fresh scratch org.

## Core idea

Coverage is a deployment gate, not a quality signal: 75% org-wide plus some coverage on every trigger, checked at deploy time and indifferent to whether a single assertion exists. That gap is why so much Apex ships with tests that call a method inside `try/catch` and assert nothing. A useful test does three things the gate does not require — it builds its own data, it runs the code as a *specific user*, and it asserts on an outcome. The 67.0 security flip makes the second one load-bearing: now that SOQL and DML default to user mode, a test that runs as the deploying admin no longer exercises the same code path as production.

## How it works

| | Resets governor limits? | Notes |
|---|---|---|
| `@TestSetup` | **No** | its DML and SOQL count against *every* test method in the class |
| `Test.startTest()` / `stopTest()` | **Yes**, once | also forces queued async work to run at `stopTest()` |
| `System.runAs(u)` | No | **costs one DML statement per call** |

- **One `@TestSetup` per class**, run before any test method. Its records are visible to all of them, changes made by a method are rolled back when that method ends, and everything is rolled back at the end of the class.
- **Static state is reinitialized before each test method** — static initializers and static blocks run again, so a `hasRun` flag set in setup is gone by the first assertion.
- **`Assert` is the current class** (Winter '23, API 56.0): `Assert.areEqual`, `isTrue`, `isNotNull`, `fail`. The old `System.assertEquals` family is *not* deprecated and has no retirement date — but the failure messages are worse.

```apex
@IsTest
private class RefundServiceTest {
    @TestSetup
    static void seed() {
        Test.startTest();                                  // the only way to stop setup
        insert TestFactory.orders(200);                    // limits leaking into every method
        Test.stopTest();
    }
    @IsTest
    static void agentWithoutEditAccessCannotRefund() {
        User agent = TestFactory.agent();                  // no Edit on Order__c
        System.runAs(agent) {                              // costs 1 DML
            Assert.isFalse(RefundService.canRefund(orderId), 'user mode should deny');
        }
    }
}
```

## 2026 currency

**The security flip lands hardest in tests, because tests are where system mode was invisible.** Under 67.0 a `with sharing` default plus user-mode SOQL means the *identity* a test runs under determines the result, so suites written entirely without `System.runAs` are now measuring the deploying admin's permissions and nothing else. Separately, **`RunRelevantTests` is Beta from Spring '26**: `sf project deploy start --test-level RunRelevantTests` runs only the tests a deployment touches, steered by `@IsTest(testFor='ApexClass:MyClass')` and overridden by `@IsTest(critical=true)` for tests that must always run. Detail: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

> **From my notes.** *"DML limits are reset by `@TestSetup` but SOQL limits are not."* — **inverted, and worth unlearning carefully.** Neither is reset. Everything a setup method consumes counts against each test method in the class, which is why a 200-record factory can push a method over a limit that its own code never approached. The only reset is `Test.startTest()`/`stopTest()`, and it works *inside* the setup method — that is the fix, not a per-annotation exemption.

## Gotchas

- **`SeeAllData=true` disables `@TestSetup` outright.** Setup methods are supported only in the default isolation mode, so adding the annotation silently removes your data factory rather than erroring.
- **A fatal error in `@TestSetup` fails the whole class** and no test method runs — one bad factory line reads as a dozen unrelated failures.
- **No coverage is calculated for a non-test method called from `@TestSetup`.** Building data through your own service layer looks like it covers that layer; it does not.
- **`Test.startTest()`/`stopTest()` is one pair per method.** A second pair throws, so you cannot reset limits twice.
- **`System.runAs` does not escape the transaction's limits** and each call spends a DML statement — a loop over ten users spends ten.
- **Isolation is not total.** Setup objects — `User`, `Profile`, `RecordType`, custom settings and custom metadata — are visible without `SeeAllData`, which is why a test can pass on a picklist value that exists only in your org.
- **75% is org-wide at deploy time**, not per class. A class at 0% deploys fine until the org average dips.

## Recall

Q: Why is `@IsTest(SeeAllData=true)` treated as a defect rather than a shortcut?
A: Data isolation has been the default since API 24.0; the annotation couples the test to org state, so it passes where it was written and fails in a fresh scratch org — and it silently disables `@TestSetup`.

Q: Does `@TestSetup` give a test method its own governor limits?
A: No. Whatever setup consumes counts against every test method in the class. Wrapping the setup body in `Test.startTest()`/`stopTest()` is the only reset.

Q: What does `Test.stopTest()` do besides restore limits?
A: It forces queued asynchronous work — Queueable, `@future`, batch — to execute before the next line.

Q: Which assertion API is current, and is the old one retired?
A: The `Assert` class (Winter '23, API 56.0). `System.assertEquals` and friends still work and have no announced retirement.

Q: What does the 67.0 security flip change about how tests should be written?
A: User mode and the `with sharing` default mean the running identity decides the outcome, so `System.runAs` moves from optional to necessary for anything access-sensitive.

## Related

- [21 · Apex testing advanced & mocking](21-apex-testing-advanced-and-mocking.md) — faking callouts and dependencies once the data problem is solved
- [10 · Apex security: user mode & FLS](10-apex-security-user-mode-and-fls.md) — why `System.runAs` became load-bearing at 67.0
- [09 · Exception handling & custom exceptions](09-exception-handling-and-custom-exceptions.md) — asserting on a thrown exception rather than swallowing it
- [26 · Testing platform events & CDC](26-testing-platform-events-and-cdc.md) — the subscriber that passes green without ever running
