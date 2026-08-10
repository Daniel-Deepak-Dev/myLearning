# Lab 05 — Insight & Segment Validation

> Status: ⬜ not started · Date run: —

## Goal

Build one calculated insight and one segment — then refuse to believe either of them until you've reproduced the number with your own SQL. The build is thirty minutes; the validation habit is the deliverable.

## Prereqs

- [Lab 04](lab-04-identity-resolution.md) done — you need unified profiles and the loyalty events from lab-03.

## Steps

1. **Calculated insight.** Something with a real aggregate: event count and last-event date per unified profile. Deploy it, note the **refresh schedule**.
2. **Reproduce it in SQL.** Write the equivalent query by hand in Query Workspace, against the DMOs, with `SET OPTIONS`. Compare row for row on five profiles.
3. **Segment.** Build one on the insight — say "profiles with 3+ events in the last 30 days". Publish it.
4. **Reproduce the segment in SQL.** Count the members yourself.
5. **Reconcile any difference.** It is almost always the refresh or publish schedule, not a bug — but you only get to say that after checking.

## How you know it worked

Your SQL count and the platform's count agree, **or** you can name exactly why they don't (insight last refreshed at X, segment last published at Y). "It looks about right" is not a result.

## Break it on purpose

1. **Change a source record**, then immediately re-check the insight and the segment. Both are stale. Note *how* stale, and that nothing anywhere indicates staleness.
2. Ask the obvious follow-up: if an agent had grounded on this insight in that window, what would it have told a customer? That's the same failure as [stale ingestion](../../02-ingestion/notes.md), one layer up — and it's confident, fluent and wrong.
3. **Write an ambiguous metric definition** ("active customer") and try to compute it two defensible ways. The gap between them is the argument for the semantic layer, in one exercise.

## Credits spent

—

## Notes from my run

—
