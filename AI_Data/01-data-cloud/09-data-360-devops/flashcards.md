# Data 360 DevOps — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is Code Extension in Data 360?
A: Custom Python scripts and functions deployed to isolated containers on the platform. Current uses: complex batch data transformations, and custom chunking logic on search index creation.

Q: Which Code Extension use case matters most, and why?
A: Custom chunking logic on search index creation. Chunking is usually the single biggest lever on retrieval quality, and until Summer '26 it was a black box.

Q: What is the permission split for Code Extension?
A: Developers author the code; users with the Data Cloud Architect permission set run and monitor it. Author is not operator, and that split is enforced by the platform.

Q: Where do Code Extension failures surface?
A: The code extensions log DLO. They aren't obvious anywhere else.

Q: What is a data kit?
A: A container that organizes Data 360 metadata before packaging — a package can contain more than one. Two kinds exist: DevOps (sandbox → production migration) and standard (a distributable solution bundle).

Q: How do DevOps and standard data kits differ?
A: DevOps — created from any data space, must deploy to the SAME data space in the target org, purpose is sandbox → prod migration. Standard — created from the default data space, deploys to ANY data space, purpose is packaging a solution to share or distribute.

Q: What happens when you add a data transform to a DevOps data kit?
A: Its associated code extension is pulled in automatically, so you don't hand-track the dependency. Convenient — but check what came along.

Q: How does a partner distribute a Data 360 solution on AppExchange?
A: A standard data kit wrapped in a managed package. Data streams, batch data transforms, calculated insights and data graphs deploy into the subscriber org via Package Manager.

Q: What is the constraint on Data 360 metadata shipped in a managed package?
A: It's locked. Subscribers can add new entities alongside it but cannot modify what shipped, so correcting a wrong calculated insight means releasing a new package version.

Q: Why do data kits matter?
A: Data 360 logic can now be promoted through a CI/CD pipeline the same way Apex and LWC metadata are. This closed one of the more painful gaps in Data Cloud DevOps.

Q: What does @IntegrationTest allow that a standard Apex unit test cannot?
A: Live callouts and mid-transaction data commits via IntegrationTest.commitTestOnly(), with cleanup in a @TearDown method. Standard tests mock every callout and roll everything back.

Q: What are the constraints on @IntegrationTest?
A: Scratch orgs only; add ApexIntegrationTests to the features array in the scratch org definition; tests run asynchronously, one at a time, via the Tooling API runTestsAsynchronous resource.

Q: What three facade tools does the Data 360 MCP server expose, and why?
A: search (find a capability by intent), payload_examples (fetch a working request body), and execute (run it) — fronting roughly 200 REST operations instead of exposing 200 flat tools.

Q: Why is the facade-tool pattern worth learning beyond Data 360?
A: It is the canonical answer to context-window blowout in MCP design — a searchable facade over a large API surface rather than a flat tool list. Directly transferable to any MCP server you build.

Q: What are the two different Data 360 MCP servers?
A: A Developer Preview open-source server for connecting a coding agent to Data 360 (build/debug/deploy), and a GA standard hosted server for Data 360 queries and graph traversal. Different purposes — don't conflate them.

Q: Which languages does Code Extension support?
A: Python only so far. Salesforce says other capabilities and languages will follow.
