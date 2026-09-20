---
vault: SF_Experience_Cloud
format: light
level: deep
status: open
gaps: 4
org_checks: 2
labs: 4
created: 2026-09-20
updated: 2026-09-20
currency: "Summer '26 (API 67.0)"
---
# Multilingual Sites & Site Translation

**One line:** One Experience Cloud site served in up to 40 languages, each translation stored against the same page and the same content item — not a second site.

**Reach for it when:** a site has to serve a second language and you must decide what gets translated, where, and who owns each part.

> **From my notes.** Site language settings, language selector, per-language URLs, CMS content variants by locale, Translation Workbench for site content. — **Corrected:** no reachable doc says a language gets its own URL. Every documented switch is a runtime selection. That is gap 1, not a fact.

## Key points

- **Languages are added per site**, in **Experience Builder → Settings → Languages → Edit Languages**, capped at **40 including the default**. That one list feeds both the authoring picker in Builder and the **Language Selector** component you place for visitors.
- **Three translation surfaces, three owners, three deploy routes.** The fact the whole topic hangs on:

| What | Where you translate it | How it travels |
|---|---|---|
| Builder strings, rich text | component property editor, per language | with the site bundle 🚩 |
| Labels, field & picklist labels, Flow screens | **Translation Workbench** | `Translations` component 🚩 |
| CMS content | the workspace, as a **variant** | 🚩 may not deploy at all |

- **Bulk route:** export site content → translate → import. Experience Builder exports **`.xlf` (XLIFF)**; Translation Workbench also offers **STF**.
- **CMS lifecycle:** add languages to the workspace → mark an item **Ready for Translation** → export zipped XLIFF → translator fills `target` → import → **publish the variant**. The variant *is* the translation, not a second content item.
- **Resolution:** an LWR site auto-detects the visitor's localized language, and for a logged-in user the **profile language beats the browser**. Missing strings fall back **per string** to the default language → [SF_core · 10](../SF_core/01-admin-and-declarative-platform/10-custom-labels-and-translation-workbench.md).

## Gotchas

- **Enabling a language translates nothing.** It creates an empty column and a selector entry; every page still renders in the default language until someone types or imports a translation.
- **Do not edit default-language content while it is out for translation.** The import overwrites the default too, so the edit is silently lost — this is documented behaviour, not folklore.
- **A literal string in a custom LWC is permanently untranslatable.** Custom labels are the only translatable surface, which makes this a day-one decision, not a retrofit → [SF_core · 17](../SF_core/03-lwc-and-slds/17-accessibility-and-internationalization.md).
- 🚩 **Imports are all-or-none.** One bad row rejects the whole file; duplicate keys and over-length labels are the usual causes.
- **Aura and LWR diverge here.** LWR reached language parity in stages and has its own add-language and default-language settings, so an Aura how-to does not transfer → [01](01-template-choice-and-site-landscape.md).

## Gaps to close

- [ ] Does a language get its own URL on an LWR site, or is language a runtime selection against one URL? If a parameter carries it, what is its exact name?
- [ ] Does the auto-generated LWR sitemap emit per-language URLs, and does anything emit `hreflang`? → [16](16-site-performance-caching-and-seo.md)
- [ ] Is a public LWR page cached once at the CDN edge or once per language? A build-and-serve model must do one or the other → [16](16-site-performance-caching-and-seo.md)
- [ ] Which metadata component carries Experience Builder's *inline* site translations — `Translations`, the bundle itself, or neither? → [18](18-experience-cloud-devops.md)

## Confirm in org

- 🚩 Experience Builder → Settings → Languages on a Build Your Own (LWR) site: is the list the org's enabled languages, or every Salesforce language regardless?
- 🚩 Retrieve a translated site and read the bundle — does an inline Builder translation appear in source at all, or only in the org?

## Hands-on

- [ ] **EC-I18N-01** · 25 min · Add a second language, place the Language Selector, translate one component inline, publish, then switch language. **Proves:** enabling a language translates nothing — fallback is per string, so the page renders a mixture.
- [ ] **EC-I18N-02** · 20 min · Export site content, edit the default-language text in Builder while the file is "out", then import it. **Proves:** the import overwrites the default you changed — the documented data-loss path.
- [ ] **EC-I18N-03** · 20 min · Hardcode a string in a custom LWC, put it on the site, then try every route to translate it. **Proves:** only custom labels are translatable; a literal is monolingual forever.
- [ ] **EC-I18N-04** · 30 min · Retrieve the site plus `Translations` into a second org and deploy. **Proves:** which half of a translation travels and which is re-keyed by hand.

