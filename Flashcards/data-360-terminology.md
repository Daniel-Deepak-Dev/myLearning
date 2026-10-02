---
area: Data 360
topic: Terminology
id_prefix: d360-term
---
# Data 360 › Terminology

The Data 360 (formerly Data Cloud) vocabulary, one term per card. Each answer gives two things: what the term **means**, and what the feature is **used for**. Read it out loud as one sentence each.

Foundations is the glossary. Hard is the terms people mix up in a design review, each with the trap. The topic decks in [data-360.md](data-360.md) hold the scenarios. Format and rules are in the README in this folder.

## Foundations

#flashcards/data-360/terminology/foundations

### Platform & licensing

**Data 360** — what is it, and what is it for? <!--id:d360-term-001-->
?
**Means:** Salesforce's lakehouse-based platform that ingests, harmonizes, unifies and activates data from any source. Renamed from Data Cloud at Dreamforce 2025; the product, licence and data model did not change.
**Used for:** one governed data layer that segments, insights and agents all read. The 2026 framing is a context engine that grounds agents.
Source: [Glossary](../GLOSSARY.md) · [Release radar](../RELEASE-RADAR/data-360.md)

**Lakehouse** — what is it, and why does it matter in Data 360? <!--id:d360-term-002-->
?
**Means:** an architecture that combines a data lake's cheap, open storage with a warehouse's query performance and governance.
**Used for:** it is the design under Data 360. DLOs are tables in the lake, and Query Editor reads them with SQL.
Source: [Glossary](../GLOSSARY.md) · [Lab Environment](../SF_Data_360/lab-environment.md)

**CDP** (customer data platform) — what is it, and how does it relate to Data 360? <!--id:d360-term-003-->
?
**Means:** the system category that unifies customer data into persistent profiles.
**Used for:** describing where Data 360 started. Salesforce now frames it as a context engine that grounds agents, a bigger job than a CDP.
Source: [Glossary](../GLOSSARY.md)

**Home org** — what is it, and what is it for? <!--id:d360-term-004-->
?
**Means:** the Salesforce org a Data 360 tenant is provisioned in. Its own CRM data is connected by default, with no connection to set up.
**Used for:** in Data Cloud One, the one place where all ingestion, identity resolution and governance are configured.
Source: [Glossary](../GLOSSARY.md) · [Lab Environment](../SF_Data_360/lab-environment.md)

**Data Cloud One** — what is it, and what is it for? <!--id:d360-term-005-->
?
**Means:** the multi-org pattern: one Data 360 instance in a home org, plus up to **three** included companion orgs that consume selected data spaces.
**Used for:** serving several Salesforce orgs from one tenant. It forces a partition decision (brand, region or legal entity), and data residency follows the home org's region.
Source: [Glossary](../GLOSSARY.md) · [Release radar](../RELEASE-RADAR/data-360.md)

**Companion org** — what is it, and what does it receive? <!--id:d360-term-006-->
?
**Means:** in Data Cloud One, an org attached to the home org's tenant that consumes shared data spaces. It receives **metadata, not data**; the records stay in the home tenant.
**Used for:** giving another org's users the unified profile, through a subset of Data 360 in the Data Cloud One app. Sandbox pairs only with sandbox, production only with production.
Source: [Glossary](../GLOSSARY.md)

**Standard CRM connection** — what is it, and what does the source org need? <!--id:d360-term-007-->
?
**Means:** a connection that ingests data from a Salesforce org other than the home org, and sends data actions back.
**Used for:** bringing another org's CRM data in. The source org needs **no Data 360 licence**, only a permission set on the user who authorizes the connection.
Trap: mixing it up with a companion connection, which points the other way and does need licences.
Source: [Glossary](../GLOSSARY.md) · [Lab Environment](../SF_Data_360/lab-environment.md)

**Data 360 Provisioning** ("Data Cloud Everywhere") — what is it, and when do you use it? <!--id:d360-term-008-->
?
**Means:** the $0 SKU that switches Data 360 on in an Enterprise Edition or higher org, with a starter allowance: about 250,000 Data Services credits and 1 TB of storage.
**Used for:** trying Data 360 inside the client's own org, rather than exporting their data to a tenant you control.
Source: [Glossary](../GLOSSARY.md) · [Lab Environment](../SF_Data_360/lab-environment.md)

**Profile**, in the billing sense — what is it, and why does it matter? <!--id:d360-term-009-->
?
**Means:** a unified individual after identity resolution, not a raw source row.
**Used for:** it is reported to be the unit Data 360 is priced on, so duplicate or fragmented profiles would inflate a recurring bill. 🚩 That figure comes from non-Salesforce sources; check the contract.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md) · [Glossary](../GLOSSARY.md)

**Data Services credits** — what are they, and what spends them? <!--id:d360-term-010-->
?
**Means:** Data 360's own consumption currency, split into **21 usage types**. Credits used = units × the rate-card multiplier. **Flex Credits** are the alternative that also covers generative AI.
**Used for:** paying for what Data 360 runs. A streaming transform costs more than a batch one, and a chatty data action on a busy DMO is a billing decision.
Source: [Lab Environment](../SF_Data_360/lab-environment.md) · [Data 360-triggered flows](../SF_core/04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md)

