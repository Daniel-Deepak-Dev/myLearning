# How notes get made here

This file exists so you never have to type the instructions again.

Paste your rough notes. The `study-notes` skill reads this contract and does the rest.

## What checks itself

Most of this contract is mechanical — a derived count, a mirrored column, a link
that must resolve. Those are checked by a script, not by remembering:

```
python scripts/vault.py check            every rule
python scripts/vault.py check --changed  only what you touched
python scripts/vault.py fix              rewrite the derived values
```

`check` is **read-only** and reports `file:line`. `fix` rewrites only values with
one correct answer — `Status` from the open-gap count, the `⏳ N months old` line,
the INDEX columns that mirror a note, the summary aggregates, and the `SF_core`
topic counts. It prints every change; read `git diff` before committing. Install it as a commit gate with
`cp scripts/pre-commit .git/hooks/pre-commit`, or run `/vault-check` in a session.

Two things it deliberately does **not** do:

- It never writes a `## Related` bullet. The "— why you would jump there" clause
  is content; a generated one would be filler. It reports the missing backlink
  and leaves the sentence to you.
- It never judges prose. Routing, `Level`, whether a gap is on-topic, whether a
  lab is a lab — those stay with you and the `study-notes` skill.

If a finding is wrong, the rule is wrong. Fix `scripts/vault.py` rather than
editing a note to satisfy a bad check.

## The problem this solves

You learn topics in whatever order work throws at you. Prompt templates on Monday. Trust Layer on Wednesday. Apex inside a prompt template on Thursday.

Your notes arrive rough and out of order. You want them to land in the right file, in an order you can learn from later, in a format you can re-read in two minutes.

## The five rules

### 1. Routing — one question decides the folder

> **Strip the product out of the sentence. Is it still true?**

Ask it once per product: *with no Agentforce in it?* *With no Experience Cloud site in it?*

- **Still true** → `SF_core/`. Apex, Flow, security, data model, integration.
- **Falls apart** → the vault that owns that product: `SF_Agentforce/`, `SF_Data_360/` or `SF_Experience_Cloud/`.

Examples:

| You learned | Goes to |
|---|---|
| What a prompt template is | `SF_Agentforce/` |
| `@InvocableMethod` signature and return types | `SF_core/02-apex-and-triggers/` |
| That a prompt template can call Apex | **Both.** The Agentforce note explains why. The Apex note explains how. They link to each other. |
| Einstein Trust Layer masking | `SF_Agentforce/` |
| Identity resolution rulesets | `SF_Data_360/` |
| What a guest user sharing rule may grant | `SF_Experience_Cloud/` |
| OWD and the grantee model underneath it | `SF_core/07-security-and-sharing/` |
| An Agentforce agent embedded on a public site | **Both.** `SF_Agentforce/` builds the agent; `SF_Experience_Cloud/` owns its site-side exposure. |

### 2. Format — light, not dense

Template: [_note-template.md](_note-template.md).

- **50 lines max — counted to `## Related`.** The ceiling is on the part you read. `## Related`, `## Sources` and `## History` are a footer: reference material you scan, not prose you re-read. They do not count.
- No paragraph longer than two sentences.
- Bullets and one table. Not prose.
- `## Key points` → `## Gotchas` → `## Gaps to close` → `## Confirm in org` → `## Hands-on` → `## Related` → `## Sources` → `## History`.

Your own wording is kept in a `> **From my notes.**` callout. That way you can always tell what you wrote from what the AI added.

Existing `SF_core` notes keep their older, longer format. Only **new** notes use the light one.

### 3. Gaps — scoped to where you actually are

Every note carries a level:

```
> Folder: SF_Agentforce · Level: basic · Status: 🌱 4 gaps open
> Created: 2026-08-27 · Updated: 2026-08-27
```

> **A note's gaps may go one level up. Never two.**

| Note level | Gaps allowed |
|---|---|
| `basic` | basic, working |
| `working` | working, deep |
| `deep` | anything on this topic |

So a `basic` prompt-template note gets gaps like *"can Sales Email ground on Lead as well as Contact?"*

It does **not** get `@InvocableMethod`. That is a `deep` item, two levels up.

When you later feed deeper notes on the same topic, the level rises. The deeper gaps unlock then.

Gaps also stay on the topic. Never a syllabus. Never "you should also learn Data 360."

Two places a gap can appear:

- `## Gaps to close` at the end — a checklist.
- An inline `> **Gap.**` callout — when the hole sits mid-topic and would confuse the bullets around it.

**A closed gap is deleted, not ticked.** Answer it, remove the line. When the last one goes, the `## Gaps to close` heading goes with it. What you learnt belongs in the note body — a list of settled questions is just clutter you have to read past.

**A gap research cannot close is not a gap.** Some questions have no public answer either way. Those move to a separate section and stop counting:

