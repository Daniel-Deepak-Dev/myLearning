# The DX MCP Server & Agent-Driven Development

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 16

**Scope:** Letting a coding agent drive your org and your project — the Salesforce DX MCP server, its toolsets and its blast radius. Agents *built on* the platform are [06-integration · 25](../06-integration-and-apis/25-mcp-servers-and-agent-facing-apis.md) and `AI_Data/`.

## Core idea

The **Salesforce DX MCP server** (`@salesforce/mcp`) exposes the developer workflow — orgs, metadata, data, users, testing, code analysis, DevOps Center — as MCP tools, so a coding agent can retrieve, deploy, query, run tests and manage work items directly instead of being told what the CLI printed.

Two things make it different from the hosted, org-side MCP servers. It runs **locally**, on your machine, from your project directory. And it **reuses your `sf` CLI authorization** — it does not authenticate separately, so whatever you are logged into is what it can reach. That is the whole security model, and it is why the org allowlist is the first flag you set.

## How it works

```json
{ "mcpServers": { "salesforce-dx": {
    "command": "npx",
    "args": ["-y", "@salesforce/mcp", "--orgs", "DEFAULT_TARGET_ORG",
             "--toolsets", "orgs,metadata,data,testing"] } } }
```

- **`--orgs`** is the allowlist. `DEFAULT_TARGET_ORG` scopes the agent to the org the project is pointed at; naming aliases explicitly is stricter still.
- **`--toolsets`** enables groups rather than everything; **`--tools`** adds a single tool by name.
- **`--allow-non-ga-tools`** is required for anything below GA — and it exists because **status is per toolset, not per server**. The DevOps toolset reached GA in April 2026; the server as a whole is Beta, and several toolsets are Developer Preview.
- **Sibling servers** cover the rest of the surface: **Metadata API Context MCP** (Beta) for accurate metadata generation, **ApexGuru** and **SLDS guideline** tools inside the DX server, **Data 360 MCP** (Developer Preview), **Omnistudio MCP** (Beta). Current status for all of them: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).
- **`sf-skills`** — Salesforce's open-source skills for coding agents (`npx skills add forcedotcom/sf-skills`) — is the knowledge half of the same setup.

## 2026 currency

This is the year the loop closed: **Next-Generation DevOps Center is operated through these tools**, so pipeline work — creating work items, reasoning about conflicts, diagnosing a failed promotion — is an agent-addressable task rather than a UI task → [11](11-devops-center.md). The wider framing Salesforce gives it is *Headless 360*: platform capability exposed as APIs, MCP tools and `sf` commands so that nothing requires a browser. Treat the framing as direction, and the individual tool's GA status as the fact.

## Gotchas

- **Never allowlist production casually, and never allowlist all orgs.** The agent inherits your session; if that session is a system administrator, the tools are a system administrator.
- **`--allow-non-ga-tools` opts into churn.** Developer Preview tools change shape without notice and are not supported — fine for a scratch org, wrong for anything a colleague depends on.
- **Retrieve is not read-only.** MCP-driven retrieves run the same conversion path that carried a zip-slip until SDR 13.0.1, so the tool version matters as much as the prompt → [05](05-metadata-api-and-deployment-mechanics.md).
- **This is not the machine-to-machine story.** Hosted MCP servers use authorization code only and have no service-account flow; the DX server sidesteps the question by being your session, which is not the same as solving it → [06-integration · 25](../06-integration-and-apis/25-mcp-servers-and-agent-facing-apis.md).
- **Generated metadata obeys the same rules as hand-written metadata.** It still has to be covered, deployable and activated → [12](12-metadata-coverage-and-manual-steps.md).
- **An agent that can deploy can also delete.** Destructive changes and `project delete source` are ordinary tool calls; scope the toolsets rather than trusting the prompt.
- **Local MCP is a local dependency.** `npx -y` fetches at start-up, so a locked-down CI runner or an offline laptop simply has no server.

## Recall

Q: How does the DX MCP server authenticate to an org?
A: It does not — it reuses the existing `sf` CLI authorization, so the allowlist passed to `--orgs` is the real access control.

Q: Why does `--allow-non-ga-tools` exist?
A: Because maturity is per toolset. DevOps tools reached GA in April 2026 while the server overall is Beta and several toolsets are Developer Preview.

Q: What changed about DevOps Center in relation to MCP?
A: Next-Generation DevOps Center exposes its work-item, conflict and deployment-failure tooling through the DX MCP server, making pipeline work agent-addressable.

Q: Why is an MCP-driven retrieve a security-relevant action?
A: It writes org-controlled bytes to local disk through the same conversion path that carried a zip-slip until SDR 13.0.1.

Q: Does the DX MCP server provide a machine-to-machine integration path?
A: No. It runs as your authenticated user; hosted MCP servers support authorization code only and have no service-account flow.

## Related

- [11 · DevOps Center](11-devops-center.md) — the pipeline these tools now drive
- [12 · Metadata coverage & manual steps](12-metadata-coverage-and-manual-steps.md) — the rules generated metadata still obeys
- [06-integration · 25 MCP servers & agent-facing APIs](../06-integration-and-apis/25-mcp-servers-and-agent-facing-apis.md) — the org-side, hosted counterpart
- [22 · Agentforce DX & AI-assisted development](22-agentforce-dx-and-ai-assisted-development.md) — reviewing what the agent produced
