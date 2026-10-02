---
area: Data 360
id_prefix: d360
---
# Data 360

Interview cards for Data 360 (formerly Data Cloud), written for a technical architect or senior developer. Answers are short on purpose: the reasoning lives in the linked note. Format and rules are in the README in this folder.

## Ingestion & Modelling

### Foundations

#flashcards/data-360/ingestion-modeling/foundations

What are a DSO, a DLO and a DMO, and which one does every downstream feature read? <!--id:d360-001-->
?
**DSO**: the data as it arrives. **DLO**: the stored lake container a data stream creates, still in the source's shape. **DMO**: the harmonized, canonical object that DLOs are mapped into. Identity resolution, insights, segments and agents all read **DMOs**, so a mapping mistake spreads into every one of them.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

The Data 360 pipeline: a connector feeds a ==data stream==, which lands rows in a ==data lake object (DLO)==, which is mapped into a ==data model object (DMO)==. <!--id:d360-002-->
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md)

What is the maximum JSON body per request for the Ingestion API's streaming pattern, and how does the bulk pattern differ? <!--id:d360-003-->
?
200 KB per request, processed about every 3 minutes. The bulk pattern takes CSV files of up to 150 MB, for periodic syncs. Both can feed the same data stream.
Exact: 200 KB
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md)

### Hard

#flashcards/data-360/ingestion-modeling/hard

Code review. An Apex-backed agent action runs this query. It returns zero rows with no exception, and the records are visible in the Data 360 UI. The developer wants to raise a platform case. <!--id:d360-004-->
```sql
SELECT Id__c, Email__c
FROM Contact_Home__dll
WHERE Email__c != null
LIMIT 10
```
?
The query has no dataspace. A DLO query without `SET OPTIONS (dataspace = '…')` at the very end returns zero records, silently. That is documented behaviour, not a bug. The dataspace option applies to DLO queries only, not DMOs.
Hint: what is this query actually running against?
Trap: rewriting the `WHERE` clause, or raising the case. Five failed filter fixes point at the wrong model of the query, not at the platform.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md) · [Interview set](../Interview/02-data-360/01-ingestion-and-modeling.md)

A utilities client has 23 data streams on a nightly batch. A new agent will answer "what is the status of my outage report?" A junior proposes switching all 23 to streaming; the data team objects on cost. What do you do? <!--id:d360-005-->
?
Decide **per stream**, not per project. Make the stream the agent reads real time (Accelerated Data Ingest for CRM data, or a streaming pattern). Leave the streams only dashboards read on a schedule.
Hint: who reads each stream?
Trap: keeping the stream nightly and having the agent action call CRM directly for freshness. That loses the unified profile and its governance.
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md) · [Interview set](../Interview/02-data-360/01-ingestion-and-modeling.md)

In four weeks an upstream system renames `cust_email_primary` to `primary_email`, and changes a second field from nullable to empty-string-defaulted. The DLO feeds an email match rule, three activated segments and an insight. Which change is the dangerous one? <!--id:d360-006-->
?
The **empty-string change**. The rename breaks the mapping loudly, so you will notice it. Moving from `NULL` to `''` changes what matching and filters see without any error, because DLOs keep `NULL` and `''` distinct. Plan and test it deliberately.
Hint: which failure announces itself?
Trap: treating it as a remapping ticket for the renamed field only.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md) · [Interview set](../Interview/02-data-360/01-ingestion-and-modeling.md)

## Identity Resolution

### Foundations

#flashcards/data-360/identity-resolution/foundations

Match rules vs reconciliation rules: what question does each answer, and what are the reconciliation options? <!--id:d360-007-->
?
**Match rules** decide *when two records are the same person*: exact, fuzzy (first name only) or normalized (email, phone, address). **Reconciliation rules** decide *which value wins*: **Last Updated**, **Most Frequent** or **Source Priority**, set per object and per field.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md)

Why is over-matching more dangerous than under-matching? <!--id:d360-008-->
?
Under-matching splits one person into several profiles, so the agent sees part of their history. Over-matching merges two people, so one customer's data reaches another. That is a privacy incident, and it looks like success: fewer, cleaner profiles.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md)

### Hard

#flashcards/data-360/identity-resolution/hard

