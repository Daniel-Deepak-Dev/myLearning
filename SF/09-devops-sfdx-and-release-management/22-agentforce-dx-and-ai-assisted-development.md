# Agentforce DX & AI-Assisted Development

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 17

**Scope:** What changes about a pipeline when agents are the artefact and a model writes some of the code. **This note owns the review and governance discipline** — the tool surface and its blast radius are [13](13-dx-mcp-server-and-agent-driven-development.md), and the lifecycle with the `sf agent` command chain is [AI_Data · ADLC](../../AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md). Neither of those covers what happens at the pull request.

## Core idea

Two unrelated things share this heading, and separating them is most of the value. **Agentforce DX** makes an agent a source-controlled artefact — Agent Script in git, authoring bundles deployed by the CLI, evaluations as YAML. **AI-assisted development** means a model is producing code that enters the same repository. The first is a packaging problem and it is largely solved. The second is a *review* problem and it is not.

The governing fact is that generated code arrives at a volume no human produced while the review budget stays exactly what it was. Everything below exists to stop that gap being closed by lowering the standard.

## How it works

- **The agent is source.** Agent Script (Apache 2.0) is committed like any other file; the bundle is generated, validated locally, then deployed, and publishing and activation are separate commands → [AI_Data · ADLC](../../AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md).
- **Evaluations are metadata too.** Scorer definitions deploy as `aiAgentScorerDefinitions`, so agent quality lives in the pipeline rather than in a spreadsheet.
- **Never build in production.** Salesforce's own guidance is scratch orgs or sandboxes only — the same rule as any other metadata, stated explicitly because the agent builders are so reachable from Setup.
- **Require the plan in the pull request.** For generated code, the prompt and the plan are the design document; without them a reviewer is reverse-engineering intent from output.
- **Review for what the model cannot know**: sharing and execution context, guest reachability, whether this duplicates an existing service, and whether the org's limits make the approach viable.
- **An approval in an editor is not a code review.** Accepting a diff in an agentic IDE is authorship, not review — the second pair of eyes still has to be a different pair.
- **Config made by prompt is still config.** Anything an assistant built in a sandbox has to be retrieved and committed, or the next deployment overwrites it → [01-admin · 19](../01-admin-and-declarative-platform/19-agentforce-in-setup-and-ai-assisted-admin.md).

## 2026 currency

The tooling moved faster than the practice. **`sf agent preview` is GA**, **evaluations are Beta**, **Agentforce Vibes 2.0 is Developer Preview**, and the **DX MCP server** puts org-aware tools — including ApexGuru — inside the editor, with **status set per toolset rather than per server** → [13](13-dx-mcp-server-and-agent-driven-development.md), [17](17-apexguru-and-performance-review.md). Two operational details matter more than any of them. **`forcedotcom/sf-skills` ships weekly, on Fridays**, so pin what your team uses rather than tracking `main`. And the **licences differ**: `sf-skills` is Salesforce's supported library, while the `agentforce-adlc` research repo is **CC BY-NC 4.0 and therefore unusable on paid client work** — a compliance question a delivery lead has to answer, not a preference.

## Gotchas

- **MCP has no machine-to-machine flow.** Authorization code only, so an MCP server cannot be a CI service account no matter how convenient that would be → [06-integration · 25](../06-integration-and-apis/25-mcp-servers-and-agent-facing-apis.md).
- **A coding agent with metadata write access is a deployment path around the pipeline.** The DX MCP server reuses your `sf` CLI authorization rather than authenticating separately, so `--orgs` is the real control → [13](13-dx-mcp-server-and-agent-driven-development.md).
- **Generated code passes the linter by construction.** It is idiomatic and well-formatted, which makes it *harder* to review, not easier — the defects are in intent.
- **`retrieve` writes org-controlled bytes into the workspace**, and an agent-driven loop retrieves constantly. The static-resource zip-slip fix is on `source-deploy-retrieve` 13.x only → [14](14-ci-cd-with-github-actions.md).
- **Agent behaviour drifts with no commit behind it.** The model, the data and user phrasing all change; a passing evaluation in March says nothing about July.
- **Bundle validation is not a test.** Agent Script compiling means it is well-formed, not that the agent does the right thing.
- **Test data and prompts leak.** A prompt pasted into a PR description can contain customer data that the repository now retains indefinitely.

## Recall

Q: What does this note own that the ADLC note does not?
A: The review and governance discipline for generated code and agent artefacts — the ADLC note owns the lifecycle and the command chain.

Q: Why can an MCP server not be used as a CI identity?
A: It supports the authorization code flow only; there is no machine-to-machine flow.

Q: What is the licence trap in the ADLC toolchain?
A: `sf-skills` is Salesforce-supported, but the `agentforce-adlc` research repo is CC BY-NC 4.0 — not usable on paid client work.

Q: Why is well-written generated code harder to review?
A: It passes every automated check by construction, so the only remaining defects are in intent — sharing, scope, duplication, and fit with the org's limits.

Q: Where do agent evaluations live so they run in a pipeline?
A: In source, as `aiAgentScorerDefinitions` metadata deployed like any other component.

## Related

- [13 · The DX MCP server & agent-driven development](13-dx-mcp-server-and-agent-driven-development.md) — the tool surface this note governs the output of
- [AI_Data · ADLC & Agentforce DX](../../AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md) — the lifecycle, the `sf agent` commands and the five phases
- [19 · Code review conventions for metadata](19-code-review-conventions-for-metadata.md) — the review protocol this note raises the stakes on
- [06-integration · 25 MCP servers & agent-facing APIs](../06-integration-and-apis/25-mcp-servers-and-agent-facing-apis.md) — the auth model behind every editor-side tool
- [24 · VS Code, Code Builder & tooling](24-vscode-code-builder-and-tooling.md) — where these assistants actually run
