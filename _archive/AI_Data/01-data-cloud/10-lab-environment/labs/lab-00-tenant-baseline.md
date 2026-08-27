# Lab 00 — Tenant Baseline

> Status: ⬜ not started · Date run: —

## Goal

Find out what your tenant actually is, and write down the numbers everything else will be measured against. Twenty minutes, no configuration changes. Skipping this means you can never answer "what did that cost me?"

## Prereqs

- A Developer Edition org with Data 360 enabled.
- If **Setup → Data 360 Setup** doesn't exist, stop: get a Partner Developer Edition org from Environment Hub instead ([why](../notes.md#gotchas--sharp-edges)).

## Steps

1. **Confirm provisioning.** Setup → Data 360 Setup. Note which nodes exist — the surface differs by tenant and it's the fastest inventory you'll get.
2. **Data spaces.** Data 360 Setup → Data Spaces. Record the name of the default space *exactly* — you'll need it in every `SET OPTIONS` clause from lab-01 onward.
3. **Licences and limits.** Setup → Company Information, and the Data 360 usage/limits page. Record storage cap and any credit allowance shown.
4. **Credit usage.** Find the usage or consumption monitoring page and record today's number. This is the baseline.
5. **What's already there.** Data Streams, Data Lake Objects, Data Model Objects — a fresh tenant usually has some standard DMOs and no streams. Note the counts.
6. **Query Workspace smoke test.** Run any trivial query. You're proving the workspace works and learning where it lives, not learning anything about data.

## Baseline record

Fill this in — it's the whole point of the lab.

| Item | Value | Noted on |
|---|---|---|
| Org ID / alias | | |
| Edition | | |
| Default data space name | | |
| Storage cap | | |
| Credits allowance | | |
| Credits consumed at baseline | | |
| Existing data streams | | |
| Existing DLOs / custom DMOs | | |
| Data 360 Setup nodes present | | |

## How you know it worked

You can answer, from your own notes and without opening the org: what's my data space called, how much storage do I have, and how many credits had I spent before I started?

## Break it on purpose

Nothing to break yet. Instead, find the page that would tell you a job had *failed* — the data stream refresh history — and look at it while it's empty. Knowing what "nothing has happened here" looks like makes "something failed here" obvious later.

## Credits spent

—

## Notes from my run

—
