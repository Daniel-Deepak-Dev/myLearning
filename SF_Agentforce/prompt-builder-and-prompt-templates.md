# Prompt Builder & Prompt Templates

> Folder: SF_Agentforce · Level: basic · Status: ✅ complete
> Created: 2026-08-27 · Updated: 2026-08-28

**One line:** Prompt Builder is the Setup tool. A prompt template is the reusable prompt it produces.

**Reach for it when:** You want the same instruction to an LLM to run against different records without rewriting it each time.

## Key points

- A **prompt template** is a saved prompt with **merge fields** that resolve to live record data at runtime.
- The same template runs against any record of its object. That reuse is the whole point.
- **Grounding** is the act of feeding real data in. Merge fields are the simplest of six sources → [Grounding a Prompt Template](grounding-a-prompt-template.md).
- Templates are **metadata**, so they deploy between orgs like any other component.
- The template's **type** decides where it can be used and what context it receives → [Prompt Template Types](prompt-template-types.md).
- **Ceilings: 128,000 characters and 50 merge fields** — counted against the *resolved* prompt, not your template text.
- Building and running are **separate permission sets**, and a live version cannot be edited → [Versions & Access](prompt-template-versions-and-access.md).
- Every call passes through the [Einstein Trust Layer](einstein-trust-layer.md).

> **From my notes.** *"Reusage prompt with different data based context"* — right, and the emphasis is worth keeping. What gets reused is not the wording. It is the **binding to a record**: one template, many records.

## Gotchas

- **Merge fields resolve at runtime, not at save.** A field the running user cannot see resolves empty rather than erroring.
- **Renaming a template breaks callers that reference it by API name**, with no compile-time warning.

## Hands-on

- [ ] **AF-PB-01** · 20 min · Build a record-grounded template on Account, run it against a fully populated record, then an almost-empty one. **Proves:** an empty merge field resolves to nothing and the model invents around the hole — it reads as a hallucination.
- [ ] **AF-PB-02** · 15 min · Rename a template's API name, then run whatever referenced it. **Proves:** renaming breaks callers with no compile-time warning.
- [ ] **AF-PB-03** · 25 min · Grow a related-list grounding until the run fails on the 128,000-character ceiling. **Proves:** the ceiling counts the resolved prompt, not your template text — copy the error verbatim.

## Related

- [Grounding a Prompt Template](grounding-a-prompt-template.md) — the six ways data reaches the prompt
- [Prompt Template Versions & Access](prompt-template-versions-and-access.md) — permissions, versions, activation
- [Prompt Template Types](prompt-template-types.md) — the six types and what each one grounds on
- [Einstein Trust Layer](einstein-trust-layer.md) — what happens to the prompt between here and the model

## Sources

- [Prompt Builder](https://help.salesforce.com/s/articleView?id=sf.prompt_builder_about.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-27 — page is JS-rendered, open it to verify
- [Prompt Builder Limits](https://help.salesforce.com/s/articleView?id=sf.prompt_builder_limits.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-28 · source of the two ceilings

## History

- 2026-08-27 · created from your Day-1 notes
- 2026-08-28 · limits confirmed and added; setup, versions and grounding split into their own notes
