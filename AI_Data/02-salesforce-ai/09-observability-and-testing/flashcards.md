# Observability & Testing — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What are Custom Scorers?
A: User-defined quality metrics that grade live agent sessions against your own KPIs, alongside Salesforce's standard quality metrics. Beta, requiring the Agentforce Scorer Beta permission set.

Q: Why does Metadata API support for scorers matter architecturally?
A: Deploying them as `aiAgentScorerDefinitions` means evaluation lives in source control, gets reviewed and ships through a pipeline — evaluation is treated as deployable infrastructure, not a UI setting.

Q: What is Refined Agent Analytics?
A: A GA view unifying Service Agent and Employee Agent analytics into one place with 40+ metrics.

Q: What does a trace file give you?
A: A record of exactly how an agent routed and which actions ran during a preview session — the primary diagnostic for mis-routing, because it shows which subagent description won.

Q: What does the @IntegrationTest annotation allow?
A: Apex tests with live callouts and mid-transaction data commits via IntegrationTest.commitTestOnly(), with cleanup in a @TearDown method — things standard unit tests can't do because they mock every callout and roll everything back.

Q: What are the constraints on @IntegrationTest?
A: Scratch orgs only; add ApexIntegrationTests to the features array in the scratch org definition; tests run asynchronously, one at a time, via the Tooling API runTestsAsynchronous resource. Scratch-org-only keeps it out of most real pipelines for now.

Q: Name the five layers of the agent testing pyramid, bottom to top.
A: Standard Apex unit tests → @IntegrationTest in a scratch org → agent preview with trace files → YAML/JSON agent evaluations → Custom Scorers on live sessions.

Q: Which CLI commands script an agent test session?
A: `sf agent preview start`, `send`, `sessions`, `end` — GA.

Q: Does a clean Agent Script compile mean the agent behaves correctly?
A: No. The compiler validates structure only. Behaviour is verified with evaluations and Custom Scorers.

Q: What does Custom Scorers grading "live sessions" imply for governance?
A: Those are real customer conversations — so consider what is being logged and who is permitted to read it.

Q: What do Testing Center actions cost?
A: 16 credits, roughly $0.08 each — cheaper than a standard action's 20 credits but not free, so a large evaluation suite carries a real bill.

Q: Why is agent observability a commercial topic, not just a QA one?
A: Under pay-per-resolution and Flex Credits, "how well is it working" is a revenue question. A client asking for ROI needs numbers from Agent Analytics, not assurances.

Q: Where does Agentforce write what a production agent actually did, and what does that imply?
A: As session trace records into Data 360, in the Standard Data Model (STDM). It means Data 360 is the observability backend for the whole agent platform — debugging a live agent is a Data 360 query, not a preview session.

Q: What is STDM?
A: Salesforce's Standard Data Model — the prebuilt Data 360 schema, so data from different sources lands in a shape the platform already understands instead of one you map by hand each time.

Q: Which tool do you reach for when someone reports an agent "did something weird yesterday"?
A: `agentforce-observe` against Data 360 traces. The split is by environment, not activity: `agentforce-generate` for authoring/debugging `.agent` files, `agentforce-test` for pre-deployment specs, `agentforce-observe` for production behaviour.

Q: What is `findSessions`, and what is its CLI prerequisite?
A: The documented entry point for locating a specific production conversation in Data 360 trace records before analysing it. The `agentforce-observe` skill declares `sf >= 2.136.8`.

Q: Before quoting a GIFT-Eval leaderboard position, which two `config.json` fields must you read, and why?
A: `replication_code_available` and `testdata_leakage`. Of the five models merged 2026-07-31, only one declared replication code available; the leakage flag is self-declared, not audited. A leaderboard position is a claim, not a result.

Q: AnchorBench separates two failure modes that sound like one. What are they?
A: **Persona collapse** — drifting off the assigned role, boundaries, values and style. **Trajectory recall** — telling what actually happened from a plausible alternative. They come apart: a model can hold steady on a checkpoint questionnaire while drifting in live conversation.

