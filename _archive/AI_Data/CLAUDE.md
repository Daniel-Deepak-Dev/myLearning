# AI_Data — how to write in this vault

Style rules: [../CLAUDE.md](../CLAUDE.md). Full conventions: [README.md](README.md).

## The four layers

One folder per topic. Templates in [_templates/](_templates/).

| File | Job | Size rule |
|---|---|---|
| `notes.md` | Learn — depth, gotchas, why it works this way | Deep but bounded |
| `cheatsheet.md` | Recall the topic in 5 minutes | **Half a page.** Overflow goes to `notes.md` |
| `flashcards.md` | Self-test | Strict `Q:`/`A:` — see below |
| `resources.md` | Sources, plus your own labs and gists | — |
| `_labs/` or `labs/` | Do — time-boxed runbooks | **No cap.** See below |

## Rules

- **The flashcard format is scriptable into Anki.** One `Q:` line, then `A:` line(s), blank line between cards. Never break it. Past ~20 cards, split into `## Core` (≤15 that must be automatic) and `## Deep`.
- **The line caps do not apply to lab files.** A runbook holds a whole procedure — verbatim commands, real payloads, exact error strings. Capping labs is what left 26 notes pointing at a `labs/` folder that did not exist.
- **Currency: Summer '26 (API 67.0).** Two traps most online material gets wrong: Data Cloud is now **Data 360**, and agents are authored in **Agent Script** — the legacy topics-and-instructions builder stopped creating new agents the week of 2026-07-13.
- **Never duplicate currency detail.** Link to [05-release-radar/](05-release-radar/README.md); it is the source of truth for what changed and when.
- **New jargon** goes in [GLOSSARY.md](GLOSSARY.md). One glossary for all three vaults.
- **New topic, fits a track** → next-numbered `NN-kebab-case` folder there, copy the four templates, add a row to that track's `INDEX.md`.
- **New topic, no home** → one bullet in [99-inbox/INBOX.md](99-inbox/INBOX.md). Never let filing friction stop capture.
- **Never edit `ai-salesforce-architect-roadmap.html`.** It is the tracker; this folder is the knowledge.
