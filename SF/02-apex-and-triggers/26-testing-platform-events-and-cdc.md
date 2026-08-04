# Testing Platform Events & CDC

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 20

**Scope:** Proving an event subscriber works — forcing delivery in a test, testing retries, and enabling CDC for a test run. Building the subscriber is [18](18-platform-events-and-cdc-in-apex.md); general test mechanics are [20](20-apex-testing-fundamentals.md) and [21](21-apex-testing-advanced-and-mocking.md).

## Core idea

An event subscriber is the one piece of Apex that can be fully broken and still show a green test. Publishing inside a test does **not** run the subscriber — the message goes onto a test-context bus and stays there. A test that publishes an event, then asserts on the records the trigger was supposed to create, fails honestly. A test that publishes and asserts nothing, or asserts only the `SaveResult`, passes while proving that `EventBus.publish()` returns success — which it does whether or not a subscriber exists at all.

So testing events is really one discipline: **force delivery explicitly, then assert on the effect.** Two things trigger delivery — `Test.getEventBus().deliver()`, which you can call repeatedly at chosen points, and `Test.stopTest()`, which flushes whatever is outstanding. The first is the one worth learning, because retry testing is impossible without it.

## How it works

| Need | Call |
|---|---|
| Deliver events published since the last delivery | `Test.getEventBus().deliver()` |
| Deliver everything outstanding, once | `Test.stopTest()` |
| Fire change event triggers regardless of Setup | `Test.enableChangeDataCapture()` |
| Inspect what the subscriber did | `SELECT … FROM EventBusSubscriber WHERE Topic = '…'` |

- **`Test.getEventBus().deliver()` delivers what was published since the previous `deliver()` call**, not everything ever published. Calling it in a loop is how a retry sequence is stepped through one attempt at a time.
- **`Test.enableChangeDataCapture()` must be called at the start of the test method, before any DML.** It makes change event triggers fire irrespective of which entities are selected in Setup — so a CDC test does not depend on org configuration.
- **`EventBusSubscriber` is queryable in a test** and carries `Position`, `Retries`, `LastError`, `Topic`, `Type` and `Name`. `Retries` is how you assert that a retry actually happened rather than assuming it.
- **A thrown `EventBus.RetryableException` does not advance `Position`**, because the message was not successfully processed — which is precisely the signal a retry test asserts on.
- **In test context the bus is not the real bus.** Event and subscriber state is reset per test and never persisted, so nothing leaks between methods.
- **`EventBus.TestBroker` covers the failure side**, simulating delivery and failed publishing where a plain `deliver()` cannot.

```apex
@IsTest
static void retriesThenSucceeds() {
    insert new Order_Event__e(Order_Id__c = 'A-1');
    Test.getEventBus().deliver();                       // attempt 1

    EventBusSubscriber s = [SELECT Retries, Position, LastError
                            FROM EventBusSubscriber WHERE Topic = 'Order_Event__e'];
    Assert.areEqual(1, s.Retries, 'the trigger should have asked for a retry');

    Test.getEventBus().deliver();                       // attempt 2 — now let it pass
    Assert.areEqual(1, [SELECT COUNT() FROM Task]);
}
```

## 2026 currency

**Parallel subscriptions for Apex platform event triggers are GA at 67.0** and they change what a passing test proves. A trigger can now be spread across **up to 10 internal partitions**, configured through `PlatformEventSubscriberConfig` with a partition key — a required custom field on the event, or the standard `EventUuid`. Salesforce is explicit that **order is preserved within a partition and not across them**, so a test asserting that event A's effect precedes event B's is asserting something production no longer guarantees once the trigger is partitioned. The feature covers **custom high-volume platform events only** — not standard events, and not change events. → [18](18-platform-events-and-cdc-in-apex.md), [06-integration · 27](../06-integration-and-apis/27-event-bus-allocations-limits-and-monitoring.md)

## Gotchas

- **Publishing without delivering passes green and tests nothing.** No exception, no warning — the assertion simply runs before the subscriber ever does.
- **A `SaveResult` of `isSuccess() == true` says the message reached the bus**, not that anything consumed it. Asserting on it is the commonest false-confidence test in this area.
- **`Test.enableChangeDataCapture()` after the DML is too late** and silently does nothing useful; it belongs on the first line.
- **Test context delivers at most 500 change event messages** from record changes, so a bulk CDC test built on 1,000 inserts does not exercise what it appears to.
- **`Test.stopTest()` flushes once.** A retry sequence needs repeated `deliver()` calls; you cannot step through attempts with `stopTest()` alone.
- **The ten-run ceiling still applies in tests** — one attempt plus nine retries, after which the subscriber errors out. A loop that keeps failing will exhaust it rather than loop forever. → [18](18-platform-events-and-cdc-in-apex.md)
- **CDC triggers depend on Setup selection in production but not in a test.** Passing tests are therefore no evidence that the object is actually enabled in the target org. → [06-integration · 13](../06-integration-and-apis/13-change-data-capture.md)

## Recall

Q: What happens if a test publishes a platform event and never calls `deliver()` or `stopTest()`?
A: The subscriber never runs. The test passes having proved only that publishing succeeded.

Q: What exactly does `Test.getEventBus().deliver()` deliver?
A: The messages published since the previous `deliver()` call — which is what makes stepping through a retry sequence possible.

Q: Where must `Test.enableChangeDataCapture()` be called, and why?
A: At the start of the test method, before any DML, so change event triggers fire regardless of the entities selected in Setup.

Q: Which `EventBusSubscriber` field proves a retry occurred, and which one does *not* advance on a retry?
A: `Retries` counts them; `Position` does not advance, because the message was not successfully processed.

Q: How many change event messages can be delivered in test context?
A: Up to 500 from record changes — a bulk CDC test above that is not exercising what it looks like.

## Related

- [18 · Platform Events & CDC in Apex](18-platform-events-and-cdc-in-apex.md) — the subscriber being tested, and the retry mechanics
- [20 · Apex testing fundamentals](20-apex-testing-fundamentals.md) — `@TestSetup`, isolation and what `startTest`/`stopTest` reset
- [21 · Apex testing advanced & mocking](21-apex-testing-advanced-and-mocking.md) — the Stub API, for the callout a subscriber usually makes
- [06-integration · 27 Event bus allocations, limits & monitoring](../06-integration-and-apis/27-event-bus-allocations-limits-and-monitoring.md) — proving it works in production, where tests cannot reach
