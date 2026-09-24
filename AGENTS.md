# myLearning — writing rules

> **Start at [HOME.md](HOME.md)** — what to study next, rebuilt from the notes.

These apply to every file in this repo. Each vault adds its own format rules in its own `AGENTS.md`.

## Style

- **Plain language, short sentences.** No dense or overly compressed phrasing. If a sentence needs a second read, split it.
- **No filler or hype.** Cut empty intros, "it's important to note", marketing tone and padding. Say the thing.
- **Concrete over abstract.** Name the exact identifier, limit, setting, API version or error string. "Governor limit" is vague; "101 SOQL queries" is not.
- **Say when unsure.** If a source does not support a claim, mark it 🚩 rather than write confident prose. 🚩 is already this repo's marker for that.

## The vaults

| Vault | Owns | Note format |
|---|---|---|
| [SF_core/](SF_core/README.md) | Core platform: Apex, LWC, Flow, Admin, Integration, Security, Data, DevOps | One flat note per topic |
| [SF_Agentforce/](SF_Agentforce/INDEX.md) | Agentforce only: prompt templates, agents, actions, Trust Layer, Atlas | Light format |
| [SF_Data_360/](SF_Data_360/INDEX.md) | Data 360 only: ingestion, DMOs, identity resolution, segments, RAG | Light format |
| [SF_Experience_Cloud/](SF_Experience_Cloud/INDEX.md) | Experience Cloud only: LWR & Aura sites, guest security, external licences, CMS, headless, site DevOps | Dense for the 20 phase-18/19 notes; light for new ones |
| [SF_Service/](SF_Service/INDEX.md) | Service Cloud only: Enhanced Chat & messaging, Omni-Channel routing, Omni Supervisor, bot-to-human handoff | Light format |
| [Interview/](Interview/README.md) | Scenario question bank | Question + model answer + rubric |

Shared at the root: [GLOSSARY.md](GLOSSARY.md) (all terms, greppable) and [RELEASE-RADAR/](RELEASE-RADAR/README.md) (what changed and when — the source of truth for currency).

[_archive/AI_Data/](_archive/AI_Data/) is the retired roadmap vault. It is a **quarry for verified facts, never a link target.** Nothing live should link into it.

## When the user pastes rough learning notes

Run the **`study-notes`** skill. Do not free-hand it.

The full contract is in [NOTES-SYSTEM.md](NOTES-SYSTEM.md). The short version:

- **Route by subtraction:** strip the product out of the sentence. *Still true with no Agentforce in it?* *With no Experience Cloud site in it?* *With no Service Cloud in it?* **Still true → `SF_core/`. Falls apart → the vault that owns that product** — `SF_Agentforce/`, `SF_Data_360/`, `SF_Experience_Cloud/` or `SF_Service/`.
- **New notes use the light format** in [templates/note.md](templates/note.md), in every vault. Start there → [HOME.md](HOME.md) is the front door.
- **Add gaps, scoped by the note's `Level`.** One level up, never two. Same topic only.
- **A link that crosses vaults gets a link back**, in the same edit. Same-vault links rely on Obsidian's Backlinks panel.
- **Metadata is YAML frontmatter.** `status`, `gaps`, `org_checks` and `labs` are recomputed by `python scripts/vault.py fix`; every other key is yours. `created` never changes, `updated` does. Staleness is derived from `updated`, never stamped.
- **A closed gap is deleted, not ticked.** When the last one goes, the `## Gaps to close` section goes too. `## History` says what changed, never a gap count.
- **A question no public doc can answer belongs in `## Confirm in org`**, not in the gap list. Research cannot close it; only an org can.
- **Every note carries 3–4 `## Hands-on` labs**, each with a `Proves:` and a time box, biased towards breaking something on purpose. **Labs are ticked, not deleted.** They queue in the vault's `PRACTICE.md` — see [SF_Agentforce/PRACTICE.md](SF_Agentforce/PRACTICE.md).
- **Every researched fact gets a `## Sources` entry** with the date it was read. Salesforce domains are trusted; anything else carries 🚩.
- **Log the feed** in [LEARNING-LOG.md](LEARNING-LOG.md).
