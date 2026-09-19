#!/usr/bin/env python3
"""vault.py — the mechanical half of the notes contract.

NOTES-SYSTEM.md is the normative source. Everything this script checks is a rule
written there that a machine can decide without judgement. Anything needing a
reading of the prose stays with you and the study-notes skill.

    python scripts/vault.py check                 every rule
    python scripts/vault.py check --rule backlink report one rule (prefix match)
    python scripts/vault.py check --changed       only files touched vs HEAD
    python scripts/vault.py check --list-rules    what it knows how to check

Exit code is 1 when anything is reported, so a pre-commit hook can use it.

Read-only. This file never writes to the vault; `fix` lands separately, one rule
at a time, so every generated value arrives as its own reviewable diff.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date

# Windows consoles default to cp1252 and the vault is full of emoji.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Vaults holding notes the contract applies to.
NOTE_VAULTS = ("SF_core", "SF_Agentforce", "SF_Data_360", "SF_Experience_Cloud")
# Walked for link integrity but not linted as notes.
OTHER_LIVE = ("RELEASE-RADAR", "Interview")
# Never walked at all.
SKIP_DIRS = {".git", "_archive", "node_modules", ".obsidian", ".vscode", ".claude"}
# Live files that are scaffolding, not notes.
NON_NOTE_NAMES = {
    "INDEX.md", "README.md", "PRACTICE.md", "PHASES.md",
    "CURRENCY.md", "CLAUDE.md", "REVIEW.md",
}

# Interview/ links out deliberately and never expects a return link.
# Interview/CLAUDE.md: "Link out, never restate."
ONE_WAY_VAULTS = ("Interview",)

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+?)(?:#[^)]*)?\)")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+\.md)(?:#[^)]*)?\)")
WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")
TRUSTED_DOMAINS = ("salesforce.com", "trailhead.com", "trailhead.salesforce.com")

STALE_MONTHS = 3
TODAY = date.today()


# ─────────────────────────────────────────────────────────────── model ──


@dataclass
class Finding:
    rule: str
    path: str
    line: int
    message: str

    def render(self) -> str:
        loc = f"{self.path}:{self.line}" if self.line else self.path
        return f"  {loc}\n      {self.message}"


@dataclass
class Note:
    path: str           # absolute
    rel: str            # repo-relative, forward slashes
    vault: str
    text: str
    lines: list[str]
    kind: str = "other"                 # light | dense | other
    meta: dict[str, str] = field(default_factory=dict)
    sections: dict[str, tuple[int, int]] = field(default_factory=dict)

    def section_text(self, name: str) -> str:
        if name not in self.sections:
            return ""
        a, b = self.sections[name]
        return "\n".join(self.lines[a + 1:b])

    def section_line(self, name: str) -> int:
        return self.sections[name][0] + 1 if name in self.sections else 0


def rel_of(path: str) -> str:
    return os.path.relpath(path, ROOT).replace("\\", "/")


def parse_meta_blockquote(lines: list[str]) -> dict[str, str]:
    """Metadata is a blockquote on lines 3-4. Never YAML frontmatter."""
    meta: dict[str, str] = {}
    for raw in lines[1:6]:
        if not raw.startswith(">"):
            continue
        body = raw.lstrip(">").strip()
        # The staleness line is prose, not key/value.
        if "months old" in body:
            meta["_stale_line"] = body
            continue
        for part in body.split("·"):
            if ":" not in part:
                continue
            k, _, v = part.partition(":")
            meta[k.strip()] = v.strip()
    return meta


def parse_sections(lines: list[str]) -> dict[str, tuple[int, int]]:
    """Map '## Heading' -> (heading index, index of next '## ' or EOF)."""
    heads = [i for i, l in enumerate(lines) if l.startswith("## ")]
    out: dict[str, tuple[int, int]] = {}
    for n, i in enumerate(heads):
        end = heads[n + 1] if n + 1 < len(heads) else len(lines)
        out[lines[i][3:].strip()] = (i, end)
    return out


def load_note(path: str) -> Note:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()
    rel = rel_of(path)
    note = Note(
        path=path, rel=rel, vault=rel.split("/")[0],
        text=text, lines=lines,
        meta=parse_meta_blockquote(lines),
        sections=parse_sections(lines),
    )
    if "Level" in note.meta and "Created" in note.meta:
        note.kind = "light"
    elif "Currency" in note.meta or "Phase" in note.meta:
        note.kind = "dense"
    return note


def walk_md(dirs: tuple[str, ...] | None = None) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            p = os.path.join(dirpath, name)
            r = rel_of(p)
            if dirs is not None and not r.startswith(dirs):
                continue
            out.append(p)
    return sorted(out)


def is_note_file(path: str) -> bool:
    """A live vault note. Anything under a _-prefixed folder is scaffolding."""
    rel = rel_of(path)
    parts = rel.split("/")
    return (
        rel.startswith(NOTE_VAULTS)
        and parts[-1] not in NON_NOTE_NAMES
        and not any(p.startswith("_") for p in parts)
    )


def load_all_notes() -> dict[str, Note]:
    return {p: load_note(p) for p in walk_md() if is_note_file(p)}


def months_between(then: date, now: date) -> int:
    return (now.year - then.year) * 12 + (now.month - then.month) - (now.day < then.day)


def parse_date(s: str) -> date | None:
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s or "")
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def parse_status(s: str) -> tuple[str, int] | None:
    """'🌱 3 gaps open' and '🌱 3 open' are the same value, rendered two ways."""
    s = (s or "").strip()
    if "complete" in s:
        return ("complete", 0)
    m = re.search(r"(\d+)\s+(?:gaps?\s+)?open", s)
    if m:
        return ("open", int(m.group(1)))
    if "learning" in s:
        return ("learning", 0)
    if s.startswith("⬜"):
        return ("scaffolded", 0)
    return None


def count_open_gaps(note: Note) -> int:
    return len(re.findall(r"^\s*-\s\[ \]", note.section_text("Gaps to close"), re.M))


def count_org_checks(note: Note) -> int:
    return len(re.findall(r"^\s*-\s*🚩", note.section_text("Confirm in org"), re.M))


def line_of(note: Note, needle: str) -> int:
    for i, l in enumerate(note.lines):
        if needle in l:
            return i + 1
    return 0


# ──────────────────────────────────────────────────────────────── rules ──

RULES: dict[str, callable] = {}


def rule(name: str):
    def deco(fn):
        RULES[name] = fn
        return fn
    return deco


# --- integrity ------------------------------------------------------------

@rule("link-broken")
def r_link_broken(notes, findings):
    """Every relative .md link resolves. Templates hold deliberate placeholders."""
    for path in walk_md():
        if os.path.basename(path).startswith("_"):
            continue
        note = load_note(path)
        base = os.path.dirname(path)
        for i, line in enumerate(note.lines, 1):
            for m in MD_LINK_RE.finditer(line):
                target = m.group(2)
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                if "<" in target or ">" in target:
                    continue
                resolved = os.path.normpath(os.path.join(base, target))
                if not os.path.exists(resolved):
                    findings.append(Finding(
                        "link-broken", note.rel, i,
                        f"target does not exist: {target}",
                    ))


@rule("link-wikilink")
def r_wikilink(notes, findings):
    """_note-template.md rule 8: relative markdown links only, no [[wiki links]]."""
    for path in walk_md():
        if os.path.basename(path).startswith("_"):
            continue
        note = load_note(path)
        for i, line in enumerate(note.lines, 1):
            if WIKILINK_RE.search(line) and "wiki link" not in line.lower():
                findings.append(Finding(
                    "link-wikilink", note.rel, i,
                    "wikilink syntax — the repo uses relative markdown links",
                ))


@rule("link-archive")
def r_link_archive(notes, findings):
    """CLAUDE.md: _archive/ is a quarry for facts, never a link target."""
    for path in walk_md(NOTE_VAULTS + OTHER_LIVE):
        if os.path.basename(path).startswith("_"):
            continue
        note = load_note(path)
        for i, line in enumerate(note.lines, 1):
            for m in MD_LINK_RE.finditer(line):
                if "_archive/" in m.group(2):
                    findings.append(Finding(
                        "link-archive", note.rel, i,
                        f"links into the archive: {m.group(2)}",
                    ))


@rule("link-label")
def r_link_label(notes, findings):
    """Catches labels left behind by a move, e.g. [05-release-radar/] -> RELEASE-RADAR/."""
    pathish = re.compile(r"^[0-9]{2}-[a-z0-9-]+/?$|^[A-Z][A-Za-z_-]+/$")
    for path in walk_md():
        if os.path.basename(path).startswith("_"):
            continue
        note = load_note(path)
        for i, line in enumerate(note.lines, 1):
            for m in LINK_RE.finditer(line):
                label, target = m.group(1).strip(), m.group(2)
                if target.startswith(("http", "mailto", "#")):
                    continue
                if not pathish.match(label):
                    continue
                stem = label.rstrip("/").lower()
                if stem not in target.lower().replace("\\", "/"):
                    findings.append(Finding(
                        "link-label", note.rel, i,
                        f"label {label!r} does not name its target {target!r}",
                    ))


# --- reciprocity ----------------------------------------------------------

@rule("backlink-missing")
def r_backlink(notes, findings):
    """NOTES-SYSTEM.md: every link out gets a link back, in the same edit.

    Reported, never written. The '— why you would jump there' clause is content;
    a generated one would be filler.
    """
    related: dict[str, set[str]] = {}
    for path, note in notes.items():
        base = os.path.dirname(path)
        targets = set()
        for m in MD_LINK_RE.finditer(note.section_text("Related")):
            t = os.path.normpath(os.path.join(base, m.group(2)))
            if t in notes:
                targets.add(t)
        related[path] = targets

    for src, targets in related.items():
        if notes[src].vault in ONE_WAY_VAULTS:
            continue
        for tgt in sorted(targets):
            if notes[tgt].vault in ONE_WAY_VAULTS:
                continue
            if src not in related.get(tgt, set()):
                findings.append(Finding(
                    "backlink-missing", notes[tgt].rel,
                    notes[tgt].section_line("Related"),
                    f"no return link to {notes[src].rel} (which links here) "
                    f"— add a ## Related bullet with a reason clause",
                ))


# --- derived values -------------------------------------------------------

@rule("status-derived")
def r_status(notes, findings):
    """Status counts '- [ ]' in ## Gaps to close ONLY. Org checks and labs never count."""
    for path, note in notes.items():
        if note.kind != "light":
            continue
        got = parse_status(note.meta.get("Status", ""))
        gaps = count_open_gaps(note)
        want = ("open", gaps) if gaps else ("complete", 0)
        if got != want:
            shown = "🌱 %d gaps open" % gaps if gaps else "✅ complete"
            findings.append(Finding(
                "status-derived", note.rel, line_of(note, "Status:"),
                f"Status is {note.meta.get('Status','(missing)')!r} "
                f"but {gaps} open gap(s) — should be {shown!r}",
            ))


