# Routine prompt — `Salesforce AI release radar`

The prompt the scheduled task runs. **This file is the source of truth; the Routine holds a copy.**

- **Trigger:** `trig_01HCBSABVKNgsM9mZa2zYkHj` · cron `30 3 * * *` (UTC) · model `claude-opus-5`
- **To change it:** edit this file, then paste the block below into the Routine's prompt field on claude.ai. The Routine was created through the web API, so an agent session cannot update it in place.

> **⚠️ One setting cannot be fixed from the prompt.** The Routine's *outcome branch* is set to
> `claude/eloquent-knuth`, so every run pushes to `claude/eloquent-knuth-<suffix>` instead of `main`.
> That is why the **2026-08-03, 08-06, 08-07 and 08-15** scans were invisible to the runs that followed
> them — each one read a stale radar and re-derived work already done. **Set the outcome branch to `main`
> in the Routine's settings.** Step 10 below tells the run to verify its push landed, but that is a
> backstop, not a fix.

---

## Prompt

````markdown
# Release radar — daily scan routine

**Goal:** find genuinely noteworthy Salesforce technical updates from the last ~24 hours (extend to 72 hours if the last 24h are thin) in three areas — **Agentforce**, **Data 360** (ex-Data Cloud), and **Salesforce AI Research** — and record them so they can be *learned from*, not just skimmed.

**Model:** Opus, extra-high thinking.

**The contract you write to lives in the repo,** at `AI_Data/05-release-radar/README.md` → **Writing contract**. Read it at the start of every run. It holds the signal gate, the routing table, the entry templates, the write discipline, the size budgets and the standing notes. Where this prompt and that section disagree, the README wins — it is the version that gets maintained.

---

## The one thing to get right

**Most runs find nothing in most areas. That is the normal case, and it must not produce a file.**

The radar's failure mode is not missing news — it is manufacturing text on quiet days. Before this contract, 14 of 42 dated notes said only "nothing cleared the relevance bar", `agentforce-adlc` was restated 23 times with only its idle-day counter changing, and the README grew from 15KB to 87KB in a fortnight by appending where it should have replaced.

Four files, four jobs:

- **Topic files** (six, at `AI_Data/05-release-radar/`) — the deliverable. Substance goes here and nowhere else.
- **`scan-log.md`** — one row per scan. This is the audit trail. A quiet day costs one `—`.
- **`watchlist.md`** — everything you check and its current state, updated **in place**. Unchanged state lives here and is restated nowhere else.
- **Dated notes** (`01-agentforce/`, `02-data-cloud/`, `03-salesforce-ai-research/`) — written **only for an area that routed at least one item to a topic file this run**. They point at substance; they never hold it.

Plus **`method-notes.md`** — lessons about *how to check*, one line each, max one new line per run.

---

## The relevance bar

An item earns a place only if it changes what an **Architect**, a **Developer**, or an **Admin** would actually do. Three tests — an item needs to pass **at least one**:

- **Architect** — it changes a design decision. New or changed limits and quotas, licensing or entitlement that gates a capability, data residency and storage boundaries, integration or grounding patterns, GA / EOL / deprecation of something you would build on.
- **Developer** — it changes code. An API version or endpoint, metadata type, CLI command, SDK or npm package, schema, platform event, or a breaking change to something that already ships.
- **Admin** — it changes the org. Setup UI, permission sets, feature toggles, enablement steps, enforcement dates, migration deadlines — anything that requires a human to go click something before it works.

Fails all three → **it does not go in.** Specifically excluded: keynote and event announcements with no shipped artifact, roadmap items with no date and no surface, customer stories, analyst placements and awards, marketing rebrands with no functional change, blog posts restating a feature the radar already holds, and repo churn (CODEOWNERS, dependabot, README edits, version bumps with no behaviour change).

**The drop test.** If you cannot write a `**Study action:**` that someone could carry out *today* in a dev org, a repo, or the CLI, the item has not shipped enough to be worth recording.

**Version state is not news.** A version number, dist-tag position, commit hash or idle-day count that has not changed behaviour you can act on is **state**. It goes in `watchlist.md` and nowhere else — no entry, no paragraph, no *State of play* sentence. Five consecutive scans once narrated an unmoving `@salesforce/cli` `latest` tag as a *stall*; the project had published its Wednesday release cadence in its own release notes.

**An empty run is a valid run.** Write no topic entries, put `—` in the `scan-log.md` row, bump `watchlist.md`, and spend the run on step 6. Do not lower the bar to fill a file.

## Step 1 — Scan

Search Salesforce blogs, release notes, documentation updates, official announcements, and the relevant GitHub repositories for new features, pricing changes, product launches, deprecations, or significant technical improvements in the three areas. `watchlist.md` names what to check and where each thing stood last run — start there.

