# SF_Agentforce — how to write in this vault

Style rules: [../AGENTS.md](../AGENTS.md). Full contract: [../NOTES-SYSTEM.md](../NOTES-SYSTEM.md).

## Scope

Agentforce only. Prompt templates, agents, topics, actions, Agent Script, Atlas Reasoning, Einstein Trust Layer, agent testing and observability.

**The routing test:** *is this sentence still true with no Agentforce in it?*

- **Yes** → it belongs in [../SF_core/](../SF_core/README.md). Write it there and link both ways.
- **No** → it belongs here.

So `@InvocableMethod` signatures and return types go to `SF_core/02-apex-and-triggers/`. *Why an agent action needs one* stays here.

**One more neighbour.** An agent **embedded on an Experience Cloud site** splits: the agent, its topics and actions are built here; the site-side exposure — the channel, the guest surface, the audit line item — is [../SF_Experience_Cloud/](../SF_Experience_Cloud/INDEX.md).

## The note format

Template: [../templates/note.md](../templates/note.md).

`## Key points` → `## Gotchas` → `## Gaps to close` → `## Confirm in org` → `## Hands-on` → `## Related`

- **50 lines max, counted to `## Related`.** The `## Related` / `## Sources` / `## History` footer does not count. No paragraph longer than two sentences.
- **One table max. One code block max, 12 lines.**
- **Metadata is YAML frontmatter**, read by Obsidian as Properties. `status`, `gaps`, `org_checks` and `labs` are recomputed by `scripts/vault.py fix`; every other key is yours. See [NOTES-SYSTEM.md](../NOTES-SYSTEM.md).
- **Filenames carry no number.** Order lives in [INDEX.md](INDEX.md).

## Rules

- **Closed gaps are deleted, not ticked.** Answer one, remove the line. Last one gone, remove the `## Gaps to close` heading too.
- **A question no public doc answers goes in `## Confirm in org`**, as a `- 🚩 ` bullet naming what to open. It is a sandbox to-do, not a gap.
- **`## Hands-on` holds 3–4 labs**, IDs `AF-<TOPIC>-NN`, one line each, every one carrying a `Proves:`. **Ticked, never deleted.** Bias to labs that break something on purpose — mine `## Gotchas` for them. New lab → `fix` adds its queue row; you place it in the queue, unblocked-first.
- **Status is derived, never typed.** `python scripts/vault.py fix` counts the `- [ ]` lines in `## Gaps to close` and writes `status: open` + `gaps: N`, or `status: complete`. `## Confirm in org` bullets and `## Hands-on` labs never count. The 🌱/✅ glyphs are how `INDEX.md` renders it, never what the note stores.
- **`## History` records what was added or changed** — never a gap tally.
- **`created` never changes. `updated` changes on every edit.** Staleness is derived from `updated`, not stamped into the note — `HOME.md` lists what has gone 3+ months.
- **Every researched fact gets a `## Sources` line** with the date read. Salesforce domains trusted; anything else carries 🚩.
- **`## History`** takes one dated line per feed.
- **`Level` sets the gap ceiling.** Gaps may go one level up, never two. A `basic` note never gets a `deep` gap.
- **Gaps stay on this topic.** Never a syllabus. Never another subject.
- **Keep the user's own wording** in a `> **From my notes.**` callout. Correct it inline if it is wrong.
- **A link that crosses vaults gets a link back**, added in the same edit — that means links into `SF_core/` and `SF_Experience_Cloud/`. Same-vault links rely on Obsidian's Backlinks panel.
- **Unsure of a fact? Mark it 🚩.** For release-dependent facts, check [../RELEASE-RADAR/agentforce-platform.md](../RELEASE-RADAR/agentforce-platform.md) first. Never draft release facts from recall.
- **Two live currency traps:** agents are authored in **Agent Script** — the legacy topics-and-instructions builder stopped creating new agents the week of 2026-07-13. And **Data Cloud is Data 360**.
- **New topic** → new file, plus a row in [INDEX.md](INDEX.md) at the right point in the path.
- **New jargon** goes in [../GLOSSARY.md](../GLOSSARY.md). One glossary for all vaults.
- **Does not route cleanly?** One dated bullet in [_inbox.md](_inbox.md). Never let filing friction stop capture.
