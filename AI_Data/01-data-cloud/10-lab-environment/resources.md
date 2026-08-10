# Lab Environment & Testing Craft — Resources

> Links checked 2026-08-10. Salesforce Help renders client-side, so these open fine in a browser but resist scripted fetching — read them in the org's own Help, not through a scraper.

## Official docs / Trailhead

**Connecting orgs**
- [Salesforce CRM Connector](https://help.salesforce.com/s/articleView?id=sf.c360_a_salesforce_crm_connector.htm&type=5) — the connector itself
- [Connect Salesforce CRM Orgs to Data 360](https://help.salesforce.com/s/articleView?id=data.c360_a_connect_salesforce_orgs.htm&type=5) — standard vs. companion, start here
- [Set Up a CRM Salesforce Org Connection](https://help.salesforce.com/s/articleView?id=data.c360_a_set_up_crm_connection.htm&type=5) — the click path for lab-02
- [Configure User Permissions for an External Salesforce Org Connection](https://help.salesforce.com/s/articleView?id=data.c360_a_setting_user_permissions_to_connect_external_org.htm&type=5) — **the source-org side; the article lab-02 is built on**
- [Object and Field Permissions for Salesforce CRM](https://help.salesforce.com/s/articleView?id=sf.c360_a_enable_user_permissions_external_salesforce_org.htm&type=5)
- [Data 360 Standard Permission Sets](https://help.salesforce.com/s/articleView?id=data.c360_a_userpermissions.htm&type=5)
- [Data Cloud One Companion Connections](https://help.salesforce.com/s/articleView?id=data.c360_a_companion_connections.htm&type=5) — the one you can't test on a DE
- [Connect Multiple Orgs with Data Cloud One](https://trailhead.salesforce.com/content/learn/modules/data-cloud-one-quick-look/connect-multiple-orgs-with-data-cloud-one) — Trailhead quick look

**Environments & limits**
- [Developer Edition Limits and Guidelines for Data 360](https://help.salesforce.com/s/articleView?id=data.c360_a_limits_and_guidelines_dev_ed.htm&type=5) — **read this before designing any lab**
- [Considerations for Sandbox in Data 360](https://help.salesforce.com/s/articleView?id=data.c360_a_data_cloud_sandbox_consideration.htm&type=5)
- [Free Data Cloud Account](https://help.salesforce.com/s/articleView?id=000396380&type=1) — what the $0 Provisioning SKU includes
- [Developer signup](https://www.salesforce.com/form/developer-signup/) — the free DE with Data 360 + Agentforce enabled
- [Cost and Usage](https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-cost-usage.html) — what actually consumes credits

**Ingestion API**
- [Ingestion API — Data 360 Integration Guide](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-ingestion-api.html)
- [Load Data Programmatically with the Ingestion API](https://developer.salesforce.com/blogs/2023/07/load-data-programmatically-with-the-ingestion-api) — dev blog walkthrough

## Courses & videos

- [Get Hands on with Data 360](https://developer.salesforce.com/workshops/agentforce-workshop/data-cloud/overview) — official 11-exercise workshop, Coral Cloud Resorts scenario: CRM connector → S3 → unified profile → calculated insights → query from Flow/SOQL. **The closest thing to a guided version of this ladder**; its S3 exercises need an AWS account, the rest don't.
- [Salesforce Data Cloud Workshop](https://datacloud-workshop.github.io/) ([repo](https://github.com/SFDC-Assets/data-cloud-workshop)) — self-guided lab plus reference-architecture ideation questions. Community-maintained, not official; assumes a facilitator-provided demo org.

## Articles & repos

- [Building a Data Cloud Ingestion API Utility on the Salesforce Platform](https://medium.com/@justusvandenberg/building-a-data-cloud-ingestion-api-utility-on-the-salesforce-platform-0e754bea8385) — Justus van den Berg. The "connect **any** org to **any** Data Cloud instance" pattern: custom auth provider + Named Credential + Apex, no middleware. Links the `lightweight-data-cloud-auth-provider` and `lightweight-data-cloud-util` packages. **Source for lab-03.**
- [mvrzan/salesforce-data-cloud-ingestion-api](https://github.com/mvrzan/salesforce-data-cloud-ingestion-api) — same API from AWS/Azure serverless, if you ever want the non-Salesforce side
- [Data 360 credits guide](https://www.szymonlewandowski.pl/blog/data-360/credits-guide) — Szymon Lewandowski; the clearest breakdown of what burns credits and the $0 Provisioning SKU contents
- [SDLC & Sandboxes in the Data Cloud One Multi-Org Ecosystem](https://www.salesforceblogger.com/2025/12/09/sdlc-sandboxes-in-the-data-cloud-one-multi-org-ecosystem/) — why the sandbox↔sandbox pairing rule shapes the whole SDLC
- [FREE Agentforce and Data Cloud Developer Org](https://www.apexhours.com/free-agentforce-and-data-cloud-developer-org/) — Apex Hours; what the current free DE actually ships with (1 data space, 10 GB, 150 LLM outputs/hr, expires after ~45 days idle)

## My own artifacts

**Org inventory** — fill this in as you provision:

| Alias | Type | Role in the ladder | Data 360? | Username |
|---|---|---|---|---|
| | DE | Data 360 home org (tenant) | ✅ | |
| | DE | source org for lab-02 / lab-03 | ❌ by design | |

- Lab runbooks: [labs/](labs/) — nine, each with results to fill in
- Baseline numbers: [labs/lab-00-tenant-baseline.md](labs/lab-00-tenant-baseline.md)
