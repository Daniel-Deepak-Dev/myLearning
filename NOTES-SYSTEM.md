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
one correct answer — `status`, `gaps`, `org_checks` and `labs` recounted from the
note body, the INDEX columns that mirror a note, the summary aggregates, the
`SF_core` topic counts, and the `PRACTICE.md` Done table. It prints every change; read `git diff` before committing. Install it as a commit gate with
`cp scripts/pre-commit .git/hooks/pre-commit`, or run `/vault-check` in a session.

Two things it deliberately does **not** do:

- It never writes a `## Related` bullet. The "— why you would jump there" clause
  is content; a generated one would be filler. It reports the missing backlink
  and leaves the sentence to you.
- It never judges prose. Routing, `Level`, whether a gap is on-topic, whether a
  lab is a lab — those stay with you and the `study-notes` skill.

If a finding is wrong, the rule is wrong. Fix `scripts/vault.py` rather than
editing a note to satisfy a bad check.

## The furniture Obsidian uses

Five things exist for Obsidian that are easy to miss because nothing else links them:

| Path | What it is |
|---|---|
| [HOME.md](HOME.md) | **Open this first.** Generated — today's session, cards, open gaps, org checks, stale notes, missing seams. Rebuild with `npm run vault:home`. |
| `<vault>/RECALL.md` | Generated with HOME — every note's `## My recall` in read order, one file per vault. The page you read top to bottom before an interview, or cover and recite. |
| `npm run today` | Writes today's session into `journal/YYYY-MM-DD.md`: cards, due reviews, one topic, one drill. See [The daily session](#the-daily-session). |
| `bases/topics.base` | Six Bases views over the frontmatter — all topics, open gaps, org checks, currency warnings, new-since-2024, oldest-first. They read the notes directly, so they cannot drift. |
| `templates/note.md`, `templates/daily.md` | Inserted by the core **Templates** plugin. The daily one holds a `<!-- today` line that `npm run today` replaces with the session, plus weak answers and what broke, verbatim. |
| `journal/` | Where **Daily Notes** and `npm run today` write. One file per day, `YYYY-MM-DD`. Its ticked lines are the study record. |
| [Flashcards/](Flashcards/README.md) | The interview flashcard bank: Foundations and Hard cards per area and topic, each linking the note that holds the reasoning. Reviewable in Obsidian's Spaced Repetition plugin as-is; `python scripts/flashcards.py sync` pushes it to Anki. |

`bases/graph-groups.json` holds the graph colour groups. `.obsidian/graph.json`
is gitignored because Obsidian rewrites its zoom level constantly; if the colours
are ever lost, re-apply them from that file in Graph view → Groups.

## The problem this solves

You learn topics in whatever order work throws at you. Prompt templates on Monday. Trust Layer on Wednesday. Apex inside a prompt template on Thursday.

Your notes arrive rough and out of order. You want them to land in the right file, in an order you can learn from later, in a format you can re-read in two minutes.

## The five rules

### 1. Routing — one question decides the folder

> **Strip the product out of the sentence. Is it still true?**

Ask it once per product: *with no Agentforce in it?* *With no Experience Cloud site in it?* *With no Service Cloud in it?* *With no Sales Cloud in it?*

- **Still true** → `SF_core/`. Apex, Flow, security, data model, integration.
- **Falls apart** → the vault that owns that product: `SF_Agentforce/`, `SF_Data_360/`, `SF_Experience_Cloud/`, `SF_Service/` or `SF_Sales/`.

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
| Queues and assignment rules | `SF_core/01-admin-and-declarative-platform/` — they also work on Lead, Task and custom objects |
| How Omni-Channel pushes a queue's work to an available rep | `SF_Service/` |
| An Agentforce agent embedded on a public site | **Three ways.** `SF_Agentforce/` builds the agent; `SF_Service/` owns the Enhanced Chat channel, its routing and the handoff to a human; `SF_Experience_Cloud/` owns the site-side exposure. |
| How lead conversion maps custom fields | `SF_Sales/` |
| The share rows an account team or a territory adds | `SF_core/07-security-and-sharing/` — read beside the other granting mechanisms. *Team roles, splits and territory forecasts* are `SF_Sales/`. |