@rule("gaps-empty-heading")
def r_gaps_empty(notes, findings):
    """When the last gap goes, the heading goes with it."""
    for path, note in notes.items():
        if "Gaps to close" in note.sections and count_open_gaps(note) == 0:
            findings.append(Finding(
                "gaps-empty-heading", note.rel, note.section_line("Gaps to close"),
                "## Gaps to close has no open gaps — delete the heading too",
            ))


@rule("stale-flag")
def r_stale(notes, findings):
    """Past 3 months a third metadata line appears; it goes the moment the note is touched."""
    for path, note in notes.items():
        if note.kind != "light":
            continue
        updated = parse_date(note.meta.get("Updated", ""))
        if not updated:
            continue
        age = months_between(updated, TODAY)
        has = "_stale_line" in note.meta
        if age >= STALE_MONTHS and not has:
            findings.append(Finding(
                "stale-flag", note.rel, 4,
                f"Updated {updated} is {age} months old — add "
                f"'> ⏳ {age} months old — recheck against release notes'",
            ))
        elif age < STALE_MONTHS and has:
            findings.append(Finding(
                "stale-flag", note.rel, 5,
                f"staleness line present but the note is only {age} months old — remove it",
            ))
        elif has:
            m = re.search(r"(\d+)\s+months old", note.meta["_stale_line"])
            if m and int(m.group(1)) != age:
                findings.append(Finding(
                    "stale-flag", note.rel, 5,
                    f"staleness line says {m.group(1)} months, actual age is {age}",
                ))


