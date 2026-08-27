# PRACTICE — the only file you open when the goal is *do something*

> **Three rules.** One item under ▶ Next. Max 3 in flight. Every unit has a time box.
>
> If you catch yourself reading instead of running, you are in the wrong file. That one is
> [05-release-radar/](05-release-radar/README.md) — and it is the **last** step of the week,
> not the first. See [STUDY-PLAN.md](STUDY-PLAN.md#weekly-rhythm).

Both dev orgs exist. Nothing here is blocked on access, and nothing here needs setting up first.

**No aliases.** Every command in every runbook targets whatever org is currently default, so there
is nothing to fill in before you start. One habit replaces the setup:

```bash
sf org display        # first command of every session — confirm you are in the org you think
```

Run it before you touch anything. The ladders are sequential by design — one at a time — so
switching org means `sf org login web --set-default`, or `sf config set target-org=<username>` for
an org you have already authorised. `sf org list` shows what you have.

> The one failure mode worth knowing: a wrong default silently sends an Agentforce lab into the
> Data 360 org. It deploys, it works, and it pollutes the tenant you were measuring in `lab-00`.
> `sf org display` costs two seconds and is the whole mitigation.

---

## ▶ Next

**[ag-00 — Agentforce tenant baseline](02-salesforce-ai/_labs/ag-00-tenant-baseline.md) · 20 min**

Write down what your Agentforce DE actually has enabled, which model is the org default, and
the starting credit balance. Nothing further up the ladder is *measurable* until those three
numbers exist on paper.

---

## In flight — max 3

| Lab | Box | Started | Blocked on |
|---|---|---|---|
| — | — | — | — |

---

## Queue

In order. Do not reorder to skip the hard one — the ladders are dependency-ordered.

### Agentforce ladder · [_labs/README.md](02-salesforce-ai/_labs/README.md)

| # | Lab | Box | Proves |
|---|---|---|---|
| 00 | [Tenant baseline](02-salesforce-ai/_labs/ag-00-tenant-baseline.md) | 20 min | What you have; the numbers everything is measured against |
| 01 | [First agent + read the trace](02-salesforce-ai/_labs/ag-01-first-agent-and-trace.md) | 30 min | The whole loop once, end to end, smallest possible |
| 02 | [Agent Script from the CLI](02-salesforce-ai/_labs/ag-02-agent-script-from-cli.md) | 45 min | generate → edit → deploy → preview. Real syntax, in your hands |
| 03 | Grounded prompt template | 40 min | Grounding narrows; test with the record that breaks it |
| 04 | Custom Apex action | 40 min | The no-arg-constructor failure, caused on purpose |
| 05 | The description experiment | 30 min | Descriptions **are** the interface — mis-select, then fix |
| 06 | Subagent routing | 40 min | Deliberate mis-route, then `does NOT handle` clauses |
| 07 | Agent tests + a Custom Scorer | 45 min | Evaluation as deployable metadata |
| 08 | Trust Layer audit trail | 30 min | Fire the injection; find the masking |
| 09 | ADL Connect data library | 45 min | Poll `status` and watch it lie; switch to `retrieverId` |

### Data 360 ladder · [labs/README.md](01-data-cloud/10-lab-environment/labs/README.md)

Nine runbooks, already written, all `⬜`. Start at `lab-00` **after** ag-02 — one ladder at a
time, or neither gets finished.

### From the radar — study actions worth doing

Seeded from `**Study action:**` lines. These are the ones with a live org surface:

- [ ] Preview a published agent with `sf agent preview --api-name <ApiName>`, confirm a
  reasoning trace is emitted, then `npm ls @salesforce/agents` and check the resolved version
  is ≥ 2.0.4. Repeat via `--authoring-bundle` and **diff the two transcripts** — they
  initialise differently, and `--api-name` used to silently drop context variables.
  → [developer-tooling-and-apis.md](05-release-radar/developer-tooling-and-apis.md)
- [ ] Clone `salesforce/agentscript` at `5e6404e`, copy the `AUTONOMOUS_AE` fixture out of
  `dialect/agentscript/src/tests/agentiq-complete-example.test.ts` into a `.agent` file, delete
  the `agent_type` line and re-lint. The five `gba-only-*` errors are the exact boundary
  between the conversational and goal-based topologies.
  → [agentforce-platform.md](05-release-radar/agentforce-platform.md)
- [ ] Compile `packages/compiler/test/fixtures/scripts/voice_v2_all.agent` and diff the emitted
  `voice_v2_all.snake.json` against `voice_v1_all`. Then paste an `inbound_keywords:` line into
  the v2 fixture and confirm the version-mixing compile error.

---

## Done — newest first

Format: `YYYY-MM-DD · lab · what broke`. The third column is the point. An entry with nothing
in it means the lab was followed rather than run.

| Date | Lab | What broke |
|---|---|---|
| — | — | — |
