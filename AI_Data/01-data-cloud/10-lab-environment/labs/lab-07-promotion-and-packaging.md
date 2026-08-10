# Lab 07 — Promotion & Packaging

> Status: ⬜ not started · Date run: —

## Goal

Find out what of the last six labs can actually **move to another org** — and what has to be rebuilt by hand. "How do we promote this?" is the awkward question in every Data 360 design review; this lab is you having already answered it.

You have one tenant, so you can't do a real sandbox → production promotion. You *can* do everything up to the deploy, which is where the learning is anyway.

## Prereqs

- Labs 01–06 built (that's the metadata you'll try to move).
- Salesforce CLI (`sf`) authenticated to the Data 360 org.
- Read [Data 360 DevOps](../../09-data-360-devops/notes.md) first — data kit types, and why the distinction bites.

## Steps

1. **Retrieve.** Use `sf project retrieve start` against the Data 360 metadata types — data streams, DLOs, DMO mappings, calculated insights, data graphs. Start with `sf org list metadata-types` to see what's actually exposed in your API version.
2. **Read what came back.** Open the files. This is the real exercise: the retrieved shape tells you what Data 360 considers configuration versus what it considers *state*.
3. **List what did NOT come back.** Connections. Credentials. Ingested data. Anything environment-specific. Write this list down — it's the "manual steps" section of every runbook you'll ever hand a client.
4. **Build a DevOps data kit** containing something from lab-05. Note that it is pinned to the data space it was created from, and that a data transform pulls its code extension along automatically.
5. **Build a standard data kit** from the default data space and compare. One is a promotion mechanism, the other is a distribution mechanism, and they aren't interchangeable.

## How you know it worked

You can write, from your own notes, the promotion runbook for the lab-02 connection: *these artifacts deploy, these must be recreated by hand in the target org, in this order.* If you can't name the manual steps, you haven't finished the lab.

## Break it on purpose

Deploy the retrieved metadata **back into the same org** and see what's rejected as already existing or immutable. Then find one thing that is genuinely not deployable at all and confirm it. Discovering a "you have to click this" the day before a go-live is the failure mode this lab prevents.

## What you can't do here

A real sandbox → production run. It needs two real orgs, and it's on the list of [things a free DE can't teach](../notes.md#what-you-cannot-learn-on-a-free-de). Say so plainly rather than implying you've done it.

## Credits spent

—

## Notes from my run

—