# --- indexes --------------------------------------------------------------

CELL_SPLIT = re.compile(r"(?<!\\)\|")


def split_row(line: str) -> list[str]:
    r"""Split a table row. An escaped pipe (component\|app) is content, not a cell edge."""
    return [c.strip() for c in CELL_SPLIT.split(line.strip().strip("|"))]


SEPARATOR_RE = re.compile(r"^\|[-: |]+\|\s*$")


def read_table_at(lines: list[str], header_i: int) -> tuple[list[str], list[tuple[int, list[str]]]]:
    headers = split_row(lines[header_i])
    rows = []
    i = header_i + 2  # skip the |---| separator
    while i < len(lines) and lines[i].strip().startswith("|"):
        rows.append((i + 1, split_row(lines[i])))
        i += 1
    return headers, rows


def parse_table(lines: list[str], start: int = 0) -> tuple[list[str], list[tuple[int, list[str]]]]:
    """The note table in this file: the first one with a 'Topic' column.

    An INDEX may open with prose and a '## Learning path' heading before its
    table, and may carry other tables after it (seams, backlog), so the table
    cannot be found by position — only by its header.
    """
    candidates = [
        i for i in range(start, len(lines) - 1)
        if lines[i].strip().startswith("|") and SEPARATOR_RE.match(lines[i + 1])
    ]
    for i in candidates:
        headers = split_row(lines[i])
        if "Topic" in headers:
            return read_table_at(lines, i)
    return read_table_at(lines, candidates[0]) if candidates else ([], [])


def index_files() -> list[str]:
    return [p for p in walk_md(NOTE_VAULTS) if os.path.basename(p) == "INDEX.md"]


@rule("index-row")
def r_index_row(notes, findings):
    """INDEX mirrors the note: Status, Org check count, Created and Updated."""
    for idx in index_files():
        note_idx = load_note(idx)
        rel_idx = note_idx.rel
        base = os.path.dirname(idx)
        headers, rows = parse_table(note_idx.lines, 0)
        if "Topic" not in headers:
            continue
        col = {h: n for n, h in enumerate(headers)}
        for lineno, cells in rows:
            if len(cells) != len(headers):
                continue
            m = MD_LINK_RE.search(cells[col["Topic"]])
            if not m:
                continue
            target = os.path.normpath(os.path.join(base, m.group(2)))
            note = notes.get(target)
            if note is None:
                continue

            def cell(name):
                return cells[col[name]] if name in col else None

            if (c := cell("Status")) is not None:
                got, want = parse_status(c), parse_status(note.meta.get("Status", ""))
                if want and got != want:
                    findings.append(Finding(
                        "index-row", rel_idx, lineno,
                        f"Status {c!r} does not match {note.rel} "
                        f"({note.meta.get('Status','(missing)')!r})",
                    ))
            if (c := cell("Org ✓")) is not None:
                want_n = count_org_checks(note)
                got_n = 0 if c in ("—", "-", "") else int(re.sub(r"\D", "", c) or 0)
                if got_n != want_n:
                    findings.append(Finding(
                        "index-row", rel_idx, lineno,
                        f"Org ✓ is {c!r} but {note.rel} has {want_n} "
                        f"## Confirm in org bullet(s)",
                    ))
            for field_name in ("Created", "Updated"):
                if (c := cell(field_name)) is not None and field_name in note.meta:
                    if parse_date(c) != parse_date(note.meta[field_name]):
                        findings.append(Finding(
                            "index-row", rel_idx, lineno,
                            f"{field_name} is {c!r} but {note.rel} says "
                            f"{note.meta[field_name]!r}",
                        ))
            if (c := cell("Level")) is not None and "Level" in note.meta:
                if c != note.meta["Level"]:
                    findings.append(Finding(
                        "index-row", rel_idx, lineno,
                        f"Level is {c!r} but {note.rel} says {note.meta['Level']!r}",
                    ))


