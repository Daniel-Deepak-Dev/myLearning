#!/usr/bin/env node
// py.js — run one of this repo's Python scripts with whatever Python 3 is installed.
//
//     node scripts/py.js scripts/flashcards.py check
//     npm run cards:check            (package.json wraps the same call)
//
// Windows usually has `py` (the launcher) or `python`, rarely `python3`;
// macOS and Linux usually have `python3`. This tries them in that order, keeps
// the first that is Python 3.9+, and exits with the script's own exit code.

"use strict";
const { spawnSync } = require("child_process");
const path = require("path");

const MIN = [3, 9];
const CANDIDATES = process.platform === "win32"
  ? [["py", ["-3"]], ["python", []], ["python3", []]]
  : [["python3", []], ["python", []]];

function findPython() {
  for (const [cmd, pre] of CANDIDATES) {
    const probe = spawnSync(cmd, [...pre, "-c", "import sys; print('%d.%d' % sys.version_info[:2])"],
      { encoding: "utf8" });
    if (probe.status !== 0 || !probe.stdout) continue;
    const [major, minor] = probe.stdout.trim().split(".").map(Number);
    if (major > MIN[0] || (major === MIN[0] && minor >= MIN[1])) return [cmd, pre];
  }
  return null;
}

const [script, ...args] = process.argv.slice(2);
if (!script) {
  console.error("usage: node scripts/py.js <script.py> [args...]");
  process.exit(2);
}

const python = findPython();
if (!python) {
  console.error(`Python ${MIN.join(".")}+ was not found (tried: ${CANDIDATES.map(c => c[0]).join(", ")}).`);
  console.error("Install it from https://www.python.org/downloads/ and run this again.");
  process.exit(127);
}

const root = path.resolve(__dirname, "..");
const run = spawnSync(python[0], [...python[1], path.resolve(root, script), ...args],
  { stdio: "inherit", cwd: root, env: { ...process.env, PYTHONIOENCODING: "utf-8" } });
process.exit(run.status === null ? 1 : run.status);
