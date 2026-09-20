---
vault: SF_Experience_Cloud
format: dense
level: working
status: open
gaps: 3
org_checks: 3
labs: 4
created: 2026-09-20
updated: 2026-09-20
currency: "Summer '26 (API 67.0)"
tags: [currency-new, currency-warning]
---
# Site Accessibility & Conformance

**Scope:** Who owes WCAG conformance for a published site, which version of the standard actually binds, and what a Salesforce conformance report does and does not cover. Component-level accessibility — ARIA, focus, labels, locale — is [03-lwc · 17](../SF_core/03-lwc-and-slds/17-accessibility-and-internationalization.md); this note owns the site-level obligation.

> **What changed.** Two claims travel together and both are wrong: *"Salesforce conforms to WCAG 2.2 AA, so our site does"* and *"the ACR is our compliance evidence."* **An Accessibility Conformance Report describes Salesforce's components, not your configured site** — and Salesforce's 2.2 target sits **above** the version that binds in the EU, where the cited harmonised standard is still **EN 301 549 v3.2.1 = WCAG 2.1 AA**.

## Core idea

Accessibility on an Experience Cloud site is **two things that are easy to merge and must not be**. The platform contributes components with a published conformance record. You contribute a template, a branding set, a page layout, content, custom components and third-party scripts — and a regulator looks at the **rendered page**, which is the sum of both. Nothing in a Salesforce ACR transfers to your site; it is evidence about one input.

The legal half has the same shape. The **European Accessibility Act** obliges the *service provider* — your client — and the duty attaches to the **service**, not to the software vendor underneath it. So the useful question on a scoping call is never "is Salesforce accessible?" It is: *which service is being provided, to whom, in which jurisdiction, and who signs the accessibility statement?*

## How it works

| Regime | Binds | Standard | Live from |
|---|---|---|---|
| **EAA** — Dir. (EU) 2019/882 | private-sector services to consumers | EN 301 549 v3.2.1 → **WCAG 2.1 AA** | **28 Jun 2025**; service contracts signed before it may run to **28 Jun 2030** |
| **Web Accessibility Directive** — (EU) 2016/2102 | EU public sector bodies | same | in force; adds a statement **and** a feedback mechanism |
| **ADA Title II** — DOJ final rule, 24 Apr 2024 | US state & local government | **WCAG 2.1 AA** | **26 Apr 2027** (pop. ≥50k) / **26 Apr 2028** (smaller, special districts) 🚩 |
| **Section 508** | US federal procurement | Revised 508 / EN 301 549 | in force |

- **EAA scope is service-by-service, not "all websites"** — e-commerce (Art. 3(30)), consumer banking, e-books, passenger transport, electronic communications, audiovisual media access. A partner portal that sells nothing to consumers can fall outside it and still be caught by a public-sector or contractual duty.
- **The accessibility statement is a deliverable, not a test result.** Art. 13(2) and Annex V require the provider to say in the general terms — **in accessible written *and* oral form** — how the service meets the requirements, and to keep it current for the life of the service. On a site that is a page you build, publish and re-check every release.
- **Two ACRs, split by runtime, and the split follows the template decision** → [01](01-template-choice-and-site-landscape.md). *Experience Cloud – LWR* covers **Build Your Own (LWR)** and **Microsite (LWR)**; *Experience Cloud – Aura* covers **Customer Service**, **Customer Account Portal** and **Partner Central**. Both **Spring '25**, VPAT 2.4 Rev INT. Base components carry a separate, newer report (**Spring '26**).
- **The LWR report is not a clean sheet** — it rates *Partially Supports* for **usage with limited vision**, and Salesforce's wording throughout is *"to the extent possible"*.
- **LWR ships F6 region navigation** and screen-reader handling built for a single-page app. **The regions come from slots in the theme layout**, which is where they are silently lost → [04](04-experience-builder-layouts-and-theme-layouts.md).
- **Contrast is a branding-set value, not a platform property.** `--dxp` hooks and SLDS 2 dark mode put the ratio in the hands of whoever set the palette → [05](05-branding-sets-design-tokens-and-slds-2.md).

## 2026 currency

