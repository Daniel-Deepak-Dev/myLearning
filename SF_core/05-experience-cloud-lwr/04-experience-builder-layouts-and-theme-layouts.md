# Experience Builder Layouts & Theme Layouts

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

**Scope:** The composition model inside Experience Builder — what a page is made of, and the two extension points you can replace with your own LWC. Component *authoring* rules are [06](06-custom-lwc-in-lwr-sites.md); colour and typography are [05](05-branding-sets-design-tokens-and-slds-2.md).

## Core idea

An LWR page is four nested things: a **theme layout** wraps every page in the site (header, nav, footer), a **page layout** divides one page's body into regions, **regions** hold components, and **components** hold content. The theme layout is site-wide chrome; the page layout is per-page structure. Getting the two straight is most of what makes Experience Builder feel predictable rather than fiddly.

What is different about LWR is that **both extension points are ordinary Lightning web components you write** — with the right target in `js-meta.xml` and a `<slot>` where child content goes. On Aura they were Aura components. That is the whole of the difference, and it is why an Aura theme layout cannot be lifted across → [12](12-aura-to-lwr-migration-and-coexistence.md).

## How it works

```xml
<!-- theme layout: site-wide chrome, appears under Settings → Theme -->
<targets><target>lightningCommunity__Theme_Layout</target></targets>
<!-- page layout: body structure, appears in the Content Layout window -->
<targets><target>lightningCommunity__Page_Layout</target></targets>
```

- **A default `<slot>` marks the main content region** in a theme layout. **Named slots create regions** in a page layout — the slot name is what Experience Builder shows as a droppable area.
- **Neither target supports component properties on its own.** `lightningCommunity__Theme_Layout` needs `lightningCommunity__Default` added alongside it, with the properties declared in `targetConfigs`, before anything is editable in the builder.
- **Only properties defined for `lightningCommunity__Page` or `lightningCommunity__Page_Layout` are editable** in Experience Builder — which is the rule people discover after wiring the property to the wrong target.
- **Theme layouts are assignable per page**, so a login page or a landing page can drop the site nav without a second site.
- **Pages come in kinds** — standard, object (list/detail/related), login, and error — and object pages are the only place record components work in LWR → [01](01-template-choice-and-site-landscape.md).
- **Expression-based visibility** is an enhanced-LWR feature; on non-enhanced LWR you get component-level visibility rules only → [02](02-lwr-architecture-and-build-model.md).
- **Audience targeting layers on top** of all of this and is covered with navigation in phase 19.

## Gotchas

- **A component with no `<slot>` swallows its children silently.** The builder shows an empty region and no error.
- **Wiring a property to `lightningCommunity__Theme_Layout` alone makes it invisible in the builder** — add `lightningCommunity__Default` or it is not editable.
- **A theme layout runs on every page including login and error pages**, so anything in it that assumes an authenticated user breaks the unauthenticated ones → [10](10-authentication-self-registration-and-sso.md).
- **Page layouts are not Salesforce page layouts.** Same word, unrelated concept; in a mixed conversation say *content layout* → [01-admin · 05](../01-admin-and-declarative-platform/05-dynamic-forms-and-lightning-app-builder.md).
- **Deleting a layout component that a page still uses breaks the page**, and the failure shows up at publish rather than at save.
- **LWR has no generic record page.** Wanting record detail on a standard page is the single commonest Aura-shaped request that LWR refuses.

## Recall

Q: What is the difference between a theme layout and a page layout in Experience Builder?
A: The theme layout is site-wide chrome around every page; the page layout divides one page's body into regions.

Q: Which targets make an LWC usable as LWR chrome and as page structure?
A: `lightningCommunity__Theme_Layout` and `lightningCommunity__Page_Layout` respectively.

Q: How do you create a droppable region inside a custom LWR layout?
A: With slots — a default `<slot>` for main content in a theme layout, named slots for regions in a page layout.

Q: Why is a custom theme layout's property not editable in Experience Builder?
A: Because the theme layout target doesn't support properties on its own; `lightningCommunity__Default` must be added with the properties in `targetConfigs`.

Q: Which visibility mechanism requires enhanced LWR?
A: Expression-based visibility — non-enhanced LWR sites get component-level visibility rules only.

## Related

- [06 · Custom LWC in LWR sites](06-custom-lwc-in-lwr-sites.md) — the rest of the target vocabulary and the SSR constraints
- [05 · Branding sets, design tokens & SLDS 2](05-branding-sets-design-tokens-and-slds-2.md) — how the chrome gets its colours
- [12 · Aura to LWR: migration & coexistence](12-aura-to-lwr-migration-and-coexistence.md) — why an Aura theme layout cannot come across
- [01-admin · 05 Dynamic Forms & Lightning App Builder](../01-admin-and-declarative-platform/05-dynamic-forms-and-lightning-app-builder.md) — the internal-app cousin of this composition model
