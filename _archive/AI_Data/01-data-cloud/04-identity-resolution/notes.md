# Harmonization & Identity Resolution

> Track: Data 360 · Roadmap: Phase 02 · Weeks 5–8 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/pricing-and-certification.md](../../05-release-radar/pricing-and-certification.md)

**Roadmap scope:** Match rules, reconciliation rules, rulesets, and how unified individual profiles get built from messy multi-source data.

## What is it?

**Identity resolution** turns many source records into one **unified profile** per real person. Two rule types do the work, and the exam wants the distinction crisp:

| Rule type | Question it answers |
|---|---|
| **Match rules** | *When are two records the same person?* Exact or fuzzy — email, name+phone, address |
| **Reconciliation rules** | *Which value wins when matched records disagree?* Most recent, most frequent, source priority |

A **ruleset** bundles both and runs on a schedule. The output is the unified profile: one individual, linked to all its source records and behaviours.

```
CRM Contact       "J. Smith, jsmith@acme.com, 555-0100"
Marketing lead    "John Smith, jsmith@acme.com"          ──► MATCH (email)
Web SDK event     "john.smith@acme.com, 555-0100"        ──► MATCH (phone)
                                    │
                          RECONCILIATION
                    (most recent wins on name)
                                    │
                            UNIFIED PROFILE
                       "John Smith, jsmith@acme.com"
```

## Why it matters (for the AI-Salesforce architect role)

**This changed from a quality concern into a cost concern on March 2, 2026 — and that's the most useful thing on this page.**

Data 360 pricing was rebuilt around a **profile-based SKU: ~$240 per 1,000 profiles** baseline, ~$420 premium. And a "profile" means a **unified individual after identity resolution** — not a raw source row.

So you are billed on the *output* of your ruleset.

| Before (credit metering) | After (profile pricing) |
|---|---|
| Rewarded processing less | Rewards **resolving fewer, better profiles** |
| Match quality was a quality issue | Match quality is a **recurring line item** |

Duplicates and under-matches now inflate a recurring bill directly. That puts money behind identity-resolution quality for the first time, and it gives you an argument that lands with a CFO rather than only with a data team.

**The two failure directions, and why they're asymmetric:**

- **Under-matching** (too strict) → one person becomes three profiles → you pay three times, *and* the agent sees a third of their history
- **Over-matching** (too loose) → two people merge into one profile → cheaper, but you've shown Person A's data to Person B

Over-matching is the dangerous one. It's cheaper *and* it's a privacy incident. Never tune matching on cost alone.

**Downstream, it caps agent quality.** If the agent grounds on a fragmented profile, it answers from a third of the customer's history and sounds confident doing it. That's a data-architecture failure that presents as an AI failure.

## How it works

### Match rule design

| Strategy | Precision | Use when |
|---|---|---|
| Exact on email | High | Email is reliably captured and unique |
| Exact on a customer ID | Highest | A shared identifier exists across sources |
| Fuzzy name + exact phone | Medium | No shared key; typical for merged CRM estates |
| Fuzzy name + address | Lower | Last resort — households collapse into individuals |

**The household problem** is the classic fuzzy-matching trap: two people at one address with similar names merge, and now a spouse's data is visible in the other's profile.

### Reconciliation strategies

- **Most recent** — good for changeable attributes (phone, address, job title)
- **Most frequent** — good where one source is often wrong but not consistently
- **Source priority** — good where you *know* one system is authoritative (CRM over a web form)

Set these per attribute, not globally. The right answer for `Email` is rarely the right answer for `LifetimeValue`.

### Measuring it

Before tuning, know your baseline: **profile count vs. source-record count**. A ratio far below expectation suggests over-matching; far above suggests fragmentation. Under profile pricing, this ratio is also your bill, so it's worth tracking over time rather than checking once.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

**→ [lab-04](../10-lab-environment/labs/lab-04-identity-resolution.md)** runs all of this across three sources, with a test set designed so the ruleset can visibly fail.

- [ ] Build a ruleset with exact-email matching, then add a fuzzy rule and compare profile counts. The delta is the money.
- [ ] **Deliberately over-match** in a sandbox (fuzzy name + address on test data with two people at one address) and look at the merged profile. Seeing the privacy failure once makes it memorable.
- [ ] Set different reconciliation strategies per attribute and verify which value won.
- [ ] Calculate the monthly cost of your current profile count at ~$240/1,000, then at a 15% duplicate rate. That's the business case.

## Gotchas & sharp edges

- **You're billed on unified profiles, not source rows.** Poor matching is a recurring cost, not a one-off cleanup task.
- **Over-matching is a privacy incident, not just a data-quality issue** — and it's the *cheaper* direction. Never tune on cost alone.
- **Fuzzy name + address merges households.** Two people, one address, similar names → one profile.
- **Reconciliation should be per attribute.** A global strategy is almost always wrong for something.
- **Rulesets run on a schedule.** A new record isn't resolved the instant it lands, so an agent may briefly see an unresolved fragment.
- **Changing the primary key upstream breaks matching.** Decide it during [data modeling](../03-data-modeling-dso-dlo-dmo/notes.md), not here.
- **A fragmented profile makes the agent look stupid.** It answers from partial history, confidently. Check profile completeness before blaming grounding or the model.

## Related topics

- [Data modeling DSO → DLO → DMO](../03-data-modeling-dso-dlo-dmo/notes.md) — matching runs on DMO fields
- [Ingestion](../02-ingestion/notes.md) — duplicate-heavy sources inflate profile counts
- [Insights & segmentation](../05-insights-segmentation/notes.md) — computed per unified profile
- [RAG on platform](../08-rag-on-platform/notes.md) — what the agent actually grounds on
- [Release radar: pricing and certification](../../05-release-radar/pricing-and-certification.md) — the March 2026 pricing rebuild
