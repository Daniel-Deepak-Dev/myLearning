# Prompt Template Types

> Folder: SF_Agentforce · Level: basic · Status: 🌱 3 gaps open
> Created: 2026-08-27 · Updated: 2026-08-28

**One line:** The type you pick when creating a template decides where it can be used and what context it receives.

**Reach for it when:** Starting a new template and choosing from the type list.

## The six types

| Type | What it does | Grounds on | Surfaces in |
|---|---|---|---|
| **Sales Email** | Drafts a personalised email | A **recipient object you pick at creation** (`{!$Input:Recipient.…}`), plus an optional related object | The email composer |
| **Field Generation** | Fills one field with the model's answer | The record the field sits on | A field on a record page |
| **Record Summary** | Writes a rich-text summary of a record | A record and its related data | A record page panel |
| **Knowledge Answers** | Shapes how an agent answers from Knowledge | Knowledge articles | **Agents** |
| **Record Prioritization** | Ranks records so the user works the top ones first | Records **owned by the requesting user** | A ranked list |
| **Flex** | Anything the other five do not cover | Whatever inputs you declare | **Anywhere — including agent actions** |

> **From my notes.** Your list had five and called the third *"Flex generations"* — the type is just **Flex**. And there is a sixth: **Record Prioritization**, already sitting in your own `capabilityType` table further down your notes but missing from the list above it.

## Gotchas

- **Record Prioritization only sees records the requesting user owns.** It is not an org-wide ranking.
- **The type is fixed at creation.** Changing your mind means a new template, not a setting.

## Gaps to close

- [ ] 🚩 Does the Sales Email recipient picker offer **Lead** as well as Contact? Every documented example uses Contact, and no source lists the full set.
- [ ] 🚩 Can Knowledge Answers be used outside an agent at all, or is it strictly agent-facing?
- [ ] 🚩 Can any type other than Flex be exposed as an agent action? No source confirms or denies it.

## Related

- [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md) — what a template is before you pick a type
- [Prompt Templates as Agent Actions](prompt-templates-as-agent-actions.md) — the Flex route into Agentforce
- [Grounding a Prompt Template](grounding-a-prompt-template.md) — the six data sources, and the 5-per-provider caps
- [SF_core · 31 Apex-grounded prompt templates](../SF_core/02-apex-and-triggers/31-apex-grounded-prompt-templates.md) — the `capabilityType` URI that binds Apex to one of these types

## Sources

- [Prompt Template Types](https://help.salesforce.com/s/articleView?id=ai.prompt_builder_standard_template_types.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-27 — page is JS-rendered, open it to verify
- [Sales Email Prompt Templates for Efficiency](https://trailhead.salesforce.com/content/learn/projects/quick-start-create-a-sales-email-prompt-template/get-started-with-sales-email-prompt-templates) — Trailhead · read 2026-08-28 · recipient and related-object behaviour
- [Prompt Templates Types in Salesforce](https://www.apexhours.com/prompt-templates-types-in-salesforce/) — third party 🚩 · read 2026-08-27 · source of the five standard types

## History

- 2026-08-27 · created from your Day-1 and Day-2 notes · added Record Prioritization as the sixth type
- 2026-08-28 · 5-input cap generalised; added where each type surfaces; Sales Email recipient shown to be a picker; agent-action route split out
