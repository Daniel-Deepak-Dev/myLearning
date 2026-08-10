# Data 360 DevOps

> Track: Data 360 · Roadmap: Phase 02 · Weeks 5–8 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/data-360.md](../../05-release-radar/data-360.md)

**Scope:** Code Extension (Python in Data 360), data kits, `@IntegrationTest`, and the Data 360 MCP server — the tooling that lets Data 360 work move through a pipeline instead of being clicked into production.

> **Why this folder exists.** Data 360's developer surface grew substantially in Summer '26. Until then, "Data Cloud DevOps" was mostly a gap you apologized for. It isn't anymore.

## What is it?

Four capabilities that together make Data 360 configuration behave like software:

| Capability | Status | What it does |
|---|---|---|
| **Code Extension** | Summer '26 | Deploy custom **Python** to isolated containers on the platform |
| **Data kits** | Summer '26 | Promote code extensions and data transforms sandbox → production |
| **`@IntegrationTest`** | Dev Preview | Apex tests with live callouts and mid-transaction commits |
| **Data 360 MCP server** | Dev Preview | Connect a coding agent to Data 360 |

## Why it matters (for the AI-Salesforce architect role)

**"How do we promote this between orgs?" used to be the awkward question in a Data Cloud design review.** Apex and LWC had a mature DevOps story; Data Cloud configuration largely didn't. Data kits close that gap — a data transform added to a data kit **automatically pulls in its associated code extension**, so lakehouse logic promotes the same way metadata does.

**Code Extension matters most for RAG.** Its headline use is **custom chunking logic on search index creation** — and chunking is usually the single biggest lever on retrieval quality. Until now it was a black box. See [vector DB & unstructured](../07-vector-db-unstructured/notes.md).

**And note the permission model**, because it's a deliberate design choice worth repeating in a governance conversation: developers **author** the code; users with the **Data Cloud Architect** permission set **run and monitor** it. Author ≠ operator, enforced by the platform rather than by convention.

## How it works

### Code Extension

Custom **Python** scripts and functions running in isolated containers. Current supported uses:

- Functions for complex **batch data transformations** — string manipulation, custom computations, data cleansing
- Scripts implementing **custom chunking logic** on search index creation

Salesforce says other capabilities and languages will follow.

**Workflow:**

```
author + debug locally
   ← project scaffold from the Data Custom Code Python SDK
   ← Salesforce CLI Code Extension plugin
        │
   validate against a sandbox (CLI)
        │
   deploy → run
        │
   monitor via the code extensions log DLO
```