@rule("index-coverage")
def r_index_coverage(notes, findings):
    """Every note has a row; every row points at a note that exists."""
    for idx in index_files():
        note_idx = load_note(idx)
        folder = os.path.dirname(idx)
        headers, rows = parse_table(note_idx.lines, 0)
        if "Topic" not in headers:
            continue
        listed = set()
        for _, cells in rows:
            if len(cells) == len(headers):
                m = MD_LINK_RE.search(cells[headers.index("Topic")])
                if m:
                    listed.add(os.path.normpath(os.path.join(folder, m.group(2))))
        here = {p for p in notes if os.path.dirname(p) == folder}
        for missing in sorted(here - listed):
            findings.append(Finding(
                "index-coverage", note_idx.rel, 0,
                f"no row for {rel_of(missing)}",
            ))


@rule("index-summary")
def r_index_summary(notes, findings):
    """The aggregate line above the table: topics, gaps open, complete, newest, oldest."""
    for idx in index_files():
        note_idx = load_note(idx)
        folder = os.path.dirname(idx)
        here = [n for p, n in notes.items() if os.path.dirname(p) == folder]
        if not here:
            continue
        for i, line in enumerate(note_idx.lines, 1):
            m = re.search(r"\*\*(\d+) topics?\*\*", line)
            if not m:
                continue
            claimed = int(m.group(1))
            if claimed != len(here):
                findings.append(Finding(
                    "index-summary", note_idx.rel, i,
                    f"claims {claimed} topics, folder holds {len(here)}",
                ))
            open_notes = [n for n in here if count_open_gaps(n) > 0]
            gaps = sum(count_open_gaps(n) for n in open_notes)
            if (g := re.search(r"(\d+) gaps? open", line)) and int(g.group(1)) != gaps:
                findings.append(Finding(
                    "index-summary", note_idx.rel, i,
                    f"claims {g.group(1)} gaps open, notes hold {gaps}",
                ))
            done = len([n for n in here if count_open_gaps(n) == 0])
            if (c := re.search(r"(\d+) complete", line)) and int(c.group(1)) != done:
                findings.append(Finding(
                    "index-summary", note_idx.rel, i,
                    f"claims {c.group(1)} complete, notes hold {done}",
                ))
            dates = [d for n in here if (d := parse_date(n.meta.get("Updated", "")))]
            created = [d for n in here if (d := parse_date(n.meta.get("Created", "")))]
            if dates and (nw := re.search(r"newest (\d{4}-\d{2}-\d{2})", line)):
                if parse_date(nw.group(1)) != max(dates):
                    findings.append(Finding(
                        "index-summary", note_idx.rel, i,
                        f"claims newest {nw.group(1)}, actual {max(dates)}",
                    ))
            if created and (od := re.search(r"oldest (\d{4}-\d{2}-\d{2})", line)):
                if parse_date(od.group(1)) != min(created):
                    findings.append(Finding(
                        "index-summary", note_idx.rel, i,
                        f"claims oldest {od.group(1)}, actual {min(created)}",
                    ))
        for i, line in enumerate(note_idx.lines, 1):
            m = re.match(r"\*\*(\d+) org checks\*\*.*?across (\d+) notes", line.strip())
            if m:
                total = sum(count_org_checks(n) for n in here)
                across = len([n for n in here if count_org_checks(n) > 0])
                if int(m.group(1)) != total or int(m.group(2)) != across:
                    findings.append(Finding(
                        "index-summary", note_idx.rel, i,
                        f"claims {m.group(1)} org checks across {m.group(2)} notes, "
                        f"actual {total} across {across}",
                    ))


@rule("readme-counts")
def r_readme_counts(notes, findings):
    """SF_core/README.md's per-area Topics column and the total below it."""
    p = os.path.join(ROOT, "SF_core", "README.md")
    if not os.path.exists(p):
        return
    readme = load_note(p)
    total = 0
    for i, line in enumerate(readme.lines, 1):
        m = re.match(r"\|\s*\[(\d{2}-[a-z0-9-]+)/\]\([^)]*\)\s*\|.*\|\s*(\d+)\s*\|\s*$", line)
        if not m:
            continue
        area, claimed = m.group(1), int(m.group(2))
        folder = os.path.join(ROOT, "SF_core", area)
        actual = len([q for q in notes if os.path.dirname(q) == folder])
        total += actual
        if claimed != actual:
            findings.append(Finding(
                "readme-counts", readme.rel, i,
                f"{area} claims {claimed} topics, folder holds {actual}",
            ))
    for i, line in enumerate(readme.lines, 1):
        m = re.search(r"\*\*(\d+) topics across (\d+) areas\.\*\*", line)
        if m and int(m.group(1)) != total:
            findings.append(Finding(
                "readme-counts", readme.rel, i,
                f"claims {m.group(1)} topics in total, areas hold {total}",
            ))


# --- format ---------------------------------------------------------------

@rule("format-length")
def r_length(notes, findings):
    """50 lines max for light notes, counted to ## Related. The footer is exempt."""
    for path, note in notes.items():
        cap = 50 if note.kind == "light" else 80
        end = note.sections.get("Related", (len(note.lines), 0))[0]
        body = len([l for l in note.lines[:end]])
        if body > cap:
            findings.append(Finding(
                "format-length", note.rel, end or len(note.lines),
                f"{body} lines to ## Related, cap is {cap}",
            ))


