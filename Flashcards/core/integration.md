---
area: Core
topic: Integration
id_prefix: core-int
---
# Core › Integration

Interview cards for the integration layer, written for a technical architect or senior developer. Every answer is short on purpose: the reasoning lives in the linked note. Format and rules are in the README one folder up.

## Foundations

#flashcards/core/integration/foundations

### Patterns & limits

Before naming any API, which three properties of a requirement fix the integration pattern? And what does a customer usually mean by "real time"? <!--id:core-int-001-->
?
Who initiates, whether the caller waits, and how many records move. "Real time" usually means *eventually, within seconds, caller free*. That is an event, not request-reply.
Source: [Integration patterns & selection](../../SF_core/06-integration-and-apis/01-integration-patterns-and-selection.md)

One integration exhausted the org's API allowance. Why do the integrations that did nothing wrong start failing, and how should a client protect itself? <!--id:core-int-002-->
?
The allowance is per org, per rolling 24 hours, and shared. `REQUEST_LIMIT_EXCEEDED` lands on whoever calls next. Read `Sforce-Limit-Info` (returned on every REST response) and throttle before the wall.
Source: [API limits, monitoring & access control](../../SF_core/06-integration-and-apis/24-api-limits-monitoring-and-access-control.md)

### APIs

Batch, Composite and Composite Graph all cut round trips. On which single axis do they really differ, and what is each one's answer? <!--id:core-int-003-->
?
The transaction boundary. **Batch** never rolls back. **Composite** rolls back only with `allOrNone: true`, and the default is false. **Graph** always rolls back, per graph, with up to 500 nodes per graph.
Source: [Composite, Batch & Graph APIs](../../SF_core/06-integration-and-apis/06-composite-batch-and-graph-apis.md)

How many subrequests can one Composite (`/composite`) request carry, and how many API calls does it cost? <!--id:core-int-004-->
?
25 subrequests, and the whole request counts as **one** API call against the 24-hour limit. That is why composite stretches an integration's budget, not just its latency.
Exact: 25
Source: [Composite, Batch & Graph APIs](../../SF_core/06-integration-and-apis/06-composite-batch-and-graph-apis.md)

Why is upsert on an external ID called the integration primitive? <!--id:core-int-005-->
?
It removes the "do I already have this record?" round trip and makes retries idempotent: the same call twice leaves one record. It works over REST (`PATCH /sobjects/Account/ExtId__c/{value}`) and in Bulk API 2.0.
Source: [REST API fundamentals](../../SF_core/06-integration-and-apis/04-rest-api-fundamentals.md)

When does Bulk API 2.0 become the right choice over REST, and what did 2.0 take off the client compared with v1? <!--id:core-int-006-->
?
Salesforce's line is more than 2,000 records. 2.0 batches server-side: no batch sizes, no per-batch polling, and no `Sforce-Enable-PKChunking` header, which is a v1-only mechanic.
Source: [Bulk API 2.0](../../SF_core/06-integration-and-apis/07-bulk-api-2.md)

Bulk API 2.0 ingest job: `POST /jobs/ingest`, upload the CSV, `PATCH` the state to ==UploadComplete==, poll until ==JobComplete==, then read ==failedResults== and `unprocessedRecords`. <!--id:core-int-007-->
Source: [Bulk API 2.0](../../SF_core/06-integration-and-apis/07-bulk-api-2.md)

### Events & CDC

What does Pub/Sub API change compared with the CometD Streaming API, and is Streaming API retired? <!--id:core-int-008-->
?
Pub/Sub is pull-based with flow control (`num_requested`), sends binary Avro, and handles publish and subscribe in one gRPC API. Streaming API is **not** retired: no end-of-life is published, and `lightning/empApi` still runs on CometD. Only PushTopic and generic events carry the *(Legacy)* label.
Trap: telling a client "CometD is dead". It isn't, and the correction lands badly in the room.
Source: [Pub/Sub API](../../SF_core/06-integration-and-apis/11-pub-sub-api.md)