**Digital Wallet** — what is it, and what is it for? <!--id:d360-term-011-->
?
**Means:** where Data 360 credit consumption is tracked, on consumption cards that show what was purchased, consumed and what remains.
**Used for:** watching spend against the allowance before it runs out.
Source: [Lab Environment](../SF_Data_360/lab-environment.md)

**Platform Integration User** — what is it, and why does it matter? <!--id:d360-term-012-->
?
**Means:** the system user Data 360 acts as when it reads back into a connected org.
**Used for:** its permission sets bound what any connected org can retrieve. "The integration can't see it" is a permission-set question, not a connector bug.
Source: [Glossary](../GLOSSARY.md)

Data 360 standard permission sets: ==Data Cloud Architect== (formerly Data Cloud Admin) can do everything; ==Data Cloud Activation Manager== manages activation targets and activations; ==Data Cloud Activation Specialist== creates segments; ==Data Cloud User== can only view. <!--id:d360-term-013-->
Source: [Lab Environment](../SF_Data_360/lab-environment.md)

**Data Cloud Salesforce Connector permission set** — what does it control? <!--id:d360-term-014-->
?
**Means:** the permission set that decides which objects the CRM connector reads. Since Winter '25 it has **View All Data** on by default in new orgs.
**Used for:** debugging "the field is empty in Data 360". A missing read permission shows up as missing data, not as an error.
Source: [Lab Environment](../SF_Data_360/lab-environment.md)

**STDM** (Standard Data Model) — what is it, and why does an agent team care? <!--id:d360-term-015-->
?
**Means:** Salesforce's prebuilt Data 360 schema, so data from different sources lands in a shape the platform already understands.
**Used for:** Agentforce writes production session traces as STDM records, so debugging a live agent is a Data 360 query.
Source: [Glossary](../GLOSSARY.md) · [Release radar](../RELEASE-RADAR/data-360.md)

### Ingestion

**Data stream** — what is it, and what is it for? <!--id:d360-term-016-->
?
**Means:** a configured ingestion feed from a connector, one per object per connection. It lands rows in a DLO, still in the source's shape.
**Used for:** the unit you schedule, refresh and monitor. Freshness is decided per stream. Read the row count in the refresh history, not the green status.
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md)

**Data stream category** — what are the three, and what does the choice decide? <!--id:d360-term-017-->
?
**Means:** **Profile** (people or accounts with identifiers), **Engagement** (time-series events) or **Other** (reference data that describes those records). Fixed once the stream is saved.
**Used for:** deciding what the data can do downstream. Only Profile and Engagement objects can be a segment's Segment On.
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md) · [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Event Time Field** — what is it, and how do you pick one? <!--id:d360-term-018-->
?
**Means:** the Date or DateTime field an Engagement stream uses to say when each event happened. It can't be edited after setup.
**Used for:** ordering engagement in time. Pick a value that never changes for a record: a mutable date adds duplicate rows with the same primary key.
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md)

**Primary key** (data stream) — what is it, and what if the source has none? <!--id:d360-term-019-->
?
**Means:** the unique field that identifies a source record in a stream. Ingestion API writes upsert on it, which makes retries safe.
**Used for:** telling a changed record from a new one. If the key is composite or missing, build it with a formula field.
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md) · [Glossary](../GLOSSARY.md)

**Starter data bundle** — what is it, and what is it for? <!--id:d360-term-020-->
?
**Means:** a Salesforce-defined data stream definition, already mapped to DMOs, for Salesforce sources such as the CRM connector.
**Used for:** standing up Salesforce-sourced streams without mapping each field by hand.
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md)

**Ingestion API** — what is it, and when do you use it? <!--id:d360-term-021-->
?
**Means:** REST push into Data 360, with an OpenAPI 3.0.x YAML schema that defines its objects. **Streaming**: JSON, up to 200 KB per request, processed about every 3 minutes. **Bulk**: CSV files up to 150 MB.
**Used for:** the universal fallback when no connector fits: a script, another org, a serverless function.
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md)

**Accelerated Data Ingest** — what is it, and what problem does it solve? <!--id:d360-term-022-->
?
**Means:** real-time CRM data into Data 360 with no pipeline delay. **GA in Summer '26**.
**Used for:** keeping what an agent grounds on as fresh as CRM, so actions don't bypass Data 360 to call CRM and lose the unified profile.
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md) · [Release radar](../RELEASE-RADAR/data-360.md)

**Batch mode vs streaming mode** (CRM connector) — what is the difference? <!--id:d360-term-023-->
?
**Means:** batch mode checks the source every **10–15 minutes**; streaming mode reflects changes as soon as they are made. After a full refresh, the CRM connector also runs an incremental refresh about every **10 minutes**.
**Used for:** matching freshness to the reader. Periodic full refresh is off by default in new streams.
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md)

