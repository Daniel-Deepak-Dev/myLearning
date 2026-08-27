# Interview — Scenario-Based Question Bank

Third vault, alongside [AI_Data/](../AI_Data/README.md) (Agentforce, Data 360, Claude) and [SF_core/](../SF_core/README.md) (core platform). Those two hold knowledge. This one holds **being asked about it under pressure**.

## Why this exists

The recall layer in the other two vaults is atomic — 633 `Q:`/`A:` flashcards and 1196 `## Recall` pairs, every one a single-fact prompt. That trains definitions, and definitions are not what an interview tests. An interview hands you a messy situation with three constraints in tension and watches you reason out loud.

Nothing in the repo rehearsed that. The three `_cert-*/practice-questions.md` files are still empty stubs. This vault is the missing layer, and it runs in both directions: **candidate** (architect interviews) and **interviewer** (screening at Geeksoft).

## Map

| Area | Sets | Drills |
|---|---|---|
| [01-agentforce/](01-agentforce/INDEX.md) | 3 · 12 scenarios | Grounding, actions and orchestration, trust and lifecycle |
| [02-data-360/](02-data-360/INDEX.md) | 3 · 12 scenarios | Ingestion and modeling, identity and segmentation, zero-copy and activation |
| [03-core-platform/](03-core-platform/INDEX.md) | 3 · 12 scenarios | Apex and limits, sharing and security, integration and async |
| [04-cross-domain/](04-cross-domain/INDEX.md) | 1 · 6 scenarios | The architect-level ones that only resolve by spanning all three |
| [WEAK-ANSWERS.md](WEAK-ANSWERS.md) | — | The fumble log. **The most valuable file here after a month of use.** |

**42 scenarios.** Sized for depth, not coverage — each one carries the reasoning, the trap, the follow-up probes and a scoring rubric.

## The two levels

| Level | What makes it this level |
|---|---|
| **Medium** | One domain, one or two constraints. A strong senior dev answers it. Tests whether you know the mechanism. |
| **Complex** | Constraints that genuinely conflict, so there is no clean answer — only a defensible trade-off with its cost named. Tests whether you can architect. |

There are no easy questions here by design. "What is a DMO?" is a flashcard, and it already exists in [AI_Data](../AI_Data/01-data-cloud/03-data-modeling-dso-dlo-dmo/flashcards.md).

## How to use it

**As a candidate.** Read the scenario. Say your answer **out loud** — not in your head, out loud, because the gap between "I know this" and "I can say this" is the entire thing being tested. *Then* open `Model answer`. Every miss goes in [WEAK-ANSWERS.md](WEAK-ANSWERS.md) with a link back to the note to re-study.

**As an interviewer.** Read the scenario aloud, skip `Model answer`, work from `Interviewer rubric`. Each rubric carries a stall-hint so a candidate who freezes on phrasing is not failed for a knowledge gap they do not have.

The answers are collapsed so one file serves both. In VS Code preview (`Ctrl+Shift+V`, already the default via `.vscode/settings.json`) each block folds independently.

## The item format

Skeleton in [_template.md](_template.md). Every scenario:

| Part | Job |
|---|---|
| `**Level:**` + `**Probes:**` | Difficulty, and relative links into the notes the answer is grounded in |
| `**Scenario.**` | Concrete setup — named objects, real volumes, the constraint that makes the obvious fix illegal |
| `**Asked as:**` | The one line an interviewer actually says out loud |
| `<details>` **Model answer** | Lead-with, the reasoning steps, **the trap**, and the follow-ups they will ask |
| `<details>` **Interviewer rubric** | 🟢/🟡/🔴 signals, plus the hint to give if they stall |

`**The trap.**` is the highest-value line in the file. It is the plausible answer that a well-read candidate gives and that is wrong — usually because it solves the surface problem while the real constraint is somewhere else.

`<details>` is the one deliberate deviation from the other vaults' pure markdown. It is what makes a single file work as both self-test and reference.

## Two rules that decide whether this is worth anything

**1. Answers are grounded in the notes, never drafted from recall.** Same rule as [SF_core/_template.md](../SF_core/_template.md) rule 2, and it bites harder here: a wrong answer rehearsed forty times becomes something you say confidently in a real interview. Every `**Probes:**` link is a link the author actually read. Two specific traps, because most material online is on the wrong side of both:

- **Agents are authored in [Agent Script](../AI_Data/02-salesforce-ai/07-agent-script/notes.md).** The *New Agent* button stopped opening the topic-and-instruction builder the week of **July 13, 2026**. An answer that walks through topics and instructions as the current model is describing a retired product.
- **Data Cloud is Data 360.** The rename is real — SKUs, release notes, the certification. Folder paths here keep the old name only where links would break.

**2. If the note does not support it, flag it 🚩 rather than invent it.** Already the repo's marker for exactly this — see the unverified domain weights at [02-salesforce-ai/INDEX.md](../AI_Data/02-salesforce-ai/INDEX.md). An answer carrying 🚩 is one to verify in an org before saying it to an interviewer.

## Flag legend

Same meanings as the other two vaults:

| Flag | Meaning |
|---|---|
| 🆕 | Turns on something that GA'd 2024–2026. Most online prep material has not caught up. |
| ⚠️ | The pre-2022 answer is now **wrong**, and the wrong answer is the well-known one. |
| 🚩 | A claim in the answer is **unverified** — status disputed between sources, or not yet confirmed in an org. |

## Conventions

- **Naming:** `NN-kebab-case.md` inside `NN-kebab-case/` areas — the flat [SF_core/](../SF_core/README.md) shape, since a question set needs one file, not four.
- **Metadata:** blockquote on line 3, never YAML frontmatter.
- **Links:** relative markdown only. Every answer links out to the note instead of restating it — [SF_core/_template.md](../SF_core/_template.md) rule 5. This vault holds *questions*, not a third copy of the knowledge.
- **New scenario:** append to the set file it belongs to, renumber nothing, bump the `Scenarios:` count in the line-3 blockquote and the area `INDEX.md`.
- **New set:** next `NN` in the area, copy [_template.md](_template.md), add a row to the area's `INDEX.md`.
- **Currency:** content is current to **Summer '26 (API 67.0)**. [AI_Data/05-release-radar/](../AI_Data/05-release-radar/README.md) is the source of truth for what changed — when a scenario goes stale, fix it there first and here second.
