---
tags: [flashcards/sandbox, review]
---
# Spaced Repetition tour

Ten flashcards, one per plugin feature, built from facts already in the vault. They produce 19 cards in review. Hand-written, not generated, so editing this file is safe. Delete the `_sandbox/` folder when you are done. Test steps are in the README in this folder.

## Apex governor limits

#flashcards/sandbox/apex

### C1 · Single-line basic

How many SOQL queries can one synchronous Apex transaction run?::100. An async transaction gets 200.

### C4 · Multi-line bidirectional

Async Apex limits
(SOQL, heap, CPU)
??
200 SOQL queries
12 MB heap
60,000 ms CPU

### C6 · Cloze with hints

A SOQL query on a `__mdt` object is ==unlimited;;counted or unlimited== in Apex, but ==counted;;counted or unlimited== inside a Flow.

### C7 · Numbered cloze groups

Sync Apex gets ==1;;100== SOQL queries and ==1;;6 MB== heap. Async Apex gets ==2;;200== SOQL queries and ==2;;12 MB== heap.

## Sharing

#flashcards/sandbox/security

### C2 · Single-line bidirectional

`inherited sharing`:::The sharing keyword for a shared utility class. It takes the caller's context and falls back to `with sharing` when entered directly.

## Order of execution

#flashcards/sandbox/order-of-execution

### C3 · Multi-line basic with formatting and a link

Where do before-save record-triggered flows fire relative to before triggers?
?
**Before them.** Flows run at step 3 and before triggers at step 4.
So a flow may already have changed `Trigger.new`.
Source: [Order of Execution & Recursion](../SF_core/02-apex-and-triggers/07-order-of-execution-and-recursion.md)

### C8 · Overlapping cloze, recite a sequence

Save order: step 3 ==ash;;before-save flows;;first== → step 4 ==has;;before triggers;;next== → step 5 ==hha;;validation rules;;then==

### C9 · Code block on the question side

What is wrong with this recursion guard in a trigger handler?
```apex
public static Boolean hasRun = false;

public void afterUpdate(List<Account> records) {
    if (hasRun) return;
    hasRun = true;
    // ...work on records
}
```
?
It guards per transaction, not per record. The first 200-record chunk sets it, and every later record in the same transaction is skipped silently. Track processed Ids in a `static Set<Id>` instead.

## Org setup

#flashcards/sandbox/admin

### C5 · Cloze with four deletions (siblings)

Sandbox refresh intervals: Developer ==1 day==, Developer Pro ==1 day==, Partial Copy ==5 days==, Full ==29 days==.

### Ignored card (wrapped in a comment, never reviewed)

<!--Does this card ever appear in review?::No. Remove the comment wrapper to bring it back.-->

## Experience Cloud

### C10 · Question-specific tags, one card in two decks

#flashcards/sandbox/experience-cloud #flashcards/sandbox/currency-warning Which Experience Cloud templates are LWR-based?::Only two: Build Your Own (LWR) and Microsite (LWR). Every other template is Aura.
