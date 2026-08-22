# Lab ag-01 — First Agent, and Reading the Trace

> Status: ⬜ not started · Box: **30 min** · Date run: —

## Goal

Go once around the whole loop — build, preview, inspect — on the smallest possible agent, and end
by reading a **reasoning trace** rather than an answer. This goes second because when `ag-02`
breaks you need to know it's the CLI and not the concept.

The deliberate constraint: **one topic, one action, no custom Apex, no grounding.** Anything you
add here is something you'll have to eliminate later when behaviour surprises you.

## Prereqs

- [ag-00](ag-00-tenant-baseline.md) done, baseline table filled in.
- Nothing else. No data, no Data 360, no Apex.

## Steps

1. **Create the agent in Agentforce Builder.** Setup → Quick Find → **Agentforce Studio** →
   Agents → New. Take the default agent type. Give it a name you will recognise in a trace file
   later — `Lab01_Echo`, not `Test`.
2. **Give it exactly one job.** One topic. Scope it to something with a verifiable answer and no
   record access: "answer questions about this org's support hours."
3. **Write the topic description like an API doc, not a label.** This is the whole experiment.
   The description is what the reasoning engine routes on — see
   [02-agentforce-anatomy](../02-agentforce-anatomy/notes.md). Write a *good* one now; `ag-05`
   deliberately writes a bad one.
4. **Attach one action.** A standard action, or none at all if the topic can answer from
   instructions. Resist adding a second.
5. **Preview in the Builder.** Send three utterances: one squarely in scope, one clearly out of
   scope, and one ambiguous. Note what each does *before* looking at the trace.
6. **Now preview from the CLI**, which is where the trace lives:
   ```bash
   sf agent preview --api-name Lab01_Echo
   ```
   Send the same three utterances.
7. **Find and read the trace.** Traces are written locally under:
   ```
   .sfdx/agents/<agent-name>/sessions/<session-id>/traces/
   ```
   Open the trace for the **ambiguous** utterance. Find: which topic matched, the confidence or
   selection reasoning, which action fired, and what was passed to it.
8. **Copy one trace excerpt into `Notes from my run`.** The part that shows topic selection. You
   are building a reference for what "normal" looks like, so that abnormal is recognisable.

## How you know it worked

- The in-scope utterance answers, and the trace shows **your topic** matched — not a fallback.
- The out-of-scope utterance declines or falls back, and the trace shows **why**.
- You can point at the exact line in the trace that made the routing decision.

Answering correctly is *not* the success condition. An agent can answer correctly by accident,
from the model's own knowledge, having matched no topic at all — and that is the single most
misleading state in this entire ladder. The trace is the only place it shows.

## Break it on purpose

1. **Empty the topic description**, re-deploy, re-send the in-scope utterance. Watch routing
   degrade while the *answer* often stays plausible. This is mechanism behind
   *"a vague subagent description is a bug, not a style issue."*
2. **Compare the two preview paths.** Run the same utterance through `--api-name` and through
   `--authoring-bundle` and diff the transcripts. They initialise sessions differently — as of
   `@salesforce/agents` 2.0.1/2.0.2 the `--api-name` path had two silent-failure bugs
   (`bypassUser`, then dropped context variables). If they disagree, that is the tooling, not you.
3. **Ask it something the org has no data for** and read the trace for whether it grounded or
   invented. Fluent, specific and wrong is the signature to memorise.

## What it does not prove

Nothing about grounding, Apex actions, sharing, or FLS — the agent touched no records. Nothing
about Agent Script: everything here was clicked, which is exactly what `ag-02` replaces.

## Notes from my run

—

## Failure signature

—