**Salesforce Interactions SDK** and the **Engagement Mobile SDK** — what are they for? <!--id:d360-term-024-->
?
**Means:** the SDKs that send behaviour to Data 360: the Interactions SDK from a website, and the Data 360 module of the Engagement Mobile SDK from an app.
**Used for:** capturing engagement events, the real-time data a streaming insight is built on.
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md) · [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

### Data model

**DSO** (data source object) — what is it? <!--id:d360-term-025-->
?
**Means:** the data exactly as it arrives from the source, before any mapping.
**Used for:** naming the first stage of DSO → DLO → DMO, so you can say where a problem starts. Nothing downstream reads it; everything reads DMOs.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

**DLO** (data lake object) — what is it, and what is it for? <!--id:d360-term-026-->
?
**Means:** the stored container a data stream creates in the lake, still in the source's shape. Its API name ends `__dll`.
**Used for:** holding data until it is mapped. A DLO does nothing for segments or agents until it is mapped to a DMO, and a SOQL query on it needs the dataspace.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

**DMO** (data model object) — what is it, and what reads it? <!--id:d360-term-027-->
?
**Means:** a harmonized object in Salesforce's canonical model, standard or custom, that DLOs are mapped into. Standard DMOs use the `ssot__` prefix.
**Used for:** everything downstream. Identity resolution matches on DMO fields; insights, segments and agents read DMOs.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

**Harmonization** (data mapping) — what is it, and why is it high stakes? <!--id:d360-term-028-->
?
**Means:** mapping DLO fields to DMO fields, so "email" from five systems becomes one attribute on one DMO.
**Used for:** cross-source consistency. A mapping mistake spreads into every feature that reads the DMO, and field data types can't be changed afterwards.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

**Standard DMO vs custom DMO** — which do you prefer, and why? <!--id:d360-term-029-->
?
**Means:** a standard DMO is Salesforce's canonical object; a custom DMO is one you define.
**Used for:** prefer standard. Standard DMOs carry downstream behaviour, and a custom DMO per source rebuilds the silos. Match tuning on unaligned DMOs is thrown away.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md) · [Identity Resolution](../SF_Data_360/identity-resolution.md)

**Individual DMO** — what is it, and what must be mapped with it? <!--id:d360-term-030-->
?
**Means:** the standard DMO for a person, and the usual target of an identity resolution ruleset.
**Used for:** unification. It needs Individual mapped, plus at least one Contact Point DMO or Party Identification.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md) · [Identity Resolution](../SF_Data_360/identity-resolution.md)

**Contact Point DMOs** — what are they, and what are they for? <!--id:d360-term-031-->
?
**Means:** DMOs that hold one way to reach a person: **Contact Point Email**, **Phone** or **Address**.
**Used for:** matching (normalized email, phone and address) and activation. Without a contact point there is nothing to activate to.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md) · [Identity Resolution](../SF_Data_360/identity-resolution.md)

**Party Identification DMO** — what is it, and how does it match? <!--id:d360-term-032-->
?
**Means:** holds third-party identifiers, such as a loyalty card or driver's licence number.
**Used for:** matching on IDs rather than names. Records with the same identification type, name and number can match.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

**Fully qualified key** (FQK) — what is it, and what does it prevent? <!--id:d360-term-033-->
?
**Means:** a source key plus a **key qualifier** that names its source. Data 360 adds key qualifier fields to DLOs and DMOs.
**Used for:** stopping keys from different streams colliding when they map into one DMO. Salesforce advises one on every primary and foreign key; up to **20** can be active.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

**Data space** — what is it, and what is it for? <!--id:d360-term-034-->
?
**Means:** a logical partition of Data 360 data for profile unification, insights and marketing. Every org has a **default data space** that can't be deleted, and one DLO can sit in more than one data space.
**Used for:** boundaries that must never be crossed, such as legal entities or residency. Not for "team A sees less": that is permission sets.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

Data 360 API names: a DLO is queried as ==`Name__dll`==, standard DMOs carry the ==`ssot__`== prefix, standard DMOs added after January 2026 end in ==`_std__dlm`==, and a calculated insight object ends in ==`__cio`==. <!--id:d360-term-035-->
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md) · [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**`SET OPTIONS`** — what is it, and when is it required? <!--id:d360-term-036-->
?
**Means:** a SOQL clause, at the very end of the query, that names the Data 360 dataspace and controls `NULL` vs empty-string handling.
**Used for:** querying DLOs. Leave out the dataspace on a DLO query and you get zero rows, with no error. The dataspace option is valid for DLO queries only.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

**`honorEmptyStrings`** — what does it control? <!--id:d360-term-037-->
?
**Means:** the `SET OPTIONS` setting for `NULL` vs `''`. DLOs store them as different values; the default (`false`) treats them as the same, like Platform objects.
**Used for:** getting filters and counts right when a source sends empty strings instead of nulls.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

**Data transform** — what is it, and batch or streaming? <!--id:d360-term-038-->
?
**Means:** a job that reshapes DLOs into new DLOs. **Batch**: scheduled, with a visual editor that joins, aggregates and appends. **Streaming**: one SQL statement run continuously, near real time.
**Used for:** cleaning and combining data before it is mapped. Choose streaming only when the use is time-sensitive: it uses more credits.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

### Identity resolution

**Identity resolution** — what is it, and what does it change in the source data? <!--id:d360-term-039-->
?
**Means:** matching records across sources and reconciling their values into unified profiles, driven by a ruleset. Source records are **linked, not merged or deleted**.
**Used for:** one profile per person for segments, insights and agents to read. Its quality decides every number computed downstream.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md)