How long does the event bus keep platform events and change events, and what does that mean for a subscriber that goes down? <!--id:core-int-009-->
?
72 hours. A subscriber offline for longer has lost those events for good. Replay IDs cannot reach past retention.
Exact: 72 hours
Source: [Pub/Sub API](../../SF_core/06-integration-and-apis/11-pub-sub-api.md)

When do you reach for Change Data Capture instead of a hand-written platform event? <!--id:core-int-010-->
?
When the requirement is "keep that system in step with Salesforce". CDC captures every write path, including Bulk loads, admins, other integrations, deletes and undeletes, which a trigger-published event misses. You design a platform event; the platform designs a change event. By default it is capped at 5 entities.
Source: [Change Data Capture](../../SF_core/06-integration-and-apis/13-change-data-capture.md)

### Auth & credentials

Pick the OAuth flow by who is present. A human at a browser uses ==web server + PKCE==. An unattended job holding a private key uses ==JWT bearer==. An unattended daemon with a client secret uses ==client credentials==, which needs a ==Run As user==. Username-password retires in Winter '27. <!--id:core-int-011-->
Source: [OAuth flows & authorization](../../SF_core/06-integration-and-apis/15-oauth-flows-and-authorization.md)

In the Winter '23+ model, what does a named credential own, what does an external credential own, and why split them? <!--id:core-int-012-->
?
The **named credential** owns *where*: the base URL. The **external credential** owns *as whom*: the auth protocol and its principals. Principals are granted through permission sets, so "who may call this system" becomes an auditable assignment. The legacy single-object named credential is deprecated, with no retirement date.
Source: [Named Credentials & External Credentials](../../SF_core/06-integration-and-apis/17-named-credentials-and-external-credentials.md)

A 2026 runbook says "create a connected app". What is wrong with that step? <!--id:core-int-013-->
?
Creating a connected app has needed a Support case since Spring '26. New integrations use **External Client Apps**, which keep the app definition separate from org policy. Existing connected apps keep working: they are superseded, not retired.
Source: [External Client Apps](../../SF_core/06-integration-and-apis/16-external-client-apps.md)

## Hard

#flashcards/core/integration/hard

### Patterns & limits

The requirement is "when an opportunity closes, tell the ERP". Today an after-update trigger calls `@future(callout=true)`, about 400 times a day. The ERP has maintenance windows of up to 2 hours, and closures are lost during them. The client asks: "Can we use Pub/Sub?" What do you ask, and what do you fix? <!--id:core-int-014-->
?
It is fire-and-forget, and the real defect is that nothing survives an outage. Ask whether the ERP can *subscribe*:
- **If yes:** publish `OpportunityClosed__e` with Publish After Commit. The 72-hour retention covers the 2-hour window.
- **If no:** use a Queueable with retry and backoff, plus a dead-letter record and an alert.
Hint: pattern first. Who initiates, does the caller wait, how many records move?
Trap: answering yes or no on Pub/Sub. Neither answer fixes the lost closures.
Source: [Integration patterns & selection](../../SF_core/06-integration-and-apis/01-integration-patterns-and-selection.md) · [Interview set](../../Interview/03-core-platform/03-integration-and-async.md)

A Pub/Sub client consumes `OrderPlaced__e` and creates warehouse shipments. Twice the warehouse shipped orders that don't exist in Salesforce. The event is sent with *Publish Immediately* from a transaction that sometimes fails a validation rule, and the consumer saves its replay ID on receipt. Name both defects. <!--id:core-int-015-->
?
1. *Publish Immediately* is not rolled back with the failed save. Use **Publish After Commit**.
2. Saving the replay ID **on receipt** means a crash mid-processing skips work for good. Save it **after** processing.
Delivery is also at-least-once, so the consumer needs a dedupe key.
Hint: is publishing transactional with DML?
Trap: fixing only the publish setting. The replay-ID bug shows up months later as *missing* shipments.
Source: [Platform Event design](../../SF_core/06-integration-and-apis/12-platform-event-design.md) · [Interview set](../../Interview/03-core-platform/03-integration-and-async.md)

