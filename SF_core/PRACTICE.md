# PRACTICE — SF_core

> The file you open when the goal is **do something**. Reading lives in [README.md](README.md).
>
> **Three rules.** One item under ▶ Next · max 3 in flight · every lab has a time box.
>
> If you catch yourself reading instead of running, you are in the wrong file.

**15 labs · ~4 h total.** Nothing here runs over 45 minutes. If one overruns it was too big — split it into `NNa` / `NNb` rather than letting it become the lab you never start.

Each lab's full wording lives in its own note, as a `- [ ]` line under `## Hands-on`. **Tick it there when it is done** — labs are ticked, not deleted, because work you actually did is a record. That tick is the whole record: [Done](#done) is rebuilt from it.

## A lab is not finished until you have written down what broke

That is the point of the **Done** table's last column. Copy the error string **verbatim** — not paraphrased, not summarised. In six months the notes will have been rewritten and the release will have moved, but an exact error string is still what you type into a search box. It is the part that keeps earning.

If a lab produced no failure at all, say so — `no failure; worked first time` is a real result and tells you the lab was too gentle.

## Order

Most of `SF_core` is dense-format notes written before `## Hands-on` existed, so this queue is short and will stay short until those notes are refed. It is not a measure of the area.

The queue is **unblocked-first**:

- **#1–3** need only **Prompt Builder** and a flow — no Agentforce licence, no Data 360, no second org.
- **#4–10** need nothing beyond a Developer Edition org. #7 wants a test user.
- **#11–13** need a local static server and an access token — CORS only exists in a browser, so curl cannot test it.
- **#14** needs an Experience Builder site; **#15** the Trailhead project org with Enhanced Chat on its site.

---

## ▶ Next

**SF-PTFLOW-01 · 20 min · [04-flow · 28 Calling a prompt template from Flow](04-flow-and-automation/28-calling-prompt-templates-from-flow.md)**

Activate a Flex template, then call it from a screen flow and display the generation on a screen. The other two assume you have done this once.

---

## In flight — max 3

| Lab | Box | Started | Blocked on |
|---|---|---|---|
| — | — | — | — |

---

## Queue

| # | Lab | Topic | Box | Proves | Needs |
|---|---|---|---|---|---|
| 1 | SF-PTFLOW-01 | [Prompt templates from Flow](04-flow-and-automation/28-calling-prompt-templates-from-flow.md) | 20 min | Activation alone publishes the action | — |
| 2 | SF-PTFLOW-02 | [Prompt templates from Flow](04-flow-and-automation/28-calling-prompt-templates-from-flow.md) | 15 min | The dependency is a string, not a reference | — |
| 3 | SF-PTFLOW-03 | [Prompt templates from Flow](04-flow-and-automation/28-calling-prompt-templates-from-flow.md) | 20 min | Two features that share a noun | — |
| 4 | SF-TOPIC-01 | [01-admin · 20 Topics for Objects](01-admin-and-declarative-platform/20-topics-for-objects.md) | 20 min | Selected fields feed topic suggestions | — |
| 5 | SF-TOPIC-03 | [01-admin · 20 Topics for Objects](01-admin-and-declarative-platform/20-topics-for-objects.md) | 10 min | Each tag is its own row | — |
| 6 | SF-TOPIC-04 | [01-admin · 20 Topics for Objects](01-admin-and-declarative-platform/20-topics-for-objects.md) | 15 min | What disabling does to existing tags | needs #4 |
| 7 | SF-TOPIC-02 | [01-admin · 20 Topics for Objects](01-admin-and-declarative-platform/20-topics-for-objects.md) | 15 min | Assign and Create Topics are separate | test user |
| 8 | SF-TURL-01 | [07-security · 27 Trusted URLs & CSP](07-security-and-sharing/27-trusted-urls-and-csp.md) | 25 min | The block is CSP; `connect-src` fixes it | — |
| 9 | SF-TURL-02 | [07-security · 27 Trusted URLs & CSP](07-security-and-sharing/27-trusted-urls-and-csp.md) | 15 min | No `script-src` route in Lightning | — |
| 10 | SF-TURL-03 | [07-security · 27 Trusted URLs & CSP](07-security-and-sharing/27-trusted-urls-and-csp.md) | 15 min | CSP Context is a real boundary | needs #8 |
| 11 | SF-CORS-01 | [06-integration · 28 CORS allowlist](06-integration-and-apis/28-cors-allowlist.md) | 20 min | An unlisted origin is blocked in the browser | local static server, access token |
| 12 | SF-CORS-02 | [06-integration · 28 CORS allowlist](06-integration-and-apis/28-cors-allowlist.md) | 10 min | The allowlist grants no access | needs #11 |
| 13 | SF-CORS-03 | [06-integration · 28 CORS allowlist](06-integration-and-apis/28-cors-allowlist.md) | 15 min | 403 or 404, and whether it is logged | event log file access · needs #11 |
| 14 | SF-TURL-04 | [07-security · 27 Trusted URLs & CSP](07-security-and-sharing/27-trusted-urls-and-csp.md) | 15 min | The violations list is Lightning-only | Experience Builder site · needs #8 |
| 15 | SF-CORS-04 | [06-integration · 28 CORS allowlist](06-integration-and-apis/28-cors-allowlist.md) | 20 min | Whether a site chat needs a CORS entry | the Knowledge & Enhanced Chat project org |

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
