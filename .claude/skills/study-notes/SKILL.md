---
name: study-notes
description: Turn rough, out-of-order Salesforce learning notes into ordered wiki notes across SF_core, SF_Agentforce, SF_Data_360, SF_Experience_Cloud, SF_Service and SF_Sales. Use whenever the user pastes study notes, says "I learned X today", dumps rough bullets about a Salesforce, Agentforce, Data 360, Service Cloud or Sales Cloud topic, or asks to file notes into the vault.
allowed-tools: Read, Write, Edit, Grep, Glob, WebFetch, WebSearch, AskUserQuestion
---

The user pastes rough notes. You file them.

Their notes arrive in whatever order they learned things. Your job is to put each piece in the right file, in an order they can learn from later.

Read [NOTES-SYSTEM.md](../../../NOTES-SYSTEM.md) once per session for the full contract. This file is the procedure.

## 1 · Split

Break the dump into distinct topics. One topic, one note.

A single sentence can belong to two topics. That is normal. Split it and cross-link.

Do not merge unrelated things into one file just because they arrived together.

## 2 · Route

One question per piece:

> **Strip the product out of the sentence. Is it still true?**

Ask it once per product: *with no Agentforce in it?* *With no Experience Cloud site in it?* *With no Service Cloud in it?* *With no Sales Cloud in it?*

- **Still true** → `SF_core/`, in the numbered area it fits.
- **Falls apart** → the vault that owns that product: `SF_Agentforce/`, `SF_Data_360/`, `SF_Experience_Cloud/`, `SF_Service/` or `SF_Sales/`.

If a topic has both sides — say "a prompt template can call Apex", or "an agent embedded on a public site" — write **both** notes. The product vault says why. The `SF_core` note says how. They link to each other.

Cannot route it? One dated bullet in that folder's `_inbox.md`. Move on. Never stall.

## 3 · Check before you write

Always search first. Duplicates are the main failure mode here.

- `Glob` the target folder for a matching filename.
- `Grep` all six vaults for the topic's key terms: `SF_core/`, `SF_Agentforce/`, `SF_Data_360/`, `SF_Experience_Cloud/`, `SF_Service/`, `SF_Sales/`.
- Also grep `_archive/AI_Data/` — it is a **quarry** for verified facts, never a link target.

Then decide:

| Found | Do |
|---|---|
| A note in the target folder | **Update it.** Merge the new facts in. Raise `Level` if the notes went deeper. |
| A note in `SF_core/` or `SF_Experience_Cloud/` in the old dense format | **Enrich it in place.** Add the cross-link and a `## Gaps to close` section. Do not create a second light file beside it. |
| Only an `_archive/AI_Data/` note | **Quarry it.** Pull verified facts into the new note, **cut to the user's level**. Never link back to the archive. |
| Nothing | **Create it.** |

## 4 · Write

Use [templates/note.md](../../../templates/note.md).

- Filenames carry **no number**. `flex-prompt-templates.md`, not `05-flex-prompt-templates.md`.
- **50 lines max, counted to `## Related`.** The footer — `## Related`, `## Sources`, `## History` — does not count. Never drop a citation to hit a line budget.
- No paragraph longer than two sentences.
- One table max. One code block max, 12 lines.
- Metadata is YAML frontmatter. Run `python scripts/vault.py fix` after writing; it sets `status`, `gaps`, `org_checks` and `labs` from the body. Never type those four.

Keep the user's own wording where it captures a real gotcha:

```markdown
> **From my notes.** <their words> — <inline correction if it is wrong>
```

That callout is how they tell what they wrote from what you added. Use it.

Set `Level` from the depth of what they actually gave you:

- `basic` — what it is, where to find it, what it is for.
- `working` — configuration, types, limits, when to pick which.
- `deep` — code, API surface, edge cases, performance.

## 5 · Gap pass

This is the part the user cares about most. Get the scope right.

> **Gaps may go ONE level above the note's `Level`. Never two.**

| Note is | Gaps may be |
|---|---|
| `basic` | basic, working |
| `working` | working, deep |
| `deep` | anything on this topic |

A `basic` prompt-template note gets gaps like *"can Sales Email ground on Lead as well as Contact?"*

It does **not** get `@InvocableMethod`. That is `deep`, two levels up. Hold it back until the note's level rises.

Also:

- **Same topic only.** Never a syllabus. Never "you should also learn Data 360."
- **Be specific.** Name the object, setting, limit or field. A gap that could apply to any topic is not worth a line.
- **Documentation considerations count.** Supported objects, limits, licence requirements, known restrictions — these are good gaps when the user's note skipped them.
- Put the checklist under `## Gaps to close`.
- Put a `> **Gap.**` callout inline instead when the hole sits mid-topic and would confuse the bullets around it.
- **If no public doc can answer it, it is not a gap.** Put it under `## Confirm in org` as a `- 🚩 ` bullet and say what to open. Those bullets never count towards `Status`.
- **Check the other notes before you write a gap.** The same question sitting in two files is counted twice and answered never. One note owns it; the others link to that note.

## 5a · Lab pass

Gaps and org checks are questions. **Labs are skills** — what the user builds to find out whether they can actually do this.

Every note gets **3–4** under `## Hands-on`, one line each:

```markdown
- [ ] **AF-VER-02** · 10 min · Deactivate the active version without activating another, then call the template. **Proves:** nothing is active and the template stops working — nothing prompts you to choose.
```

Grammar, in order: **ID · time box · what you do · `Proves:` · `Needs:`** (licence, Data 360, 2nd org — omit if none) **· `Settles:`** (the 🚩 it answers — omit if none).