### 2. Format — light, not dense

Template: [templates/note.md](templates/note.md) — Obsidian's Templates plugin inserts it with *Insert template*.

- **50 lines max — counted to `## Related`.** The ceiling is on the part you read. `## Related`, `## Sources` and `## History` are a footer: reference material you scan, not prose you re-read. They do not count.
- No paragraph longer than two sentences.
- Bullets and one table. Not prose.
- `## My recall` → `## My code` → `## Key points` → `## Gotchas` → `## Gaps to close` → `## Confirm in org` → `## Hands-on` → `## Related` → `## Sources` → `## History`.

Existing `SF_core` notes keep their older, longer format. Only **new** notes use the light one. Both formats take the recall layer.

### 2a. The recall layer — your words on top

Every note has two layers. **The top is yours. The rest is reference.**

```markdown
## My recall

- **DI event** — low-code LMS · App Builder only · one → many
- **Map it** — `{!Event.prop1}` in the receiver's property

## My code

<a snippet you wrote and ran, with your own comments — optional>
```

- **`## My recall` is 3–7 lines of `**cue** — power words`, in your words.** The cue on the left is what you see when you test yourself; everything after the dash is what you say.
- **Claude never writes vocabulary here.** When you feed rough notes it may reorder, trim and fix spelling. It never adds a word, phrase or fact of its own.
- **A wrong line stays, flagged.** Claude appends `🚩 <why>` and you rewrite the line. The fix is the study.
- **No links, tables or code inside it.** `RECALL.md` lives in another folder, so a relative link would break there. Code goes in `## My code`.
- **Both sections come first,** before the reference body, and neither counts towards the line or code-block caps.
- **Written when you study a topic, not before.** A note without one is fine. `npm run today` brings up one topic a day, and `RECALL.md` counts how many are in your words.

Old notes carry your words in a `> **From my notes.**` callout. Those stay. When `npm run today` picks one of those notes, start the recall layer from the callout.

Why: you remember what you produce, not what you read. Every study behind this design is listed in the 2026-10-02 decisions-log rows.

### 2b. The daily session

`npm run today` picks one session and writes it into `journal/YYYY-MM-DD.md`. It is built for 30–45 minutes:

| Block | Time | What you do |
|---|---|---|
| Cards | 10 min | Due Anki cards. A miss means rewrite that answer in your words; keep its id. |
| Review | 5 min | Up to 3 notes in your words whose spaced date has come. Read only the cues; say the rest. |
| Topic | 20 min | Blurt everything you remember **before** opening the note. Then open it, write what you missed, and write or fix its `## My recall`. |
| Drill | 10 min | Mon/Wed a scenario out loud · Tue/Thu the topic's code from a blank file · Fri a project story · weekend a recall sheet, answers covered. |
| Claude Code | 20 min + lab | **Learn** the next unfed topic on the [Claude_Code/](Claude_Code/README.md) path, then paste what you learnt. **Build** the first unticked lab in a fed note. |

**How it picks**, all derived and nothing stamped:

- **Area** rotates daily through Core dev, Architect, Agentforce and Data 360 (`STUDY_AREAS` in `scripts/vault.py`).
- **Topic** — an open [WEAK-ANSWERS](Interview/WEAK-ANSWERS.md) row in that area first. Then a new note an interview question probes, then one a flashcard cites, then read order. Then the note studied longest ago.
- **Reviews** come back 3, 7, 16, 35 and 75 days after each tick. A Claude Code note counts its `created` date as its first tick, because you feed it rather than `today` picking it.
- **Claude Code** is a track outside the rotation. The first README path row with an empty `Note` cell is the Learn line. A fed note's first unticked lab is the Build line.
- **The record is the tick.** A ticked `- [x]` line in a journal file is what counts as studied. An unticked pick is a day skipped, and it comes back.

