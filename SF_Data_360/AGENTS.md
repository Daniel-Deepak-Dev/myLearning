# SF_Data_360 — how to write in this vault

Style rules: [../AGENTS.md](../AGENTS.md). Full contract: [../NOTES-SYSTEM.md](../NOTES-SYSTEM.md).

## Scope

Data 360 only. Ingestion and connectors, DSO/DLO/DMO modelling, identity resolution, calculated insights, segmentation, zero-copy and BYOL, vector search, RAG on platform, Data 360 DevOps.

**The routing test:** *is this sentence still true with no Data 360 in it?*

- **Yes** → it belongs in [../SF_core/](../SF_core/README.md). Write it there and link both ways.
- **No** → it belongs here.

So SOQL syntax and Bulk API limits go to `SF_core/`. *How a DMO maps back to a Salesforce object* stays here.

## The note format

Template: [../templates/note.md](../templates/note.md).

`## Key points` → `## Gotchas` → `## Gaps to close` → `## Confirm in org` → `## Hands-on` → `## Related` → `## Sources` → `## History`

- **50 lines max.** No paragraph longer than two sentences.
- **One table max. One code block max, 12 lines.**
- **Metadata is YAML frontmatter**, read by Obsidian as Properties. `status`, `gaps`, `org_checks` and `labs` are recomputed by `scripts/vault.py fix`; every other key is yours. See [NOTES-SYSTEM.md](../NOTES-SYSTEM.md).
- **Filenames carry no number.** Order lives in [INDEX.md](INDEX.md).

## Rules

- **Closed gaps are deleted, not ticked.** Answer one, remove the line. Last one gone, remove the `## Gaps to close` heading too.
- **Status is derived, never typed.** `python scripts/vault.py fix` counts the `- [ ]` lines in `## Gaps to close` and writes `status: open` + `gaps: N`, or `status: complete`. `## Confirm in org` bullets and `## Hands-on` labs never count. The 🌱/✅ glyphs are how `INDEX.md` renders it, never what the note stores.
- **`## History` records what was added or changed** — never a gap tally.
- **`created` never changes. `updated` changes on every edit.** Staleness is derived from `updated`, not stamped into the note — `HOME.md` lists what has gone 3+ months.
- **Every researched fact gets a `## Sources` line** with the date read. Salesforce domains trusted; anything else carries 🚩.
- **`## History`** takes one dated line per feed.
- **`Level` sets the gap ceiling.** Gaps may go one level up, never two. A `basic` note never gets a `deep` gap.
- **Gaps stay on this topic.** Never a syllabus. Never another subject.
- **Keep the user's own wording** in a `> **From my notes.**` callout. Correct it inline if it is wrong.
- **A link that crosses vaults gets a link back**, added in the same edit — that means links into `SF_core/`, `SF_Agentforce/`, `SF_Experience_Cloud/`, `SF_Service/` and `SF_Sales/`. Same-vault links rely on Obsidian's Backlinks panel.
- **Unsure of a fact? Mark it 🚩.** For release-dependent facts, check [../RELEASE-RADAR/data-360.md](../RELEASE-RADAR/data-360.md) first. Never draft release facts from recall.
- **Naming:** the product is **Data 360**. Write Data 360, not Data Cloud. Mention the old name once where a note would otherwise be unsearchable.
- **New topic** → new file, plus a row in [INDEX.md](INDEX.md) at the right point in the path.
- **New jargon** goes in [../GLOSSARY.md](../GLOSSARY.md). One glossary for all vaults.
- **Does not route cleanly?** One dated bullet in [_inbox.md](_inbox.md). Never let filing friction stop capture.
