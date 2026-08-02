# Static Resources & Third-Party JavaScript

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 07

**Scope:** Getting a chart library, a font or an image into a component, and handing part of the DOM to code the framework does not control. What LWS itself blocks is [09](09-lightning-web-security.md).

## Core idea

An LWC bundle has no `npm install`. Third-party code arrives one of two ways, and the platform has a clear preference. **Upload it as a static resource** and load it with `loadScript` — the file is served from your org, needs no external permission, and cannot disappear because someone else's CDN did. Or **reference an external origin**, which requires a CSP Trusted Site entry and makes a third party a runtime dependency of your page. The second is where most of the confusion in this area lives: a CDN script that will not load is almost always **Content Security Policy**, and it gets blamed on Lightning Web Security, which is a different mechanism with a much narrower blocked set ([09](09-lightning-web-security.md)). The other half of the topic is what happens once the library is loaded — because a library that writes DOM is writing into a tree the framework believes it owns, and that needs `lwc:dom="manual"` and a hard look at where the markup came from.

## How it works

- **Upload, then import the URL.** `import D3 from '@salesforce/resourceUrl/d3'` gives you the URL, not the library. `@salesforce/contentAssetUrl/x` does the same for a content asset.
- **A zip static resource is addressed by path** — `RESOURCE + '/dist/chart.min.js'` — which is how you ship a library with its CSS and fonts in one artefact.
- **`loadScript` and `loadStyle` return promises** and de-duplicate: loading the same URL twice in a page fetches once. Import them from `lightning/platformResourceLoader`.
- **Load in `renderedCallback`, guarded by a flag.** The library usually needs a DOM node to attach to, and `renderedCallback` runs on **every** render — without the flag you reload on every reactive change.
- **External origins need a CSP Trusted Site** — Setup → CSP Trusted Sites, with the right directive checked (`script-src` for scripts, `connect-src` for `fetch`, `font-src`, `img-src`). Missing entry, silent console-only failure.
- **`lwc:dom="manual"`** marks an element whose children are inserted outside the framework, so synthetic shadow can still scope styles into it. It goes on the *container*, and nothing inside it is reactive.

```js
import { loadScript, loadStyle } from 'lightning/platformResourceLoader';
import CHART from '@salesforce/resourceUrl/chartjs';       // a zip: lib + css

export default class Viz extends LightningElement {
    initialized = false;

    async renderedCallback() {
        if (this.initialized) return;                       // renderedCallback fires on every render
        this.initialized = true;
        await Promise.all([
            loadScript(this, CHART + '/dist/chart.umd.js'),
            loadStyle(this, CHART + '/dist/chart.css')
        ]);
        new window.Chart(this.template.querySelector('canvas'), this.config);
    }
}
```

## 2026 currency

Two constraints tightened. **At 67.0 LWS blocks the `data:` URI scheme** — a pattern that shows up constantly in chart-export and download-link code, where `data:image/png;base64,…` was the obvious answer. Build a blob and use a **`blob:`** object URL instead ([09](09-lightning-web-security.md)). And the ambient answer to "which library" has changed: **the platform now ships things that used to need one.** Virtualized lists are a base component in Developer Preview ([16](16-lwc-performance-and-debugging.md)), `<details name>` gives a zero-JavaScript accordion at 67.0 ([02](02-templates-directives-and-rendering.md)), and CSS custom properties cover most of what a theming library did ([14](14-slds-2-and-styling-hooks.md)). Every third-party library is a permanent LWS-compatibility and upgrade liability, so the question to ask first is whether the platform already does it.

## Gotchas

- **A blocked CDN script is CSP, not LWS.** Checking LWS settings for this wastes an afternoon; the fix is a CSP Trusted Site entry with the correct directive.
- **`renderedCallback` without a guard reloads the library on every render** — the single most common cause of a component that gets slower the longer it is open.
- **`@salesforce/resourceUrl/x` is a URL, not the library.** Importing it does not make `window.Chart` exist; `loadScript` does.
- **Libraries that use `eval`, `document.write()` or `Worker()` can fail under LWS** — `document.write()` and `Worker()` are on the genuinely blocked list.
- **`lwc:dom="manual"` content is outside reactivity and outside accessibility management.** Nothing re-renders it, and nothing manages its ARIA or focus → [17](17-accessibility-and-internationalization.md).
- **`innerHTML` with server data is an XSS hole.** Template bindings are sanitized; manual DOM is not. Sanitize, or build nodes rather than strings.
- **Static resources cap at 5 MB each and 250 MB per org** — a full charting suite with locales and fonts gets close faster than expected.
- **Cache Control `Public` vs `Private` matters in Experience Cloud** — a `Private` resource is not cached for guest users, and guest access has its own rules → [05-experience](../05-experience-cloud-lwr/INDEX.md).

## Recall

Q: A CDN-hosted script will not load in an LWC. What is the first thing to check?
A: CSP Trusted Sites, with `script-src` enabled for that origin. This is Content Security Policy, not Lightning Web Security.

Q: Why must `loadScript` in `renderedCallback` be guarded by a flag?
A: `renderedCallback` runs after every render, so an unguarded load re-fetches and re-initialises the library on every reactive change.

Q: What does `@salesforce/resourceUrl/myLib` actually import?
A: The URL of the static resource. The library is only available after `loadScript` resolves.

Q: What is `lwc:dom="manual"` for, and what does it cost?
A: It marks a container whose children are inserted outside the framework so synthetic shadow can scope styles into it. The cost is that its content is outside reactivity, accessibility management and template sanitization.

Q: Why is `data:` no longer usable for a generated download or image at 67.0?
A: LWS blocks the `data:` URI scheme. Create a blob and use a `blob:` object URL.

## Related

- [09 · Lightning Web Security](09-lightning-web-security.md) — what LWS genuinely blocks, and the three things routinely misattributed to it
- [13 · Shadow DOM, styling & scoped CSS](13-shadow-dom-styling-and-scoped-css.md) — why manual DOM needs a directive at all
- [17 · Accessibility & internationalization](17-accessibility-and-internationalization.md) — the a11y cost of DOM the framework does not manage
- [22 · LWC OSS & off-platform reuse](22-lwc-open-source-and-off-platform-reuse.md) — where `npm install` *is* the answer
- [07-security · Secure coding](../07-security-and-sharing/INDEX.md) — XSS, sanitization and CSP as an org-level control
