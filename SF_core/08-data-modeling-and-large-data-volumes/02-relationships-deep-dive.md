# Relationships Deep Dive

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** The **consequences** of a relationship choice — deletion, ownership, sharing, roll-ups, reparenting and depth. The definitions and the lookup-vs-master-detail comparison table are [01-admin · 03](../01-admin-and-declarative-platform/03-objects-fields-and-relationships.md); this note assumes them.

## Core idea

Picking master-detail over lookup is not a modelling preference, it is four decisions taken at once and taken permanently: **who owns the child, who can see the child, what happens when the parent dies, and whether the parent can aggregate.** None of those are recoverable later without a migration, because converting between the two types has preconditions that a populated org rarely satisfies.

The useful way to hold it is that **master-detail deletes the child's independence.** A detail record has no `OwnerId`, no org-wide default, no sharing rules and no manual shares of its own — it inherits everything from its master. That is exactly why roll-up summaries are possible on master-detail and impossible on lookup: the platform can safely aggregate children only when it knows nobody can see a child their parent hides.

## How it works

- **Cascade delete ignores sharing.** Deleting a master deletes every detail record beneath it, including ones the acting user has no access to and no visibility of. This is the single most surprising behaviour in the model, and it is by design.
- **Lookup delete behaviour is configurable, and the default is dangerous either way.** *Clear the value* leaves orphans; *Don't allow deletion* blocks the parent delete and turns routine cleanup into a support ticket. A **required** lookup cascade-deletes like master-detail — the same consequence, reached by a different setting.
- **Reparenting is off by default on master-detail.** *Allow reparenting* must be ticked at creation-time thinking, and every reparent triggers a sharing recalculation for the child and its own children → [07-security · 16](../07-security-and-sharing/16-sharing-recalculation-and-performance.md).
- **Depth: 3 custom detail levels, 2 master-detail relationships per object, 40 relationship fields per object.** The depth limit binds sooner than it sounds, because a junction object already consumes both master-detail slots.
- **Roll-up summaries live only on the master**, cap at **25 per object** (Support-raisable to a hard **40**), and recalculate *after* after-triggers in the save order → [01-admin · 07](../01-admin-and-declarative-platform/07-formula-fields-and-roll-up-summaries.md).
- **`__r` is the traversal name.** Child-to-parent is 5 levels in SOQL, parent-to-child is 1 level of subquery — a modelling constraint, not just a query one → [10-soql · 04](../10-soql-and-sosl/04-relationship-queries-in-depth.md).
- **External and indirect lookups** join on an external ID rather than a Salesforce Id, and exist for external objects → [06-integration · 20](../06-integration-and-apis/20-salesforce-connect-and-external-objects.md).

> **From my notes.** `Lead Broker Field Migration` (2023) is catalogued here but is really a deployment checklist — missing report types across sandboxes, fields present in Stage and absent in devsd and QA. One durable data-modelling lesson survives it, and it is not obvious: its first task is *"change the field label and relationship label and rel api name"*. **A relationship's API name is part of the schema, and report types are built on relationship paths** — so renaming one invalidates every report type that traverses it, and report types are metadata that has to be deployed rather than something that follows the field. That is why the page's other two items are both "things missing in the other sandbox". Rename a relationship and you have signed up for a report-type deployment.

## Gotchas

- **Every write to a detail record locks its master.** This is the mechanism behind account skew and the commonest cause of `UNABLE_TO_LOCK_ROW` in bulk loads → [12](12-record-locking-and-concurrency.md).
- **`Controlled by Parent` is not a lookup setting.** It is master-detail, and it removes the child's own OWD, sharing rules and manual sharing entirely → [07-security · 06](../07-security-and-sharing/06-org-wide-defaults-and-record-access.md).
- **Master-detail → lookup requires deleting every roll-up summary on the master first**, and the child then needs an owner populated.
- **Lookup → master-detail is impossible while any child has a blank parent.** Populate the lookup on 100% of rows first — at volume that is itself a load project.
- **The first master-detail on a junction object is the primary one**, and it silently decides look-and-feel, ownership and detail behaviour. Creating them in the wrong order is a rebuild.
- **A lookup with millions of children pointing at one parent is lookup skew** even though nothing cascades — the locking cost is real without any of master-detail's benefits → [10](10-data-skew.md).
- **Cascade delete is not blocked by validation rules or by a required-field check on the child.** Nothing on the child gets a vote.

## Recall

Q: Why can roll-up summaries exist on master-detail but not on lookup?
A: A detail record has no independent sharing, so the platform knows nobody can see a child whose parent is hidden — the aggregate is always safe to show.

Q: What happens when a user deletes a master record whose detail records they cannot see?
A: All of them are deleted anyway. Cascade delete ignores sharing entirely.

Q: Which lookup configuration behaves like master-detail on delete?
A: A **required** lookup — it cascade-deletes children when the parent is deleted.

Q: What must be true before converting master-detail to lookup, and before converting lookup to master-detail?
A: To lookup: every roll-up summary on the master deleted, and the child given an owner. To master-detail: every child row already has a parent populated.

Q: Why does writing to a detail record cause lock contention?
A: The write takes a lock on the master record, so concurrent writes to siblings serialise behind the same parent.

## Related

- [01-admin · 03 Objects, fields & relationships](../01-admin-and-declarative-platform/03-objects-fields-and-relationships.md) — the definitions this note deliberately does not repeat
- [10 · Data skew](10-data-skew.md) — what these relationships do when the distribution goes lopsided
- [12 · Record locking & concurrency](12-record-locking-and-concurrency.md) — the parent lock, in full
- [07-security · 06 Org-wide defaults & record access](../07-security-and-sharing/06-org-wide-defaults-and-record-access.md) — where `Controlled by Parent` lands in the access model
