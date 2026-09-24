---
vault: SF_Service
format: light
level: basic
status: open
gaps: 2
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [sharing]
---
# Knowledge

**One line:** Lightning Knowledge is Service Cloud's article base. Each article version is a `Knowledge__kav` record, shaped by a record type, classified by data categories and published to one or more channels.

**Reach for it when:** agents, customers or site visitors need one reviewed answer instead of every rep writing their own.

> **From my notes.** why "Without enabling Salesforce Knowledge topics, articles can't be displayed outside an org."? — **Corrected:** topics don't make an article visible. Its **channel** checkboxes and the reader's access do; topics only decide where an Aura site surfaces it → [EC 23](../SF_Experience_Cloud/23-topics-and-knowledge-on-sites.md).

## Key points

- **Setup is a guided flow.** The project used Setup → **Salesforce Go** → Knowledge; Help documents the same steps from **Service Setup**. It enables Lightning Knowledge, makes your chosen users authors, creates the **FAQ** record type and layout, and adds data category groups. By hand it is Setup → **Knowledge Settings** → **Enable Lightning Knowledge**, which can't be undone.
- **Record types replace Classic article types.** A record type such as FAQ sets an article's fields and layout, up to 200 per object. The project's `Text` field is an ordinary custom field on `Knowledge__kav`.
- **Authors need the Knowledge User feature licence**, a checkbox on the User record: "To do more than read articles, agents need the Knowledge User license." Customer and partner users don't need it. The flow also assigns authors the **Knowledge LSF** permission set.
- **Permissions:** reading published articles takes **Allow View Knowledge** plus Read on Knowledge. **Manage Articles** creates, edits, publishes and archives; **View Draft Articles** and **View Archived Articles** open the other states.
- **The lifecycle is `PublishStatus`:** `Draft` → `Online` (shown as Published) → `Archived`. An article holds one draft, one published and several archived versions; editing a published one makes a draft that publishes as a new version. Publish now, or schedule it — scheduled publishing runs in 15-minute intervals.
- **Channels are four checkboxes on the layout** — the real answer to "who outside the org can read this":

| Layout label | Field | Read by |
|---|---|---|
| Visible in Internal App | `IsVisibleInApp` | internal users |
| Visible to Customer | `IsVisibleInCsp` | customer site users |
| Visible to Partner | `IsVisibleInPrm` | partner site users |
| Visible in Public Knowledge Base | `IsVisibleInPkb` | guests on sites and Salesforce Sites |

- **Data categories classify articles:** Setup → **Data Category Setup**. Defaults: 5 groups with 3 active, 100 categories per group, 5 levels, 8 categories per group on one article. A new group stays inactive until activated, and translations inherit the primary article's categories.
- **Data category visibility is the default access model.** Set All, None or Custom per role, permission set, permission set group or profile — high-volume portal users have no role — and definitions combine with OR. A reader must see one category per group on the article, and seeing France also shows Europe and every French city.
- **Or switch to standard sharing:** Knowledge Settings → **Use standard Salesforce sharing**. Then OWD and sharing rules decide access — Public Read/Write internal, Private external by default — and guest user sharing rules decide what guests read.

## Gotchas

- **A channel is necessary, not sufficient.** The reader must also pass data category visibility or sharing, hold Read on Knowledge, and have field-level security on the fields shown.
- **Once any category visibility is set, users with none see only uncategorized articles**, unless a group is visible by default. Setting it for one team quietly narrows everyone else.
- **The Classic Public Knowledge Base package doesn't work with Lightning Knowledge.** For guests, Help points to an Experience Cloud site such as the Help Center template.

## Gaps to close

- [ ] On the publish dialog, what does answering yes to "do my changes affect existing translations" do — does it set `IsOutOfDate` on each translation?
- [ ] Which channel does a Customer Community Plus user read on a customer site: Customer, or Partner because the licence carries roles?

## Confirm in org

- 🚩 Does Salesforce Go's Knowledge setup do what Service Setup's flow is documented to do — tick **Knowledge User** and assign **Knowledge LSF** — and what does that permission set actually grant? — open an author's User record and the permission set after the flow.

## Hands-on

