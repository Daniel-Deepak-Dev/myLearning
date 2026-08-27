# Harmonization & Identity Resolution — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Match rules decide *when* two records are the same person, reconciliation rules decide *which value wins* — and since March 2026 the resulting profile count is what you're billed on.

## Key terms
| Term | Definition |
|---|---|
| Match rules | Exact or fuzzy criteria deciding when two records represent one person. |
| Reconciliation rules | Which value wins on conflict: most recent, most frequent, source priority. |
| Ruleset | Both rule types bundled, run on a schedule. |
| Unified profile | The output — and **the billing unit** (~$240 per 1,000). |

## Rules of thumb

- Set reconciliation **per attribute**. The right rule for `Email` is rarely right for `LifetimeValue`.
- Track **profile count ÷ source-record count** over time. Far below expectation = over-matching; far above = fragmentation.
- Prefer a shared customer ID → exact email → fuzzy name+phone. Fuzzy name+address is a last resort.
- Cost case: profile count × $0.24/month. A 15% duplicate rate is a number a CFO understands.

## Exam traps / common confusions

- A "profile" for billing is a **unified individual after resolution**, not a raw source row.
- **Over-matching is the dangerous direction** — cheaper *and* a privacy incident (Person A's data visible to Person B). Never tune on cost alone.
- **Fuzzy name + address merges households**: two people, one address, similar names → one profile.
- Rulesets run **on a schedule** — a new record isn't resolved the instant it lands.
- A fragmented profile makes an agent answer from partial history, confidently. Data failure, looks like an AI failure.

## Minimal example

```
CRM Contact    "J. Smith, jsmith@acme.com, 555-0100"
Marketing lead "John Smith, jsmith@acme.com"        → MATCH on email
Web SDK event  "john.smith@acme.com, 555-0100"      → MATCH on phone
                          ↓ reconcile: most recent wins on Name
                  UNIFIED PROFILE  (billed once)

Under-match → 3 profiles → 3× bill + agent sees ⅓ of history
Over-match  → 1 profile  → cheaper + privacy incident
```
