# Multi-Currency, Multi-Language & Locale

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** What internationalisation does to the *data model* — extra columns, conversion at read time, and one switch you cannot take back. Where the org physically sits is [23](23-hyperforce-residency-and-data-locality.md).

## Core idea

Multi-currency is usually discussed as a display feature. It is a **schema change**. Enabling it adds a `CurrencyIsoCode` to every object with a currency field, makes every amount two numbers — the entered value and its converted value — and puts a conversion step between your data and every report, roll-up and comparison that crosses records.

And it is **one-way**. Multi-currency cannot be turned off once enabled, which puts it in the same category as Person Accounts: a decision to take deliberately, in a sandbox first, with the reporting consequences understood → [05](05-person-accounts-and-one-way-modeling-decisions.md).

Language and locale are the opposite shape — reversible, per user, and touching presentation rather than storage — which is exactly why they get confused with each other.

## How it works

- **Corporate currency is the pivot.** Every record stores its own `CurrencyIsoCode` and its amount; anything that aggregates across records converts to the corporate currency first.
- **Static rates convert with today's rate** — including historical records. Last year's closed deal silently restates when the rate is updated.
- **Advanced Currency Management (ACM)** fixes that with `DatedConversionRate`: a rate mapped to a date range, so a record converts at the rate that applied when it happened. Enabling ACM turns your existing rates into the first dated set.
- **Dated rates cover Opportunities and their related records — and nothing else.** Notably, forecasting does not use them, which produces numbers that disagree with the reports beside them.
- **Roll-ups convert to the parent's currency**, so a master-detail across currencies is doing arithmetic on converted values, not entered ones.
- **SOQL needs `convertCurrency()`** to compare or aggregate across currencies; filters can be written against a specific currency (`Amount > USD100`).
- **Language, locale and time zone are three separate user settings.** Language translates the UI; **locale formats** dates, numbers and name order; time zone shifts datetimes. Only the first involves translation.
- **Translation Workbench translates metadata labels, never data.** A translated picklist still stores its API name — which is what makes translated picklists safe to filter and report on.

## Gotchas

- **Multi-currency cannot be disabled.** Prove the reporting model in a sandbox before enabling it in production.
- **`DatedConversionRate.StartDate` is settable on insert or upsert only** — never on update. Loading dated rates is an upsert job, and getting it wrong means deleting and reloading.
- **Forecast figures ignore dated rates**, so forecasts and opportunity reports can legitimately disagree. Know which number you are being asked about.
- **Currency formula fields lose their meaning across currencies** unless every operand is converted the same way.
- **Locale changes sort order.** A list users swore was alphabetical is alphabetical *in their collation*, and export/import round-trips can reorder it.
- **Date and number parsing on import follows the running user's locale** — the classic cause of a load that turns 03/04 into the wrong month → [25](25-data-migration-and-cutover.md).
- **Translated picklist labels do not change the stored value.** Automation and integrations keyed on the label were always broken; translation is where it becomes visible.
- **State and Country picklists are a separate one-way-ish conversion** with its own data cleanup — do not bundle it into the same release.

## Recall

Q: Can multi-currency be switched off after it is enabled?
A: No. It is a permanent schema change — every currency-bearing object gains `CurrencyIsoCode` and every amount gains a conversion step.

Q: What does Advanced Currency Management add, and where does it apply?
A: Dated exchange rates via `DatedConversionRate`, so records convert at the rate that applied at the time — and it applies to Opportunities and related records only.

Q: Which figures ignore dated exchange rates?
A: Forecasts — which is why they can disagree with opportunity reports in the same org.

Q: What is the difference between the language and locale user settings?
A: Language translates the UI; locale formats dates, numbers and name order. Locale does no translation.

Q: Does translating a picklist change what is stored?
A: No — the API name is stored, so filters, automation and reports are unaffected by translation.

## Related

- [05 · Person Accounts & one-way modeling decisions](05-person-accounts-and-one-way-modeling-decisions.md) — the other switch you cannot un-flip
- [23 · Hyperforce, residency & data locality](23-hyperforce-residency-and-data-locality.md) — where the data physically lives, which is a different question
- [25 · Data migration & cutover](25-data-migration-and-cutover.md) — locale-driven parsing errors in a load
- [01 · Data model design principles](01-data-model-design-principles.md) — why schema-level switches deserve design review
