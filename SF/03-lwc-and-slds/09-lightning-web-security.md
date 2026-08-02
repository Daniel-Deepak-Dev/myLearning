# Lightning Web Security

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 06

**Scope:** The sandbox your component's JavaScript actually runs in, and the behaviour changes it causes. Org-level security — profiles, permission sets, sharing — is [07-security](../07-security-and-sharing/INDEX.md); CSP trusted sites belong to [06-integration](../06-integration-and-apis/INDEX.md).

> **What changed.** **Lightning Locker was replaced by Lightning Web Security (LWS)** — a different architecture with different rules, so every "Locker blocks X" answer needs re-testing rather than translating. Two corrections to the usual telling: Locker is **not retired** (it remains the default in orgs created before Winter '23, and LWS is a Session Settings checkbox you can still switch off), and LWS is **not a blanket firewall** — it is namespace isolation, and most of what people attribute to it is actually namespacing, sanitization, CSP or the LWC framework.

## Core idea

Locker handed your code wrapped objects — `SecureWindow`, `SecureDocument`, `SecureElement` — proxies that intercepted access and refused the dangerous parts. That is why so much ordinary JavaScript and so many third-party libraries broke under it: they were not talking to the real DOM. LWS inverts the approach. It **virtualizes the browser per namespace**: your code gets its own JavaScript sandbox with real standard APIs, and the platform *distorts* individual ones — altering specific native functions and property accessors so they cannot be used to escape the sandbox. The practical consequence is that most code and most libraries now just work, and the failures that remain are narrow and specific. The mental shift the ⚠️ is really about is this: under Locker you asked "is this allowed?"; under LWS you ask **"is this namespaced, sanitized, distorted, or genuinely blocked?"** — four different answers with four different symptoms.

## How it works

| Mechanism | What you see |
|---|---|
| Namespace sandbox | your own `window`, `document`, real standard APIs |
| Namespaced storage | `localStorage`/`sessionStorage` keys silently prefixed (`LSKey…`) |
| Namespaced cookies | `document.cookie` returns only cookies your namespace set |
| Distortions | specific APIs altered — filtered, sanitized, or throwing |
| Cross-namespace proxies | objects from another namespace arrive as `Proxy` |
| Blocked outright | `document.write()`, `Worker()`, `ServiceWorkerContainer`, `window.find()`, XSLT |

- **Namespacing failures are silent.** A key written by another namespace reads back as `null` with no error — it looks like the data was never saved. For anything cross-namespace or session-related, go to Apex.
- **Mutating an object you received from another namespace does nothing.** The change is absorbed by the proxy and the originating component keeps the old value. Clone, mutate the clone, and send a `CustomEvent` back. → [04](04-events-and-component-communication.md)
- **Complex objects in an event `detail` can unwrap to `null` across a namespace boundary.** Serialize to JSON, or send primitives — which is also what [04](04-events-and-component-communication.md) recommends for unrelated reasons.
- **Three common failures are not LWS at all.** External CDN `<script>` tags are blocked by **CSP** (use a static resource with `lightning/platformResourceLoader`); `$A`, `Aura`, `Sfdc` and `sforce` are blocked by the **LWC framework**; `fetch('/aura')` is blocked because it is an internal endpoint. Blaming LWS for these sends you looking in the wrong place.
- **LWS does not sanitize your own shadow DOM.** `innerHTML` still works and is still an XSS vector — the sandbox is isolation, not input validation. Use the template directives or `lightning-formatted-rich-text`.

```js
// 67.0: LWS blocks the `data:` scheme on an anchor's href — client-side downloads must use blob:
const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
const a = Object.assign(document.createElement('a'), { href: url, download: 'orders.csv' });
a.click();
URL.revokeObjectURL(url);                 // origin-bound; revoke or it leaks for the page's life
```

## 2026 currency

**Summer '26 shipped a batch of new distortions, and one of them breaks working code.** `HTMLAnchorElement.prototype.href` now **blocks the `data:` URI scheme** — the standard "build a CSV in JavaScript and hand the user a download link" pattern stops working, and the fix is the `blob:` object URL above, which was the better pattern anyway. The rest of the batch covers `Element.getAttribute`, the `innerHTML`/`outerHTML` **getters**, `MutationObserver.observe`, the `IndexedDB` factory and `Promise.then`/`catch`/`finally`, each with a matching ESLint rule. Two tools make this checkable rather than guessable: the **updated LWS ESLint package**, and the **LWS Distortion Viewer**, which lists every distorted API and what it does. Run both before raising a bundle's `apiVersion`, because a distortion change lands with the API version, not with the org upgrade. → [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md)

## Gotchas

- **`data:` URLs in an anchor `href` are dead at 67.0.** Also check event payloads and anything building a download link. Grep for `data:` before upgrading.
- **A namespaced storage miss returns `null`, not an error** — the single most misdiagnosed LWS symptom.
- **Cross-namespace mutation fails silently.** No exception, no warning, just a stale value in the component that sent the object.
- **`eval()` and `Function()` are not blocked.** They run inside the sandbox — which means LWS is not protecting you from an injection you wrote yourself.
- **Web Workers have no supported workaround.** `Worker()` throws, and there is no LWS-safe equivalent; move the work to the server.
- **Turning LWS on is org-wide, not per-component.** Session Settings → *Use Lightning Web Security for Lightning web components and Aura components* — test in a sandbox, because it changes every component at once.
- **Distortions can be disabled for debugging only.** Useful to confirm a distortion is the cause; never a fix, and never available in production.

## Recall

Q: How does LWS's approach differ from Lightning Locker's?
A: Locker wrapped objects in secure proxies; LWS virtualizes the browser per namespace and distorts specific native APIs, so standard JavaScript and third-party libraries mostly work unchanged.

Q: Is Lightning Locker retired?
A: No. LWS is the default for orgs created in Winter '23 and later and GA for all orgs, but pre-Winter-'23 orgs still default to Locker and the setting is a Session Settings checkbox.

Q: Why does `localStorage` appear to lose data under LWS?
A: Keys are namespaced transparently. Anything written by another namespace reads back as `null` with no error.

Q: What broke at 67.0 and what replaces it?
A: `data:` URIs in an anchor's `href` are blocked. Build a `Blob` and use a `blob:` object URL, revoking it after use.

Q: Name three restrictions commonly blamed on LWS that are something else.
A: External CDN scripts (CSP), `$A`/`Sfdc`/`sforce` globals (the LWC framework), and `fetch` to `/aura` or `/webruntime` (internal endpoints).

## Related

- [04 · Events & component communication](04-events-and-component-communication.md) — why event payloads should be primitives, doubly so across namespaces
- [13 · Shadow DOM, styling & scoped CSS](13-shadow-dom-styling-and-scoped-css.md) — the other boundary that changes what your JavaScript can reach
- [07-security · secure coding](../07-security-and-sharing/INDEX.md) — XSS, CSP and the checks LWS explicitly does not do for you
