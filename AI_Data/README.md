# AI_Data — AI-Salesforce Architect Study Base

Companion folder to [ai-salesforce-architect-roadmap.html](ai-salesforce-architect-roadmap.html) (open it in a browser — it's the interactive progress tracker). This folder is organized **by track**, not by phase, so knowledge clusters stay together for long-term reference. [STUDY-PLAN.md](STUDY-PLAN.md) maps the 26-week phases onto these folders.

## Map

| Folder | Track |
|---|---|
| [00-core-skills/](00-core-skills/INDEX.md) | SQL, Python, AI theory, data engineering |
| [01-data-cloud/](01-data-cloud/INDEX.md) | Data Cloud → **Data Cloud Consultant** cert |
| [02-salesforce-ai/](02-salesforce-ai/INDEX.md) | Agentforce, Prompt Builder, Trust Layer → **Agentforce Specialist** cert |
| [03-claude-cca/](03-claude-cca/INDEX.md) | Claude API, agents, MCP, Claude Code → **CCA-F** cert |
| [04-capstone/](04-capstone/INDEX.md) | The shipped proof: MCP server, RAG assistant, Agentforce build |
| [05-release-radar/](05-release-radar/README.md) | Running log of Salesforce AI / Agentforce / Data 360 updates worth knowing |
| [99-inbox/](99-inbox/INBOX.md) | Capture anything new before it has a home |
| [journal/](journal/) | Weekly learning log |
| [GLOSSARY.md](GLOSSARY.md) | All 77 terms, greppable |
| [dashboard.html](dashboard.html) | Visual master index (open in browser) |

## The layers — how to use each file

Every topic folder has the same four files (templates in [_templates/](_templates/)):

| File | Purpose | When you touch it |
|---|---|---|
| `notes.md` | **Learn.** Deep understanding, diagrams, gotchas, "why it works this way" | While studying |
| `cheatsheet.md` | **Recall.** Half a page future-you reads in 5 minutes to reload the topic | Distill after notes.md feels solid |
| `flashcards.md` | **Self-test.** Strict `Q:`/`A:` pairs (Anki-scriptable). Pre-seeded from the glossary | Review weekly; add cards as you learn |
| `resources.md` | **Sources.** Docs, courses, repos, plus your own labs/gists | Whenever you find something good |
| `labs/` | Hands-on scripts, screenshots, org configs | Create on demand — not pre-made |

**The recall loop that makes this work:** study → write notes → distill the cheatsheet → quiz yourself from flashcards → log the week in `journal/`. Months later, re-entry = cheatsheet first, flashcards second, notes only if something's still fuzzy.

## Conventions

- **Naming:** `NN-kebab-case` folders, numbered in learning order within a track.
- **Links:** relative markdown links; browse in VS Code (preview: `Ctrl+Shift+V`).
- **New topic, fits a track** → create the next-numbered folder there, copy the four templates from `_templates/`, add a row to that track's `INDEX.md`.
- **New topic, no obvious home** → one bullet in [99-inbox/INBOX.md](99-inbox/INBOX.md) now, triage later. Never let filing friction stop capture.
- **Cert prep** lives in `_cert-*/` folders: exam-guide breakdown, practice questions (log every miss + why), weak-areas checklist updated after each mock.
- The roadmap HTML stays untouched — it's the tracker; this folder is the knowledge.
