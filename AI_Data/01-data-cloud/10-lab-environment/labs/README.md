# The Data 360 Lab Ladder

Nine runbooks, in order. Each one builds on the previous tenant state — don't skip ahead, the later labs need the data the earlier ones created.

Every runbook has the same shape:

**Goal · Prereqs · Steps · How you know it worked · Break it on purpose · Credits spent · Notes from my run**

The last three sections are the ones that matter. *Break it on purpose* is where the learning is — a failure signature you've caused once is one you'll recognise at a client. *Credits spent* and *Notes from my run* are yours to fill in; empty ones mean the lab hasn't really been done.

## Environment

| Role | Org | Why |
|---|---|---|
| **Data 360 home org** | Developer Edition with Data 360 enabled | Holds the tenant. Everything is configured here. |
| **Source org** | A *second* free Developer Edition, **no Data 360** | Proves the licence lives on the Data 360 side. Also keeps client data out of a personal tenant — see [Governance](../notes.md#governance-the-client-sandbox-question). |

Get the second org from [the developer signup form](https://www.salesforce.com/form/developer-signup/). Seed it by hand with 20–50 Contacts you invented, because you need to know the right answer in advance.

## The ladder

| # | Lab | Teaches | Status |
|---|---|---|---|
| 00 | [Tenant baseline](lab-00-tenant-baseline.md) | What you actually have; the numbers everything else is measured against | ⬜ |
| 01 | [Home org connector](lab-01-home-org-crm-connector.md) | DSO → DLO → DMO, and verifying a count three ways | ⬜ |
| 02 | [**External org connection**](lab-02-external-org-connection.md) | Connecting an unlicensed org; the connector permission model | ⬜ |
| 03 | [Ingestion API from any org](lab-03-ingestion-api-any-org.md) | The raw API, bulk vs streaming, upsert semantics | ⬜ |
| 04 | [Identity resolution](lab-04-identity-resolution.md) | Match rules across three sources; designing a test set that can fail | ⬜ |
| 05 | [Insights & segments](lab-05-insights-and-segments.md) | Validating a metric against SQL instead of trusting the UI | ⬜ |
| 06 | [Data action round trip](lab-06-data-actions-round-trip.md) | Data 360 → Flow → back into the source org | ⬜ |
| 07 | [Promotion & packaging](lab-07-promotion-and-packaging.md) | Data kits, CLI metadata retrieve, what can't move | ⬜ |
| 99 | [Parked](lab-99-parked-external-sources.md) | S3, zero-copy, Web SDK — what each needs before it's runnable | ⏸️ |

Mark ⬜ → ✅ as you go, and put the date in the runbook.

## Ground rules

1. **Keep datasets in the hundreds.** Identity resolution bills on records reviewed. A careless fuzzy ruleset over a large stream is how a free tenant dies.
2. **Record the credit number before and after** every lab. Lab-00 exists for this.
3. **Never connect the client sandbox.** It's the same mechanism as lab-02 and it puts their data in a tenant Geeksoft doesn't control.
4. **Log in every ~45 days** or the Developer Edition expires and takes the ladder with it.
