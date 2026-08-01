# Dynamic Forms & Lightning App Builder

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 02

**Scope:** How record detail is composed on a Lightning record page, and what the page layout still owns. Action visibility is [06 · Dynamic Actions](06-dynamic-actions-and-list-views.md); record-type-driven UI is [04](04-record-types-and-picklist-architecture.md).

> **What changed.** Designing *which fields a user sees* in the page layout editor is the old answer. Since **Winter '24** Dynamic Forms covers every LWC-enabled standard object as well as custom objects, so fields, sections and their visibility rules live on the Lightning record page. But page layouts are **not retired** — they still own related lists, actions, compact layouts, Salesforce Classic, and the required/read-only field properties Dynamic Forms inherits.

## Core idea

Dynamic Forms replaces the single opaque **Record Detail** component with individual **Field** and **Field Section** components you can place anywhere on the page. Each one carries its own visibility rule, so conditional display becomes a property of the component rather than an assignment of a whole layout. That is what kills the record-type × profile layout matrix: one Lightning page with rules replaces six layouts that differed by three fields. The layout object survives in a reduced role — it is now a field-property and related-list container that the page reads from, not the place you design the form.

## How it works

- **Migration wizard.** Open the record page in Lightning App Builder, select the Record Detail component, and run the wizard. It lifts the fields, sections and save options from a page layout you choose, drops them onto the page as components, and removes the Record Detail component.
- **Placement is free.** A Field Section can go anywhere on the page — column, tab, accordion — and fields can go anywhere inside a section.
- **Visibility rules** on Field and Field Section components filter on record field values, the running user (profile, role, permission), and device form factor. An **eye icon** beside the component name means a rule is applied.
- **Coverage test that always works:** open the object's record page in App Builder. **No *Fields* tab in the component panel → Dynamic Forms is not supported for that object** (e.g. `Note`, which has a fixed layout).
- **Mobile.** Dynamic Forms on Mobile went GA in Winter '24 and is **on by default in new orgs** since Spring '24. If the org has *not* opted in, migration adds a **Record Detail - Mobile** component for the Phone form factor; if it has, that component is not added.
- **Still the page layout's job:** related lists, actions, compact layouts, Classic record pages, and the **required / read-only** field properties. Some fields arrive locked to Read-Only or Required and the properties panel will not let you change that — the layout decided it.

## 2026 currency

Object coverage completed at **Winter '24**; there is no remaining "custom objects only" caveat to work around. What is *not* true is that page layouts are deprecated — no retirement has been announced, and an org running Dynamic Forms everywhere still maintains layouts. Treat "page layout" in pre-2023 tutorials as meaning "the form design surface" and mentally redirect it.

## Gotchas

- **Never put a Record Detail component and Field Sections on the same page.** You get overlapping save/cancel bars in inline edit and visibility rules that silently stop working.
- **Enable Collapsible Sections** (User Interface setup) has no effect on a Dynamic Forms page — the Field Section's own expand/collapse wins. It still applies to Classic and to pages using Record Detail.
- Required and read-only come from the **page layout**, so a "why can't I make this editable?" bug is usually solved in the layout editor, not App Builder.
- Visibility rules hide a field from the **page**, not from the user — reports, the API, list views and search still return it. Hiding is not security; that is FLS.
- Migrating a page does **not** delete the layout, and a second page assigned to the same object can still use Record Detail. Half-migrated orgs are the normal state and the confusing one.
- A field removed from the layout after migration does not vanish from the page automatically; the component keeps pointing at it.
- Form factor is a rule input, so a rule written without one shows the component on **every** device — the commonest cause of a cluttered mobile record page.

## Recall

Q: Which objects support Dynamic Forms, and how do you check without looking it up?
A: All LWC-enabled standard objects and custom objects since Winter '24. Open the record page in App Builder — no *Fields* tab in the component panel means unsupported.

Q: After migrating to Dynamic Forms, what does the page layout still control?
A: Related lists, actions, compact layouts, Salesforce Classic pages, and the required/read-only field properties.

Q: What are the three inputs a Field or Field Section visibility rule can filter on?
A: Record field values, user attributes (profile, role, permission), and device form factor.

Q: Why should a page never contain both a Record Detail component and Field Sections?
A: Duplicate save/cancel bars during inline edit and visibility rules that stop working correctly.

Q: Does a visibility rule protect a field's data?
A: No. It hides the component on that page only — reports, list views, search and the API still expose the field. Use field-level security for protection.

## Related

- [06 · Dynamic Actions & list views](06-dynamic-actions-and-list-views.md) — the same shift applied to buttons instead of fields
- [04 · Record types & picklist architecture](04-record-types-and-picklist-architecture.md) — what record types are still for once layouts stop carrying visibility
- [03-lwc · INDEX](../03-lwc-and-slds/INDEX.md) — custom components placed on the same page, and why LWC enablement gates coverage
