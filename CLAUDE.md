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
| [SF_core/](SF_core/README.md) | Core platform: Apex, LWC, Flow, Admin, Experience Cloud, Integration, Security, Data, DevOps | One flat note per topic |
| [SF_Agentforce/](SF_Agentforce/INDEX.md) | Agentforce only: prompt templates, agents, actions, Trust Layer, Atlas | Light format |
| [SF_Data_360/](SF_Data_360/INDEX.md) | Data 360 only: ingestion, DMOs, identity resolution, segments, RAG | Light format |
| [AI_Data/](AI_Data/README.md) | The AI-Architect roadmap, Claude, capstone, release radar | Folder per topic, four files |
| [Interview/](Interview/README.md) | Scenario question bank | Question + model answer + rubric |

## When the user pastes rough learning notes

Run the **`study-notes`** skill. Do not free-hand it.

The full contract is in [NOTES-SYSTEM.md](NOTES-SYSTEM.md). The short version:

- **Route with one question:** *is this sentence still true with no Agentforce in it?* Yes → `SF_core/`. No → `SF_Agentforce/` or `SF_Data_360/`.
- **New notes use the light format** in [_note-template.md](_note-template.md), in every vault.
- **Add gaps, scoped by the note's `Level`.** One level up, never two. Same topic only.
- **Every link out gets a link back**, in the same edit.
- **Log the feed** in [LEARNING-LOG.md](LEARNING-LOG.md).
