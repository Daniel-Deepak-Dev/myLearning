# Lab 06 — Data Action Round Trip

> Status: ⬜ not started · Date run: —

## Goal

Close the loop: something changes in Data 360 → a data action fires → a Data Cloud-triggered Flow writes a record back into the **source org from lab-02**. This proves the CRM connection carries traffic in both directions, and it's the pattern behind most real "Data 360 did something useful" demos.

## Prereqs

- [Lab 05](lab-05-insights-and-segments.md) done.
- The lab-02 external org connection still live.

## Steps

1. **Data action target.** Configure one against the external org connection (or the platform event / Flow target, depending on what your tenant exposes).
2. **Data action.** Trigger it on the insight or segment from lab-05 — e.g. a profile crossing the 3-events threshold.
3. **Data Cloud-triggered Flow.** Consume the action and create a record in the source org — a Task on the matching Contact is the simplest visible outcome.
4. **Fire it.** Change source data so a profile crosses the threshold, wait for the insight refresh, and watch.

## How you know it worked

The Task exists in the **source org**. Not "the flow ran" — the record is there, on the right Contact, with data that came from Data 360.

Check the Flow's own debug/error log too, even on success. Learn where that log lives while things are working; you don't want to be looking for it during an incident.

## Break it on purpose

1. **Remove create permission** on the target object for the integration user, then fire the action again. It fails **silently** from Data 360's point of view — the action reports fine, nothing appears in the source org. Find where the failure is actually recorded.
2. **Point the action at a required field you don't populate.** Same class of failure, different log line.

This is the lab that teaches the most useful debugging instinct in the whole ladder: **when a round trip "does nothing", start at the target org's permissions, not at the data action.**

## Credits spent

—

## Notes from my run

—