@rule("format-blocks")
def r_blocks(notes, findings):
    """One table max, one code block max of 12 lines — the light template only."""
    for path, note in notes.items():
        # These caps come from _note-template.md, which governs the light format.
        # The dense SF_core notes predate it and are not held to them.
        if note.kind != "light":
            continue
        tables = len(re.findall(r"^\|[-: |]+\|\s*$", note.text, re.M))
        if tables > 1:
            findings.append(Finding(
                "format-blocks", note.rel, 0,
                f"{tables} tables — the template allows one",
            ))
        fences = [i for i, l in enumerate(note.lines) if l.startswith("```")]
        if len(fences) // 2 > 1:
            findings.append(Finding(
                "format-blocks", note.rel, fences[2] + 1,
                f"{len(fences) // 2} code blocks — the template allows one",
            ))
        for a, b in zip(fences[::2], fences[1::2]):
            if b - a - 1 > 12:
                findings.append(Finding(
                    "format-blocks", note.rel, a + 1,
                    f"code block is {b - a - 1} lines, cap is 12",
                ))


@rule("format-sections")
def r_section_order(notes, findings):
    """Key points -> Gotchas -> Gaps -> Confirm in org -> Hands-on -> Related -> Sources -> History."""
    order = ["Key points", "Gotchas", "Gaps to close", "Confirm in org",
             "Hands-on", "Related", "Sources", "History"]
    rank = {n: i for i, n in enumerate(order)}
    for path, note in notes.items():
        if note.kind != "light":
            continue
        seen = [(rank[n], n, pos[0]) for n, pos in note.sections.items() if n in rank]
        seen.sort(key=lambda t: t[2])
        for (r1, n1, _), (r2, n2, l2) in zip(seen, seen[1:]):
            if r2 < r1:
                findings.append(Finding(
                    "format-sections", note.rel, l2 + 1,
                    f"## {n2} appears after ## {n1} — expected order is {' -> '.join(order)}",
                ))
                break


@rule("sources")
def r_sources(notes, findings):
    """Every source carries the date it was read. Non-Salesforce domains carry 🚩."""
    for path, note in notes.items():
        if "Sources" not in note.sections:
            continue
        a, b = note.sections["Sources"]
        for i in range(a + 1, b):
            line = note.lines[i]
            if not line.strip().startswith("-"):
                continue
            m = re.search(r"\((https?://[^)]+)\)", line)
            if not m:
                continue
            if not re.search(r"(?:read|via search)\s+\d{4}-\d{2}-\d{2}", line):
                findings.append(Finding(
                    "sources", note.rel, i + 1,
                    "no read-date — every researched fact carries the date it was read",
                ))
            host = re.sub(r"^https?://", "", m.group(1)).split("/")[0].lower()
            if not any(host.endswith(d) for d in TRUSTED_DOMAINS) and "🚩" not in line:
                findings.append(Finding(
                    "sources", note.rel, i + 1,
                    f"{host} is not a Salesforce domain — mark it 🚩",
                ))


@rule("history-tally")
def r_history(notes, findings):
    """History says what changed, never a gap count."""
    for path, note in notes.items():
        if "History" not in note.sections:
            continue
        a, b = note.sections["History"]
        for i in range(a + 1, b):
            if re.search(r"\d+\s+gaps?\s+(opened|closed)", note.lines[i], re.I):
                findings.append(Finding(
                    "history-tally", note.rel, i + 1,
                    "History carries a gap tally — say what was added or changed instead",
                ))


# --- labs -----------------------------------------------------------------

LAB_RE = re.compile(
    r"^\s*-\s\[([ x])\]\s\*\*(?P<id>[A-Z0-9]+-[A-Z0-9]+-\d{2})\*\*\s*·\s*"
    r"(?P<box>\d+)\s*min\s*·(?P<rest>.*)$"
)


def collect_labs(notes) -> dict[str, list[tuple[Note, int, re.Match]]]:
    labs = defaultdict(list)
    for path, note in notes.items():
        if "Hands-on" not in note.sections:
            continue
        a, b = note.sections["Hands-on"]
        for i in range(a + 1, b):
            m = LAB_RE.match(note.lines[i])
            if m:
                labs[m.group("id")].append((note, i + 1, m))
    return labs


@rule("lab-format")
def r_lab_format(notes, findings):
    """ID · time box · what you do · Proves:. IDs stable and never reused; nothing over 45 min."""
    labs = collect_labs(notes)
    for lab_id, places in sorted(labs.items()):
        if len(places) > 1:
            where = ", ".join(f"{n.rel}:{ln}" for n, ln, _ in places)
            findings.append(Finding(
                "lab-format", places[0][0].rel, places[0][1],
                f"lab id {lab_id} used {len(places)} times — ids are never reused ({where})",
            ))
        for note, lineno, m in places:
            # A lab needs a claim, not a bare verb. "Settles:" makes the same
            # promise for a lab whose whole point is answering an open 🚩.
            if not re.search(r"\*\*(Proves|Settles):\*\*", m.group("rest")):
                findings.append(Finding(
                    "lab-format", note.rel, lineno,
                    f"{lab_id} has no 'Proves:' or 'Settles:' — a lab needs a claim, not a verb",
                ))
            if int(m.group("box")) > 45:
                findings.append(Finding(
                    "lab-format", note.rel, lineno,
                    f"{lab_id} is boxed at {m.group('box')} min — nothing runs over 45",
                ))
    for path, note in notes.items():
        if "Hands-on" not in note.sections:
            continue
        a, b = note.sections["Hands-on"]
        n = len([1 for i in range(a + 1, b) if LAB_RE.match(note.lines[i])])
        malformed = len([
            1 for i in range(a + 1, b)
            if note.lines[i].strip().startswith("- [") and not LAB_RE.match(note.lines[i])
        ])
        if malformed:
            findings.append(Finding(
                "lab-format", note.rel, note.section_line("Hands-on"),
                f"{malformed} lab line(s) do not match "
                f"'- [ ] **<VAULT>-<TOPIC>-NN** · N min · … **Proves:** …'",
            ))
        if n and not 3 <= n <= 4:
            findings.append(Finding(
                "lab-format", note.rel, note.section_line("Hands-on"),
                f"{n} labs — the contract says 3 to 4 per note",
            ))


