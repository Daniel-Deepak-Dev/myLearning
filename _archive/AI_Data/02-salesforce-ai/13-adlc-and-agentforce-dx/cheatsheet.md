# ADLC & Agentforce DX — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

The five-phase lifecycle for agents — **Ideation & Design → Development (inner loop) → Testing & Validation → Deployment → Monitoring & Tuning (outer loop)** — driven in practice by three Agent Skills and the `sf agent` commands, from plain language in a coding agent.

## Key terms
| Term | Definition |
|---|---|
| Inner loop | The tight build-and-try cycle run many times a day. |
| Outer loop | The slow cycle of watching production and feeding it back. Where drift is caught. |
| Agent Skills | Open format ([agentskills.io](https://agentskills.io/home)) teaching a coding agent one task. `npx skills add forcedotcom/sf-skills`. |
| `developing-agentforce` | Design + build + deploy + publish. |
| `testing-agentforce` | `sf agent preview` smoke tests, `sf agent test` YAML regression. |
| `observing-agentforce` | Production traces via the **Session Trace Data Model**; **AgentLens** to walk the graph. |
| `agentforce-adlc` | SalesforceAIResearch toolkit. **CC BY-NC 4.0 — non-commercial.** Research-grade, unsupported. |
| Agentforce Vibes 2.0 | Agentic IDE, **Developer Preview**. Free in every Dev Edition org since April 2026. |

## Rules of thumb

- **Design-first.** Plan mode + design interview *before* generating. The spec is what the model executes.
- **Build only in scratch orgs or sandboxes — never production.** Automated fix-and-retry loops make an unscoped deploy genuinely dangerous.
- **Commit Agent Script to Git.** It's source code.
- **`--json` on every command**, or the assistant misparses human-formatted output.
- **Scope deployments explicitly** so unrelated metadata doesn't ship.
- Token economics belong in the **test** phase. Cost is a test result, not an invoice surprise.

## Exam traps / common confusions

- **Three artifacts, three licences:** Agent Script **Apache 2.0** · `sf-skills` Salesforce-supported · **`agentforce-adlc` CC BY-NC 4.0 (non-commercial — not for client work)**.
- **"ADLC" names two things** — the lifecycle framework and the repo implementing a version of it.
- **`agent preview` is GA; agent evaluations are Beta.** Adjacent commands, different maturity.
- **Deployment is day one**, not the finish line — the SDLC intuition is the trap.
- **Drift has no commit.** Nothing changes in Git when an agent degrades.
- A GitHub "Updated" date is repository metadata — check `commits/main.atom` before believing it.

## Minimal example

```bash
npx skills add forcedotcom/sf-skills        # Node.js + Salesforce CLI required

# design   → plan mode (Shift+Tab), design interview, graph: router + subagents
# build    → sf agent generate authoring-bundle
#            sf project deploy start          (backing Flow/Apex first)
# test     → sf agent preview start | send | end
#            sf agent test create | run       (YAML specs)
# publish  → sf agent publish authoring-bundle
#            sf agent activate
# observe  → .sfdx/agents/[name]/sessions/…/traces/   (local)
#            Session Trace Data Model + AgentLens     (production)
```
