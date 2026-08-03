# Cross-Org Data Sharing & Consolidation

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** Data across more than one Salesforce org — sharing it, unifying it, or collapsing the orgs. The org-strategy view is [01-admin · 18](../01-admin-and-declarative-platform/18-salesforce-foundations-and-org-strategy.md); the migration mechanics are [25](25-data-migration-and-cutover.md).

> **What changed.** **Salesforce-to-Salesforce is being retired.** No new enablement from **Spring '26**, **support ended in Summer '26**, and it is **fully retired in Spring '27 — it stops functioning**. Any org still publishing or subscribing records over S2S has a migration with a fixed deadline. Salesforce names Partner Cloud, **Data Cloud One**, MuleSoft Anypoint and MuleSoft for Flow as the replacements, and which one you need depends on why the orgs are separate.

## Core idea

Multiple orgs are almost always the residue of something else — an acquisition, a regional rollout, a business unit that bought its own. The data question that follows is narrower than "should we consolidate": it is **do these orgs need to share records, to see a shared picture, or to become one?** Those are three different projects with three different price tags.

The trap is answering the third question when the business only asked the first. Consolidation is a migration, a deduplication and an access-model rebuild happening at once, and it is rarely the cheapest way to get a shared customer view — that is what unification at the data tier is for.

## How it works

| Need | Answer | Notes |
|---|---|---|
| Hand records to a partner org | **Partner Cloud** | branded, with end-to-end visibility |
| Read another org's data live | **Salesforce Connect cross-org adapter** | **gained named credential support in Summer '26** → [06-integration · 20](../06-integration-and-apis/20-salesforce-connect-and-external-objects.md) |
| One customer view across orgs | **Data Cloud One** / Data 360 | unification without merging → [18](18-zero-copy-and-data-360-as-data-tier.md) |
| Event-driven sync | Pub/Sub, CDC, Event Relay | → [06-integration · 13](../06-integration-and-apis/13-change-data-capture.md) |
| Orchestrated, transformed sync | MuleSoft | where mapping is non-trivial |
| Become one org | migration + dedup + access rebuild | → [25](25-data-migration-and-cutover.md) |

- **Record Ids do not travel.** An Id is meaningful only in the org that issued it, so every cross-org design keys on an **External ID** → [03](03-record-ids-external-ids-and-upsert.md).
- **Limits are per org.** Two orgs have two API allocations, two storage allocations and two sets of governor limits — which is occasionally the honest reason to keep them apart → [06](06-storage-model-and-schema-limits.md).
- **Consolidation is three projects.** Migrate the data, resolve the duplicates the merge exposes ([19](19-data-quality-deduplication-and-mdm.md)), and rebuild the access model, because two orgs never share a role hierarchy or a permission design → [07-security · 03](../07-security-and-sharing/03-profiles-and-the-permission-set-led-model.md).
- **Metadata divergence bites before data does.** Two orgs' picklist values, record types and currencies are the mapping work nobody scoped.

## 2026 currency

Beyond the S2S retirement above, the direction of travel is that **cross-org problems are increasingly solved at the data tier rather than by moving records**. Data Cloud One unifies profiles across orgs without either org giving up its records, which is a fundamentally different answer from S2S's publish-and-subscribe copying. Worth noting the naming: the feature keeps the words **Data Cloud** even though the product was renamed **Data 360** in October 2025 → [18](18-zero-copy-and-data-360-as-data-tier.md). On the federation side, the cross-org adapter's Summer '26 named credential support removes the weakest link in org-to-org connections → [06-integration · 17](../06-integration-and-apis/17-named-credentials-and-external-credentials.md).

## Gotchas

- **S2S has a hard stop.** Support ended Summer '26; it stops working in Spring '27. Inventory publish/subscribe connections now, not in the release that breaks them.
- **"We'll just merge the orgs" is a multi-quarter programme**, and its longest pole is usually the access model, not the data.
- **Duplicates are created by consolidation, not discovered by it** — the same customer exists legitimately in both orgs until the moment they do not.
- **Cross-org federation inherits every external-object limitation**: no triggers, no roll-ups, no sharing rules → [17](17-external-objects-vs-replicated-copies.md).
- **The source org's outage becomes the target org's outage** for anything federated live.
- **Currency and locale settings rarely match between orgs**, and multi-currency cannot be enabled reversibly to fix it → [22](22-multi-currency-multi-language-and-locale.md).
- **Retiring an org is a retention decision.** Something must hold its data for as long as the obligation runs → [15](15-archiving-and-retention-strategy.md).

## Recall

Q: What is the retirement timeline for Salesforce-to-Salesforce?
A: No new enablement from Spring '26, support ended Summer '26, fully retired and non-functional in Spring '27.

Q: What does Salesforce name as the replacements for S2S?
A: Partner Cloud, Data Cloud One, MuleSoft Anypoint and MuleSoft for Flow — chosen by why the orgs are separate.

Q: Why can't a cross-org integration key on record Ids?
A: Ids are only meaningful in the org that issued them; cross-org designs key on External IDs.

Q: What are the three projects hiding inside an org consolidation?
A: A data migration, a deduplication, and a rebuild of the access model.

Q: Which cross-org connector improved in Summer '26?
A: The Salesforce Connect cross-org adapter, which gained named credential support.

## Related

- [25 · Data migration & cutover](25-data-migration-and-cutover.md) — consolidation is this, with a second Salesforce org as the source
- [17 · External objects vs replicated copies](17-external-objects-vs-replicated-copies.md) — the same copy-or-federate decision between orgs
- [18 · Zero-copy & Data 360 as data tier](18-zero-copy-and-data-360-as-data-tier.md) — unification as the alternative to consolidation
- [01-admin · 18 Salesforce Foundations & org strategy](../01-admin-and-declarative-platform/18-salesforce-foundations-and-org-strategy.md) — why the org count is what it is
