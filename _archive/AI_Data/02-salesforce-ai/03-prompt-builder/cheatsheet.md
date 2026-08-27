# Prompt Builder — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Declarative, versioned prompt templates that merge live CRM data and grounding sources, always routed through the Trust Layer — reusable as UI actions, agent actions, or MCP prompts.

## Key terms
| Term | Definition |
|---|---|
| Flex template | The general-purpose type with arbitrary declared inputs. The one used for agent actions. |
| Dynamic grounding | Injecting live CRM / Data 360 data at runtime so the model answers from your data. |
| Retriever | A configured query against a search index or data graph — the RAG building block. |
| Agentforce Data Library | Managed retriever over Knowledge or uploaded files; the 2026 default for documents. |

## Rules of thumb

- Ground with the **narrowest source that answers the question** — every extra token is paid on every invocation, and Agentforce bills per action.
- Order of preference: record merge fields → Flow → Apex → retriever. Cheapest first.
- Test with the record that will **break** it (empty fields, missing related records), not the demo record.
- One template can serve three consumers: UI action, agent action, **MCP prompt**.

## Exam traps / common confusions

- Prompt Builder **never calls the model directly** — the Trust Layer is always in the path. That's the answer to "where does our data go?"
- The **model is set per template**, and can differ from the org default *and* from the model pinned in an agent's Agent Script.
- Templates are metadata: versioned ≠ automatically promoted. They still need deploying.
- Apex grounding now runs in **user mode** at 67.0 — it may legitimately return less than before.

## Minimal example

```
Flex template "Case Risk Summary"
  inputs:    Case record
  grounding: {!Case.Subject}, {!Case.Contact.Name}
             + retriever → Data Library "Support Runbooks"
  prompt:    "Summarize the risk on this case in 3 bullets.
              Cite the runbook section you used."
  →  exposed as an agent action AND an MCP prompt
```
