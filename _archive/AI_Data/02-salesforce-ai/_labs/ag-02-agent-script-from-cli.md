# Lab ag-02 — Agent Script from the CLI

> Status: ⬜ not started · Box: **45 min** · Date run: —

## Goal

Own the authoring loop: **generate → edit → deploy → preview**, with a real `.agent` file open in
your editor. By the end you have a working Agent Script file *you* wrote, and a recorded snippet
of syntax you have personally compiled.

> **Read this once.** [07-agent-script/notes.md](../07-agent-script/notes.md) deliberately refuses
> to transcribe syntax, on the grounds that it changes faster than notes do. That is true, and it
> created a deadlock: the note withholds the syntax until you have run it, and you cannot run it
> without the syntax. This lab breaks the deadlock the honest way — **it never quotes syntax from
> memory.** Every construct below comes from one of two authoritative sources: a bundle the CLI
> generated for your org, or a compiler fixture in the open-source language repo. Both compile by
> definition. Neither can go stale without you noticing, because you regenerate them.

## Prereqs

- [ag-01](ag-01-first-agent-and-trace.md) done — you have a clicked agent and have read a trace.
- `sf` on Node 22+, `@salesforce/agents` ≥ 2.0.4 (checked in `ag-00`).
- An `sfdx-project.json` — any DX project directory will do. Create one if needed:
  `sf project generate --name agentforce-labs`.

## Steps

### Part A — get real syntax into your editor (15 min)

1. **Generate an authoring bundle from your existing agent.** This is the single most useful
   command in the ladder: it emits current, valid, org-specific Agent Script.
   ```bash
   sf agent generate authoring-bundle
   ```
   Find the `.agent` file it produced. **Open it.** This is the ground truth — not a doc, not a
   blog, not these notes.
2. **Retrieve the whole agent as metadata too**, so you can see both representations of the same
   thing:
   ```bash
   sf project retrieve start --root-type-with-dependencies Bot
   ```
   `--root-type-with-dependencies` takes exactly two values — `Bot` and
   `AiAgentDefinitionVersion` — and naming a `Bot` pulls its dependent `GenAiPlannerBundle`,
   `GenAiPlugin` and `GenAiFunction` with it. *(CLI availability: `nightly`-only as of
   2026-08-14 — if the flag is rejected, record that and use a manifest instead.)*
3. **Clone the language repo for the fixtures.** These are the compiler's own test inputs, so they
   are guaranteed-valid Agent Script covering constructs your org's bundle may not use:
   ```bash
   git clone https://github.com/salesforce/agentscript
   ls agentscript/packages/compiler/test/fixtures/scripts/
   ```
   Apache-2.0 on the language and tooling; **the runtime is not open** — it compiles to a
   Salesforce-internal specification format that executes on Salesforce infrastructure.

### Part B — edit and round-trip it (20 min)

4. **Change one thing.** In your generated `.agent` file, edit a single topic description — the
   same field you emptied in `ag-01`, now in text form and under version control.
5. **Deploy it back.** Catching problems locally is the entire point of having a language:
   ```bash
   sf project deploy start
   ```
6. **Preview the bundle**, not the published agent — this path sends context variables correctly
   and is the one the authoring loop is built around:
   ```bash
   sf agent preview --authoring-bundle <path-to-bundle>
   ```
7. **Diff the trace against ag-01's.** Same utterance, same agent, different authoring path. They
   should agree. If they don't, you have found the tooling seam, not a mistake of yours.

### Part C — record what you learned (10 min)

8. **Fill in `My verified syntax` below** with 10–20 lines copied out of the file you just
   compiled, plus the date and the dialect version. Copied, not retyped.
9. **Record the dialect version**, because a syntax claim without one is worthless:
   ```bash
   cd agentscript && git log -1 --format="%h %ad %s" && grep '"version"' packages/compiler/package.json
   ```

## My verified syntax

> Paste from a file that compiled. Stamp it. Correct it on drift rather than deleting it.

```
compiled: —          dialect: —          agentscript commit: —
```

```
(paste here)
```

## The block vocabulary, as verified by this repo's radar

Not syntax — the **names**, so you recognise them in a file and know what to search for. Sourced
from [agentforce-platform.md](../../05-release-radar/agentforce-platform.md), the 2026-08-19 sync.

| Block | Topology | Note |
|---|---|---|
| `config` | both | Carries `config.agent_type` and `config.runtime.*` |
| `start_agent` | conversational | Entry point when a user turn arrives |
| `subagent` | conversational | Routing target |
| `modality voice:` | conversational | **Two incompatible schemas** — v1 flat keys, v2 nested `inbound:` / `outbound:` |
| `orchestrator` | goal-based | Replaces `start_agent` as the entry point |
| `workflows` · `trigger` · `actions` · `bundles` | goal-based | `trigger:` fires a workflow on cron — `schedule: "*/5 * * * *"` |

`config.agent_type: "GoalBasedAgent"` (internal name **AgentIQ**) switches the grammar. The two
topologies are **mutually exclusive, and the linter enforces it both ways**: `gba-only-<block>`
outside a goal-based agent, `gba-forbidden-<block>` inside one.

## How you know it worked

- A `.agent` file you edited deployed cleanly, and the change is visible in the Builder UI.
- `sf agent preview --authoring-bundle` returns a trace matching `ag-01`'s for the same utterance.
- `My verified syntax` above is filled in, dated, and version-stamped.

## Break it on purpose

1. **Mis-type `agent_type`.** Set it to `GoalBasedAgnet` and lint. You will *not* get an
   unknown-type error — the check is `agentType.trim().toLowerCase() === "goalbasedagent"`, so a
   typo silently yields a **conversational** agent that then fails on every goal-based block.
   Record the error list you get instead.
2. **Put a `workflows:` block in a conversational script.** Expect `gba-only-workflows`. Then set
   `agent_type: "GoalBasedAgent"` and add a `subagent` — expect `gba-forbidden-subagent`. Those
   two error codes *are* the boundary between the topologies.
3. **Mix voice schema versions.** Paste an `inbound_keywords:` line into a script that already has
   a nested `outbound:` block. Expected, verbatim: *"Invalid modality voice configuration. Both
   Voice schema versions were detected, use only one at a time."* The compile returns `null` —
   so adding one nested block to a working v1 script breaks the **whole** compile, not that block.
4. **Try `additional_parameter__disable_graph_runtime`.** Hard error,
   `disabled-additional-parameter`, no runtime replacement. Six sibling `additional_parameter__`
   fields merely warn (`deprecated-additional-parameter`) in favour of `config.runtime.*` — find
   which six, and note them here.

## What it does not prove

- **Nothing about activation.** Publishing is eval-gated: `publish activate=true` was removed in
  favour of `agentscript_eval action='run_release'`, with `acknowledge_untested_activation=true`
  as the escape hatch. That is `ag-07`.
- **Nothing about the goal-based topology at runtime.** A cron-triggered agent has **no inbound
  turn to authorise against**, so its run-as identity, sharing and FLS are a design decision that
  nothing in the script states. Read it; don't deploy one until you have decided that.
- `GoalBasedAgent` had **no Salesforce announcement, release note or doc page** as of 2026-08-20 —
  a language surface published ahead of the product. Do not quote it to a client as shipping.

## Notes from my run

—

## Failure signature

—
