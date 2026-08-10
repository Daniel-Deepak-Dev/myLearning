# Lab Environment & Testing Craft — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.
> This is the file future-you re-reads in 5 minutes to reload the topic.

## In one sentence

Four ways to get data into a Data 360 tenant — and only one of them (**Data Cloud One companion**) needs a licence in the *other* org, which is why a plain Dev Edition can ingest from anything.

## Key terms

| Term | Definition |
|---|---|
| **Home org** | The org the Data 360 tenant is provisioned in. Its CRM data is connected by default. |
| **Standard CRM connection** | Data 360 ingests from *another* Salesforce org. Perm set + OAuth in the source org. **No licence needed there.** |
| **Companion connection** | Data Cloud One. Pushes unified *metadata* out to another org. Needs companion licences; prod↔prod or sandbox↔sandbox only. |
| **Ingestion API** | REST push into Data 360 from anything. Bulk (CSV) or streaming (incremental). Tenant-specific endpoint + OAS YAML schema. |
| **Platform Integration User** | The system user Data 360 reads back through. Its permission sets bound what you get. |
| **Data 360 Provisioning ("Everywhere")** | $0 SKU: EE/UE orgs get ~250k credits, 1 TB, 1 admin, ~100 users, 5 integration users. |

## Rules of thumb

- **Licence lives on the Data 360 side.** Source orgs need permissions, not licences.
- **Baseline before you build.** Counts and credit usage, written down, or you can't attribute anything later.
- **Green is not evidence.** Check the row count on every stream.
- **Break it on purpose once**, so you recognise the failure signature at a client.
- **Test data you invented > sample data you downloaded** — you know the right answer.
- **Never point a client sandbox at a personal tenant.** Second free DE org instead; $0 Provisioning for real work.
- **Keep identity-resolution datasets in the hundreds.** Credits are billed on records reviewed.

## Exam traps / common confusions

- "Connect an org" means **two opposite things**: standard CRM connection ingests data *in*; a Data Cloud One companion pushes metadata *out*.
- The source org in a standard CRM connection needs **no Data Cloud licence** — only a permission set and a user to OAuth as.
- Data Cloud One **cannot cross environments**: sandbox home ↔ sandbox companions, production ↔ production.
- A DLO query without `SET OPTIONS` for the data space returns **zero rows with no error** — not an empty DLO.
- An **unmapped DMO field returns null**, indistinguishable from real missing data.
- Over-matching in identity resolution reduces profile count, which looks like a **win** and is a privacy incident.

## Minimal example

Connect an unlicensed org as a source, in six steps:

```
SOURCE ORG (no Data 360 licence)
  1. New permission set
  2. Enable the Data 360 Salesforce Connector integration permissions
  3. Object: Read + View All   ·   Fields: Read
  4. Assign it to the user you'll authenticate as

DATA 360 ORG
  5. Setup → Salesforce CRM connector → New → OAuth as that user
  6. Pick objects → create data stream → run

VERIFY
  Stream refresh history: status Success AND row count > 0
  Query Workspace: SELECT COUNT(*) ... SET OPTIONS (dataspace = 'default')
  Compare against COUNT() in the source org
```
