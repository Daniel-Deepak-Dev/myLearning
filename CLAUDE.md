# myLearning — writing rules

These apply to every file in this repo. Each vault adds its own format rules in its own `CLAUDE.md`.

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
| [Interview/](Interview/README.md) | Scenario question bank | Question + model answer + rubric |

Shared at the root: [GLOSSARY.md](GLOSSARY.md) (all terms, greppable) and [RELEASE-RADAR/](RELEASE-RADAR/README.md) (what changed and when — the source of truth for currency).

[_archive/AI_Data/](_archive/AI_Data/) is the retired roadmap vault. It is a **quarry for verified facts, never a link target.** Nothing live should link into it.

## When the user pastes rough learning notes

Run the **`study-notes`** skill. Do not free-hand it.

The full contract is in [NOTES-SYSTEM.md](NOTES-SYSTEM.md). The short version:

- **Route by subtraction:** strip the product out of the sentence. *Still true with no Agentforce in it?* *With no Experience Cloud site in it?* **Still true → `SF_core/`. Falls apart → the vault that owns that product** — `SF_Agentforce/`, `SF_Data_360/` or `SF_Experience_Cloud/`.
- **New notes use the light format** in [_note-template.md](_note-template.md), in every vault.
- **Add gaps, scoped by the note's `Level`.** One level up, never two. Same topic only.
- **Every link out gets a link back**, in the same edit.
- **Every note carries dates and a status.** `Created` never changes, `Updated` does. **Status is derived from the `## Gaps to close` lines** — never typed, and `## Confirm in org` bullets never count. Past 3 months, add the `⏳ N months old` line.
- **A closed gap is deleted, not ticked.** When the last one goes, the `## Gaps to close` section goes too. `## History` says what changed, never a gap count.
- **A question no public doc can answer belongs in `## Confirm in org`**, not in the gap list. Research cannot close it; only an org can.
- **Every note carries 3–4 `## Hands-on` labs**, each with a `Proves:` and a time box, biased towards breaking something on purpose. **Labs are ticked, not deleted.** They queue in the vault's `PRACTICE.md` — see [SF_Agentforce/PRACTICE.md](SF_Agentforce/PRACTICE.md).
- **Every researched fact gets a `## Sources` entry** with the date it was read. Salesforce domains are trusted; anything else carries 🚩.
- **Log the feed** in [LEARNING-LOG.md](LEARNING-LOG.md).
