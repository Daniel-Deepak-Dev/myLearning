# ADLC & Agentforce DX — Resources

> **Source note.** `developer.salesforce.com` fetches cleanly and is the authority for the workflow, commands and skill names in this topic. `architect.salesforce.com` and `salesforce.com` return HTTP 403 to automated fetching — open those in a browser. Where the architect framing (five phases) and the developer blog (the concrete command sequence) describe the same lifecycle differently, they are complementary, not contradictory: one is the model, the other is the implementation.

## Official docs / Trailhead

**The two that matter most:**
- **Master the Agentic Development Lifecycle for Agentforce** (Developers Blog, June 24 2026) — the command-by-command workflow, the three skills, the five workflow rules — https://developer.salesforce.com/blogs/2026/06/master-the-agentic-development-lifecycle-for-agentforce
- **The Agent Development Lifecycle: From Conception to Production** (Architect fundamentals) — the five-phase framework — https://architect.salesforce.com/docs/architect/fundamentals/guide/agent-development-lifecycle.html

**Supporting:**
- Agentforce DX — developer guide — https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx.html
- Agent Development Lifecycle product page — https://www.salesforce.com/agentforce/agent-development-lifecycle/
- Exploring the Agentforce Development Lifecycle (Salesforce blog) — https://www.salesforce.com/blog/exploring-the-agentforce-development-lifecycle/
- Salesforce CLI release notes — ships weekly — https://github.com/forcedotcom/cli/blob/main/releasenotes/README.md
- Agentforce Vibes Workshop — https://developer.salesforce.com/workshops/agentforce-vibes-workshop/explore-agentforce-vibes/overview
- New in Developer Edition: Agentforce Vibes IDE, Claude 4.5, MCP (April 2026) — https://developer.salesforce.com/blogs/2026/04/new-developer-edition-agentforce-vibes-claude-mcp

## Courses & videos
- Explore Agentforce Vibes: Enhancing Developer Productivity (Trailhead) — https://trailhead.salesforce.com/content/learn/modules/einstein-for-developers/get-to-know-einstein-for-developers
- Build a Decision-Scoring Skill for Any Agent (Developers Blog, June 16 2026, Dave Norris) — a worked skill, useful as a template. _URL not captured; find it in the [June 2026 blog archive](https://developer.salesforce.com/blogs)._

## Articles & repos

**Repos — check the licence on each before use:**
- [`forcedotcom/sf-skills`](https://github.com/forcedotcom/sf-skills) — Salesforce's skill library; `npx skills add forcedotcom/sf-skills`. Includes [developing](https://github.com/forcedotcom/sf-skills/tree/main/skills/developing-agentforce), [testing](https://github.com/forcedotcom/sf-skills/tree/main/skills/testing-agentforce), [observing](https://github.com/forcedotcom/sf-skills/tree/main/skills/observing-agentforce)
- [`SalesforceAIResearch/agentforce-adlc`](https://github.com/SalesforceAIResearch/agentforce-adlc) — **CC BY-NC 4.0, non-commercial, research-grade.** Verify activity via [commits/main.atom](https://github.com/SalesforceAIResearch/agentforce-adlc/commits/main), not the Updated column
- [`salesforce/agentscript`](https://github.com/salesforce/agentscript) — parser, linter, compiler, LSP. Apache 2.0
- [agentskills.io](https://agentskills.io/home) — the open skill format itself

**Commentary:**
- Salesforce Tackles the Entire Agent Development Lifecycle (ISG) — the analyst read — https://research.isg-one.com/analyst-perspectives/salesforce-tackles-the-entire-agent-development-lifecycle
- Applied AI: Why Building AI Agents Requires a New Playbook (Salesforce) — https://www.salesforce.com/news/stories/applied-ai-building-agents-playbook/
- ADLC vs SDLC (Atlan) — vendor-neutral framing of the same shift — https://atlan.com/know/ai-agent/adlc-vs-sdlc/

## In this repo
- [Observability & Testing](../09-observability-and-testing/notes.md) — **the tools this lifecycle uses**; don't duplicate them here
- [Agent Script](../07-agent-script/notes.md) — the artifact being versioned
- [Release radar: developer tooling & APIs](../../05-release-radar/developer-tooling-and-apis.md) — CLI, Vibes, Agent Skills, dated
- [Capstone: MCP server for Salesforce](../../04-capstone/01-mcp-server-salesforce/notes.md) — the cross-track build
- [Claude CCA track](../../03-claude-cca/) — same skill format, other side of the seam

## My own artifacts
<!-- labs, gists, dev orgs, scripts you built for this topic -->
<!-- Keep here: the design-interview transcript from the first plan-mode run, and the before/after of one
     full outer-loop pass (production trace → failure pattern → fix → redeploy). That pass is the
     demonstrable deliverable for a client conversation. -->
