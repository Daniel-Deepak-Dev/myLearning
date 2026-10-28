---
vault: SF_core
area: 09-devops-sfdx-and-release-management
format: dense
status: learning
created: 2026-08-04
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 17
tags: [currency-warning]
---
# VS Code, Code Builder & Tooling

**Scope:** Where a Salesforce developer actually sits, and which of the names in older material still refer to a live product. The component-authoring loop is [03-lwc · 21](../03-lwc-and-slds/21-local-dev-and-lightning-dev-server.md); installing and configuring the CLI is [01](01-sf-cli-v2-fundamentals.md).

> **What changed.** **Code Builder is now Agentforce Vibes IDE** — same browser-hosted VS Code, renamed. And the mirror-image error is just as common: the **Developer Console carries a *legacy* label in the docs but has no announced retirement date** and still works — although since **Winter '27** it is hidden from Setup by default. Two failure modes, one page: calling a renamed product by a dead name, and calling a labelled-legacy product retired.

## Core idea

There is no single answer to "which IDE", and the reason is entitlement rather than taste. Salesforce now ships three environments with **different org coverage**, and the right recommendation for a client depends on which editions and clouds they run — which is a governance question that arrives disguised as a developer-preference question.

Underneath all three is the same thing: the **Salesforce Extensions for VS Code**, driving the same CLI against the same Metadata API. Choosing an environment changes where the process runs, not what it can do.

## How it works

- **Salesforce Extension Pack** (and *Expanded*) is the desktop baseline — Apex language server, LWC support, org browser, CLI integration, published to both the VS Code Marketplace and Open VSX.
- **Agentforce Vibes IDE** — browser-hosted, cloud-run VS Code launched from Setup, fully authenticated to the org, no local install. The same Salesforce extensions as the desktop.
- **Agentforce Vibes** the *extension* ships inside the Extension Pack, so the agentic assistant is available on the desktop too → [22](22-agentforce-dx-and-ai-assisted-development.md).
- **Web Console** — an IDE inside the org itself. Open beta from **14 April 2026**, **GA in Winter '27** (announced September 2026) and **on by default for admins**; org-wide control at Setup → Development → Web Console. Apex, LWC files through Org Browser, anonymous Apex, SOQL with query plans, Apex tests, trace flags and debug logs. **Apex is read-only in production.** **Salesforce-provided extensions only**.
- **Coverage is the differentiator.** **Agentforce Vibes excludes Professional Edition, Government Cloud, the EU Operating Zone, FedRAMP High and China Cloud.** Web Console runs in Developer, Enterprise, Unlimited, Performance and Professional editions (Professional with restricted features), but its FAQ says it is **not yet on Government Cloud** — so neither IDE runs there. 🚩 Web Console in the EU Operating Zone and China Cloud is not confirmed.
- **Two debuggers.** Apex **Replay** Debugger is free and reads a log → [21](21-observability-logging-and-prod-debugging.md); the **Interactive** debugger is licensed and sandbox-only.
- **Every Developer Edition org has included Agentforce Vibes IDE, Claude Sonnet 4.5 as the default coding model, and Salesforce Hosted MCP Servers at no cost since April 2026** — which makes the free org the honest place to evaluate all of this.

> **From my notes** — the [inventory](../_notion-seed/INVENTORY.md) line only; the note body is not in the vault. A 2019 page listing VS Code and Chrome extensions is the most perishable kind of note in the vault — the CLI it was written against has been replaced, and so has half the list. One thing in it has not aged: a browser extension that reads your org **has your session**. That is a security decision made once per developer and never reviewed → [07-security · 18](../07-security-and-sharing/18-session-security-login-policies-and-step-up.md).

## Gotchas

- **Same extensions ≠ same environment.** Web Console permits only Salesforce-provided extensions, so a team standard built on third-party ones does not transfer.
- **A cloud IDE still needs the org's session policy to permit it.** IP restrictions and login-hours policies apply to the browser-hosted environments too.
- **Anything called *Local Dev* in a 2024 note is the Live Preview extension now** → [03-lwc · 21](../03-lwc-and-slds/21-local-dev-and-lightning-dev-server.md).
- **The Metadata Visualizer is Beta and partial** — objects, permission sets and flexipages. Useful; not an org diagram.
- **"Where did the Developer Console go?"** Since Winter '27 it is not in the Setup menu by default. Re-enable it at Setup → Development → Web Console → *Enable Developer Console*. Setting Web Console to Inactive brings the Developer Console back by default.
- **The extension pack pins nothing.** It updates independently of the CLI version your pipeline pinned, so a developer and CI can disagree about a deploy → [14](14-ci-cd-with-github-actions.md).

## Recall

Q: What is Code Builder called now?
A: **Agentforce Vibes IDE** — the browser-hosted VS Code environment, renamed.

Q: Is the Developer Console retired?
A: No. It is labelled *legacy* in the documentation, with no announced retirement date. Since Winter '27 it is hidden from Setup by default and re-enabled from the Web Console setup page.

Q: When would you recommend Web Console over Agentforce Vibes?
A: For a quick single-org edit with nothing to set up, or in Professional Edition, which Vibes excludes. Not for Government Cloud — Web Console is not there yet either.

Q: Which Apex debugger costs nothing?
A: The Apex Replay Debugger, which replays a captured debug log; the Interactive debugger is licensed and sandbox-only.

Q: What does a Developer Edition org include for free since April 2026?
A: Agentforce Vibes IDE, Claude Sonnet 4.5 as the default coding model, and Salesforce Hosted MCP Servers.

## Related

- [22 · Agentforce DX & AI-assisted development](22-agentforce-dx-and-ai-assisted-development.md) — the review discipline for what these assistants produce
- [21 · Observability, logging & prod debugging](21-observability-logging-and-prod-debugging.md) — what the Replay Debugger consumes
- [03-lwc · 21 Local dev & the Lightning dev server](../03-lwc-and-slds/21-local-dev-and-lightning-dev-server.md) — the component authoring loop these host
- [01 · `sf` CLI v2 fundamentals](01-sf-cli-v2-fundamentals.md) — the CLI every one of them shells out to

## Sources

- [Announcing General Availability: Web Console](https://developer.salesforce.com/blogs/2026/09/announcing-general-availability-web-console-your-modern-in-browser-ide) — Salesforce Developers · via search 2026-10-28 · GA; on by default for admins; Apex read-only in production; LWC editing; Setup → Development → Web Console; Developer Console can be re-enabled there
- [The Salesforce Developer's Guide to the Winter '27 Release](https://developer.salesforce.com/blogs/2026/10/developers-guide-to-the-winter-27-release) — Salesforce Developers · via search 2026-10-28 · Web Console GA in Winter '27; *"In Winter '27, Developer Console doesn't appear in the Setup menu by default"* and the *Enable Developer Console* path
- [Web Console — Winter '27 release notes](https://help.salesforce.com/s/articleView?id=release-notes.rn_webconsole.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-28 · if Web Console is Inactive, Developer Console activates by default; both can be Active
- [Web Console FAQ](https://developer.salesforce.com/docs/platform/webconsole/guide/faq.html) — Salesforce Developers · via search 2026-10-28 · editions (Professional restricted); not yet available on Government Cloud

## History

- 2026-10-28 · Winter '27 currency check: Web Console GA and on by default; Developer Console hidden from Setup; corrected "Web Console covers Government Cloud"
