# Search configuration & Einstein Search

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 02

**Scope:** What an admin can tune about global search, and what Einstein Search adds for free. Programmatic search (SOSL) is [02-apex](../02-apex-and-triggers/INDEX.md).

## Core idea

Global search runs against a **search index**, not against the tables — which is why it is fast, why it is eventually consistent, and why "the record exists but search can't find it" is a normal condition rather than a bug. An admin does not control relevance directly; they control what goes into the index and what comes out of the results: searchable objects and fields, synonym groups, the fields shown per object, and how many results appear. **Einstein Search** sits on top and is on by default in Lightning Experience, so personalization and natural-language queries are the baseline behaviour users already have, not a project.

## How it works

- **Einstein Search, enabled by default**, contributes three things:
  - **Personalization** — reorders results toward the objects and records that user works with most, and improves per search.
  - **Actionable instant results** — record previews, actions, quick links and suggested searches the moment the cursor enters the search box.
  - **Natural language search** — everyday phrasing (`my open opportunities this month`, `cases closed last week`) resolves to a filtered list.
- **Synonym groups** (Setup → *Synonyms*): searching any term in a group returns results for every term in it. Up to **10,000 groups**, **6 terms** each. This is the main lever for company jargon — "PO", "purchase order", "requisition".
- **Search layouts** per object control which fields appear in search results, in lookups and in list-view buttons — the *Search Results* field set is what users read after searching.
- **Search Settings** (Setup) covers document content search, CJKT optimization, sidebar auto-complete, lookup behaviour and the number of results returned per object.
- **Promoted Search Terms** pin a **Knowledge article** to the top for chosen terms. It is a Knowledge feature, not a general relevance override.
- **Search Manager** is the newer surface for reviewing which objects and fields are searchable in one place instead of object by object.

## 2026 currency

Einstein Search needs no enablement in Lightning Experience and no separate licence — treat any guide that describes turning it on, or that presents personalization as a beta, as stale. Do not confuse **Einstein Search Dictionaries**, which is a **Commerce** storefront feature for shopper search synonyms, with the CRM synonym groups above; they are different products with similar names. Nothing in Summer '26 changed the admin surface.

## Gotchas

- **Indexing is asynchronous.** After a data load or a merge, records are unsearchable for a window; anything scripted against search immediately after DML is a race.
- **Formula fields are not indexed**, so a value a user can see on the page may be unfindable by search. Store it in a real field if it must be searchable.
- Search respects sharing, so "search is broken for that user" is usually an access question — verify with *Login As* before touching search config.
- Synonym groups are bidirectional and apply org-wide; a group added for one team changes everyone's results.
- Promoted search terms only affect **Knowledge articles**; using them to try to promote an Account or Case does nothing.
- Search layouts are per object **and** per profile in effect, because profile assignment decides which layout applies — a "missing column in results" ticket is layout, not index.
- Natural language search parses the phrase against fields it recognises; unusual custom field names simply do not resolve, and the query degrades to a keyword search with no warning.
- Number-of-results settings are per object, so a heavily used object can crowd the panel and hide the others.

## Recall

Q: Is Einstein Search something an admin turns on?
A: No — it is enabled by default in Lightning Experience, contributing personalization, actionable instant results and natural language search.

Q: What are the synonym group limits, and what does a group do?
A: Up to 10,000 groups of up to 6 terms; a search for any term in a group returns results for all of its terms.

Q: Why might a record that clearly exists not appear in global search?
A: The search index is updated asynchronously, the field may be a non-indexed formula field, or the user lacks sharing access.

Q: What do Promoted Search Terms apply to?
A: Knowledge articles only — they pin an article to the top of results for the chosen terms.

Q: Which similarly named feature is not part of CRM search configuration?
A: Einstein Search Dictionaries, which is a Commerce storefront feature for shopper search synonyms.

## Related

- [03 · Objects, fields & relationships](03-objects-fields-and-relationships.md) — which field types can be indexed at all
- [10 · Custom labels & Translation Workbench](10-custom-labels-and-translation-workbench.md) — searching in a multi-language org
- [02-apex · INDEX](../02-apex-and-triggers/INDEX.md) — SOSL, the programmatic path into the same index
