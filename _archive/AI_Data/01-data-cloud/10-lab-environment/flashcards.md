# Lab Environment & Testing Craft — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: Can a Salesforce org with no Data 360 licence be connected as a data source to a Data 360 tenant?
A: Yes — via a standard Salesforce CRM connection. The source org needs a permission set and a user to OAuth as, not a licence. The licence lives entirely on the Data 360 side.

Q: What are the four ways to get data into a Data 360 tenant?
A: Home org connector; standard Salesforce CRM connection to an external org; Data Cloud One companion connection; Ingestion API.

Q: Which of the four connection mechanisms cannot be tested on a free Developer Edition tenant, and why?
A: The Data Cloud One companion connection — it needs companion licences and pairs only production↔production or sandbox↔sandbox.

Q: A standard CRM connection and a Data Cloud One companion connection both "connect an org". How do they differ in direction?
A: A standard CRM connection ingests data INTO Data 360 (with data actions back out). A companion connection pushes unified METADATA out to the companion org; the records stay in the home tenant.

Q: What must you configure in the SOURCE org for a standard CRM connection?
A: A permission set with the Data 360 Salesforce Connector integration permissions, Read + View All on each object, Read on each field, assigned to the user who authorises the connection.

Q: Why does the OAuth-as-a-user design of the CRM connector matter for governance?
A: Data 360 borrows a real user's access, so the source org's own sharing and field-level security permanently bound what Data 360 can see. You grant a user access, not the platform.

Q: A data stream shows status "Success". What have you actually proven?
A: Almost nothing — a stream can succeed having ingested zero rows. You must check the row count in the refresh history.

Q: A DLO query returns zero rows and no error. What is the first thing to check?
A: The data space — a DLO query without the correct `SET OPTIONS` dataspace clause returns zero rows silently.

Q: How does an unmapped field in a DMO present itself?
A: As a null value, not as an error — indistinguishable from genuinely missing data.

Q: How do you validate a calculated insight or a segment rather than trusting the UI?
A: Recompute the same thing as raw SQL in Query Workspace and compare. Differences are usually refresh or publish schedule, not a bug.

Q: What is the universal fallback for ingesting from a system with no connector, and what are its two patterns?
A: The Ingestion API. Bulk (CSV, periodic) and streaming (incremental, near-real-time).

Q: What is the Apex-side shape of an Ingestion API integration?
A: Custom auth provider (JWT) → Named Credential → Apex callout, against the tenant-specific endpoint, with an OpenAPI (OAS) YAML schema uploaded to the connector to define the objects.

Q: Why should you not connect a client or employer sandbox to a personal Developer Edition Data 360 tenant?
A: It moves client data into a tenant your company doesn't control, monitor or own — a data-protection problem, made worse because sandboxes often carry copied production data.

Q: What is the legitimate zero-cost way to get Data 360 into a real Enterprise or Unlimited org?
A: The $0 Data 360 Provisioning SKU ("Data Cloud Everywhere") — roughly 250,000 Data Services credits, 1 TB storage, 1 admin, ~100 users, 5 integration users.

Q: Which Data 360 operation burns credits fastest, and what follows for lab design?
A: Identity resolution — you're billed on records reviewed during unification. Keep lab datasets in the hundreds of records.

Q: What does a free Developer Edition give you in Data 360 terms?
A: One data space and about 10 GB of storage — and the org expires if you don't log in roughly every 45 days.

Q: Your Developer Edition org has no Data 360 Setup node. What's the fallback?
A: A Partner Developer Edition org created through Environment Hub. PDE was historically the only dev-tier route to Data Cloud, and older DE orgs weren't all retrofitted.

Q: Why does every lab in the ladder include a "break it on purpose" step?
A: Because failure signatures — a silent zero-row query, a permission-denied data action — can only be recognised later if you've caused them once deliberately.

Q: Name three things you genuinely cannot learn on a free Developer Edition tenant.
A: Data Cloud One companion connections; real sandbox→production promotion; scale, performance and production credit economics. (Also Marketing Cloud activation.)

Q: Why is invented test data better than downloaded sample data for identity-resolution labs?
A: Because you know the correct answer in advance — including which pairs must NOT match — so you can detect over-matching instead of admiring a lower profile count.
