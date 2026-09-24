# PRACTICE — SF_Sales

> The file you open when the goal is **do something**. Reading lives in [INDEX.md](INDEX.md).
>
> **Three rules.** One item under ▶ Next · max 3 in flight · every lab has a time box.
>
> If you catch yourself reading instead of running, you are in the wrong file.

**40 labs · ~13 h total.** Nothing here runs over 30 minutes. If one overruns it was too big — split it into `NNa` / `NNb` rather than letting it become the lab you never start.

Each lab's full wording lives in its own note, as a `- [ ]` line under `## Hands-on`. **Tick it there when it is done** — labs are ticked, not deleted, because work you actually did is a record. That tick is the whole record: [Done](#done) is rebuilt from it.

## A lab is not finished until you have written down what broke

That is the point of the **Done** table's last column. Copy the error string **verbatim** — not paraphrased, not summarised. In six months the notes will have been rewritten and the release will have moved, but an exact error string is still what you type into a search box. It is the part that keeps earning.

If a lab produced no failure at all, say so — `no failure; worked first time` is a real result and tells you the lab was too gentle.

## Order

The queue is **unblocked-first**, not INDEX order:

- **#1–19** need only a Developer Edition org and you. #7 creates the standard price book entry that #10–15 reuse.
- **#20–30** need a **second user** — someone to sit on a team, in a territory, or below you in a forecast. #24–27 also set the Account org-wide default to Private.
- **#31–34** need **Pipeline Inspection** in the org. Help lists it only for Enterprise, Performance and Unlimited, so answer the note's `## Confirm in org` question first and park these if a Developer Edition org lacks it.
- **#35–39** need something outside Salesforce: a Google **reCAPTCHA v2** key pair, then a **Gmail or Microsoft 365** test mailbox.
- **#40** needs a **spare org**, because multiple currencies can't be turned off.

That split is deliberate. Nothing in the first 19 needs a licence a Developer Edition org may lack. Pipeline Inspection and Einstein Activity Capture come last because whether a Developer Edition org has them is itself an open question.

---

## ▶ Next

**SLS-LEAD-01 · 20 min · [Lead Management & Conversion](lead-management-and-conversion.md)**

Add a Lead validation rule that requires `Industry`, leave **Require Validation for Converted Leads** off, and convert a lead with no Industry. Then tick the setting and convert another. It proves the rule gates conversion only with the setting on, and it is the quickest way to feel how conversion bypasses what a normal save enforces.

---

## In flight — max 3

| Lab | Box | Started | Blocked on |
|---|---|---|---|
| — | — | — | — |

---

## Queue

