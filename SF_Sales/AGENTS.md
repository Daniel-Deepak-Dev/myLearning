# SF_Sales — how to write in this vault

Style rules: [../AGENTS.md](../AGENTS.md). Full contract: [../NOTES-SYSTEM.md](../NOTES-SYSTEM.md).

## Scope

Sales Cloud only. Leads and lead conversion, opportunities, sales processes and Path, products and price books, quotes, orders and contracts, account and opportunity teams, Opportunity Splits, Enterprise Territory Management, Collaborative Forecasts, campaigns and campaign influence, Pipeline Inspection, Einstein Activity Capture, Sales Engagement, CPQ and Revenue Cloud.

**The routing test:** *is this sentence still true with no Sales Cloud in it?*

- **Yes** → it belongs in [../SF_core/](../SF_core/README.md). Write it there and link both ways.
- **No** → it belongs here.

So assignment rules, record types and business processes, the share rows teams add, and the Lead → Opportunity → PricebookEntry object graph go to `SF_core/`. *How lead conversion maps fields* and *how a forecast rolls up* stay here.

**The seam that matters most.** [SF_core · 07-security · 10](../SF_core/07-security-and-sharing/10-teams-territories-and-account-sharing.md) owns the **sharing** side of teams and territories: `RowCause = Team`, share-row growth, the territory hierarchy as a second path up. This vault owns the **selling** side: team roles, splits, territory types, assignment and forecasts. It was extracted, not moved, on 2026-09-24.

**Four neighbours.**

- A **Sales agent** that nurtures leads or coaches a rep is built in [../SF_Agentforce/](../SF_Agentforce/INDEX.md). This vault owns the lead and opportunity records it works and the sales process it coaches against.
- A **partner site** splits. The partner licence, external sharing and the site are [../SF_Experience_Cloud/](../SF_Experience_Cloud/INDEX.md) · 08. The lead and opportunity process partners work in stays here.
- **Leads routed by Omni-Channel** split. *How Omni-Channel pushes a lead to a rep* is [../SF_Service/](../SF_Service/INDEX.md). Lead statuses, assignment and conversion stay here.
- **Multi-currency and dated rates** are a platform setting in `SF_core/08-data-modeling-and-large-data-volumes/`. *Which Sales features ignore dated rates* stays here.

## The note format

Template: [../templates/note.md](../templates/note.md).

`## Key points` → `## Gotchas` → `## Gaps to close` → `## Confirm in org` → `## Hands-on` → `## Related`

- **50 lines max, counted to `## Related`.** The `## Related` / `## Sources` / `## History` footer does not count. No paragraph longer than two sentences.
- **One table max. One code block max, 12 lines.**
- **Metadata is YAML frontmatter**, read by Obsidian as Properties. `status`, `gaps`, `org_checks` and `labs` are recomputed by `scripts/vault.py fix`; every other key is yours. See [NOTES-SYSTEM.md](../NOTES-SYSTEM.md).
- **Filenames carry no number.** Order lives in [INDEX.md](INDEX.md).

## Rules

- **Closed gaps are deleted, not ticked.** Answer one, remove the line. Last one gone, remove the `## Gaps to close` heading too.
- **A question no public doc answers goes in `## Confirm in org`**, as a `- 🚩 ` bullet naming what to open. It is a sandbox to-do, not a gap.
- **`## Hands-on` holds 3–4 labs**, IDs `SLS-<TOPIC>-NN`, one line each, every one carrying a `Proves:`. **Ticked, never deleted.** Bias to labs that break something on purpose — mine `## Gotchas` for them. **A new lab needs a queue row in [PRACTICE.md](PRACTICE.md), added by hand** and placed unblocked-first; `check` reports a missing row but nothing writes it.
- **Status is derived, never typed.** `python scripts/vault.py fix` counts the `- [ ]` lines in `## Gaps to close` and writes `status: open` + `gaps: N`, or `status: complete`. `## Confirm in org` bullets and `## Hands-on` labs never count.
- **`created` never changes. `updated` changes on every edit.** Staleness is derived from `updated`, not stamped into the note — `HOME.md` lists what has gone 3+ months.
- **Every researched fact gets a `## Sources` line** with the date read. Salesforce domains trusted; anything else carries 🚩.
- **`## History`** takes one dated line per feed, saying what was added or changed — never a gap tally.
- **`Level` sets the gap ceiling.** Gaps may go one level up, never two. A `basic` note never gets a `deep` gap.
- **Gaps stay on this topic.** Never a syllabus. Never another subject.
- **Keep the user's own wording** in a `> **From my notes.**` callout. Correct it inline if it is wrong.
- **A link that crosses vaults gets a link back**, added in the same edit — that means links into `SF_core/`, `SF_Agentforce/`, `SF_Experience_Cloud/` and `SF_Service/`. Same-vault links rely on Obsidian's Backlinks panel.
- **Unsure of a fact? Mark it 🚩.** There is no Sales Cloud radar file. For release-dependent facts, check [../SF_core/CURRENCY.md](../SF_core/CURRENCY.md) and [../RELEASE-RADAR/pricing-and-certification.md](../RELEASE-RADAR/pricing-and-certification.md) first. Never draft release facts from recall.

## Four live currency traps

- **Sales Cloud is now called Agentforce Sales.** Help release notes read *"Sales Cloud is now Agentforce Sales. You may see references to Sales Cloud in the application and documentation"*, and the v68.0 Object Reference writes *"Agentforce Sales (formerly Sales Cloud)"*. The consultant cert followed on 24 July 2026. This vault keeps writing **Sales Cloud** on purpose, because *Agentforce Sales* collides with the *Agentforce for Sales* add-on and with the Sales agents built in `SF_Agentforce/`. Know both names.
- **Two features were renamed, and their API names were not.** Collaborative Forecasts is **Pipeline Forecasting** since Spring '25; the objects are still `Forecasting*` → [collaborative-forecasts.md](collaborative-forecasts.md). Enterprise Territory Management is **Sales Territories** since Summer '24; the objects are still `Territory2*` → [enterprise-territory-management.md](enterprise-territory-management.md). The notes keep the old names in their titles and mention the new ones, so a search for either finds them.
- **Their predecessors are retired, not legacy.** Customizable Forecasting retired in Summer '20 and original Territory Management in Summer '21, whose data is no longer reachable by UI or API. Flag any answer built on `Territory` or `UserTerritory` without the `2`.
- **Einstein Activity Capture email is no longer off-platform by default.** Setups since Summer '25 store `Task` and `EmailMessage` records. The legacy reports retire in Spring '27, and Microsoft 365 connections set up before Spring '26 must move to Microsoft Graph by **1 October 2026** → [einstein-activity-capture.md](einstein-activity-capture.md).

**Also moving, not yet traps:** Salesforce CPQ is end of sale, not end of life, and Revenue Cloud Advanced is its successor. Lightning Sync retires on 1 April 2027 and Salesforce for Outlook on 1 December 2027.

## Housekeeping

- **New topic** → new file, plus a row in [INDEX.md](INDEX.md) at the right point in the path.
- **New jargon** goes in [../GLOSSARY.md](../GLOSSARY.md), in the `## Sales Cloud` section. One glossary for all vaults.
- **Does not route cleanly?** One dated bullet in [_inbox.md](_inbox.md). Never let filing friction stop capture.
