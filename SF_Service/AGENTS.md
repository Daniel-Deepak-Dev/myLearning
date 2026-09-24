# SF_Service — how to write in this vault

Style rules: [../AGENTS.md](../AGENTS.md). Full contract: [../NOTES-SYSTEM.md](../NOTES-SYSTEM.md).

## Scope

Service Cloud only. Enhanced Chat (formerly Messaging for In-App and Web) and the other messaging channels, Omni-Channel routing and capacity, Omni-Channel flows, Omni Supervisor, bot and agent handoff to a human, the Service Console, case management, entitlements, Knowledge, Service Cloud Voice.

**The routing test:** *is this sentence still true with no Service Cloud in it?*

- **Yes** → it belongs in [../SF_core/](../SF_core/README.md). Write it there and link both ways.
- **No** → it belongs here.

So queues, assignment rules and the grantee model go to `SF_core/`. They also work on Lead, Task and custom objects. *How Omni-Channel pushes a queue's work to a rep* stays here.

**Three neighbours.**

- An **Agentforce Service Agent** is built in [../SF_Agentforce/](../SF_Agentforce/INDEX.md). This vault owns the channel it answers on, the Omni-Channel flow that routes to it, and the handoff to a human.
- The **Enhanced Chat widget on an Experience Cloud site** splits. The channel, deployment and routing are here. The site-side exposure is [../SF_Experience_Cloud/](../SF_Experience_Cloud/INDEX.md) · 19: the Experience Builder component, the guest user and the audit line item.
- **Custom Lightning Types** for chat output are an LWC contract in `SF_core/03-lwc-and-slds/`. *Which Enhanced Chat version renders them* stays here.

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
- **`## Hands-on` holds 3–4 labs**, IDs `SVC-<TOPIC>-NN`, one line each, every one carrying a `Proves:`. **Ticked, never deleted.** Bias to labs that break something on purpose — mine `## Gotchas` for them. New lab → `fix` adds its queue row; you place it in [PRACTICE.md](PRACTICE.md), unblocked-first.
- **Status is derived, never typed.** `python scripts/vault.py fix` counts the `- [ ]` lines in `## Gaps to close` and writes `status: open` + `gaps: N`, or `status: complete`. `## Confirm in org` bullets and `## Hands-on` labs never count.
- **`created` never changes. `updated` changes on every edit.** Staleness is derived from `updated`, not stamped into the note — `HOME.md` lists what has gone 3+ months.
- **Every researched fact gets a `## Sources` line** with the date read. Salesforce domains trusted; anything else carries 🚩.
- **`## History`** takes one dated line per feed, saying what was added or changed — never a gap tally.
- **`Level` sets the gap ceiling.** Gaps may go one level up, never two. A `basic` note never gets a `deep` gap.
- **Gaps stay on this topic.** Never a syllabus. Never another subject.
- **Keep the user's own wording** in a `> **From my notes.**` callout. Correct it inline if it is wrong.
- **A link that crosses vaults gets a link back**, added in the same edit — that means links into `SF_core/`, `SF_Agentforce/`, `SF_Data_360/` and `SF_Experience_Cloud/`. Same-vault links rely on Obsidian's Backlinks panel.
- **Unsure of a fact? Mark it 🚩.** There is no Service Cloud radar file. For release-dependent facts, check [../SF_core/CURRENCY.md](../SF_core/CURRENCY.md) and [../RELEASE-RADAR/agentforce-platform.md](../RELEASE-RADAR/agentforce-platform.md) first. Never draft release facts from recall.

## Four live currency traps

- **Service Cloud is now called Agentforce Service.** Help titles read *"Agentforce Service (formerly Service Cloud)"*, and Service Cloud Voice is now *Salesforce Voice*. This vault keeps writing **Service Cloud** on purpose, because *Agentforce Service* collides with *Agentforce Service Agent*, which is the AI agent rather than the product. Know both names; a search for either should find the note.
- **MIAW is Enhanced Chat.** *Messaging for In-App and Web* was renamed **Enhanced Chat in June 2025**. Salesforce's own docs still use both names. Write Enhanced Chat, and mention the old name once where a note would otherwise be unsearchable → [enhanced-chat.md](enhanced-chat.md).
- **Legacy Chat is retired, not merely legacy.** Chat / Live Agent retired on **14 February 2026** (Help 001790618). Flag any answer that builds on it → [enhanced-chat.md](enhanced-chat.md).
- **There is one Omni-Channel now.** Standard Omni-Channel retired in **Summer '26**; orgs moved to **Enhanced Omni-Channel**. A "standard vs enhanced" choice is a migration question, not a design one → [omni-channel-fundamentals.md](omni-channel-fundamentals.md).

## Housekeeping

- **New topic** → new file, plus a row in [INDEX.md](INDEX.md) at the right point in the path.
- **New jargon** goes in [../GLOSSARY.md](../GLOSSARY.md), in the `## Service Cloud` section. One glossary for all vaults.
- **Does not route cleanly?** One dated bullet in [_inbox.md](_inbox.md). Never let filing friction stop capture.
