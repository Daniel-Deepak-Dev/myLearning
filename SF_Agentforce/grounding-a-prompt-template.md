# Grounding a Prompt Template

> Folder: SF_Agentforce · Level: working · Status: 🌱 4 gaps open
> Created: 2026-08-28 · Updated: 2026-08-28

**One line:** The six ways real data gets into a prompt before the model sees it.

**Reach for it when:** Deciding how to feed a template — or working out why the model answered from nothing.

## The six sources

| Source | Reaches | Cap |
|---|---|---|
| **Record merge fields** | The record's own CRM fields | 50 merge fields total |
| **Related list merge fields** | Child records of that record | 5 |
| **Flow** | Anything — CRM, Data 360, external | 5 |
| **Apex** | Anything, same reach as Flow | 5 |
| **Retriever** | RAG over an index; you pick returned fields and result count | — |
| **Data 360 enrichment** | Data 360 fields, layered onto merge fields and related lists | — |

- **Merge fields are the default.** Flow and Apex are the unlimited-reach escapes; a retriever is the RAG option, semantic search rather than a known record path. The caps above are **per provider, not shared**.
- **Resolve → Trust Layer → model.** Every reference is surfaced first, into one assembled prompt; only then does it pass through the [Einstein Trust Layer](einstein-trust-layer.md) and reach the LLM. That order is why grounding runs under the running user's permissions, and why the *assembled* size — not your template text — hits the character ceiling.

## Gotchas

- **Empty grounding does not fail.** The reference resolves to nothing and the model answers fluently around the hole. It reads as a hallucination. Ask of every template: *what does this emit when grounding returns zero rows?*
- **Masking expands the prompt.** The documented error *"Prompt size exceeds the token limit when PII is enabled"* means the Trust Layer pushed you over a ceiling you were under before.

## Gaps to close

- [ ] 🚩 Does Data 360 enrichment still require the input to be a **Contact or Lead**? My source is an April 2024 blog; Summer '26 Help lists Data 360 objects in flow merge fields, so this has likely lifted. Confirm in org.
- [ ] What does a retriever actually index, and who configures it?
- [ ] Can one template combine a retriever *and* Apex, or are they alternatives?
- [ ] Does the 128,000-character ceiling count template text, resolved prompt, or both?

## Related

- [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md) — what a template is, and the headline limits
- [Template-Triggered Prompt Flows](template-triggered-prompt-flows.md) — the flow source in full
- [SF_core · 31 Apex-grounded prompt templates](../SF_core/02-apex-and-triggers/31-apex-grounded-prompt-templates.md) — the Apex source in full, and the injection surface it opens
- [SF_Data_360 · INDEX](../SF_Data_360/INDEX.md) — where the Data 360 and retriever story continues

## Sources

- [Ground Your Prompt Templates with Data Using Flow or Apex](https://developer.salesforce.com/blogs/2024/04/ground-your-prompt-templates-with-data-using-flow-or-apex) — Salesforce Developers, **April 2024** · read 2026-08-28 · source of the Contact/Lead enrichment limit, which is why that one is flagged
- [Ground Prompt Templates with Salesforce Resources](https://help.salesforce.com/s/articleView?id=sf.prompt_builder_ground_template.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-28 — page is JS-rendered, open it to verify

## History

- 2026-08-28 · split out of [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md) once the full source list was researched
