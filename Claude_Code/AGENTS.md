# Claude_Code — how to write in this folder

Style rules: [../AGENTS.md](../AGENTS.md). How the loop works: [README.md](README.md).

## Scope

Claude Code itself: instructions and memory, settings and permissions, skills and commands, hooks, subagents, output styles, MCP, headless runs and scheduling, plugins.

This folder is a **track, not a vault**. The Salesforce routing test doesn't apply here, and `scripts/vault.py check` lints only its links. The rules below are kept by hand.

## Filing a feed

The user learns a topic, pastes rough notes, and the `study-notes` skill files them here.

1. **Find the note.** If the topic has a note already, update it. Otherwise create `<slug>.md` from [../templates/claude-code-note.md](../templates/claude-code-note.md). File names carry no number; the order lives in the README path table.
2. **Fill the README `Note` cell** for that topic with a link to the note. A topic that isn't listed gets a new row in its logical place, numbered in sequence.
3. **Log the feed** in [../LEARNING-LOG.md](../LEARNING-LOG.md).

## The note format

`## My recall` → `## Key points` → `## Gotchas` → `## Hands-on` → `## Sources` → `## History`

- **Frontmatter is `track`, `created` and `updated`. No `format` key**, so the Obsidian Bases views stay Salesforce-only.
- **`created` is the day the topic was fed.** `npm run today` treats it as the first study date and schedules reviews from it. It never changes. `updated` changes on every edit.
- **40 lines max**, counted to `## Sources`. Bullets, not prose. One table and one code block (12 lines) at most.

## Rules

- **`## My recall` is the user's words.** Tighten, reorder and fix spelling. Never add a word, phrase or fact. A wrong line keeps its wording and gets `🚩 <why>`, and the user fixes it.
- **Everything below `## My recall` is researched**, from the current docs. Never write it from recall: Claude Code changes every few weeks. Fetch through the `claude-code-guide` agent or the docs directly.
- **Every researched fact gets a `## Sources` line** with the date read. Trusted: `code.claude.com`, `docs.claude.com` and `docs.anthropic.com`. Anything else carries 🚩.
- **Unsure of a fact? Mark it 🚩.** Say what you saw and where.
- **`## Hands-on` holds 2–3 labs**, IDs `CC-<TOPIC>-NN`, in the format `- [ ] **CC-HOOK-01** · 30 min · <what you do>. **Proves:** <what it shows>.` Each lab builds or breaks something real in this repo. **Ticked, never deleted.** `npm run today` shows the first unticked lab as the day's **Build** line.
- **No flashcards** for this track yet.
- **`## History`** takes one dated line per feed, saying what was added or changed.
