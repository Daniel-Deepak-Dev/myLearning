# SF_Agentforce — how to write in this vault

Style rules: [../CLAUDE.md](../CLAUDE.md). Full contract: [../NOTES-SYSTEM.md](../NOTES-SYSTEM.md).

## Scope

Agentforce only. Prompt templates, agents, topics, actions, Agent Script, Atlas Reasoning, Einstein Trust Layer, agent testing and observability.

**The routing test:** *is this sentence still true with no Agentforce in it?*

- **Yes** → it belongs in [../SF_core/](../SF_core/README.md). Write it there and link both ways.
- **No** → it belongs here.

So `@InvocableMethod` signatures and return types go to `SF_core/02-apex-and-triggers/`. *Why an agent action needs one* stays here.

## The note format

Template: [../_note-template.md](../_note-template.md).

`## Key points` → `## Gotchas` → `## Gaps to close` → `## Related`

- **50 lines max.** No paragraph longer than two sentences.
- **One table max. One code block max, 12 lines.**
- **Metadata is a blockquote on lines 3–4.** Never YAML frontmatter.
- **Filenames carry no number.** Order lives in [INDEX.md](INDEX.md).

## Rules

- **Closed gaps are deleted, not ticked.** Answer one, remove the line. Last one gone, remove the `## Gaps to close` heading too.
- **Status is derived, never typed.** Count `- [ ]` lines: some → `🌱 N gaps open`; none, or no section at all → `✅ complete`.
- **`## History` records what was added or changed** — never a gap tally.
- **`Created` never changes. `Updated` changes on every edit.** Past 3 months without a touch, add `> ⏳ N months old — recheck against release notes`. Remove it when the note is updated.
- **Every researched fact gets a `## Sources` line** with the date read. Salesforce domains trusted; anything else carries 🚩.
- **`## History`** takes one dated line per feed.
- **`Level` sets the gap ceiling.** Gaps may go one level up, never two. A `basic` note never gets a `deep` gap.
- **Gaps stay on this topic.** Never a syllabus. Never another subject.
- **Keep the user's own wording** in a `> **From my notes.**` callout. Correct it inline if it is wrong.
- **Every link out gets a link back**, added in the same edit. That includes links into `SF_core/`.
- **Unsure of a fact? Mark it 🚩.** For release-dependent facts, check [../RELEASE-RADAR/agentforce-platform.md](../RELEASE-RADAR/agentforce-platform.md) first. Never draft release facts from recall.
- **Two live currency traps:** agents are authored in **Agent Script** — the legacy topics-and-instructions builder stopped creating new agents the week of 2026-07-13. And **Data Cloud is Data 360**.
- **New topic** → new file, plus a row in [INDEX.md](INDEX.md) at the right point in the path.
- **New jargon** goes in [../GLOSSARY.md](../GLOSSARY.md). One glossary for all vaults.
- **Does not route cleanly?** One dated bullet in [_inbox.md](_inbox.md). Never let filing friction stop capture.