### 3. Gaps — scoped to where you actually are

Every note carries a level:

```yaml
---
vault: SF_Agentforce
format: light
level: basic
status: open
gaps: 4
created: 2026-08-27
updated: 2026-08-27
---
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

IDs are `<VAULT>-<TOPIC>-NN` — `AF-TRUST-01`, `AF-ATLAS-02`, `EC-I18N-01`, `SVC-OMNI-01`, `SLS-LEAD-01`. Stable, never reused, so you can say "close AF-ATLAS-02" and so the practice queue can point at a lab without copying its text.

**The doing view is a separate file.** Each vault gets a `PRACTICE.md`: `▶ Next` (exactly one), `In flight` (max 3), a dependency-ordered `Queue` with a time box and a `Proves` phrase, and a `Done` table. The note is where a lab is captured; `PRACTICE.md` is what you open when the goal is to *run* something. See [SF_Agentforce/PRACTICE.md](SF_Agentforce/PRACTICE.md).

**A lab is not finished until you have written down what broke, verbatim.** That is the `Done` table's last column. Notes get rewritten and releases move on, but an exact error string is still what you type into a search box in six months. `no failure; worked first time` is a real result too — it tells you the lab was too gentle.

Two things `PRACTICE.md` deliberately does **not** have: progress counters, and a copy of the lab text. `Done` is append-only, which is far harder to desync than a tally, and the note stays the single source of truth for what a lab actually is.

### 4. Cross-vault links go both ways

**When a link crosses vaults, the far side gets a link back — in the same edit.**
When an Agentforce note links to an Apex note, the Apex note links back.

**Same-vault links do not need one.** Obsidian's Backlinks panel already shows
every inbound link for free, so a hand-written return bullet inside one vault is
duplicated effort. The rule used to apply to every link and sat at 50% compliance
— including in notes written the same week the rule was restated. A rule kept half
the time is not a rule.

A cross-vault link is different: it is the jump a reader cannot guess, and on
GitHub there is no panel to fall back on. Those are worth writing by hand.

**The reason clause is the point, not the link.** `— the *other* kind of action,
and the description-as-specification rule both share` is knowledge. A generated
`— see also` is filler that looks finished. `vault.py` reports a missing return
link and never writes one.

### 5. Dates, status and sources

**Metadata is YAML frontmatter.** Obsidian reads it as Properties — that is what
makes the Bases views, property search and sorting in [HOME.md](HOME.md) possible.
It replaced a `>` blockquote, which no tool could read.

**Four keys are the machine's; the rest are yours.** `python scripts/vault.py fix`
recounts `status`, `gaps`, `org_checks` and `labs` from the note body and will
overwrite whatever you type there. `vault`, `area`, `format`, `level`, `created`,
`currency`, `phase` and `tags` are yours — edit them in Obsidian's Properties
panel and the tool leaves them alone.

**Status is derived, never typed.** Count the `- [ ]` lines in `## Gaps to close` — and only those. `## Confirm in org` bullets and `## Hands-on` labs never count:

- at least one → `status: open` with `gaps: N`
- none, or no section at all → `status: complete`

A note can be `✅ complete` and still carry org checks. Complete means *the research is done*, not *there is nothing left to verify*.

Delete a gap and the status moves on its own. A typed status goes stale the first time you forget to update it.

**Dates.** `created` never changes. `updated` changes on every edit. Notes written
before the frontmatter migration had their dates backfilled from git history, but
an authored date always won — nothing hand-written was overwritten.

