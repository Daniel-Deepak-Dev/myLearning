---
vault: SF_Data_360
format: light
level: basic
status: open
gaps: 1
org_checks: 1
labs: 3
created: 2026-10-02
updated: 2026-10-02
currency: "Summer '26 (API 67.0)"
---
# Lab Environment

**One line:** Where to practise Data 360 without a client tenant, what a Developer Edition org can and can't do, and which orgs can feed it.

**Reach for it when:** you are about to start the Data 360 labs, or a design depends on a connection you have never wired.

## Key points

- **A Developer Edition with Data 360 has hard limits:** **1 data space** (the default), **10 GB** of data, at most **5 batch transforms**, and **no scheduled refreshes** or scheduled ruleset jobs. You run everything manually.
- **The home org's own CRM data is connected by default.** No connection to create: pick objects and build streams → [Ingestion](ingestion-and-data-streams.md).
- **A standard CRM connection ingests from another Salesforce org.** Any CRM org, including a sandbox or another Developer Edition, can be a source. The source org needs **no Data 360 licence**, only a permission set on the user who authorizes the connection.
- **The Data Cloud Salesforce Connector permission set** controls which objects the connector reads. Since Winter '25 it has **View All Data** on by default in new orgs.
- **The Ingestion API works from anything** — an org with no connector, a script, a serverless function → [Ingestion](ingestion-and-data-streams.md).
- **Enterprise Edition and above can provision Data 360 at no cost** with the Data 360 Provisioning (Everywhere) licence, added under *Your Account*.
- **Four standard permission sets.** **Data Cloud Architect** (formerly Data Cloud Admin): everything. **Data Cloud Activation Manager** (formerly Marketing Manager): activation targets and activations. **Data Cloud Activation Specialist** (formerly Marketing Specialist): segments. **Data Cloud User**: view only.
- **Three tools to look at data.** **Data Explorer** browses objects. **Profile Explorer** shows one unified profile → [Identity resolution](identity-resolution.md). **Query Editor** runs Data 360 SQL over DLOs, DMOs, CIOs and data graphs. Both explorers are on by default for admins; other users need a permission set.
- **Everything spends credits.** **Data Services credits** are Data 360's own currency, split into 21 usage types; **Flex Credits** also cover generative AI. Credits used = units × the rate-card multiplier, tracked on **Digital Wallet** consumption cards.

## Gotchas

- **Don't connect a client sandbox to a personal Developer Edition.** It works technically, and it moves client data into a tenant they don't control. Use a second Developer Edition seeded with invented data.
- **"Green" is not evidence.** A stream can succeed with 0 rows, a DLO query without a dataspace returns 0 rows, and an unmapped field reads as null.
- **Invented test data beats downloaded samples.** You know the right answer, so you can tell when identity resolution is wrong.
- **Some things can't be learnt on a Developer Edition:** multi-org Data Cloud One, real sandbox-to-production promotion, scale behaviour and production cost. Say "I've read the constraints, I haven't run it."

## Gaps to close

- [ ] Re-read Developer Edition Limits and Guidelines for Data 360 and Set Up and Turn On Data 360 in full once help.salesforce.com is reachable. This note was built from search extracts.

## Confirm in org

- 🚩 Does a newly signed-up Developer Edition show *Data 360 Setup*, or does it need a Partner Developer Edition?

## Hands-on

- [ ] **D360-LAB-01** · 15 min · Open Data 360 Setup in your Developer Edition, record the data space count, storage used and the limits page. **Proves:** your baseline before any lab, so later counts mean something.
- [ ] **D360-LAB-02** · 30 min · Connect a second Developer Edition as a standard CRM source: permission set on the source user, then OAuth from the Data 360 org. **Proves:** the source needs no Data 360 licence; the connection borrows that user's access. **Needs:** a second Developer Edition.
- [ ] **D360-LAB-03** · 15 min · Remove one field's read permission in the source org and refresh the stream. **Proves:** permission failures show up as missing data, not as errors. **Needs:** #2.

## Related

- [Ingestion & Data Streams](ingestion-and-data-streams.md) — the three ways in that this lab environment exercises
- [Data 360 DevOps](data-360-devops.md) — what you can't practise without a real sandbox
- [Identity Resolution](identity-resolution.md) — the topic where invented test data matters most

## Sources

- [Developer Edition Limits and Guidelines for Data 360](https://help.salesforce.com/s/articleView?language=en_US&id=data.c360_a_limits_and_guidelines_dev_ed.htm&type=5) — Salesforce Help · via search 2026-10-02 · 1 data space, 10 GB, 5 batch transforms, no scheduled refreshes or ruleset jobs
- [Set Up a Standard Salesforce Org Connection in Data Cloud](https://help.salesforce.com/s/articleView?id=sf.c360_a_set_up_crm_connection.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-02 · connect orgs other than the home org
- [Data 360 Standard Permission Sets](https://help.salesforce.com/s/articleView?id=data.c360_a_userpermissions.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-02 · the Salesforce Connector permission set; View All Data by default since Winter '25
- [Free Data Cloud Account](https://help.salesforce.com/s/articleView?language=en_US&id=000396380&type=1) — Salesforce Help · via search 2026-10-02 · Enterprise Edition and above, Data 360 Provisioning at no cost
- [Data Cloud Standard Permission Sets](https://help.salesforce.com/s/articleView?language=en_US&id=sf.c360_a_userpermissions.htm&type=5) — Salesforce Help · via search 2026-10-02 · Architect, Activation Manager, Activation Specialist, User; the former names
- [Grant or Remove Access to Data Explorer or Profile Explorer](https://help.salesforce.com/s/articleView?language=en_US&id=sf.c360_a_enable_data_explorer_permissions.htm&type=5) and [Query Editor](https://help.salesforce.com/s/articleView?id=sf.c360_a_query_editor.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-02
- [Data Services Billable Usage Types](https://help.salesforce.com/s/articleView?id=data.c360_a_data_usage_types.htm&language=en_US&type=5) and [Maximize Your Data 360 Credits](https://trailhead.salesforce.com/content/learn/modules/data-cloud-credit-consumption-quick-look/get-started-with-data-cloud-credit-consumption) — Salesforce Help, Trailhead · via search 2026-10-02 · 21 usage types; Flex Credits; units × multiplier; Digital Wallet

## History

- 2026-10-02 · created — facts carried over from the archived lab-environment note and confirmed against Salesforce search extracts
- 2026-10-02 · updated — standard permission sets, the three data tools and credits, for the terminology flashcards
