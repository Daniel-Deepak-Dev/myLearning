# Scoping Rules

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** Setting the default set of records a user works with, without changing what they may access. The mechanism that genuinely removes access is [11](11-restriction-rules.md).

## Core idea

Scoping rules are **not** a security feature and confusing them with restriction rules is the single commonest mistake in this pair. A scoping rule sets the *default filter* — what a user sees when they open a list view, run a report or issue a query without saying otherwise — and the user can widen it straight back out. That makes it a focus tool: a sales rep in a 4 million-record Account object opens their list and sees their region, not everything, because seeing everything by default is useless rather than because seeing everything is forbidden. Reach for it when the complaint is *"there's too much here to work with"*. Reach for [11](11-restriction-rules.md) when the complaint is *"they shouldn't be seeing that"*.

## How it works

- **Same two-criteria shape as a restriction rule**: which users the rule applies to, and which records make up their default scope.
- **It applies to list views, reports and SOQL.** It does **not** apply to search, SOSL, lookups or related lists — which is exactly the gap that makes it useless as a control.
- **The user can escape it.** Changing the list view filter, or querying outside the scope, returns the wider set, because the access was never removed.
- **Available on custom objects and a set of standard ones** — Account, Case, Contact, Event, Lead, Opportunity and Task among them. Note this is close to the *inverse* of the restriction-rule list.
- **One scoping rule per object per user**, as with restriction rules. Overlapping user criteria are a design error.
- **Metadata-managed** (`ScopingRule`) and deployable, so it belongs in the pipeline rather than in an admin's head.
- **The two combine.** A scoping rule can set the default view *inside* the set a restriction rule has already narrowed; the scoping rule never widens past the restriction.

## 2026 currency

GA since **Summer '22** and unchanged in Summer '26. The reason it still needs a note is that the two rule types arrived within three releases of each other, are configured in adjacent places with near-identical UIs, and are constantly described interchangeably in secondary material. The distinction to keep: **scoping changes the default, restriction changes the answer.** If a requirement contains the word *shouldn't*, a scoping rule does not meet it.

## Gotchas

- **A scoping rule is not access control.** The user can widen the filter and get everything back. Never satisfy a compliance requirement with one.
- **It does not reach search or lookups.** A record outside the scope is still findable in global search and still selectable in a lookup field.
- **Reports respect it, which surprises report builders** — a report returning fewer rows than expected may be scoped, not filtered.
- **SOQL from Apex respects it too**, so an integration's row counts change when someone adds a scoping rule for its running user. → [14](14-code-execution-context-and-security.md)
- **The supported-object lists differ from restriction rules'**, so the object you want is quite likely supported by one and not the other.
- **Nothing in the UI says "you are scoped."** As with restriction rules, the shrunken result set has no explanation attached.
- **Scoping cannot widen past a restriction rule.** If both apply, restriction wins and scoping operates inside what is left.

## Recall

Q: What does a scoping rule change?
A: The default set of records a user sees in list views, reports and SOQL. It changes nothing about what they are allowed to access.

Q: Can a user get around a scoping rule?
A: Yes — by widening the list view filter or querying outside the scope. That is by design.

Q: Which surfaces does a scoping rule *not* reach?
A: Search, SOSL, lookups and related lists. Restriction rules reach all of those.

Q: When both a scoping rule and a restriction rule apply to the same object and user, what happens?
A: The restriction rule decides what is accessible; the scoping rule sets the default view inside that narrowed set.

Q: What word in a requirement rules out a scoping rule?
A: *Shouldn't* — anything phrased as prohibition needs a restriction rule or a change to the grants.

## Related

- [11 · Restriction rules](11-restriction-rules.md) — the sibling that actually removes access
- [06 · Org-wide defaults & record access](06-org-wide-defaults-and-record-access.md) — the grants both rules operate on top of
- [01-admin · 06 Dynamic actions & list views](../01-admin-and-declarative-platform/06-dynamic-actions-and-list-views.md) — the list view surface a scoping rule defaults