**Ruleset** — what is it, and when does it apply? <!--id:d360-term-040-->
?
**Means:** the match rules and reconciliation rules for one object, such as Individual. It runs as a job.
**Used for:** defining how one object unifies. Because it runs as a job, a new record can sit unresolved for a while, and an agent may briefly see a fragment.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md)

Identity resolution match methods: ==exact== (no typos or format differences), ==fuzzy== (tolerates spelling differences, first name only) and ==normalized== (same value whatever the format, for email, phone and address). <!--id:d360-term-041-->
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md)

**Reconciliation rule** — what is it, and what are the options? <!--id:d360-term-042-->
?
**Means:** the rule that picks which value wins when matched records disagree: **Last Updated**, **Most Frequent** or **Source Priority**.
**Used for:** deciding what the unified profile shows, per object and per field. `Email` can follow Source Priority while `Phone` follows Last Updated.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md)

**Unified profile** (Unified Individual) — what is it? <!--id:d360-term-043-->
?
**Means:** the single record identity resolution produces for a person, linked to all their source records and behaviour.
**Used for:** what segments, insights and agents treat as "the customer". Fragmented or merged profiles give wrong metrics.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md) · [Glossary](../GLOSSARY.md)

**Unified Link Individual** — what is it, and what is it for? <!--id:d360-term-044-->
?
**Means:** the identity resolution output object that joins each source record to its Unified Individual. The run also creates unified contact point objects.
**Used for:** tracing a profile value back to its source, for example by joining Individual, Unified Link Individual and Unified Individual in SQL.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md)

**Real-time identity resolution** — what is it, and what does it feed? <!--id:d360-term-045-->
?
**Means:** compares an active visitor with existing profiles in milliseconds, using an existing ruleset.
**Used for:** in-session decisions. Its output feeds a real-time data graph.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md)

**Profile Explorer** — what is it, and when do you open it? <!--id:d360-term-046-->
?
**Means:** a dashboard view of one unified profile.
**Used for:** checking a resolved profile against its sources, for example to spot two people merged at one address.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md)

### Insights, segments & activation

**Calculated insight** — what is it, and what is it for? <!--id:d360-term-047-->
?
**Means:** a metric computed over stored data in high-volume batches, defined in SQL, such as lifetime value or engagement score.
**Used for:** segment criteria, personalization, and governed numbers for agents. Cheaper and safer than letting a model aggregate raw rows.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md) · [Glossary](../GLOSSARY.md)

**Calculated insight object** (CIO) — what is it, and what can use it? <!--id:d360-term-048-->
?
**Means:** the output object of a calculated insight, with the `__cio` suffix, such as `Avg_Spends__cio`.
**Used for:** querying insight results like a DMO, and starting a Data Cloud-triggered flow, which fires on a DMO or CIO change.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md) · [Data 360-triggered flows](../SF_core/04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md)

**Streaming insight** — what is it, and what data can it use? <!--id:d360-term-049-->
?
**Means:** a near-real-time time-series aggregate over **engagement** data, such as Web or Mobile SDK events. It can't be built on streaming profile data.
**Used for:** driving data actions and orchestration as events happen.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**RFM** — what is it, and what is the catch? <!--id:d360-term-050-->
?
**Means:** recency, frequency, monetary. An insight that emits a tier label from quintile ranks, which are **relative** and re-cut on every run.
**Used for:** customer value tiers. Don't trigger automation on a tier change: a customer can move tier because others moved.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Segment** — what is it, and what is it for? <!--id:d360-term-051-->
?
**Means:** an audience definition built from profiles, attributes and insights.
**Used for:** the unit you publish to an activation. Match its refresh to how often the target actually uses it.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Segment On** — what is it, and what does it decide? <!--id:d360-term-052-->
?
**Means:** the DMO a segment is built on, such as Unified Individual or Account. It must be a Profile or Engagement object.
**Used for:** setting the level the segment works at and which attributes you can filter on.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Nested segment** — what is it, and what is it for? <!--id:d360-term-053-->
?
**Means:** a segment that reuses an existing segment (the inner one) inside a new one (the outer one).
**Used for:** defining shared filters once and keeping related audiences consistent.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Waterfall segment** — what is it, and what is it for? <!--id:d360-term-054-->
?
**Means:** up to **20** existing segments in priority order. Each profile lands only in the first segment it matches, so the audiences are mutually exclusive.
**Used for:** campaigns with several offers where each customer gets one. Rapid Publish isn't available for it.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Real-time segment** — what is it, and what can't it do? <!--id:d360-term-055-->
?
**Means:** a segment that completes on demand in milliseconds.
**Used for:** in-the-moment audiences. It can't use exclusion criteria, segment counts or manual publish.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Rapid Publish** — what is it, and what is the standard alternative? <!--id:d360-term-056-->
?
**Means:** a segment publish schedule of every **1 or 4 hours**. The standard schedule is every **12 or 24 hours**.
**Used for:** fresher audiences when the target uses them that often. Publishing more often than the target reads costs money and changes nothing.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Activation** — what is it, and what is it for? <!--id:d360-term-057-->
?
**Means:** publishing a segment to an activation target, where something happens.
**Used for:** getting an audience to Marketing Cloud, ad platforms or other systems. Since January 2026 an activation can also start a flow.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md) · [Data 360-triggered flows](../SF_core/04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md)

