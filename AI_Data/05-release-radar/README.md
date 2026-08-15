# 05-release-radar — Salesforce AI / Agentforce / Data 360 updates

**What this is:** a running log of Salesforce technical updates worth knowing as an AI-Salesforce architect. Fed by the `Salesforce AI release radar` scheduled task, which writes to the [Writing contract](#writing-contract) below.

**How it's organized.** Five kinds of file, and only the first is for learning from.

- **Topic files** at the root are **the layer to learn from** — the *running story* of one subject, newest-first, each entry carrying **What changed / Why it matters / Gotchas / Study action / Status / Sources**. They stay at the root because most cut across areas.
- **[scan-log.md](scan-log.md)** — one row per scan: did a scan run, and did it find anything. A quiet day reads as a quiet day here, at one row.
- **[watchlist.md](watchlist.md)** — what gets checked and where each thing stands. Updated **in place** every run. Unchanged state lives here and is restated nowhere else.
- **Dated scan notes** in [`01-agentforce/`](01-agentforce/), [`02-data-cloud/`](02-data-cloud/), [`03-salesforce-ai-research/`](03-salesforce-ai-research/) — written **only when that area routed at least one item to a topic file**. They point at the substance; they do not hold it.
- **[method-notes.md](method-notes.md)** — sourcing and versioning mistakes, one line each, learned once.

**How to read it:** skim *State of play* below → open the topic file for the subject you care about → use [scan-log.md](scan-log.md) only when you need to know *when* something was recorded.

> Notes dated 2026-07-26 → 2026-07-31 predate this contract and are full write-ups. They are left as-is.

## Topic files — the running story

| File | Covers |
|---|---|
| [agentforce-platform.md](agentforce-platform.md) | Agentforce Builder, Agent Script, Multi-Agent Orchestration, Voice, Contact Center, mobile SDK, observability |
| [data-360.md](data-360.md) | Data 360 (ex-Data Cloud): SOQL changes, Code Extension, Intelligent Context, semantic layer, zero-copy |
| [developer-tooling-and-apis.md](developer-tooling-and-apis.md) | Hosted MCP servers, Headless 360, **MuleSoft Agent Fabric**, **ADLC workflow**, Apex/LWC changes, CLI, Agentforce Vibes, Agent Skills |
| [trust-security-and-governance.md](trust-security-and-governance.md) | Einstein Trust Layer, user-mode defaults, SOAP login retirement, secrets handling |
| [pricing-and-certification.md](pricing-and-certification.md) | Flex Credits, pay-per-resolution, Agentforce Specialist exam changes |
| [ai-research-and-benchmarks.md](ai-research-and-benchmarks.md) | Salesforce AI Research: CRMArena, GIFT-Eval, AnchorBench, MFCL Audio, LoCoBench-Agent, EDR, and the licences on them |

## State of play — as of 2026-08-15

Five things define the current Salesforce AI landscape. If you only retain five, retain these.

1. **The season turned: Winter '27 release notes are live, and the next eight weeks are a migration window, not a reading exercise.** Sandbox refresh cutoff **Aug 27, 18:00 PT**; preview instances upgrade **Aug 28–29**; production weekends **Aug 29 / Oct 3 / Oct 10**. **Two** Release Updates will break things quietly, and they fail differently: the **retirement of the OAuth 2.0 username-password flow** — every script posting `grant_type=password` stops getting a token on its org's upgrade date — and the **end of support for incorrect instanced URLs in API traffic**, which is not a code pattern but a *value* that went stale when Salesforce moved your org between instances, enforced **rolling** rather than on a date. Summer '26 remains the current GA release.
2. **Headless 360 is still the organizing theme, and the agent surface keeps widening underneath it.** Every major capability is reachable as an API, an MCP tool or a CLI command; hosted MCP servers are GA. What 08-09 adds is that the surface is now wider than the announcements — a default-enabled **`sf-data360`** extension with eleven `data360_*` tools shipped inside a repo on the weekly source list, with no press release at all.
3. **Agent Script + the new Agentforce Builder are GA** — since the week of **July 13, 2026** the *New Agent* button opens nothing else — and Agent Script is **open source** (Apache 2.0). But the platform now authors agents **two contradictory ways**: Agent Script (explicit, version-controlled) and the **digital blueprint** of Agentforce Operations (generated from a document or diagram, edited in prose). One governance model does not cover both.
4. **Data 360 is the context engine, and it finally has a first-class Apex surface.** The rename is real (SKUs, release notes, the consultant cert). Winter '27 adds the **`sfsqlquery`** namespace — `SqlStatement`, `SqlRowIterator`, `Row`, `QueryHandle`, `SqlQueueable` — so an agent action can compute a live aggregate instead of reading a scheduled insight. The dataspace trap survives intact: omit it on a DLO query and get **zero rows, silently**.
5. **Security defaults flipped, the boundary runs both ways, and commercials moved to consumption.** At API 67.0, Apex DML/SOQL run in **user mode** and classes default to **`with sharing`**; the **metadata pipeline is an inbound trust boundary too** (the SDR zip-slip); and IL5 showed the Trust Layer decides **which models exist at all** in an environment. On price: **Flex Credits** ($500 / 100k, ~$0.10 per action), **pay-per-resolution** at $2 for the Help Agent, and negotiated **AELAs** at the top end.

**Newest additions (scan of 2026-08-15, 03:37 UTC):** `@salesforce/agents` **2.0.2** — `sf agent preview --api-name` silently discarded `--context-variables`; the wire field is `variables`, and a truthy options object also enabled Apex debugging and created TraceFlags unasked. Second `--api-name` vs `--authoring-bundle` divergence in five days. `sf-skills` **1.38.0** adds 17 skills; `accessCheck` gains an `orgPref` type and is **ANDed with no OR operator**, and a fifth unannounced MCP server (`media-management`) appears in `mcpTools`. From 08-14: **SDR 13.1.1** patches a TOCTOU symlink escape in the same transformer as the zip-slip, and `sf project retrieve start --root-type-with-dependencies` takes a closed enum of `Bot` and `AiAgentDefinitionVersion`. The rule to keep is the pinning asymmetry: **`sf` pins plugins exactly; plugins range their libraries** — so a library patch reaches stable on a fresh install, a plugin feature cannot.

## Open questions to chase

- **Three undated `sf-pi` breaking changes.** The `CHANGELOG` keeps everything under a permanent `## Unreleased` heading, so no change can be tied to a release. **(1) Agent Script publish is eval-gated** — always creates an inactive `BotVersion`, `publish activate=true` is removed, escape hatch is `acknowledge_untested_activation=true`. **(2)** `SF_KERNEL.md` is no longer read; guidance is append-only via `sf-brain/SF_CONSTITUTION_APPEND.md`. **(3)** The bundled `sf-agentscript` and `sf-browser` Pi skills are retired into extension-owned `AGENT_GUIDE.md` files. **Date each by bisecting `git log` on `CHANGELOG.md`, then write up (1)** — it breaks the publish flow of the platform's default authoring model. _(Raised 2026-08-11.)_
- **Two Summer '26 Data 360 features have titles and nothing else** — *Currency Reporting* and *Result Reuse for Data 360 Live*. No technical detail is obtainable because `help.salesforce.com` is unreadable to automated fetching. **Open the release notes in a browser and settle both.** _(Raised 2026-08-01.)_
- **What exists in which regulated environment, and who authorized IL5?** The Trust Layer's model roster is a property of the *environment*, not the org — Anthropic-supplied models had to be disabled to obtain IL5. **No matrix exists** for commercial vs Government Cloud vs Government Cloud Plus vs IL5 (GC Plus already drops Coworker, Vibes and ApexGuru/Scale Center). **No press release names the authorizing body, the date or an ATO package identifier**, so "IL5-authorized" is a company claim until a DISA listing confirms it. **Build the matrix from [compliance.salesforce.com](https://compliance.salesforce.com/) and find the DISA listing.** _(Raised 2026-08-06.)_
- **What else is in Winter '27?** The API version is settled — **68.0** ([entry](developer-tooling-and-apis.md#2026-08-12--winter-27-is-api-680-confirmed--and-it-brings-a-new-agent-runtime-metadata-pair-aiagentdefinition--aiagentdefinitionversion)). **Still open:** the full Release Update list, *Custom Lightning Type Bundles with Agentforce Vibes Skills*, two Data 360 titles with no surface (*select writeback operation types for Data 360 objects*, *assign data model object categories for Data 360 compatibility*), what **`AiAgentDefinitionPlanner`** is, and whether the four telephony-provider types are the Agentforce Voice provider surface. **Open Setup → Release Updates in a preview org after Aug 30 and enumerate what is actually queued.** _(Raised 2026-08-09.)_
- **Agentforce Operations has no first-party detail and no price.** GA **2026-04-29**, recorded [here](agentforce-platform.md#2026-04-29--agentforce-operations--the-fifth-prebuilt-agent-family-ga-for-102-days-and-never-recorded-here) entirely from search-result snippets. Unresolved: **what a digital blueprint is as an artifact** (metadata type? deployable? versioned?), whether the Flow integration ever left the May 2026 Beta, and **what it costs** — no SKU or Flex Credits mapping exists anywhere, which is the one cell keeping the buy-vs-build table open. _(Raised 2026-08-09.)_
- **"Agent Albert" has never been recorded here.** April 2026 coverage describes a Salesforce platform, code-named Agent Albert, that **observes end-user work and acts on the user's behalf**, targeted for a public unveil **by the end of 2026** and positioned as the successor step to Agentforce rather than a feature of it. Every source is secondary and 403-blocked — no first-party detail, no surface, no confirmed date. **Find a first-party source — a newsroom post, a Dreamforce '26 session, or an earnings-call transcript — before it turns up in someone's roadmap conversation.** _(Raised 2026-08-05.)_
- **Agentforce Coworker GA** — Beta since May 21, 2026 with **no announced GA date**, and no word on whether the pilot sources (Google Drive, SharePoint, Jira) reach Beta first. Also unconfirmed: the "later this year" ship dates for the Teams, ChatGPT, Claude and desktop surfaces. Re-check before it goes near a delivery commitment.
- **Context Indexing GA** — reported in June 2026 as expected "later in July 2026", but no confirmation found as of 2026-07-28. Status open; re-check against the monthly Data 360 release notes.
- **Agent Broker's real status** — launch coverage puts it **GA October 2025**; coverage of the April 2026 Agent Fabric expansion describes a **Beta from April 2026**. Likely reconciliation: base Broker GA, guided determinism in Beta — but that's inference. Also unresolved: what Agent Fabric costs and which MuleSoft entitlement it needs. **No public pricing found.**
- **The official Agentforce Specialist domain weights.** **Narrowed 2026-08-15:** third-party guides now converge on **AI Agents 35% · Prompt Engineering 20% · Data Cloud for Agentforce 20% · Development Lifecycle 20% · Multi-Agent Interoperability 5%** — so the 15% MAI claim looks dead and the ~5% recorded here holds, but **a Development Lifecycle domain exists at 20%** where the radar recorded none. Every source is still secondary and the official PDF is unread, so this stays open. **Actionable now: raise Development Lifecycle in the study plan; do not raise Multi-Agent Interoperability.**
- **Agent Script in the Agentforce Specialist exam** — it became the default authoring model in July 2026 but isn't named in the exam guide. Assume implicit scope; re-check before booking.
- **Exact Agentforce Builder / Agent Script GA date** — no first-party announcement located; secondary sources conflict between February 2026 and the Summer '26 cadence. The July 13, 2026 legacy-builder cutoff is confirmed.
- **`salesforce-datacloud-connector` GA** — the Python Data 360 client v2 has been at **2.0.0b1 beta since June 2, 2026** with no announced GA date, while **v1 (`salesforce-cdp-connector`) is deprecated with removal tied to that GA**. Re-check before writing either into anything long-lived.
- **Fin acquisition** — Salesforce signed a definitive agreement to acquire Fin (announced June 15, 2026; expected to close Q4 FY27), an SMB-focused autonomous service agent platform used by 30,000+ companies. Watch how it lands relative to the Help Agent.

---

## Writing contract

The `Salesforce AI release radar` routine writes to this contract. It lives here rather than in the prompt so the rules travel with the repo. Where the prompt and this section disagree, **this section wins**.

### The signal gate — what gets written at all

Most scans find nothing in most areas. That is the normal case, and **it must not produce a file.**

| What the scan found | What gets written |
|---|---|
| An item clears the relevance bar | Topic-file entry **+** a dated note for that area **+** a `scan-log.md` cell |
| Nothing clears the bar | A `—` in that area's `scan-log.md` cell. **Nothing else.** Bump `watchlist.md` and move on |
| Fifth consecutive quiet scan for an area | No scan note. That area's budget goes to a **gap check**; record what was checked |

**Never create a file whose `## What changed` says that nothing changed.** A dated note with no routed item is not an audit record — `scan-log.md` is the audit record.

**An empty run is a valid run.** It still commits: the `scan-log.md` row and the `watchlist.md` diff are the log.

### Negatives are state, not prose

An artifact that has not changed gets its `Last checked` cell bumped in [watchlist.md](watchlist.md) and **is mentioned nowhere else**. `git log -p watchlist.md` is the audit trail.

A negative earns prose in exactly two cases:

- it **closes an open question**, or
- it **contradicts something already published here** — then it is a `> **Correction (YYYY-MM-DD):**` on the entry that was wrong.

`## Verified negatives` and `## Watched, not recorded` are **abolished as note sections**. An item worth watching gets a `watchlist.md` row **with a re-check date**. No date means it is not worth watching, and it goes nowhere.

### Version state is not news

A version number, dist-tag position, commit hash or idle-day count that **has not changed behaviour you can act on** is state. It belongs in `watchlist.md` and nowhere else. Do not write an entry, a paragraph, or a *State of play* sentence about a tag that did not move.

The failure this prevents: five scans narrated an unmoving `@salesforce/cli` `latest` tag as a *stall*, when the project had published its Wednesday cadence in its own release notes.

### The radar does not write about the radar

- **Corrections stay mandatory** — `> **Correction (YYYY-MM-DD):** <what this said before, what it is now>` on the entry itself. Never delete a superseded claim; supersede it visibly.
- **Method lessons go to [method-notes.md](method-notes.md)**, one line each, **max one per run**. A lesson already listed is not re-learned in prose.
- **Banned inside topic-file entries, dated notes and *State of play*:** the phrase *"this radar"*, *"Nth consecutive scan"*, and any sentence whose subject is the scanning process rather than Salesforce. [`scan-log.md`](scan-log.md) and [`method-notes.md`](method-notes.md) are the only two files where the process is legitimately the subject — quiet streaks are tracked there because they trigger a gap check, not because they are news.

### Routing — one canonical home per item

Write the full entry in exactly one topic file. Other topic files may carry a one-line cross-link, never a copy.

| Subject | Canonical file |
|---|---|
| Builder, Agent Script, orchestration, Voice, Contact Center, mobile SDK, observability, Coworker, prebuilt agents | [agentforce-platform.md](agentforce-platform.md) |
| Data 360 ingestion, modeling, grounding, SOQL, Code Extensions, connectors, zero-copy, semantic layer | [data-360.md](data-360.md) |
| MCP servers, Headless 360, Agent Fabric, ADLC, `sf` CLI, npm libraries, Apex/LWC, IDEs | [developer-tooling-and-apis.md](developer-tooling-and-apis.md) |
| Trust Layer, execution modes, sharing, auth retirements, secrets, Release Update enforcement | [trust-security-and-governance.md](trust-security-and-governance.md) |
| Flex Credits, pay-per-resolution, ELAs, certifications, acquisitions | [pricing-and-certification.md](pricing-and-certification.md) |
| Benchmarks, papers, open models, evaluation method, research-artifact licences | [ai-research-and-benchmarks.md](ai-research-and-benchmarks.md) |

**There are six topic files.** Every run reports the last-touched date of all six.

**Tie-breakers.** MCP servers route to `developer-tooling-and-apis.md` even when Data-360-specific — `data-360.md` gets the cross-link. A licence, price or exam-scope fact about a tool routes to `pricing-and-certification.md`; the tool itself stays in its own file. A **licence on a research artifact** stays in `ai-research-and-benchmarks.md`, because there the licence *is* the finding. A CVE-class fix in a Salesforce npm package or CLI routes to `developer-tooling-and-apis.md` — `trust-security-and-governance.md` gets the cross-link and the generalised governance point.

### Topic-file entry — the primary deliverable

```markdown
## YYYY-MM-DD · <Title — names the thing, no marketing verbs>

**What changed.** <the fact, ≤60 words>

- **<Bolded lead label>.** <detail>
- **<Bolded lead label>.** <detail>

**Relevant to:** Architect / Developer / Admin — <half a sentence on what it changes for each>

**Why it matters.** <2–4 sentences: the practitioner consequence, not a restatement of the fact.>

**Gotchas:**
- <the trap, with the exact identifier that triggers it>

**Study action:** <one concrete thing to do in a dev org, a repo or the CLI.>

**Status:** GA / Beta / Pilot / Developer Preview / Announced / Open source — plus the release and date.

**Sources:** [Title](url) · [Title](url)
```

Rules:

- **No paragraph over ~60 words.** Any inline enumeration — "four skills:", "Three concrete things", "(1)…(2)…(3)" — becomes a list.
- **`**Why it matters.**` is a fixed literal string.** Not "why it's worth your time", not "what it means practically". It has to stay greppable.
- **`**Relevant to:**` is mandatory** — it is the relevance gate's receipt. If you cannot fill it, the entry should not exist.
- **`**Study action:**` is mandatory on every entry.**
- **`**Gotchas:**` is mandatory when the item has an API, CLI, metadata type, permission set or config surface**, and identifiers must be exact. The bar is the Data Library entry: treat the library as ready when `retrieverId` goes non-null, not when `status` flips; `rag_feature_config_id` is `"ARFPC_" + libraryId`.
- **Mermaid diagrams belong here**, not in a scan log. Use one for a flow, a routing decision or a dependency graph.
- **A negative finding carries a timestamp.** "No commits since July 24" was true when checked on 07-28 and false hours later.

### Write discipline

- **New entry** → append at the top. Every topic file reads newest-first.
- **Status change to an existing entry** → mutate in place and prepend `> **Correction (YYYY-MM-DD):** <what this said before, what it is now>`.
- **Never bump an existing heading's date.** That is what put a 07-27 entry between two 07-26 entries in `agentforce-platform.md`.
- **Never delete a superseded claim** — supersede it visibly.
- Touching several topic files in one run is normal; commit once per run.

### Dated scan note — a pointer, not a write-up

Written **only for an area that routed at least one item this run.** Target **≤12 lines**: header, window, routed items. Nothing else.

```markdown
# <Area> — <Month D, YYYY>

**Window:** <UTC range> (24h / extended to 72h) · **Checked:** <sources> · **Not reachable:** <hosts>

## What changed

- **<Item>** → [agentforce-platform.md](../agentforce-platform.md#anchor) — <one line>
```

Every bullet resolves to a real anchor in a topic file.

### Size budget — checked before every commit

| File | Budget | If over |
|---|---|---|
| This README | **≤4,000 words** (`wc -w README.md`; it is **3,532** as of 2026-08-15) | Consolidate before committing — prune *Open questions* first |
| *State of play* | 5 numbered items + **one** additions paragraph ≤150 words | The previous additions paragraph is **replaced, not demoted to "Previous additions"** |
| *Open questions* | ≤60 words each; prune closed ones at the weekly pass | A question answered is deleted, not struck through and kept |
| Coverage and staleness | **One section**, the current run | Overwrite it. Never append a second |
| A dated scan note | ≤12 lines | Cut to the routed items |
| `method-notes.md` | One new line per run, max | If the lesson is already listed, write nothing |

The README grew from 15KB to 87KB in fourteen days — 2,020 words to 11,531 — purely by appending where it should have replaced. Every row above says *replace*. That is the fix; the word count is only the smoke alarm.

### Standing notes — do not restate these anywhere

- `salesforce.com`, `salesforceben.com`, `arxiv.org` and `huggingface.co` return **403** to automated fetching. Use search-result snippets and secondary coverage; a negative from these sources is weaker than one from GitHub.
- **Egress varies between runs and can be much narrower than 403s alone** — `EGRESS_BLOCKED` is a proxy refusal, not a site 403. When it happens, name the reachable sources in the note's `**Window:**` line and treat everything else as **unchecked, not absent**.
- An **org-wide OSPO CODEOWNERS sweep on 2026-07-29** makes many Salesforce repositories look freshly updated. Repository metadata is not code — check commits.
- The three `agentforce-*` skills ship from one internal source into two public repos at identical versions: `SalesforceAIResearch/agentforce-adlc` (**CC BY-NC 4.0**, blocks client work) and `forcedotcom/sf-skills` (**Apache-2.0**). The restriction attaches to the copy you took — prefer `sf-skills` for anything commercial.

### Feeding the study base

- New jargon defined in an entry → the right alphabetical section of [GLOSSARY.md](../GLOSSARY.md).
- Each scan that produces an entry adds strict `Q:` / `A:` pairs to the relevant `../02-salesforce-ai/NN-topic/flashcards.md`.
- An item big enough to be its own subject (a product or capability with its own surface, not a version bump) → next-numbered `NN-kebab-case` folder in [02-salesforce-ai](../02-salesforce-ai/INDEX.md) from `../_templates/`, update that INDEX, and link it from the radar entry with a `**Study folder:**` line.

### Coverage, staleness and the weekly pass

- **Every run** reports the last-touched date of all **six** topic files in the single Coverage table below, **overwriting** it. The table is the report — no essay, no "method finding", no "next to watch" prose.
- Anything untouched **>14 days** gets a gap check that run.
- An **area quiet for 5 consecutive scans** gets a gap check instead of a sixth identical scan.
- **Weekly (first run on or after Sunday):** rewrite *State of play*, prune resolved *Open questions*, refresh the `scan-log.md` streak table and the footer date, and reconcile any item that has landed in two topic files.

## Coverage and staleness — 2026-08-15

| Topic file | Last touched | Age | This run |
|---|---|---|---|
| [developer-tooling-and-apis.md](developer-tooling-and-apis.md) | 2026-08-15 | 0d | ✅ two entries — `@salesforce/agents` 2.0.2, `sf-skills` 1.38.0 |
| [agentforce-platform.md](agentforce-platform.md) | 2026-08-15 | 0d | ✅ cross-link — the two preview clients and the two context-variable namespaces |
| [trust-security-and-governance.md](trust-security-and-governance.md) | 2026-08-15 | 0d | ✅ cross-link — declared prerequisites that read as AND; unrequested TraceFlags |
| [data-360.md](data-360.md) | 2026-08-12 | 3d | ❌ quiet. Gap check due at 5 consecutive quiet scans |
| [ai-research-and-benchmarks.md](ai-research-and-benchmarks.md) | 2026-08-07 | 8d | ❌ quiet for 6 consecutive scans — **gap check owed next run** |
| [pricing-and-certification.md](pricing-and-certification.md) | 2026-08-02 | **13d** | ❌ exam domain weights narrowed, no Agentforce Operations SKU found; every source secondary. **Compulsory 2026-08-16** |

---

_Last updated: 2026-08-15 · Sources are linked inline in each topic file._