Q: What is AnchorBench's most transferable result for a long-lived service agent?
A: User-state changes are recalled at chance (~0.25 on four-option questions). The customer says at turn 3 that they cancelled; at turn 40 the agent still acts on the old state. That deserves an explicit Testing Center case, not an assumption.

Q: Which AnchorBench finding is invisible to adversarial security testing?
A: Social pressure beats direct attack — schedules built on emotional vulnerability and agreement-seeking surfaced more behavioural failures than explicit adversarial probing. Sycophancy under sustained politeness is a separate axis from prompt injection; both need testing.

Q: Why does MFCL Audio grade argument values, not just function names?
A: Voice adds perception errors — homophones, noise, disfluencies, accent — that corrupt a tool call's *arguments* rather than its intent. An agent that understands "cancel my order" but mis-hears the order number executes the right function on the wrong record.

Q: What is the CRMArena-Pro result you should act on first?
A: Confidentiality awareness is close to absent unless the agent is explicitly prompted for it. Agents disclose what they can reach, so data governance is a prompt-and-permission problem before it is a model problem.

Q: LoCoBench-Agent found comprehension and efficiency negatively correlated. What follows commercially?
A: An agent that explores exhaustively is not simply "better" — under Flex Credits you pay per action, so thoroughness is a priced choice. Measure tool calls per resolved task and decide where on that curve you want to sit.

Q: What is the method warning AnchorBench raises about your own evaluations?
A: Do not measure what the agent *says about itself* at checkpoints. Checkpoint answers held steady while live behaviour drifted, so measure what the agent *does* across a long conversation.

Q: What does `sf_pi.turn_response_integrity` catch that an LLM-judge eval cannot?
A: Double-texting — a turn emitting more than one non-empty LLM completion. A judge reads the final message, and the final message is usually fine. The policy parses `lastExecution.llmEvents` deterministically instead, with no model call.

Q: Why does response-integrity gating run before the org call rather than after the run?
A: At `severity: "error"` it fails local preflight, so a violating suite never spends an org call or an Evaluation API request. The general principle: the cheapest agent test reads evidence you already have.

Q: A suite upgraded to `sf-pi` v0.257.0 shows no integrity findings. Is it protected?
A: No. A suite without the `sf_pi.turn_response_integrity` block keeps advisory-only behaviour — the gate is opt-in. Also check `response_integrity_evidence`, a separate field from the verdict.

Q: What problem does an Agent Script Eval seed profile solve, and what is its hard constraint?
A: Hard-coded record IDs that rot when a suite moves org. A seed profile resolves exactly one row from one bounded read-only SOQL query; zero rows, several rows, null or mistyped fields fail before the run is created. A reused profile executes once per run, not once per scenario.

Q: On the GIFT-Eval leaderboard, what does `model_type: agentic` actually mean?
A: An orchestrator picking among forecasters — not necessarily an LLM. EXAONE-Forecast-Agent routes with XGBoost over seven foundation models, no LLM involved. A router costs N model calls per window; a rank next to a single small model is not a like-for-like comparison.

Q: Two GIFT-Eval PRs carried the same one-line `org` fix and one was closed. What is the durable lesson?
A: The `org` column is self-declared free text in `results/<model>/config.json`, corrected by pull request, and mirrored into a separate Hugging Face leaderboard Space that can drift. Attribution on a leaderboard is a claim like everything else on it.

Q: A React Native Agentforce app on iOS never fires `onAgentResponse`, with no error. What is the diagnosis?
A: It was a no-op on iOS until `@salesforce/react-native-agentforce` 0.4.0 (2026-08-03), while working on Android. Audit for polling or UI-scraping workarounds before upgrading — the workaround becomes the bug.

Q: sf-pi records a turn with no `llmEvents` as `unavailable`, never a passing zero. What hole did that leave, and how was it closed?
A: A looping agent whose instrumentation never arrived produced no verdict at all. v0.260.1 (2026-08-07) added exact repeated-surface detection, which reads what the agent actually said rather than the event log, so it fires even when `llmEvents` evidence is absent.

