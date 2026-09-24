---
vault: SF_Experience_Cloud
format: light
level: basic
status: open
gaps: 2
org_checks: 2
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [guest-access]
---
# Topics & Knowledge on Sites

**One line:** On an Aura site, topics are the site's own map of its Knowledge and discussions. Navigational topics build the **Topics** menu, featured topics are home-page tiles, and content topics tag the rest.

**Reach for it when:** you build an Aura self-service site on Knowledge, or someone asks why a published article is not on the site.

> **From my notes.** "what is Featured Topics, Navigational Topics, Article Management in CMS of Experience cloud?" — **Corrected:** they live in Experience Workspaces → **Content Management → Topics**, the site's topic management. That is not Salesforce CMS, whose workspaces and channels are [14](14-enhanced-cms-and-content-delivery.md).

## Key points

- **Prerequisite:** Setup → **Topics for Objects** → Knowledge → **Enable Topics** → [SF_core · 01 · 20](../SF_core/01-admin-and-declarative-platform/20-topics-for-objects.md). After that each site builds its own: a site topic is a `Topic` row with the site's `NetworkId` and a `ManagedTopicType` of `Navigational`, `Featured` or `Content`.

| Type | Content Management → Topics → | Visitors see | Cap |
|---|---|---|---|
| Navigational | **Navigational Topics** | the **Topics** menu on every page, plus the Topic Catalog (menu link **More Topics...**) once a subtopic exists; banner 1400 × 180 | 25 parents, two subtopic levels of 10 in the UI; 2,775 via Connect API |
| Featured | **Featured Topics** — reuse a navigational or member-created topic | tiles in the home page body; thumbnail 385 × 385 | 25 |
| Content | **All Topics → All Content Topics** → New, **Enable for content** | a tag on your own content | 5,000 |

- **Article Management** (Content Management → Topics → **Article Management**) tags articles one by one: search, filter by data category, type a topic, and a comma after a new name creates it. "No articles found" means the article's channel doesn't match the site type, or its language isn't your user language.
- **Automatic Topic Assignment** tags every article in a data category, future ones included, adding topics up the category hierarchy but never down and never removing them. It is set per site, like every topic assignment.

## The Trailhead claim, corrected

- **Topics don't decide who can see an article.** That takes a published article, the right channel — **Visible to Customer**, **Visible to Partner**, or **Visible in Public Knowledge Base** for guests — and access: category visibility or sharing, Read on Knowledge, field-level security → [Knowledge](../SF_Service/knowledge.md).
- **Topics decide where an Aura site shows it:** the Topics menu, featured tiles and topic pages — and "any article with an assigned navigational, featured, or content topic is included in search results." So the claim states a navigation fact as an access fact. 🚩 Whether an untopicked, customer-visible article is still reachable by search or URL is unsourced.
- **LWR uses data categories instead.** Winter '24 notes say knowledge articles "were mapped to topics instead of data categories" and reached LWR "only through search". Data categories on LWR went GA in Spring '24: **Knowledge Article List**, **Subcategories List**, **Data Category Path**.

## Gotchas

- **Guests need Read on Knowledge and a Topic Detail page variation with Audience = Default**, which Help gives as causes of guests seeing no articles → [07](07-guest-user-security-model.md). Topic images also need Administration → Preferences → **Let guest users view asset files and CMS content available to the site**.
- **Linking a navigational topic to a data category adds current articles only.** Repeat it for new ones, or use Automatic Topic Assignment.
- **Merging a navigational or featured topic** discards its type, image and subtopic links.

## Gaps to close

- [ ] Do the Help Center and Build Your Own (Aura) templates render navigational and featured topics as Customer Service does, with the same caps?
- [ ] Does the `ManagedTopics` metadata type carry topic images and article assignments, or only the topic tree?

## Confirm in org

- 🚩 On a Customer Service site, can a customer find a published, Visible-to-Customer article with no topic by site search, or open it by URL? — search its title as the customer, then paste its URL.
- 🚩 Does a **Build Your Own (LWR)** site show Content Management → Topics, and does its Navigation Menu offer a topic item? — create one in a Developer Edition org.

## Hands-on

- [ ] **EC-TOPIC-01** · 30 min · On a Customer Service site add two navigational topics (one with a subtopic), feature one with a 385 × 385 image, tag articles in Article Management, publish and browse. **Proves:** navigational is the Topics menu, featured is home-page tiles, and a tagged article lands on its topic page.
- [ ] **EC-TOPIC-02** · 15 min · Publish an article with **Visible to Customer** unticked, then look for it in Article Management and on the site as a customer. **Proves:** the channel gates it — Article Management shows "No articles found" and the site never lists it. **Needs:** a customer user.
- [ ] **EC-TOPIC-03** · 20 min · Remove the only topic from a customer-visible article, then check its topic page, site search and its URL as a customer. **Proves:** exactly where an untopicked article disappears. **Settles:** the first 🚩 in Confirm in org. **Needs:** a customer user.
- [ ] **EC-TOPIC-04** · 15 min · Untick **Enable Topics** for Knowledge in Topics for Objects, then reopen Article Management and a topic page. **Proves:** what the site's topic tools do when the platform switch under them is off.