Salesforce recommends pairing the [code extension Agent Skill](https://github.com/forcedotcom/sf-skills/tree/main/skills/developing-datacloud-code-extension) with the Data 360 MCP server to automate the build/debug/deploy loop — which is a neat instance of using an AI coding agent to build the thing that grounds AI agents.

### Data kits

A **data kit** is a container for Data 360 metadata — the thing you put components into before packaging them. A package can hold more than one. **There are two kinds, and confusing them is the mistake worth avoiding:**

| | DevOps data kit | Standard data kit |
|---|---|---|
| Purpose | Migrate metadata sandbox → production | Package a solution to share or distribute |
| Created from | Any data space | The **default** data space |
| Deploys to | The **same** data space in the target org | **Any** data space in the target org |
| Typical author | Whoever runs the pipeline | A partner, or an internal team building a reusable asset |

A **DevOps data kit** moves code extensions — or the data transforms built from them — from sandbox to production. Adding such a transform to a data kit automatically pulls in its associated code extension, so you don't hand-track the dependency.

A **standard data kit** is the packaging path. Wrapped in a **managed package**, it's how partners ship Data 360 solutions on **AppExchange** — data streams, batch data transforms, calculated insights and data graphs land in the subscriber org via Package Manager. Note the constraint: **all Data 360 feature metadata in a managed package is locked.** Subscribers can add new entities alongside what you shipped, but cannot modify it. A calculated insight whose definition was slightly wrong is a new package version, not a five-minute fix.

**The architect's question is which one you're building** — a one-off promotion, or a reusable accelerator. The data-space rule forces the answer early: a DevOps kit pinned to one data space doesn't quietly become a distributable asset later.

### `@IntegrationTest` (Developer Preview)

Allows **live callouts** and mid-transaction data commits via `IntegrationTest.commitTestOnly()`, with cleanup in a `@TearDown` method. Standard unit tests mock every callout and roll everything back, which makes asserting on real Data 360 or Agentforce behaviour impossible.

**Constraints:** scratch orgs only; add `ApexIntegrationTests` to the `features` array in the scratch org definition; tests run asynchronously, one at a time, via the Tooling API `runTestsAsynchronous` resource.

Be honest about the first constraint — **scratch-org-only keeps it out of most real pipelines for now.** It's the beginning of an answer to "you can't really test it", not the whole answer.

### The Data 360 MCP server — and the design lesson

An open-source MCP server connecting a coding agent to Data 360. **The design choice is worth studying on its own**, independent of Data 360.

Rather than exposing roughly **200 REST operations as 200 tools**, it fronts them with **three facade tools**:

| Tool | Purpose |
|---|---|
| `search` | find a capability by intent |
| `payload_examples` | fetch a working request body |
| `execute` | run it |

**This is the canonical answer to context-window blowout in MCP design:** a searchable facade over a large API surface instead of a flat tool list. Directly transferable if you build your own MCP servers — see [the capstone MCP project](../../04-capstone/01-mcp-server-salesforce/notes.md) and [MCP in the Claude track](../../03-claude-cca/05-mcp/notes.md).

There is also a **Data 360 standard hosted MCP server (GA)** for queries and graph traversal — different thing, different purpose. The Dev Preview one is for *coding agents building Data 360 things*; the GA hosted one is for *agents querying Data 360 data*.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

**→ [lab-07](../10-lab-environment/labs/lab-07-promotion-and-packaging.md)** — retrieve Data 360 metadata with the CLI and find out what *doesn't* come back. That list is the manual-steps section of every promotion runbook you'll write.

- [ ] Install the Python SDK and CLI plugin, scaffold a project, deploy a trivial Code Extension.
- [ ] Write a custom chunking extension that splits on document headings.
- [ ] Promote it between orgs with a data kit and confirm the dependency was pulled in automatically.
- [ ] Connect the Data 360 MCP server to Claude Code and use it to build/debug an extension.
- [ ] Write one `@IntegrationTest` in a scratch org against a real Data 360 callout.

## Gotchas & sharp edges

- **`@IntegrationTest` is scratch-org only**, async, one at a time. Don't design a CI pipeline around it yet.
- **Author ≠ operator.** Running and monitoring needs the Data Cloud Architect permission set. Plan for both roles.
- **Monitor via the code extensions log DLO** — that's where failures surface; they aren't obvious otherwise.
- **Python only, for now.** Other languages are promised, not shipped.
- **Two different Data 360 MCP servers** — Dev Preview (for coding agents) and GA hosted (for querying data). Don't conflate them in a design doc.
- **Data kits pull dependencies automatically**, which is convenient and also means you should check what came along.
- **Custom chunking changes require re-indexing**, which is expensive on a large corpus. Get it approximately right first.

## Related topics

- [Vector DB & unstructured](../07-vector-db-unstructured/notes.md) — custom chunking, the main use case
- [Data modeling](../03-data-modeling-dso-dlo-dmo/notes.md) — what data transforms operate on
- [Capstone: MCP server](../../04-capstone/01-mcp-server-salesforce/notes.md) — the facade-tool pattern, applied
- [Observability & testing](../../02-salesforce-ai/09-observability-and-testing/notes.md) — the agent-side equivalent
- [Release radar: Data 360](../../05-release-radar/data-360.md) · [developer tooling and APIs](../../05-release-radar/developer-tooling-and-apis.md)
