---
vault: SF_Data_360
format: light
level: working
status: open
gaps: 2
org_checks: 1
labs: 3
created: 2026-10-02
updated: 2026-10-02
currency: "Summer '26 (API 67.0)"
---
# Identity Resolution

**One line:** A **ruleset** of match rules and reconciliation rules that links source records into one **unified profile** per person, without merging or deleting the source records.

**Reach for it when:** profile counts look wrong, an agent mixes up two customers, or someone proposes "just loosen the matching".

## Key points

- **Two rule types, two questions.** **Match rules** decide *when two records are the same person*. **Reconciliation rules** decide *which value wins* when matched records disagree.
- **Three match methods.** **Exact**: no typos, no format differences. **Fuzzy**: tolerates spelling differences, and is available **only for first name**. **Normalized**: same value regardless of formatting, for **email, phone and address**.
- **Three reconciliation rules:** **Last Updated**, **Most Frequent** and **Source Priority**. They are set at **object and field level**, so `Email` and `LifetimeValue` can follow different rules.
- **A ruleset targets one object**, such as Individual, and runs as a job. The output links each source record to its unified individual (Unified Individual and the link objects) → [Data model](data-model-dso-dlo-dmo.md).
- **Unified Link Individual is the bridge.** It joins each source record to its Unified Individual, so you can trace a profile value back to its source. Join Individual, Unified Link Individual and Unified Individual in SQL to see the result. The run also creates unified contact point objects.
- **Profile Explorer** shows one unified profile as a dashboard. Use it to check a resolved profile against its sources.
- **Real-time identity resolution** compares an active visitor with existing profiles in milliseconds. It uses an existing ruleset whose output feeds a **real-time data graph**.
- **Under-matching vs over-matching are not symmetric.** Too strict splits one person into several profiles, so the agent sees part of their history. Too loose merges two people, so one customer's data reaches another. That is a **privacy incident**.

## Gotchas

- **Over-matching is the cheaper direction, and the dangerous one.** Fewer profiles look like success. A merged profile looks exactly like a correctly resolved one.
- **Fuzzy first name plus a shared address collapses households**: spouses, joint account holders, generations at one address.
- **Rulesets run as jobs, not instantly.** A new record can sit unresolved, and an agent may briefly see a fragment.
- **Don't tune matching on a broken model.** If each source has its own custom DMO, fix the mapping first; match tuning on unaligned DMOs is thrown away.
- 🚩 **Billing is reported to be per unified profile**, so poor matching may become a recurring cost. That figure came from non-Salesforce sources; check the contract.

## Gaps to close

- [ ] Re-read Identity Resolution Rulesets, Match Methods and Reconciliation Rules in full once help.salesforce.com is reachable. This note was built from search extracts.
- [ ] What are the limits on rulesets per data space and match rules per ruleset at API 67.0?

## Confirm in org

- 🚩 How long does a ruleset run take on a few hundred records in a Developer Edition, where scheduled ruleset jobs are not available?

## Hands-on

- [ ] **D360-IDR-01** · 30 min · Load three sources (CRM Contact, an Ingestion API file and a CSV) with planned duplicates, build an exact-email ruleset, and record the profile count. **Proves:** the profile-to-source ratio is the baseline you tune against.
- [ ] **D360-IDR-02** · 20 min · Add a fuzzy first name + normalized address rule against two invented people at one address. **Proves:** the household merge looks like a cleaner result; open the unified profile to see the wrong data.
- [ ] **D360-IDR-03** · 20 min · Set Source Priority on Email and Last Updated on Phone, then change both in one source. **Proves:** reconciliation is per field; check which value won.

## Related

- [Data Model: DSO, DLO & DMO](data-model-dso-dlo-dmo.md) — matching runs on DMO fields
- [Calculated Insights & Segmentation](calculated-insights-and-segmentation.md) — computed per unified profile, so it inherits every matching error
- [Vector Search & RAG](vector-search-and-rag.md) — data graphs, the read path real-time resolution feeds
- [SF_core · 08-data · 19 Data quality, deduplication & MDM](../SF_core/08-data-modeling-and-large-data-volumes/19-data-quality-deduplication-and-mdm.md) — CRM duplicate rules and merge, which resolution does not replace
- [Interview · Identity & segmentation](../Interview/02-data-360/02-identity-and-segmentation.md) — the household-collapse and ruleset-change scenarios

## Sources

- [Identity Resolution Rulesets](https://help.salesforce.com/s/articleView?language=en_US&id=data.c360_a_identity_resolution_ruleset.htm&type=5) — Salesforce Help · via search 2026-10-02 · match and reconciliation rules about a specific object
- [Identity Resolution Match Methods](https://help.salesforce.com/s/articleView?language=en_US&id=data.c360_a_match_rules_criteria_fuzzy_normalized.htm&type=5) — Salesforce Help · via search 2026-10-02 · exact, fuzzy (first name only), normalized (email, phone, address)
- [Identity Resolution Reconciliation Rules](https://help.salesforce.com/s/articleView?language=en_US&id=sf.c360_a_reconciliation_rules.htm&type=5) — Salesforce Help · via search 2026-10-02 · Last Updated, Most Frequent, Source Priority; object and field level
- [Real-Time Identity Resolution](https://help.salesforce.com/s/articleView?language=en_US&id=data.c360_a_identity_resolution_real_time.htm&type=5) — Salesforce Help · via search 2026-10-02 · milliseconds; ruleset output feeds a real-time data graph
- [Unify Your Data](https://trailhead.salesforce.com/content/learn/projects/explore-data-cloud-core-functionality/unify-your-data) — Trailhead · via search 2026-10-02 · reconciliation by frequency, recency or source
- [Building a Complete View of Your Customers with Data Cloud and Identity Resolution](https://developer.salesforce.com/blogs/2024/10/data-cloud-and-identity-resolution) — Salesforce Developers blog · via search 2026-10-02 · Unified Link Individual joins source data to the unified individual
- [Understand Unified Profiles](https://trailhead.salesforce.com/content/learn/modules/data-and-identity-in-salesforce-cdp/get-to-know-unified-profiles) — Trailhead · via search 2026-10-02 · unified, link and unified contact point objects
- [Profile Explorer in Data 360](https://help.salesforce.com/s/articleView?language=en_US&id=data.c360_a_profile_explorer.htm&type=5) — Salesforce Help · via search 2026-10-02 · validate unified profile data

## History

- 2026-10-02 · created — facts carried over from the archived roadmap notes and confirmed against Salesforce search extracts; corrected "most recent" to the documented **Last Updated** and narrowed fuzzy matching to first name
- 2026-10-02 · updated — Unified Link Individual and Profile Explorer, for the terminology flashcards
