# PRACTICE — SF_Experience_Cloud

> The file you open when the goal is **do something**. Reading lives in [INDEX.md](INDEX.md).
>
> **Three rules.** One item under ▶ Next · max 3 in flight · every lab has a time box.
>
> If you catch yourself reading instead of running, you are in the wrong file.

**20 labs · ~7.3 h total.** Nothing here runs over 45 minutes. If one overruns it was too big — split it into `NNa` / `NNb` rather than letting it become the lab you never start.

Each lab's full wording lives in its own note, as a `- [ ]` line under `## Hands-on`. **Tick it there when it is done** — labs are ticked, not deleted, because work you actually did is a record. That tick is the whole record: [Done](#done) is rebuilt from it.

## A lab is not finished until you have written down what broke

That is the point of the **Done** table's last column. Copy the error string **verbatim** — not paraphrased, not summarised. In six months the notes will have been rewritten and the release will have moved, but an exact error string is still what you type into a search box. It is the part that keeps earning.

If a lab produced no failure at all, say so — `no failure; worked first time` is a real result and tells you the lab was too gentle.

## Order

The queue is **unblocked-first**, not INDEX order:

- **#1–3** need one Build Your Own (LWR) site you can publish. **#3** also wants a custom LWC you are willing to deploy badly on purpose.
- **#4** is the only one needing a **second org**.
- **#5–8** need that same site **published and reachable as a guest**, because the accessibility obligation attaches to the public surface. **#6** wants a branding set you are willing to wreck, **#7** a custom theme layout, **#8** a custom LWC and a screen reader (NVDA or VoiceOver — both are free).
- **#9–11** reuse the same site and need nothing else — the security level is a site setting.
- **#12–15** need a **Customer Service (Aura)** site on Lightning Knowledge — topics are an Aura feature. **#14–15** also want a customer user.
- **#16** needs the Trailhead project org, with Enhanced Chat already on its site.
- **#17–20** need an **Enhanced Chat channel with a queue and a rep** — build it first with SF_Service's [SVC-CHSET-01](../SF_Service/PRACTICE.md) — plus a Build Your Own (LWR) site you can publish. #20 also switches the site's CSP level, so run it after #9.

This vault's twenty phase-18/19 notes carry no labs — they were written in the dense format, before the `## Hands-on` contract existed. The queue starts here and grows as topics are fed.

---

## ▶ Next

**EC-I18N-01 · 25 min · [Multilingual Sites & Site Translation](21-multilingual-sites-and-translation.md)**

Add a second language, place the Language Selector, translate one component inline, publish, then switch language. Everything else in this queue assumes you have seen a half-translated page once.

---

## In flight — max 3

| Lab | Box | Started | Blocked on |
|---|---|---|---|
| — | — | — | — |

---

## Queue

| # | Lab | Topic | Box | Proves | Needs |
|---|---|---|---|---|---|
| 1 | EC-I18N-01 | [Multilingual sites](21-multilingual-sites-and-translation.md) | 25 min | Enabling a language translates nothing | — |
| 2 | EC-I18N-02 | [Multilingual sites](21-multilingual-sites-and-translation.md) | 20 min | The import overwrites the default you edited | needs #1 |
| 3 | EC-I18N-03 | [Multilingual sites](21-multilingual-sites-and-translation.md) | 20 min | A literal in an LWC is monolingual forever | custom LWC |
| 4 | EC-I18N-04 | [Multilingual sites](21-multilingual-sites-and-translation.md) | 30 min | Which half of a translation actually travels | 2nd org |
| 5 | EC-A11Y-01 | [Accessibility](22-site-accessibility-and-conformance.md) | 30 min | The tools pass a page the keyboard fails | — |
| 6 | EC-A11Y-02 | [Accessibility](22-site-accessibility-and-conformance.md) | 20 min | Contrast is a branding-set value, and dark mode moves it | — |
| 7 | EC-A11Y-03 | [Accessibility](22-site-accessibility-and-conformance.md) | 25 min | Whether F6 regions vanish with the theme layout | — |
| 8 | EC-A11Y-04 | [Accessibility](22-site-accessibility-and-conformance.md) | 25 min | IDREF ARIA dies at the shadow boundary | custom LWC · screen reader |
| 9 | EC-CSP-01 | [Site CSP](24-site-csp-security-level-and-trusted-scripts.md) | 20 min | Strict blocks inline script; Relaxed runs it | — |
| 10 | EC-CSP-02 | [Site CSP](24-site-csp-security-level-and-trusted-scripts.md) | 20 min | A Trusted URL cannot carry a script | — |
| 11 | EC-CSP-04 | [Site CSP](24-site-csp-security-level-and-trusted-scripts.md) | 15 min | Script entries survive the level switch | needs #10 |
| 12 | EC-TOPIC-01 | [Topics & Knowledge](23-topics-and-knowledge-on-sites.md) | 30 min | Navigational menu versus featured tiles | Customer Service (Aura) site |
| 13 | EC-TOPIC-04 | [Topics & Knowledge](23-topics-and-knowledge-on-sites.md) | 15 min | Site topic tools without the platform switch | needs #12 |
| 14 | EC-TOPIC-02 | [Topics & Knowledge](23-topics-and-knowledge-on-sites.md) | 15 min | The channel, not the topic, gates articles | customer user · needs #12 |
| 15 | EC-TOPIC-03 | [Topics & Knowledge](23-topics-and-knowledge-on-sites.md) | 20 min | Where an untopicked article disappears | customer user · needs #12 |
| 16 | EC-CSP-03 | [Site CSP](24-site-csp-security-level-and-trusted-scripts.md) | 20 min | Which directives the chat's `scrt2URL` needs | the Knowledge & Enhanced Chat project org |
| 17 | EC-CHAT-01 | [Chat on a site](25-enhanced-chat-on-a-site-step-by-step.md) | 30 min | The site side is five steps | Enhanced Chat channel · rep |
| 18 | EC-CHAT-02 | [Chat on a site](25-enhanced-chat-on-a-site-step-by-step.md) | 20 min | Which publish each change needs | needs #17 |
| 19 | EC-CHAT-03 | [Chat on a site](25-enhanced-chat-on-a-site-step-by-step.md) | 15 min | What a domain mismatch looks like | needs #17 |
| 20 | EC-CHAT-04 | [Chat on a site](25-enhanced-chat-on-a-site-step-by-step.md) | 20 min | Site code needs Relaxed CSP | needs #17 · after #9 |

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