**EN 301 549 v4.1.1 was published by ETSI on 2 September 2026** — it moves to **WCAG 2.2** and adds an annex mapping the standard onto the EAA. It is **not yet cited in the Official Journal**, and citation is what creates the presumption of conformity under Art. 15, so **v3.2.1 and WCAG 2.1 AA are still what bind**. Read the other direction too: Salesforce's own WCAG 2.2 work is still landing. **Two accessibility Release Updates for WCAG 2.2 *Resize and Reflow* have now been postponed twice** — date pickers, popovers, bottom utility bars and record headers (first available Winter '26), and page headers and modal windows (first available Summer '25) — both were scheduled for Summer '26 and both are now **Winter '27** → [../RELEASE-RADAR/](../RELEASE-RADAR/README.md).

## Gotchas

- **Accessibility Mode is Salesforce Classic only.** It does nothing for Lightning Experience and nothing for a site's public pages. No portal was ever made conformant by ticking it.
- **An accessible name hardcoded in a custom LWC is frozen in one language.** `aria-label`, `alt` and error text have to come from Custom Labels or nothing can translate them — on a multilingual site that is a conformance failure no Salesforce release will ever fix for you → [21](21-multilingual-sites-and-translation.md).
- **A Lighthouse or axe pass is not conformance.** Automated tooling evaluates roughly **20–30% of WCAG success criteria** 🚩; keyboard and screen-reader testing is the rest → [16](16-site-performance-caching-and-seo.md).
- **"Fines up to €100,000 or 4% of turnover" is folklore.** The EAA leaves penalties to Member States (Art. 30) and they differ by country. Quote the country, not the meme.
- **The ACR carries an explicit disclaimer** — it is not part of any contract unless Salesforce acknowledges that in writing. It is evidence to reason from, not a warranty to forward to procurement.
- **The microenterprise exemption is services-only** (<10 staff **and** ≤€2m) and belongs to whoever provides the service. Your consultancy being small does not exempt your client.
- **Disproportionate burden is a documented assessment, not an opinion** — Art. 14, criteria in Annex VI, re-run at least every five years.
- **The public, unauthenticated pages are the regulated surface** — the same pages [11](11-public-site-exposure-audit.md) audits for data exposure. One surface, two audits, and only one of them is usually scheduled.

## Recall

Q: Does a Salesforce Accessibility Conformance Report make your Experience Cloud site conformant?
A: No. It describes Salesforce's components. A regulator looks at the rendered page — template, branding set, content, custom components — and the obligation sits with the service provider.

Q: Which WCAG version binds under the European Accessibility Act?
A: WCAG 2.1 AA, via EN 301 549 v3.2.1 — the version cited in the Official Journal. v4.1.1 (WCAG 2.2) was published 2 September 2026 but is not yet cited, so it confers no presumption of conformity.

Q: Which ACR covers your site, and what decides it?
A: The runtime, fixed by the template. *Experience Cloud – LWR* covers Build Your Own (LWR) and Microsite (LWR); *Experience Cloud – Aura* covers Customer Service, Customer Account Portal and Partner Central.

Q: What does the EAA require beyond an accessible site?
A: A statement — Art. 13(2) and Annex V — in the general terms, in accessible written and oral form, explaining how the service meets the requirements and kept current for the life of the service.

Q: Where do an LWR site's F6 navigation regions come from?
A: Slots in the theme layout. A custom theme layout that drops them loses the regions with no error.

## Gaps to close

- [ ] Which WCAG success criteria the *Experience Cloud – LWR* ACR marks **Partially Supports**, and what its remarks say.
- [ ] Does Enhanced Chat / embedded messaging carry its own ACR, and does it cover the agent surface on a public site? → [19](19-embedded-messaging-and-agents-in-sites.md)
- [ ] Is a Mobile Publisher app covered by any ACR? The EAA covers mobile apps, not only websites → [17](17-mobile-publisher-and-pwa-delivery.md)

## Confirm in org

- 🚩 Does a published LWR page emit `<html lang>` matching the site language, and does it change per language on a multilingual site? View source on a guest page (WCAG 3.1.1).
- 🚩 Does Experience Builder surface any contrast or accessibility warning in the Theme panel? Nothing in the documentation says it does.
- 🚩 Do F6 regions survive a custom theme layout, or does replacing the slots remove them?

## Hands-on

- [ ] **EC-A11Y-01** · 30 min · Run Lighthouse and axe on a published guest page, then tab the same page end to end with the mouse unplugged. **Proves:** the tools pass a page the keyboard fails.
- [ ] **EC-A11Y-02** · 20 min · Set a branding set to a 3:1 text/background pair, publish, measure it, then switch the site to an SLDS 2 dark theme. **Proves:** contrast is a branding-set value, and dark mode moves it without touching a component.
- [ ] **EC-A11Y-03** · 25 min · Publish a page on a custom theme layout that omits the standard slots, then press F6. **Settles:** whether F6 regions come from the theme layout and vanish with it.
- [ ] **EC-A11Y-04** · 25 min · Put `aria-labelledby` on a custom LWC pointing at a label in another component, add a second using `aria-label`, and listen to both with a screen reader. **Proves:** IDREF ARIA dies at the shadow boundary on a real site page.

## Related

- [01 · Template choice & site landscape](01-template-choice-and-site-landscape.md) — the template decision is what fixes which ACR you can put in front of procurement
- [05 · Branding sets, design tokens & SLDS 2](05-branding-sets-design-tokens-and-slds-2.md) — where the contrast ratio is actually set, and what dark mode does to it
- [06 · Custom LWC in LWR sites](06-custom-lwc-in-lwr-sites.md) — SSR components cannot use synthetic shadow, so the IDREF ARIA workaround is unavailable
- [11 · Public site exposure audit](11-public-site-exposure-audit.md) — the same guest surface, audited for the other reason
- [16 · Site performance, caching & SEO](16-site-performance-caching-and-seo.md) — where Lighthouse already appears, and why its a11y score is not a conformance claim
- [../SF_core/03-lwc-and-slds/17 · Accessibility & internationalization](../SF_core/03-lwc-and-slds/17-accessibility-and-internationalization.md) — the component half: ARIA across a shadow boundary, `variant="label-hidden"`, locale imports

## Sources

- [Accessibility Standards](https://help.salesforce.com/s/articleView?id=xcloud.accessibility_overview.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-20
- [Product Accessibility Status](https://www.salesforce.com/company/legal/508_accessibility/) — Salesforce · read 2026-09-20
- [Experience Cloud – LWR Accessibility Conformance Report, Spring '25](https://www.salesforce.com/en-us/wp-content/uploads/sites/4/documents/legal/508%20accessibility/experience-cloud-lightning-web-runtime-desktop-and-web-mobile-spring-25-accessibility-conformance-report.pdf) — Salesforce · via search 2026-09-20
- [Experience Cloud – Aura Accessibility Conformance Report, Spring '25](https://www.salesforce.com/en-us/wp-content/uploads/sites/4/documents/legal/508%20accessibility/experience-cloud-aura-desktop-and-web-mobile-spring-25-accessibility-conformance-report.pdf) — Salesforce · via search 2026-09-20
- [Accessibility in LWR Sites](https://developer.salesforce.com/docs/atlas.en-us.exp_cloud_lwr.meta/exp_cloud_lwr/template_differences_accessibility.htm) — Salesforce Developers · via search 2026-09-20 — returned **403** to every direct fetch this run; the F6 and slot detail is snippet-sourced
- [Accessibility Mode Features](https://help.salesforce.com/s/articleView?id=xcloud.accessibility_mode_enabled.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-20
- [Directive (EU) 2019/882 (European Accessibility Act)](https://eur-lex.europa.eu/eli/dir/2019/882/oj) — EUR-Lex 🚩 · read 2026-09-20
- [The European accessibility standard EN 301 549 has been updated](https://accessible-eu-centre.ec.europa.eu/content-corner/news/european-accessibility-standard-en-301-549-has-been-updated-2026-09-07_en) — AccessibleEU, European Commission 🚩 · read 2026-09-20
- [DOJ extends ADA Title II web compliance deadlines](https://accessible.org/news/doj-extends-ada-title-ii-web-compliance-deadline/) — third party 🚩 · via search 2026-09-20
- [How much of accessibility can automated tools catch?](https://wcagc.com/blog/how-much-do-automated-accessibility-tools-catch) — third party 🚩 · via search 2026-09-20

## History

- 2026-09-20 · created — nothing owned the site-level obligation; `03-lwc · 17` covered components only
