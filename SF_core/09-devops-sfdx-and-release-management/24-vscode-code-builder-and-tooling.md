# VS Code, Code Builder & Tooling

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 17

**Scope:** Where a Salesforce developer actually sits, and which of the names in older material still refer to a live product. The component-authoring loop is [03-lwc · 21](../03-lwc-and-slds/21-local-dev-and-lightning-dev-server.md); installing and configuring the CLI is [01](01-sf-cli-v2-fundamentals.md).

> **What changed.** **Code Builder is now Agentforce Vibes IDE** — same browser-hosted VS Code, renamed. And the mirror-image error is just as common: the **Developer Console carries a *legacy* label in the docs but has no announced retirement date** and still works. Two failure modes, one page: calling a renamed product by a dead name, and calling a labelled-legacy product retired.

## Core idea

There is no single answer to "which IDE", and the reason is entitlement rather than taste. Salesforce now ships three environments with **different org coverage**, and the right recommendation for a client depends on which editions and clouds they run — which is a governance question that arrives disguised as a developer-preference question.

Underneath all three is the same thing: the **Salesforce Extensions for VS Code**, driving the same CLI against the same Metadata API. Choosing an environment changes where the process runs, not what it can do.

## How it works

- **Salesforce Extension Pack** (and *Expanded*) is the desktop baseline — Apex language server, LWC support, org browser, CLI integration, published to both the VS Code Marketplace and Open VSX.
- **Agentforce Vibes IDE** — browser-hosted, cloud-run VS Code launched from Setup, fully authenticated to the org, no local install. The same Salesforce extensions as the desktop.
- **Agentforce Vibes** the *extension* ships inside the Extension Pack, so the agentic assistant is available on the desktop too → [22](22-agentforce-dx-and-ai-assisted-development.md).
- **Web Console (Beta)** — an IDE inside the org itself, in open beta from **14 April 2026**, enabled at Setup → Development. Apex, LWC, anonymous Apex, trace flags and debug levels in one place; **Salesforce-provided extensions only**.
- **Coverage is the differentiator.** Web Console works across orgs and editions on admin opt-in; **Agentforce Vibes excludes Professional Edition, Government Cloud, the EU Operating Zone, FedRAMP High and China Cloud**. For those, Web Console is the answer.
- **Two debuggers.** Apex **Replay** Debugger is free and reads a log → [21](21-observability-logging-and-prod-debugging.md); the **Interactive** debugger is licensed and sandbox-only.
- **Every Developer Edition org has included Agentforce Vibes IDE, Claude Sonnet 4.5 as the default coding model, and Salesforce Hosted MCP Servers at no cost since April 2026** — which makes the free org the honest place to evaluate all of this.

> **From my notes** — the [inventory](../_notion-seed/INVENTORY.md) line only; the note body is not in the vault. A 2019 page listing VS Code and Chrome extensions is the most perishable kind of note in the vault — the CLI it was written against has been replaced, and so has half the list. One thing in it has not aged: a browser extension that reads your org **has your session**. That is a security decision made once per developer and never reviewed → [07-security · 18](../07-security-and-sharing/18-session-security-login-policies-and-step-up.md).

## Gotchas

- **Same extensions ≠ same environment.** Web Console permits only Salesforce-provided extensions, so a team standard built on third-party ones does not transfer.
- **A cloud IDE still needs the org's session policy to permit it.** IP restrictions and login-hours policies apply to the browser-hosted environments too.
- **Anything called *Local Dev* in a 2024 note is the Live Preview extension now** → [03-lwc · 21](../03-lwc-and-slds/21-local-dev-and-lightning-dev-server.md).
- **The Metadata Visualizer is Beta and partial** — objects, permission sets and flexipages. Useful; not an org diagram.
- **Beta means no upgrade guarantee.** Standardising a team on Web Console today is a decision to re-evaluate at GA.
- **The extension pack pins nothing.** It updates independently of the CLI version your pipeline pinned, so a developer and CI can disagree about a deploy → [14](14-ci-cd-with-github-actions.md).

## Recall

Q: What is Code Builder called now?
A: **Agentforce Vibes IDE** — the browser-hosted VS Code environment, renamed.

Q: Is the Developer Console retired?
A: No. It is labelled *legacy* in the documentation, with no announced retirement date.

Q: When would you recommend Web Console over Agentforce Vibes?
A: When the org is outside Vibes' coverage — Professional Edition, Government Cloud, the EU Operating Zone, FedRAMP High or China Cloud.

Q: Which Apex debugger costs nothing?
A: The Apex Replay Debugger, which replays a captured debug log; the Interactive debugger is licensed and sandbox-only.

Q: What does a Developer Edition org include for free since April 2026?
A: Agentforce Vibes IDE, Claude Sonnet 4.5 as the default coding model, and Salesforce Hosted MCP Servers.

## Related

- [22 · Agentforce DX & AI-assisted development](22-agentforce-dx-and-ai-assisted-development.md) — the review discipline for what these assistants produce
- [21 · Observability, logging & prod debugging](21-observability-logging-and-prod-debugging.md) — what the Replay Debugger consumes
- [03-lwc · 21 Local dev & the Lightning dev server](../03-lwc-and-slds/21-local-dev-and-lightning-dev-server.md) — the component authoring loop these host
- [01 · `sf` CLI v2 fundamentals](01-sf-cli-v2-fundamentals.md) — the CLI every one of them shells out to
