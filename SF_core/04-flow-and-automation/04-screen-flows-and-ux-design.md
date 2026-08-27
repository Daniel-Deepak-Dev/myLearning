# Screen Flows & UX Design

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** The designer's side of a user-facing flow — screen composition, validation, navigation. Same-screen recalculation is [05](05-reactive-screen-flows.md); the *component-authoring* contract for a custom LWC is [03-lwc · 11](../03-lwc-and-slds/11-lwc-in-flow-screens-and-quick-actions.md).

## Core idea

A screen flow is the only flow type a user sees, and the design problem is not which components exist but **where a screen boundary belongs**. Every boundary is a round trip: state is committed to flow variables, the runtime re-renders, and the user pays a wait. The old builder forced boundaries you did not want, because nothing on a screen could react to anything else on it — a dependent picklist meant Next, then Back. Reactivity removed that constraint, and the practical consequence is that modern screen flows have *fewer, richer* screens than the ones in older tutorials. The second design idea is that a screen is a form, so it owes the same things any form owes: validation before advance, a sensible tab order, and a visible way to fail.

## How it works

| Component group | Members |
|---|---|
| **Input** | Text, Long Text, Number, Currency, Date/Time, Checkbox, Picklist, Radio Buttons, **Radio Button Group** 🆕, Toggle, Slider, Lookup, Choice Lookup, Name, Address, Email, Phone, URL |
| **Display** | Display Text, Image, Section, Column, **Data Table**, **Repeater**, Action Button |
| **Structural** | conditional visibility per component, footer control, help text |

- **`Section` + `Column` are the only native layout.** No tabs, no accordions, no wizard progress bar without a custom component or an AppExchange package.
- **Conditional visibility is client-side and free** — it costs no round trip and is the first tool to reach for before adding a screen.
- **Validation is per input component**, a formula returning a Boolean plus an error message. It runs on Next, not as the user types.
- **`Repeater`** (Spring '24 → **GA Summer '24**, screen flows only) collects N of something on one screen and supports conditional visibility, validation and help text on its children.
- **Footer control** — hide Previous, Pause or Finish per screen. Hiding Previous is how you stop a user rewinding past a commit.

## 2026 currency

Summer '26 filled in the two things screen flows kept needing a custom LWC for. **A native `Show Toast Message` action** now fires success, warning, error and information toasts straight from a flow — worth pairing with the finding in [03-lwc · 18](../03-lwc-and-slds/18-error-handling-and-user-feedback.md), that `ShowToastEvent` fails *silently* in LWR sites; a flow no longer needs a toast component at all in Lightning Experience. **An `Open a Page` action** redirects to a new record or an external URL at the end of a flow, replacing the navigation-only LWC. Alongside those: the **Radio Button Group** component, **Data Table lookup columns that render record names as clickable links** instead of raw Ids, static-resource images browsable from inside the builder, and **styling overrides extended to eleven more components** including Action Button, Address, Choice Lookup, Dependent Picklists, Slider and Toggle. One deployment fix worth knowing: **Send Email action v3.0.1+ stores an email template by name rather than Id**, which is what used to break the action on the way from sandbox to production.

## Gotchas

- **Every screen boundary is a round trip.** Conditional visibility and reactivity are cheaper than another screen; reach for them first.
- **Validation fires on Next, not on input.** A user can fill an invalid value and only learn at the bottom of a long screen.
- **`Repeater` is screen-flow only.** It has no meaning in an autolaunched or triggered flow.
- **Hiding the Previous button is the only way to protect a committed step** — flow does not roll back on Back, it simply re-renders an earlier screen with old values.
- **A `Display Text` component renders rich text, which makes it an injection surface** when it interpolates user-supplied variables.
- **A Data Table returns a *collection*, even when single-select** — assigning it to a record variable fails at run time, not at save.
- **Screen flows honour the running user's FLS.** A field the user cannot edit renders read-only with no warning to the builder. → [07-security](../07-security-and-sharing/INDEX.md)
- **Older tutorials add a screen where reactivity now suffices.** If a design has a screen whose only job is to make the next one see a value, it is out of date. → [05](05-reactive-screen-flows.md)

## Recall

Q: What is the real cost of adding a screen to a flow?
A: A round trip — state is committed to variables and the runtime re-renders. Conditional visibility and reactivity avoid it.

Q: When does screen input validation actually run?
A: On Next, not as the user types.

Q: Which component collects a variable number of entries on one screen, and where can it be used?
A: `Repeater`, GA Summer '24 — screen flows only.

Q: What replaced the toast-notification LWC in Summer '26?
A: A native `Show Toast Message` action in Flow Builder, covering success, warning, error and information.

Q: Why did a Send Email action break when deployed from sandbox to production, and what fixed it?
A: It stored the email template by Id, which differs per org. Action version 3.0.1+ stores the template by name.

## Related

- [05 · Reactive screen flows](05-reactive-screen-flows.md) — how a screen recalculates without a Next click
- [03-lwc · 11 LWC in Flow screens](../03-lwc-and-slds/11-lwc-in-flow-screens-and-quick-actions.md) — the authoring contract when no stock component fits
- [10 · Fault paths & custom errors](10-fault-paths-and-custom-errors.md) — what the user sees when a screen flow fails mid-way
