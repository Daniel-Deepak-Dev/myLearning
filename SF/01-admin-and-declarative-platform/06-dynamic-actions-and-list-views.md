# Dynamic Actions & list views

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 02

**Scope:** Where record-page actions come from and how they are filtered, plus the list view surface admins configure. Field composition is [05 · Dynamic Forms](05-dynamic-forms-and-lightning-app-builder.md).

> **What changed.** "Give that record type its own layout so the button only shows there" is the old answer. Action visibility is now set by **Dynamic Actions rules in Lightning App Builder** — the same filter engine Dynamic Forms uses — so one page conditionally shows different buttons instead of many layouts each hard-coding a button set.

## Core idea

Dynamic Actions moves the action bar out of the page layout's *Salesforce Mobile and Lightning Experience Actions* section and into the **Highlights Panel** on the Lightning record page, where each action carries its own filters. The consequence is the same as with Dynamic Forms: what used to be an assignment problem (which layout does this profile and record type get?) becomes a rule problem (under what conditions does this button appear?). List views are the other half of the daily admin surface — the same records without a record page — and they have their own visibility, filter and default-view model that has nothing to do with layouts.

## How it works

- **Where:** App Builder → Highlights Panel (or Dynamic Highlights Panel) → *Add Action*. Actions are ordered here, not in the layout editor.
- **Filters** per action: record field values, the running user, and **device type** — so a mobile-only or desktop-only button is a filter, not a separate layout. An **eye icon** marks a filtered action.
- **Standard objects need an org switch first:** Setup → *Salesforce Mobile App* → **Enable Dynamic Actions on Mobile**. It reads as a mobile setting but it is the gate for standard-object dynamic actions generally — the commonest reason the option is missing.
- **Mobile consolidation:** if a desktop page has several Highlights Panels each carrying dynamic actions, mobile merges them into **one action bar** for that page.
- **Fallback:** a page without dynamic actions falls back to the page layout's action list. Both models coexist per page, which is why two record pages on one object can behave differently.

| Surface | Configured in | Visibility driven by |
|---|---|---|
| Dynamic Actions | Lightning App Builder (Highlights Panel) | per-action filters: field, user, device |
| Layout actions (legacy) | Page layout editor | which layout the profile × record type gets |
| List view buttons | Search layouts / *List View* button layout | object permissions only |

- **List views:** filter logic per view, sort by **up to 5 columns** in Lightning (Classic allows one), inline edit, mass actions on selected rows, charts, and a **Kanban** toggle with drag-to-update and inline edit of key fields.
- **List view search** scans **all searchable fields on the object, not only the displayed columns** — results that look impossible are usually a match on a hidden field.
- **Pinning** a list view makes it that object's default. It is per user, so "everyone sees the wrong default list" is a user-level fix, not a config one.
- **Sharing:** a list view is visible to all users, to a set of groups/roles, or only to its creator. Sharing a view does not share its records.

## 2026 currency

Dynamic Actions covers standard and custom objects on desktop and mobile; the old "custom objects only" limitation is gone. Layout-driven actions are still supported and still the fallback, so this is a shift in where you *should* configure, not a retirement. Nothing here has changed in Summer '26 itself.

## Gotchas

- Dynamic Actions is configured on the **Lightning page**, so an org with several record pages per object must repeat the rules on each — divergence between them is invisible until a user complains.
- The **Enable Dynamic Actions on Mobile** switch is org-wide and one-way in practice; enable it deliberately, because it changes what mobile users see on standard objects.
- Filters hide buttons, they do not grant permission. A user who lacks *Edit* still cannot act after you show them the button — and one who has it can still reach the action through the API or a list view.
- Removing an action from the layout does not remove it from a page already using dynamic actions, and vice versa.
- **Predefined field values** on a quick action are set on the action, not the filter, so two conditional buttons that differ only in defaults are two actions.
- List view sort is capped at 5 columns and the cap is silent — the sixth click replaces rather than appends.
- A user's **pinned** list view overrides whatever default you set; support tickets about "the wrong list" are usually this.

## Recall

Q: Where is action visibility configured now, and what replaced the layout-per-record-type pattern?
A: In Lightning App Builder on the Highlights Panel, using per-action filters on field values, user and device type.

Q: A standard object shows no option to add dynamic actions. What is missing?
A: The org switch Setup → Salesforce Mobile App → *Enable Dynamic Actions on Mobile*, which gates standard-object dynamic actions.

Q: What happens to dynamic actions from multiple Highlights Panels when the page is viewed on a phone?
A: They are consolidated into a single action bar for that record page.

Q: Why can a list view search return a record whose visible columns do not contain the search term?
A: List view search looks at every searchable field on the object, not just displayed columns.

Q: How many columns can a Lightning list view be sorted by, and what does pinning a view do?
A: Up to 5 columns; pinning makes it that user's default list view for the object.

## Related

- [05 · Dynamic Forms & Lightning App Builder](05-dynamic-forms-and-lightning-app-builder.md) — the field half of the same visibility model
- [11 · Queues, assignment & escalation rules](11-queues-assignment-and-escalation-rules.md) — queue list views are where routed records actually get worked
- [07-security · INDEX](../07-security-and-sharing/INDEX.md) — why hiding a button is not access control
