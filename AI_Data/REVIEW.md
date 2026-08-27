# REVIEW — the only file you open when the goal is *recall*

> **Three rules.** One unit per session. 20-minute box. Every miss gets logged.
>
> If you catch yourself *adding* cards instead of answering them, you are in the wrong file.
> That one is the topic's own `flashcards.md`, and it is the end of a study session — not this.

The cards already exist: **1,848** of them, every one in strict `Q:`/`A:` format. Nothing here
creates content. This file decides *what you answer today* and remembers *what you got wrong*.

Recall is the twin of [PRACTICE.md](PRACTICE.md), and the split is the same one that runs
everywhere else in this repo: PRACTICE is where a claim gets **verified**, REVIEW is where it
gets **retained**. Neither substitutes for the other.

---

## ▶ This week

Three units. Do them in any order, one per sitting.

1. **[02-salesforce-ai/03-prompt-builder](02-salesforce-ai/03-prompt-builder/cheatsheet.md)** —
   studied externally in August and never tested. Start here.
2. **[02-salesforce-ai/02-agentforce-anatomy](02-salesforce-ai/02-agentforce-anatomy/cheatsheet.md)** —
   Atlas 3.0 and the legacy-vs-Agent-Script split. The thing most tutorials still get wrong.
3. **SF_core · `02-apex-and-triggers` notes 22, 31, 32, 33, 34** — the Apex-side prompt trio plus
   Models API and LLM mocking. Same subject as unit 1, opposite artefact.

---

## How a session runs

Twenty minutes, four steps, no variations.

1. **Read the `cheatsheet.md` cold.** 5 minutes. Do not open `notes.md` — if the cheatsheet
   cannot reload the topic on its own, that is a finding about the cheatsheet, and it goes in
   the miss log like anything else.
2. **Cover the `A:` column** in `flashcards.md` (or the `## Recall` block in an `SF_core/` note) and
   answer **out loud**. Out loud is not a flourish — silent recognition feels like knowing and
   is not, and an interview is spoken.
3. **Log every miss** in `## Misses` below. One line. Not "I'll remember that one".
4. **Promote or demote** the unit in `## The rotation`. Clean pass → next interval out.
   **Three or more misses → back to weekly**, whatever it was before.

Only `## Core` decks are in scope for a weekly session. `## Deep` is a pre-exam or
pre-interview pass — see [_templates/flashcards-template.md](_templates/flashcards-template.md).

---

## The rotation

Three intervals, moved by hand: **weekly** (new or shaky) → **monthly** (solid) →
**quarterly** (cold storage). Everything starts weekly because nothing has been reviewed yet.

### AI_Data — one topic per session

| Track | Topics in rotation | Interval | Last reviewed |
|---|---|---|---|
| [00-core-skills](00-core-skills/INDEX.md) | 4 | weekly | — |
| [01-data-cloud](01-data-cloud/INDEX.md) | 10 | weekly | — |
| [02-salesforce-ai](02-salesforce-ai/INDEX.md) | 14 | weekly | — |
| [04-capstone](04-capstone/INDEX.md) | 3 | quarterly | — |

**31 topics in rotation, not 38.** All six [03-claude-cca](03-claude-cca/INDEX.md) topics and
`04-capstone/04-writeup` are `⬜ not started` — scaffolding with empty headings. They enter the
rotation the week they are written, not before. CCA-F is roadmap weeks 15–20.

### SF_core — five notes per session, by cursor

238 notes × 5 cards. An area is too big for one sitting, so the unit is **five consecutive
notes** (25 cards) and each area carries a cursor. At one session per area per week, a full
pass takes about 48 sessions — that number is the honest cost of 238 topics, and it is the
argument for the cursor rather than against the notes.

| Area | Notes | Cursor | Interval | Last reviewed |
|---|---|---|---|---|
| [01-admin-and-declarative-platform](../SF_core/01-admin-and-declarative-platform/INDEX.md) | 19 | 01 | monthly | — |
| [02-apex-and-triggers](../SF_core/02-apex-and-triggers/INDEX.md) | 34 | 22 | weekly | — |
| [03-lwc-and-slds](../SF_core/03-lwc-and-slds/INDEX.md) | 24 | 01 | monthly | — |
| [04-flow-and-automation](../SF_core/04-flow-and-automation/INDEX.md) | 27 | 01 | monthly | — |
| [05-experience-cloud-lwr](../SF_core/05-experience-cloud-lwr/INDEX.md) | 20 | 01 | quarterly | — |
| [06-integration-and-apis](../SF_core/06-integration-and-apis/INDEX.md) | 27 | 01 | monthly | — |
| [07-security-and-sharing](../SF_core/07-security-and-sharing/INDEX.md) | 26 | 01 | monthly | — |
| [08-data-modeling-and-large-data-volumes](../SF_core/08-data-modeling-and-large-data-volumes/INDEX.md) | 26 | 01 | monthly | — |
| [09-devops-sfdx-and-release-management](../SF_core/09-devops-sfdx-and-release-management/INDEX.md) | 25 | 01 | quarterly | — |
| [10-soql-and-sosl](../SF_core/10-soql-and-sosl/INDEX.md) | 10 | 01 | monthly | — |

The `02-apex-and-triggers` cursor starts at **22**, not 01, because notes 22 and 31–34 are the
Agentforce Apex surface and that is what is live right now. Move it to 01 once those are solid.

### Interview — one set per session, answered aloud

Different exercise: not cards, but a scenario defended end to end. Log fumbles in
[WEAK-ANSWERS.md](../Interview/WEAK-ANSWERS.md), which already exists for exactly this.

| Area | Sets | Interval | Last reviewed |
|---|---|---|---|
| [01-agentforce](../Interview/01-agentforce/INDEX.md) | 3 | weekly | — |
| [02-data-360](../Interview/02-data-360/INDEX.md) | 3 | monthly | — |
| [03-core-platform](../Interview/03-core-platform/INDEX.md) | 3 | monthly | — |
| [04-cross-domain](../Interview/04-cross-domain/INDEX.md) | 1 | monthly | — |

---

## Misses

Newest first. **The fourth column is the whole point** — the same way `PRACTICE.md`'s
*What broke* column is. "Forgot it" is not a reason; find the actual one.

Three misses on one topic sends it back to weekly. A card missed twice in a row is usually a
badly written card, not a badly remembered fact — rewrite it rather than re-drilling it.

| Date | Topic | The card | Why I missed it |
|---|---|---|---|
| — | — | — | — |

---

## Coverage

What is genuinely recallable today, measured 2026-08-27.

| | Count |
|---|---|
| Q/A cards, all vaults | **1,848** |
| — in `AI_Data` flashcards | 654 |
| — in `SF_core` `## Recall` blocks | 1,194 |
| Malformed cards | **0** |
| `AI_Data` topics in rotation | 31 of 38 |
| Topics `⬜ not started` | 7 (six CCA, one capstone writeup) |
| Sessions logged | 0 |

Two things this table is watching for:

- **A track whose card count keeps climbing but is never reviewed.** The release radar adds
  cards; only this file removes the debt.
- **`Sessions logged: 0` after a fortnight.** If that number does not move, the problem is the
  shape of this file, not your discipline. Change the file.