Q: What changed for Voice eval suites in sf-pi v0.260.0?
A: Generated Voice suites now declare strict `sf_pi.turn_response_integrity` automatically, and an exact-version Voice release contract refuses a designated suite that omits it. Hand-written or older suites still have no policy and get refused late, at release rather than at authoring.

Q: Why is double-texting worse on voice than in chat?
A: In chat two completions are untidy and the user can scroll back. On a call they are two voices talking over each other with no recovery — which is why the strict policy is automatic for Voice suites specifically.

Q: What are the limits of sf-pi's repeated-surface detection?
A: It is an exact surface match, not semantic. An agent that rewords the same non-answer on every turn still passes.

Q: What does SCUBA measure, and what are its headline numbers?
A: Computer-use agents — agents driving the Salesforce GUI by screenshot, accessibility tree and DOM rather than by API — on 300 CRM tasks across admin, sales and service personas. Zero-shot: under 5% success on open-source models, 39% on closed-source. With demonstrations: ~50%, at 13–16% less time and cost.

Q: How do you use SCUBA's result in an architecture argument?
A: It prices the alternative to building actions. If a capability is reachable as an Apex action, an API or an MCP tool, use that — pointing a computer-use agent at the UI is a coin flip at best. Pixels are the fallback for surfaces you cannot get an API to, and they need a human approval gate.

Q: SCUBA's cheapest lesson is not about model size. What is it?
A: Demonstrations beat scale. Adding worked examples moved success from 39% to ~50% *and* cut time and cost 13–16% — a bigger return than swapping models, and something you can add to an agent you have already shipped.

Q: Why should you read SCUBA's numbers with a date attached?
A: They are a 2025 measurement of a UI that has changed since. The repo's newest functional commit is 2026-04-21, and it pins `@salesforce/cli@2.86.9` — hundreds of versions behind current. Treat the gap between paradigms as the durable finding, not the exact percentages.

Q: What non-obvious obstacle does SCUBA's commit history reveal about computer-use agents in an enterprise?
A: Authentication. Its first substantive commit was "bypass the multi-factor-auth", and it needed a further "Login fix" months later. A computer-use agent meets your MFA and session handling before it meets any business logic — that is where these projects stall, not on reasoning.

Q: Why should you not cite SCUBA's scores as evidence about Agentforce?
A: Different modality. SCUBA grades agents that navigate by screenshot, accessibility tree and DOM with a 19- or 15-action mouse/keyboard space. Agentforce acts through invocable actions and APIs. SCUBA is evidence about the screenshot-and-click approach, not about Agentforce.

Q: What is the trap in quoting a SCUBA percentage?
A: Scoring is milestone-based, so partial progress accrues on tasks that never complete. A 39% milestone score is not 39% of tasks finished — check which figure a citation means.

Q: What does SCUBA's OSWorld comparison tell you about general-purpose agents?
A: Performance drops sharply moving from generic desktop benchmarks into enterprise CRM. Broad computer-use ability does not transfer to Salesforce — which is the practical argument for giving agents APIs rather than a cursor.

Q: On SCUBA, open-source-model computer-use agents score under 5% while closed-source reach 39%. What decision does that number drive?
A: It prices "just let the agent drive the existing UI". The best agent fails six times in ten on real CRM work, so any capability reachable as an API, MCP tool or `sf` command should be taken there instead. That gap is the argument for Headless 360 in one number.

Q: Why does SCUBA use milestone scoring instead of pass/fail?
A: Binary scoring throws away where a long enterprise task broke. Partial credit distinguishes misreading the UI, losing the plot mid-workflow, and fumbling the final commit — three different fixes.

Q: Someone quotes "SCUBA: 50%". What must you ask before believing it?
A: Which setting. Zero-shot and demonstration-augmented are separate data files (`data/test_zero_shot.json`, `data/test_demo_aug.json`) and differ by roughly 10 percentage points. ~50% is the demonstration-augmented figure, not zero-shot.

Q: GIFT-Eval #184–#186 merged within two days; #188 has been open four. What does that teach about leaderboard submissions?
A: "Submitted" is an indefinite state, not a queue position. Merge latency is not predictable from a previous batch, so a submission is not a result until you see the merged commit.
