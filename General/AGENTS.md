# General — how to write in this folder

Style rules: [../AGENTS.md](../AGENTS.md). How the loop works: [README.md](README.md).

## Scope

Anything the user learns that is **not Salesforce and not Claude Code**. Money, history, health, a language, cooking, or general tech such as Git or networking.

Ask in this order:

1. **About Salesforce?** → the Salesforce vaults, by the routing test in [../NOTES-SYSTEM.md](../NOTES-SYSTEM.md).
2. **About Claude Code?** → [../Claude_Code/](../Claude_Code/README.md).
3. **Neither** → here.

General tech that Salesforce happens to use, such as OAuth 2.0, REST or JavaScript promises, lands here only when the notes never mention Salesforce. If they name a Salesforce feature, it is a Salesforce note.

This folder is **not a vault**. The routing test, gaps, org checks, labs and flashcards don't apply. `scripts/vault.py check` lints only its links. The rules below are kept by hand.

## Filing a feed

1. **Split** the dump into topics. One topic, one note.
2. **Pick the subject.** List `General/` first and reuse a folder that fits. Otherwise create one: a broad, kebab-case noun such as `finance`, `history`, `health` or `programming`. A subject is wider than a topic: `finance/`, not `index-funds/`. One level deep, no nested subjects.
3. **Search before writing.** Grep `General/` for the topic's key terms. Found a note → update it. Nothing → create `<subject>/<topic-slug>.md` from [../templates/general-note.md](../templates/general-note.md). Filenames carry no number.
4. **A stray fact with no topic of its own** goes into the closest note in that subject. If there is none, it gets its own note. One recall line is enough.
5. **Run `npm run vault:home`.** It rebuilds [INDEX.md](INDEX.md) from the notes. Never edit the index by hand.
6. **Log the feed** in [../LEARNING-LOG.md](../LEARNING-LOG.md).

**English learning** has scoped practice rules in [english/AGENTS.md](english/AGENTS.md) and a guide in [english/README.md](english/README.md). Read those before coaching or filing English notes. The user has requested speaking and grammar practice with Tamil support.

## The note format

`## My recall` → `## My code` (optional) → `## Key points` → `## Related` (optional) → `## Sources` → `## History`

- **Frontmatter is `track: general`, `created` and `updated`.** No `format` key, so the Obsidian Bases views stay Salesforce-only. The subject is the folder; don't repeat it in the frontmatter.
- **`created` is the day the topic was fed.** `npm run today` counts it as the first study and schedules reviews from it. English is the exception: prepared lessons need a spoken-practice tick in the journal. `created` never changes. `updated` changes on every edit.
- **`**One line:**` under the title is required.** INDEX.md shows it next to the link.
- **30 lines max**, counted to `## Related`. Bullets, not prose. One table and one code block (12 lines) at most.

## Rules

- **`## My recall` is the user's words.** Tighten, reorder and fix spelling. Never add a word, phrase or fact. A wrong line keeps its wording and gets `🚩 <why>`, and the user fixes it. 1–7 lines of `**cue** — power words`. No links, tables or code inside it.
- **`## Key points` is researched**: 3–6 bullets at the user's depth. Check their claims against a source, and add what the topic plainly needs. Never a syllabus.
- **A question in the user's notes** gets answered in `## Key points`, with a source. If no source settles it, write it there as `🚩 Open: <question>`.
- **Every researched fact gets a `## Sources` line** with the date read. Trusted: primary sources, meaning official docs, standards bodies, government and public institutions, peer-reviewed papers and the original author. Anything else carries 🚩.
- **Unsure of a fact? Mark it 🚩.** Say what you saw and where.
- **No labs, gaps, org checks or flashcards.** If the user wants to practise a topic, they will ask.
- **English practice is requested.** Its notes may add `## Say it aloud` between Key points and Related, within the same 30-line cap. See its scoped rules.
- **Links out are one-way.** A note here may link to a Salesforce vault note. That note needs no link back.
- **`## History`** takes one dated line per feed, saying what was added or changed.
