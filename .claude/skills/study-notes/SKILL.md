---
name: study-notes
description: Turn rough, out-of-order Salesforce learning notes into ordered wiki notes across SF_core, SF_Agentforce and SF_Data_360. Use whenever the user pastes study notes, says "I learned X today", dumps rough bullets about a Salesforce, Agentforce or Data 360 topic, or asks to file notes into the vault.
allowed-tools: Read, Write, Edit, Grep, Glob, WebFetch, AskUserQuestion
---

The user pastes rough notes. You file them.

Their notes arrive in whatever order they learned things. Your job is to put each piece in the right file, in an order they can learn from later.

Read [NOTES-SYSTEM.md](../../../NOTES-SYSTEM.md) once per session for the full contract. This file is the procedure.

## 1 · Split

Break the dump into distinct topics. One topic, one note.

A single sentence can belong to two topics. That is normal. Split it and cross-link.

Do not merge unrelated things into one file just because they arrived together.

## 2 · Route

One question per piece:

> **Is this sentence still true with no Agentforce in it?**

- **Yes** → `SF_core/`, in the numbered area it fits.
- **No** → `SF_Agentforce/` or `SF_Data_360/`.

If a topic has both sides — say "a prompt template can call Apex" — write **both** notes. The Agentforce note says why. The `SF_core` note says how. They link to each other.

Cannot route it? One dated bullet in that folder's `_inbox.md`. Move on. Never stall.

## 3 · Check before you write

Always search first. Duplicates are the main failure mode here.

- `Glob` the target folder for a matching filename.
- `Grep` all four vaults for the topic's key terms: `SF_core/`, `SF_Agentforce/`, `SF_Data_360/`, `AI_Data/`.

Then decide:

| Found | Do |
|---|---|
| A note in the target folder | **Update it.** Merge the new facts in. Raise `Level` if the notes went deeper. |
| A note in `SF_core/` in the old dense format | **Enrich it in place.** Add the cross-link and a `## Gaps to close` section. Do not create a second light file beside it. |
| Only an `AI_Data/` note | **Migrate.** Fold the useful parts into the new note. Leave a one-line pointer in the `AI_Data` file. |
| Nothing | **Create it.** |

## 4 · Write

Use [_note-template.md](../../../_note-template.md).

- Filenames carry **no number**. `flex-prompt-templates.md`, not `05-flex-prompt-templates.md`.
- **50 lines max.** No paragraph longer than two sentences.
- One table max. One code block max, 12 lines.
- Metadata is a blockquote on line 3. Never YAML frontmatter.

Keep the user's own wording where it captures a real gotcha:

```markdown
> **From my notes.** <their words> — <inline correction if it is wrong>
```

That callout is how they tell what they wrote from what you added. Use it.

Set `Level` from the depth of what they actually gave you:

- `basic` — what it is, where to find it, what it is for.
- `working` — configuration, types, limits, when to pick which.
- `deep` — code, API surface, edge cases, performance.

## 5 · Gap pass

This is the part the user cares about most. Get the scope right.

> **Gaps may go ONE level above the note's `Level`. Never two.**

| Note is | Gaps may be |
|---|---|
| `basic` | basic, working |
| `working` | working, deep |
| `deep` | anything on this topic |

A `basic` prompt-template note gets gaps like *"can Sales Email ground on Lead as well as Contact?"*

It does **not** get `@InvocableMethod`. That is `deep`, two levels up. Hold it back until the note's level rises.

Also:

- **Same topic only.** Never a syllabus. Never "you should also learn Data 360."
- **Be specific.** Name the object, setting, limit or field. A gap that could apply to any topic is not worth a line.
- **Documentation considerations count.** Supported objects, limits, licence requirements, known restrictions — these are good gaps when the user's note skipped them.
- Put the checklist under `## Gaps to close`.
- Put a `> **Gap.**` callout inline instead when the hole sits mid-topic and would confuse the bullets around it.

## 6 · Link both ways

Every link out gets a link back. In the same edit.

Write the Agentforce note's `## Related` bullet pointing at the Apex note. Then open the Apex note and add its bullet pointing back.

Skipping the return link is the one mistake that quietly breaks the whole system.

Relative markdown links only. No `[[wiki links]]` — nothing in this repo uses them.

## 7 · Update the indexes

For each note you created or moved:

- Insert or move its row in the folder's `INDEX.md`, at the right point in the learning path.
- Fill `#`, `Topic`, `One line`, `Level`, `Prereq`, `Fed`.
- Renumber the `#` column only. **Never rename a file to reorder.**
- Update the topic count line.

Then add a dated entry to `LEARNING-LOG.md`, newest first.

## 8 · Facts you are not sure of

- Release-dependent or version-dependent → check `AI_Data/05-release-radar/` first. It is the repo's source of truth for what changed and when.
- Still unsure → `WebFetch` `help.salesforce.com` or `developer.salesforce.com`.
- Cannot confirm → write it with 🚩, or with the suffix `*(unverified — confirm in org)*`.
- **Never invent a Salesforce feature, limit or object name.** A wrong fact learned confidently is worse than a gap.
- Never use 🆕 or ⚠️ as confidence markers. Those mean something specific in the `SF_core/README.md` flag legend.

Two live currency traps to watch for in the user's notes:

- Agents are authored in **Agent Script**. The legacy topics-and-instructions builder stopped creating new agents the week of 2026-07-13.
- **Data Cloud is Data 360.**

If their note contradicts one of these, correct it inline in the `> **From my notes.**` callout. Do not silently drop what they wrote.

## 9 · Report back

Short. Bullets. No paragraphs.

- Files created, with paths.
- Files updated, and what changed in each.
- Gaps added, and the level you scoped them to.
- Reciprocal links added.
- Anything sent to `_inbox.md`, and why.
- Anything you marked 🚩 and want them to confirm in an org.

Ask a question only when routing is genuinely ambiguous. Otherwise decide, file it, and say what you decided.