A partner posts orders to your Apex REST endpoint. At peak they got timeouts and 503s, retried every 5 seconds, and 240 duplicate orders appeared. Salesforce logs show every request succeeded. Who is at fault, and what do you change? <!--id:core-int-016-->
?
The endpoint. A timeout is not a failure, so retrying was correct. Have the partner send an idempotency key, and store it in a **unique external ID** field: `DUPLICATE_VALUE` then means "return the first result". Give the key an expiry. The partner should also use exponential backoff with jitter and retry only retryable errors.
Hint: what does a timeout tell the caller about whether the work happened?
Trap: confirming that "the partner double-posted". The endpoint will duplicate again on the next slow week.
Source: [Idempotency, retries & error handling](../../SF_core/06-integration-and-apis/23-idempotency-retries-and-error-handling.md)

An Enterprise org has one external Pub/Sub client on a busy high-volume platform event. Publishing is far below 250,000 per hour, yet deliveries stop every afternoon. The team now wants CDC on two more objects. What is happening? <!--id:core-int-017-->
?
Delivery is a **separate meter**: 25,000 per rolling 24 hours in Enterprise. It is shared between platform events and CDC, and only external subscribers (Pub/Sub, CometD, `empApi`, Event Relay) spend it. Apex and Flow subscribers are free. Adding CDC spends the same pool. Watch it with `PlatformEventUsageMetric`, because `EventBusSubscriber` cannot see external clients.
Hint: there are two meters with two different windows.
Source: [Event bus allocations, limits & monitoring](../../SF_core/06-integration-and-apis/27-event-bus-allocations-limits-and-monitoring.md)

### APIs

Code review. The client marks success on HTTP 200, and the Contact subrequest fails a validation rule. What is left in the org, and what is the fix? <!--id:core-int-018-->
```json
POST /services/data/v67.0/composite
{ "compositeRequest": [
  { "method": "POST", "url": "/services/data/v67.0/sobjects/Account",
    "referenceId": "acct", "body": { "Name": "Acme" } },
  { "method": "POST", "url": "/services/data/v67.0/sobjects/Contact",
    "referenceId": "ct",
    "body": { "LastName": "Lee", "AccountId": "@{acct.id}" } } ] }
```
?
An orphan Account. `allOrNone` defaults to false, so the response is HTTP 200 with the failure inside the body. Add `"allOrNone": true`, or use Composite Graph, which always rolls back per graph. Then check each subresult, not the status code.
Hint: what is the default for allOrNone?
Trap: trusting the HTTP status code.
Source: [Composite, Batch & Graph APIs](../../SF_core/06-integration-and-apis/06-composite-batch-and-graph-apis.md)

A nightly Bulk API 2.0 upsert of Contacts reports `JobComplete` and the client marks it done. Weeks later some contacts are stale, and the loads keep logging `UNABLE_TO_LOCK_ROW`. What was missed, and how do you fix the slowness? <!--id:core-int-019-->
?
`JobComplete` means processing finished, not that every record succeeded. Always read `failedResults`, and resubmit `unprocessedRecords`. The lock errors are parent-child contention: sort the file by `AccountId` so each chunk touches one parent. Serial mode is the fallback.
Hint: a finished job has three result buckets.
Trap: adding `Sforce-Enable-PKChunking`. That is a v1 header and does nothing in 2.0.
Source: [Bulk API 2.0](../../SF_core/06-integration-and-apis/07-bulk-api-2.md)

Code review. What stops this endpoint from working, and what else would you flag? <!--id:core-int-020-->
```apex
@RestResource(urlMapping='/orders/*')
public with sharing class OrderApi {
    @HttpPost
    public static Id submit(String accountId) { return null; }
    @HttpPost
    public static Id cancel(String orderId) { return null; }
}
```
?
It doesn't exist yet. The class and its methods must be `global`, and two `@HttpPost` methods in one class is a compile error: one method per verb per class. Also flag the missing version in `urlMapping` (you own versioning), and grant *Apex Class Access*, because deploying it reaches nobody.
Hint: check the access modifiers, then count the verbs.
Source: [Apex REST & custom endpoints](../../SF_core/06-integration-and-apis/18-apex-rest-and-custom-endpoints.md)

