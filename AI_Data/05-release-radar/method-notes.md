# Method notes — sourcing and versioning mistakes, learned once

Lessons about *how to check*, not about what shipped. They were previously written as multi-paragraph
essays in the README, one per scan, which pushed the findings off the front page.

**The rules:** one line each. **Maximum one new note per run.** A lesson already on this list is not
re-learned in prose — if a scan rediscovers one, nothing is written. Never re-narrate a mistake the radar
has already recorded.

## Sourcing

- **"Unobtainable" is a statement about one method, not about the fact.** Two scans declared the Winter '27 API version unobtainable because an org endpoint was blocked; it was in `METADATA_SUPPORT.md` in a repo already on the weekly list. _(2026-08-13)_
- **Read the repo's docs directory before trusting a press-release silence.** Seven scans of "Data 360 is quiet" came from press releases while both eventual findings sat in a query guide and a repo already being read weekly. _(2026-08-09)_
- **Fetch the raw file path, not the rendered page.** `raw.githubusercontent.com` answers when `github.com` compare views time out and `.patch` returns 403. _(2026-08-12)_
- **Repository metadata is not code — check commits.** An org-wide OSPO CODEOWNERS sweep on 2026-07-29 makes many Salesforce repos look freshly updated. _(2026-07-29)_
- **A negative finding carries a timestamp.** "No commits since July 24" was true when checked on 07-28 and false hours later when five PRs merged. _(2026-07-29)_
- **"Sales" in a paper title is not "Salesforce".** Two arXiv preprints surfaced on a title match turned out to be Microsoft and Xi'an Jiaotong / Xidian. _(2026-08-11)_

## Versions and release trains

- **When a schedule looks like a stall, check whether the project published its cadence.** Five scans tracked an unmoving `latest` tag as a decision; the CLI release notes state stable ships on Wednesdays. _(2026-08-13)_
- **Release notes may date a version by its planned stable date, not its publish date.** `## 2.148.3 (August 19, 2026)` describes a build published 2026-08-12. _(2026-08-13)_
- **A dist-tag tells you where a pointer is today, not when a version first existed.** 2.147.0 was the first Node-22 CLI, not 2.147.3 — that was just what sat on `nightly` when a scan read the tag. _(2026-08-03)_
- **Ask which layer a change lives in before predicting whether it can reach you.** `sf` pins each plugin to an exact version; each plugin *ranges* its libraries. A library patch arrives on a fresh install; a plugin feature cannot arrive until a new `sf` ships. _(2026-08-14)_
- **A version bump can be actively misleading evidence.** A dist-tag move promoted a *newer* CLI that was still on the unpatched SDR line. _(2026-08-06)_

## Habits that hide things

- **A counting habit reads the diff and misses the artifact.** `sf-skills` was covered four times by counting skills and diffing frontmatter, while it shipped a versioned Claude Code plugin with agents, hooks and an MCP host that none of those entries noticed. _(2026-08-12)_
- **If a scan's output is not on `main`, the next scan cannot see it.** Three scans landed on unmerged `claude/*` branches and every later run re-derived work already done. _(2026-08-08, recurred 2026-08-15)_
