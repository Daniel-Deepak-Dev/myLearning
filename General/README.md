# General

Everything you learn that isn't Salesforce or Claude Code. A podcast, a book chapter, a late-night rabbit hole.

This is a home, not a vault. There are no flashcards, labs or gaps, and it is not in the daily area rotation. Your words go on top. Claude checks them against a source and files them by subject.

## How it works

1. **Paste your rough notes** and say "I learned … today". Any order, any length. One line is fine.
2. **The `study-notes` skill files them.** It splits the dump into topics, picks a subject folder, and updates a note or creates one. Rules: [AGENTS.md](AGENTS.md).
3. **Your words go into `## My recall`**, tightened but never added to. A wrong line gets 🚩 and a reason, and you fix it.
4. **Find it later in [INDEX.md](INDEX.md)**, grouped by subject. `npm run vault:home` rebuilds it.
5. **It comes back.** A note's `created` date counts as your first study. `npm run today` lists it under **Review** 3, 7, 16, 35 and 75 days later.

## Layout

```
General/
  INDEX.md                  generated: every subject and topic
  <subject>/<topic>.md      e.g. finance/compound-interest.md
```

One folder per subject, made when the first topic needs it. One level deep.
