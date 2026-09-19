# SF_core — how to write in this vault

Style rules: [../AGENTS.md](../AGENTS.md). Full conventions: [README.md](README.md).

## Two note formats live here

- **Existing notes** (the 238 already written) keep the format below. Do not rewrite them wholesale.
- **New notes** use the light format in [../templates/note.md](../templates/note.md): 50 lines, bullets, `## Gaps to close`. Filenames still take the area's next `NN-` prefix.
- **A fed topic that already has a note here** → enrich that note in place. Add the cross-link and a `## Gaps to close` section. Never create a second file for the same topic.

- **Metadata is YAML frontmatter**, read by Obsidian as Properties. `status`, `gaps`, `org_checks` and `labs` are recomputed by `python scripts/vault.py fix`; `vault`, `area`, `format`, `level`, `created`, `currency`, `phase` and `tags` are yours.

Full contract for fed notes: [../NOTES-SYSTEM.md](../NOTES-SYSTEM.md).

## The existing note format

One flat `.md` per topic. Skeleton in [_template.md](_template.md):

`## Core idea` → `## How it works` → `## 2026 currency` → `## Gotchas` → `## Recall` → `## Related`

- **Hard cap ~80 lines.** If it will not fit, the taxonomy is wrong — split the topic.
- **At most one table and one code block (≤15 lines)** in `## How it works`.
- **`## Recall` is 5 `Q:`/`A:` pairs**, kept strict so one Anki script works across the vault.
- **Delete `## 2026 currency`** when nothing has changed. An empty heading is noise.

## Rules

- **🆕 topic → research the release notes before writing. Never draft from recall.**
- **⚠️ topic → the one-line "What changed" correction comes first,** before `## Core idea`.
- **Status flags are load-bearing.** ⬜ means scaffolded, not written, and is excluded from the review rotation. 🌱 means written and being learnt. Never let a ⬜ note read 🌱.
- **Currency: Summer '26 · API 67.0** — see [CURRENCY.md](CURRENCY.md). Winter '27 (68.0) is preview only; nothing here assumes it.
- **Never duplicate currency detail.** Link to [../RELEASE-RADAR/](../RELEASE-RADAR/README.md).
- **Out of scope:** Aura, Visualforce, OmniStudio, Analytics. Agentforce lives in [../SF_Agentforce/](../SF_Agentforce/INDEX.md), Data 360 in [../SF_Data_360/](../SF_Data_360/INDEX.md), **Experience Cloud in [../SF_Experience_Cloud/](../SF_Experience_Cloud/INDEX.md)** — it was area 05 here until 2026-09-19.
- **The line is drawn by artefact.** `SF_core/` owns class names, signatures, exceptions, limits and entitlement. The AI vaults own prompt authoring, agent reasoning and Trust Layer policy; `SF_Experience_Cloud/` owns what a site container does to them. **Ask: strip the product out — is the sentence still true?** *No Agentforce in it? No Experience Cloud site in it?* Still true → it belongs here. Falls apart → it belongs there.
- **The Experience Cloud seam, concretely.** OWD, sharing rules and the grantee model are here, in [07-security-and-sharing/](07-security-and-sharing/INDEX.md); *what a guest user sharing rule may grant* is there. `NavigationMixin` and `ShowToastEvent` are here, in [03-lwc-and-slds/](03-lwc-and-slds/INDEX.md); *which of them work in an LWR container* is there.
- **Link both ways.** When a note here gains a link to `SF_Agentforce/`, `SF_Data_360/` or `SF_Experience_Cloud/`, add the return link in that file in the same edit. Same-vault links do not need one — Obsidian's Backlinks panel shows those for free.
- **New topic** → next number in the area, plus a row in that area's `INDEX.md`.
- **New jargon** goes in [../GLOSSARY.md](../GLOSSARY.md).
- **Commits:** one per phase — `SF: phase NN — <title>`.
