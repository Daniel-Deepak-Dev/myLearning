# Linting, Formatting & Pre-commit

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 17

**Scope:** The gate that runs in under ten seconds on a developer's own machine. The deep analysis is [16](16-code-analyzer-v5.md); the conventions a human enforces are [19](19-code-review-conventions-for-metadata.md).

## Core idea

The point of a pre-commit hook is **not** to catch bugs — it is to make the pull request contain only the change. A repo without formatting discipline produces diffs where four lines of logic are buried in eighty lines of re-indentation, and the reviewer, being human, approves it. Formatting is therefore a *review-quality* control disguised as a style control.

Salesforce projects have an unusual amount of this to manage because a single repo holds four unrelated languages — Apex, JavaScript, HTML templates and a great deal of XML — and the XML is machine-generated, which is where the noise actually comes from.

## How it works

- **Prettier is the formatter, with `prettier-plugin-apex`.** It is the only widely-used Apex formatter, and it is slow enough on large classes that you want it running on staged files, not the tree.
- **ESLint owns JavaScript**, configured through `@salesforce/eslint-config-lwc`. Three levels ship — `base`, `recommended`, `extended` — and picking `recommended` on a legacy codebase is how teams end up with 900 warnings and no gate.
- **The LWS ESLint rules matter more than the style rules.** They catch what Lightning Web Security will block at runtime, which is otherwise a bug you find in a sandbox → [03-lwc · 09](../03-lwc-and-slds/09-lightning-web-security.md).
- **`husky` + `lint-staged` is the standard wiring** — format and lint only what is staged, so the hook stays fast enough that nobody disables it.
- **`.forceignore` is part of this conversation.** Keeping generated or org-specific metadata out of the repo removes more diff noise than any formatter.
- **The same commands run in CI**, non-negotiably. A hook can be bypassed with `--no-verify`; the pipeline cannot.

## 2026 currency

The one item here that is a correctness issue rather than a taste issue is **LWS distortions**. Summer '26 added several — `data:` URIs blocked on anchor `href`, plus changes around `getAttribute`, `innerHTML`/`outerHTML` getters, `MutationObserver.observe`, the IndexedDB factory and `Promise` methods. The **updated LWS ESLint package** is how you find these before a component breaks in an org, and the **LWS Distortion Viewer** is how you check one you are unsure about → [AI_Data/05-release-radar](../../AI_Data/05-release-radar/developer-tooling-and-apis.md). Note the standing correction: **LWS is the default and Locker was not retired** — an org can still be on the older architecture, so "it works in my org" is not portable evidence → [03-lwc · 09](../03-lwc-and-slds/09-lightning-web-security.md).

## Gotchas

- **Introduce a formatter in its own commit.** Reformatting the repo inside a feature branch makes the feature unreviewable and poisons `git blame` for everyone.
- **Add `.git-blame-ignore-revs`** naming that commit, so blame still works afterwards. This is the step everyone skips.
- **Prettier and the Apex plugin must have matching versions.** A mismatch reformats differently on two machines and produces a war.
- **XML formatting is where the real noise is.** Field ordering inside an `.object-meta.xml` is not stable across retrieves, and no formatter fixes that → [19](19-code-review-conventions-for-metadata.md).
- **A hook is advisory.** `--no-verify` exists, junior developers find it, and only the CI job is a gate.
- **Do not put slow analysis in a pre-commit hook.** Anything over a few seconds gets bypassed within a week; SFGE belongs in CI → [16](16-code-analyzer-v5.md).
- **Line endings.** A Windows developer and a Linux runner disagree unless `.gitattributes` settles it, and the symptom is an entire file showing as changed.

## Recall

Q: What is the actual purpose of formatting discipline in a Salesforce repo?
A: Keeping the diff limited to the real change, so review works — not aesthetics.

Q: Which ESLint rules are correctness rather than style?
A: The Lightning Web Security rules — they catch what LWS will block at runtime.

Q: How do you introduce a formatter without destroying `git blame`?
A: One dedicated formatting commit, listed in `.git-blame-ignore-revs`.

Q: Why can a pre-commit hook never be the gate?
A: It can be bypassed with `--no-verify`; the same checks must also run in CI.

Q: What broke in Summer '26 that the LWS ESLint package catches?
A: Blocked `data:` URIs on anchor `href` and several other new distortions — client-side downloads must use a `blob:` URL instead.

## Related

- [16 · Code Analyzer v5](16-code-analyzer-v5.md) — the slow gate this one runs in front of
- [19 · Code review conventions for metadata](19-code-review-conventions-for-metadata.md) — the diff noise a formatter cannot remove
- [03-lwc · 09 Lightning Web Security](../03-lwc-and-slds/09-lightning-web-security.md) — why the LWS lint rules are load-bearing
- [03-lwc · 15 LWC testing with Jest](../03-lwc-and-slds/15-lwc-testing-with-jest.md) — the other check that needs no org
