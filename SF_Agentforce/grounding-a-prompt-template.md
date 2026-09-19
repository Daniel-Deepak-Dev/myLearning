# Grounding a Prompt Template

> Folder: SF_Agentforce · Level: working · Status: ✅ complete
> Created: 2026-08-28 · Updated: 2026-08-30

**One line:** The six ways real data gets into a prompt before the model sees it.

**Reach for it when:** Deciding how to feed a template — or working out why the model answered from nothing.

## The six sources

| Source | Reaches | Cap |
|---|---|---|
| **Record merge fields** | The record's own CRM fields | 50 merge fields total |
| **Related list merge fields** | Child records of that record | 5 |
| **Flow** | Anything — CRM, Data 360, external | 5 |
| **Apex** | Anything, same reach as Flow | 5 |
| **Retriever** | RAG over a search index; you pick returned fields and result count | — |
| **Data 360 enrichment** | Data 360 fields, layered onto merge fields and related lists | — |

- **Merge fields are the default.** Flow and Apex are the unlimited-reach escapes; a retriever is the RAG option, semantic search rather than a known record path. The caps above are **per provider, not shared**.
- **Sources combine.** One template can insert a retriever *and* a Flow *and* merge fields. They are separate resources on one template, not alternatives.
- **Resolve → Trust Layer → model.** Every reference is surfaced first, into one assembled prompt; only then does it pass through the [Einstein Trust Layer](einstein-trust-layer.md) and reach the LLM. That order is why grounding runs under the running user's permissions, and why the **assembled** prompt — not your template text — hits the 128,000-character ceiling.

## The retriever, in full

A **search index** does the indexing; the **retriever** is the query wrapper you point a template at.

- The index chunks unstructured or semi-structured data, embeds each chunk, and stores chunks in a chunk DMO and embeddings in a vector DMO. Two index types: **vector** and **hybrid** (semantic plus keyword).
- The index is built in the **Data 360 app → Search Index**; the retriever under **AI Models → Retrievers** (also Agentforce Studio → Build → Data → Retrievers).
- The retriever holds **fields to return**, **number of results** (20 by default), **filters** and **citation settings** — relevance tuning lives there, not in the prompt.
- Inserted in Prompt Builder via **Insert Resource → Actions → Retrievers**, then you map its search text and output fields.

## Gotchas

- **Empty grounding does not fail.** The reference resolves to nothing and the model answers fluently around the hole. It reads as a hallucination. Ask of every template: *what does this emit when grounding returns zero rows?*
- **Masking expands the prompt.** The documented error *"Prompt size exceeds the token limit when PII is enabled"* means the Trust Layer pushed you over a ceiling you were under before.
- **A retriever returns 20 results unless you say otherwise.** Twenty chunks of text is a large share of the assembled prompt — turn it down before you tune anything else.

## Confirm in org

- 🚩 Does Data 360 enrichment still require the input to be a **Contact or Lead**? The source is an April 2024 blog; Summer '26 Help lists Data 360 objects in flow merge fields, so this has likely lifted.

## Hands-on

- [ ] **AF-GRND-01** · 40 min · Build a search index and a retriever, then ground a template on it. **Proves:** relevance tuning lives on the retriever, not in the prompt. **Needs:** Data 360.
- [ ] **AF-GRND-02** · 15 min · Run once at the 20-result default, then at 3, comparing the resolved prompt size. **Proves:** the default eats a large share of the prompt budget. **Needs:** Data 360.
- [ ] **AF-GRND-03** · 20 min · Put a retriever, a Flow and merge fields on one template. **Proves:** the six sources combine rather than compete.
- [ ] **AF-GRND-04** · 20 min · Try Data 360 enrichment on a Contact, then on something that is neither Contact nor Lead. **Settles:** whether that restriction has lifted 🚩. **Needs:** Data 360.

## Related

- [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md) — what a template is, and the headline limits
- [Prompt Template Types](prompt-template-types.md) — the type decides which of these six a template can even reach
- [Flex Prompt Templates](flex-prompt-templates.md) — declared inputs are **not** grounding: the caller passes them in, where these six are pulled during resolution
- [Template-Triggered Prompt Flows](template-triggered-prompt-flows.md) — the flow source in full
- [SF_core · 31 Apex-grounded prompt templates](../SF_core/02-apex-and-triggers/31-apex-grounded-prompt-templates.md) — the Apex source in full, and the injection surface it opens
- [SF_Data_360 · INDEX](../SF_Data_360/INDEX.md) — where the Data 360 and retriever story continues

## Sources

- [Ground Your Prompt Templates with Data Using Flow or Apex](https://developer.salesforce.com/blogs/2024/04/ground-your-prompt-templates-with-data-using-flow-or-apex) — Salesforce Developers, **April 2024** · read 2026-08-28 · source of the Contact/Lead enrichment limit, which is why that one is flagged
- [Create a Search Index, Retriever, and Prompt Template](https://trailhead.salesforce.com/content/learn/modules/advanced-rag-with-data-360-and-agentforce/create-a-search-index-retriever-and-prompt-template) — Trailhead · read 2026-08-28 · retriever settings and the Insert Resource path
- [Step 3 — Create Search Index and Retriever](https://developer.salesforce.com/docs/ai/ground-agentforce-on-website/guide/aes-create-search-index-and-retriever.html) — Salesforce Developers · read 2026-08-28 · chunking, vector DMO, where each is built

## History

- 2026-08-28 · split out of [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md) once the full source list was researched
- 2026-08-28 · retriever written up properly — index vs retriever, where each is built, the settings it exposes, the 20-result default; confirmed sources combine rather than compete
- 2026-08-30 · linked to [Flex Prompt Templates](flex-prompt-templates.md) to draw the line between a declared input and a grounding source
