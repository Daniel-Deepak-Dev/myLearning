# Enhanced CMS & Content Delivery

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 19

**Scope:** Authoring and delivering structured content with Salesforce CMS — workspaces, content types, channels, collections and taxonomy — and how an **enhanced** LWR site consumes it. Headless delivery of the same content is [15](15-headless-sites-and-connect-apis.md).

## Core idea

Salesforce CMS is a hybrid content platform: content is authored once in a **workspace** and delivered to many **channels** — one or more Experience Cloud sites, plus external systems via API. A **content type** is the schema (News, Image, Document, or a **custom content type** with your own fields); a content item is an instance. **Channels** decouple authoring from delivery — the same News article feeds a public site, a partner site and a mobile app. The "enhanced" platform is the current generation: since Winter '25 every new workspace is enhanced by default, adding cross-workspace content sharing, variants, folders and **taxonomy** tags. The catch that matters here: **Enhanced CMS delivers to enhanced LWR sites** (and Aura), and enhanced LWR is a different product from plain LWR → [02](02-lwr-architecture-and-build-model.md).

## How it works

- **Workspace → channel is many-to-many.** A workspace can publish to several channels; a channel (public or restricted) can draw from several enhanced workspaces. Restricted channels gate delivery behind authentication.
- **Content types:** standard (News, Image, Document) plus up to **100 active custom content types** org-wide. Create/edit them with the CMS Content Type Manager app, or via **Metadata API (`ManagedContentType`)** or **Tooling API (`ManagedContentNodeType`)**.
- **Collections** are curated groupings used to bind a component (list, carousel) to content without hard-coding item IDs. **Both tiers have a cap:** a *manual* collection holds up to **50 items of one content type**; a *dynamic* (query-driven) collection returns up to **250 items**, ordered by relevance.
- **Workspaces are capped at 2,000 per org** — rarely a constraint, but it is a hard one.
- **Taxonomy** classifies content org-wide: a taxonomist defines one hierarchy of terms, applied as tags across enhanced workspaces for faceted retrieval.
- **In-site consumption:** CMS components in Experience Builder bind to a channel; the LWR build caches published content at the edge → [16](16-site-performance-caching-and-seo.md).

## 2026 currency

Enhanced workspaces are the default and the only place taxonomy, variants and cross-workspace sharing work — classic workspaces are frozen feature-wise. Enhanced LWR sites are deployed as the **`DigitalExperienceBundle`** metadata type, not `ExperienceBundle` — the deployment trap in [18](18-experience-cloud-devops.md). **Quote the caps in pairs:** content types 100 active, workspaces 2,000, collections 50 manual / 250 dynamic.

## Gotchas

- **Enhanced ≠ classic, and you can't convert in place.** Moving classic content to an enhanced workspace is a migration, not a toggle.
- **Enhanced CMS features assume enhanced LWR.** A non-enhanced LWR or Aura site won't get the full enhanced-delivery surface — check the site's runtime first, [02](02-lwr-architecture-and-build-model.md).
- **Custom content type cap is 100 active** org-wide, shared across all workspaces — not per workspace.
- **Manual collections cap at 50 items, single type — and dynamic ones at 250.** "Use a dynamic collection instead" raises the ceiling; it does not remove it, and a catalogue above 250 needs paging or a different component.
- **Restricted channels still need sharing.** Authenticating a channel controls delivery; it doesn't grant record access to anything the content references.
- **Publishing is per-channel.** Content live in a workspace is invisible on a site until published to that site's channel.

## Recall

Q: What is the relationship between a CMS workspace and a channel?
A: Many-to-many — a workspace publishes to multiple channels, and a channel can draw from multiple enhanced workspaces. It decouples authoring from delivery.

Q: How do you create a custom content type programmatically, and what's the cap?
A: Via Metadata API (`ManagedContentType`) or Tooling API (`ManagedContentNodeType`); up to 100 active custom types org-wide.

Q: What are the collection limits?
A: A manual collection holds **50 items** of a single content type; a dynamic, query-driven collection returns up to **250**, by relevance. Both tiers are capped — quote them together.

Q: What changed with "enhanced" CMS workspaces, and since when?
A: Since Winter '25 new workspaces are enhanced by default, adding cross-workspace sharing, variants, folders and org-wide taxonomy tags. Classic workspaces are the migration source.

Q: Which site runtime does Enhanced CMS assume, and why does it matter?
A: Enhanced LWR (distinct from plain LWR) — the wrong runtime won't get the full enhanced-delivery surface, so verify the site's runtime before designing around it.

## Related

- [15 · Headless sites & Connect APIs](15-headless-sites-and-connect-apis.md) — delivering this same content to a decoupled front end
- [18 · Experience Cloud DevOps](18-experience-cloud-devops.md) — `DigitalExperienceBundle` when deploying enhanced sites + CMS
- [02 · LWR architecture & build model](02-lwr-architecture-and-build-model.md) — LWR vs enhanced LWR, the distinction Enhanced CMS depends on