**Staleness is derived, not stamped.** There is no `⏳` line to add or remove any
more; `vault.py` computes age from `updated` and [HOME.md](HOME.md) lists what has
gone 3+ months. One fewer thing in the file that can be wrong.

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
| 2026-09-24 | `SF_Service/` created as a root vault for Service Cloud | Enhanced Chat, Omni-Channel and the handoff to a human fail the routing test for `SF_core/` — strip Service Cloud out and the sentence falls apart. Nothing owned them: most Service terms had zero hits in the repo. |
| 2026-09-24 | Service Cloud content was **extracted, not moved** | Only `SF_Experience_Cloud` · 19 had a real Service core, and its guest-exposure half belongs where it is. The Service half became `SF_Service/` notes; 19 keeps its number and points across. Queues and assignment rules stay in `SF_core/` because they also work on Lead, Task and custom objects. |
| 2026-09-24 | `SF_Sales/` created as a root vault for Sales Cloud | Forecasts, splits, Path, territories and campaign influence fail the routing test for `SF_core/`. `SF_core/README.md` had parked "Sales Cloud functional depth" as a future area; a peer vault matches how Service Cloud was handled the same day. |
| 2026-09-24 | Sales Cloud content was **extracted, not moved** | Only `SF_core/07` · 10 fails the test by subject, and it is written as a sharing note: `RowCause`, share-row growth, a second hierarchy. It keeps its number and phase; the selling side became `SF_Sales/` notes, linked both ways. The Sales rows in `08` · 04 and `08` · 22 stay as the object-graph and currency summary. |
| 2026-08-27 | Level beats migration depth | A one-line note of yours does not get replaced by 119 lines from the archive. Write at your level; the depth arrives when your notes do. |
| 2026-10-02 | Every note gets a `## My recall` layer on top, in the user's words; Claude may tighten it but never add to it | The vault was almost entirely Claude-written: 0 of 189 labs done, the journal empty, and "not my words" was the first complaint. Self-generated material is remembered better than read material, d ≈ 0.40 across 86 studies ([Bertsch 2007](https://pubmed.ncbi.nlm.nih.gov/17645161/)). People who wrote with an LLM could not quote their own essays minutes later ([Kosmyna 2025](https://maketecheasier.com/mit-researchers-wired-eeg-sensors-onto-54-people-writing-essays-and-found-that-the-group-using-chatgpt-not-only-thought-the-least-measured-by-brain-connectivity-but-afterwards-mostly-could-not-recal/) 🚩 preprint). |
| 2026-10-02 | `RECALL.md` per vault, generated from the recall layers | The user's interview habit is reading a short summary top to bottom. Generating it from the notes means it cannot drift from them. |
| 2026-10-02 | `npm run today` replaces HOME's single-lab pick with a daily session: recall first, then the note | Practice testing and spacing are the only techniques rated high utility; rereading is rated low ([Dunlosky 2013](https://www.psychologicalscience.org/news/releases/which-study-strategies-make-the-grade.html)). Recall beat restudy 80% to 36% after a week ([Karpicke & Roediger 2008](https://sciencedaily.com/releases/2009/12/091210125928.htm)). 189 queued labs were "too many to start". |
| 2026-10-02 | Claude checks, flags and researches, and does not author what the user learns from | Unrestricted GPT-4 raised practice scores 48% and cut exam scores 17%; a tutor that gave hints, not answers, caused no loss ([Bastani, PNAS 2025](https://papers.ssrn.com/abstract=4895486)). Release changes are flagged for the user to fix: re-encoding was how the old Notion notes stuck. |
| 2026-10-02 | Flashcards moved from the `## Recall` export to a hand-written bank in `Flashcards/` | You found the 1,201 exported Recall pairs useless for interviews: single facts with no scenario and no level. The bank is written for architect and senior-developer interviews, split Foundations/Hard by topic, and syncs to Anki with IDs so edits keep review history. `## Recall` stays in notes as a self-check; the two `_cards.md` decks were deleted. |
