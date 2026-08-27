# Harmonization & Identity Resolution — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is identity resolution?
A: Matching records across sources into one unified individual using match rules and reconciliation rules.

Q: Match rules vs reconciliation rules?
A: Match rules decide WHEN two records represent the same person; reconciliation rules pick the WINNING VALUE when matched records conflict.

Q: What is a unified profile?
A: The single individual record produced after identity resolution, linking all source records and behaviors. It is also the Data 360 billing unit.

Q: Name three reconciliation strategies.
A: Most recent, most frequent, source priority.

Q: How is Data 360 priced since March 2, 2026, and why does it change identity-resolution design?
A: A profile-based SKU at roughly $240 per 1,000 profiles (about $420 premium). A profile is a unified individual after resolution, so you are billed on the output of your ruleset — duplicates and under-matches inflate a recurring bill directly.

Q: What are the two failure directions in matching, and which is more dangerous?
A: Under-matching (too strict) fragments one person into several profiles — you pay several times and the agent sees partial history. Over-matching (too loose) merges two people — cheaper, but it exposes one person's data to another. Over-matching is more dangerous precisely because it is cheaper.

Q: Why must you never tune matching rules on cost alone?
A: Because the cheaper direction is over-matching, which is a privacy incident, not just a data-quality issue.

Q: What is the household problem in fuzzy matching?
A: Fuzzy name plus address merges two people living at one address with similar names into a single profile — a spouse's data becomes visible in the other's profile.

Q: Should reconciliation strategy be set globally or per attribute?
A: Per attribute. The right rule for Email is rarely the right rule for LifetimeValue.

Q: Which metric tells you whether your matching is healthy?
A: Profile count divided by source-record count. Far below expectation suggests over-matching; far above suggests fragmentation. Under profile pricing it is also your bill, so track it over time.

Q: An agent answers using only part of a customer's history. What is the likely cause?
A: A fragmented profile from under-matching. It is a data-architecture failure that presents as an AI failure — check profile completeness before blaming grounding or the model.

Q: Are new records resolved the moment they land?
A: No. Rulesets run on a schedule, so an agent may briefly see an unresolved fragment.