## Related

- [14 · Enhanced CMS & content delivery](14-enhanced-cms-and-content-delivery.md) — the workspace, channel and variant model the CMS half of this note runs on
- [16 · Site performance, caching & SEO](16-site-performance-caching-and-seo.md) — the build-and-serve model that gaps 2 and 3 have to resolve against
- [18 · Experience Cloud DevOps](18-experience-cloud-devops.md) — the bundle types a translation travels beside, and gap 4
- [22 · Site accessibility & conformance](22-site-accessibility-and-conformance.md) — holds the org check this note would otherwise duplicate: whether a published page's `<html lang>` changes per language, which is WCAG 3.1.1 and not cosmetic
- [SF_core · 01-admin · 10 Custom labels & Translation Workbench](../SF_core/01-admin-and-declarative-platform/10-custom-labels-and-translation-workbench.md) — the org-level translation engine this note sits on top of, and where per-label fallback is established
- [SF_core · 08-data · 22 Multi-currency, multi-language & locale](../SF_core/08-data-modeling-and-large-data-volumes/22-multi-currency-multi-language-and-locale.md) — language vs locale vs time zone, and why a translated picklist is still safe to filter on

## Sources

- [Create a Multilingual LWR Site](https://developer.salesforce.com/docs/atlas.en-us.exp_cloud_lwr.meta/exp_cloud_lwr/multilingual_lwr.htm) — Salesforce Developers · via search 2026-09-20
- [Add a Language to Your LWR Site](https://developer.salesforce.com/docs/atlas.en-us.exp_cloud_lwr.meta/exp_cloud_lwr/multilingual_lwr_add_language.htm) — Salesforce Developers · via search 2026-09-20
- [Export Content from Your LWR Site for Translation](https://developer.salesforce.com/docs/atlas.en-us.exp_cloud_lwr.meta/exp_cloud_lwr/multilingual_lwr_export_content.htm) — Salesforce Developers · via search 2026-09-20
- [Import Translated Content to Your LWR Site](https://developer.salesforce.com/docs/atlas.en-us.exp_cloud_lwr.meta/exp_cloud_lwr/multilingual_lwr_import_content.htm) — Salesforce Developers · via search 2026-09-20
- [Multilingual Sites](https://help.salesforce.com/s/articleView?id=experience.community_builder_multilingual_overview.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-20
- [Set Language Options](https://help.salesforce.com/s/articleView?id=experience.community_builder_multilingual_settings.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-20
- [Language Selector](https://help.salesforce.com/s/articleView?id=experience.rss_language_picker.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-20
- [Work with Enhanced CMS Content in the Translation Lifecycle](https://help.salesforce.com/s/articleView?id=sf.cms_translation_lifecycle.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-20
- [Add Languages to a CMS Workspace](https://help.salesforce.com/s/articleView?id=sf.cms_translation_add_languages.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-20
- [Localized Language Is Automatically Detected for LWR Sites](https://help.salesforce.com/s/articleView?id=release-notes.rn_experiences_lwr_localized_language_automatic.htm&language=en_US&type=5) — Salesforce release notes · via search 2026-09-20
- [Translate Your LWR Site into Even More Languages](https://help.salesforce.com/s/articleView?id=release-notes.rn_experiences_lwr_translate_forty.htm&language=en_US&type=5) — Salesforce release notes · via search 2026-09-20
- [Salesforce Language Support](https://help.salesforce.com/s/articleView?id=sf.faq_getstart_language_support.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-20
- [Lost in Translation? Make Your Experience Cloud Site Multilingual](https://www.salesforceben.com/lost-in-translation-make-your-experience-cloud-site-multilingual/) — third party 🚩 · via search 2026-09-20

## History

- 2026-09-20 · created from your multilingual-sites feed; per-language URL behaviour could not be sourced from any reachable first-party page and is carried as the first gap
