# Prompt Builder

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/](../../05-release-radar/README.md)

**Roadmap scope:** Prompt templates, merge fields, and dynamic grounding with record data, Flows, and Data 360 retrievers.

> Naming note: the roadmap says "Data Cloud"; the product is **Data 360** since Dreamforce 2025. Folder paths keep the old name so links don't break.

## What is it?

Prompt Builder is the declarative tool for authoring **prompt templates** — reusable, versioned prompt definitions with merge fields, resolved against live data at runtime.

A template has four parts:

1. **Type** — determines where it can be used and what context it receives.
2. **The prompt text** — with merge fields in `{!...}` syntax.
3. **Grounding** — record fields, related lists, Flow output, Apex output, or a Data 360 **retriever**.
4. **Model + settings** — which LLM, temperature, and response length.

### Template types worth knowing

| Type | Context it gets | Typical use |
|---|---|---|
| **Sales Email** | A record + recipient | Drafted outreach in the email composer |
| **Field Generation** | The record the field is on | Auto-populating a summary field |
| **Record Summary** | A record and its related data | "Summarize this case" panels |
| **Flex** | Whatever objects you declare | The general-purpose one — use for agent actions |

**Flex is the one that matters for agent work.** It takes arbitrary declared inputs, which is what lets a prompt template be invoked as an agent action.

## Why it matters (for the AI-Salesforce architect role)

**A prompt template is the smallest reusable unit of AI behaviour on the platform.** It is versioned, deployable metadata — not a string buried in Apex. That has three consequences worth internalizing:

1. **It's the boundary between admin and developer work.** Admins can iterate on wording without touching code; developers own the grounding and the actions. Getting this split right is most of a good Agentforce delivery.
2. **It composes upward.** The same template can be a field generator, an agent action, *and* — new in the Headless 360 era — an **MCP prompt** exposed to external clients like Claude. One definition, three consumers.
3. **It's where cost and quality get decided.** Grounding too much data inflates tokens on every call; grounding too little produces hallucination. This is the tuning surface.

## How it works

### Grounding — the part that determines quality

| Source | What it gives you | When |
|---|---|---|
| **Record merge fields** | Fields from the triggering record and related records | Always cheapest; use first |
| **Flow** | Anything a Flow can compute or fetch | Complex conditional data assembly |
| **Apex** | Anything code can produce | When Flow can't express it — note the 67.0 access-mode changes |
| **Data 360 retriever** | Semantically relevant chunks from a search index | Unstructured content: PDFs, knowledge, transcripts |
| **Agentforce Data Library** | Managed retriever over Knowledge or uploaded files | The 2026 default for document grounding |

**Rule:** ground with the *narrowest* source that answers the question. Every extra token is paid for on every single invocation.

### The runtime path

```
template invoked (UI action, Flow, agent action, or MCP prompt)
   → merge fields resolve against live records
   → grounding sources execute (retriever query / Flow / Apex)
   → assembled prompt → Einstein Trust Layer (mask PII, injection check)
   → LLM
   → response → Trust Layer (unmask, toxicity score, audit)
   → returned to caller
```

Prompt Builder never talks to the model directly — **everything goes through the Trust Layer**. That's the answer to "where does our data go?", and it's why Prompt Builder is preferred over hand-rolled callouts.

### Prompt templates as MCP prompts

Under Headless 360, a prompt template can be exposed through a **custom hosted MCP server** as an MCP *prompt* primitive. An external client — Claude Desktop, Claude Code, Cursor — can then invoke your governed, grounded template rather than improvising its own wording. The Trust Layer still applies.

This is a genuinely useful bridge between the Salesforce and Claude tracks: see [MCP](../../03-claude-cca/05-mcp/notes.md) and [the capstone MCP project](../../04-capstone/01-mcp-server-salesforce/notes.md).

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Build a Flex template grounded on a record, then invoke it as an agent action.
- [ ] Add a Data 360 retriever as a second grounding source and compare answer quality with and without it.
- [ ] Open the **Trust Layer audit trail** after a run and read what was actually sent to the model. This is the exercise that makes masking concrete.
- [ ] Expose one template as an MCP prompt and call it from Claude Desktop.

## Gotchas & sharp edges

- **Test with the record that will break it**, not a tidy demo record. Empty fields, missing related records and unusual picklist values are where templates fail — merge fields resolve to nothing and the model invents a replacement.
- **Grounding is not free.** Every retriever hit and every merged related list is tokens on each invocation, and Agentforce bills per action. A chatty template is a recurring cost.
- **Masking can degrade output.** If PII is masked and the prompt asks the model to use a customer's name, it works with a placeholder. Usually fine, occasionally not — check real output rather than assuming.
- **Versioning is not automatic promotion.** Templates are metadata; they need deploying like anything else.
- **The model setting is per template.** It can differ from the org default *and* from the model pinned in an agent's Agent Script. When output looks unexpectedly different between two paths, check which model each actually used.
- **Apex-based grounding runs under the 67.0 rules** — user mode by default. A grounding class that used to see everything may now legitimately return less. See [custom agent actions](../05-custom-agent-actions/notes.md).

## Related topics

- [Agentforce Anatomy](../02-agentforce-anatomy/notes.md) — where templates become actions
- [Einstein Trust Layer](../04-einstein-trust-layer/notes.md) — what wraps every invocation
- [RAG on platform](../../01-data-cloud/08-rag-on-platform/notes.md) — retrievers and Data Libraries in depth
- [Custom Agent Actions](../05-custom-agent-actions/notes.md) — Apex/Flow grounding under user mode
- [Prompt engineering (Claude track)](../../03-claude-cca/04-prompt-engineering/notes.md) — the vendor-neutral craft
