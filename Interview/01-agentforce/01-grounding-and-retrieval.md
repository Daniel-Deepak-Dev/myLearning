# Agentforce — Grounding & Retrieval

> Area: Agentforce · Set 01 of 03 · Scenarios: 4 · Level: medium→complex · Currency: **Summer '26 (API 67.0)**

**Drills:** the agent is fluent, specific and wrong. Every scenario here is a retrieval or freshness failure that presents as a model failure — which is why they get misdiagnosed in production.

---

### Q1 · The agent knows the customer, badly

**Level:** Medium · **Probes:** [RAG on Platform](../../AI_Data/01-data-cloud/08-rag-on-platform/notes.md) · [Identity Resolution](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md)

**Scenario.** A retail client runs a Service agent that answers "what do we know about this customer?" for tier-1 reps. It is grounded on a search index built over ingested profile data — contact details, order history, support history, loyalty tier. Reps complain it is slow (3–5 seconds), and roughly one answer in six is missing recent orders that are visibly present in the CRM record open on the next tab. The client's proposed fix, already scoped and costed, is to increase Top-N on the retriever and add a re-ranking step.

**Asked as:** "They want to spend the budget on better retrieval. Do you sign that off?"

<details><summary><b>Model answer</b></summary>

**Lead with.** No — this is structured data behind a semantic search, which is the wrong retrieval primitive, and the missing orders are a separate defect that better ranking cannot touch. Two problems are being treated as one.

**Then work through.**
- **The wrong primitive.** Vector search is for unstructured content where you do not know which document holds the answer. "What do we know about this customer" is a known-shape lookup against a known key. A **data graph** serves it precomputed and denormalized in **milliseconds**, exactly and without ranking. Semantic search over structured data is slower, fuzzier and costlier — swapping the source fixes the latency complaint outright, not incrementally.
- **Top-N cannot retrieve what is not indexed.** One-in-six missing recent orders is a freshness or completeness failure upstream. Re-ranking reorders candidates; it does not create them. Spending here buys nothing on the accuracy complaint.
- **Where the missing orders actually come from.** Two candidates, and they are distinguishable. If the order data arrives on a **scheduled** stream, the agent is reading a stale copy — the fix is [Accelerated Data Ingest](../../AI_Data/01-data-cloud/02-ingestion/notes.md), GA and the default for CRM. If ingestion is current, suspect a **fragmented profile**: under-matching split one person across several unified profiles, so the agent sees a fraction of the history and reports it confidently.
- **How to tell them apart before spending anything.** Check the profile-count-to-source-row ratio for a customer that failed. Far above expectation means fragmentation. Then change one order in the source and time how long until the agent sees it — that isolates freshness.

**The trap.** Accepting the framing that this is a retrieval-quality problem because the symptoms are retrieval-shaped. It is a source-choice problem plus a data-pipeline problem, and the proposed fix addresses neither. Worse, Top-N raises tokens and cost per action, so it makes the bill worse while the accuracy complaint survives.

**Follow-ups they will ask.**
- "When *would* you use vector search for customer data?" — unstructured only: call transcripts, emails, uploaded documents.
- "The client already paid for the search index. Wasted?" — no, repoint it at the unstructured corpus where it earns its keep; run the graph alongside it.
- "Under profile pricing, what does fragmentation cost?" — you are billed on unified profiles at ~$240/1,000, so one person split three ways is billed three times *and* answers from a third of their history.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Rejects the premise, separates the latency problem from the accuracy problem, names data graph for structured lookups, and gives a way to distinguish staleness from fragmentation before spending |
| 🟡 Partial | Says "use a data graph" for the latency but treats the missing orders as the same problem, or as a model limitation |
| 🔴 Weak | Tunes retrieval — Top-N, chunking, re-ranking, a better embedding model. Any answer that stays inside the retriever |

**Ask this if they stall:** "Forget the agent for a second. If a rep asked you for that customer's last five orders, would you write a SOQL query or a search?"

</details>

---