@rule("lab-practice-sync")
def r_practice(notes, findings):
    """Every lab has a PRACTICE row, and every row has a lab."""
    labs = collect_labs(notes)
    for vault in NOTE_VAULTS:
        pfile = os.path.join(ROOT, vault, "PRACTICE.md")
        vault_labs = {
            lid: places for lid, places in labs.items()
            if any(n.vault == vault for n, _, _ in places)
        }
        if not os.path.exists(pfile):
            if vault_labs:
                findings.append(Finding(
                    "lab-practice-sync", f"{vault}/PRACTICE.md", 0,
                    f"{len(vault_labs)} labs in {vault} have no PRACTICE.md to queue them",
                ))
            continue
        practice = load_note(pfile)
        queued = {}
        for i, line in enumerate(practice.lines, 1):
            m = re.match(r"\|\s*\d+\s*\|\s*([A-Z0-9]+-[A-Z0-9]+-\d{2})\s*\|", line)
            if m:
                queued[m.group(1)] = i
        for lid, places in sorted(vault_labs.items()):
            if lid not in queued:
                note, lineno, _ = places[0]
                findings.append(Finding(
                    "lab-practice-sync", note.rel, lineno,
                    f"{lid} is not queued in {vault}/PRACTICE.md",
                ))
        for lid, lineno in sorted(queued.items(), key=lambda kv: kv[1]):
            if lid not in labs:
                findings.append(Finding(
                    "lab-practice-sync", practice.rel, lineno,
                    f"{lid} is queued but no note defines it",
                ))
        for i, line in enumerate(practice.lines, 1):
            m = re.match(r"\*\*(\d+) labs", line.strip())
            if m and int(m.group(1)) != len(vault_labs):
                findings.append(Finding(
                    "lab-practice-sync", practice.rel, i,
                    f"claims {m.group(1)} labs, notes define {len(vault_labs)}",
                ))


# --- naming ---------------------------------------------------------------

# "Data Cloud" survives as a proper noun in product and permission names
# (Data Cloud One, Data Cloud User, Data Cloud-triggered flow). Renaming those
# would be wrong, not pedantic — so only a bare, generic use is reported.
DATA_CLOUD_BARE = re.compile(r"\bData Cloud\b(?![- ][A-Z]|-trigger)")
# Lines that are *about* the rename legitimately say the old name.
RENAME_TALK = re.compile(r"old name|renamed|formerly|used to be|was called", re.I)


@rule("naming")
def r_naming(notes, findings):
    """SF_Data_360/CLAUDE.md: the product is Data 360. Write Data 360, not Data Cloud."""
    for path, note in notes.items():
        sources = note.sections.get("Sources")
        for i, line in enumerate(note.lines, 1):
            if not DATA_CLOUD_BARE.search(line) or "Data 360" in line:
                continue
            # Source titles and link labels are quoted, not ours to rewrite.
            if sources and sources[0] < i - 1 < sources[1]:
                continue
            if re.search(r"\[[^\]]*Data Cloud[^\]]*\]|`[^`]*Data Cloud[^`]*`", line):
                continue
            if RENAME_TALK.search(line):
                continue
            findings.append(Finding(
                "naming", note.rel, i,
                "'Data Cloud' — the product is Data 360 "
                "(keep it only when naming the old name explicitly)",
            ))


# ───────────────────────────────────────────────────────────────── fix ──
#
# Only values with exactly one correct answer. Nothing here writes prose, a
# ## Related bullet, or a reason clause — those stay with you.

FIXERS: dict[str, callable] = {}


def fixer(name: str):
    def deco(fn):
        FIXERS[name] = fn
        return fn
    return deco


class Editor:
    """Line edits that keep each line's original ending (this repo is CRLF)."""

    def __init__(self, path: str):
        self.path = path
        with open(path, encoding="utf-8", newline="") as fh:
            self.raw = fh.read().splitlines(keepends=True)
        self.dirty = False

    def get(self, i: int) -> str:
        return self.raw[i].rstrip("\r\n")

    def set(self, i: int, text: str) -> None:
        body = self.get(i)
        if body == text:
            return
        self.raw[i] = text + self.raw[i][len(body):]
        self.dirty = True

    def newline(self) -> str:
        return "\r\n" if any(l.endswith("\r\n") for l in self.raw) else "\n"

    def insert(self, i: int, text: str) -> None:
        self.raw.insert(i, text + self.newline())
        self.dirty = True

    def drop(self, i: int) -> None:
        del self.raw[i]
        self.dirty = True

    def save(self) -> bool:
        if self.dirty:
            with open(self.path, "w", encoding="utf-8", newline="") as fh:
                fh.write("".join(self.raw))
        return self.dirty