## Related

- [SF_core · 01-admin · 20 Topics for Objects](../SF_core/01-admin-and-declarative-platform/20-topics-for-objects.md) — the org switch, and the `Topic` / `TopicAssignment` rows every site topic is built from
- [SF_Service · Knowledge](../SF_Service/knowledge.md) — channels, data categories and access: what really decides whether an article can be seen
- [01 · Template choice & site landscape](01-template-choice-and-site-landscape.md) — why Customer Service gives you topic navigation free and Build Your Own (LWR) does not
- [13 · Navigation, search & audiences](13-navigation-search-and-audiences.md) — the navigation menu that holds the Topics dropdown and the Topic Catalog link
- [14 · Enhanced CMS & content delivery](14-enhanced-cms-and-content-delivery.md) — Salesforce CMS, the thing Content Management → Topics is not
- [07 · Guest user security model](07-guest-user-security-model.md) — the guest profile and sharing rules a Public Knowledge Base article still depends on

## Sources

- [Experience Cloud Sites Managers Guide (PDF)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_communities_managers_guide.pdf) — Salesforce, Winter '27, last updated 22 July 2026 · read 2026-09-24 · the three topic types, Workspaces paths, caps (25 / 10 / 10, 2,775, 25 featured, 5,000 content), image sizes, Article Management, Automatic Topic Assignment, Topic Catalog, merge, search inclusion — nothing used is Winter '27-only
- [Organize Experience Cloud Sites with Topics](https://help.salesforce.com/s/articleView?id=experience.networks_topics_overview.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Set Up Navigational Topics](https://help.salesforce.com/s/articleView?id=networks_topics_navigational.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · the Customer Service caps table and the 2,775 API total
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `Topic.ManagedTopicType` (API 44.0+) and `Topic.NetworkId` — a Winter '27 build; long-standing fields only
- [ManagedTopics](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_managedtopics.htm) — Metadata API Developer Guide · via search 2026-09-24 · *"navigational and featured topics managed in an Experience Cloud site"*
- [No Articles Found in Experience Cloud Site Workspaces Topics Article Management](https://help.salesforce.com/s/articleView?id=000393316&language=en_US&type=1) — Salesforce Help 000393316 · read 2026-09-24 · channel or language mismatch
- [Guest Users Not Able to Access Knowledge Articles](https://help.salesforce.com/s/articleView?id=000382783&language=en_US&type=1) — Salesforce Help 000382783 · read 2026-09-24 · default Topic Detail page variation; Read on Knowledge for the guest profile
- [Salesforce Winter '24 Release Notes (PDF)](https://resources.docs.salesforce.com/246/latest/en-us/sfdc/pdf/salesforce_winter24_release_notes.pdf) — Salesforce · read 2026-09-24 · *Structure Your Help Site with Data Categories (Beta)*; *Show Knowledge Articles on Your Enhanced LWR Site*
- [Salesforce Spring '24 Release Notes (PDF)](https://resources.docs.salesforce.com/248/latest/en-us/sfdc/pdf/salesforce_spring24_release_notes.pdf) — Salesforce · read 2026-09-24 · LWR data categories GA; Subcategories List; Data Category Path
- [Set Up Knowledge for Enhanced LWR Sites](https://help.salesforce.com/s/articleView?id=service.knowledge_set_up_lwr.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · LWR Knowledge pages and the data category route
- [LWR Sites for Experience Cloud (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/exp_cloud_lwr.pdf) — Salesforce Developers · read 2026-09-24 · no topic feature documented; LWR Template Limitations list — absence is not proof, hence the org check
- [Add Knowledge to the Site Using Topics](https://trailhead.salesforce.com/content/learn/projects/build-a-community-with-knowledge-and-chat/add-branding-and-components-to-the-community) — Trailhead · read 2026-09-24 · Workspaces → Content Management → Topics; the three navigational and featured topics; Article Management
- [Enable and Configure Lightning Knowledge](https://trailhead.salesforce.com/content/learn/projects/build-a-community-with-knowledge-and-chat/add-knowledge-to-the-community-using-topics) — Trailhead · read 2026-09-24 · *"Without enabling Salesforce Knowledge topics, articles can't be displayed outside an org"*

## History

- 2026-09-24 · created from your Trailhead feed (Knowledge & Enhanced Chat site project)
