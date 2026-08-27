# Interview — how to write in this vault

Style rules: [../CLAUDE.md](../CLAUDE.md). Full conventions: [README.md](README.md).

## The item format

Skeleton in [_template.md](_template.md). Every scenario, in this order:

`**Level:**` + `**Probes:**` → `**Scenario.**` → `**Asked as:**` → `<details>` **Model answer** → `<details>` **Interviewer rubric**

- **Both lenses on every item.** A model answer without a rubric makes the file single-purpose.
- **`**The trap.**` is mandatory** and is the point of the item — the plausible answer a well-read candidate gives that is wrong. If there is no plausible wrong answer, the scenario is too easy: add a constraint or drop it.
- **Keep the `<details>` blocks.** They are the one deliberate deviation from the other vaults' pure markdown, and they are what makes one file serve both candidate and interviewer.
- **Metadata is a blockquote on line 3.** Never YAML frontmatter.

## Rules

- **Ground every answer in the linked notes. Never draft from recall.** A wrong answer rehearsed forty times becomes something said confidently in a real interview. Every `**Probes:**` link is a note actually read.
- **If the note does not support a claim, flag it 🚩** rather than invent it.
- **Link out, never restate.** This vault holds questions; [../AI_Data/](../AI_Data/README.md) and [../SF/](../SF/README.md) hold the knowledge.
- **No easy questions.** "What is a DMO?" is a flashcard and already exists in the other vaults.
- **Two currency traps:** agents are authored in Agent Script — the legacy builder stopped creating new agents the week of 2026-07-13 — and Data Cloud is Data 360.
- **New scenario** → append to the set file it belongs to, renumber nothing, bump the `Scenarios:` count in the line-3 blockquote **and** in the area `INDEX.md`.
- **New set** → next `NN` in the area, copy [_template.md](_template.md), add a row to the area's `INDEX.md`.
- **Misses go in** [WEAK-ANSWERS.md](WEAK-ANSWERS.md), with a link back to the note to re-study.
