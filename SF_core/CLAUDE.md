# SF_core — how to write in this vault

Style rules: [../CLAUDE.md](../CLAUDE.md). Full conventions: [README.md](README.md).

## Two note formats live here

- **Existing notes** (the 238 already written) keep the format below. Do not rewrite them wholesale.
- **New notes** use the light format in [../_note-template.md](../_note-template.md): 50 lines, bullets, `## Gaps to close`. Filenames still take the area's next `NN-` prefix.
- **A fed topic that already has a note here** → enrich that note in place. Add the cross-link and a `## Gaps to close` section. Never create a second file for the same topic.

Full contract for fed notes: [../NOTES-SYSTEM.md](../NOTES-SYSTEM.md).

## The existing note format

One flat `.md` per topic. Skeleton in [_template.md](_template.md):

`## Core idea` → `## How it works` → `## 2026 currency` → `## Gotchas` → `## Recall` → `## Related`

- **Hard cap ~80 lines.** If it will not fit, the taxonomy is wrong — split the topic.
- **At most one table and one code block (≤15 lines)** in `## How it works`.
- **`## Recall` is 5 `Q:`/`A:` pairs**, same format as AI_Data flashcards so one Anki script works across both vaults.
- **Delete `## 2026 currency`** when nothing has changed. An empty heading is noise.

## Rules

- **🆕 topic → research the release notes before writing. Never draft from recall.**
- **⚠️ topic → the one-line "What changed" correction comes first,** before `## Core idea`.
- **Status flags are load-bearing.** ⬜ means scaffolded, not written, and is excluded from the review rotation. 🌱 means written and being learnt. Never let a ⬜ note read 🌱.
- **Currency: Summer '26 · API 67.0** — see [CURRENCY.md](CURRENCY.md). Winter '27 (68.0) is preview only; nothing here assumes it.
- **Never duplicate currency detail.** Link to [../AI_Data/05-release-radar/](../AI_Data/05-release-radar/README.md).
- **Out of scope:** Aura, Visualforce, OmniStudio, Analytics. Agentforce lives in [../SF_Agentforce/](../SF_Agentforce/INDEX.md), Data 360 in [../SF_Data_360/](../SF_Data_360/INDEX.md), Claude and the roadmap in [../AI_Data/](../AI_Data/README.md).
- **The line is drawn by artefact.** `SF_core/` owns class names, signatures, exceptions, limits and entitlement. The AI vaults own prompt authoring, agent reasoning and Trust Layer policy. **Ask: is this sentence still true with no Agentforce in it?** Yes → it belongs here. No → it belongs there.
- **Link both ways.** When a note here gains a link to `SF_Agentforce/` or `SF_Data_360/`, add the return link in that file in the same edit. One-way links break the wiki.
- **New topic** → next number in the area, plus a row in that area's `INDEX.md`.
- **New jargon** goes in [../AI_Data/GLOSSARY.md](../AI_Data/GLOSSARY.md).
- **Commits:** one per phase — `SF: phase NN — <title>`.