An architect proposes Salesforce Connect external objects for 2 million ERP invoices, "so we don't need a sync". Sales wants an Account roll-up and a flow when an invoice goes overdue. What is your verdict? <!--id:core-int-021-->
?
No, for this requirement. External objects fire no triggers or flows and support no roll-up summaries, and an ERP outage becomes the page's outage. Reacting to data needs a copy or an event. Hyperforce lifted the per-hour OData limits, so limits are no longer the argument. Automation is.
Trap: arguing about the old hourly limits instead of the automation gap.
Source: [Salesforce Connect & external objects](../../SF_core/06-integration-and-apis/20-salesforce-connect-and-external-objects.md)

### Events & CDC

Your CDC subscriber writes changes into an external database, which writes its own edits back through the API. Updates now ping-pong forever. How do you break the loop robustly? <!--id:core-int-022-->
?
The writer sets a client ID on its API calls. Each change event's `changeOrigin` then carries `client=<id>`, and the subscriber skips its own writes. `commitUser` only works while the integration has a dedicated user; `changeOrigin` survives a shared one.
Hint: which header field says who made the change?
Source: [Change Data Capture](../../SF_core/06-integration-and-apis/13-change-data-capture.md)

A CDC-fed replica of Account drifted silently after an admin converted a picklist field. The subscriber handles CREATE, UPDATE and DELETE. What did it miss? <!--id:core-int-023-->
?
**Gap events.** `GAP_UPDATE` and its siblings are `changeType` values sent when the platform can't generate full detail. A picklist conversion can emit one for every affected record. Branch on them and re-fetch the record. Also order by `commitNumber` / `commitTimestamp`, not arrival order.
Hint: they aren't a separate channel. They are a changeType.
Source: [Change Data Capture](../../SF_core/06-integration-and-apis/13-change-data-capture.md)

### Auth & credentials

A nightly ETL job gets its token by posting a username and password to `/services/oauth2/token`, running as a System Administrator. Redesign its authentication. <!--id:core-int-024-->
?
The username-password flow retires in Winter '27. Use an **External Client App** with one of:
- **JWT bearer**: a private key, the certificate uploaded, the user pre-authorized.
- **Client credentials**: a Run As user on the free *Salesforce Integration* licence, with a least-privilege permission set.
Narrow the scope too: `api` drags Metadata and Tooling along with it.
Hint: who is present at token time, and as whom should it act?
Trap: client credentials with a System Administrator as the Run As user. The client secret then *is* the whole org.
Source: [OAuth flows & authorization](../../SF_core/06-integration-and-apis/15-oauth-flows-and-authorization.md)

A portal callout uses a named credential with a Per User Principal and works fine for users. A new nightly batch that calls the same API fails in production with an *authentication* error. Why, and what is the fix? <!--id:core-int-025-->
?
A Per User Principal has no stored credential for the automation user the batch runs as. Give automation its own **Named Principal**, granted through a permission set. Note the misleading symptom: a missing principal grant shows up as an authentication failure, not a permissions error.
Hint: whose credential does the batch actually have?
Source: [Named Credentials & External Credentials](../../SF_core/06-integration-and-apis/17-named-credentials-and-external-credentials.md)

### Agent-facing APIs

A team wants an AI agent to call your org's hosted MCP server unattended overnight, "as a service account". What do you tell them? <!--id:core-int-026-->
?
That isn't available. Hosted MCP enforces the authorization code flow, with no machine-to-machine option, so every session is a real user. Set it up through an External Client App with the `mcp_api` and `refresh_token` scopes, not `api`. Tools enforce that user's sharing and FLS. Make the tools idempotent, because agents retry, and shorten the one-year refresh token.
Hint: which OAuth flows does hosted MCP accept?
Trap: suggesting client credentials. That path doesn't exist for MCP today.
Source: [MCP servers & agent-facing APIs](../../SF_core/06-integration-and-apis/25-mcp-servers-and-agent-facing-apis.md)
