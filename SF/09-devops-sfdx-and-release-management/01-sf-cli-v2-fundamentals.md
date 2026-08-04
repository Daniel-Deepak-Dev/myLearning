# `sf` CLI v2 Fundamentals

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 16

**Scope:** The command surface itself — grammar, configuration, plugins, release train. What the commands *do* to a project is [02](02-sfdx-project-structure-and-source-format.md) onward.

> **What changed.** `sfdx force:…` is not deprecated — **it was removed**. The `force:source:*`, `force:mdapi:*` and `force:org:create|delete` commands were deleted from Salesforce CLI on **6 November 2024**, and the standalone `sfdx` (v7) CLI **receives no updates at all**. The current CLI is `sf` (v2), shipped as the npm package **`@salesforce/cli`**, with a different topic grammar: `sf project deploy start`, not `sfdx force:source:deploy`. Any tutorial whose first command starts `sfdx force:` is teaching a CLI that errors out.

## Core idea

One executable, `sf`, built on **oclif**, with commands grouped into topics that read *noun → verb*: `sf project deploy start`, `sf org create scratch`, `sf package version promote`. Topics come from plugins, several of which are **just-in-time** — not installed until first use.

The thing to internalise is that **the CLI is on its own release train**. A new stable build ships **every Wednesday**, plus a release candidate and a nightly, entirely independent of the platform's three annual releases. So "which release is my org on" and "which CLI am I running" are two unrelated questions, and CLI behaviour can change between two Salesforce releases.

## How it works

| Retired `sfdx` command | Current `sf` command |
|---|---|
| `force:source:deploy` | `project deploy start` |
| `force:source:retrieve` | `project retrieve start` |
| `force:source:push` / `:pull` | `project deploy start` / `project retrieve start` |
| `force:source:status` | `project deploy preview` / `project retrieve preview` |
| `force:source:manifest:create` | `project generate manifest` |
| `force:mdapi:convert` / `force:source:convert` | `project convert mdapi` / `project convert source` |
| `force:org:create` | `org create scratch` / `org create sandbox` |
| `force:auth:web:login` | `org login web` |
| `force:apex:test:run` | `apex run test` |
| `force:data:soql:query` | `data query` |

- **Configuration resolves flag → environment variable → local config → global config.** `sf config set target-org=dev` inside a project writes `.sf/config.json`; `--global` writes to the home directory. Environment variables use the `SF_` prefix (`SF_TARGET_ORG`, `SF_LOG_LEVEL`).
- **`--json` on every command** is the scripting contract — parse it, never scrape the human output, which is free to change weekly.
- **Plugins:** `sf plugins install`, `sf plugins`, and a JIT set that installs on first invocation. `sf commands --deprecated` lists what still runs but is on the way out.

## 2026 currency

Three CLI-level changes bite in 2026. **Secrets are redacted by default** since 27 May 2026 — `org display`, `org list --json`, `org login … --json` and friends no longer print access tokens, SFDX auth URLs or passwords; retrieve them deliberately with `org auth show-access-token`, `org auth show-sfdx-auth-url`, `org auth show-user-password`. The `SF_TEMP_SHOW_SECRETS=true` escape hatch exists only to unbreak pipelines and **is scheduled for removal** → [03](03-org-auth-and-environment-management.md). **The `template generate` reorganisation (Feb 2026)** moved `project generate`, `apex generate class`, `lightning generate component` and the rest under one `sf template generate …` topic — the old names still work, with a deprecation warning, which means even *`sf`-era* tutorials now show superseded commands. And **`org login device` was removed** because OAuth device flow is blocked platform-side → [06-integration · 16](../06-integration-and-apis/16-external-client-apps.md). Version-level detail, including the Node 22 floor and the retrieve-path zip-slip fix, is tracked in [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

## Gotchas

- **`sf` v1 and `sf` v2 are different CLIs.** v1 was a short-lived parallel experiment with its own command set; blog posts from 2022–23 saying "the new `sf`" may mean either. `sf version` settles it — v2 reports `@salesforce/cli/2.x`.
- **`npm dist-tags` for `@salesforce/cli` are not version-ordered.** `latest` can be *older* than `latest-rc` and `nightly`; `npm install -g @salesforce/cli` does not mean "newest".
- **Installing `@salesforce/cli` also puts an `sfdx` executable on your path.** It is a shim, not v7 — the removed `force:` commands still fail.
- **JIT plugins install on first use**, so the first CI run of a command is slow and needs network access to the npm registry.
- **`sf update` only works for installer/TAR installs**; npm installs update through npm. Mixing the two leaves two binaries and a confusing `sf version`.
- **Deprecation warnings go to stderr**, so a pipeline that only captures stdout will never show you that a command name has moved.

> **From my notes.** The seed corpus lists `Important commands` (2025) and the inventory flags it for retired `sfdx force:` syntax. The vault holds only that inventory line, not the note body — so treat the flag as the lesson rather than the finding: **a 2025 command cheatsheet is not automatically safe**, because `force:source:*` had already been removed for over a year when it was written.

## Recall

Q: What exactly happened to `sfdx force:source:deploy`?
A: Removed from Salesforce CLI on 6 November 2024, along with all `force:source:*`, `force:mdapi:*` and `force:org:create|delete` commands. `sfdx` v7 also receives no updates.

Q: How often does Salesforce CLI ship, and is it tied to the platform release?
A: A stable build every Wednesday, plus a release candidate and nightly — completely independent of the three annual platform releases.

Q: Why does `sf org display` no longer show an access token?
A: Credentials have been redacted from command output since 27 May 2026; use `sf org auth show-access-token` deliberately instead.

Q: What is the correct scripting contract for the CLI?
A: The `--json` output. Human-readable output changes weekly and must never be scraped.

Q: What replaced `sfdx force:source:status`?
A: `sf project deploy preview` and `sf project retrieve preview`.

## Related

- [02 · SFDX project structure & source format](02-sfdx-project-structure-and-source-format.md) — what the CLI operates on
- [03 · Org auth & environment management](03-org-auth-and-environment-management.md) — where the secrets-redaction change lands
- [03-lwc · 21 Local dev](../03-lwc-and-slds/21-local-dev-and-lightning-dev-server.md) — `sf lightning dev`, the component-authoring loop
- [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md) — weekly CLI detail, dist-tags, Node floor
