# The note template moved

The template now lives at **[templates/note.md](templates/note.md)**, so Obsidian's
core **Templates** plugin can insert it — `Ctrl+P` → *Insert template* → `note`.

It is a real template, not a copy of the rules. Two things changed with it:

- **Metadata is YAML frontmatter**, not a `>` blockquote. Obsidian reads it as
  Properties, which is what makes the Bases views and [HOME.md](HOME.md) work.
- **The 43 numbered rules that used to sit in an HTML comment here are gone.**
  They were a fourth copy of [NOTES-SYSTEM.md](NOTES-SYSTEM.md), and the copies
  drifted. The rules a machine can decide are now enforced by
  `python scripts/vault.py check` instead of restated in prose.

The contract is [NOTES-SYSTEM.md](NOTES-SYSTEM.md). Everything mechanical in it is
checkable with `python scripts/vault.py check --list-rules`.
