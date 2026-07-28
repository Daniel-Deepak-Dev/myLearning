# Capstone: MCP Server for Salesforce — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Not "build an MCP server" any more — **choose between standard hosted, custom hosted and self-hosted, and justify it**, because hosted servers went GA and enforce the org's sharing model for you.

## Key terms
| Term | Definition |
|---|---|
| Standard hosted (GA) | Salesforce-hosted: SObject CRUD/SOQL/search, Data 360, Tableau. |
| Custom hosted | Salesforce-hosted, you pick the tools. **Respects full org sharing + security.** |
| Self-hosted | Your server, your code — enforces only what you implemented. |
| Facade tools | `search` / `payload_examples` / `execute` over a broad API surface. |

## Rules of thumb

- **The decision record is the deliverable**, not the code.
- Custom hosted tools can wrap: `@InvocableMethod`, Flows, Apex REST, `@AuraEnabled`, Named Query API, Prompt Builder, whole agents, API Catalog endpoints.
- Self-host only for: cross-system composition, custom caching/rate-limiting, client infra constraints, or something the hosted options can't express.
- Read-only by default; **make write tools idempotent** — agents retry after timeouts.

## Exam traps / common confusions

- **Don't hand-roll what's GA.** Rebuilding SObject CRUD is a weaker portfolio piece, not a stronger one.
- A self-built server gets FLS, sharing and polymorphic fields wrong in ways the platform gets right.
- **Who may create custom hosted servers?** A security-review question — they expose org data to external AI clients.
- A **flat tool list blows the context window** — 200 tools cost context before any work happens.
- Under user mode, the **connected user's permissions are the enforcement boundary**. Least-privilege it.

## Minimal example

The demo that makes the whole argument:

```
1. connect Claude Code → standard SObject server (Dev org)
2. query as an ADMIN user      → sees everything
3. reconnect as a RESTRICTED user → sees less
   ^ same server, no code changed. Screenshot this.

That's org sharing + FLS enforced for free.
A self-hosted server enforces only what you remembered.
```