**Activation target** — what is it, and what does it hold? <!--id:d360-term-058-->
?
**Means:** the destination platform for activations, and its authentication: Marketing Cloud, Data 360 itself, B2C Commerce, Amazon Ads, Google.
**Used for:** setting up a destination once. Each activation points at one target.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Data action** — what is it, and what is it for? <!--id:d360-term-059-->
?
**Means:** forwards a change event on a DMO or CIO from Data 360 to a data action target. Flow is not involved.
**Used for:** telling another system that something changed. At volume it costs Data Services credits.
Source: [Data 360-triggered flows](../SF_core/04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md)

**Data action target** — what are the three types, and which is the useful bridge? <!--id:d360-term-060-->
?
**Means:** where a data action sends its event: a **Salesforce platform event**, a **webhook** or **Marketing Cloud Engagement**.
**Used for:** the platform event target is the bridge: a platform event-triggered flow can then handle the change with nothing new to learn.
Source: [Data 360-triggered flows](../SF_core/04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md) · [Glossary](../GLOSSARY.md)

**Data Cloud-triggered flow** — what is it, and what can't it do? <!--id:d360-term-061-->
?
**Means:** a flow in core Salesforce that starts when a DMO or CIO record meets criteria, within a data space.
**Used for:** doing CRM work from a Data 360 change. It runs after the change commits: no before-save, and prior values are unreliable.
Source: [Data 360-triggered flows](../SF_core/04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md)

**Activation-triggered flow** — what is it, and what gap did it close? <!--id:d360-term-062-->
?
**Means:** a flow whose start node is a Data 360 activation. Added in January 2026.
**Used for:** orchestrating what happens after an activation (CRM writes, API calls, MuleSoft connectors) in Flow Builder, instead of per activation target.
Source: [Data 360-triggered flows](../SF_core/04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md)

**Copy field enrichment** — what is it, and what is it for? <!--id:d360-term-063-->
?
**Means:** copies a Data 360 value, such as lifetime value from an insight, into a CRM field on a record.
**Used for:** putting a Data 360 number where CRM users already work, such as a Total Lifetime Value field on Account.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Related list enrichment** — what is it, and how does it differ from copy field? <!--id:d360-term-064-->
?
**Means:** shows Data 360 records as a related list on a CRM record page, **without storing them in CRM**.
**Used for:** a customer 360 view on a record page with nothing copied. Copy field stores the value; related list only displays it.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Semantic layer** (Tableau Semantics) — what is it, and what is it for? <!--id:d360-term-065-->
?
**Means:** a governed layer of business definitions, such as what counts as "revenue", between raw data and its consumers. Tableau Semantics is Salesforce's implementation.
**Used for:** an agent asked "what was churn last quarter" gets the company's definition. It makes a disagreement visible; it doesn't choose the winner.
Source: [Glossary](../GLOSSARY.md) · [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

### Zero copy & sharing

**Zero copy** (BYOL) — what is it, and what doesn't it remove? <!--id:d360-term-066-->
?
**Means:** Data 360 reads data where it already lives (Snowflake, BigQuery, Redshift, Databricks, an Iceberg lake) instead of copying it in. "Bring your own lake."
**Used for:** large or externally governed data, with no ETL pipeline. It removes Data 360 storage and pipeline lag, not cost or source staleness.
Source: [Zero Copy & BYOL](../SF_Data_360/zero-copy-and-byol.md)

**Live Query** — what is it, and what does it cost? <!--id:d360-term-067-->
?
**Means:** pushes the query to the source's engine and returns only the result.
**Used for:** always-fresh interactive analysis and live dashboards. It spends source compute, and its speed is the source's speed.
Source: [Zero Copy & BYOL](../SF_Data_360/zero-copy-and-byol.md)

**Accelerated Query** — what is it, and what does it trade? <!--id:d360-term-068-->
?
**Means:** a cached local copy of a federated query, refreshed every **15 minutes to 7 days**.
**Used for:** speed when slightly old data is acceptable. You trade freshness for speed.
Source: [Zero Copy & BYOL](../SF_Data_360/zero-copy-and-byol.md)

**File Federation** — what is it, and why is it cheaper? <!--id:d360-term-069-->
?
**Means:** reads the source's storage layer directly, such as Iceberg tables through an Iceberg REST catalog, with Data 360's own compute.
**Used for:** large historical data. There is no warehouse cluster to run and no external compute bill. AWS Glue Data Catalog is GA; Microsoft Fabric OneLake is Beta.
Source: [Zero Copy & BYOL](../SF_Data_360/zero-copy-and-byol.md) · [Zero-copy as a data tier](../SF_core/08-data-modeling-and-large-data-volumes/18-zero-copy-and-data-360-as-data-tier.md)

**Data share** and **data share target** — what are they, and which way does data go? <!--id:d360-term-070-->
?
**Means:** the share-out half of zero copy. The **data share target** is the connection to an external platform such as Snowflake. The **data share** is the set of Data 360 objects linked to it.
**Used for:** letting that platform read Data 360 objects natively, with nothing copied.
Source: [Zero Copy & BYOL](../SF_Data_360/zero-copy-and-byol.md)

**Unity Catalog file sharing** — what is it, and who reads whose data? <!--id:d360-term-071-->
?
**Means:** Salesforce Data 360 File Sharing into Databricks Unity Catalog (GA October 2025). Databricks reads Data 360 objects in place, on Databricks compute, authenticated by secretless IAM Workload Identity Federation.
**Used for:** a data scientist's notebook reading Salesforce data without an export. It is the opposite direction to Data 360's own federation.
Source: [Release radar](../RELEASE-RADAR/data-360.md) · [Glossary](../GLOSSARY.md)

### Search, RAG & data graphs

**Search index** — what is it, and what types are there? <!--id:d360-term-072-->
?
**Means:** unstructured content (PDFs, transcripts, Knowledge) that Data 360 has chunked and embedded so it can be searched. Types: keyword, vector and hybrid.
**Used for:** the corpus a retriever queries to ground a prompt or agent.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md)

