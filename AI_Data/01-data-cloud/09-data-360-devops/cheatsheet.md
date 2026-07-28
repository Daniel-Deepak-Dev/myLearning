# Data 360 DevOps — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Python Code Extensions, data kits for promotion, `@IntegrationTest` for real callouts, and an MCP server for coding agents — the tooling that finally gives Data 360 a DevOps story.

## Key terms
| Term | Definition |
|---|---|
| Code Extension | Custom Python in isolated containers. Headline use: **custom chunking**. |
| Data kit | Promotes code extensions + data transforms sandbox → prod, pulling dependencies automatically. |
| `@IntegrationTest` | Apex tests with live callouts + `commitTestOnly()`. **Scratch orgs only.** |
| Facade tools | `search` / `payload_examples` / `execute` over ~200 REST ops. |

## Rules of thumb

- **Author ≠ operator**: developers write Code Extensions; the **Data Cloud Architect** perm set runs and monitors them. Plan both roles.
- Monitor via the **code extensions log DLO** — failures don't surface obviously anywhere else.
- Get chunking approximately right before indexing a large corpus; re-indexing is expensive.
- Steal the **facade-tool pattern** for any MCP server you build over a large API.

## Exam traps / common confusions

- **Two different Data 360 MCP servers:** Dev Preview (for coding agents building things) vs GA hosted (for agents querying data). Don't conflate them.
- `@IntegrationTest` is scratch-org only, async, one at a time — not CI-ready.
- Code Extension is **Python only** so far; other languages are promised, not shipped.
- Data kits pull dependencies automatically — convenient, but check what came along.

## Minimal example

The facade pattern, and why it matters beyond Data 360:

```
BAD   200 REST operations → 200 MCP tools
      → tool list alone blows the context window

GOOD  3 facade tools
      search(intent)          → find the capability
      payload_examples(op)    → get a working body
      execute(op, body)       → run it
```