def set_meta_field(ed: Editor, key: str, value: str) -> bool:
    """Replace one `Key: …` field inside the metadata blockquote, in place."""
    for i in range(min(6, len(ed.raw))):
        line = ed.get(i)
        if not line.startswith(">") or f"{key}:" not in line:
            continue
        new = re.sub(
            rf"{key}:\s*[^·\n]*?(\s*)(?=·|$)",
            lambda m: f"{key}: {value}{m.group(1)}",
            line, count=1,
        )
        ed.set(i, new)
        return True
    return False


@fixer("status-derived")
def fix_status(notes, changes):
    """Status is recomputed from the open-gap count."""
    for path, note in notes.items():
        if note.kind != "light":
            continue
        gaps = count_open_gaps(note)
        want_pair = ("open", gaps) if gaps else ("complete", 0)
        if parse_status(note.meta.get("Status", "")) == want_pair:
            continue
        shown = f"🌱 {gaps} gaps open" if gaps else "✅ complete"
        ed = Editor(path)
        if set_meta_field(ed, "Status", shown) and ed.save():
            changes.append((note.rel, f"Status -> {shown}"))


@fixer("stale-flag")
def fix_stale(notes, changes):
    """The '⏳ N months old' line is added, corrected or removed."""
    for path, note in notes.items():
        if note.kind != "light":
            continue
        updated = parse_date(note.meta.get("Updated", ""))
        if not updated:
            continue
        age = months_between(updated, TODAY)
        ed = Editor(path)
        at = next(
            (i for i in range(min(8, len(ed.raw)))
             if ed.get(i).startswith(">") and "months old" in ed.get(i)),
            None,
        )
        want = f"> ⏳ {age} months old — recheck against release notes"
        if age >= STALE_MONTHS and at is None:
            last = max(
                (i for i in range(min(6, len(ed.raw))) if ed.get(i).startswith(">")),
                default=1,
            )
            ed.insert(last + 1, want)
            changes.append((note.rel, f"added staleness line ({age} months)"))
        elif age < STALE_MONTHS and at is not None:
            ed.drop(at)
            changes.append((note.rel, "removed staleness line"))
        elif at is not None and ed.get(at) != want:
            ed.set(at, want)
            changes.append((note.rel, f"staleness line -> {age} months"))
        ed.save()


