# Lab ag-00 — Agentforce Tenant Baseline

> Status: ⬜ not started · Box: **20 min** · Date run: —

## Goal

Establish the three numbers every later lab is measured against: **what is enabled**, **which
model is the org default**, and **the credit balance**. This lab produces no agent. It produces a
table you will look back at, and it exists because "the output changed and I don't know why" is
almost always one of these three moving underneath you.

## Prereqs

- An Agentforce-enabled Developer Edition, authorised in your CLI. `sf org list` shows what you have.
- `sf --version` ≥ the Node 22 floor. If `sf` is older than 2.146, upgrade before `ag-02`.

## Steps

1. **Make this org the default, then confirm it.** No aliases anywhere in the ladder — every
   command targets the default org, so the only thing that matters is that the default is right.
   ```bash
   sf org login web --set-default     # skip if already authorised
   sf org display                     # the org name here is the one every later step uses
   ```
   Copy the **username** and **instance URL** into the table below. That is the record of which
   org these numbers describe — and the reason no alias is needed to keep it straight later.
2. **Record what is on.** Setup → Quick Find → **Einstein Setup** / **Agentforce**. Capture, as
   on/off: Einstein Generative AI, Agentforce (Agents), Prompt Builder, Model Builder, Einstein
   Trust Layer, Data 360. Screenshot the page — this is the one time a screenshot beats notes.
3. **Find the org default model.** Setup → **Einstein Generative AI** → Models (or Model Builder →
   default). Write down the exact model name *and* the date you read it.
4. **Record the credit balance.** Setup → **Digital Wallet** (or Usage → Agentforce credits).
   Record the number and today's date.
5. **List what the CLI can already see.** These commands cost nothing and tell you whether the
   authoring loop in `ag-02` will work at all:
   ```bash
   sf agent --help
   npm ls @salesforce/agents          # inside the sf install; want >= 2.0.4
   sf org list metadata-types | grep -iE "GenAi|AiAgent|Bot"
   ```
6. **Fill in the baseline table below.** Not later. Now, while the pages are open.

## Baseline

| Thing | Value | Read on |
|---|---|---|
| Org username | | |
| Org edition / instance | | |
| API version | | |
| Einstein Generative AI | | |
| Agentforce (Agents) | | |
| Prompt Builder | | |
| Model Builder | | |
| Trust Layer | | |
| Data 360 in this org | | |
| **Org default model** | | |
| **Credit balance** | | |
| `sf` version | | |
| `@salesforce/agents` version | | |
| Metadata types present | | |

## How you know it worked

Every row above has a value and a date. That is the entire success condition.

If **Agentforce (Agents)** is off and you cannot turn it on, stop and record that — it changes
which labs are runnable and is worth knowing now rather than at step 6 of `ag-01`.

## Break it on purpose

1. **Run one throwaway agent interaction, then re-read the credit balance.** You are looking for
   the delta of a single turn. That number is what turns "credits" from an abstraction into a unit
   you can multiply — `actions per resolution × cost` is how
   [14-prebuilt-agents-and-buy-vs-build](../14-prebuilt-agents-and-buy-vs-build/notes.md) builds a
   business case, and it is worth having your own measured figure rather than the doc's.
2. **Query a metadata type that isn't there.** `sf org list metadata-types | grep AiAgentScorer` —
   if Custom Scorers aren't in this org, `ag-07` is parked, and better to learn that here.

## What it does not prove

Nothing about behaviour. A fully-enabled org with a healthy balance still tells you nothing about
whether grounding works — that starts at `ag-01`.

## Notes from my run

—

## Failure signature

—
