# Flashcards

Interview flashcards for Salesforce, written for **technical architect and senior developer** interviews. One hand-written bank, reviewable in two places:

- **Anki** (desktop, AnkiDroid, AnkiWeb): `npm run cards:sync` pushes the bank in through AnkiConnect.
- **Obsidian**: the files are already in the Spaced Repetition plugin's format. Nothing to build.

Every card links the note that holds the full reasoning. The card is the prompt; the note is the answer you would give out loud.

## What's in the bank

| File | Area › Topic | Foundations | Hard |
|---|---|---|---|
| [core/integration.md](core/integration.md) | Core › Integration | 13 | 13 |
| [data-360.md](data-360.md) | Data 360 › Ingestion & Modelling, Identity Resolution, Insights & Segmentation, Zero Copy, RAG & Vector Search, DevOps & Environments | 12 | 12 |
| [data-360-terminology.md](data-360-terminology.md) | Data 360 › Terminology: one term per card, *what it means* and *what it's used for*. Hard = commonly confused terms | 89 | 12 |

Next: Agentforce, then Service, Sales, Experience Cloud and the other Core topics.

## Levels

- **Foundations**: a must-know concept *and why it matters*, with the exact identifier, limit or setting. If you can't answer these, the Hard cards won't land.
- **Hard**: a scenario, trade-off, failure mode or code review, the way an interviewer actually asks. The question carries the constraints; the answer defends a decision.

## Using it in Anki

### First time

1. Install the **AnkiConnect** add-on in Anki desktop: *Tools → Add-ons → Get Add-ons*, code `2055492159`. Restart Anki.
2. With Anki open, from the repo folder, run:

   ```
   npm run cards:sync:dry
   npm run cards:preset
   ```

   No `npm install` is needed. It only needs Node and Python 3.9+, and finds `py`, `python` or `python3` by itself. Pass extra options after `--`, e.g. `npm run cards:sync -- --vault "My Vault"`.

   The dry run shows what will change. `--preset` creates the **Salesforce Interview** deck options: 10 new cards a day, and leeches tagged rather than suspended.
3. Turn on **FSRS**: *deck options → FSRS → on*, desired retention **0.90**. After about a month of reviews, press **Optimize**. FSRS is a global switch and can't be set by script.
4. Sync Anki (top right) so the cards reach AnkiDroid and AnkiWeb.

After editing the bank, run `sync` again. Cards are matched by ID, so an edited card keeps its review history.

### What you get

- **Decks**: `Salesforce › Core › Integration › Foundations` and `› Hard`. Study a whole topic, or one level of it. Study `Salesforce › Data 360 › Terminology` to drill just the vocabulary.
- **Colour-coded cards**:
  - An accent bar per area: Core blue, Agentforce purple, Data 360 teal, Service green, Sales orange, Experience Cloud pink.
  - A green **FOUNDATIONS** or red **HARD** pill.
  - The breadcrumb *Area › Topic › Subtopic* on every card.
  - Code in a dark block. Night mode is supported on desktop and AnkiDroid.
- **Show hint** (Hard cards): a nudge on the question side, revealed only when you tap it.
- **Type-in answers** for exact limits. Anki compares what you typed with the answer, and AnkiDroid shows a number pad when the answer is numeric. 🚩 Not yet checked on AnkiWeb.
- **Cloze cards** for sequences and lists. Each blank becomes its own card.
- **⚠ Trap** box on the back: the plausible wrong answer an interviewer listens for.
- **📄 Source link** that opens the note in Obsidian. It uses `obsidian://`, so Obsidian must be installed on that device. If your vault folder is not named `myLearning`, sync with `--vault "<name>"`.

### Tags (all automatic)

| Tag | Example | Use it for |
|---|---|---|
| `area::` | `area::core` | one area across all topics |
| `topic::` | `topic::core::integration` | one topic |
| `sub::` | `sub::events-cdc` | one subtopic, e.g. just events |
| `level::` | `level::hard` | a mock interview across everything |
| `kind::` | `kind::scenario`, `concept`, `code`, `cloze`, `exact` | drill one card style |
| `currency::` | `currency::warning` | the 2019–2021 answer is now wrong; `currency::new` = GA'd 2024–2026 |

Tags you add yourself (`leech`, `marked`, anything else) are never touched by sync.