**Chunking** — what is it, and why does it matter most? <!--id:d360-term-073-->
?
**Means:** splitting documents into the pieces that get embedded and retrieved.
**Used for:** it is usually the biggest RAG quality lever: retrieval returns chunks, and a chunk split mid-procedure gives half a procedure. Changing it means re-indexing.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md)

**Vector database** (Data 360) — what is it, and what is its limit? <!--id:d360-term-074-->
?
**Means:** Data 360's built-in store of embeddings for unstructured content.
**Used for:** semantic search and grounded answers. It finds similar, not correct: a confidently retrieved wrong chunk still gives a wrong answer.
Source: [Glossary](../GLOSSARY.md) · [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md)

**Retriever** — what is it, and what is it for? <!--id:d360-term-075-->
?
**Means:** the configured query against a search index that fetches the most relevant content. It is not the index itself.
**Used for:** grounding a prompt template or agent with relevant content at run time.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md)

**Top-N** — what is it, and why is it a cost lever? <!--id:d360-term-076-->
?
**Means:** how many chunks a retriever returns.
**Used for:** every retrieved chunk is tokens in every call. Raising it can't fetch what was never indexed.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md)

**UDLO** and **UDMO** — what are they, and is the content imported? <!--id:d360-term-077-->
?
**Means:** unstructured data lake object and unstructured data model object. Files are referenced through a UDLO mapped to a UDMO.
**Used for:** building a search index over files. From a blob store, Data 360 doesn't import the files; the UDMO references them.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md)

**Data graph** — what is it, and when does it beat vector search? <!--id:d360-term-078-->
?
**Means:** a precomputed, denormalized view of related DMO data around a profile, combined into one JSON blob.
**Used for:** exact, millisecond reads by agents and personalization, such as "what do we know about this customer". Structured lookups want a data graph, not semantic search.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md) · [Glossary](../GLOSSARY.md)

**Standard data graph vs real-time data graph** — what is the difference? <!--id:d360-term-079-->
?
**Means:** a standard data graph refreshes with a delay of minutes to hours. A real-time data graph refreshes continuously and is read in milliseconds.
**Used for:** real-time when an in-session decision needs current data. Real-time identity resolution feeds it.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md) · [Identity Resolution](../SF_Data_360/identity-resolution.md)

**Intelligent Context** — what is it, and what is it for? <!--id:d360-term-080-->
?
**Means:** automatic extraction of unstructured content (PDFs, tables, images, flowcharts) into grounding data, through a low-code pipeline.
**Used for:** grounding agents on complex documents. The same content can be interpreted from several business perspectives.
Source: [Glossary](../GLOSSARY.md) · [Release radar](../RELEASE-RADAR/data-360.md)

**Code Extension** — what is it, and what can it do today? <!--id:d360-term-081-->
?
**Means:** custom **Python** scripts and functions deployed into isolated containers inside Data 360.
**Used for:** batch data transforms and custom chunking for search indexes. Developers author it; users with the Data Cloud Architect permission set run and monitor it.
Source: [Data 360 DevOps](../SF_Data_360/data-360-devops.md) · [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md)

### DevOps & developer tools

**Data kit** — what is it, and what are the two kinds? <!--id:d360-term-082-->
?
**Means:** a package of Data 360 configuration, such as data streams, DLOs, calculated insights, data graphs and code extensions. A **DevOps** kit migrates sandbox to production; a **standard** kit packages a solution to share.
**Used for:** promoting Data 360 config with `sf project retrieve start --manifest` and `sf project deploy start`, like other metadata.
Source: [Data 360 DevOps](../SF_Data_360/data-360-devops.md)

