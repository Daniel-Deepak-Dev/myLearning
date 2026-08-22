# The Agentforce Lab Ladder

Ten runbooks, in order. Each builds on the org state the previous one left behind — don't skip
ahead. The counterpart ladder for the data layer is
[01-data-cloud/10-lab-environment/labs/](../../01-data-cloud/10-lab-environment/labs/README.md);
this one assumes you can already get data into a tenant, or that you don't need to yet.

Every runbook has the same shape:

**Goal · Box · Prereqs · Steps · How you know it worked · Break it on purpose · What it does not prove · Notes from my run · Failure signature**

The last three are the ones that matter.

- *Break it on purpose* is where the learning is. A failure signature you have caused once is
  one you will recognise at a client.
- *Notes from my run* is yours to fill in. **Empty means the lab hasn't really been done.**
- *Failure signature* holds the **verbatim** error text or the exact wrong output — copied, not
  paraphrased. In six months this is the only section still earning its keep, because error
  strings are what you actually search for.

> **Box** is a time box, and it is a promise: no runbook here needs more than 45 minutes. If one
> overruns, it is too big — split it into `ag-NNa` / `ag-NNb` rather than letting it become the
> lab you never start.

## Environment

| Role | Org | Why |
|---|---|---|
| **Agentforce DE** | Developer Edition with Agentforce enabled | Everything here runs in one org. No second tenant needed. |
| **Local CLI** | `sf` (Node 22+), `@salesforce/agents` ≥ 2.0.4 | From `ag-02` onward the authoring loop is CLI-first. |

Data 360 is **not** a prerequisite until `ag-09`. That is deliberate — the two ladders were
coupled only by accident, and it is what made both of them feel like they needed a spare weekend.

## The ladder

| # | Lab | Teaches | Box | Status |
|---|---|---|---|---|
| 00 | [Tenant baseline](ag-00-tenant-baseline.md) | What is enabled, default model, credit balance | 20 min | ⬜ |
| 01 | [First agent + read the trace](ag-01-first-agent-and-trace.md) | The whole loop once, smallest possible | 30 min | ⬜ |
| 02 | [**Agent Script from the CLI**](ag-02-agent-script-from-cli.md) | generate → edit → deploy → preview; real syntax | 45 min | ⬜ |
| 03 | Grounded prompt template | Grounding narrows; the record that breaks it | 40 min | ⬜ |
| 04 | Custom Apex action | The no-arg-constructor failure, on purpose | 40 min | ⬜ |
| 05 | The description experiment | Descriptions *are* the interface | 30 min | ⬜ |
| 06 | Subagent routing | Mis-route, then `does NOT handle` clauses | 40 min | ⬜ |
| 07 | Agent tests + a Custom Scorer | Evaluation as deployable metadata | 45 min | ⬜ |
| 08 | Trust Layer audit trail | Fire the injection; find the masking | 30 min | ⬜ |
| 09 | ADL Connect data library | `status` lies; `retrieverId` doesn't | 45 min | ⬜ |
| 99 | Parked | Voice (US/CA only), Coworker (Beta), Agent Fabric | — | ⏸️ |

Mark ⬜ → ✅ as you go, and put the date in the runbook itself.

## Ground rules

1. **`sf org display` is the first command of every session.** No runbook here uses `--target-org`
   or an alias — every command hits the default org, so the default being right is the only setup
   this ladder has. Two seconds spent confirming it prevents the one silent failure that matters:
   an Agentforce lab deployed into the Data 360 org, which succeeds, works, and quietly pollutes
   the tenant `lab-00` was measuring.
2. **The org default model is a variable, not a constant.** Record it in `ag-00` and re-check it
   whenever output changes for no reason you can name. A silent default change looks exactly like
   a prompt regression.
3. **Every agent action costs credits.** A `for` loop over a Models API call has a line-item
   cost. Note the balance before and after anything that loops — `ag-00` exists for this.
4. **Read the trace, never the answer.** A plausible answer proves nothing; the trace shows which
   topic matched, which action fired, and what grounding was actually retrieved. Any lab whose
   verification is "the reply looked right" is not a lab.
5. **Never point an agent at the Geeksoft sandbox.** Same rule as the data ladder, same reason —
   see [Governance](../../01-data-cloud/10-lab-environment/notes.md#governance-the-client-sandbox-question).
6. **Log in every ~45 days** or the Developer Edition expires and takes the ladder with it.

## Why this ladder exists

The Data 360 track had nine runbooks and this track had none, while being the faster-moving of
the two. The exercises were not missing — they were already designed, scattered across the
`## Hands-on / labs` sections of fourteen notes as unchecked bullets with no order and no size.
`ag-04`, `ag-05` and `ag-06` in particular are lifted almost verbatim from
[05-custom-agent-actions](../05-custom-agent-actions/notes.md) and
[08-multi-agent-orchestration](../08-multi-agent-orchestration/notes.md), which had described
them well and never once sized them.
