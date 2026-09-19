---
allowed-tools: Bash(python scripts/vault.py:*), Read, Edit, Glob, Grep
argument-hint: "[rule prefix, e.g. backlink or index] — omit for everything"
description: Run the mechanical half of the notes contract and report what drifted.
---

Run the vault checker and report what it found.

```
!python scripts/vault.py check $ARGUMENTS
```

## How to read it

`scripts/vault.py` only checks rules from [NOTES-SYSTEM.md](../../NOTES-SYSTEM.md) that a
machine can decide without judgement. It is read-only — it never edits a note.

Group the findings for me by what they cost to fix:

1. **Derived values that are simply stale** — `status-derived`, `stale-flag`,
   `index-row`, `index-summary`, `readme-counts`, `lab-practice-sync`. These have
   exactly one correct answer. `python scripts/vault.py fix` rewrites all of
   them; offer that rather than editing the files one at a time.
2. **Integrity breaks** — `link-broken`, `link-label`, `link-archive`,
   `link-wikilink`, `index-coverage`. Usually a move that left something behind.
   Say what moved before changing anything.
3. **`backlink-missing`** — the standing backlog, currently in the hundreds.
   **Never auto-write these.** A `## Related` bullet needs a real "— why you
   would jump there" clause, and a generated one is filler. Surface a handful at
   a time, grouped by area, and write the clause by hand.
   A hub with 20+ inbound links does not want 20 return bullets — it would blow
   the line budget. Say so rather than adding them.
4. **Format** — `format-length`, `format-blocks`, `format-sections`,
   `sources`, `history-tally`, `lab-format`, `naming`. These need a judgement
   call about the prose. Show the line, suggest a fix, do not apply it silently.

If a finding is wrong, the rule is wrong — fix `scripts/vault.py`, do not edit the
note to satisfy a bad check.
