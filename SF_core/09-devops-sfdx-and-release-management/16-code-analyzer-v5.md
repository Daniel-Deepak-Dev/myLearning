# Code Analyzer v5

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 17

**Scope:** Static analysis as a pipeline gate — the engines, the config file, and what it does and does not catch. Runtime performance analysis is [17](17-apexguru-and-performance-review.md); the human half of review is [19](19-code-review-conventions-for-metadata.md).

> **What changed.** **Code Analyzer v4 reached end-of-life in August 2025.** The command topic moved from `scanner` to `code-analyzer`, and the per-engine flag soup was replaced by **one `code-analyzer.yml`**. The `@salesforce/sfdx-scanner` plugin was also dropped from the CLI's just-in-time install list, so `sf scanner …` now needs a deliberate manual install — if it runs on your machine, that is a plugin somebody installed, not a supported default. Any guide that configures PMD by passing a ruleset path on the command line is describing the old tool.

## Core idea

Code Analyzer is not a linter. It is a **façade over seven independent engines**, each with its own rule catalogue, unified behind one command, one config file and one normalised severity scale. The value is that a pipeline gate becomes a single exit code instead of five tools' worth of glue.

The engine that justifies the whole thing is **SFGE, the Salesforce Graph Engine**. Everything else pattern-matches a file; SFGE builds a data-flow graph across files and answers questions a regex cannot — *does this path reach a DML statement without a CRUD check?* That is also why it is slow and why it is the one you have to configure deliberately.

## How it works

- **Seven engines:** `pmd` (Apex), `eslint` (JS/LWC), `cpd` (copy-paste), `regex` (your own patterns), `retire-js` (vulnerable JS dependencies), `flowtest` (Flow security), `sfge` (graph/data-flow).
- **Three commands.** `sf code-analyzer rules` lists what would run, `sf code-analyzer run` runs it, `sf code-analyzer config` writes the starting `code-analyzer.yml`. Explore with `rules` before wiring `run` into a gate.
- **`code-analyzer.yml` lives in the repo**, so the standard is versioned and reviewable rather than living in someone's CI script.
- **`--rule-selector` is the whole ergonomics story** — `pmd:1` for critical PMD rules, `eslint:2`, `Security`, or a named rule. Selectors compose.
- **Severity is 1–5**: Critical, High, Moderate, Low, Info. `--severity-threshold 2` makes the command exit non-zero at High or worse, which is the gate.
- **Output formats include SARIF**, which is what makes findings appear as annotations on the PR diff instead of in a log nobody opens.
- **In CI, use the `run-code-analyzer@v2` action** — v1 wraps the retired v4.

## 2026 currency

The interesting movement is not in the tool but around it. **`flowtest` means declarative automation is now in scope for the same gate as Apex**, which closes the oldest hole in Salesforce code review — a Flow could always do what a reviewer would have blocked in a trigger. And the analysis surface has grown a second, non-CLI head: **ApexGuru inside the DX MCP Server** puts review in the editor, driven by runtime metrics rather than static rules → [17](17-apexguru-and-performance-review.md). Treat them as complementary: Code Analyzer says *this code is wrong*, ApexGuru says *this code is slow in your org*.

## Gotchas

- **SFGE is the slow one, by an order of magnitude.** Running it on every push is how teams end up disabling analysis entirely. Run pattern engines on push, SFGE on PR or nightly.
- **SFGE needs the whole project to be resolvable.** Point it at a subset of files and it reports path-not-found style noise, because a partial graph is not a graph.
- **Default severity mapping is not your severity mapping.** A rule you consider a blocker may ship as Moderate, and the threshold flag is org-agnostic — tune the config, not the threshold.
- **A custom PMD ruleset does not currently override the severity of bundled rules**, only of rules you define; this catches teams migrating a v4 ruleset.
- **`retire-js` scans what is in the repo**, so a library loaded from a static resource zip or a CDN at runtime is invisible to it → [03-lwc · 23](../03-lwc-and-slds/23-static-resources-and-third-party-javascript.md).
- **It does not understand intent.** Sharing decisions, guest-user reachability and agent action scope are human review → [07-security · 26](../07-security-and-sharing/26-secure-coding-checklist.md).
- **Zero findings on a legacy codebase means the config is wrong**, not that the codebase is clean.

## Recall

Q: What replaced the `sf scanner` command topic, and when?
A: `sf code-analyzer`, with v4 at end-of-life since **August 2025** — and the old plugin dropped from just-in-time install, so `sf scanner` only exists where someone installed it by hand.

Q: Which engine does something the others cannot?
A: SFGE, the Salesforce Graph Engine — cross-file data-flow analysis rather than per-file pattern matching.

Q: How does the command become a pass/fail gate?
A: `--severity-threshold` — the command exits non-zero when a finding at or above that severity (1 Critical … 5 Info) exists.

Q: Which output format puts findings on the pull request diff?
A: SARIF.

Q: What does the `flowtest` engine add?
A: Flow security analysis, so declarative automation is gated by the same command as Apex and JavaScript.

## Related

- [17 · ApexGuru & performance review](17-apexguru-and-performance-review.md) — runtime evidence where this note has static rules
- [18 · Linting, formatting & pre-commit](18-linting-formatting-and-pre-commit.md) — the faster gate that runs before this one
- [07-security · 26 Secure coding checklist](../07-security-and-sharing/26-secure-coding-checklist.md) — what static analysis structurally cannot decide
- [02-apex · 08 Bulkification patterns](../02-apex-and-triggers/08-bulkification-patterns.md) — the rules PMD fires on most often
