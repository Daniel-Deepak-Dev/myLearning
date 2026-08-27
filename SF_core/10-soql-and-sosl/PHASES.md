# Phases for 10 · SOQL & SOSL

## Phase 22 — The query language as its own area · 10 files ✅

**The first new area since the skeleton, and the first added after the build was declared complete.** [../README.md](../README.md) had reserved the slot — *"Add as areas 10–12 later if wanted"* — so this is the plan being taken up rather than exceeded.

```
01-query-anatomy-and-the-soql-model.md
02-filtering-operators-and-literals.md
03-date-datetime-and-locale-literals.md
04-relationship-queries-in-depth.md
05-aggregates-group-by-rollup-and-cube.md
06-semi-joins-anti-joins-and-set-filtering.md
07-dynamic-soql-and-injection-defence.md
08-sosl-mechanics-and-the-search-index.md
09-sosl-search-modifiers-and-relevance.md
10-querying-across-stores-and-tooling.md
```

**The area exists because query knowledge was split five ways and one half of it was missing.** Before this run, SOQL lived in `02-apex · 03`/`04` (the language, mixed with Apex's API for it), `08-data · 08`/`09`/`11` (performance), `08-data · 12`/`13` (locking, `ALL ROWS`) and `06-integration · 04`/`07` (the wire endpoints). That split is defensible for *performance* — the numbers belong with the data area — and indefensible for the language itself, which had no owner.

**SOSL was the clearest gap in the vault.** The entire coverage was a four-row comparison table and about four bullets inside `02-apex · 04`. Grepping all of `SF_core/` for `SEARCH GROUP`, `WITH DATA CATEGORY`, `WITH SNIPPET`, `SPELL_CORRECTION`, `WITH HIGHLIGHT` and `toLabel` returned **zero hits each**. Two notes now carry it: [08](08-sosl-mechanics-and-the-search-index.md) for the engine and statement, [09](09-sosl-search-modifiers-and-relevance.md) for the modifiers and matching behaviour.

**Four SOQL features that were absent vault-wide.** `INCLUDES`/`EXCLUDES` for multi-select picklists, `GROUP BY ROLLUP`/`CUBE` with `GROUPING()`, `FORMAT()` and `toLabel()`. The first is the one most worth having written down: **the punctuation is the reverse of everyone's guess — a semicolon inside a quoted string means AND, a comma between strings means OR** — and getting it backwards returns a plausible, wrong row set with no error.

**A seed mapping that was marked done and never was.** [../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) row 83 records *Group By Rollup / Aggregate Functions + Group By Rollup* → `03-soql-fundamentals-and-relationship-queries` with a **✅**. That note contains no `ROLLUP`, and a vault-wide grep found the token only in the LWC GraphQL adapter note, describing a different feature. **The ✅ recorded an intent rather than a verified outcome** — a distinct failure mode from anything in [../CURRENCY.md](../CURRENCY.md), because nothing was ever *wrong*, only absent while marked present. The inventory rows are now repointed and [05](05-aggregates-group-by-rollup-and-cube.md) fulfils the mapping.

**The correction that reached outside this area.** Verifying `Database.Cursor` for [10](10-querying-across-stores-and-tooling.md)'s cross-store table surfaced a published error in the vault: phase 04 recorded cursors as **"GA and have been since Summer '24 (API 61.0)"**, in a `CURRENCY.md` callout headed *"Not new — a myth corrected in phase 04"*. Summer '24 was **Beta**. **GA is Spring '26, API 66.0** — Salesforce's own Spring '26 developer release guide says *"Apex cursors (now GA in API v66.0)"*. Corrected in four places: `CURRENCY.md`, `02-apex/INDEX.md`, `02-apex · 17` and the phase-04 entry in `02-apex/PHASES.md`. **The substance of the phase-04 finding survives** — a cursor is still not a row-limit escape hatch, and Salesforce's Spring '26 material now says so explicitly (*"Each fetch() counts against the SOQL query limit"*). Only the date was wrong. This is phase 13's lesson recurring: **a date is a citable fact and gets cited — verify it against the source, not against another note in the vault.** The specific trap is that *introduced* and *generally available* are different events, and phase 04 collapsed them. Also picked up: `Limits.getApexCursors()` and `Limits.getApexCursorRows()`.

**The 🆕 in this area is [10](10-querying-across-stores-and-tooling.md), and it is a bigger deal than its placement suggests.** **Named Query API is GA at Spring '26** (Beta Winter '26): an admin defines and validates SOQL **in Setup**, and saving it **automatically publishes a REST endpoint** — the query's name becomes the resource path, its parameters become URI query parameters — with the same definition exposable as a **custom agent action (Beta)**. It removes the commonest reason to write an `@RestResource` class at all, and moves part of the API contract from code review into Setup, which is a governance change as much as a developer-experience one. Alongside it, Winter '26 shipped **Database Insights** (inefficient SOQL with recommendations) and **Platform Cache Detection for SOQL** (repeat queries that should be cached), and Winter '25 added **SOQL stub methods for external objects in Apex tests**, far more specific **dynamic SOQL error messages**, and **negative currency support** in dynamic and API-issued queries.

**Two notes carry a ⚠️-grade finding without the flag**, because the old answer was never published here to correct. **[06](06-semi-joins-anti-joins-and-set-filtering.md):** at 67.0 an anti-join runs its subquery in user mode too, so `NOT IN (SELECT AccountId FROM Case)` means *"accounts with no cases **you** can see"* — and a low-privilege user therefore gets a **larger** result set than an administrator. That inverts the usual user-mode symptom, which is why it is worth stating rather than leaving as a corollary. **[04](04-relationship-queries-in-depth.md):** along a traversal path, **FLS raises an exception and sharing returns null** — the difference is the fastest available diagnosis of a query that "works for me".

**What this area deliberately does not contain.** Selectivity thresholds, Query Plan cost, skinny tables, the 10-second lock wait, and the soft-delete storage cost are all [08-data](../08-data-modeling-and-large-data-volumes/INDEX.md)'s and appear here only as links — verified by grepping the new files for `30%`, `10/5`, `1.0`, `10-second` and `ALL ROWS` and confirming each is a link rather than a restated number. **This area owns the `FOR UPDATE` clause; area 08 owns what the lock does.** Getting that boundary right was the main design risk in adding a tenth area that overlaps three existing ones.

**02 · 03 and 02 · 04 were narrowed, not moved.** Both keep their filenames — six external files and five inside area 02 link to them, and note 23 already set the precedent of keeping a filename because it is what a reader searches for. Their titles and scope lines now say they are the Apex-facing slice, and the language depth defers here.
