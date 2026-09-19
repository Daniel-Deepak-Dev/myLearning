# How notes get made here

This file exists so you never have to type the instructions again.

Paste your rough notes. The `study-notes` skill reads this contract and does the rest.

## The problem this solves

You learn topics in whatever order work throws at you. Prompt templates on Monday. Trust Layer on Wednesday. Apex inside a prompt template on Thursday.

Your notes arrive rough and out of order. You want them to land in the right file, in an order you can learn from later, in a format you can re-read in two minutes.

## The five rules

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

### 2. Format — light, not dense

Template: [_note-template.md](_note-template.md).

- 50 lines max.
- No paragraph longer than two sentences.
- Bullets and one table. Not prose.
- `## Key points` → `## Gotchas` → `## Gaps to close` → `## Related` → `## Sources` → `## History`.

Your own wording is kept in a `> **From my notes.**` callout. That way you can always tell what you wrote from what the AI added.

Existing `SF_core` notes keep their older, longer format. Only **new** notes use the light one.

### 3. Gaps — scoped to where you actually are

Every note carries a level:

```
> Folder: SF_Agentforce · Level: basic · Status: 🌱 4 gaps open
> Created: 2026-08-27 · Updated: 2026-08-27
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

Gaps also stay on the topic. Never a syllabus. Never "you should also learn Data 360."

Two places a gap can appear:

- `## Gaps to close` at the end — a checklist.
- An inline `> **Gap.**` callout — when the hole sits mid-topic and would confuse the bullets around it.

**A closed gap is deleted, not ticked.** Answer it, remove the line. When the last one goes, the `## Gaps to close` heading goes with it. What you learnt belongs in the note body — a list of settled questions is just clutter you have to read past.

### 4. Links go both ways

When an Agentforce note links to an Apex note, the Apex note gets a link back. In the same edit.

One-way links are a folder of files. Two-way links are a wiki. You asked for a wiki.

### 5. Dates, status and sources

**Status is derived, never typed.** Count the `- [ ]` lines in `## Gaps to close`:

- at least one → `Status: 🌱 N gaps open`
- none, or no section at all → `Status: ✅ complete`

Delete a gap and the status moves on its own. A typed status goes stale the first time you forget to update it.

**Dates.** `Created` never changes. `Updated` changes on every edit.

**Staleness.** Past 3 months without an update, a third metadata line appears:

```
> ⏳ 4 months old — recheck against release notes
```

It disappears the moment the note is touched. Salesforce AI moves fast enough that a note going quiet for a quarter is worth flagging.

**Sources.** Every researched fact carries a link and the date it was read:

```markdown
## Sources

- [Prompt Template Types](https://help.salesforce.com/...) — Salesforce Help · read 2026-08-27
- [Apex Hours](https://www.apexhours.com/...) — third party 🚩 · read 2026-08-27
```

Salesforce domains are trusted. Anything else carries 🚩.

**History.** One dated line per feed, saying what was **added or changed** — never a gap tally:

```markdown
## History

- 2026-08-27 · created from your Day-1 notes
- 2026-09-02 · added Record Prioritization as the sixth type
```

## Order without renumbering

Filenames carry **no number**. `prompt-templates.md`, not `02-prompt-templates.md`.

The learning order lives in each folder's `INDEX.md`:

| # | Topic | One line | Level | Status | Pre | Created | Updated |
|---|---|---|---|---|---|---|---|
| 1 | `einstein-trust-layer.md` | The masking and audit gate | basic | 🌱 3 open | — | 2026-08-27 | 2026-08-27 |
| 2 | `prompt-template-types.md` | The six types | basic | 🌱 4 open | 1 | 2026-08-27 | 2026-08-27 |

- `#` is the recommended read order.
- `Pre` is the hard prerequisite.
- `Status`, `Created` and `Updated` mirror the note's own metadata.

Above the table, a summary line: **topic count · gaps open · complete · newest · oldest**. That answers "how old is all this?" without opening a note.

Why no numbers in filenames: you will feed a Day-5 topic that belongs at position 3. With numbered filenames that means renaming files and fixing every link. Here it means moving one table row.

`SF_core/PHASES.md` already records renumbering as expensive in that vault. We are not repeating it.

## The archive

`_archive/AI_Data/` holds the old roadmap vault — 24 researched Agentforce and Data 360 topics, the study plan, the labs and the trackers.

It is a **quarry, not a reference.**

- When you feed a topic it already covered, its verified facts get pulled into your new note, **cut to your level**.
- Nothing links back to it. No note says "go read the archive".
- Its glossary and release radar were kept and promoted: [GLOSSARY.md](GLOSSARY.md) and [RELEASE-RADAR/](RELEASE-RADAR/README.md).

## Anything that does not route

Goes to that folder's `_inbox.md`, as one bullet, with the date.

Filing friction must never stop capture. Triage it later.

## Decisions log

| Date | Decision | Why |
|---|---|---|
| 2026-08-27 | `SF/` renamed to `SF_core/` | Makes room for `SF_Agentforce/` and `SF_Data_360/` as peers. 112 links across 23 files repaired in the same pass. |
| 2026-08-27 | New folders start empty | You wanted a vault fed by what you actually learn, not by a generated roadmap. |
| 2026-08-27 | Filenames carry no number | You feed topics in random order. Numbered filenames make every insertion a rename. |
| 2026-08-27 | Light format for all new notes, in every vault | You asked for notes you can recall from, not paragraphs. |
| 2026-08-27 | Existing `SF_core` notes are enriched in place, not duplicated | 238 notes already exist. A second light file beside each would split the topic in two. |
| 2026-08-27 | `AI_Data/` retired to `_archive/` | You said you will not use it for reference or recall. Its glossary and release radar were promoted to the root; ~270 links repointed to the new folders. |
| 2026-08-27 | Archive is a quarry, never a link target | Keeps the research without asking you to read a vault you have abandoned. |
| 2026-08-27 | Dates, derived status, staleness flag, sources and history on every note | You asked to know how old a note is and whether it is finished. Deriving status from the gap checklist stops it going stale. |
| 2026-08-28 | Closed gaps are deleted, not ticked; empty section removed | A checklist of settled questions is clutter. What you learnt goes in the note body. |
| 2026-08-28 | `## History` never records gap counts | It logs what changed, not bookkeeping. |
| 2026-08-27 | Level beats migration depth | A one-line note of yours does not get replaced by 119 lines from the archive. Write at your level; the depth arrives when your notes do. |
