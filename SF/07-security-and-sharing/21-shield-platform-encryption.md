# Shield Platform Encryption

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 11

**Scope:** Encryption at rest as a *product decision* — what it protects against, what it costs you in platform behaviour, and who holds the keys. The audit and monitoring pillars of Shield are [22](22-field-audit-trail-and-data-retention.md) and [23](23-event-monitoring-and-transaction-security.md).

## Core idea

Shield Platform Encryption encrypts field values, files and attachments at rest, in the database, with keys your org controls. What it does **not** do is control who sees data — a user with FLS on an encrypted field sees the plaintext exactly as before ([13](13-field-level-security-and-visibility-layers.md)). Its threat model is the storage layer and the compliance requirement, not the access model, and confusing the two is the commonest scoping error on the product. The useful architectural knowledge here is therefore not the cryptography, which is unremarkable, but the **incompatibility list**: encrypting a field changes what the platform can do with it, and those losses land on features nobody associated with encryption.

## How it works

| | Probabilistic *(default)* | Deterministic |
|---|---|---|
| same input → same ciphertext | no | yes |
| exact-match filter (`WHERE`, list views, report filters) | **no** | **yes** |
| sort (`ORDER BY`), ranges, `LIKE` | no | **no** |
| aggregates (`MIN`, `MAX`) | no | no |
| relative security | higher | lower — repeats are visible as repeats |

- **Choose per field, not per org.** Deterministic comes in case-sensitive and exact-match case-insensitive flavours; pick it only where a filter genuinely exists, because it leaks the equality relation.
- **Key material is a hierarchy you can own.** Salesforce-derived tenant secrets by default; **BYOK** uploads your own; **Cache-Only Key Service** keeps the key entirely outside Salesforce and fetches it per transaction — which also means your key endpoint's availability becomes your org's availability.
- **Rotating a key does not re-encrypt existing data.** Old data stays readable under the archived key until you mass-re-encrypt; rotation limits future exposure, not past.
- **Encrypting an existing field is a background job**, and the field is not filterable during it. Encrypt early or plan a window.
- **Encrypted data is decrypted in memory for Apex, Flow and the API**, so encryption is no defence against over-broad code. That is what [14](14-code-execution-context-and-security.md) is for.

## 2026 currency

Shield's encryption coverage keeps widening — platform events, Data 360 fields and more standard objects have been added release by release — and the reasonable working assumption is that **the feature list grew, the incompatibility list shrank, and neither disappeared**. Check the current *General Shield Platform Encryption Considerations* page in Salesforce Help against your specific field list before committing; the platform contradicts year-old blog posts routinely, in both directions. Treat any claim that a release lets you "encrypt everything with no loss of functionality" as unverified marketing until it appears in that page — the shape of this product has been *fewer exceptions, never none*, for a decade.

## Gotchas

- **Deterministic encryption still cannot sort.** People read "filtering works" and design a sorted list view; that is a different capability and it is not there.
- **Criteria-based sharing rules cannot use encrypted fields**, which quietly couples an encryption decision to the access model. → [09](09-sharing-rules-and-manual-sharing.md)
- **Duplicate management breaks on encrypted Account and Contact names** — matching rules need to compare, and they cannot.
- **`MIN`/`MAX`/`GROUP BY` on an encrypted field fail**, so an encrypted currency or date field takes a report with it. → [02-apex · 03](../02-apex-and-triggers/03-soql-fundamentals-and-relationship-queries.md)
- **External ID and unique fields conflict with probabilistic encryption**, so upsert keys and integration match fields need designing around it. → [08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md)
- **Managed packages may not tolerate encrypted fields** and the failure appears inside code you cannot read. Test in a sandbox with the package installed.
- **Cache-Only Key Service turns your key service into a hard dependency.** If it is unreachable, the data is unreadable — which is correct behaviour and a production incident.
- **Encryption does not satisfy a "restrict who can see it" requirement.** That is FLS plus sharing; saying otherwise in a compliance conversation is a credibility loss.

## Recall

Q: What does Shield Platform Encryption protect against, and what does it not?
A: Data at rest in the database and in files. It does not restrict who can see a field — an authorised user reads plaintext exactly as before.

Q: What does deterministic encryption enable, and what does it still not?
A: Exact-match filtering in SOQL `WHERE`, list views and report filters. It still cannot sort, range-filter, `LIKE`, or aggregate.

Q: Does rotating a key re-encrypt existing data?
A: No. Existing data stays readable under the archived key until you explicitly re-encrypt; rotation limits future exposure.

Q: What is the operational risk of Cache-Only Key Service?
A: The key never resides in Salesforce, so your key endpoint's availability becomes a hard dependency for reading your own data.

Q: Name two platform features encryption breaks that nobody expects.
A: Criteria-based sharing rules on the encrypted field, and duplicate management on encrypted Account/Contact names.

## Related

- [22 · Field Audit Trail & data retention](22-field-audit-trail-and-data-retention.md) — Shield's second pillar, and the one people actually buy it for
- [23 · Event Monitoring & Transaction Security](23-event-monitoring-and-transaction-security.md) — the third pillar
- [13 · Field-level security & visibility layers](13-field-level-security-and-visibility-layers.md) — the control that actually decides who sees a field
- [25 · Privacy, consent & data protection](25-privacy-consent-and-data-protection.md) — where the compliance requirement usually originates