### Q2 · The library says it is ready 🆕

**Level:** Medium · **Probes:** [RAG on Platform](../../AI_Data/01-data-cloud/08-rag-on-platform/notes.md) · [Agent Script](../../AI_Data/02-salesforce-ai/07-agent-script/notes.md)

**Scenario.** You have scripted Data Library provisioning through the ADL Connect API so it runs in CI — create, upload, index, wire into the agent's `knowledge:` block. The pipeline polls the library's top-level `status` field and proceeds when it reports ready. It passes in CI. Roughly a third of deployments then produce an agent that answers every knowledge question with "I don't have information about that", and re-running the identical pipeline an hour later fixes it with no code change.

**Asked as:** "Intermittent, timing-dependent, fixes itself on retry. Where do you look first?"

<details><summary><b>Model answer</b></summary>

**Lead with.** The pipeline is polling the wrong field. `status` leads `retrieverId` by **10–30 minutes** — so the library reports ready, the deployment proceeds, and the retriever that actually serves queries does not exist yet.

**Then work through.**
- **The fix.** Poll until **`retrieverId` is non-null**, not until `status` flips. That is the only signal that means retrievable. Everything else about the pipeline is fine.
- **Why it passed CI and the ~1-in-3 rate.** The gap is a race, and the window is wide — 10 to 30 minutes. Whether you land inside it depends on indexing time, which depends on corpus size and load. A CI run with a small fixture indexes fast enough to slip through; a production-sized corpus does not. This is the standard shape of a race condition that survives testing.
- **How it presents, and why that misleads.** "I don't have information about that" is indistinguishable from a genuine retrieval miss, so the first instinct is to blame chunking, the corpus or the model. Nothing in the symptom points at provisioning.
- **What else to check in the same pass.** Three adjacent gotchas in the same API, all cheap to verify: `sourceType` is nested under `groundingSource`, not top-level; `rag_feature_config_id` is `"ARFPC_" + libraryId`, not the raw ID; and the S3 pre-signed upload needs the returned headers forwarded **verbatim** or it 403s.
- **The status caveat.** 🚩 The ADL Connect API is **Beta**. Fine to build on — this pipeline is the right shape — but not something to make contractually load-bearing.

**The trap.** Treating "fixes itself on retry" as evidence of a transient platform fault and adding a retry loop or a fixed sleep. That converts a deterministic bug into a slower deterministic bug: a `sleep 1800` is not a fix, and any sleep short enough to tolerate in CI is short enough to lose the race under load.

**Follow-ups they will ask.**
- "How would you have caught this before production?" — assert on a real retrieval, not on a provisioning status code. A smoke test that asks one known question and checks for a cited answer.
- "Why does Salesforce expose a status that lies?" — it reports library provisioning, which genuinely is complete; indexing and retriever construction happen behind it. The field is not wrong, it answers a different question than the one the pipeline is asking.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Names the `status` / `retrieverId` lag and the 10–30 minute window unprompted, and says the smoke test should assert on a retrieval rather than a status |
| 🟡 Partial | Reasons correctly to "the index isn't ready when we start querying" without knowing the specific field, but proposes polling the right thing |
| 🔴 Weak | Adds a sleep or a retry; or investigates chunking, embeddings or the model |

**Ask this if they stall:** "The pipeline has four steps and one of them reports its own completion. How much do you trust that report?"

</details>

---

### Q3 · The question RAG cannot answer

**Level:** Complex · **Probes:** [RAG on Platform](../../AI_Data/01-data-cloud/08-rag-on-platform/notes.md) · [Custom Agent Actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) · [Agent Script](../../AI_Data/02-salesforce-ai/07-agent-script/notes.md)

**Scenario.** An insurance client wants an agent to answer "am I covered for this?" from policy documents. You build it properly: ADL over the policy corpus, tuned chunking, citations back to source clauses. Testing looks good — answers are fluent, cite real clauses, and the SME panel approves the sample. In UAT, a customer asks about a claim scenario where coverage depends on a policy clause **and** their premium being current **and** the incident date falling inside the cover period. The agent cites the correct clause and states the customer is covered. They are not — the policy lapsed in March. Legal now wants the agent switched off.

