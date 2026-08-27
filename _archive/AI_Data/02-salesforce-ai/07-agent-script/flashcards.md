# Agent Script — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is Agent Script?
A: A human-readable expression language for defining Agentforce agents that compiles to portable JSON, blending deterministic control flow with agentic LLM reasoning.

Q: What licence is Agent Script released under, and what ships with it?
A: Apache 2.0 — the parser, linter, compiler, Language Server Protocol implementation and editor integrations, at github.com/salesforce/agentscript.

Q: What is Hybrid Reasoning?
A: The Agent Script design point — dialling, per decision point, how much is structured business logic and how much is left to the model.

Q: Name the four things that follow from agents compiling to JSON.
A: Diffs and PR review; linting and testing in a plain CI job with no org connection; portability to third-party harnesses; and model pinning declared alongside the logic.

Q: Why was the topic-and-instruction model replaced?
A: Behaviour lived in natural-language prose: contradictions were silent, nothing compiled, there was no meaningful diff, nothing was testable outside an org, and reliability problems were untraceable because there was no artifact to trace.

Q: What is the strongest strategic signal in Agent Script being open source?
A: That Salesforce wants agent logic to be portable rather than org-locked — third parties can already execute compiled Agent Script under harnesses like Pydantic AI.

Q: What does the one-click legacy upgrade do, and what must you do afterwards?
A: It converts all subagents, actions, system messages, data and connections into Agent Script, then optionally optimizes for reliability. Afterwards, diff the two behaviours in preview — the optimize step can change behaviour.

Q: Does a definition that compiles cleanly behave correctly?
A: No. The compiler validates structure, not judgement. Behaviour is verified with evaluations and Custom Scorers.

Q: What is the limit on Agent Script portability?
A: The compiled JSON is portable, but the actions it invokes are still org-bound Apex and Flows. Don't oversell "runs anywhere".

Q: Which CLI commands drive an agent preview session?
A: `sf agent preview start`, `send`, `sessions`, `end` — GA — plus trace files showing exactly how the agent routed and acted.

Q: What is the confirmed date fact about Agent Script's rollout?
A: The week of July 13, 2026, the *New Agent* button stopped opening the legacy builder. The exact GA date is not pinned by any first-party announcement.

Q: Is Agent Script on the Agentforce Specialist exam?
A: It isn't named in the exam guide despite being the default authoring model since July 2026. Given the guide's emphasis on deterministic behaviour, filters and variables, assume implicit scope and re-check before booking.

Q: What does `config.agent_type: "GoalBasedAgent"` change about an Agent Script script?
A: It switches the script to a second, mutually exclusive topology. Entry becomes an `orchestrator` block instead of `start_agent`, and `trigger:` fires a `workflows:` entry on a cron schedule with no user turn. Added in the `@agentscript/agentscript` 3.x dialect, synced to open source 2026-08-19.

Q: Which top-level blocks are GoalBasedAgent-only, and which are forbidden inside a GoalBasedAgent?
A: GBA-only — `bundles`, `workflows`, `trigger`, `actions`, `orchestrator`; using them elsewhere raises `gba-only-<block>`. Forbidden inside a GBA — `subagent` and `start_agent`, raising `gba-forbidden-<block>`.

Q: Why is the run-as identity the first design question for a GoalBasedAgent?
A: A cron-triggered run has no inbound user turn to authorise against, so nothing in the conversation determines sharing, FLS or record ownership — and nothing in the script states it either. It has to be designed explicitly.

Q: What happens to `additional_parameter__disable_graph_runtime` in the 2026-08-19 Agent Script sync?
A: It becomes a hard Error (`disabled-additional-parameter`) with no runtime replacement — "Disabling the graph runtime is not permitted." Six other `additional_parameter__` fields are only deprecated, mapping to `config.runtime.*` equivalents.

Q: A GoalBasedAgent-only block lints clean in a plugin dialect. Is that proof it's allowed?
A: No. `gba-only-blocks` returns early when the schema context has no `config` namespace, so plugin dialects are exempt by design. Test the rule in an agent script, not a plugin one.

Q: Your agent uses `connected_subagent` to delegate. `sf agent publish authoring-bundle` fails with `TypeError: Cannot read properties of undefined (reading 'map')`. Why?
A: `connected_subagent` compiles to a **`related_agent`** node — a delegation stub with **no `tools` key at all** — and `ScriptAgentPublisher.retrieveAgentMetadata` mapped `n.tools` unconditionally. Fixed in `@salesforce/agents` **2.0.6** (2026-08-24). Note the existing test covered `tools: []`; the crash needs the property *absent*, not empty.

Q: Is `connected_subagent` a `GoalBasedAgent`-only block?
A: No. The compiler fixture `delegate_escalation.agent` uses it under `config.agent_type: "AgentforceServiceAgent"` alongside `start_agent`, so conversational multi-agent scripts use it too. The blocks the linter restricts to GBAs are `bundles`, `workflows`, `trigger`, `actions` and `orchestrator`.