```markdown
## Gaps to close

- [ ] What does a retriever actually index, and who configures it?

## Confirm in org

- 🚩 Does Prompt Template Manager also confer Prompt Template User's run rights?
```

`## Gaps to close` is a reading list — someone can go and answer it. `## Confirm in org` is a sandbox to-do. Mixing them made the gap count read as unfinished research when half of it was waiting on an org login.

**And a third thing: `## Hands-on`.** Gaps and org checks are both *questions*. Labs are *skills* — the things you build to find out whether you can actually do any of this.

```markdown
## Hands-on

- [ ] **AF-VER-02** · 10 min · Deactivate the active version without activating another, then call the template. **Proves:** nothing is active and the template stops working — nothing prompts you to choose.
```

Four rules, and each one is doing work:

- **A lab needs a `Proves:`, not a verb.** "Build a Flex template" is a chore. "Prove an unactivated template is invisible to an agent" is a lab. This is the difference between a to-do list and a curriculum.
- **Break it on purpose.** The best labs cause a failure deliberately. Your `## Gotchas` section is already a list of things that break — mine it. A failure signature you have caused once is one you will recognise at a client.
- **Ticked, not deleted.** The opposite of the gap rule, and deliberately so. A settled question is clutter; work you actually did is a record.
- **3–4 per note, one line each, scoped to the note's `Level`** — the same ceiling gaps get. Labs never count towards `Status`.

IDs are `<VAULT>-<TOPIC>-NN` — `AF-TRUST-01`, `AF-ATLAS-02`. Stable, never reused, so you can say "close AF-ATLAS-02" and so the practice queue can point at a lab without copying its text.

**The doing view is a separate file.** Each vault gets a `PRACTICE.md`: `▶ Next` (exactly one), `In flight` (max 3), a dependency-ordered `Queue` with a time box and a `Proves` phrase, and a `Done` table. The note is where a lab is captured; `PRACTICE.md` is what you open when the goal is to *run* something. See [SF_Agentforce/PRACTICE.md](SF_Agentforce/PRACTICE.md).

**A lab is not finished until you have written down what broke, verbatim.** That is the `Done` table's last column. Notes get rewritten and releases move on, but an exact error string is still what you type into a search box in six months. `no failure; worked first time` is a real result too — it tells you the lab was too gentle.

Two things `PRACTICE.md` deliberately does **not** have: progress counters, and a copy of the lab text. `Done` is append-only, which is far harder to desync than a tally, and the note stays the single source of truth for what a lab actually is.

### 4. Links go both ways

When an Agentforce note links to an Apex note, the Apex note gets a link back. In the same edit.

One-way links are a folder of files. Two-way links are a wiki. You asked for a wiki.

### 5. Dates, status and sources

**Status is derived, never typed.** Count the `- [ ]` lines in `## Gaps to close` — and only those. `## Confirm in org` bullets and `## Hands-on` labs never count:

- at least one → `Status: 🌱 N gaps open`
- none, or no section at all → `Status: ✅ complete`

A note can be `✅ complete` and still carry org checks. Complete means *the research is done*, not *there is nothing left to verify*.

Delete a gap and the status moves on its own. A typed status goes stale the first time you forget to update it.

**Dates.** `Created` never changes. `Updated` changes on every edit.

**Staleness.** Past 3 months without an update, a third metadata line appears:

```
> ⏳ 4 months old — recheck against release notes
```

It disappears the moment the note is touched. Salesforce AI moves fast enough that a note going quiet for a quarter is worth flagging.

**Sources.** Every researched fact carries a link and the date it was read:

```markdown
## Sources

- [Prompt Template Types](https://help.salesforce.com/...) — Salesforce Help · read 2026-08-27
- [Apex Hours](https://www.apexhours.com/...) — third party 🚩 · read 2026-08-27
```

Salesforce domains are trusted. Anything else carries 🚩.

**History.** One dated line per feed, saying what was **added or changed** — never a gap tally:

```markdown
## History

- 2026-08-27 · created from your Day-1 notes
- 2026-09-02 · added Record Prioritization as the sixth type
```

## Order without renumbering

Filenames carry **no number**. `prompt-templates.md`, not `02-prompt-templates.md`.

The learning order lives in each folder's `INDEX.md`:

| # | Topic | One line | Level | Status | Org ✓ | Pre | Created | Updated |
|---|---|---|---|---|---|---|---|---|
| 1 | `einstein-trust-layer.md` | The masking and audit gate | basic | 🌱 3 open | 1 | — | 2026-08-27 | 2026-08-27 |
| 2 | `prompt-template-types.md` | The six types | basic | 🌱 4 open | — | 1 | 2026-08-27 | 2026-08-27 |