- **Exclude general AI industry news** (OpenAI, Anthropic, Google, etc.) unless directly tied to a Salesforce product, partnership, or integration.
- **Record the UTC timestamp of every check.** A negative finding expires.
- Read the **Standing notes** in the README before concluding anything is absent. Several key domains return HTTP 403 or `EGRESS_BLOCKED` to automated fetching, and a July 2026 org-wide CODEOWNERS sweep makes many Salesforce repos look freshly updated when nothing shipped.
- Read `method-notes.md`. It lists the ways this radar has already been wrong. Do not re-learn one.

If the 24h window is thin, extend to 72h. If 72h is genuinely empty — or everything in it fails the relevance bar — **do not pad**. Go to step 6.

## Step 2 — Gate, route, and dedupe *before* writing anything

For each candidate, in this order:

1. **Run the relevance bar.** Which of Architect / Developer / Admin does this change something for, and what? If none, it is not an item.
2. Grep all **six** topic files for the feature name and its identifiers.
3. Classify it: **new** / **update to an existing entry** / **correction to an existing entry**.
4. Pick exactly one canonical topic file from the routing table in the README. Other topic files get a one-line cross-link, never a copy.

## Step 3 — Write the topic-file entry

Use the entry template in the README verbatim. Order within the file is newest-first. Order of new entries added in one run is most-consequential-first.

Write for someone who wants to **learn** the thing. Define jargon on first use. Length is not how you achieve that:

- **No paragraph over ~60 words.** If a paragraph is enumerating — "four skills:", "(1)…(2)…(3)" — it is a list, so make it a list.
- **`**Relevant to:**` on every entry.** `Architect`, `Developer`, `Admin`, or any combination, plus half a sentence on what it changes for each. This is the gate's receipt. If you cannot fill it, the entry should not exist.
- **`**Why it matters.**` is a fixed literal string.** It must stay greppable.
- **`**Study action:**` on every entry.** One concrete thing to do in a dev org, a repo or the CLI.
- **`**Gotchas:**` whenever the item has an API, CLI, metadata type, permission set or config surface** — with exact identifiers.
- **Mermaid diagrams go here, in the topic file** — for a flow, a routing decision, or a dependency graph. Never in a scan log.

**Write discipline:** new entry → append at the top. Status change → mutate in place and prepend `> **Correction (YYYY-MM-DD):** <what this said before, what it is now>`. **Never bump an existing heading's date** — other files link to it as an anchor. Never delete a superseded claim; supersede it visibly.

## Step 4 — The signal gate: decide what files exist at all

For **each area**, exactly one of these three:

| Condition | What you write |
|---|---|
| The area routed ≥1 item to a topic file | A dated note **+** its `scan-log.md` cell |
| Nothing cleared the bar | `—` in the `scan-log.md` cell. **No file.** |
| 5th consecutive quiet scan for that area | **No file.** Spend that area's budget on a gap check (step 6) and record what you checked |

**Never create a file whose `## What changed` says that nothing changed.** `scan-log.md` is the audit record; a note that routes nothing is not one.

The dated note, when it exists, is **≤12 lines**: title, `**Window:**` line, and the routed items. Nothing else.

- **No `## Verified negatives` section.** Abolished — that is `watchlist.md`.
- **No `## Watched, not recorded` section.** Abolished — a watched item gets a `watchlist.md` row **with a re-check date**, or it goes nowhere.
- **No streak counts, no "Nth consecutive scan", no method notes, no gap-check essays.**
- Every `## What changed` bullet links to a real anchor in a topic file.

## Step 5 — Update `watchlist.md` in place

Bump `Last checked` on every row you checked. Change `Current state` only when it actually changed. Add a row for anything new worth tracking; delete rows that stopped mattering. `git log -p watchlist.md` is the audit trail — that is why nothing here is restated in prose.

A negative earns prose in exactly two cases: it **closes an open question**, or it **contradicts something already published** (then it is a `> **Correction**` on the entry that was wrong).

## Step 6 — Coverage, staleness and gap checks

Report the last-touched date of all **six** topic files in the README's single *Coverage and staleness* table, **overwriting** it. The table is the whole report — **no "method finding" essay, no "next to watch" prose.**

- Anything untouched **>14 days** gets a gap check that run.
- An **area quiet for 5 consecutive scans** gets a gap check instead of a sixth identical scan.
- Apply the same relevance bar to whatever a gap check turns up.

Gap checks are where this radar's best output comes from — a flagship product (Agentforce Coworker) that had never been recorded at all, and an "unobtainable" API version that was sitting in a repo already on the weekly list.

## Step 7 — Feed the study base

- New jargon defined in an entry → the right alphabetical section of `AI_Data/GLOSSARY.md`.
- Each scan that produced an entry adds strict `Q:` / `A:` pairs to the relevant `AI_Data/02-salesforce-ai/NN-topic/flashcards.md`.
- An item big enough to be its own subject (a product or capability with its own surface, not a version bump) → next-numbered `NN-kebab-case` folder in `AI_Data/02-salesforce-ai/` from `AI_Data/_templates/`, update that INDEX, and link it from the radar entry with a `**Study folder:**` line.

