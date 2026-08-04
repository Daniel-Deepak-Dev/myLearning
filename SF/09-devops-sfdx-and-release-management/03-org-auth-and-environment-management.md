# Org Auth & Environment Management

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 16

**Scope:** Getting the CLI authorized against an org and keeping several orgs straight. The OAuth flows themselves are [06-integration · 15](../06-integration-and-apis/15-oauth-flows-and-authorization.md); this is the developer-and-CI end.

> **What changed.** **The CLI stopped printing credentials.** Since **27 May 2026**, `org display`, `org list --json`, `org create scratch --json`, every `org login … --json` and `org list auth --json` redact access tokens, SFDX auth URLs and passwords. Any CI recipe that pipes `sf org display --verbose` into `grep sfdxAuthUrl` is broken. Ask for the secret explicitly — `org auth show-access-token`, `org auth show-sfdx-auth-url`, `org auth show-user-password` — and treat `SF_TEMP_SHOW_SECRETS=true` as a countdown, not a fix: Salesforce has said it will be disabled.

## Core idea

Authorization is per machine and per org, stored in the CLI's home directory, and surfaced by an **alias**. Everything downstream — deploy, retrieve, packaging, tests — resolves an org through `--target-org`/`-o`, the `target-org` config variable, or the `SF_TARGET_ORG` environment variable, in that order.

The distinction that matters operationally is **interactive vs headless**. A human authorizes with a browser; CI cannot, and must use a flow with no user present. That is JWT bearer, and increasingly it is the only one left.

## How it works

| Command | Use |
|---|---|
| `org login web` | interactive, a human at a browser |
| `org login jwt` | headless CI — needs a private key, a consumer key and a username |
| `org login sfdx-url` | restore a stored auth URL, usually from a CI secret |
| `org login access-token` | short-lived, an already-issued token |
| ~~`org login device`~~ | **removed** — OAuth device flow is blocked platform-side |

- **Aliases and config:** `sf alias set uat=user@example.com`, `sf config set target-org uat` (project-local) or `--global`. `sf org list` shows everything authorized; `sf org logout` removes it.
- **Dev Hub** is a separate config variable, `target-dev-hub`, because scratch orgs and packages are created against it rather than against the working org → [04](04-scratch-orgs-and-org-shape.md).
- **Sandboxes** are created and refreshed from the CLI too — `sf org create sandbox`, `sf org resume sandbox` — and each refresh reissues a new My Domain host → [07-security · 20](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md).

## 2026 currency

Beyond the redaction above, the CI story has a **structural problem worth planning around**: the standard JWT recipe says "create a connected app with a digital certificate", and **connected-app creation has been Support-gated org-wide since Spring '26**, after being disabled by default for new orgs in Winter '26. Existing connected apps keep working and are *not* retired, but a new pipeline in a new org cannot follow the 2023 runbook — the current object is an **External Client App** → [06-integration · 16](../06-integration-and-apis/16-external-client-apps.md). The `org login device` removal is the same story one step further along: the flow was blocked outright in September 2025, so the command was deleted rather than left to fail.

## Gotchas

- **The auth file *is* the org.** A stored SFDX auth URL is a refresh token in a string; leaking one in a CI log is a full compromise, which is precisely why the redaction happened.
- **`--target-dev-hub` and `--target-org` are different flags** and a packaging command silently doing the wrong thing is usually this.
- **Project-local config beats global config**, so a stale `.sf/config.json` in a repo will quietly redirect a colleague's deploy.
- **JWT auth fails with an unhelpful error when the user is not pre-authorized** for the connected app — assign the app to a permission set rather than relying on "admin approved users are pre-authorized" being set.
- **Scratch org auth expires with the org**, but the alias does not — `sf org list` accumulates dead entries, and CLI commands slow down when `target-org` points at a long-expired one.
- **MFA does not exempt CI**, but JWT bypasses the interactive challenge by design; the compensating control is the certificate and the permission set, not a second factor → [07-security · 17](../07-security-and-sharing/17-authentication-and-mfa.md).
- **`sf org open` opens as the authorized user**, which in production is usually an admin — an easy way to make a change nobody committed.

## Recall

Q: Which auth flow does headless CI use, and why not the others?
A: JWT bearer — it needs no browser and no interactive user. Web login needs a human; device flow is blocked and its command was removed.

Q: What broke in CI pipelines on 27 May 2026?
A: Credentials were redacted from CLI output, so scripts scraping `org display` or `org list --json` for tokens or auth URLs stopped working. Use the `org auth show-*` commands.

Q: Why can't a new org follow the classic JWT connected-app runbook?
A: Connected-app creation has been Support-gated org-wide since Spring '26. External Client Apps are the current object.

Q: What is the resolution order for the target org?
A: The `--target-org` flag, then `SF_TARGET_ORG`, then project-local config, then global config.

Q: Why is a stored SFDX auth URL treated as a high-value secret?
A: It contains a refresh token — anyone holding it has ongoing access to the org as that user.

## Related

- [01 · `sf` CLI v2 fundamentals](01-sf-cli-v2-fundamentals.md) — config precedence and the `--json` contract
- [04 · Scratch orgs & org shape](04-scratch-orgs-and-org-shape.md) — what `target-dev-hub` is for
- [06-integration · 16 External Client Apps](../06-integration-and-apis/16-external-client-apps.md) — why "create a connected app" is no longer a step you can take
- [07-security · 17 Authentication & MFA](../07-security-and-sharing/17-authentication-and-mfa.md) — the enforcement wave this sits under
