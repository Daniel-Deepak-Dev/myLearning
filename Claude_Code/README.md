# Claude Code

Learning Claude Code by building it into this repo. This is a self-paced track, not a vault: there are no flashcards, it's not in the daily area rotation, and it has no INDEX or PRACTICE file.

## How the loop works

1. **`npm run today`** adds a `## Claude Code` block to your journal page:
   - **Learn**: the first topic below with an empty `Note` cell, and the docs page to learn it from.
   - **Build**: the first unticked lab in a note you have already fed.
2. **Learn it**, then paste what you learnt and say "I learned … today". The `study-notes` skill files it into this folder, following [AGENTS.md](AGENTS.md), and fills that topic's `Note` cell.
3. **The note comes back.** It counts as studied on its `created` date, and reappears under **Review** 3, 7, 16, 35 and 75 days later, the same timing as your Salesforce notes.
4. **Build the lab** in this repo. Tick it in the note when it works. The next day's **Build** line moves on.

The order below is a suggestion, not a rule. Feed a topic early and its row fills in early. Feed something that isn't listed and it gets a new row.

## Path

| # | Topic | Learn from | Note |
|---|---|---|---|
| 1 | Instructions & memory | [How Claude remembers your project](https://code.claude.com/docs/en/memory) | |
| 2 | Settings & permissions | [Configure permissions](https://code.claude.com/docs/en/permissions) | |
| 3 | Slash commands & skills | [Custom Commands and Skills](https://code.claude.com/docs/en/skills) | |
| 4 | Hooks: events & exit codes | [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide) | |
| 5 | Hooks: guards & context | [Hooks reference](https://code.claude.com/docs/en/hooks) | |
| 6 | Subagents | [Create custom subagents](https://code.claude.com/docs/en/sub-agents) | |
| 7 | Output styles | [Output styles](https://code.claude.com/docs/en/output-styles) | |
| 8 | MCP servers | [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) | |
| 9 | Headless & scheduling | [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) | |
| 10 | Plugins | [Plugins overview](https://code.claude.com/docs/en/plugins/overview) | |

## What each topic can build here

Ideas for the labs a filed note will carry. You build them; Claude reviews.

- **1 · Instructions & memory:** find out why this repo's `AGENTS.md` loads; add a rule to [AGENTS.md](AGENTS.md) and prove it applies only in this folder.
- **2 · Settings & permissions:** move shared allows from `.claude/settings.local.json` to `.claude/settings.json`; deny edits to `_archive/` and watch one get blocked.
- **3 · Skills:** take apart `/vault-check`; make a skill description vague and watch it stop triggering.
- **4 · Hooks I:** a PostToolUse hook that runs `python scripts/vault.py check --changed` and feeds findings back to Claude.
- **5 · Hooks II:** a PreToolUse guard on `_archive/`; a SessionStart hook that loads today's session.
- **6 · Subagents:** a read-only `recall-quizzer` that quizzes you from a `RECALL.md`.
- **7 · Output styles:** a "tutor" style that asks you to predict before it explains.
- **8 · MCP:** add one project-scoped server in `.mcp.json`.
- **9 · Headless:** a `claude -p` run that summarises `vault.py check`; a weekly routine.
- **10 · Plugins:** bundle the skill, hooks and agent into a local plugin.
