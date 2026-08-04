# Navigation, Search & Audiences

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 19

**Scope:** How a visitor moves through an LWR site and what they see — navigation menus, site search, and audience-based personalization. The site scaffold this sits on is built in [02](02-lwr-architecture-and-build-model.md); the guest visibility rules underneath it are [07](07-guest-user-security-model.md).

## Core idea

Three separate systems decide what a user encounters. **Navigation** is menu structure — a Navigation Menu that can point at site pages, external URLs, standard objects or menu labels. **Search** is a query surface over the records, CMS content and Knowledge the user is allowed to see. **Audiences** are the personalization layer: a targeting rule (profile, location, record field, permission, or CMS-driven criteria) that swaps which page variation, component, or nav menu a given visitor gets. They compose — an audience can assign a different navigation menu entirely, so the same URL renders differently per segment.

## How it works

- **Navigation menus are metadata, not page config.** One menu can be reused across pages and theme layouts; a page references it. Menu items carry their own audience rules, so a link can be hidden from guests without touching the target page.
- **Search in LWR** is component-driven — the Search Block / Search Results components and a global search box in the theme layout. What is searchable is governed by the object's sharing plus whether it is a searchable object for the site, **not** by what is merely on a page.
- **Audiences target at three grains:** page variations (a whole alternate page), component visibility (show/hide within a page), and navigation assignment. First matching audience wins — order matters.
- **Audience criteria** include user fields, profile, permission, domain, location (IP), and — in enhanced sites — **record- and CMS-content-based** criteria for content-driven personalization.

## 2026 currency

Enhanced LWR sites expanded audience criteria beyond the classic profile/location set to **record- and CMS-driven** targeting, so personalization can key off the CMS content a page renders rather than only who the user is. Guest-facing search continues to tighten: a searchable object still surfaces nothing a guest sharing rule hasn't granted.

## Gotchas

- **A nav link is not an access grant.** Hiding a menu item via audience hides the *link*, not the *page* — the URL is still reachable. Enforce access with guest sharing and page-level audiences → [07](07-guest-user-security-model.md).
- **Search returns only share-visible records.** An empty result for a guest is usually a missing guest sharing rule, not a search-config bug.
- **Audience order is first-match.** A broad audience above a narrow one shadows it — the narrow rule never fires.
- **Menu items pointing at objects** respect the object's tab/visibility settings; a hidden object yields a dead link for some users.
- **Deleting a page** leaves nav items dangling — they don't auto-remove, and a guest hitting one gets an error page.
- **External-URL menu items** bypass SSR/caching entirely; don't expect them in the sitemap or SEO crawl.

## Recall

Q: What are the three grains an audience can target in an LWR site?
A: A whole page variation, an individual component's visibility, and which navigation menu is assigned.

Q: Why does hiding a navigation item not secure a page?
A: The audience rule hides the link, but the page's URL is still directly reachable — access must be enforced by guest sharing and page-level rules.

Q: What determines whether a record type appears in site search results?
A: It must be a searchable object for the site *and* the running (or guest) user must have sharing visibility to the record.

Q: When two audiences both match a visitor, which applies?
A: The first matching audience in order — ordering shadows narrower rules placed below broad ones.

Q: What new audience criteria did enhanced LWR sites add?
A: Record-based and CMS-content-based criteria, enabling content-driven personalization rather than only user attributes.

## Related

- [14 · Enhanced CMS & content delivery](14-enhanced-cms-and-content-delivery.md) — the content that CMS-driven audiences key off
- [07 · Guest user security model](07-guest-user-security-model.md) — why menu hiding is never a security control
- [07-security · 06 OWD](../07-security-and-sharing/06-org-wide-defaults-and-record-access.md) — the sharing model search visibility rests on