- `#` is the recommended read order.
- `Pre` is the hard prerequisite.
- `Org ✓` counts the note's `## Confirm in org` bullets. `—` when it has none.
- `Status`, `Created` and `Updated` mirror the note's own metadata.

Above the table, a summary line: **topic count · gaps open · complete · newest · oldest**, then a line naming the total org checks. That answers "how old is all this?" and "what is waiting on a sandbox?" without opening a note.

Why no numbers in filenames: you will feed a Day-5 topic that belongs at position 3. With numbered filenames that means renaming files and fixing every link. Here it means moving one table row.

`SF_core/PHASES.md` already records renumbering as expensive in that vault. We are not repeating it.

## The archive

`_archive/AI_Data/` holds the old roadmap vault — 24 researched Agentforce and Data 360 topics, the study plan, the labs and the trackers.

It is a **quarry, not a reference.**

- When you feed a topic it already covered, its verified facts get pulled into your new note, **cut to your level**.
- Nothing links back to it. No note says "go read the archive".
- Its glossary and release radar were kept and promoted: [GLOSSARY.md](GLOSSARY.md) and [RELEASE-RADAR/](RELEASE-RADAR/README.md).

## Anything that does not route

Goes to that folder's `_inbox.md`, as one bullet, with the date.

Filing friction must never stop capture. Triage it later.

## Decisions log

| Date | Decision | Why |
|---|---|---|
| 2026-08-27 | `SF/` renamed to `SF_core/` | Makes room for `SF_Agentforce/` and `SF_Data_360/` as peers. 112 links across 23 files repaired in the same pass. |
| 2026-08-27 | New folders start empty | You wanted a vault fed by what you actually learn, not by a generated roadmap. |
| 2026-08-27 | Filenames carry no number | You feed topics in random order. Numbered filenames make every insertion a rename. |
| 2026-08-27 | Light format for all new notes, in every vault | You asked for notes you can recall from, not paragraphs. |
| 2026-08-27 | Existing `SF_core` notes are enriched in place, not duplicated | 238 notes already exist. A second light file beside each would split the topic in two. |
| 2026-08-27 | `AI_Data/` retired to `_archive/` | You said you will not use it for reference or recall. Its glossary and release radar were promoted to the root; ~270 links repointed to the new folders. |
| 2026-08-27 | Archive is a quarry, never a link target | Keeps the research without asking you to read a vault you have abandoned. |
| 2026-08-27 | Dates, derived status, staleness flag, sources and history on every note | You asked to know how old a note is and whether it is finished. Deriving status from the gap checklist stops it going stale. |
| 2026-08-28 | Closed gaps are deleted, not ticked; empty section removed | A checklist of settled questions is clutter. What you learnt goes in the note body. |
| 2026-08-28 | `## History` never records gap counts | It logs what changed, not bookkeeping. |
| 2026-08-28 | Org-only questions split into `## Confirm in org` and excluded from the status count | A third of the open gaps had no public answer. Counting them made research look unfinished when it was done. |
| 2026-08-28 | The `study-notes` skill closes gaps as well as opening them | The skill only ever opened gaps, so the count could rise but never fall without you asking. |
| 2026-08-28 | Every note carries 3–4 `## Hands-on` labs, ticked rather than deleted | Nine complete notes still could not tell you whether you can *do* any of it. Ticking keeps the record of work done; deleting would throw it away. |
| 2026-08-28 | Labs are captured in the note but queued in a per-vault `PRACTICE.md` | The note is where you meet a lab; the queue is what you open to run one. One source of truth, no counters, `Done` append-only. |
| 2026-08-28 | The 50-line ceiling counts to `## Related`, not to end of file | A fully-sourced note cannot fit sources, links, history *and* a body in 50 lines. Capping the body is what the rule was for; capping the footer only pushed out citations. |
| 2026-09-19 | `SF_core/05-experience-cloud-lwr/` promoted to the root vault `SF_Experience_Cloud/` | Experience Cloud is a product with its own runtime, licences, security model and deployment story — the same case that made `SF_Agentforce/` and `SF_Data_360/` peers rather than areas. 65 inbound links across 27 files and ~100 outbound links repointed in the same pass. |
| 2026-09-19 | Experience Cloud filenames keep their `NN-` numbers | The numbering is the learning path and `PHASES.md` depends on it. Eight notes in other vaults cite **05 · 07–12** by number in link text; renumbering would break all of them for no gain. |
| 2026-09-19 | Currency and the phase record stay in `SF_core/` | `CURRENCY.md` is one ledger for the whole platform and its Experience Cloud rows cross-reference LWC, security and DevOps rows. Splitting it would break the running *"the plan's own correction was stale"* thread that phases 10–19 built. |
| 2026-08-27 | Level beats migration depth | A one-line note of yours does not get replaced by 119 lines from the archive. Write at your level; the depth arrives when your notes do. |