**Asked as:** "The retrieval was correct and the citation was correct. So what went wrong, and what do you build instead?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Retrieval worked exactly as designed and the architecture was still wrong. "Am I covered" is not a document-lookup question — it is a **deterministic eligibility decision over live policy state**, and RAG has no access to state. The agent answered the question it could answer and presented it as the question that was asked.

**Then work through.**
- **Split the question.** Two different problems wearing one sentence. *"What does my policy say about water damage"* is genuinely retrieval — unstructured, semantic, RAG is right. *"Is my policy in force and does this incident fall in the cover period"* is a lookup and a date comparison against live records. Retrieval cannot answer the second and cannot know it is missing it.
- **What to build.** The eligibility decision goes in a **deterministic action** — invocable Apex or an autolaunched Flow reading live policy status, premium state and cover dates. Then use Agent Script's **Hybrid Reasoning** to make the control flow explicit: run the eligibility action first, branch on its result, and only let the model reason over retrieved clauses *within* a coverage outcome the code has already established. This is precisely the dial Agent Script exists to set — deciding which parts the LLM should be deciding at all.
- **Why the model could not save itself here.** With only the clause in context, nothing signals absent information. An LLM will not spontaneously ask "is this policy current?" — that constraint was never in the prompt. The fix has to be structural.
- **What the testing missed, and this is the transferable lesson.** The SME panel reviewed sample answers, which tests *fluency and citation*. It cannot catch a scenario class that was never in the sample. Multi-constraint eligibility cases needed to be an explicit test category — that is what [agent evaluations and Custom Scorers](../../AI_Data/02-salesforce-ai/09-observability-and-testing/notes.md) are for. A scorer asserting "did it verify policy status before answering coverage" would have failed this on day one.
- **What to tell Legal.** They are right to escalate, and the honest framing is that the agent is currently scoped to answer *what the policy says* and was allowed to answer *whether you are covered*. Narrow the scope now — including the action's description, so the agent stops selecting it for eligibility questions — and re-open with the deterministic path in place.

**The trap.** Reaching for prompt engineering: add "always check policy status" to the instructions, or add status to the retrieved context. That leaves a **legal determination depending on a model choosing to comply**. It will hold in testing and fail on the phrasing nobody tried. When an answer has legal consequence, the constraint belongs in code, not in prose.

**Follow-ups they will ask.**
- "The client says the deterministic action makes it 'not really AI'." — the AI is doing the part only AI can do: reading unstructured clauses and explaining them in the customer's words. Eligibility was never the interesting part.
- "How do you stop the agent answering eligibility at all?" — the action and subagent **descriptions** are the control surface, including explicit *does NOT* clauses. Those descriptions are executable configuration, not documentation.
- "Would citations have saved you?" — no. Cited ≠ correct. The citation was accurate; the conclusion drawn from it was not. Citations make an error findable, which is most of their value, but they are not a correctness guarantee.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Splits the question into a retrieval half and a deterministic half, puts eligibility in code with the model reasoning inside a decided outcome, and names the testing gap as a missing scenario class rather than bad luck |
| 🟡 Partial | Sees that live policy state is missing and adds it to the grounding context, but leaves the determination with the model |
| 🔴 Weak | Prompt-engineers a guardrail instruction; or blames the model, or the chunking, or proposes a bigger model |

**Ask this if they stall:** "Suppose the retrieval had been perfect and returned every clause in the policy. Would the answer have been right?"

</details>

---

### Q4 · Triage in ninety seconds

**Level:** Complex · **Probes:** [Landscape](../../AI_Data/02-salesforce-ai/01-landscape/notes.md) · [Ingestion](../../AI_Data/01-data-cloud/02-ingestion/notes.md) · [Observability & Testing](../../AI_Data/02-salesforce-ai/09-observability-and-testing/notes.md) · [Multi-Agent Orchestration](../../AI_Data/02-salesforce-ai/08-multi-agent-orchestration/notes.md)

