# Lab 02 — External Org Connection

> Status: ⬜ not started · Date run: —

**The headline lab.** It answers: *can an org with no Data Cloud licence be connected to a Data 360 tenant for testing?* Yes. This is how, and this is how you prove it.

## Goal

Ingest Contacts from a **second Salesforce org that has no Data 360 licence at all**, via a standard Salesforce CRM connection. Along the way, learn the connector permission model — the thing every broken connection in the wild turns out to be about.

## Prereqs

- [Lab 01](lab-01-home-org-crm-connector.md) done.
- A **second free Developer Edition org**, no Data 360, from [the developer signup form](https://www.salesforce.com/form/developer-signup/). Seed it with 20–50 Contacts, deliberately overlapping ~10 of the home org's people (same email, slightly different names) — lab-04 needs that overlap.
- Admin access to both orgs.

> **Do not use the client/employer sandbox here.** Same mechanism, same learning, but it moves their data into a tenant Geeksoft doesn't control. See [Governance](../notes.md#governance-the-client-sandbox-question).

## Steps

### In the SOURCE org (the one with no licence)

1. **New permission set.** Setup → Permission Sets → New. Call it `Data360_Connector_Source`.
2. **System/user permissions.** Enable the **Data 360 Salesforce Connector** integration permissions (the connector's own integration permission, plus API Enabled).
3. **Object settings.** For `Contact`: **Read** and **View All**. View All matters — without it you get whatever the user's sharing rules happen to allow, and the ingested count silently under-reports.
4. **Field permissions.** **Read** on every field you intend to ingest. Leave one field's read access **off** on purpose; that's the break-it step.
5. **Assign** the permission set to the user you're going to authenticate as. Note that username — you'll need it in a moment.

### In the DATA 360 org

6. **New connection.** Setup → Data 360 Setup → the **Salesforce CRM** connector → **New**. Give it a name that says which org it is; you will forget.
7. **Authenticate.** OAuth flow → log in **as the source-org user from step 5**. This is the conceptual heart of the lab: Data 360 doesn't get access, it *borrows a user's* access.
8. **New data stream** on that connection → `Contact` → the fields you granted → category **Profile**.
9. **Deploy and run.** Watch refresh history for status *and* row count.
10. **Map** the DLO to the same **Individual** DMO you used in lab-01, so both orgs' people land in one model.

## How you know it worked

- Source-org `SELECT COUNT() FROM Contact` == stream row count == DLO `COUNT(*)` (with `SET OPTIONS`).
- The DMO now holds records from **both** orgs. Query it and group by source to see them side by side.
- **And the point of the whole lab:** go back to the source org and check its licences. There is no Data 360 licence there. There never was. Write that down — it's the empirical answer to the question that started this topic.

## Break it on purpose

1. **The withheld field.** Query the DMO for the field whose FLS you left off in step 4. Note precisely how it presents — is it absent from the stream's field list, or present and null? Whichever it is, that's the signature of "the connector user can't see it", and it looks identical to "the data isn't there".
2. **Revoke and re-run.** Remove the permission set from the connecting user, then trigger a refresh. Record the exact error and *where* it surfaces — stream detail, refresh history, or nowhere useful.
3. **Re-assign** and confirm recovery.

## What this lab does *not* prove

The source org still can't *see* anything in Data 360 — no Data 360 UI, no unified profile, no metadata. That's a **Data Cloud One companion connection**, which needs companion licences and prod↔prod / sandbox↔sandbox pairing, and cannot be done here. Don't let a successful lab-02 turn into a claim you've tested Data Cloud One.

## Credits spent

—

## Notes from my run

—
