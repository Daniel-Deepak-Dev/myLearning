# Custom Labels & Translation Workbench

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 01

**Scope:** Externalising user-facing strings into custom labels, referencing them from every runtime, and translating them. Stops at Experience Cloud site localisation — that is [05-experience-cloud](../05-experience-cloud-lwr/INDEX.md).

## Core idea

A custom label is a named string stored as metadata and referenced instead of hardcoded text. Its value is that one label serves every runtime — Apex, LWC, Flow, validation rules, formula fields — so a wording change is one edit rather than a search across the codebase. Its second value is translation: labels are the unit the Translation Workbench operates on, so externalising a string is the prerequisite for ever supporting a second language. Because labels are metadata rather than data, they deploy with your source and are versioned alongside it.

## How it works

- **Allocations** — up to **5,000** custom labels per org, each up to **1,000 characters**. Labels from managed packages do not count against your total.
- **Reference syntax differs per runtime:**

```
Formula / validation rule   $Label.My_Label
Apex                        System.Label.My_Label
LWC                         import MyLabel from '@salesforce/label/c.My_Label';
Flow                        $Label global variable in the resource picker
Visualforce                 {!$Label.My_Label}
```

- **The LWC import is resolved at compile time.** The label name must be a literal in the import statement — you cannot build it dynamically, which rules out `$Label[someVariable]`-style lookups.
- **Translation Workbench** must be explicitly enabled in Setup. You then add languages, assign translators per language, and translate labels along with other translatable metadata (field labels, picklist values, record types, Flow screen text).
- **Managed package overrides** — Translation Workbench is also how you override labels and translations shipped inside a managed package without modifying it.
- **Fallback is to the master language**, per label. A partially translated org shows a mixture rather than failing.

## Gotchas

- A label has a **Name** (the API name you reference) and a separate **Short Description** and **Value**. Renaming the Name breaks every reference; changing the Value breaks nothing.
- **Deleting a label that is still referenced fails**, which is good — but the error names the label, not the referencing component, so finding the reference is on you.
- Labels do **not** support merge fields or parameters. Dynamic text means storing `{0}` placeholders and substituting with `String.format()` in Apex or a template in LWC.
- The 1,000-character ceiling makes labels wrong for long-form content; that belongs in Knowledge, CMS, or a rich text field.
- Translation Workbench must be enabled *before* translations can exist — turning it on later does not retroactively surface anything.
- Concatenating translated fragments produces broken grammar in most languages. Translate whole sentences, not pieces.
- Labels are metadata, so a wording fix in production is a **deployment**, not an admin edit — plan for it in the release, not the same afternoon.
- Flow screen text and label translations are managed in different places; translating the label does not translate text typed directly into a Flow screen.

## Recall

Q: How many custom labels can an org hold, and how long can each be?
A: 5,000 labels of up to 1,000 characters each; managed-package labels do not count toward the total.

Q: How is a custom label referenced from Apex, from a formula, and from LWC?
A: `System.Label.My_Label`, `$Label.My_Label`, and `import MyLabel from '@salesforce/label/c.My_Label'`.

Q: Why can you not choose an LWC label dynamically at runtime?
A: The `@salesforce/label` import is resolved at compile time, so the label name must be a literal.

Q: How do you produce a label containing a dynamic value such as a record name?
A: Store a placeholder like `{0}` in the label and substitute at runtime — `String.format()` in Apex. Labels have no native merge-field support.

Q: What happens when a label has no translation in the user's language?
A: It falls back to the master language for that label, so a partly translated org shows a mixture rather than erroring.

## Related

- [09 · Custom Metadata vs Custom Settings](09-custom-metadata-vs-custom-settings.md) — the other place configuration lives as metadata
- [03-lwc · INDEX](../03-lwc-and-slds/INDEX.md) — the `@salesforce/label` module and component-side i18n
- [05-experience-cloud · INDEX](../05-experience-cloud-lwr/INDEX.md) — site-level localisation built on top of labels
