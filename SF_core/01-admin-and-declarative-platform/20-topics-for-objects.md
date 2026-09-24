---
vault: SF_core
area: 01-admin-and-declarative-platform
format: light
level: basic
status: open
gaps: 3
org_checks: 2
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
---
# Topics for Objects

**One line:** A topic is a free-text tag on a record, file or post. **Setup → Topics for Objects** switches tagging on per object and picks the text fields that feed topic suggestions.

**Reach for it when:** users need to group records by theme across objects, or a site has to organise Knowledge articles by topic.

> **From my notes.** "what is salesforce knowledge topics? … what is topics for objects?" — **Corrected:** there is no separate "Knowledge topics" feature. It is Topics for Objects with **Knowledge** ticked, which makes articles taggable, not visible → [Knowledge](../../SF_Service/knowledge.md).

## Key points

- **A topic is one row; each tag is another.** `Topic` holds the name (API 28.0+). `TopicAssignment` links one `TopicId` to one `EntityId` — a record, file or feed item — and `EntityType` names the object.
- **Enable per object:** Setup → **Topics for Objects** → click the object → tick **Enable Topics** → pick fields → **Save**. You need **Customize Application**. Help says topics are on by default for most standard objects.
- **Objects Help lists:** accounts, assets, campaigns, cases, contacts, contracts, files, leads, opportunities, orders, solutions, custom objects and English Knowledge articles.
- **The field selection feeds suggestions.** From the selected text fields combined, "up to three suggestions are made from the first 2,000 characters". Suggestions are English only, and encrypted fields can't be used.
- **Standard objects have a shortcut:** **Use topic suggestions from default fields** uses the object's usual name and description fields. Untick it to choose your own. On a custom object you always choose.
- **Users tag in the Topics component**, which you place on the Lightning record page in Lightning App Builder. They type, pick a suggestion or press Enter to create a new topic.
- **Chatter is optional.** Topics tag records without it. With Chatter on, a topic links to a topic detail page whose **Feed** tab shows posts carrying that topic.
- **Permissions:** Read and Edit on the record, plus **Assign Topics** to add an existing topic or remove one, and **Create Topics** to add a new one. **Edit Topics** renames; **Delete Topics** or Modify All Data deletes.
- **Limits:** up to **100 topics per record**. A closing square bracket `]` isn't allowed in a topic name.
- **Sites reuse the same objects.** A site topic carries the site's `NetworkId` and a `ManagedTopicType` of Navigational, Featured or Content (API 44.0+) → [EC 23](../../SF_Experience_Cloud/23-topics-and-knowledge-on-sites.md).

## Gotchas

- **Enabling topics turns off public tags** on that object's records. Personal tags aren't affected.
- **A topic on a post is not a topic on the record.** Topics on posts in a record's feed aren't copied to the record — add them there too. Files are the exception: a topic on a post with the file attached is added to the file.
- **Enabling is not publishing.** Ticking Knowledge here lets articles be tagged. It makes no article readable by a customer or a guest — the article's channel and access do that → [Knowledge](../../SF_Service/knowledge.md).
- **The field list shapes suggestions only.** Users can still type any topic. A bad field choice gives noisy suggestions, not a blocked tag.

## Gaps to close

- [ ] Are topic names visible to users who can't see the records they tag, for example in a topic list or in search?
- [ ] Which Metadata API type carries the Topics for Objects setting between orgs, and does it carry the suggestion-field selection?
- [ ] Does the Lightning **Topics** component show suggestions from the selected fields, or is that a Salesforce Classic behaviour?

## Confirm in org

- 🚩 On a fresh Developer Edition org, is **Knowledge** already ticked in Topics for Objects? — open Setup → Topics for Objects → Knowledge before touching it.
- 🚩 Unticking **Enable Topics** on an object that has tags: are the `TopicAssignment` rows deleted, or only hidden? — query `TopicAssignment` before and after.

## Hands-on

- [ ] **SF-TOPIC-01** · 20 min · Enable topics on a custom object with one long text field selected, place the **Topics** component on its record page, then save a record with a paragraph of English in that field. **Proves:** the selected field feeds up to three suggestions, and an unselected field feeds none.
- [ ] **SF-TOPIC-02** · 15 min · Give a test user **Assign Topics** but not **Create Topics**, then have them add an existing topic and a brand-new one. **Proves:** reusing a topic and minting one are separate permissions — copy the error verbatim. **Needs:** second user.
- [ ] **SF-TOPIC-03** · 10 min · Tag two Accounts with one topic, then run `SELECT Topic.Name, EntityId, EntityType FROM TopicAssignment WHERE TopicId = '<id>'`. **Proves:** each tag is its own `TopicAssignment` row, pointing at a polymorphic `EntityId`.
- [ ] **SF-TOPIC-04** · 15 min · Untick **Enable Topics** on the object from SF-TOPIC-01, reopen the record and query its `TopicAssignment` rows. **Proves:** what disabling does to existing tags. **Settles:** the second 🚩 in Confirm in org.

## Related

- [SF_Service · Knowledge](../../SF_Service/knowledge.md) — the article object you tick here, and the channels that decide who outside the org can read an article
- [SF_Experience_Cloud · 23 Topics & Knowledge on sites](../../SF_Experience_Cloud/23-topics-and-knowledge-on-sites.md) — what an Aura site builds on this switch: navigational, featured and content topics
- [05 · Dynamic Forms & Lightning App Builder](05-dynamic-forms-and-lightning-app-builder.md) — where the Topics component is placed on a record page
- [16 · Search configuration & Einstein Search](16-search-configuration-and-einstein-search.md) — the other way users find Knowledge: Promoted Search Terms, not tags

## Sources

- [Enable and Configure Topics for Objects in Salesforce Classic](https://help.salesforce.com/s/articleView?id=experience.collab_topics_records_admin.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · the supported-object list; *"up to three suggestions are made from the first 2,000 characters"*; public tags disabled; topic pages need Chatter
- [Configure Topics for Records in Lightning Experience](https://help.salesforce.com/s/articleView?id=experience.collab_topics_records_admin_LEX.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · *"By default, topics are enabled for most standard objects"*; Topics component; no encrypted fields
- [Add and Remove Topics from Records in Lightning Experience](https://help.salesforce.com/s/articleView?id=xcloud.basics_add_remove_topics_records_lex.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · 100 topics per record; `]` unsupported; Create Topics vs Assign Topics; the Feed tab; post topics not copied to the record
- [Topics for Objects](https://help.salesforce.com/s/articleView?language=en_US&id=sf.collab_admin_topics.htm&type=5) — Salesforce Help · via search 2026-09-24 · **Use topic suggestions from default fields** on standard objects
- [Enable Topics for Articles](https://help.salesforce.com/s/articleView?language=en_US&id=sf.knowledge_topics.htm&type=5) — Salesforce Help · via search 2026-09-24 · suggested topics are English only
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `Topic` (`ManagedTopicType`, `NetworkId`) and `TopicAssignment` fields; Create/Edit/Delete/Assign Topics — a Winter '27 build; only fields at API 44.0 or earlier are used
- [Enable and Configure Lightning Knowledge](https://trailhead.salesforce.com/content/learn/projects/build-a-community-with-knowledge-and-chat/add-knowledge-to-the-community-using-topics) — Trailhead · read 2026-09-24 · Topics for Objects → Knowledge → **Enable Topics** + **Title**; the claim corrected above

## History

- 2026-09-24 · created from your Trailhead feed (Knowledge & Enhanced Chat site project)
