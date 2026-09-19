---
allowed-tools: Bash(python scripts/vault.py:*), Read, Edit, Glob, Grep
argument-hint: "[rule prefix, e.g. backlink or index] — omit for everything"
description: Run the mechanical half of the notes contract and report what drifted.
---

Run the vault checker and report what it found.

```
!python scripts/vault.py check $ARGUMENTS
```

## The commands

| Command | What it does |
|---|---|
| `check` | read-only; reports `file:line` for every mechanical rule |
| `fix` | rewrites derived values only — never prose |
| `home` | regenerates `HOME.md`, the what-to-study-next page |
| `cards` | exports the `## Recall` pairs to Anki TSV + Obsidian decks |
| `migrate` | one-shot, already run: blockquote metadata → frontmatter |

After any note changes, the loop is `fix` → `home` → `check`.

## How to read the findings

`scripts/vault.py` only covers rules from [NOTES-SYSTEM.md](../../NOTES-SYSTEM.md)
that a machine can decide without judgement.

1. **Derived values** — `status-derived`, `index-row`, `index-summary`,
   `readme-counts`, `tags`, `frontmatter`. One correct answer each.
   `python scripts/vault.py fix` rewrites them all; offer that rather than
   editing files one at a time. `lab-practice-sync` has no fixer — the queue
   order is unblocked-first, which is a judgement call.
2. **Integrity** — `link-broken`, `link-label`, `link-archive`,
   `link-wikilink`, `index-coverage`. Usually a move that left something
   behind. Say what moved before changing anything.
3. **`backlink-missing`** — cross-vault seams only, currently ~31.
   **Never auto-write these.** A `## Related` bullet needs a real "— why you
   would jump there" clause; a generated one is filler that looks finished.
   Surface a few at a time and write the clause by hand after reading both
   notes. Same-vault links are no longer checked — Obsidian's Backlinks panel
   covers those.
4. **`stale`** — notes 3+ months old. A study signal, not a defect; it sits
   deliberately outside the pre-commit gate.
5. **Format** — `format-length`, `format-blocks`, `format-sections`,
   `sources`, `history-tally`, `lab-format`, `naming`. These need a judgement
   call about the prose. Show the line, suggest a fix, do not apply silently.

## Two standing rules

**Four frontmatter keys belong to the tool** — `status`, `gaps`, `org_checks`,
`labs`. Everything else (`vault`, `area`, `format`, `level`, `created`,
`currency`, `phase`, `tags`) is the user's. Never hand-edit the first four,
and never let `fix` touch the rest.

**If a finding is wrong, the rule is wrong.** Fix `scripts/vault.py`, do not
edit a note to satisfy a bad check.