Never modify `ai-salesforce-architect-roadmap.html`.

## Step 8 — Weekly consolidation (first run on or after Sunday)

- Rewrite **State of play**: 5 numbered items, then **one** additions paragraph of **≤150 words**. The previous additions paragraph is **replaced, not demoted to "Previous additions".** Its substance is already in the topic files.
- **Prune** *Open questions to chase*: delete answered ones outright rather than striking them through and keeping them. Keep each ≤60 words.
- Refresh the `scan-log.md` quiet-streak table and the README footer date.
- Reconcile any item that has landed in two topic files.

## Step 9 — Size budget, checked before committing

| File | Budget |
|---|---|
| `README.md` | **≤4,000 words** (`wc -w`) |
| *State of play* | 5 items + one ≤150-word additions paragraph |
| *Open questions* | ≤60 words each |
| *Coverage and staleness* | **one** section, overwritten |
| A dated scan note | ≤12 lines |
| `method-notes.md` | one new line per run, max |

If the README is over, prune *Open questions* first. **Every budget says replace, not append** — appending is what took the README to 87KB.

## Step 10 — Commit

**Commit directly to `main`.** Pull, commit, push to `main`. One commit per run, subject `Release radar: YYYY-MM-DD scan`.

**Verify the push landed on `main` before finishing.** Scans on 2026-08-03, 08-06, 08-07 and 08-15 committed to `claude/*` branches instead and were invisible to every later run, which then re-derived work already done. If you cannot reach `main`, say so loudly in the run output rather than leaving the work on a branch silently.

A run with no qualifying items still commits — the `scan-log.md` row and the `watchlist.md` diff are the log, and the log is the point.

Repo: `Daniel-Deepak-Dev/myLearning`, path `AI_Data/05-release-radar/`.

---

## Self-check before committing

- [ ] **No file was created whose only content is that nothing happened.** Quiet areas got a `—` in `scan-log.md` and nothing else.
- [ ] **No unchanged version state was written as prose** anywhere — no dist-tag position, commit hash or idle-day count outside `watchlist.md`.
- [ ] No `## Verified negatives` or `## Watched, not recorded` section exists in any note.
- [ ] No "Nth consecutive scan", no "this radar", no paragraph whose subject is the scanning process — outside `scan-log.md` and `method-notes.md`.
- [ ] Every recorded item clears the relevance bar, and `**Relevant to:**` names which role and why.
- [ ] Every new topic entry has `**Why it matters.**` as that exact string, plus `**Relevant to:**`, `**Study action:**`, `**Status:**`, `**Sources:**`; `**Gotchas:**` wherever there is a technical surface.
- [ ] No paragraph over ~60 words; no enumeration left as prose.
- [ ] Each item appears in exactly one topic file; cross-references are one-liners.
- [ ] Each dated note is ≤12 lines and every `## What changed` bullet resolves to a real anchor.
- [ ] Topic-file headings read newest-first; no existing heading's date was changed; status changes are `> **Correction (…)**` blockquotes.
- [ ] `watchlist.md` updated in place; `scan-log.md` has this run's row.
- [ ] Coverage table **overwritten**, not appended. `wc -w README.md` under 4,000.
- [ ] Glossary and flashcards updated where the scan introduced new terms.
- [ ] **Committed and pushed to `main` — verified, not assumed.**
````

---

## What changed from the previous prompt, and why

| Change | The failure it fixes |
|---|---|
| **Step 4 signal gate** — a note exists only for an area that routed an item | 14 of 42 dated notes said only "nothing cleared the relevance bar" |
| **Step 5 `watchlist.md`** replaces per-note `## Verified negatives` | `agentforce-adlc` restated 23 times, changing only "13 days idle" → "14" → "15" |
| **`## Watched, not recorded` abolished** | 21 sections recording items the routine had just decided were not worth recording |
| **"Version state is not news"** added to the relevance bar | Five scans narrated an `@salesforce/cli` dist-tag that had not moved |
| **"The radar does not write about the radar"** | 23 "this radar…" phrases and 4 "Method finding" essays in the README alone |
| **Step 9 size budgets, all replace-not-append** | README grew 15KB → 87KB in 13 days |
| **Step 8 replaces the additions paragraph** instead of demoting it | 15 stacked "Previous additions" paragraphs, 5,940 words duplicating the topic files |
| **Quiet-area escalation to a gap check at 5 scans** | Data 360 was re-scanned identically for 6 quiet scans and reported as such each time |
| **"six topic files"**, and `**Relevant to:**` now in the README template | The prompt said five and required a field the template omitted |
| **Step 10 verifies the push landed on `main`** | Four scans lost to `claude/*` branches |
