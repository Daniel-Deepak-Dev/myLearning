---
description: Analyse how a Salesforce feature behaves for a human UI user vs an agent or external API caller, then offer to add a "Human vs Agent" section to the note.
argument-hint: [path to an SF_core/, SF_Agentforce/, SF_Data_360/ or AI_Data/ note — omit to use the open file]
allowed-tools: Read, Grep, Glob, Edit, WebFetch, AskUserQuestion
---

Target note: $ARGUMENTS

## Job

Read the target note, work out how its feature behaves for a **human in the UI** versus an **agent or external API caller** (Headless 360), print the finding, and offer to write it into the note.

## 1 · Resolve the target

- Use the path above. If empty, use the file currently open in the IDE. If there is none, ask for one — do not guess.
- Accept only `.md` files under `SF_core/`, `SF_Agentforce/`, `SF_Data_360/` or `AI_Data/`. Refuse anything else in one line and stop.
- Read the whole file before analysing. Read `SF_core/README.md` or the sibling `INDEX.md` only if the feature is unclear from the note.

## 2 · Analyse against these six axes

Always the same six, so notes stay comparable:

1. **UI enforcement** — what the platform stops a human from doing on screen.
2. **API enforcement** — what survives on REST, SOAP, Bulk and Apex DML.
3. **Discovery** — how a headless client *reads* the rule: describe, UI API, Tooling API, Metadata API, GraphQL.
4. **The gap** — where 1 and 2 diverge, and what closes it (validation rule, invocable Apex/Flow, UI API write path, restricted picklist, Shield).
5. **Agent identity** — which user an Agentforce action or integration runs as, and what grants it access.
6. **Dead weight** — the part of the feature that exists only for a rendered UI and means nothing to an agent.

Three honest verdicts are possible. Do not force a divergence that is not there:

- **UI-only** — the UI enforces something the API does not. The interesting case.
- **Enforced everywhere** — same behaviour on every write path. Say so plainly.
- **No agent surface** — the feature does not meaningfully differ. Say so and skip the edit.

## 3 · Verify what you are unsure of

- Enforcement behaviour shifts between releases. Never assert it from recall alone.
- For any claim you are not confident in, `WebFetch` `help.salesforce.com` or `developer.salesforce.com` before stating it.
- Verified → cite the doc URL.
- Still unsure → write the claim with the suffix `*(unverified — confirm in org)*`.
- Never use 🆕 or ⚠️ as confidence markers. Those already mean something specific in the `SF_core/README.md` flag legend.

## 4 · Print the finding

**Bullets only. One line each, roughly 15 words maximum. No paragraphs anywhere — not in the terminal, not in the file.**

Open with the verdict (`UI-only` / `Enforced everywhere` / `No agent surface`), then the proposed section verbatim.

## 5 · Ask before editing

Use `AskUserQuestion` to offer: insert it, adjust it first, or skip. On skip, change nothing and stop.

## 6 · Insert

Section shape — keep it to about 12 lines:

```markdown
## Human vs Agent

| Behaviour | Human (UI) | Agent / API |
|---|---|---|
| <axis> | <phrase> | <phrase> |

- **Discover:** <the endpoint or describe call that returns the rule>
- **Gap:** <what the UI enforces that the API does not>
- **Close it:** <validation rule / invocable / UI API write path>
- **Agent identity:** <which user, granted by what>
- **Dead weight:** <the UI-only part an agent ignores>
```

Placement:

- After `## How it works`. The `SF_core` and `AI_Data` templates use that heading.
- Light-format notes (`SF_Agentforce/`, `SF_Data_360/`, new `SF_core/` notes) have no `## How it works`. There, insert after `## Key points`.
- Fallback order: before `## Gotchas` → before `## Gotchas & sharp edges` → before `## Gaps to close` → before `## Recall` → append at the end.
- If `## Human vs Agent` already exists, rewrite it in place. Never create a second one.

## 7 · Report the line count

- `SF_core/README.md` caps its existing notes at **~80 lines**, and its rule 1 says a note that will not fit means the taxonomy is wrong — split the topic.
- Light-format notes cap at **50 lines** — see `../_note-template.md`.
- After inserting, state the new line count.
- Over cap → say so and name what to trim or split. Never trim the note silently.

## House conventions

- **Headless 360** is the established term for this whole subject — see `SF_core/06-integration-and-apis/25-mcp-servers-and-agent-facing-apis.md`.
- Cross-link instead of restating: `06-integration-and-apis/08-ui-api-and-metadata-aware-clients.md` for record-type-aware and layout-aware reads, `25-mcp-servers-and-agent-facing-apis.md` for agent-facing APIs.
- Currency detail links to `AI_Data/05-release-radar/` rather than being duplicated.
- Relative markdown links only.
- Name the exact endpoint, object, permission or setting. A bullet that could apply to any feature is not worth a line.