### Filtered decks worth creating

*Tools → Create Filtered Deck*, with these searches:

| Name | Search |
|---|---|
| Mock interview | `deck:Salesforce tag:level::hard` |
| Release traps | `deck:Salesforce tag:currency::warning` |
| Code review drill | `deck:Salesforce tag:kind::code` |
| Weak spots | `deck:Salesforce (prop:lapses>2 OR tag:leech)` |
| Rewrite queue | `deck:Salesforce flag:2` |

AnkiDroid 2.23+ can save these as searches in its Browser.

### Flags (your markers during review)

Rename them once in the desktop Browser (sidebar → Flags → right-click → Rename). 🚩 Whether the names show up in AnkiDroid isn't verified.

| Flag | Meaning | What to do |
|---|---|---|
| 🔴 1 Red | Missed it in a mock interview | Re-read the Source note |
| 🟠 2 Orange | The card itself is wrong or unclear | Fix it **in the bank**, then sync |
| 🟢 3 Green | Interview-ready | — |
| 🔵 4 Blue | Ask me this in a mock | Use it for practice with someone |

### Habits that matter

- **Press Again, not Hard, when you forgot.** FSRS reads Hard as "remembered with effort", so pressing it after a miss makes your intervals far too long.
- **Answer Hard cards out loud** before you flip. On AnkiDroid, the whiteboard is good for sketching an architecture before revealing the answer.
- **Never edit cards in Anki.** The next sync overwrites the edit. Flag it orange and fix it in the bank.

## Using it in Obsidian

Install the **Spaced Repetition** community plugin. The decks appear as `flashcards › core › integration › foundations / hard`. Hint, Trap, Exact and Source lines show on the back of the card. The plugin writes `<!--SR:…-->` schedule comments into these files; sync ignores them. The two apps keep separate schedules, so pick one for daily review.

Useful plugin features:

- **Cram** a topic before an interview: *Spaced Repetition: Cram flashcards in this note*.
- **Context**: the plugin shows the heading path above each question.
- **Statistics**: *Spaced Repetition: View statistics*.

## Writing cards

### Format

```
## Hard

#flashcards/core/integration/hard

### Events & CDC

Question, on one or more lines. <!--id:core-int-014-->
?
Answer: 1–3 lines, plain. Bullets are fine.
Hint: a nudge, Hard cards only.
Trap: the plausible wrong answer.
Exact: 25
Source: [Note title](../../SF_core/<area>/<note>.md)
```

- **The deck comes from the tag line**: `#flashcards/<area>/<topic>/<level>`. Area is one of `core`, `agentforce`, `data-360`, `experience-cloud`, `service`, `sales`; level is `foundations` or `hard`. A `###` heading below it is the subtopic.
- **Cloze cards** have no `?` line. Mark each blank `==text==`. Use `==text;;hint==` for a hint, or `==2;;text==` so all the `2` blanks hide together.
- **`Hint:`, `Trap:`, `Exact:` are optional.** `Source:` is required.
- **No blank lines inside a card.** A blank line ends the card, except inside a fenced code block.
- **No `::` outside backticks.** Obsidian would read it as a single-line card.
- **New card?** Leave the ID off and run `npm run cards:ids`. **Never change or reuse an ID**: it is what links the card to its Anki history.

### Rules

1. **Ground every card in a live note.** Never from recall, never from `_archive/`. If the note doesn't support it, fix the note first.
2. **Short answers.** If an answer needs a paragraph, the reasoning belongs in the note.
3. **A Hard card needs a trap.** If there is no plausible wrong answer, it is a Foundations card.
4. **Currency:** say **Data 360**, not Data Cloud; agents are authored in **Agent Script**.

### Checking

| npm | What it does |
|---|---|
| `npm run cards:check` | IDs, decks, Source links, cloze syntax |
| `npm run cards:ids` | gives new cards an ID |
| `npm run cards:sync:dry` | shows what a sync would change in Anki |
| `npm run cards:sync` | pushes the bank to Anki |
| `npm run cards:preset` | sync, plus the deck-options preset |
| `npm run cards:export` | TSV fallback in `cards/` (note types must exist: run a sync once) |
| `npm run check` | the whole vault check plus the bank check; run before committing |

Without npm, call the scripts directly: `python scripts/flashcards.py check` (or `py -3 …` on Windows).
