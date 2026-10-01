# Spaced Repetition plugin — test steps

A test bench for the Obsidian **Spaced Repetition** plugin (v1.15.4). It uses [spaced-repetition-tour.md](spaced-repetition-tour.md), which holds 10 flashcards that produce **19 cards**. Every card is a real fact from the vault, so a test run is also a study session.

This README carries no flashcard tag, so the plugin ignores it. When you are done, delete the whole `_sandbox/` folder.

## What each flashcard demonstrates

| # | Feature | Syntax | Cards |
|---|---|---|---|
| C1 | Single-line basic | `question::answer` | 1 |
| C2 | Single-line bidirectional | `a:::b` | 2 (a→b and b→a) |
| C3 | Multi-line basic with bold, inline code and a link | `?` on its own line | 1 |
| C4 | Multi-line bidirectional | `??` on its own line | 2 |
| C5 | Cloze with four deletions (sibling cards) | `==text==` | 4 |
| C6 | Cloze with hints | `==answer;;hint==` | 2 |
| C7 | Numbered cloze groups | `==1;;text==`, `==2;;text==` | 2 |
| C8 | Overlapping cloze — recite a sequence | `==ash;;text;;hint==` | 3 |
| C9 | Code block on the question side | a fenced `apex` block above the `?` | 1 |
| C10 | Question-specific tags: one card in two decks | tags at the start of the card line | 1 |
| — | Ignored card | wrapped in `<!-- -->` | 0 |

The file also tests **deck tags** (a tag line under each `##` heading), **card context** (the heading path shown above each question) and **note review** (the `review` tag in its frontmatter).

## 0 · Set up (once)

1. Pull the branch so `_sandbox/` is in your vault.
2. Settings → Community plugins → Browse → **Spaced Repetition** → Install → Enable.
3. Leave every setting at its default for now. Some steps below change one setting, then change it back.

## 1 · Deck tree and subdecks

1. Click the **flashcard icon** in the left ribbon.
2. Expand `flashcards` → `sandbox`. Expect **19 new cards** in `sandbox`, split as:

   | Subdeck | New | Comes from |
   |---|---|---|
   | `apex` | 7 | C1, C4, C6, C7 |
   | `order-of-execution` | 5 | C3, C8, C9 |
   | `admin` | 4 | C5 |
   | `security` | 2 | C2 |
   | `experience-cloud` | 1 | C10 |
   | `currency-warning` | 1 | C10 — the same card |

3. **Proves:** C10 counts in two subdecks but only once in `sandbox`. A tag line sets the deck for every card below it, until the next tag line.

Your real decks (`SF_core`, `SF_Experience_Cloud`) also show in this tree. That's expected.

## 2 · Every card type

Click `sandbox` to start a review. The order is random, so match each card by its text.

- **Context line.** Above each question you should see `spaced-repetition-tour > Spaced Repetition tour > <section> > <C-heading>`.
- **C1** shows the question; the answer is "100. An async transaction gets 200."
- **C2** appears twice: once with `inherited sharing` on the front, once with the definition on the front.
- **C3**: the answer renders **bold**, `code`, and a clickable link to the Order of Execution note.
- **C4** appears twice: "Async Apex limits" → the three numbers, and the three numbers → "Async Apex limits".
- **C5** appears four times. Each time one interval is `[...]` and the other three are visible.
- **C6**: the blank shows the hint `[counted or unlimited]` instead of `[...]`.
- **C7**: card 1 blanks *both* sync numbers together; card 2 blanks both async numbers.
- **C8** asks the save order one step at a time. Card 1 shows `[first]` and hides the rest as `...`. Card 2 shows step 3 and asks step 4 (`[next]`). Card 3 shows step 4 and asks step 5 (`[then]`).
- **C9**: the question shows the Apex as a formatted code block, blank line included. A blank line inside a code fence does not end the card.
- **C10**: the question shows **no** tags. They were used to set its decks and then removed from the text.
- The ignored card never appears.

## 3 · Review controls

During any review:

| Key / button | Expect |
|---|---|
| `Space` or `Enter` | Shows the answer |
| `1` / `2` / `3` | Rates Hard / Good / Easy. The buttons show the next interval |
| `0` | Resets the card's progress (like Anki's *Again*) |
| `S` | Skips the card without scheduling it |
| **Info** button | Shows the card's schedule |
| **Edit** button | Edits the card text in place |
| **Reset** button | Puts the interval back to 1 day and the ease back to the default |

