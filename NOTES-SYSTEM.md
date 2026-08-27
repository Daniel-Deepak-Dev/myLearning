# How notes get made here

This file exists so you never have to type the instructions again.

Paste your rough notes. The `study-notes` skill reads this contract and does the rest.

## The problem this solves

You learn topics in whatever order work throws at you. Prompt templates on Monday. Trust Layer on Wednesday. Apex inside a prompt template on Thursday.

Your notes arrive rough and out of order. You want them to land in the right file, in an order you can learn from later, in a format you can re-read in two minutes.

## The four rules

### 1. Routing — one question decides the folder

> **Is this sentence still true with no Agentforce in it?**

- **Yes** → `SF_core/`. Apex, Flow, security, data model, integration.
- **No** → `SF_Agentforce/` or `SF_Data_360/`.

Examples:

| You learned | Goes to |
|---|---|
| What a prompt template is | `SF_Agentforce/` |
| `@InvocableMethod` signature and return types | `SF_core/02-apex-and-triggers/` |
| That a prompt template can call Apex | **Both.** The Agentforce note explains why. The Apex note explains how. They link to each other. |
| Einstein Trust Layer masking | `SF_Agentforce/` |
| Identity resolution rulesets | `SF_Data_360/` |

This is the rule `SF_core` already used to split itself from `AI_Data`. It works. We reuse it.

### 2. Format — light, not dense

Template: [_note-template.md](_note-template.md).

- 50 lines max.
- No paragraph longer than two sentences.
- Bullets and one table. Not prose.
- `## Key points` → `## Gotchas` → `## Gaps to close` → `## Related`.

Your own wording is kept in a `> **From my notes.**` callout. That way you can always tell what you wrote from what the AI added.

Existing `SF_core` notes keep their older, longer format. Only **new** notes use the light one.

### 3. Gaps — scoped to where you actually are

Every note carries a level:

```
> Folder: SF_Agentforce · Level: basic · Status: 🌱 · Fed: 2026-08-27
```

> **A note's gaps may go one level up. Never two.**

| Note level | Gaps allowed |
|---|---|
| `basic` | basic, working |
| `working` | working, deep |
| `deep` | anything on this topic |

So a `basic` prompt-template note gets gaps like *"can Sales Email ground on Lead as well as Contact?"*

It does **not** get `@InvocableMethod`. That is a `deep` item, two levels up.

When you later feed deeper notes on the same topic, the level rises. The deeper gaps unlock then.

Gaps also stay on the topic. Never a syllabus. Never "you should also learn Data Cloud."

Two places a gap can appear:

- `## Gaps to close` at the end — a checklist.
- An inline `> **Gap.**` callout — when the hole sits mid-topic and would confuse the bullets around it.

### 4. Links go both ways

When an Agentforce note links to an Apex note, the Apex note gets a link back. In the same edit.

One-way links are a folder of files. Two-way links are a wiki. You asked for a wiki.

## Order without renumbering

Filenames carry **no number**. `prompt-templates.md`, not `02-prompt-templates.md`.

The learning order lives in each folder's `INDEX.md`:

| # | Topic | One line | Level | Prereq | Fed |
|---|---|---|---|---|---|
| 1 | `einstein-trust-layer.md` | The masking and audit gate | basic | — | 2026-08-24 |
| 2 | `prompt-templates.md` | Reusable LLM instruction as metadata | basic | 1 | 2026-08-22 |

- `#` is the recommended read order.
- `Prereq` is the hard dependency.
- `Fed` is the day you learned it.

Why this way: you will feed a Day-5 topic that belongs at position 3. With numbered filenames that means renaming files and fixing every link. Here it means moving one table row.

`SF_core/PHASES.md` already records renumbering as expensive in that vault. We are not repeating it.

## The `Fed` column and the log

Your memory is by date. The vault is by topic.

[LEARNING-LOG.md](LEARNING-LOG.md) records each feed with a date and where it landed. The `Fed` column in each `INDEX.md` does the same per topic.

So "that thing I learned on Wednesday" is findable, even when you have forgotten its name.

## Migrating out of AI_Data

`AI_Data/02-salesforce-ai/` and `AI_Data/01-data-cloud/` already hold written Agentforce and Data 360 notes.

We are not moving them all at once. Instead:

- Feed a topic `AI_Data` already covers → the useful content gets folded into the new note.
- The old `AI_Data` file gets a one-line pointer to the new home.
- Everything else in `AI_Data` stays where it is.

Migration follows what you are actually studying.

## Anything that does not route

Goes to that folder's `_inbox.md`, as one bullet, with the date.

Filing friction must never stop capture. Triage it later.

## Decisions log

| Date | Decision | Why |
|---|---|---|
| 2026-08-27 | `SF/` renamed to `SF_core/` | Makes room for `SF_Agentforce/` and `SF_Data_360/` as peers. 112 links across 23 files were repaired in the same commit. |
| 2026-08-27 | New folders start empty | You wanted a vault fed by what you actually learn, not by a generated roadmap. |
| 2026-08-27 | Gradual migration from `AI_Data`, not a bulk move | A bulk move would break `STUDY-PLAN.md`, `REVIEW.md`, `GLOSSARY.md`, both `INDEX.md` files and every `Interview/` probe link at once. |
| 2026-08-27 | Filenames carry no number | You feed topics in random order. Numbered filenames make every insertion a rename. |
| 2026-08-27 | Light format for all new notes, in every vault | You asked for notes you can recall from, not paragraphs. |
| 2026-08-27 | Existing `SF_core` notes are enriched in place, not duplicated | 238 notes already exist. A second light file beside each would split the topic in two. |