A financial-services client has 4.1M profiles for an estimated 2.6M customers. The data team proposes adding fuzzy name + address matching to cut that to about 2.7M; the CFO likes the saving. Many customers are joint account holders and multi-generational households. Do you approve it? <!--id:d360-009-->
?
No. Fuzzy name plus address is the household-collapse rule, and this population is full of households. Merged profiles show one customer's data to another, in a regulated industry, and the merge is invisible because it looks like resolution working. Fix precision instead, for example with a shared customer ID or a corrected model.
Hint: who shares an address?
Trap: approving it "with monitoring". A merged profile looks exactly like a correctly resolved one, so there is nothing to monitor for.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md) · [Interview set](../Interview/02-data-360/02-identity-and-segmentation.md)

Three ruleset changes are approved: an exact match on a new shared customer ID, a tighter email rule, and `Email` reconciliation from Last Updated to Source Priority. There are 4.1M profiles, live activations and an agent, and no full-volume sandbox. How do you land it? <!--id:d360-010-->
?
- Baseline first: profile-to-source ratio, segment sizes, insight values.
- **Sequence the three changes**: customer ID first, email second, reconciliation last.
- **Pause activations across each cutover**, because published audiences can't be recalled.
- Validate correctness in a subset sandbox.
- Check the ratio after each step.
The reconciliation change moves values without moving counts, so check it separately.
Hint: which consumer can't be undone?
Trap: one window for all three. If segments move 20%, you can't say which change did it.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md) · [Interview set](../Interview/02-data-360/02-identity-and-segmentation.md)

## Insights & Segmentation

### Foundations

#flashcards/data-360/insights-segmentation/foundations

Calculated insight vs streaming insight: what data does each run on, and what is each for? <!--id:d360-011-->
?
A **calculated insight** runs over stored data, any data, in high-volume batches. It feeds segment criteria and personalization. A **streaming insight** runs over real-time **engagement** data (Web or Mobile SDK), as near-real-time aggregates that drive data actions. It can't be built on streaming profile data.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

What do a segment, an activation and an activation target each hold? <!--id:d360-012-->
?
The **segment** is the audience definition. The **activation** publishes a segment. The **activation target** holds the platform and its authentication: Marketing Cloud, Data 360 itself, B2C Commerce, Amazon Ads, Google.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

### Hard

#flashcards/data-360/insights-segmentation/hard

A retention campaign triggers when a profile moves from "champion" to "loyal" in an RFM insight. Last night it fired on 34,000 profiles, including customers who bought this week. Nothing was deployed and the insight definition hasn't changed. What happened? <!--id:d360-013-->
?
RFM quintile ranks are **relative** and re-cut on every run. The population moved, so customers changed tier without changing their own behaviour. The automation sits on a moving boundary. Trigger on absolute behaviour instead, such as days since last purchase.
Hint: what are quintiles relative to?
Trap: debugging the insight's SQL or schedule. Nothing is broken.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md) · [Interview set](../Interview/02-data-360/02-identity-and-segmentation.md)

An exec asks the agent for last quarter's churn and gets 11.2%. The finance board pack says 7.8%. Finance excludes downgrades and counts on contract end date; the Data 360 insight counts any lapse on the lapse date. "Why is the agent making up numbers?" <!--id:d360-014-->
?
It isn't. It computed one definition correctly. Two definitions of one metric is a **governance** problem: get finance and the data owners to agree one definition, put it in the semantic layer, and name the other metric differently.
Hint: is either number wrong?
Trap: picking a number in the room, or telling the agent to hedge. Hedged wrong numbers are still wrong.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md) · [Interview set](../Interview/02-data-360/02-identity-and-segmentation.md)

## Zero Copy

### Foundations

#flashcards/data-360/zero-copy/foundations

Live Query vs Accelerated Query vs File Federation: what does each do? <!--id:d360-015-->
?
**Live Query** pushes the query to the source's engine and returns only the result: always fresh, and it spends source compute. **Accelerated Query** keeps a cached local copy refreshed every 15 minutes to 7 days. **File Federation** reads the source's storage layer with Data 360's own compute. It suits large historical data and generally costs less.
Source: [Zero Copy & BYOL](../SF_Data_360/zero-copy-and-byol.md)

At Summer '26, which federation connector is GA and which is Beta, and what does that mean in a proposal? <!--id:d360-016-->
?
**AWS Glue Data Catalog** federation is **GA**: safe to commit to. **Microsoft Fabric OneLake** federation is **Beta**: prototype and demo only, never load-bearing for a dated go-live. Beta is a support and stability label, not a statement about whether the demo works.
Source: [Zero Copy & BYOL](../SF_Data_360/zero-copy-and-byol.md)

### Hard

#flashcards/data-360/zero-copy/hard

