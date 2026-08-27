# SOSL Search Modifiers & Relevance

> Area: 10-soql-and-sosl · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 22

**Scope:** The optional `WITH` clauses that scope, enrich and correct a search, plus the matching behaviour — stemming, synonyms and ranking — that decides what comes back first. The statement itself is [08](08-sosl-mechanics-and-the-search-index.md).

## Core idea

The `FIND` clause decides *what* matches. Everything in this note decides **which slice of the org is searched and what the user sees of the match** — and these are the parts that turn a working search box into a good one. Two of them change results (`DATA CATEGORY`, `NETWORK`, `DIVISION`, `PRICEBOOKID` scope the corpus; `SPELL_CORRECTION` changes what was searched for), and two of them change presentation without changing the result set at all (`SNIPPET` and `HIGHLIGHT`). The distinction matters because the presentation modifiers are cheap to add and the scoping ones silently alter counts — a search that "stopped finding things" after a `WITH NETWORK` was added is not broken.

## How it works

| Clause | Effect |
|---|---|
| `WITH DATA CATEGORY` | restricts to Knowledge article categories — `WITH DATA CATEGORY Geography__c ABOVE_OR_BELOW usa__c` |
| `WITH NETWORK` | scopes to one or more Experience Cloud sites, or `'NetworkIdSpec'` for all |
| `WITH DIVISION` | scopes to a division in a division-enabled org |
| `WITH PRICEBOOKID` | required to search Product2 within a specific price book |
| `WITH SNIPPET` | returns a **short excerpt with the matched term in context**, `target_length=n` |
| `WITH HIGHLIGHT` | marks matched terms in the returned fields for display |
| `WITH SPELL_CORRECTION` | on by default; `= false` disables the automatic correction |
| `WITH METADATA` | returns extra metadata such as field labels alongside results |

- **Matching is linguistic, not literal.** The index applies **stemming**, so `running` matches `run`; **synonym groups** defined in Setup expand a term to its configured equivalents; and lemmatization is language-specific, driven by the org's and record's language.
- **`WITH SPELL_CORRECTION` is enabled by default** and applies to English only. It silently searches for something the user did not type — desirable in a search box, and wrong in a lookup that must be exact, which is where you set it to `false`.
- **Relevance ranking is the platform's, and is not exposed.** There is no relevance score to read or sort on. `ORDER BY` inside a `RETURNING` clause overrides ranking for that object, which trades relevance for determinism.

## 2026 currency

The modifier set has been stable through the 2024–2026 window; none of these clauses is new and none was withdrawn. The change worth recording is in how search *results* are governed rather than expressed: **restriction rules apply to SOSL, search, lookups and related lists**, and **`View All Data` does not exempt a user from them** — so a `WITH NETWORK` search in an Experience Cloud site is filtered by two independent mechanisms, the network scope and any restriction rule on the object, and only one of them is visible in the query. Guest-user search in particular is a place where "the record exists but nobody can find it" is the intended configuration rather than a defect. → [07-security · 11](../07-security-and-sharing/11-restriction-rules.md), [05-experience · 09](../05-experience-cloud-lwr/09-sharing-for-external-users.md)

## Gotchas

- **`WITH SPELL_CORRECTION` is on unless you turn it off**, and it is English-only. A lookup that must match exactly should set it to `false` rather than assume literal matching.
- **`WITH SNIPPET` and `WITH HIGHLIGHT` cannot be combined** in one statement, and `SNIPPET` cannot be used with `ORDER BY` on the same `RETURNING` clause.
- **`WITH DATA CATEGORY` applies to Knowledge and a small set of category-enabled objects only** — using it elsewhere is an error, not an ignored clause.
- **`WITH NETWORK` scopes the *search*, not the sharing.** It narrows which site's content is searched; it does not grant or restrict record access, which is still sharing plus restriction rules.
- **Stemming means the match may not contain the typed string.** A user searching `ran` can get `run`, which looks like a bug in a UI that highlights literal substrings itself instead of using `WITH HIGHLIGHT`.
- **Synonym groups are org configuration, not query syntax.** A search behaving differently between sandbox and production usually means the synonym groups were never deployed.
- **There is no relevance score.** Any requirement to explain or tune ranking beyond `ORDER BY` needs a different product, not a different query.

## Recall

Q: Which SOSL modifiers change the result set and which only change presentation?
A: `DATA CATEGORY`, `NETWORK`, `DIVISION`, `PRICEBOOKID` and `SPELL_CORRECTION` change what is found. `SNIPPET`, `HIGHLIGHT` and `METADATA` change only what is returned about each match.

Q: What is the default state of `WITH SPELL_CORRECTION`, and when should it be disabled?
A: Enabled, and English-only. Disable it for exact-match lookups, where silently searching a corrected term is wrong.

Q: Why might a search find a record that does not contain the typed text?
A: Stemming and synonym groups. The index matches word roots and configured equivalents, so `ran` can match `run`.

Q: What does `WITH NETWORK` control, and what does it not?
A: It scopes which Experience Cloud site's content is searched. It does not affect record access, which is still sharing plus restriction rules.

Q: Can you sort SOSL results by relevance score?
A: No. Ranking is the platform's and is not exposed. `ORDER BY` in a `RETURNING` clause replaces ranking with a deterministic sort for that object.

## Related

- [08 · SOSL mechanics & the search index](08-sosl-mechanics-and-the-search-index.md) — the statement these clauses attach to, and the index they read
- [07-security · 11 Restriction rules](../07-security-and-sharing/11-restriction-rules.md) — the one access control that reaches search and ignores `View All Data`
- [05-experience · 09 Sharing for external users](../05-experience-cloud-lwr/09-sharing-for-external-users.md) — why `WITH NETWORK` is not an access control
- [10 · Querying across stores & the tooling surface](10-querying-across-stores-and-tooling.md) — where else a query can be issued from, including Knowledge and Data 360
