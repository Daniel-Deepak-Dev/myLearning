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
