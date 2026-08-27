# SF_Data_360 — how to write in this vault

Style rules: [../CLAUDE.md](../CLAUDE.md). Full contract: [../NOTES-SYSTEM.md](../NOTES-SYSTEM.md).

## Scope

Data 360 only. Ingestion and connectors, DSO/DLO/DMO modelling, identity resolution, calculated insights, segmentation, zero-copy and BYOL, vector search, RAG on platform, Data 360 DevOps.

**The routing test:** *is this sentence still true with no Data 360 in it?*

- **Yes** → it belongs in [../SF_core/](../SF_core/README.md). Write it there and link both ways.
- **No** → it belongs here.

So SOQL syntax and Bulk API limits go to `SF_core/`. *How a DMO maps back to a Salesforce object* stays here.

## The note format

Template: [../_note-template.md](../_note-template.md).

`## Key points` → `## Gotchas` → `## Gaps to close` → `## Related`

- **50 lines max.** No paragraph longer than two sentences.
- **One table max. One code block max, 12 lines.**
- **Metadata is a blockquote on line 3.** Never YAML frontmatter.
- **Filenames carry no number.** Order lives in [INDEX.md](INDEX.md).

## Rules

- **`Level` sets the gap ceiling.** Gaps may go one level up, never two. A `basic` note never gets a `deep` gap.
- **Gaps stay on this topic.** Never a syllabus. Never another subject.
- **Keep the user's own wording** in a `> **From my notes.**` callout. Correct it inline if it is wrong.
- **Every link out gets a link back**, added in the same edit. That includes links into `SF_core/` and `SF_Agentforce/`.
- **Unsure of a fact? Mark it 🚩.** For release-dependent facts, check [../AI_Data/05-release-radar/data-360.md](../AI_Data/05-release-radar/data-360.md) first. Never draft release facts from recall.
- **Naming:** the product is **Data 360**. Write Data 360, not Data Cloud. Mention the old name once where a note would otherwise be unsearchable.
- **New topic** → new file, plus a row in [INDEX.md](INDEX.md) at the right point in the path.
- **New jargon** goes in [../AI_Data/GLOSSARY.md](../AI_Data/GLOSSARY.md). One glossary for all vaults.
- **Does not route cleanly?** One dated bullet in [_inbox.md](_inbox.md). Never let filing friction stop capture.
