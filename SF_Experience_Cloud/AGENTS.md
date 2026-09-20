# SF_Experience_Cloud — how to write in this vault

Style rules: [../AGENTS.md](../AGENTS.md). Full contract: [../NOTES-SYSTEM.md](../NOTES-SYSTEM.md).

## Scope

Experience Cloud only. LWR and Aura sites, Experience Builder, branding and themes, guest users, external licences and sharing, site auth and SSO, CMS, headless sites, site performance and SEO, Mobile Publisher, site DevOps, site limits and monitoring.

**The routing test:** *is this sentence still true with no Experience Cloud site in it?*

- **Yes** → it belongs in [../SF_core/](../SF_core/README.md). Write it there and link both ways.
- **No** → it belongs here.

So OWD, sharing rules and the grantee model are `SF_core/07-security-and-sharing/`. *What a guest user sharing rule may grant* stays here. `NavigationMixin` and the page reference vocabulary are `SF_core/03-lwc-and-slds/`. *Which of them work in an LWR container* stays here.

**The two near neighbours.** An embedded **agent** is built in [../SF_Agentforce/](../SF_Agentforce/INDEX.md) — this vault owns only its site-side exposure, in [19](19-embedded-messaging-and-agents-in-sites.md) and as a line item on [11](11-public-site-exposure-audit.md). Site data feeding a segment is [../SF_Data_360/](../SF_Data_360/INDEX.md).

## Two note formats live here

- **The 20 notes written as SF_core area 05** (phases 18–19) keep the dense format below. Do not rewrite them wholesale.
- **New notes** use the light format in [../templates/note.md](../templates/note.md): 50 lines, bullets, `## Gaps to close`, `## Hands-on`. Filenames still take the next `NN-` prefix.
- **A fed topic that already has a note here** → enrich that note in place. Add the cross-link and a `## Gaps to close` section. Never create a second file for the same topic.

## The dense format

`## Core idea` → `## How it works` → `## 2026 currency` → `## Gotchas` → `## Recall` → `## Related`

- **Hard cap ~80 lines.** If it will not fit, the taxonomy is wrong — split the topic.
- **At most one table and one code block (≤15 lines)** in `## How it works`.
- **`## Recall` is 5 `Q:`/`A:` pairs**, kept strict so one Anki script works across the vault.
- **Delete `## 2026 currency`** when nothing has changed. An empty heading is noise.
- **Metadata is YAML frontmatter**, read by Obsidian as Properties. `status`, `gaps`, `org_checks` and `labs` are recomputed by `scripts/vault.py fix`; every other key is yours. See [NOTES-SYSTEM.md](../NOTES-SYSTEM.md).

## Rules

- **🆕 topic → research the release notes before writing. Never draft from recall.**
- **⚠️ topic → the one-line "What changed" correction comes first,** before `## Core idea`.
- **Currency: Summer '26 · API 67.0** — the currency ledger stays shared, in [../SF_core/CURRENCY.md](../SF_core/CURRENCY.md). Never duplicate currency detail; link to [../RELEASE-RADAR/](../RELEASE-RADAR/README.md).
- **Filenames keep their numbers.** Order is the learning path and [PHASES.md](PHASES.md) depends on it. Renumbering is expensive — append, never insert.
- **Closed gaps are deleted, not ticked.** Last one gone, remove the `## Gaps to close` heading too.
- **A question no public doc answers goes in `## Confirm in org`**, as a `- 🚩 ` bullet naming what to open. A sandbox to-do, not a gap.
- **`## Hands-on` holds 3–4 labs** on new notes, IDs `EC-<TOPIC>-NN`, each with a `Proves:` and a time box. **Ticked, never deleted.** Bias to labs that break something on purpose — mine `## Gotchas` for them. New lab → add its row to `PRACTICE.md` in the same edit, creating that file when the first lab lands.
- **A link that crosses vaults gets a link back**, added in the same edit — that means links into `SF_core/`. Same-vault links rely on Obsidian's Backlinks panel.
- **Unsure of a fact? Mark it 🚩.**

## Four live currency traps

- **"LWR is the default" is a strategy statement, not a Setup fact.** Only **Build Your Own (LWR)** and **Microsite (LWR)** are LWR. Customer Service, Partner Central, Customer Account Portal, Help Center and Build Your Own are **Aura, still creatable at 67.0, still receiving Summer '26 features, with no announced retirement date** → [01](01-template-choice-and-site-landscape.md).
- **LWR ≠ enhanced LWR.** Different metadata types, and the *Upgrade to Enhanced LWR Sites* Release Update **has not been enforced since Summer '25** → [02](02-lwr-architecture-and-build-model.md).
- **Experience Delivery went; SSR did not — and the vault's own overcorrection is the live trap now.** **Experience Delivery is discontinued as of Winter '27**; it was the Cloudflare-backed *hosting* tier, and republishing moves a site to standard LWR infrastructure. **Islands SSR remains a standard LWR capability**, on by default on Build Your Own (LWR) standard pages and gated per page by `lightning__ServerRenderable` on the theme layout. Flag both errors: *"just switch on Experience Delivery"* **and** *"LWR has no SSR"* → [02](02-lwr-architecture-and-build-model.md), [16](16-site-performance-caching-and-seo.md).
- **The March 2026 campaign was a configuration failure, not a platform vulnerability.** Salesforce's 7 March 2026 advisory is explicit. Equally flag the inverse — the 2020–21 controls presented as *sufficient* without the standing-audit point → [11](11-public-site-exposure-audit.md).

## Housekeeping

- **New topic** → next number, plus a row in [INDEX.md](INDEX.md) at the right point in the path.
- **New jargon** goes in [../GLOSSARY.md](../GLOSSARY.md). One glossary for all vaults.
- **Does not route cleanly?** One dated bullet in [_inbox.md](_inbox.md). Never let filing friction stop capture.
