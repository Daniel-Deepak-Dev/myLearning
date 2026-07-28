# Agentforce Coworker — Resources

> **Source note.** `salesforce.com` and `admin.salesforce.com` return HTTP 403 to automated fetching, so those pages were read via search extracts rather than directly — same constraint the radar records in [01-agentforce/2026-07-28.md](../../05-release-radar/01-agentforce/2026-07-28.md). Everything technical below (setup steps, permission sets, limits, billing) comes from `developer.salesforce.com`, which was fetched directly. Prefer it when the two disagree.

## Official docs / Trailhead

**First-party developer guide — the authoritative set:**
- Agentforce Coworker (Beta) — guide home — https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-a-home.html
- About Agentforce Coworker (Beta) — https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-a-about-home.html
- Benefits and Use Cases (Beta) — https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-benefits-and-use-cases.html
- **Turn On Agentforce Coworker (Beta)** — the setup click-path, permission sets, editions — https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-turn-on-infrastructure.html
- **Billing Considerations (Beta)** — seat-based vs usage-based, what's free — https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-billing-considerations.html
- **Limits and Guidelines (Beta)** — the rate limits and ingestion caps; **read this before quoting the "270+ sources" number** — https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-limits-and-guidelines.html

**Product / marketing (secondary — treat claims as aspirational):**
- Introducing Agentforce Coworker — https://www.salesforce.com/agentforce/coworker/
- Meet Your Users' New AI Teammate (Salesforce Admins) — https://admin.salesforce.com/blog/2026/meet-your-users-new-ai-teammate-introducing-agentforce-coworker
- Agentforce for Employees in Slack — the neighbouring product, useful for telling them apart — https://slack.com/blog/news/ai-for-employees-agentforce-slack

## Courses & videos
<!-- No Trailhead module located as of 2026-07-28 — expect one once it leaves Beta. -->

## Articles & repos
- Salesforce Announces Agentforce Coworker: AI 'In Every Search Bar' (Salesforce Ben) — the May 21 announcement in context — https://www.salesforceben.com/salesforce-announces-agentforce-coworker-ai-in-every-search-bar/
- How to Setup Agentforce Coworker (salesforceblogger.com) — walkthrough incl. the Slack-is-federated detail — https://www.salesforceblogger.com/2026/05/10/how-to-setup-agentforce-coworker-a-new-search-experience-for-salesforce/
- What Is Agentforce Coworker? (Salesforce Break) — https://salesforcebreak.com/2026/05/26/agentforce-coworker/

## In this repo
- [Release radar: Agentforce platform](../../05-release-radar/agentforce-platform.md) — the dated entry with sources
- [Agentforce Anatomy](../02-agentforce-anatomy/notes.md) — Service vs Employee Agent, for telling the three apart
- [Multi-Agent Orchestration](../08-multi-agent-orchestration/notes.md) — the specialist agents Coworker routes to
- [Zero copy & BYOL](../../01-data-cloud/06-zero-copy-byol/notes.md) — federation vs ingestion, the same trade-off

## My own artifacts
<!-- labs, gists, dev orgs, scripts you built for this topic -->
<!-- Keep the restricted-user sharing test here — screenshots of what Coworker did and didn't return. -->