A service agent grounds partly on order history federated from BigQuery. It is fast all week, but takes 8–12 seconds between 8 and 10 a.m. on Mondays, sometimes timing out. Agentforce shows nothing unusual. The client wants you to escalate to Salesforce. What do you say? <!--id:d360-017-->
?
Not a Salesforce escalation. Under zero copy, **query performance is inherited from the source**, and a weekly time-of-day pattern is warehouse contention. Take it to the BigQuery owner. Consider Accelerated Query for that data if minutes-old order history is acceptable.
Hint: where does a Live Query actually run?
Trap: escalating, or raising the timeout. A 12-second wait is not a fix.
Source: [Zero Copy & BYOL](../SF_Data_360/zero-copy-and-byol.md) · [Interview set](../Interview/02-data-360/03-zero-copy-and-activation.md)

A retailer federated 40 TB of Snowflake data rather than copying any of it. Phase two (identity resolution across Snowflake, CRM and loyalty data, plus segments and an agent) isn't working, and they say Data 360 was mis-sold. Your answer? <!--id:d360-018-->
?
Not mis-sold. Zero copy gives reach, not every feature on federated data. Decide **per dataset**: ingest the identity-bearing, segment-filtered and grounding slice, and leave the bulk of the 40 TB federated. A small, governed, named subset is something the governance board can approve.
Hint: is "federation doesn't support phase two" a global fact or a per-feature one?
Trap: proposing to ingest all 40 TB, the very migration they avoided.
Source: [Zero Copy & BYOL](../SF_Data_360/zero-copy-and-byol.md) · [Interview set](../Interview/02-data-360/03-zero-copy-and-activation.md)

## RAG & Vector Search

### Foundations

#flashcards/data-360/rag/foundations

Search index vs retriever: what is the difference? <!--id:d360-019-->
?
A **search index** is the chunked, embedded corpus: keyword, vector or hybrid. A **retriever** is the configured query against that index, which supplies grounding to a prompt template or agent. They are not interchangeable.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md)

What does a hybrid search index do that a vector index doesn't? <!--id:d360-020-->
?
It builds both a vector index and a keyword index, queries both (semantic and lexical), then merges and ranks the results. It catches exact terms such as product codes that similarity search misses.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md)

### Hard

#flashcards/data-360/rag/hard

An agent answers "what do we know about this customer?" with vector search over ingested profile data. It takes 3–5 seconds and misses recent orders. The client's fix is a higher Top-N plus re-ranking. Your view? <!--id:d360-021-->
?
Two separate problems. A known-key lookup over structured data is the wrong primitive for vector search: use a **data graph**, which is precomputed and answers in milliseconds, exactly. The missing orders are a freshness or completeness problem upstream; Top-N can't retrieve what isn't indexed.
Hint: is this unstructured content?
Trap: tuning the retriever: Top-N, re-ranking, a better embedding model.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md) · [Interview set](../Interview/01-agentforce/01-grounding-and-retrieval.md)

RAG answers about a procedure are fluent but only half right. The procedure's key steps sit in a long table inside the article. What do you change first, and what does it cost? <!--id:d360-022-->
?
**Chunking.** Retrieval returns chunks, and these chunks split the table from its context. Use structure-aware chunking: a Code Extension Python function set as the chunking strategy in the index's Advanced Setup. The cost is a full re-index of the corpus.
Hint: what does retrieval actually return?
Trap: switching the model or raising Top-N.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md)

## DevOps & Environments

### Foundations

#flashcards/data-360/devops/foundations

DevOps data kit vs standard data kit: which data space can each be created from and deployed to? <!--id:d360-023-->
?
A **DevOps** data kit migrates metadata from sandbox to production. It is created from **any** data space and deploys to the **same** data space in the target. A **standard** data kit packages a solution to share. It is created from the **default** data space and deploys to **any** data space.
Source: [Data 360 DevOps](../SF_Data_360/data-360-devops.md)

### Hard

#flashcards/data-360/devops/hard

In a new Data 360 sandbox, the data streams show production row counts, but agents ground on nothing and every connection is Inactive. The team calls it a bug. Is it? <!--id:d360-024-->
?
No. A Data 360 sandbox holds **metadata only**; no data is copied, even in a Full Copy sandbox. Counts and dates show production values until data is ingested there. Connections are replicated without their authorization, so they arrive Inactive. Re-authorize each one, then ingest test data.
Hint: what does a Data 360 sandbox copy?
Trap: asking for a Full Copy sandbox to "get the data".
Source: [Data 360 DevOps](../SF_Data_360/data-360-devops.md)