def _row_text(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


@fixer("index-row")
def fix_index_row(notes, changes):
    """INDEX Status / Org ✓ / Level / Created / Updated are copied from the note."""
    for idx in index_files():
        note_idx = load_note(idx)
        base = os.path.dirname(idx)
        headers, rows = parse_table(note_idx.lines)
        if "Topic" not in headers:
            continue
        col = {h: n for n, h in enumerate(headers)}
        ed = Editor(idx)
        for lineno, cells in rows:
            if len(cells) != len(headers):
                continue
            m = MD_LINK_RE.search(cells[col["Topic"]])
            if not m:
                continue
            note = notes.get(os.path.normpath(os.path.join(base, m.group(2))))
            if note is None:
                continue
            before = list(cells)
            if "Status" in col and (w := note.meta.get("Status")):
                if parse_status(cells[col["Status"]]) != parse_status(w):
                    gaps = count_open_gaps(note)
                    cells[col["Status"]] = f"🌱 {gaps} open" if gaps else "✅ complete"
            if "Org ✓" in col:
                n = count_org_checks(note)
                cells[col["Org ✓"]] = str(n) if n else "—"
            for f in ("Created", "Updated"):
                if f in col and f in note.meta:
                    cells[col[f]] = note.meta[f]
            if "Level" in col and "Level" in note.meta:
                cells[col["Level"]] = note.meta["Level"]
            if cells != before:
                ed.set(lineno - 1, _row_text(cells))
                changes.append((note_idx.rel, f"row {cells[0]} synced to {note.rel}"))
        ed.save()


@fixer("index-summary")
def fix_index_summary(notes, changes):
    """The '**N topics** · N gaps open · …' aggregate line is recomputed."""
    for idx in index_files():
        note_idx = load_note(idx)
        folder = os.path.dirname(idx)
        here = [n for p, n in notes.items() if os.path.dirname(p) == folder]
        if not here:
            continue
        gaps = sum(count_open_gaps(n) for n in here)
        done = len([n for n in here if count_open_gaps(n) == 0])
        upd = [d for n in here if (d := parse_date(n.meta.get("Updated", "")))]
        crt = [d for n in here if (d := parse_date(n.meta.get("Created", "")))]
        ed = Editor(idx)
        for i in range(len(ed.raw)):
            line = ed.get(i)
            if not re.search(r"\*\*\d+ topics?\*\*", line):
                continue
            new = re.sub(r"\*\*\d+ topics?\*\*", f"**{len(here)} topics**", line)
            new = re.sub(r"\d+ gaps? open", f"{gaps} gaps open", new)
            new = re.sub(r"\d+ complete", f"{done} complete", new)
            if upd:
                new = re.sub(r"newest \d{4}-\d{2}-\d{2}", f"newest {max(upd)}", new)
            if crt:
                new = re.sub(r"oldest \d{4}-\d{2}-\d{2}", f"oldest {min(crt)}", new)
            if new != line:
                ed.set(i, new)
                changes.append((note_idx.rel, "summary line recomputed"))
        for i in range(len(ed.raw)):
            line = ed.get(i)
            if not re.match(r"\*\*\d+ org checks\*\*", line.strip()):
                continue
            total = sum(count_org_checks(n) for n in here)
            across = len([n for n in here if count_org_checks(n) > 0])
            new = re.sub(r"\*\*\d+ org checks\*\*", f"**{total} org checks**", line)
            new = re.sub(r"across \d+ notes", f"across {across} notes", new)
            if new != line:
                ed.set(i, new)
                changes.append((note_idx.rel, "org-check line recomputed"))
        ed.save()


@fixer("readme-counts")
def fix_readme_counts(notes, changes):
    """SF_core/README.md's Topics column and the total below it."""
    p = os.path.join(ROOT, "SF_core", "README.md")
    if not os.path.exists(p):
        return
    ed, total = Editor(p), 0
    for i in range(len(ed.raw)):
        line = ed.get(i)
        m = re.match(r"(\|\s*\[(\d{2}-[a-z0-9-]+)/\]\([^)]*\)\s*\|.*\|\s*)(\d+)(\s*\|\s*)$", line)
        if not m:
            continue
        folder = os.path.join(ROOT, "SF_core", m.group(2))
        actual = len([q for q in notes if os.path.dirname(q) == folder])
        total += actual
        if int(m.group(3)) != actual:
            ed.set(i, f"{m.group(1)}{actual}{m.group(4)}")
            changes.append((rel_of(p), f"{m.group(2)} -> {actual} topics"))
    for i in range(len(ed.raw)):
        line = ed.get(i)
        new = re.sub(r"\*\*\d+ topics across (\d+) areas\.\*\*",
                     lambda m: f"**{total} topics across {m.group(1)} areas.**", line)
        if new != line:
            ed.set(i, new)
            changes.append((rel_of(p), f"total -> {total} topics"))
    ed.save()


# ────────────────────────────────────────────────────────────── driver ──


def changed_files() -> set[str] | None:
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
        extra = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except Exception:
        return None
    return {p.strip() for p in (out + extra).splitlines() if p.strip().endswith(".md")}


def main() -> int:
    ap = argparse.ArgumentParser(prog="vault.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    chk = sub.add_parser("check", help="report contract violations (read-only)")
    chk.add_argument("--rule", action="append", default=[],
                     help="only rules whose name starts with this (repeatable)")
    chk.add_argument("--changed", action="store_true",
                     help="only findings in files changed against HEAD")
    chk.add_argument("--list-rules", action="store_true")
    chk.add_argument("--quiet", action="store_true", help="counts only")

    fx = sub.add_parser("fix", help="rewrite derived values (never prose)")
    fx.add_argument("--rule", action="append", default=[],
                    help="only fixers whose name starts with this (repeatable)")
    fx.add_argument("--list-rules", action="store_true")
    args = ap.parse_args()

    if getattr(args, "list_rules", False):
        table = FIXERS if args.cmd == "fix" else RULES
        for name, fn in sorted(table.items()):
            doc = (fn.__doc__ or "").strip().splitlines()[0]
            print(f"  {name:<22} {doc}")
        return 0

    if args.cmd == "fix":
        chosen = sorted(
            n for n in FIXERS
            if not args.rule or any(n.startswith(r) for r in args.rule)
        )
        if not chosen:
            print(f"no fixer matches {args.rule}", file=sys.stderr)
            return 2
        changes: list[tuple[str, str]] = []
        # Notes first, then the indexes that mirror them, off freshly read notes.
        for name in [c for c in chosen if not c.startswith(("index", "readme"))]:
            FIXERS[name](load_all_notes(), changes)
        for name in [c for c in chosen if c.startswith(("index", "readme"))]:
            FIXERS[name](load_all_notes(), changes)

        if not changes:
            print("nothing to fix — every derived value already matches.")
            return 0
        by_file: dict[str, list[str]] = defaultdict(list)
        for path, what in changes:
            by_file[path].append(what)
        for path in sorted(by_file):
            print(f"  {path}")
            for what in by_file[path]:
                print(f"      {what}")
        print(f"\n{len(changes)} change(s) in {len(by_file)} file(s). "
              f"Review with `git diff` before committing.")
        return 0

    selected = sorted(
        n for n in RULES
        if not args.rule or any(n.startswith(r) for r in args.rule)
    )
    if not selected:
        print(f"no rule matches {args.rule}", file=sys.stderr)
        return 2

    notes = load_all_notes()
    findings: list[Finding] = []
    for name in selected:
        RULES[name](notes, findings)

    if args.changed:
        touched = changed_files()
        if touched is not None:
            findings = [f for f in findings if f.path in touched]

    by_rule: dict[str, list[Finding]] = defaultdict(list)
    for f in findings:
        by_rule[f.rule].append(f)

    print(f"vault check · {len(notes)} notes · {len(selected)} rules · {TODAY}")
    print()
    for name in selected:
        hits = by_rule.get(name, [])
        if not hits:
            print(f"  ok    {name}")
            continue
        print(f"  {len(hits):<5} {name}")
    print()

    if not args.quiet:
        for name in selected:
            hits = by_rule.get(name, [])
            if not hits:
                continue
            doc = (RULES[name].__doc__ or "").strip().splitlines()[0]
            print(f"── {name} ({len(hits)}) ".ljust(78, "─"))
            print(f"   {doc}\n")
            for f in sorted(hits, key=lambda x: (x.path, x.line))[:60]:
                print(f.render())
            if len(hits) > 60:
                print(f"  … {len(hits) - 60} more")
            print()

    print(f"{len(findings)} finding(s) across {len(by_rule)} rule(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
