# Lab 99 — Parked: External Sources

> Status: ⏸️ parked — each needs an account you don't currently have

Not abandoned. Written up now, while the context is fresh, so that the day an account appears the lab is a two-hour job rather than a research project.

## S3 connector

**Needs:** an AWS account (free tier is enough — a bucket and a few CSVs).

**Would teach:** the most common real-world ingestion pattern by far. Batch file ingestion, the manifest/prefix conventions, refresh scheduling, and how file-based streams fail differently from CRM streams (bad row → whole file? just the row?).

**Shortcut:** the [official Data 360 workshop](https://developer.salesforce.com/workshops/agentforce-workshop/data-cloud/overview) is built on exactly this — Coral Cloud Resorts with contacts in CRM and reservations in S3. Do its S3 exercises rather than inventing your own.

## Zero-copy federation

**Needs:** a Snowflake trial (~30 days, credit-limited), a BigQuery sandbox, or Databricks free edition.

**Would teach:** the ingest-vs-federate decision, which is a genuine architecture choice and a frequent exam topic. The lab that matters is measuring **query latency federated vs. ingested for the same dataset** — the number is the argument. Also worth probing: where identity resolution and segmentation behave differently on federated data.

**Watch out:** trials expire mid-lab. Plan it as one sitting. See [zero copy & BYOL](../../06-zero-copy-byol/notes.md).

## Web SDK / engagement data

**Needs:** somewhere to host a static page — GitHub Pages is free and sufficient.

**Would teach:** the only source of genuinely *behavioural* data in the ladder. Engagement DMOs behave differently from profile DMOs, and identity resolution across anonymous → known (a visitor browsing, then logging in) is the interesting case. It's also the fastest way to see streaming ingestion arrive in near-real-time without writing any Apex.

**This is the highest-value parked lab** — it needs the least infrastructure and teaches something none of labs 00–07 cover.

## Marketing Cloud activation

**Needs:** a Marketing Cloud licence. Not happening on a personal tenant.

**Instead:** activate a segment to a target you *do* have (CRM, or a file export) and read the docs for the MC path. Then be honest about the distinction — "I've activated to CRM, I've read the MC integration" is a perfectly good sentence in an interview. Claiming the MC experience you don't have is not.
