# Capstone: MCP Server for Salesforce

> Track: Capstone · Roadmap: Phase 05 · Weeks 21–26 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/developer-tooling-and-apis.md](../../05-release-radar/developer-tooling-and-apis.md)

**Roadmap scope:** Expose SOQL queries, record actions, and metadata reads as MCP tools so Claude (and Claude Code) can work against a real org safely.

> ⚠️ **The premise of this project changed in Summer '26.** Salesforce **hosted MCP servers went GA**. Building a server from scratch against the REST API — the original plan — now demonstrates less than choosing correctly between three options and justifying it. Read the next section before starting.

## What is it?

The project is no longer *"build an MCP server"*. It's:

> **Connect Claude to a Salesforce org safely — then justify which of three architectures you chose and why.**

That's a better project. It's the actual decision an architect gets asked to make, and the reasoning is what a client or an interviewer will probe.

### The three options

| Option | What it is | Enforces org sharing/FLS? |
|---|---|---|
| **Standard hosted** (GA) | Salesforce-hosted: SObject CRUD + SOQL + search, Data 360, Tableau | **Yes** |
| **Custom hosted** | Salesforce-hosted, you choose the tools exposed | **Yes — full sharing and security model** |
| **Self-hosted** | Your own server against the REST API | **Only what you implement** |

Every connection uses standard OAuth. Salesforce hosts the first two, so there's no infrastructure to run.

**Custom hosted servers can expose tools built from:** Apex `@InvocableMethod` actions, autolaunched Flows, Apex REST endpoints, `@AuraEnabled` methods, the **Named Query API** (parameterized SOQL as a tool), Prompt Builder templates (as MCP prompts), whole **Agentforce agents**, and curated API Catalog endpoints.

## Why it matters (for the AI-Salesforce architect role)

**The security argument is the whole point, and it's what makes this a portfolio piece rather than a demo.**

Custom hosted MCP servers **respect the org's full sharing and security model**. A server you build yourself enforces exactly what you remembered to implement — and getting FLS, sharing rules, and polymorphic field access right in hand-written code is genuinely hard. Under API 67.0's user-mode defaults, the platform does it for you.

So the interesting inversion: **instead of building an MCP server to *reach* Salesforce, you configure one and Salesforce enforces sharing and FLS for you.**

**When self-hosting is still the right answer** — and being able to say this is what makes the argument credible rather than dogmatic:

- You need tools that compose across Salesforce *and* other systems in one call
- You need custom caching, rate-limiting or transformation logic
- The client can't or won't route through Salesforce-hosted infrastructure
- You're building something Salesforce's tool-construction options can't express

If none of those apply, self-hosting is a liability you chose.

## How it works

### Recommended shape for the capstone

1. **Start with a standard SObject server** — connect Claude Desktop or Claude Code to a Dev Edition org. Prove the OAuth flow works end to end.
2. **Add a custom hosted server** exposing one `@InvocableMethod` as a tool. This single exercise covers both the CCA-F and Agentforce tracks.
3. **Write the decision record** — the three options, your choice, and the criteria. *This is the actual deliverable.*
4. **Optional, for depth:** build a small self-hosted server too, and demonstrate concretely what you had to implement yourself that the hosted one gave you free. That comparison is the strongest thing you can put in a write-up.

### Tool design — steal the facade pattern

The **Data 360 MCP server** fronts roughly **200 REST operations** with **three tools** rather than exposing 200:

| Tool | Purpose |
|---|---|
| `search` | find a capability by intent |
| `payload_examples` | fetch a working request body |
| `execute` | run it |

**This is the canonical answer to context-window blowout in MCP design.** A flat tool list of 200 entries consumes the context window before the model does any work. Apply it if your server covers a broad surface — and cite it in the write-up, because it shows you understand tool design and not just tool plumbing.

The same principle appears in the **Headless 360 MCP Server**, which exposes ~100 admin-facing *skills* rather than thousands of flat tools.

### Safety rails to demonstrate

| Rail | Why |
|---|---|
| Read-only by default; writes opt-in | An agent retrying a write can double it |
| Idempotent write tools | Timeout + retry is normal agent behaviour |
| Narrow tool descriptions with exclusions | Descriptions drive selection — same principle as agent actions |
| Least-privilege connected user | Under user mode, the running user *is* the access control |
| Audit what the agent did | "Which agent changed this record?" will be asked |

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Connect Claude Code to a Dev org via a **standard SObject server**.
- [ ] Expose one `@InvocableMethod` through a **custom hosted server** and call it from Claude.
- [ ] Test the sharing model: connect as a restricted user and confirm the agent sees less. **Screenshot this** — it's the most persuasive artifact in the project.
- [ ] Build a facade-tool server over a broad API surface.
- [ ] Write the decision record comparing all three options.

## Gotchas & sharp edges

- **Don't build what's already GA.** Hand-rolling SObject CRUD when the standard server does it is a weaker portfolio piece, not a stronger one.
- **A self-built server enforces only what you implemented.** Sharing, FLS and polymorphic fields are all easy to get subtly wrong.
- **Who can create custom hosted MCP servers?** They expose org data to external AI clients. That's a security-review question, not a developer preference — raise it.
- **A flat tool list blows the context window.** Use a facade over a broad surface.
- **Make write tools idempotent.** Agents retry.
- **Least-privilege the connected user.** At 67.0, that user's permissions are the enforcement boundary.
- **Tool descriptions drive selection** — write them like prompts, with exclusions, exactly as for [agent actions](../../02-salesforce-ai/05-custom-agent-actions/notes.md).

## Related topics

- [Custom Agent Actions](../../02-salesforce-ai/05-custom-agent-actions/notes.md) — `@InvocableMethod` as an MCP tool
- [MCP (Claude track)](../../03-claude-cca/05-mcp/notes.md) — protocol fundamentals
- [Data 360 DevOps](../../01-data-cloud/09-data-360-devops/notes.md) — the facade pattern in detail
- [Einstein Trust Layer](../../02-salesforce-ai/04-einstein-trust-layer/notes.md) — why more paths in means more control-point pressure
- [Write-up & pitch](../04-writeup/notes.md) — where the decision record lands
- [Release radar: developer tooling and APIs](../../05-release-radar/developer-tooling-and-apis.md)
