# Quickstart Links — Agentforce & Data 360

> Fastest path from zero to hands-on. Curated, not exhaustive — every link here is one you'd actually open in week 1.
> Current to **Summer '26 (API 67.0)** as of **2026-07-28**. Read [Before you click anything](#before-you-click-anything) first — it saves you from studying a retired product.

---

## Before you click anything

Two renames/retirements make most search results wrong. Check these before trusting any tutorial:

| What changed | What it means for your search results |
|---|---|
| **Data Cloud → Data 360** | A real rename (SKUs, docs, the cert). URLs still say `data-cloud` and redirect — that's fine. Content calling it "Customer 360 Audiences" is two names stale. |
| **Agent Script replaced topics-and-instructions** | Since **July 13, 2026** the *New Agent* button no longer opens the legacy builder. **Any tutorial that starts by "adding a Topic" is teaching a retired model.** Check the publication date — if it's before mid-2026, assume it's legacy. |
| **Einstein Copilot is gone** | Folded into Agentforce. A source treating Copilot as current is out of date. |

Rule of thumb: **anything published before 2026 teaches the old builder.** Prefer `developer.salesforce.com/docs` and the release notes over blog posts.

---

## Day 1 — three links, in this order

1. **[Free Developer Edition org](https://developer.salesforce.com/free-trials)** — includes Agentforce **and** Data 360 out of the box, free, doesn't expire as long as you log in every 45 days. Also ships Agentforce Vibes IDE, Claude models, and Salesforce Hosted MCP servers. *Do this before reading anything — every link below is better with an org open in another tab.*
2. **[Agentforce Developer Center](https://developer.salesforce.com/developer-centers/agentforce)** — the single best hub. Quick starts ("Build a Service Agent", "Prompt Builder") are ~100 points each and get you a working agent in under an hour.
3. **[Data 360 Learning Journey](https://trailhead.salesforce.com/data-cloud-trail)** — Trailhead's official 3-part progression (foundation → hands-on → advanced). Start here rather than picking modules at random.

---

## Agentforce — fastest path

### Get it working (hands-on first)
- [Quick Start: Build a Service Agent](https://developer.salesforce.com/developer-centers/agentforce) — via the dev center; first working agent
- [Get Hands-On with Agentforce](https://trailhead.salesforce.com/users/strailhead/trailmixes/first-agentforce) — official Trailhead trailmix
- [Learn to Develop Agents with Agentforce DX Tools](https://trailhead.salesforce.com/content/learn/projects/create-an-agent-using-pro-code-tools/get-started-with-agentforce-dx) — the pro-code path (CLI + VS Code). As a dev, go here early; clicking through Builder teaches you less.
- [Agentforce Builder tour](https://help.salesforce.com/s/articleView?id=ai.agent_builder_tour.htm&type=5) — UI orientation

### Understand it (docs, in reading order)
- [Agent Script guide](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-script.html) — **the** doc. Agent Script *is* how agents are authored now.
- [Agent Script model reference](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-model.html) — pinning a model per agent (a cost/latency decision)
- [Einstein Trust Layer architecture](https://help.salesforce.com/s/articleView?id=ai.generative_ai_trust_arch.htm&language=en_US&type=5) — masking, grounding, audit; heavily tested
- [Prompt Builder](https://help.salesforce.com/s/articleView?id=ai.prompt_builder_general.htm&type=5)
- [Multi-agent orchestration](https://help.salesforce.com/s/articleView?id=ai.agent_multi_orch.htm&type=5) — GA since Summer '26; subagent **descriptions** are the routing contract
- [Agentforce Testing Center](https://help.salesforce.com/s/articleView?id=ai.agent_studio_testing_center_setup_tests.htm&type=5) — evals; the part most people skip and then regret

### Repos & tooling
- [salesforce/agentscript](https://github.com/salesforce/agentscript) — Apache 2.0 toolchain, real examples
- [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills) — official Claude Code skills; see [`developing-agentforce`](https://github.com/forcedotcom/sf-skills/tree/main/skills/developing-agentforce), [`testing-agentforce`](https://github.com/forcedotcom/sf-skills/tree/main/skills/testing-agentforce), [`observing-agentforce`](https://github.com/forcedotcom/sf-skills/tree/main/skills/observing-agentforce)
- [Agentforce Vibes IDE (VS Code)](https://marketplace.visualstudio.com/items?itemName=salesforce.salesforcedx-agentforce-vibes-2)

---

## Data 360 — fastest path

### Get it working
- [Data 360 Learning Journey](https://trailhead.salesforce.com/data-cloud-trail) — the 3-part official progression
- [Data 360: Explore Setup to Activation](https://trailhead.salesforce.com/content/learn/trails/data-cloud-explore-setup-to-activation) — end-to-end trail: ingest → model → resolve → segment → activate
- [Connect Data Cloud to Agentforce and Prompt Builder](https://developer.salesforce.com/developer-centers/agentforce) — the module that joins the two tracks

### Understand it (docs)
- [Identity resolution](https://help.salesforce.com/s/articleView?id=sf.c360_a_identity_resolution.htm&type=5) — match/reconcile rules; the concept most exam questions hinge on
- [Calculated insights](https://help.salesforce.com/s/articleView?id=sf.c360_a_calculated_insights.htm&type=5)
- [Data 360 release notes (rolling)](https://help.salesforce.com/s/articleView?id=data.c360_a_dc_releases.htm&type=5) — Data 360 ships continuously, not just per-release
- [Zero-copy / BYOL overview](https://www.salesforce.com/data/connectivity/zero-copy/) — the "don't move the data" story
- [Data 360 MCP server (developer preview)](https://developer.salesforce.com/blogs/2026/05/introducing-the-data-360-mcp-server-developer-preview)

### DSO/DLO/DMO in one sitting
The three-letter object soup is the single biggest early blocker. Your notes cover it: [01-data-cloud/03-data-modeling-dso-dlo-dmo/cheatsheet.md](01-data-cloud/03-data-modeling-dso-dlo-dmo/cheatsheet.md) — read that before the Trailhead modules and they'll go twice as fast.

### Code path (skip until week 2+)
- [Data Cloud custom code SDK](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/set-up-sdk.html) · [`salesforce-data-customcode` on PyPI](https://pypi.org/project/salesforce-data-customcode/)
- [Data 360 ↔ Databricks file sharing (public preview)](https://www.databricks.com/blog/announcing-public-preview-salesforce-data-360-file-sharing-unity-catalog)

---

## Where the two actually meet

This is the part worth learning properly — **Agentforce without Data 360 grounding is a polite chatbot.**

- [Data Library / retrievers](https://help.salesforce.com/s/articleView?id=ai.agent_data_library.htm&type=5) — how unstructured data becomes groundable
- [Semantic layer for AI agents](https://www.salesforce.com/blog/semantic-layer-ai-agents-data-360/) — why agents need modeled meaning, not raw tables
- [Headless 360: what it means for developers](https://developer.salesforce.com/blogs/2026/05/headless-360-what-it-means-for-developers) — the Summer '26 organizing idea: every capability = API, MCP tool, or CLI command
- [Headless 360 MCP server (beta)](https://developer.salesforce.com/blogs/2026/07/announcing-the-headless-360-mcp-server-beta)
- [Connect Claude with Salesforce-hosted MCP servers](https://developer.salesforce.com/blogs/2026/05/connect-claude-with-salesforce-hosted-mcp-servers) — bridges straight into your [03-claude-cca/](03-claude-cca/INDEX.md) track

---

## Certifications

| Cert | Page | Prep |
|---|---|---|
| **Data 360 Consultant** (`Data-Con-101`) | [credentials/data360consultant](https://trailhead.salesforce.com/credentials/data360consultant) | [Prep trail](https://trailhead.salesforce.com/content/learn/trails/prepare-for-your-salesforce-data-360-consultant-exam) · [Exam guide](https://trailhead.salesforce.com/help?article=Salesforce-Certified-Data-Cloud-Consultant-Exam-Guide) |
| **Agentforce Specialist** | [credentials/agentforcespecialist](https://trailhead.salesforce.com/credentials/agentforcespecialist) | [Cert prep module](https://trailhead.salesforce.com/content/learn/modules/cert-prep-agentforce-specialist/get-started-with-salesforce-agentforce-specialist-certification-prep) |

~60 questions / 105 min / ~62% to pass / ~$200 for Data 360 Consultant. Note the Agentforce Specialist exam now includes **Multi-Agent Interoperability (~5%)** — MCP, A2A, Agent API. Detail lives in [_cert-data-cloud-consultant/](01-data-cloud/_cert-data-cloud-consultant/) and [_cert-agentforce-specialist/](02-salesforce-ai/_cert-agentforce-specialist/).

---

## Staying current

Both products move faster than any book. Four sources are enough:

- [Salesforce Summer '26 release notes](https://help.salesforce.com/s/articleView?id=release-notes.salesforce_release_notes.htm&language=en_US&release=262&type=5) — the primary source
- [The Salesforce Developer's Guide to the Summer '26 Release](https://developer.salesforce.com/blogs/2026/06/the-salesforce-developers-guide-to-the-summer-26-release) — the dev-relevant 10%
- [Agentforce — what's new](https://www.salesforce.com/agentforce/what-is-new/)
- [Salesforce AI Research](https://www.salesforceairesearch.com/) · [GitHub org](https://github.com/SalesforceAIResearch) — where next year's features are published this year

Your own running log is [05-release-radar/](05-release-radar/README.md) — check it *before* searching the web; it already has the story with sources.

---

## Suggested first week

| Day | Do this |
|---|---|
| 1 | Sign up for the [Developer Edition org](https://developer.salesforce.com/free-trials). Build the Quick Start service agent. Don't read theory yet. |
| 2 | [Agent Script guide](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-script.html) end to end, then rebuild day 1's agent in Agent Script. |
| 3 | [Data 360 Learning Journey](https://trailhead.salesforce.com/data-cloud-trail) part 1 + your [DSO/DLO/DMO cheatsheet](01-data-cloud/03-data-modeling-dso-dlo-dmo/cheatsheet.md). |
| 4 | Ingest a CSV → model it → run identity resolution in your org. The concepts only stick once you've watched a unified profile form. |
| 5 | [Data Library / retrievers](https://help.salesforce.com/s/articleView?id=ai.agent_data_library.htm&type=5) — ground day 2's agent in day 4's data. **This is the whole game in one exercise.** |
| 6 | [Trust Layer](https://help.salesforce.com/s/articleView?id=ai.generative_ai_trust_arch.htm&language=en_US&type=5) + [Testing Center](https://help.salesforce.com/s/articleView?id=ai.agent_studio_testing_center_setup_tests.htm&type=5). |
| 7 | Write it up: distill into the relevant `cheatsheet.md` files, log the week in [journal/](journal/). |

---

## Related in this repo

- [README.md](README.md) — how the study base is organized
- [STUDY-PLAN.md](STUDY-PLAN.md) — 26-week phase → folder map
- [GLOSSARY.md](GLOSSARY.md) — 106 terms, marked for currency
- [01-data-cloud/INDEX.md](01-data-cloud/INDEX.md) · [02-salesforce-ai/INDEX.md](02-salesforce-ai/INDEX.md)
- [02-salesforce-ai/01-landscape/cheatsheet.md](02-salesforce-ai/01-landscape/cheatsheet.md) — the whole Salesforce AI landscape in half a page; read it first if you want the map before the territory