**Data 360 sandbox** — what does it hold? <!--id:d360-term-083-->
?
**Means:** a sandbox with Data 360 provisioned. It holds **metadata only**: no data is copied, even in a Full Copy sandbox, and connections arrive Inactive.
**Used for:** building and testing configuration before promoting it with a DevOps data kit. Its components show production counts until you ingest data there.
Source: [Data 360 DevOps](../SF_Data_360/data-360-devops.md)

**`sfsqlquery`** — what is it, and what does it replace? <!--id:d360-term-084-->
?
**Means:** the Apex namespace, from the Winter '27 release notes, for running Data 360 SQL from Apex: `SqlStatement`, `SqlRowIterator`, `Row`, `QueryHandle` and `SqlQueueable`.
**Used for:** an Apex-backed agent action computing a live aggregate, instead of HTTP callouts to the Direct API. The DLO dataspace trap still applies.
Source: [Release radar](../RELEASE-RADAR/data-360.md) · [Glossary](../GLOSSARY.md)

**Query Editor** — what is it, and what is it for? <!--id:d360-term-085-->
?
**Means:** runs Data 360 SQL over DLOs, DMOs, CIOs and data graphs.
**Used for:** ad-hoc analysis, and checking an insight or transform against SQL you wrote by hand rather than trusting the UI.
Source: [Lab Environment](../SF_Data_360/lab-environment.md) · [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

**Data Explorer** — what is it, and who has it? <!--id:d360-term-086-->
?
**Means:** the built-in tool for browsing Data 360 object data without writing SQL.
**Used for:** a quick look at what landed. It is on by default for Data 360 admins; other users need a permission set.
Source: [Lab Environment](../SF_Data_360/lab-environment.md)

**Code Extension CLI plugin** — what is the package called, and what does it need? <!--id:d360-term-087-->
?
**Means:** `@salesforce/plugin-data-code-extension`, installed explicitly (it isn't bundled in `sf`), alongside the Data Custom Code Python SDK. `run` needs Python 3.11 and takes `--target-org`.
**Used for:** scaffolding, running and deploying code extensions.
Trap: `@salesforce/plugin-data-codeextension`, without the hyphen, is printed in some skill docs and does not exist.
Source: [Release radar](../RELEASE-RADAR/data-360.md) · [Data 360 DevOps](../SF_Data_360/data-360-devops.md)

**`@IntegrationTest`** — what is it, and where can it run? <!--id:d360-term-088-->
?
**Means:** an Apex annotation (Developer Preview) that allows live callouts and mid-transaction commits via `IntegrationTest.commitTestOnly()`, cleaned up in a `@TearDown` method.
**Used for:** asserting on real Data 360 and Agentforce behaviour, which mocked unit tests can't. Scratch orgs only, with `ApexIntegrationTests` in the org definition's features.
Source: [Release radar](../RELEASE-RADAR/data-360.md)

**Python Data 360 connector** — which package do you use today? <!--id:d360-term-089-->
?
**Means:** `salesforce-cdp-connector` (v1) is deprecated. Its replacement, `salesforce-datacloud-connector` **2.0.0b1**, is a pre-release: `pip install --pre`, with no GA date.
**Used for:** querying Data 360 into pandas for notebooks and feature engineering. You can target a non-default dataspace at connection time.
Source: [Release radar](../RELEASE-RADAR/data-360.md)

## Hard

#flashcards/data-360/terminology/hard

### Commonly confused

In a design review: "We'll **activate** the high-value segment **to a platform event**, and a flow will create follow-up Tasks." Which term is wrong, and what do they actually need? <!--id:d360-term-090-->
?
An activation publishes a segment to an **activation target**; a platform event is a **data action target**. A data action forwards a DMO or CIO change. For "a segment lands, then do CRM work", use an **activation-triggered flow**. For "a record changed", use a data action or a Data Cloud-triggered flow.
Hint: which mechanism has a platform event as its target?
Trap: treating activation, data action and Data Cloud-triggered flow as three names for one thing.
Source: [Data 360-triggered flows](../SF_core/04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md)

The service team should see fewer customer attributes than marketing. An admin proposes a second **data space** for service. Do you agree? <!--id:d360-term-091-->
?
No. A data space is a hard partition: data spaces can't share a customer graph, so you would split unification. "Team A sees less" is a permission set and feature permission job. Keep data spaces for boundaries that must never be crossed: legal entity or residency.
Hint: what can't cross a data space boundary?
Trap: treating a data space as record-level security.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md) · [Release radar](../RELEASE-RADAR/data-360.md)

A data scientist wants to read unified profiles from a Databricks notebook without an export. A colleague proposes a Data 360 **zero-copy federation** connector to Databricks. Right tool? <!--id:d360-term-092-->
?
Wrong direction. Data 360's federation lets **Data 360 read the warehouse**. For **Databricks to read Data 360** in place, use Data 360 File Sharing into Unity Catalog, which Databricks' Lakehouse Federation queries, authenticated by IAM Workload Identity Federation.
Hint: who reads whose data?
Trap: one connector for both directions. Get it wrong and you design a pipeline neither side needed.
Source: [Release radar](../RELEASE-RADAR/data-360.md) · [Zero Copy & BYOL](../SF_Data_360/zero-copy-and-byol.md)

An Engagement stream of order events uses `LastModifiedDate` as its **Event Time Field**. The DLO now holds several rows per order ID. A developer proposes a transform to de-duplicate. What is the real fix? <!--id:d360-term-093-->
?
The event time must never change for a record. A mutable date adds a new row with the same primary key each time it moves. The Event Time Field can't be edited after setup, so rebuild the stream on an immutable date, such as the order date.
Hint: can the setting be changed on the existing stream?
Trap: de-duplicating downstream. The stream keeps producing duplicates.
Source: [Ingestion & Data Streams](../SF_Data_360/ingestion-and-data-streams.md)

CRM and an e-commerce platform both map customers into the Individual DMO. Both use numeric IDs, and customer `1001` in one system is a different person from `1001` in the other. Records are colliding. Which term solves it? <!--id:d360-term-094-->
?
**Fully qualified keys.** Configure key qualifiers so each key becomes source key + qualifier, and the two `1001`s stay distinct. Salesforce advises a key qualifier on every primary and foreign key field.
Hint: what does a key need besides its value?
Trap: a custom DMO per source to keep them apart. That rebuilds the silos.
Source: [Data Model: DSO, DLO & DMO](../SF_Data_360/data-model-dso-dlo-dmo.md)

Sales wants each Account's lifetime value, from a Data 360 insight, in list views and CRM reports. An admin builds a **related list enrichment**. Does it meet the need? <!--id:d360-term-095-->
?
No. A related list enrichment displays Data 360 records on the page without storing them in CRM, so list views and reports have no field to read. A **copy field enrichment** copies the value into a CRM field, which they can.
Hint: where does the value end up?
Trap: choosing the related list because it shows live data.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

A campaign has three offers: platinum, gold and standard. A customer who qualifies for several must get only the highest. The team builds three **nested segments** with hand-written exclusions. Which segment type fits? <!--id:d360-term-096-->
?
A **waterfall segment**: up to 20 existing segments in priority order, and each profile lands only in the first it matches. Exclusivity comes by design. Nested segments reuse filters; they don't make audiences exclusive.
Hint: which type makes audiences mutually exclusive?
Trap: maintaining exclusions by hand across segments.
Source: [Calculated Insights & Segmentation](../SF_Data_360/calculated-insights-and-segmentation.md)

An admin refuses to run **identity resolution** in production: "it will merge our duplicate Contacts, and we can't undo it." Correct them. <!--id:d360-term-097-->
?
Identity resolution **links** source records into a unified profile through Unified Link objects. It doesn't merge or delete source records, in Data 360 or in CRM. CRM duplicates are a job for CRM duplicate rules and merge. The real risk is over-matching inside the unified profile.
Hint: what does a ruleset actually write?
Trap: promising that it cleans up the CRM duplicates.
Source: [Identity Resolution](../SF_Data_360/identity-resolution.md) · [Data quality, dedup & MDM](../SF_core/08-data-modeling-and-large-data-volumes/19-data-quality-deduplication-and-mdm.md)

A colleague reads the Summer '26 notes as "Data 360 now has no-code **semi-joins and anti-joins**" and plans to use them in segmentation. Right? <!--id:d360-term-098-->
?
No. That item is a **CRM Analytics lens** feature (Beta), not Data 360. The tell is the help article ID: `analytics.` means CRM Analytics; Data 360 pages are `data.` or `release-notes.rn_c360_*`.
Hint: whose help article is it?
Trap: reading "filed near Data 360" as "part of Data 360".
Source: [Glossary](../GLOSSARY.md) · [Release radar](../RELEASE-RADAR/data-360.md)

A group's US production org holds Data 360. It wants to attach its EU subsidiary's org as a **companion org**, "so EU data stays in the EU org". What is wrong? <!--id:d360-term-099-->
?
A companion org gets metadata, not data. Ingestion and records live in the home org's tenant, and residency follows the **home org's** region. If EU residency is required, a separate Data 360 instance is the correct answer, not the lazy one.
Hint: where do a companion org's records actually live?
Trap: assuming the companion's own region governs its data.
Source: [Glossary](../GLOSSARY.md) · [Release radar](../RELEASE-RADAR/data-360.md)

"To ingest from our second org, we must buy Data 360 licences for it." True? <!--id:d360-term-100-->
?
No. A **standard CRM connection** ingests from another org with no Data 360 licence there, only a permission set on the user who authorizes it. A **companion connection** (Data Cloud One) points the other way, and that one does need licences.
Hint: which way does the data flow?
Trap: treating a standard CRM connection and a companion connection as the same thing.
Source: [Glossary](../GLOSSARY.md) · [Lab Environment](../SF_Data_360/lab-environment.md)

You tightened a DLO's **data space filter** to exclude a closed brand. A week later, the agent still retrieves that brand's articles. Why? <!--id:d360-term-101-->
?
Changing a data space filter doesn't update a search index already built on the DMO. The index keeps what it indexed under the old filter, even rows that no longer qualify. Rebuild the index after a filter change.
Hint: when did the index last read the filter?
Trap: debugging the retriever or the agent's instructions.
Source: [Vector Search & RAG](../SF_Data_360/vector-search-and-rag.md)