**Check the schedule comment.** Rate C1 *Good*, then open `spaced-repetition-tour.md`. A line like `<!--SR:!2026-10-04,3,250-->` now sits under C1. It's invisible in Reading view. **Proves:** the schedule lives in the file, which is why `vault.py cards` has to carry it across rebuilds.

## 4 · Cram mode

1. Open `spaced-repetition-tour.md`.
2. Command palette (`Ctrl/Cmd+P`) → **Spaced Repetition: Cram flashcards in this note**.
3. Expect all 19 cards, **including the ones you just rated**. Cramming does not change any schedule.
4. Also try **Select a deck to cram** and pick `sandbox/apex` (7 cards).

## 5 · Bury sibling cards

1. Settings → Spaced Repetition → Flashcards → turn on **Bury sibling cards until the next day**.
2. Start a fresh review of `sandbox/admin` and rate one C5 card.
3. Expect the other three C5 cards to be gone for today. The same applies to C2, C4, C6, C7 and C8 siblings.
4. Turn the setting off again if you prefer.

## 6 · Note review (whole notes, not cards)

1. Command palette → **Spaced Repetition: Open Notes Review Queue in sidebar**.
2. Click the ribbon icon once to refresh the queue. Expect `spaced-repetition-tour` under **New** in the `#review` deck.
3. Open the note, then **⋯ menu → Review: Good**.
4. Expect three keys added to its frontmatter: `sr-due`, `sr-interval`, `sr-ease`. The note moves to a dated group in the queue.
5. The status bar shows `Review: N note(s), M card(s) due`. Clicking it opens the next due note.

**Proves:** this is what tagging a weak topic note with `review` would do. It writes into the note's frontmatter, which `vault.py fix` leaves alone, because only `status`, `gaps`, `org_checks` and `labs` are derived.

## 7 · Statistics

Command palette → **Spaced Repetition: View statistics**, or Settings → Spaced Repetition → **Statistics**. Expect a forecast of due cards, plus charts of intervals, eases and card types (new, young, mature). It fills in as you review.

## 8 · Ignoring cards, tags and folders

1. **One card.** In the file, delete the `<!--` and `-->` around the ignored card. Expect `sandbox/admin` to go from 4 to 5 cards. Put the wrapper back.
2. **A tag.** Settings → Flashcards → **Tags to ignore** → add `#flashcards/sandbox`. Expect the **whole file** to vanish from the decks, not just one section: ignoring works per file. Remove it again.
3. **A folder.** Settings → Notes → **Folders to ignore** → add `_sandbox/`. Expect the cards *and* the note-review entry to vanish. Then replace it with `_archive/` and `templates/`, which is worth keeping permanently.

## 9 · Scheduling comment on the same line

1. Settings → **Save scheduling comment on the same line as the flashcard's last line** → on.
2. Reset C1 (Reset button), then rate it again.
3. Expect the `<!--SR:…-->` comment at the end of C1's own line instead of on the next line.

This only affects single-line cards. Turn it back off: every generated card in `_cards.md` is multi-line, and the rebuild script expects the comment on its own line.

## 10 · FSRS (optional — read first)

The plugin warns that FSRS "may cause unforeseen data loss, as it is still not tested enough". The sandbox is the safe place to try it.

1. Settings → Algorithm → **FSRS** → confirm the warning.
2. Review a sandbox card.
3. Expect a longer comment: `<!--SR:!fsrs,…-->`.
4. Decide whether to keep it **before** you review your real decks. The plugin says it rewrites a card back to the older format the next time you review it with SM-2-OSR, but there is no reason to switch back and forth.

## Not demonstrated, on purpose

- **Blank lines or tables inside a card.** These need the *end of multiline flashcards* marker setting. Once it is set, a blank line no longer ends a card, so every card in the generated `_cards.md` decks would run into the next one. **Leave it empty.**
- **Convert folders to decks.** The deck tags already give you per-topic decks. Folders would add a second, overlapping tree.
- **Convert `**bold**` to clozes.** Safe today: none of the 1,201 generated questions contain bold. But any future question with bold text would silently turn into a cloze. Leave it off.
- **Review reminders.** The settings exist in the plugin's source code. 🚩 They are not in the 1.15.x changelog, so they may not be in the version you install.
- **RTL text.** Not relevant to this vault.

## Clean up

Delete the `_sandbox/` folder. Its cards and its note-review entry disappear on the plugin's next sync. Your real decks are untouched.