| # | Lab | Topic | Box | Proves | Needs |
|---|---|---|---|---|---|
| 1 | SLS-LEAD-01 | [Leads](lead-management-and-conversion.md) | 20 min | Lead validation gates conversion only when the setting is on | nothing |
| 2 | SLS-LEAD-03 | [Leads](lead-management-and-conversion.md) | 20 min | An unmapped custom lead field is dropped silently | nothing |
| 3 | SLS-LEAD-04 | [Leads](lead-management-and-conversion.md) | 15 min | Converting into an existing contact fills blanks only | nothing |
| 4 | SLS-OPP-01 | [Opportunities & Path](opportunities-sales-process-and-path.md) | 15 min | Whether an API close resets a future Close Date | nothing |
| 5 | SLS-OPP-03 | [Opportunities & Path](opportunities-sales-process-and-path.md) | 25 min | The record type limits Stage and Path to one sales process | nothing |
| 6 | SLS-OPP-04 | [Opportunities & Path](opportunities-sales-process-and-path.md) | 15 min | Only four fixed fields write stage history | nothing |
| 7 | SLS-PROD-01 | [Products & Price Books](products-and-price-books.md) | 15 min | No standard price, no custom price | nothing |
| 8 | SLS-PROD-03 | [Products & Price Books](products-and-price-books.md) | 20 min | A scheduled line's `Quantity` update is ignored, not rejected | nothing |
| 9 | SLS-PROD-04 | [Products & Price Books](products-and-price-books.md) | 15 min | Apex tests need the standard entry too | nothing |
| 10 | SLS-OPP-02 | [Opportunities & Path](opportunities-sales-process-and-path.md) | 20 min | `Amount` ignores the API once products exist | needs #7 |
| 11 | SLS-PROD-02 | [Products & Price Books](products-and-price-books.md) | 20 min | The price book can't change under existing lines | a second custom price book · needs #7 |
| 12 | SLS-QUOTE-01 | [Quotes, Orders & Contracts](quotes-orders-and-contracts.md) | 20 min | One synced quote; syncing another replaces the lines | Quotes enabled · needs #7 |
| 13 | SLS-QUOTE-02 | [Quotes, Orders & Contracts](quotes-orders-and-contracts.md) | 15 min | An inactive product blocks sync | needs #12 |
| 14 | SLS-QUOTE-03 | [Quotes, Orders & Contracts](quotes-orders-and-contracts.md) | 25 min | An inactive contract blocks order activation | Orders enabled · needs #7 |
| 15 | SLS-QUOTE-04 | [Quotes, Orders & Contracts](quotes-orders-and-contracts.md) | 20 min | Reduction orders are Classic-only and block deactivation | needs #14 |
| 16 | SLS-CAMP-02 | [Campaigns](campaigns-and-campaign-influence.md) | 20 min | Hierarchy rollups include children; a parent's own fields don't | nothing |
| 17 | SLS-CAMP-03 | [Campaigns](campaigns-and-campaign-influence.md) | 25 min | No contact role, no influence | nothing |
| 18 | SLS-CAMP-04 | [Campaigns](campaigns-and-campaign-influence.md) | 20 min | The Primary Campaign Source model is system-owned | needs #17 |
| 19 | SLS-TEAM-01 | [Teams](account-and-opportunity-teams.md) | 15 min | One role list serves both team types | nothing |
| 20 | SLS-CAMP-01 | [Campaigns](campaigns-and-campaign-influence.md) | 15 min | What the Marketing User checkbox actually gates | second user |
| 21 | SLS-TEAM-02 | [Teams](account-and-opportunity-teams.md) | 20 min | Revenue splits must total 100%; overlay splits need not | second user |
| 22 | SLS-TEAM-03 | [Teams](account-and-opportunity-teams.md) | 20 min | A hidden split from an inactive type still blocks removal | second user · needs #21 |
| 23 | SLS-TEAM-04 | [Teams](account-and-opportunity-teams.md) | 15 min | A default team isn't added on transfer | second user |
| 24 | SLS-ETM-01 | [Territories](enterprise-territory-management.md) | 30 min | A Planning model previews assignments but grants nothing | second user, Account OWD Private |
| 25 | SLS-ETM-02 | [Territories](enterprise-territory-management.md) | 15 min | Rules run on save only when asked | needs #24 |
| 26 | SLS-ETM-03 | [Territories](enterprise-territory-management.md) | 30 min | A type-priority tie leaves `Territory2Id` blank | DX project · needs #25 |
| 27 | SLS-ETM-04 | [Territories](enterprise-territory-management.md) | 20 min | Four models in Developer Edition, and archiving is final | needs #26 |
| 28 | SLS-FCST-01 | [Forecasts](collaborative-forecasts.md) | 20 min | A role alone isn't a forecast manager | second user |
| 29 | SLS-FCST-02 | [Forecasts](collaborative-forecasts.md) | 15 min | Switching the rollup method deletes adjustments | needs #28 |
| 30 | SLS-FCST-03 | [Forecasts](collaborative-forecasts.md) | 15 min | Nobody sets their own quota | Manage Quotas · needs #28 |
| 31 | SLS-PIPE-01 | [Pipeline Inspection](pipeline-inspection.md) | 15 min | Moved Out and Increased catch the change | Pipeline Inspection in the org |
| 32 | SLS-PIPE-03 | [Pipeline Inspection](pipeline-inspection.md) | 15 min | Two rollup settings give two Best Case numbers | needs #28, #31 |
| 33 | SLS-PIPE-04 | [Pipeline Inspection](pipeline-inspection.md) | 10 min | The flow chart is gated by Revenue Intelligence | needs #31 |
| 34 | SLS-PIPE-02 | [Pipeline Inspection](pipeline-inspection.md) | 15 min | Access comes from the permission set | a spare user licence · needs #31 |
| 35 | SLS-LEAD-02 | [Leads](lead-management-and-conversion.md) | 25 min | reCAPTCHA rejects a stripped form post | reCAPTCHA v2 key pair |
| 36 | SLS-EAC-01 | [Activity Capture](einstein-activity-capture.md) | 25 min | Captured email is a real `EmailMessage` row — or the org is on legacy storage | Gmail or Microsoft 365 test mailbox |
| 37 | SLS-EAC-02 | [Activity Capture](einstein-activity-capture.md) | 15 min | No configuration, no capture | needs #36 |
| 38 | SLS-EAC-03 | [Activity Capture](einstein-activity-capture.md) | 15 min | An exclusion keeps mail out of both stores | needs #36 |
| 39 | SLS-EAC-04 | [Activity Capture](einstein-activity-capture.md) | 20 min | Header-only capture keeps no subject or body | needs #36 |
| 40 | SLS-FCST-04 | [Forecasts](collaborative-forecasts.md) | 25 min | Forecasts ignore dated exchange rates | a spare Developer Edition org — multi-currency is permanent |

---

## Done

**Generated from the ticked labs — do not add rows by hand.** Tick `- [x]` in the
note and run `python scripts/vault.py fix`; the row appears here. The `What broke`
cell is yours: fill it in and it is preserved on every rebuild.

| Lab | Date | What broke — verbatim |
|---|---|---|
| — | — | — |

---

## Parked

Nothing yet. Park a lab here rather than leaving it in the queue when it is blocked on something outside your control — a licence, a Beta, a region restriction — and say what would unblock it.
