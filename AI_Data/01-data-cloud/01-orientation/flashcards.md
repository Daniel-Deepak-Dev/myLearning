# Data 360 Orientation — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is Data 360 in one sentence?
A: Salesforce's lakehouse-based platform that ingests, harmonizes, unifies and activates customer data from any source — and grounds AI agents in it.

Q: What was Data 360 called before, and when did it change?
A: Data Cloud. Salesforce began calling it Data 360 at Dreamforce 2025 (October 14, 2025), positioning it inside the Agentforce 360 umbrella.

Q: Name the full Data 360 naming lineage.
A: Customer 360 Audiences → Salesforce CDP → Marketing Cloud CDP → Salesforce Genie → Salesforce Data Cloud → Data 360. Six names, all still in circulation.

Q: Is the Data 360 rename just marketing?
A: No. The pricing calculator, SKUs, the Summer '26 release-notes section and the certification all use it. The underlying product, licence, integrations and data model are unchanged.

Q: What is a CDP?
A: A system that unifies customer data from many sources into persistent profiles usable by other tools. Data 360 began as Salesforce's CDP; its 2026 framing is a context engine that grounds agents.

Q: What is a lakehouse?
A: Architecture combining a data lake's cheap open storage with a warehouse's query performance and governance.

Q: The Data 360 flow, in order?
A: Ingest → model → unify → insight → activate.

Q: What is the real shift behind the Data 360 rename?
A: The repositioning from a passive customer data store into an active context engine that grounds AI agents. Every 2026 feature follows from that.

Q: How does Data 360 relate to a core CRM org?
A: It sits alongside, not instead of. CRM remains the system of record for transactions; Data 360 is the system of context.

Q: How often does Data 360 ship?
A: Monthly, not on the three-times-a-year seasonal cadence. Checking only the seasonal release notes means missing most Data 360 changes.

Q: What is the certification called now?
A: Salesforce Certified Data 360 Consultant — renamed from Data Cloud Consultant on 2026-03-27. The exam code Data-Con-101 is unchanged.

Q: Which three data decisions cap agent quality?
A: Ingestion freshness (stale data → confident wrong answers), identity-resolution quality (duplicates → wrong profile), and chunking strategy (the biggest lever on retrieval quality).

Q: A client has five Salesforce orgs and wants one customer view. What is the recommended Data 360 pattern?
A: Data Cloud One — one Data 360 instance in a designated home org, with other orgs attached as companion orgs. Three companion connections are included; more need add-on licensing.

Q: In Data Cloud One, what actually reaches a companion org?
A: Metadata, not data. Records stay in the home org's tenant; the companion consumes the shared data spaces and the unified profile through it, with a subset of Data 360 functionality via the Data Cloud One app.

Q: Which Data Cloud One constraint most often disqualifies the pattern outright?
A: Data residency follows the home org's region, not the companion's. An EU subsidiary attached to a US home org inherits US residency — separate instances are then the correct answer.

Q: When should you create a second data space rather than use permission sets?
A: Only for boundaries that must never be crossed — distinct legal entities that cannot share a customer graph, or incompatible data-residency regimes. For "different teams see different data", use permission sets and keep the unified profile intact.

Q: Why does Data Cloud One make the SET OPTIONS dataspace clause more dangerous to forget?
A: A SOQL query against a DLO without its dataspace returns zero records silently, with no error. More data spaces means more ways to hit that failure without noticing.

Q: What sandbox constraint applies to Data Cloud One connections?
A: A sandbox home org may only pair with sandbox CRM orgs, and a production home org only with production orgs. The topology has to be planned in both tiers or the connection cannot be tested at all.
