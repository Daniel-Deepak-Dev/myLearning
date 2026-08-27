# 04 · Capstone — Ship Billable Work

Convert learning into architect-track proof. One shipped project beats five certificates in a client conversation. Roadmap tag: **Capstone** (green).

> **Two premises changed in Summer '26.** Hosted MCP servers went **GA**, so the MCP project is now about *choosing and justifying* an architecture rather than hand-building one. And agents are authored in **Agent Script**, with per-action billing that makes unit economics part of the design.

| Project | What it proves | Files |
|---|---|---|
| [MCP Server for Salesforce](01-mcp-server-salesforce/notes.md) | Standard vs custom vs self-hosted — and that **custom hosted servers enforce the org's sharing model** while a self-built one enforces only what you wrote | [cheatsheet](01-mcp-server-salesforce/cheatsheet.md) · [flashcards](01-mcp-server-salesforce/flashcards.md) · [resources](01-mcp-server-salesforce/resources.md) |
| [RAG Assistant over CRM Data](02-rag-assistant-crm/notes.md) | Data Libraries + ADL Connect API + **custom chunking**, with a measured before/after against a fixed question set | [cheatsheet](02-rag-assistant-crm/cheatsheet.md) · [flashcards](02-rag-assistant-crm/flashcards.md) · [resources](02-rag-assistant-crm/resources.md) |
| [End-to-End Agentforce Use Case](03-agentforce-use-case/notes.md) | One measurable outcome, authored in **Agent Script**, with **unit economics** and an honest failure analysis | [cheatsheet](03-agentforce-use-case/cheatsheet.md) · [flashcards](03-agentforce-use-case/flashcards.md) · [resources](03-agentforce-use-case/resources.md) |
| [Write-up & Internal Pitch](04-writeup/notes.md) ⬜ | Architecture diagram, tradeoffs, demo video — the Geeksoft "AI + Data solutions" calling card | ⬜ scaffolded — not yet written · [resources](04-writeup/resources.md) |

Milestone: one demoable AI + Data project shipped, plus the dual credential (Salesforce certs + CCA-F).

## What makes these architect-level rather than developer-level

The same three things apply to all of them, and they're what an interviewer probes for:

1. **A measured outcome** — a baseline taken before you built, and a number after.
2. **Stated unit economics** — you pay per *action* (~$0.10), so architecture has a price you can quote.
3. **An honest failure analysis** — what it gets wrong and what you'd fix next. This is what separates a real project from a rehearsed demo.