- [ ] **SVC-KNOW-01** · 15 min · Publish an FAQ, edit and republish it, then query `Knowledge__kav` for its `KnowledgeArticleId` — first with no `PublishStatus` filter, then with `PublishStatus = 'Archived' AND IsLatestVersion = false`. **Proves:** one article is many version rows, and whether the documented "filter `PublishStatus` or `Id`" rule still errors — copy it verbatim.
- [ ] **SVC-KNOW-02** · 25 min · Give a test user's permission set Custom category visibility on one category, file one article under a different category and leave a second uncategorized, then log in as the user. **Proves:** the categorized article vanishes and the uncategorized one stays. **Needs:** second user.
- [ ] **SVC-KNOW-03** · 10 min · Untick **Knowledge User** on an author, then try to create and to edit an article. **Proves:** without the feature licence a user can only read — copy the message verbatim. **Needs:** second user.
- [ ] **SVC-KNOW-04** · 30 min · Schedule an article to publish 20 minutes out, look for a way to cancel it from the draft, then note when it goes live. **Proves:** publishing lands on a 15-minute slot, and a Lightning draft has no **Cancel Publication** button.

## Related

- [SF_core · 01-admin · 20 Topics for Objects](../SF_core/01-admin-and-declarative-platform/20-topics-for-objects.md) — the Setup switch that makes articles taggable, and what a topic actually is
- [SF_Experience_Cloud · 23 Topics & Knowledge on sites](../SF_Experience_Cloud/23-topics-and-knowledge-on-sites.md) — how a site surfaces articles, and the Trailhead claim corrected in full
- [SF_core · 07-security · 02 Licences & what they gate](../SF_core/07-security-and-sharing/02-licences-and-what-they-gate.md) — the Knowledge User feature licence, and why it hides as a checkbox on the User record
- [SF_core · 10-soql · 09 SOSL modifiers & relevance](../SF_core/10-soql-and-sosl/09-sosl-search-modifiers-and-relevance.md) — `WITH DATA CATEGORY`, the query side of the categories set up here
- [SF_core · 01-admin · 16 Search configuration & Einstein Search](../SF_core/01-admin-and-declarative-platform/16-search-configuration-and-einstein-search.md) — Promoted Search Terms, which pin an article to the top for chosen search terms
- [Enhanced Chat](enhanced-chat.md) — the channel where reps insert article content into a live conversation

## Sources

- [Lightning Knowledge Guide (PDF)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/lightning_knowledge_guide.pdf) — Salesforce, Winter '27, last updated 22 July 2026 · read 2026-09-24 · the setup flow and **Knowledge LSF**; the Knowledge User licence and permissions table; versions; scheduling in 15-minute intervals; the four channel labels; data category limits and visibility; standard sharing — nothing used is Winter '27-only
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `Knowledge__kav` (API 39.0+): `IsVisibleInApp`/`Csp`/`Prm`/`Pkb`, `PublishStatus` values, the Knowledge User access rule — a Winter '27 build; only long-standing fields are used
- [Discover and Set Up Service Features with Salesforce Go](https://help.salesforce.com/s/articleView?id=service.salesforce_go_service.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Setup → Salesforce Go → search *Knowledge*
- [Salesforce Knowledge Article Visibility and Data Category](https://help.salesforce.com/s/articleView?id=000382931&language=en_US&type=1) — Salesforce Help 000382931 · read 2026-09-24 · no visibility means uncategorized articles only
- [No Articles Found in Experience Cloud Site Workspaces Topics Article Management](https://help.salesforce.com/s/articleView?id=000393316&language=en_US&type=1) — Salesforce Help 000393316 · read 2026-09-24 · `IsVisibleInCsp` customer sites, `IsVisibleInPrm` partner sites, `IsVisibleInPkb` sites and Salesforce Sites
- [Salesforce Winter '21 Release Notes (PDF)](https://resources.docs.salesforce.com/228/latest/en-us/sfdc/pdf/salesforce_winter21_release_notes.pdf) — Salesforce · read 2026-09-24 · *Use Knowledge Sharing with Guest Users and High-Volume Community Users*: guest user security policies apply to Knowledge under standard sharing
- [Enable and Configure Lightning Knowledge](https://trailhead.salesforce.com/content/learn/projects/build-a-community-with-knowledge-and-chat/add-knowledge-to-the-community-using-topics) — Trailhead · read 2026-09-24 · the Salesforce Go route, FAQ record type, `Text` field, **Visible to Customer**, **Publish now**, and the claim corrected above

## History

- 2026-09-24 · created from your Trailhead feed (Knowledge & Enhanced Chat site project)
