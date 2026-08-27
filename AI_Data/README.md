# AI_Data — AI-Salesforce Architect Study Base

Companion folder to [ai-salesforce-architect-roadmap.html](ai-salesforce-architect-roadmap.html) (open it in a browser — it's the interactive progress tracker). This folder is organized **by track**, not by phase, so knowledge clusters stay together for long-term reference. [STUDY-PLAN.md](STUDY-PLAN.md) maps the 26-week phases onto these folders.

## Map

| Folder | Track |
|---|---|
| **[PRACTICE.md](PRACTICE.md)** | **Start here when the goal is to *do* something.** The single queue: one next action, max 3 in flight, every unit time-boxed |
| **[REVIEW.md](REVIEW.md)** | **Start here when the goal is to *recall* something.** The rotation, the 20-minute session, and the miss log. Drives all three vaults |
| [00-core-skills/](00-core-skills/INDEX.md) | SQL, Python, AI theory, data engineering |
| [01-data-cloud/](01-data-cloud/INDEX.md) | **Data 360** (ex-Data Cloud) → **Data 360 Consultant** cert |
| [02-salesforce-ai/](02-salesforce-ai/INDEX.md) | Agentforce, Agent Script, Trust Layer, orchestration → **Agentforce Specialist** cert |
| [03-claude-cca/](03-claude-cca/INDEX.md) | Claude API, agents, MCP, Claude Code → **CCA-F** cert |
| [04-capstone/](04-capstone/INDEX.md) | The shipped proof: MCP server, RAG assistant, Agentforce build |
| [05-release-radar/](05-release-radar/README.md) | Running log of Salesforce AI updates, in three areas: `01-agentforce/`, `02-data-cloud/`, `03-salesforce-ai-research/` |
| [../SF/](../SF/README.md) | **Core Salesforce platform** — Apex, LWC, Flow, Admin, Experience Cloud, Integration, Security, Data, DevOps. The platform underneath this path |
| [../Interview/](../Interview/README.md) | **Scenario-based interview prep** — 42 medium-to-complex situations across Agentforce, Data 360, core platform and cross-domain, each with a model answer and an interviewer rubric |
| [99-inbox/](99-inbox/INBOX.md) | Capture anything new before it has a home |
| [journal/](journal/) | Weekly learning log |
| [QUICKSTART-LINKS.md](QUICKSTART-LINKS.md) | **Start here for Agentforce + Data 360** — curated links, first-week plan, outdated-source traps |
| [GLOSSARY.md](GLOSSARY.md) | All 109 terms, greppable, marked for currency |
| [dashboard.html](dashboard.html) | Visual master index (open in browser) |

## Currency

Content is current to **Summer '26 (API 67.0)** as of **2026-07-28**. Two things changed structurally since this base was first laid out, and both trip up anyone studying from older material:

- **Data Cloud → Data 360.** A real rename — SKUs, release notes and the certification all use it. Folder paths keep the old name so links don't break; the content doesn't.
- **Agent Script replaced topics-and-instructions.** Since the week of **July 13, 2026** the *New Agent* button no longer opens the legacy builder. Most tutorials online still teach the retired model — check publication dates.

[05-release-radar/](05-release-radar/README.md) is the source of truth for what's changed; topic folders link back into it rather than duplicating the detail.

## The layers — how to use each file

Every topic folder has the same four files (templates in [_templates/](_templates/)):

| File | Purpose | When you touch it |
|---|---|---|
| `notes.md` | **Learn.** Deep understanding, diagrams, gotchas, "why it works this way" | While studying |
| `cheatsheet.md` | **Recall.** Half a page future-you reads in 5 minutes to reload the topic | Distill after notes.md feels solid |
| `flashcards.md` | **Self-test.** Strict `Q:`/`A:` pairs (Anki-scriptable). Pre-seeded from the glossary | Review weekly; add cards as you learn |
| `resources.md` | **Sources.** Docs, courses, repos, plus your own labs/gists | Whenever you find something good |
| `_labs/` | **Do.** Time-boxed runbooks — the only place a claim becomes verified | Every topic. **Mandatory, not on demand** |

The two ladders: [Agentforce](02-salesforce-ai/_labs/README.md) · [Data 360](01-data-cloud/10-lab-environment/labs/README.md). Enter both through [PRACTICE.md](PRACTICE.md), never by browsing.

> **The line caps do not apply to lab files.** `notes.md` stays deep-but-bounded and `cheatsheet.md` stays half a page — those caps are what make them re-readable. But a runbook has to hold a whole procedure: verbatim commands, real payloads, exact error strings. Capping it is what left 26 notes pointing at a `labs/` folder that didn't exist.

**Two loops, and only one of them was running.**

- **Recall:** study → write notes → distill the cheatsheet → quiz from flashcards → log the week in `journal/`. Re-entry months later = cheatsheet first, flashcards second, notes only if still fuzzy.
- **Run:** pick the next lab from `PRACTICE.md` → run it in a real org → fill in *Notes from my run* and *Failure signature* → move it to `## Done`. A topic you have only read is marked `not yet run` in its own `## Do it` section, and that is not a criticism — it is the difference between "I've read the constraints" and "I've hit them", which is exactly the distinction worth being able to make out loud.

## Conventions

- **Naming:** `NN-kebab-case` folders, numbered in learning order within a track.
- **Links:** relative markdown links; browse in VS Code (preview: `Ctrl+Shift+V`).
- **New topic, fits a track** → create the next-numbered folder there, copy the four templates from `_templates/`, add a row to that track's `INDEX.md`.
- **New topic, no obvious home** → one bullet in [99-inbox/INBOX.md](99-inbox/INBOX.md) now, triage later. Never let filing friction stop capture.
- **Cert prep** lives in `_cert-*/` folders: exam-guide breakdown, practice questions (log every miss + why), weak-areas checklist updated after each mock.
- The roadmap HTML stays untouched — it's the tracker; this folder is the knowledge.
