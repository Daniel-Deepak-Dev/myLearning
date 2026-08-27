# Privacy, Consent & Data Protection

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 11

**Scope:** The obligations that come from outside the org — consent, subject rights, retention and non-production data — and the platform objects that record them. Encryption as a control is [21](21-shield-platform-encryption.md); the AI-side governance story is [AI_Data](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Core idea

Everything else in this area answers *may this user see this record*. Privacy asks a different question that the access model cannot express: **should this data exist here at all, and did the person it describes agree to what you are doing with it?** Salesforce's answer is a **data model**, not a feature — a set of standard objects centred on `Individual` that record preferences about a *person*, independent of which Lead, Contact, Person Account or User row happens to represent them today. That decoupling is the whole design: a person who opts out should stay opted out when they later appear as a different record type, and only a person-level object can hold that.

## How it works

| Level | What it expresses | Where it lives |
|---|---|---|
| **Global** | all-or-nothing preferences for the person | `Individual` — *Don't Process*, *Don't Market*, *Don't Track*, *Forget this Individual* |
| **Engagement channel** | consent per channel — email, phone, post | `ContactPointTypeConsent` |
| **Contact point** | consent for one specific address or number | `ContactPointEmail`, `ContactPointPhone`, `ContactPointConsent` |
| **Data use purpose** | consent for a *reason* — marketing, research, service | `DataUsePurpose`, joined to the consent records |

- **`Individual` is created and linked, not derived.** Enable *Data Protection and Privacy* in Setup, then relate Lead, Contact, Person Account and User records to one `Individual` — the linkage is your job and the model is worthless without it.
- **The consent flags are records, not enforcement.** Nothing on the platform refuses to send an email because *Don't Market* is checked; your automation must check it. That is the single most misunderstood thing about the model.
- **Privacy Center is the paid add-on** that operationalises subject rights — retention policies, right-to-be-forgotten runs, data portability exports — on top of the same objects.
- **Data Mask handles the non-production half.** It anonymises, pseudonymises, pattern-matches or deletes sensitive data **in a sandbox** after refresh, which is the standard answer to "production PII is sitting in five developer sandboxes". → [09-devops · INDEX](../09-devops-sfdx-and-release-management/INDEX.md)
- **Deletion is harder than it looks.** A subject-rights erasure has to reach field history ([22](22-field-audit-trail-and-data-retention.md)), event logs ([23](23-event-monitoring-and-transaction-security.md)), big objects, backups and any replicated copy in a warehouse — the CRM record is the easy part.

## Gotchas

- **Consent records enforce nothing.** Every flow, Apex class and marketing integration must consult them; the platform will happily send to an opted-out contact point.
- **Field-level security is not a privacy control.** Hiding a field from a user does not reduce what the org processes, and a regulator asks about processing. → [13](13-field-level-security-and-visibility-layers.md)
- **Encryption is not anonymisation.** Encrypted personal data is still personal data — reversible by design, and therefore still in scope. → [21](21-shield-platform-encryption.md)
- **Sandbox PII is the finding that turns up in every audit**, because refreshing a Full sandbox copies real data by default and nobody owns the follow-up. Automate masking as part of the refresh.
- **"Forget this Individual" is a flag, not an erasure.** It records the request; carrying it out is a process you build or buy.
- **Consent captured in Experience Cloud lands as a guest-user write**, which needs the sharing and object permissions to exist first. → [05-experience-cloud · INDEX](../05-experience-cloud-lwr/INDEX.md)
- **Retention obligations point both ways.** Privacy law says delete it; financial regulation says keep it ten years. `HistoryRetentionPolicy` and the archive are how you hold both at once. → [22](22-field-audit-trail-and-data-retention.md)
- **Agents widen the processing surface.** An agent that summarises a customer's history is processing personal data at speed — the grounding and retention rules live in [AI_Data](../../AI_Data/05-release-radar/trust-security-and-governance.md), not here.

## Recall

Q: Why does the consent model centre on `Individual` rather than on Contact?
A: Preferences belong to a *person*, who may exist as a Lead today and a Contact tomorrow. Only a person-level object keeps the opt-out attached across those records.

Q: What are the four levels of the Salesforce consent data model?
A: Global (on `Individual`), engagement channel, contact point, and data use purpose.

Q: Does checking *Don't Market* stop Salesforce sending marketing email?
A: No. The consent objects record intent; enforcement is entirely up to your automation and integrations.

Q: What is the standard answer to production PII in sandboxes?
A: Data Mask — anonymise, pseudonymise, pattern-match or delete sensitive data in the sandbox after refresh, as part of the refresh process.

Q: Why is a subject-rights erasure not just a record delete?
A: The data also sits in field history, event logs, big objects, backups and replicated copies — all of which are in scope and none of which a record delete touches.

## Related

- [22 · Field Audit Trail & data retention](22-field-audit-trail-and-data-retention.md) — retention as a policy object, and the archive erasure has to reach
- [21 · Shield Platform Encryption](21-shield-platform-encryption.md) — the control most often mistaken for a privacy answer
- [13 · Field-level security & visibility layers](13-field-level-security-and-visibility-layers.md) — visibility, which is not the same as processing
- [AI_Data · trust, security & governance](../../AI_Data/05-release-radar/trust-security-and-governance.md) — where the agent-era version of this conversation continues
