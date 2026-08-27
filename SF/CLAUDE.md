# SF — how to write in this vault

Style rules: [../CLAUDE.md](../CLAUDE.md). Full conventions: [README.md](README.md).

## The note format

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
- **Out of scope:** Aura, Visualforce, OmniStudio, Analytics. Agentforce, Data 360 and Claude live in [../AI_Data/](../AI_Data/README.md). **The line is drawn by artefact:** `SF/` owns class names, signatures, exceptions, limits and entitlement; `AI_Data/` owns prompt authoring, agent reasoning and Trust Layer policy. If a sentence is still true with no Apex in it, it belongs there.
- **New topic** → next number in the area, plus a row in that area's `INDEX.md`.
- **New jargon** goes in [../AI_Data/GLOSSARY.md](../AI_Data/GLOSSARY.md).
- **Commits:** one per phase — `SF: phase NN — <title>`.