- **Every lab needs a `Proves:`.** A lab without one is a chore. "Build a Flex template" is a chore; "prove an unactivated template is invisible to an agent" is a lab.
- **Roughly a third should break something on purpose.** `## Gotchas` is already a list of things that break — mine it. A failure caused deliberately once is one the user will recognise at a client.
- **Scope to the note's `Level`**, same ceiling as gaps. Nothing over 45 minutes; if a lab needs more, split it `NNa` / `NNb`.
- **IDs are `<VAULT>-<TOPIC>-NN`**, stable and never reused. `AF-` for SF_Agentforce, `EC-` for SF_Experience_Cloud, `SVC-` for SF_Service, `SLS-` for SF_Sales.
- **Ticked, never deleted** — the opposite of the gap rule. Labs never count towards `Status`.

## 5b · Close pass

Opening gaps without ever closing them makes the count climb forever. Before you write to a note that already exists:

1. **Read its `## Gaps to close` first.**
2. **Answer every one the new feed resolves.** Put the answer in the note body, then delete the gap line.
3. **Say so in `## History`** — what was answered, not how many.

Two rules keep this honest:

- **A research pass that spawns a deeper note must say so in the report.** That is what keeps the total flat, and the user should hear it from you rather than work it out from the index.
- **Never close a gap by asserting.** If you cannot source the answer, either leave the gap or move it to `## Confirm in org`.

## 6 · What you write, and what the tool writes

**Closed gaps are deleted, not ticked.** When you answer a gap, remove its line. When the last one goes, remove the `## Gaps to close` heading with it. The answer belongs in the note body; a checklist of settled questions is clutter.

**Never close a gap by asserting.** If you cannot source the answer, either leave the gap or move it to `## Confirm in org`. A `✅ complete` note may still carry org checks — complete means the research is done, not that nothing is left to verify.

**Sources.** Every fact you researched gets a `## Sources` entry with the date you read it. Salesforce domains are trusted; anything else carries 🚩.

**History.** One dated line per feed, under `## History`, saying what was **added or changed**. Never a gap tally.

### Then run the tool — do not do this by hand

```
python scripts/vault.py fix      # recounts status, gaps, org_checks, labs
                                 # rebuilds INDEX rows, summary lines, README
                                 # counts and the PRACTICE Done table
python scripts/vault.py home     # rebuilds HOME.md
python scripts/vault.py check    # reports whatever is left
```

`fix` owns exactly four frontmatter keys — `status`, `gaps`, `org_checks`, `labs` — and recomputes them from the note body. **Never type those four.** `vault`, `area`, `format`, `level`, `created`, `currency`, `phase` and `tags` are the user's, and the tool leaves them alone.

Staleness is derived from `updated`, not stamped into the file. There is no `⏳` line any more.

## 7 · Link both ways, across vaults only

A link that **crosses vaults** gets a link back, in the same edit. Same-vault links do not — Obsidian's Backlinks panel shows those for free.

Write the Agentforce note's `## Related` bullet pointing at the Apex note. Then open the Apex note and add its bullet pointing back.

**The reason clause is the content.** `— the *other* kind of action, and the description-as-specification rule both share` is knowledge. `— see also` is filler. Never generate one.

Relative markdown links only. No `[[wiki links]]` — nothing in this repo uses them.

## 8 · What is still yours to place

`vault.py fix` rebuilds the index rows, counts and queues. Three things it cannot decide, because they are judgement:

- **Where a note's `#` row sits** in the `INDEX.md` learning path, and its `Pre` prerequisite. That is pedagogical order, not data.
- **Where a lab sits in the `PRACTICE.md` queue.** The queue is **unblocked-first**, not INDEX order — labs needing Data 360, an extra licence or a second org go later, so the user is never blocked twenty minutes in. The `Proves` phrase there is 3–6 words, never a copy of the note's sentence.
- **The `LEARNING-LOG.md` entry**, newest first — what you fed and why.

## 9 · Facts you are not sure of

- Release-dependent or version-dependent → check `RELEASE-RADAR/` first. It is the repo's source of truth for what changed and when.
- Still unsure → `WebFetch` `help.salesforce.com` or `developer.salesforce.com`.
- **Salesforce Help pages are JS-rendered and often return only a nav shell.** When that happens, try Trailhead or the developer blog, which serve static HTML. If nothing confirms it, do not guess.
- Cannot confirm → write it with 🚩, or with the suffix `*(unverified — confirm in org)*`.
- **Never invent a Salesforce feature, limit or object name.** A wrong fact learned confidently is worse than a gap.
- Never use 🆕 or ⚠️ as confidence markers. Those mean something specific in the `SF_core/README.md` flag legend.

Two live currency traps to watch for in the user's notes:

- Agents are authored in **Agent Script**. The legacy topics-and-instructions builder stopped creating new agents the week of 2026-07-13.
- **Data Cloud is Data 360.**

If their note contradicts one of these, correct it inline in the `> **From my notes.**` callout. Do not silently drop what they wrote.

## 10 · Report back

Short. Bullets. No paragraphs.

- Files created, with paths.
- Files updated, and what changed in each.
- Corrections made to what they wrote, and why.
- Gaps **closed**, and gaps added with the level you scoped them to.
- Whether a research pass spawned a new deeper note — say it plainly, it is why the total may not fall.
- Anything moved to `## Confirm in org`, and what to open in the org to settle it.
- Labs added, their IDs, and where they landed in the `PRACTICE.md` queue.
- Reciprocal links added.
- Anything sent to `_inbox.md`, and why.
- Anything you marked 🚩 and want them to confirm in an org.

Ask a question only when routing is genuinely ambiguous. Otherwise decide, file it, and say what you decided.