**Scenario.** You are on a call with a client whose Service agent has been live for three weeks. Their complaint: "it hallucinates." That is the whole brief. Escalation rate is up, one rep has screenshotted an answer quoting a discount policy that was withdrawn last quarter, and the client's exec sponsor is asking whether they should move to a different model vendor. You have the call, not the org.

**Asked as:** "You have ninety seconds before the sponsor forms an opinion. What do you say, and what do you ask for?"

<details><summary><b>Model answer</b></summary>

**Lead with.** "Hallucination" is a symptom with about five distinct root causes, and only one of them is the model — so a vendor change is the most expensive way to not fix this. The withdrawn-discount screenshot is the useful detail, because a *specific, plausible, obsolete* fact is the signature of stale grounding, not invention. The model did not make that policy up; something served it.

**Then work through — the triage order, cheapest first.**
- **Is the source stale?** By far the most common root cause, and the one misdiagnosed as a model problem almost every time. A withdrawn policy still sitting in the indexed corpus, or a scheduled data stream lagging live CRM, produces fluent specific wrongness. **Ask for:** when that discount document was withdrawn, whether it was removed from the Data Library, and the refresh schedule on every agent-facing stream.
- **Is the profile fragmented?** Under-matching means the agent answers from part of the customer's history, confidently. **Ask for:** the profile-count-to-source-row ratio.
- **Is it mis-routing rather than hallucinating?** If an orchestrator sent a discount question to a subagent that has no business answering it, the answer is out-of-scope, not invented — and that is a **specification bug in a description**, not a model failure. **Ask for:** the trace files for the escalated sessions. They show which subagent description won the routing decision, which is the difference between guessing and knowing.
- **Is the retrieval empty and the model filling the gap?** Distinguishable from the above: check whether failing answers carry citations. Uncited answers on a grounded agent point at retrieval returning nothing.
- **Only then, the model.** And even here, the lever is usually **per-agent model pinning** in Agent Script rather than a vendor change — a cheap experiment, versioned with the logic.

**Then the framing for the sponsor.** Three weeks live with no scorers is the real finding. Right now "it hallucinates" is an anecdote and a screenshot; there is no measurement, so nobody can say whether this is 2% of sessions or 30%, or whether it is getting better. **The first deliverable is a domain-specific Custom Scorer** — "did it cite a current policy document" — deployed via the `aiAgentScorerDefinitions` metadata type so it lives in source control. That turns the argument from vibes into a number, and under outcome pricing the number is a revenue question, not a QA nicety.

**The trap.** Accepting "it hallucinates" as a diagnosis and reasoning about model quality — or, just as bad, defending the agent. Both concede that this is a model conversation. It is a **data freshness and instrumentation** conversation, and the screenshot is the evidence for that reading rather than against it.

**Follow-ups they will ask.**
- "The sponsor insists on a model comparison anyway." — fine, and cheap: pin a different model per agent and measure. But land the scorers first or you are comparing two things you cannot score.
- "How do you tell stale grounding from genuine invention?" — stale is specific, plausible and *checkable against a real historical document*. Invention is usually vaguer and cites nothing.
- "What if all of that comes back clean?" — then the corpus itself is contradictory, which is a content-governance problem: two live documents disagreeing, and retrieval faithfully returning whichever ranked higher.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Refuses the diagnosis, gives an ordered triage from cheapest cause, reads the withdrawn-policy screenshot as evidence of stale grounding, and makes measurement the first deliverable |
| 🟡 Partial | Lists plausible causes including staleness but unordered, and does not push back on the model-vendor framing |
| 🔴 Weak | Discusses model quality, temperature, or a bigger model; or defends the agent; or promises to "look at the prompts" |

**Ask this if they stall:** "That withdrawn discount policy — the agent quoted it accurately. Where would it have read it?"

</details>
