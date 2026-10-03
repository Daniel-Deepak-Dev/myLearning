#!/usr/bin/env python3
"""vault.py — the mechanical half of the notes contract.

NOTES-SYSTEM.md is the normative source. Everything this script checks is a rule
written there that a machine can decide without judgement. Anything needing a
reading of the prose stays with you and the study-notes skill.

    python scripts/vault.py check                 every rule
    python scripts/vault.py check --rule backlink report one rule (prefix match)
    python scripts/vault.py check --changed       only files touched vs HEAD
    python scripts/vault.py check --list-rules    what it knows how to check
    python scripts/vault.py home                  rebuild HOME.md and every RECALL.md
    python scripts/vault.py today                 write today's session into journal/

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
NOTE_VAULTS = ("SF_core", "SF_Agentforce", "SF_Data_360", "SF_Experience_Cloud", "SF_Service", "SF_Sales")
# Walked for link integrity but not linted as notes.
OTHER_LIVE = ("RELEASE-RADAR", "Interview", "Claude_Code")
# Never walked at all.
SKIP_DIRS = {".git", "_archive", "node_modules", ".obsidian", ".vscode", ".claude"}
# Live files that are scaffolding, not notes.
NON_NOTE_NAMES = {
    "INDEX.md", "README.md", "PRACTICE.md", "PHASES.md",
    "CURRENCY.md", "AGENTS.md", "REVIEW.md", "RECALL.md",
}

# Interview/ links out deliberately and never expects a return link.
# Interview/AGENTS.md: "Link out, never restate."
ONE_WAY_VAULTS = ("Interview",)

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+?)(?:#[^)]*)?\)")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+\.md)(?:#[^)]*)?\)")
WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")
TRUSTED_DOMAINS = ("salesforce.com", "trailhead.com", "trailhead.salesforce.com")

STALE_MONTHS = 3

# The flashcard bank lives in Flashcards/ and has its own tool; vault.py only
# counts it for HOME.md and runs its check as one more rule.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flashcards import load_bank, validate as validate_bank  # noqa: E402

# Bank area key for each vault, for HOME.md's per-vault card count.
VAULT_AREA = {
    "SF_core": "core", "SF_Agentforce": "agentforce", "SF_Data_360": "data-360",
    "SF_Experience_Cloud": "experience-cloud", "SF_Service": "service", "SF_Sales": "sales",
}
TODAY = date.today()

# Tags the tool owns, derived from the ⚠️ / 🆕 flags curated on INDEX rows.
MACHINE_TAGS = {"currency-warning", "currency-new"}

# The controlled vocabulary. Folders express product and area; tags express the
# themes that cut across them. Kept short on purpose — a tag list that sprawls
# stops being a filter and becomes noise. Add here first, then use.
ALLOWED_TAGS = MACHINE_TAGS | {
    "governor-limits", "security", "sharing", "api-67", "licensing",
    "retirement", "performance", "testing", "deployment", "integration",
    "async", "bulkification", "trust-layer", "grounding", "guest-access",
}


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
    meta: dict = field(default_factory=dict)
    sections: dict[str, tuple[int, int]] = field(default_factory=dict)
    body_start: int = 0                 # first line after the frontmatter block

    def section_text(self, name: str) -> str:
        if name not in self.sections:
            return ""
        a, b = self.sections[name]
        return "\n".join(self.lines[a + 1:b])

    def section_line(self, name: str) -> int:
        return self.sections[name][0] + 1 if name in self.sections else 0


def rel_of(path: str) -> str:
    return os.path.relpath(path, ROOT).replace("\\", "/")


# ─────────────────────────────────────────────────────── metadata I/O ──
#
# Metadata is YAML frontmatter. Obsidian reads it as Properties, which is what
# makes Bases views, property search and sorting possible. The legacy `>`
# blockquote reader below is kept only so `migrate` can read what it replaces.

# Emitted in this order so every note's frontmatter reads the same way.
FM_ORDER = [
    "vault", "area", "format", "level", "status",
    "gaps", "org_checks", "labs",
    "created", "updated", "currency", "phase",
    "set", "set_total", "scenarios", "tags",
]

# Legacy blockquote key -> canonical frontmatter key.
LEGACY_KEYS = {
    "Folder": "vault", "Area": "area", "Level": "level", "Status": "status",
    "Created": "created", "Updated": "updated", "Currency": "currency",
    "Phase": "phase", "Scenarios": "scenarios",
}

# Legacy status glyph/prose -> canonical word.
STATUS_WORDS = {
    "learning": "learning", "complete": "complete",
    "not started": "not-started", "parked": "parked", "open": "open",
}

FM_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")
PLAIN_SCALAR_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _./-]*$")
YAML_RESERVED = {"yes", "no", "true", "false", "null", "on", "off", "~"}


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        body = s[1:-1]
        return body.replace('\\"', '"').replace("\\\\", "\\") if s[0] == '"' else body
    return s


def yaml_scalar(v) -> str:
    """Quote anything YAML would not read back as the string we meant."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    s = str(v)
    if s == "":
        return '""'
    if PLAIN_SCALAR_RE.match(s) and s.lower() not in YAML_RESERVED:
        return s
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_frontmatter(lines: list[str]) -> tuple[dict, int]:
    """Return (meta, body_start). ({}, 0) when the file has no frontmatter."""
    if not lines or lines[0].strip() != "---":
        return {}, 0
    close = next((i for i in range(1, len(lines))
                  if lines[i].strip() in ("---", "...")), None)
    if close is None:
        return {}, 0
    meta: dict = {}
    key = None
    for raw in lines[1:close]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.strip()
        if stripped.startswith("- ") and key:          # block-sequence item
            meta.setdefault(key, [])
            if isinstance(meta[key], list):
                meta[key].append(_unquote(stripped[2:]))
            continue
        m = FM_KEY_RE.match(raw)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "":
            meta[key] = []
        elif val.startswith("[") and val.endswith("]"):
            meta[key] = [_unquote(x) for x in val[1:-1].split(",") if x.strip()]
        else:
            meta[key] = _unquote(val)
    return meta, close + 1


def dump_frontmatter(meta: dict) -> list[str]:
    """Render meta as frontmatter lines, canonical order first."""
    out = ["---"]
    rest = [k for k in sorted(meta) if k not in FM_ORDER and not k.startswith("_")]
    for k in FM_ORDER + rest:
        if k not in meta:
            continue
        v = meta[k]
        if isinstance(v, list):
            if v:
                out.append(f"{k}: [{', '.join(yaml_scalar(x) for x in v)}]")
        else:
            out.append(f"{k}: {yaml_scalar(v)}")
    out.append("---")
    return out


def parse_meta_blockquote(lines: list[str]) -> dict[str, str]:
    """LEGACY. The pre-migration format: a `>` blockquote on lines 3-4."""
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


def legacy_to_canonical(raw: dict[str, str]) -> dict:
    """Map a blockquote dict onto the frontmatter schema."""
    meta: dict = {}
    for old, new in LEGACY_KEYS.items():
        if old in raw:
            meta[new] = raw[old]
    if "_stale_line" in raw:
        meta["_stale_line"] = raw["_stale_line"]
    if "currency" in meta:
        meta["currency"] = meta["currency"].replace("**", "").strip()
    if "phase" in meta:
        meta["phase"] = meta["phase"].lstrip("0") or "0"
    if "status" in meta:
        parsed = parse_status(meta["status"])
        if parsed:
            kind, n = parsed
            meta["status"] = STATUS_WORDS.get(kind, kind)
            if kind == "open":
                meta["gaps"] = n
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
    """Read a note in either format. Frontmatter wins where both exist."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()
    rel = rel_of(path)
    meta, body_start = parse_frontmatter(lines)
    if meta:
        kind = meta.get("format") or ("light" if "level" in meta else "dense")
    else:
        legacy = parse_meta_blockquote(lines)
        meta = legacy_to_canonical(legacy)
        # Pre-migration, kind is inferred from which keys happen to be present.
        if "Level" in legacy and "Created" in legacy:
            kind = "light"
        elif "Currency" in legacy or "Phase" in legacy:
            kind = "dense"
        else:
            kind = "other"
    return Note(
        path=path, rel=rel, vault=rel.split("/")[0],
        text=text, lines=lines, kind=kind, meta=meta,
        sections=parse_sections(lines), body_start=body_start,
    )


def note_status(note: Note) -> tuple[str, int] | None:
    """Status as (kind, gap count), whichever metadata format the note uses."""
    raw = note.meta.get("status", "")
    if not raw:
        return None
    if raw == "open":
        try:
            return ("open", int(note.meta.get("gaps") or 0))
        except (TypeError, ValueError):
            return ("open", 0)
    return parse_status(str(raw))


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


# ─────────────────────────────────────────────────────── the user's layer ──
#
# `## My recall` and `## My code` are the user's words, not Claude's. They sit
# above the reference body as its first sections, so the caps that govern the
# body never count them. NOTES-SYSTEM.md, "The recall layer".

OWN_SECTIONS = ("My recall", "My code")
RECALL_MAX = 7
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def own_lines(note: Note) -> set[int]:
    """Line indices inside the user's own sections, headings included."""
    out: set[int] = set()
    for name in OWN_SECTIONS:
        if name in note.sections:
            out.update(range(*note.sections[name]))
    return out


def recall_lines(note: Note) -> list[str]:
    """The written lines of ## My recall. The template's guidance comment is not one."""
    text = HTML_COMMENT_RE.sub("", note.section_text("My recall"))
    return [l.rstrip() for l in text.splitlines() if l.strip()]


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


@rule("flashcards-bank")
def r_flashcards(notes, findings):
    """Flashcards/README.md: IDs, deck tags and Source links. Same check as flashcards.py."""
    for card, message in validate_bank(load_bank()):
        findings.append(Finding("flashcards-bank", card.file, card.line, message))


@rule("link-wikilink")
def r_wikilink(notes, findings):
    """NOTES-SYSTEM.md: relative markdown links only, no [[wiki links]].

    GitHub and VS Code render [[x]] as literal text, and the vault holds ~5,300
    markdown links already.
    """
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
    """AGENTS.md: _archive/ is a quarry for facts, never a link target."""
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
    """NOTES-SYSTEM.md: a link that CROSSES VAULTS gets a link back, in the same edit.

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
            # Same-vault links rely on Obsidian's Backlinks panel, which shows
            # every inbound link for free. Only a crossing between vaults earns
            # a hand-written return bullet: that is the jump a reader cannot
            # guess, and the one a GitHub reader has no panel for.
            if notes[src].vault == notes[tgt].vault:
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
        got = note_status(note)
        gaps = count_open_gaps(note)
        want = ("open", gaps) if gaps else ("complete", 0)
        if got != want:
            shown = "🌱 %d gaps open" % gaps if gaps else "✅ complete"
            findings.append(Finding(
                "status-derived", note.rel, line_of(note, "Status:"),
                f"status is {note.meta.get('status','(missing)')!r} "
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


@rule("stale")
def r_stale(notes, findings):
    """Notes not updated in 3+ months. Derived from `updated` — nothing is stamped.

    This is a study signal, not a defect, so it is deliberately left out of the
    pre-commit gate. `HOME.md` surfaces the same list.
    """
    for path, note in notes.items():
        updated = parse_date(str(note.meta.get("updated", "")))
        if not updated:
            continue
        age = months_between(updated, TODAY)
        if age >= STALE_MONTHS:
            findings.append(Finding(
                "stale", note.rel, 1,
                f"last updated {updated} — {age} months old, recheck against release notes",
            ))


@rule("frontmatter-dupes")
def r_frontmatter_dupes(notes, findings):
    """No key appears twice in a frontmatter block.

    YAML takes the last value silently, so a duplicate key quietly discards
    whatever you wrote first — easy to create by hand, impossible to see.
    """
    for path, note in notes.items():
        if not note.body_start:
            continue
        seen: dict[str, int] = {}
        for i in range(1, note.body_start - 1):
            m = FM_KEY_RE.match(note.lines[i])
            if not m:
                continue
            key = m.group(1)
            if key in seen:
                findings.append(Finding(
                    "frontmatter-dupes", note.rel, i + 1,
                    f"`{key}` is set twice (also line {seen[key] + 1}) — "
                    f"YAML keeps the last one and drops the first",
                ))
            seen[key] = i


@rule("tags")
def r_tags(notes, findings):
    """Tags come from the controlled vocabulary in ALLOWED_TAGS."""
    for path, note in notes.items():
        for tag in note.meta.get("tags", []):
            if tag not in ALLOWED_TAGS:
                findings.append(Finding(
                    "tags", note.rel, 1,
                    f"`{tag}` is not in the controlled vocabulary — "
                    f"add it to ALLOWED_TAGS in scripts/vault.py first",
                ))


@rule("frontmatter")
def r_frontmatter(notes, findings):
    """Every note carries YAML frontmatter with the required keys for its format."""
    required = {"vault", "format", "status", "created", "updated"}
    for path, note in notes.items():
        if note.body_start == 0:
            findings.append(Finding(
                "frontmatter", note.rel, 1,
                "no YAML frontmatter — run `vault.py migrate`",
            ))
            continue
        for key in sorted(required - set(note.meta)):
            findings.append(Finding(
                "frontmatter", note.rel, 1, f"frontmatter is missing `{key}`",
            ))
        if (blockquote := next(
            (i for i in range(note.body_start, min(note.body_start + 8, len(note.lines)))
             if note.lines[i].startswith(">") and re.search(r"\b(Status|Area|Folder|Currency|Phase|Level|Created|Updated):", note.lines[i])),
            None,
        )) is not None:
            findings.append(Finding(
                "frontmatter", note.rel, blockquote + 1,
                "legacy metadata blockquote left behind — frontmatter is the source now",
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
                got, want = parse_status(c), note_status(note)
                if want and got != want:
                    findings.append(Finding(
                        "index-row", rel_idx, lineno,
                        f"Status {c!r} does not match {note.rel} "
                        f"({note.meta.get('status','(missing)')!r})",
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
            dates = [d for n in here if (d := parse_date(str(n.meta.get("updated", ""))))]
            created = [d for n in here if (d := parse_date(str(n.meta.get("created", ""))))]
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
    """50 lines max for light notes, counted to ## Related. The footer and the user's own sections are exempt."""
    for path, note in notes.items():
        cap = 50 if note.kind == "light" else 80
        end = note.sections.get("Related", (len(note.lines), 0))[0]
        # Frontmatter is metadata, not body — it never counts towards the cap.
        # Neither does the user's own layer: the cap governs the reference body.
        own = sum(1 for i in own_lines(note) if note.body_start <= i < end)
        body = max(0, end - note.body_start - own)
        if body > cap:
            findings.append(Finding(
                "format-length", note.rel, end or len(note.lines),
                f"{body} lines to ## Related, cap is {cap}",
            ))


@rule("format-blocks")
def r_blocks(notes, findings):
    """One table max, one code block max of 12 lines — the light template only."""
    for path, note in notes.items():
        # These caps govern the light format only (NOTES-SYSTEM.md). The dense
        # SF_core notes predate them and are not held to them.
        if note.kind != "light":
            continue
        # The user's own code is theirs at whatever length they ran it.
        own = own_lines(note)
        tables = sum(1 for i, l in enumerate(note.lines)
                     if i not in own and SEPARATOR_RE.match(l))
        if tables > 1:
            findings.append(Finding(
                "format-blocks", note.rel, 0,
                f"{tables} tables — the template allows one",
            ))
        fences = [i for i, l in enumerate(note.lines)
                  if i not in own and l.startswith("```")]
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


@rule("recall-layer")
def r_recall(notes, findings):
    """## My recall then ## My code come first; recall is at most 7 lines, no links, tables or code."""
    for path, note in notes.items():
        expected = [n for n in OWN_SECTIONS if n in note.sections]
        if not expected:
            continue
        heads = [n for _, n in sorted((a, n) for n, (a, _) in note.sections.items())]
        if heads[:len(expected)] != expected:
            findings.append(Finding(
                "recall-layer", note.rel, note.section_line(expected[0]),
                f"{' and '.join('## ' + n for n in expected)} must be the first "
                f"section(s), in that order — they are the top layer",
            ))
        if "My recall" not in note.sections:
            continue
        start = note.section_line("My recall")
        lines = recall_lines(note)
        if len(lines) > RECALL_MAX:
            findings.append(Finding(
                "recall-layer", note.rel, start,
                f"{len(lines)} recall lines, cap is {RECALL_MAX} — power words, not a summary",
            ))
        for off, line in enumerate(note.lines[start:note.sections["My recall"][1]], start + 1):
            if LINK_RE.search(line) or WIKILINK_RE.search(line):
                # RECALL.md sits in another folder, so a relative link would
                # break there; links belong in ## Related anyway.
                findings.append(Finding(
                    "recall-layer", note.rel, off,
                    "link in ## My recall — keep it to words; links go in ## Related",
                ))
            elif line.startswith("```") or SEPARATOR_RE.match(line):
                findings.append(Finding(
                    "recall-layer", note.rel, off,
                    "table or code in ## My recall — code goes in ## My code",
                ))


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
    """SF_Data_360/AGENTS.md: the product is Data 360. Write Data 360, not Data Cloud."""
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


def write_meta(path: str, updates: dict, drop: tuple[str, ...] = ()) -> list[str]:
    """Merge `updates` into a note's frontmatter and rewrite the block in place.

    The whole block is re-rendered so key order and quoting stay canonical.
    Returns the names of the keys that actually changed, or [] if nothing did.
    """
    ed = Editor(path)
    meta, body_start = parse_frontmatter([ed.get(i) for i in range(len(ed.raw))])
    if not body_start:
        return []
    before = dict(meta)
    for key in drop:
        meta.pop(key, None)
    meta.update(updates)
    if meta == before:
        return []
    for _ in range(body_start):
        ed.drop(0)
    for line in reversed(dump_frontmatter(meta)):
        ed.insert(0, line)
    ed.save()
    return sorted(k for k in set(before) | set(meta)
                  if str(before.get(k)) != str(meta.get(k)))


@fixer("derived-fields")
def fix_derived(notes, changes):
    """status, gaps, org_checks and labs are recounted from the note body.

    These four are the machine's fields. Everything else in the frontmatter —
    vault, area, format, level, created, currency, phase, tags — is yours, and
    this never touches it.
    """
    for path, note in notes.items():
        if not note.body_start:
            continue
        gaps = count_open_gaps(note)
        org = count_org_checks(note)
        labs = len([
            i for i in range(*note.sections.get("Hands-on", (0, 0)))
            if LAB_RE.match(note.lines[i])
        ]) if "Hands-on" in note.sections else 0

        updates: dict = {}
        drop: list[str] = []
        # A dense note's status is authored (learning / not-started / parked);
        # only the light format derives it from the gap count.
        if note.kind == "light":
            updates["status"] = "open" if gaps else "complete"
        for key, value in (("gaps", gaps), ("org_checks", org), ("labs", labs)):
            if value:
                updates[key] = value
            else:
                drop.append(key)

        if changed := write_meta(path, updates, tuple(drop)):
            changes.append((note.rel, "recounted " + ", ".join(changed)))


# No `stale-flag` fixer: staleness is derived from `updated` at read time
# and surfaced by the `stale` rule and HOME.md. Nothing is stamped into a
# note, so there is nothing to write back.


@fixer("tags-currency")
def fix_tags_currency(notes, changes):
    """currency-warning / currency-new mirror the ⚠️ / 🆕 flags on INDEX rows.

    Those flags are curated in the indexes, so the index is the source and the
    tag is derived. Every other tag on a note is yours and is left alone.
    """
    wanted: dict[str, set[str]] = {}
    for idx in index_files():
        note_idx = load_note(idx)
        base = os.path.dirname(idx)
        headers, rows = parse_table(note_idx.lines)
        if "Topic" not in headers:
            continue
        for _, cells in rows:
            if len(cells) != len(headers):
                continue
            cell = cells[headers.index("Topic")]
            m = MD_LINK_RE.search(cell)
            if not m:
                continue
            target = os.path.normpath(os.path.join(base, m.group(2)))
            if target not in notes:
                continue
            tags = set()
            if "⚠️" in cell:
                tags.add("currency-warning")
            if "🆕" in cell:
                tags.add("currency-new")
            wanted[target] = tags

    for path, tags in wanted.items():
        note = notes[path]
        current = list(note.meta.get("tags", []))
        merged = sorted(set(t for t in current if t not in MACHINE_TAGS) | tags)
        if merged == sorted(current):
            continue
        updates = {"tags": merged} if merged else {}
        drop = () if merged else ("tags",)
        if write_meta(path, updates, drop):
            changes.append((note.rel, f"tags -> {merged or '(none)'}"))


@fixer("practice-done")
def fix_practice_done(notes, changes):
    """The PRACTICE.md `## Done` table is rebuilt from ticked labs.

    Ticking `- [x]` in the note is the whole record. This never writes a tick
    and never removes one -- it only reflects them, so finishing a lab costs
    one click instead of an edit in two files. Any "what broke" text you have
    written is keyed by lab id and preserved.
    """
    ticked: dict[str, list[tuple[Note, re.Match]]] = defaultdict(list)
    for path, note in notes.items():
        if "Hands-on" not in note.sections:
            continue
        for i in range(*note.sections["Hands-on"]):
            m = LAB_RE.match(note.lines[i])
            if m and m.group(1) == "x":
                ticked[note.vault].append((note, m))

    for vault in NOTE_VAULTS:
        pfile = os.path.join(ROOT, vault, "PRACTICE.md")
        if not os.path.exists(pfile):
            continue
        practice = load_note(pfile)
        if "Done" not in practice.sections:
            continue
        head, tail = practice.sections["Done"]

        # Keep whatever you wrote, keyed by lab id.
        authored: dict[str, tuple[str, str]] = {}
        for i in range(head, tail):
            cells = split_row(practice.lines[i]) if practice.lines[i].strip().startswith("|") else []
            if len(cells) >= 3 and re.fullmatch(r"[A-Z0-9]+-[A-Z0-9]+-\d{2}", cells[0]):
                authored[cells[0]] = (cells[1], cells[2])

        rows = []
        for note, m in sorted(ticked.get(vault, []), key=lambda t: t[1].group("id")):
            lab = m.group("id")
            when, broke = authored.get(lab, ("—", "—"))
            rows.append(_row_text([lab, when, broke]))
        if not rows:
            rows = [_row_text(["—", "—", "—"])]

        header = ["| Lab | Date | What broke — verbatim |", "|---|---|---|"]
        start = next((i for i in range(head, tail)
                      if practice.lines[i].strip().startswith("| Lab |")), None)
        if start is None:
            continue
        end = start + 2
        while end < tail and practice.lines[end].strip().startswith("|"):
            end += 1

        if [l.rstrip() for l in practice.lines[start:end]] == header + rows:
            continue
        ed = Editor(pfile)
        for _ in range(end - start):
            ed.drop(start)
        for line in reversed(header + rows):
            ed.insert(start, line)
        if ed.save():
            changes.append((practice.rel,
                            f"Done table rebuilt from {len(ticked.get(vault, []))} ticked lab(s)"))


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
            # The INDEX renders a status as "🌱 3 open" and the note stores it
            # as status/gaps, so these are compared as values, never as strings.
            if "Status" in col and note_status(note):
                if parse_status(cells[col["Status"]]) != note_status(note):
                    gaps = count_open_gaps(note)
                    cells[col["Status"]] = f"🌱 {gaps} open" if gaps else "✅ complete"
            if "Org ✓" in col:
                n = count_org_checks(note)
                cells[col["Org ✓"]] = str(n) if n else "—"
            for column, key in (("Created", "created"), ("Updated", "updated")):
                if column in col and key in note.meta:
                    cells[col[column]] = str(note.meta[key])
            if "Level" in col and "level" in note.meta:
                cells[col["Level"]] = str(note.meta["level"])
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
        upd = [d for n in here if (d := parse_date(str(n.meta.get("updated", ""))))]
        crt = [d for n in here if (d := parse_date(str(n.meta.get("created", ""))))]
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


# ──────────────────────────────────────────────────────────────── home ──
#
# HOME.md answers one question: what do I study next? It is generated, so it
# cannot go stale the way the hand-maintained REVIEW.md did -- that file sat at
# "Sessions logged: 0" with 18 empty rows, in the one folder the rules forbid
# linking to.
#
# Its top used to be the first unblocked lab in a 189-lab queue. That was a wall,
# and none got done. It now shows the same session `today` writes: one topic.


def cmd_home() -> int:
    notes = load_all_notes()
    ticked = {
        m.group("id")
        for note in notes.values() if "Hands-on" in note.sections
        for i in range(*note.sections["Hands-on"])
        if (m := LAB_RE.match(note.lines[i])) and m.group(1) == "x"
    }
    total_labs = len(collect_labs(notes))
    bank = load_bank()

    out = [
        "---", "vault: root", "format: dashboard", "---",
        "# What to study next", "",
        "**Generated — `python scripts/vault.py home`. Do not edit by hand.**",
        "Everything below is counted from the notes, so it cannot drift.", "",
    ]

    # --- one session, not a list ----------------------------------------
    # The same pick `npm run today` writes into the journal: one area, one
    # topic, the reviews that are due and one drill.
    recall = write_recall_sheets(notes)
    s = plan_session(notes, TODAY)
    jrel = f"journal/{TODAY}.md"
    jpath = os.path.join(ROOT, jrel)
    out += ["## ▶ Today", ""]
    if os.path.exists(jpath) and not session_marker_at(jpath):
        out += [f"Your session is in [{jrel}]({jrel}). Tick each line as you do it.", ""]
    else:
        out += [f"Run `npm run today`. It writes this session into `{jrel}`, "
                f"with room to blurt before you open the note.", ""]
    if s.topic:
        out.append(f"- **{s.area}** · [{note_title(s.topic)}]({s.topic.rel}) — {s.why}")
    out += [
        f"- **Review:** {len(s.reviews)} due" + (
            " — " + ", ".join(f"[{note_title(n)}]({n.rel})" for n in s.reviews)
            if s.reviews else ""),
        f"- **Drill:** {DRILL_NAMES[s.drill]}",
    ]
    if s.learn or s.build:
        parts = [f"learn next: {s.learn[0]}"] if s.learn else []
        if s.build:
            parts.append(f"build: [{note_title(s.build[0])}]({s.build[0].rel})")
        out.append(f"- **{TRACK_TITLE}** · " + " · ".join(parts))
    out.append("")
    mine = sum(m for m, _ in recall.values())
    total = sum(t for _, t in recall.values())
    out += [f"*In your words: {mine} of {total} notes. Each vault's `RECALL.md` "
            f"collects them — linked in the table at the bottom.*", ""]

    # --- review ---------------------------------------------------------
    levels = defaultdict(lambda: defaultdict(int))
    for c in bank:
        levels[c.area][c.level] += 1
    out += ["## Review", "",
            f"**{len(bank)} flashcards** in [Flashcards/](Flashcards/README.md) — "
            "`npm run cards:sync` pushes them to Anki.", ""]
    if levels:
        out += ["| Area | Foundations | Hard |", "|---|---|---|"]
        for area in sorted(levels):
            out.append(f"| {area} | {levels[area]['Foundations']} | {levels[area]['Hard']} |")
        out.append("")

    # --- open questions --------------------------------------------------
    gapped = sorted(
        ((count_open_gaps(n), n) for n in notes.values() if count_open_gaps(n)),
        key=lambda t: -t[0],
    )
    if gapped:
        out += ["## Open gaps — research can close these", ""]
        out += [f"- **{c}** · [{n.rel}]({n.rel})" for c, n in gapped] + [""]

    orgs = sorted(
        ((count_org_checks(n), n) for n in notes.values() if count_org_checks(n)),
        key=lambda t: -t[0],
    )
    if orgs:
        out += ["## Confirm in an org — only a sandbox can close these", ""]
        out += [f"- **{c}** · [{n.rel}]({n.rel})" for c, n in orgs[:12]] + [""]

    # --- currency --------------------------------------------------------
    warn = sorted(n.rel for n in notes.values()
                  if "currency-warning" in n.meta.get("tags", []))
    new = sorted(n.rel for n in notes.values()
                 if "currency-new" in n.meta.get("tags", []))
    out += [
        "## Currency", "",
        f"**{len(warn)} notes** carry ⚠️ — the 2019–2021 answer is now wrong. "
        f"Search the vault for `tag:currency-warning`.",
        f"**{len(new)} notes** carry 🆕 — GA'd 2024–2026. `tag:currency-new`.", "",
    ]

    stale = sorted(
        (parse_date(str(n.meta.get("updated", ""))), n) for n in notes.values()
        if (d := parse_date(str(n.meta.get("updated", ""))))
        and months_between(d, TODAY) >= STALE_MONTHS
    )
    if stale:
        out += [f"**{len(stale)} notes** not updated in {STALE_MONTHS}+ months:", ""]
        out += [f"- {d} · [{n.rel}]({n.rel})" for d, n in stale[:10]] + [""]

    missing_backlinks: list[Finding] = []
    RULES["backlink-missing"](notes, missing_backlinks)
    if missing_backlinks:
        out += [
            "## Cross-vault seams missing a return link", "",
            f"**{len(missing_backlinks)}** notes are linked to from another vault "
            f"but do not link back. Each needs one `## Related` bullet with a real "
            f"reason clause — never a generated one.", "",
        ]
        by_target: dict[str, list[str]] = defaultdict(list)
        for f in missing_backlinks:
            by_target[f.path].append(f.message.split("to ")[1].split(" (")[0])
        for target in sorted(by_target)[:10]:
            srcs = ", ".join(f"`{s}`" for s in sorted(by_target[target]))
            out.append(f"- [{target}]({target}) ← {srcs}")
        if len(by_target) > 10:
            out.append(f"- … {len(by_target) - 10} more — "
                       f"`python scripts/vault.py check --rule backlink`")
        out.append("")

    out += [
        "## The vault", "",
        f"| Vault | Notes | In my words | Cards | Labs |", "|---|---|---|---|---|",
    ]
    for vault in NOTE_VAULTS:
        vn = [n for n in notes.values() if n.vault == vault]
        vc = [c for c in bank if c.area_key == VAULT_AREA[vault]]
        vl = [l for l, places in collect_labs(notes).items()
              if any(n.vault == vault for n, _, _ in places)]
        # SF_core indexes per area, so its front door is README.md.
        door = "README.md" if vault == "SF_core" else "INDEX.md"
        out.append(f"| [{vault}/]({vault}/{door}) | {len(vn)} "
                   f"| [{recall[vault][0]}]({vault}/RECALL.md) | {len(vc)} | {len(vl)} |")
    out += ["", f"*Rebuilt {TODAY}.*", ""]

    path = os.path.join(ROOT, "HOME.md")
    nl = "\r\n" if os.path.exists(path) and b"\r\n" in open(path, "rb").read() else "\n"
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(nl.join(out) + nl)
    print(f"wrote HOME.md — {len(ticked)}/{total_labs} labs, {len(bank)} flashcards, "
          f"{sum(c for c, _ in gapped)} open gaps, {sum(c for c, _ in orgs)} org checks")
    print(f"wrote {len(recall)} RECALL.md sheets — {mine} of {total} notes in your words")
    return 0


# ──────────────────────────────────────────────────── recall and today ──
#
# RECALL.md is the summary page: every note's ## My recall, in read order, one
# file per vault. `today` picks one session from the notes and the journal and
# writes it into journal/YYYY-MM-DD.md. Both are derived, so neither can drift.

VAULT_TITLE = {
    "SF_core": "Core platform", "SF_Agentforce": "Agentforce", "SF_Data_360": "Data 360",
    "SF_Experience_Cloud": "Experience Cloud", "SF_Service": "Service Cloud",
    "SF_Sales": "Sales Cloud",
}

# The interview areas `today` rotates through, one a day:
# (name, note path prefixes, interview file prefixes). Experience Cloud,
# Service and Sales are out of the rotation; add a row to bring one in.
STUDY_AREAS = (
    ("Core dev",
     ("SF_core/01-", "SF_core/02-", "SF_core/03-", "SF_core/04-", "SF_core/10-"),
     ("Interview/03-core-platform/01-", "Interview/03-core-platform/03-")),
    ("Architect",
     ("SF_core/06-", "SF_core/07-", "SF_core/08-", "SF_core/09-"),
     ("Interview/03-core-platform/02-", "Interview/04-cross-domain/")),
    ("Agentforce", ("SF_Agentforce/",), ("Interview/01-agentforce/",)),
    ("Data 360", ("SF_Data_360/",), ("Interview/02-data-360/",)),
)

# A self-paced track outside the vault contract: no cards, no rotation, no
# linting. Its README's path table orders the topics; a note exists once fed.
TRACK_DIR, TRACK_TITLE = "Claude_Code", "Claude Code"
TRACK_README = os.path.join(ROOT, TRACK_DIR, "README.md")

# Days until a studied topic comes back, by how many times it has been ticked.
REVIEW_DAYS = (3, 7, 16, 35, 75)
REVIEWS_PER_DAY = 3

# Monday is 0. Scenarios and code alternate; Friday is a story; the weekend
# reads a recall sheet with the answers covered.
DRILL_BY_WEEKDAY = ("scenario", "code", "scenario", "code", "story", "sheet", "sheet")
DRILL_NAMES = {
    "scenario": "one scenario question, out loud",
    "code": "the topic's code, from a blank file",
    "story": "one project story, out loud",
    "sheet": "one recall sheet, answers covered",
}

JOURNAL = os.path.join(ROOT, "journal")
DAILY_TEMPLATE = os.path.join(ROOT, "templates", "daily.md")
STORIES = os.path.join(ROOT, "Interview", "my-stories.md")
TICKED_RE = re.compile(r"^\s*-\s\[[xX]\]\s(.*)$")
QUESTION_RE = re.compile(r"^###\s+(Q\d+)\s*·\s*(.+?)\s*$")
STORY_FIELD_RE = re.compile(r"^-\s\*\*[^*]+:\*\*\s*(.*)$")


def write_generated(path: str, out: list[str]) -> None:
    """Write a generated file with LF endings, as .gitattributes stores them."""
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(out) + "\n")


def note_title(note: Note) -> str:
    for line in note.lines[note.body_start:]:
        if line.startswith("# "):
            return line[2:].strip()
    return os.path.splitext(os.path.basename(note.rel))[0]


def read_order(notes) -> list[Note]:
    """Every note in INDEX order: vault by vault, SF_core area by area. Unlisted notes last."""
    def key(p: str) -> tuple[int, str]:
        r = rel_of(p)
        return NOTE_VAULTS.index(r.split("/")[0]), r

    seen: set[str] = set()
    out: list[Note] = []
    for idx in sorted(index_files(), key=key):
        folder = os.path.dirname(idx)
        headers, rows = parse_table(load_note(idx).lines, 0)
        if "Topic" not in headers:
            continue
        col = headers.index("Topic")
        for _, cells in rows:
            m = MD_LINK_RE.search(cells[col]) if len(cells) > col else None
            p = os.path.normpath(os.path.join(folder, m.group(2))) if m else None
            if p in notes and p not in seen:
                seen.add(p)
                out.append(notes[p])
    out += sorted((n for p, n in notes.items() if p not in seen), key=lambda n: n.rel)
    return out


def write_recall_sheets(notes) -> dict[str, tuple[int, int]]:
    """Write <vault>/RECALL.md for every vault. Returns vault -> (in your words, notes)."""
    order = read_order(notes)
    counts: dict[str, tuple[int, int]] = {}
    for vault in NOTE_VAULTS:
        vnotes = [n for n in order if n.vault == vault]
        mine = [n for n in vnotes if recall_lines(n)]
        out = [
            "---", f"vault: {vault}", "format: recall", "---",
            f"# {VAULT_TITLE[vault]} — in my words", "",
            "**Generated from every note's `## My recall` by `npm run vault:home`. "
            "Edit the note, never this file.**",
            "Cover everything after the dash, say it out loud, then check.", "",
        ]
        area = None
        for n in mine:
            if vault == "SF_core":
                folder = n.rel.split("/")[1]
                if folder != area:
                    area = folder
                    num, _, name = folder.partition("-")
                    out += [f"## {num} · {name.replace('-', ' ').capitalize()}", ""]
            heading = "###" if vault == "SF_core" else "##"
            out += [f"{heading} [{note_title(n)}]({n.rel[len(vault) + 1:]})", ""]
            out += recall_lines(n) + [""]
        if not mine:
            out += ["*Nothing here yet.* A note appears once you write its `## My recall`. "
                    "`npm run today` brings up one topic a day.", ""]
        out += ["---", "", f"*In your words: {len(mine)} of {len(vnotes)} notes.*"]
        write_generated(os.path.join(ROOT, vault, "RECALL.md"), out)
        counts[vault] = (len(mine), len(vnotes))
    return counts


def journal_record(before: date) -> tuple[dict[str, set[date]], str]:
    """What the journal says was done: note rel -> dates its link was ticked, plus all ticked text.

    Only ticked lines count — an unticked pick is a day skipped, and it comes
    back. Files dated `before` or later are ignored, so the pick holds all day.
    """
    studied: dict[str, set[date]] = defaultdict(set)
    text: list[str] = []
    if not os.path.isdir(JOURNAL):
        return studied, ""
    for name in sorted(os.listdir(JOURNAL)):
        d = parse_date(name)
        if not name.endswith(".md") or not d or d >= before:
            continue
        with open(os.path.join(JOURNAL, name), encoding="utf-8") as fh:
            for line in fh:
                m = TICKED_RE.match(line)
                if not m:
                    continue
                text.append(m.group(1))
                for _, target in MD_LINK_RE.findall(m.group(1)):
                    studied[rel_of(os.path.normpath(os.path.join(JOURNAL, target)))].add(d)
    return studied, "\n".join(text)


def interview_questions() -> list[tuple[str, str, str, set[str]]]:
    """(file rel, Qn, title, note rels it probes) for every scenario in Interview/."""
    out = []
    for p in walk_md(("Interview/",)):
        name = os.path.basename(p)
        if name in NON_NOTE_NAMES or name.startswith("_"):
            continue
        with open(p, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        for i, line in enumerate(lines):
            m = QUESTION_RE.match(line)
            if not m:
                continue
            probes: set[str] = set()
            for nxt in lines[i + 1:i + 6]:
                if "Probes:" in nxt:
                    probes = {
                        rel_of(os.path.normpath(os.path.join(os.path.dirname(p), t)))
                        for _, t in MD_LINK_RE.findall(nxt)
                    }
                    break
            out.append((rel_of(p), m.group(1), m.group(2), probes))
    return out


def weak_answer_notes() -> list[tuple[date, str]]:
    """(date logged, note rel) for every open WEAK-ANSWERS row that names a note to re-study."""
    path = os.path.join(ROOT, "Interview", "WEAK-ANSWERS.md")
    if not os.path.exists(path):
        return []
    lines = load_note(path).lines
    start = next((i for i, l in enumerate(lines) if l.startswith("## Open")), None)
    if start is None:
        return []
    headers, rows = parse_table(lines, start)
    if "Re-study" not in headers:
        return []
    out = []
    for _, cells in rows:
        d = parse_date(cells[0]) if cells else None
        if not d or len(cells) <= headers.index("Re-study"):
            continue
        for _, t in MD_LINK_RE.findall(cells[headers.index("Re-study")]):
            rel = rel_of(os.path.normpath(os.path.join(ROOT, "Interview", t)))
            if rel.startswith(NOTE_VAULTS):
                out.append((d, rel))
    return out


def story_slots() -> list[tuple[str, bool]]:
    """(heading, filled?) for each story in Interview/my-stories.md."""
    if not os.path.exists(STORIES):
        return []
    note = load_note(STORIES)
    out = []
    for name, (a, b) in sorted(note.sections.items(), key=lambda kv: kv[1][0]):
        fields = [STORY_FIELD_RE.match(l) for l in note.lines[a + 1:b]]
        if any(fields):
            out.append((name, any(m and m.group(1).strip() for m in fields)))
    return out


def first_open_lab(note: Note) -> str | None:
    """The note's first unticked ## Hands-on lab, rendered for a session line."""
    if "Hands-on" not in note.sections:
        return None
    for line in note.lines[slice(*note.sections["Hands-on"])]:
        m = LAB_RE.match(line)
        if m and m.group(1) == " ":
            return f"**{m.group('id')}** · {m.group('box')} min ·{m.group('rest')}"
    return None


def track_notes() -> list[Note]:
    """Every fed note in the track folder. None until the first feed."""
    folder = os.path.join(ROOT, TRACK_DIR)
    if not os.path.isdir(folder):
        return []
    return [load_note(os.path.join(folder, f)) for f in sorted(os.listdir(folder))
            if f.endswith(".md") and f not in NON_NOTE_NAMES and not f.startswith("_")]


def track_path(notes: list[Note]) -> list[tuple[str, str, Note | None]]:
    """The README path table as (topic, learn from, fed note or None), in order.

    Fed notes the table does not list follow at the end, so their labs still surface.
    """
    if not os.path.exists(TRACK_README):
        return []
    by_rel = {n.rel: n for n in notes}
    headers, rows = parse_table(load_note(TRACK_README).lines, 0)
    if "Topic" not in headers:
        return []
    col = {h: headers.index(h) for h in ("Topic", "Learn from", "Note") if h in headers}
    cell = lambda cells, h: cells[col[h]] if h in col and len(cells) > col[h] else ""
    out, listed = [], set()
    for _, cells in rows:
        m = MD_LINK_RE.search(cell(cells, "Note"))
        rel = rel_of(os.path.normpath(os.path.join(ROOT, TRACK_DIR, m.group(2)))) if m else None
        note = by_rel.get(rel)
        if note:
            listed.add(note.rel)
        out.append((cell(cells, "Topic"), cell(cells, "Learn from"), note))
    out += [(note_title(n), "", n) for n in notes if n.rel not in listed]
    return out


@dataclass
class Session:
    day: date
    area: str
    area_vault: str
    topic: Note | None
    why: str
    reviews: list[Note]
    drill: str
    question: tuple[str, str, str, set[str]] | None
    lab: str | None
    story: str | None
    learn: tuple[str, str] | None = None      # track: next topic to learn, where from
    build: tuple[Note, str] | None = None     # track: next unticked lab in a fed note


def plan_session(notes, day: date) -> Session:
    """One area, one topic, the due reviews and one drill — derived, never stored."""
    studied, ticked_text = journal_record(day)
    order = read_order(notes)

    # Track notes are fed, never picked, so the day they were fed is their first study.
    track = track_notes()
    for n in track:
        fed = parse_date(str(n.meta.get("created", "")))
        if fed and fed < day:
            studied[n.rel].add(fed)

    # Reviews: notes in your words whose next spaced date has come, most overdue first.
    due = []
    for n in order + track:
        dates = studied.get(n.rel)
        if not dates or not recall_lines(n):
            continue
        wait = REVIEW_DAYS[min(len(dates), len(REVIEW_DAYS)) - 1]
        over = (day - max(dates)).days - wait
        if over >= 0:
            due.append((-over, n.rel, n))
    reviews = [n for *_, n in sorted(due)][:REVIEWS_PER_DAY]
    skip = {n.rel for n in reviews}

    area, prefixes, q_prefixes = STUDY_AREAS[day.toordinal() % len(STUDY_AREAS)]
    in_area = [n for n in order if n.rel.startswith(prefixes) and n.rel not in skip]
    by_rel = {n.rel: n for n in in_area}
    questions = interview_questions()
    asked = {r for *_, probes in questions for r in probes}
    carded = {p for c in load_bank() for _, p in c.sources}

    topic, why = None, ""
    for logged, rel in weak_answer_notes():
        if rel in by_rel and not any(d >= logged for d in studied.get(rel, ())):
            topic, why = by_rel[rel], "it is in your weak answers"
            break
    # New topics first, the ones an interview question probes ahead of the rest.
    fresh = [n for n in in_area if n.rel not in studied]
    for pool, reason in ((asked, "an interview question probes it"),
                         (carded, "a flashcard leans on it")):
        if not topic:
            topic = next((n for n in fresh if n.rel in pool), None)
            why = reason
    if not topic and fresh:
        topic, why = fresh[0], "next in read order"
    if not topic and in_area:
        topic = min(in_area, key=lambda n: max(studied[n.rel]))
        why = "studied longest ago"

    drill = DRILL_BY_WEEKDAY[day.weekday()]
    if drill == "code" and not (topic and "```" in topic.text):
        drill = "scenario"  # nothing to write from blank; say it instead
    unused = [q for q in questions if f"{q[1]} · {q[2]}" not in ticked_text]
    question = None
    if topic:
        question = next((q for q in unused if topic.rel in q[3]), None)
    if not question:
        question = next((q for q in unused if q[0].startswith(q_prefixes)), None)

    lab = first_open_lab(topic) if topic else None

    slots = story_slots()
    empty = [h for h, filled in slots if not filled]
    story = empty[0] if empty else (slots[day.toordinal() % len(slots)][0] if slots else None)

    path = track_path(track)
    learn = next(((t, src) for t, src, n in path if not n), None)
    build = next(((n, l) for _, _, n in path if n and (l := first_open_lab(n))), None)

    return Session(day, area, prefixes[0].split("/")[0], topic, why, reviews,
                   drill, question, lab, story, learn, build)


def render_session(s: Session) -> list[str]:
    """The session block that replaces the template's `<!-- today` line."""
    def link(n: Note) -> str:
        return f"[{note_title(n)}](../{n.rel})"

    out = [
        f"**{s.area} day.** Tick each line when it is done. A ticked line is the "
        f"whole record: `npm run today` reads the ticks to decide what comes back, and when.",
        "",
        "## Cards · 10 min", "",
        "- [ ] Review the cards due in Anki (`npm run cards:sync` first). "
        "Missed one? Rewrite its answer in your own words, and keep its id.",
        "",
        "## Review · 5 min", "",
    ]
    if s.reviews:
        out += ["Read only the cues. Say the rest, then check the note.", ""]
        out += [f"- [ ] {link(n)}" for n in s.reviews]
    else:
        out += ["*Nothing due.* A topic comes back 3, 7, 16, 35 and 75 days after you "
                "tick it, once it has a `## My recall`."]
    out += ["", "## Topic · 20 min", ""]
    if s.topic:
        out += [f"- [ ] {link(s.topic)} — picked because {s.why}.", "",
                "1. **Blurt** everything you remember below, before you open the note.",
                "2. Open the note. Under **Missed**, write what it had that you did not.",
                "3. Write or fix the note's `## My recall`: 3–7 lines of "
                "`**cue** — power words`, in your words only."]
        if "From my notes" in s.topic.text:
            out.append("4. Your old wording is in its `From my notes` callout. Start from that.")
    else:
        out.append("*No topic left in this area.*")
    out += ["", "### Blurt", "", "- ", "", "### Missed", "", "- ", "",
            "## Drill · 10 min", ""]

    if s.drill == "scenario" and s.question:
        rel, qid, title, _ = s.question
        source = note_title(load_note(os.path.join(ROOT, rel)))
        out.append(f"- [ ] **Scenario** · {qid} · {title} — [{source}](../{rel}). "
                   f"Answer out loud before you open the model answer, then score it on the rubric.")
    elif s.drill == "scenario" and s.topic:
        out.append(f"- [ ] **Scenario** · Explain {link(s.topic)} out loud in two minutes, "
                   f"as if an interviewer asked. Then check the note.")
    elif s.drill == "code" and s.topic:
        out.append(f"- [ ] **Code from blank** · In an empty file, write the smallest working "
                   f"example of {link(s.topic)} from memory. Compare it with the note, and keep "
                   f"the version you ran in its `## My code`.")
        if s.lab:
            out.append(f"- [ ] *With an org:* {s.lab}")
    elif s.drill == "story" and s.story:
        out.append(f"- [ ] **Story** · {s.story} — fill it in "
                   f"[my-stories.md](../Interview/my-stories.md), then say it out loud in "
                   f"under two minutes.")
    else:
        out += [f"- [ ] **Recall sheet** · Open [{VAULT_TITLE[s.area_vault]} — in my words]"
                f"(../{s.area_vault}/RECALL.md). Cover everything after the dash and say it.",
                "- [ ] **Cards** · Rewrite the answer of every card you missed this week."]
    out += ["", "Said something wrong, thin or slow? Log it under **Weak answers** and as a "
            "row in [WEAK-ANSWERS.md](../Interview/WEAK-ANSWERS.md). That row brings the "
            "topic back."]

    if os.path.exists(TRACK_README):
        out += ["", f"## {TRACK_TITLE}", ""]
        if s.learn:
            topic, source = s.learn
            out.append(f"- [ ] **Learn** · 20 min · {topic}" + (f" — {source}" if source else "")
                       + ". Then paste what you learnt and say \"I learned … today\".")
        if s.build:
            out.append(f"- [ ] **Build** · {link(s.build[0])} — {s.build[1]} "
                       f"Tick the lab in the note too.")
        if not (s.learn or s.build):
            out.append(f"*Path done — add the next topic to [{TRACK_DIR}/README.md]"
                       f"(../{TRACK_DIR}/README.md).*")
    return out


def session_marker_at(path: str) -> int | None:
    """Index of the template's `<!-- today` line, or None once the session is written."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    return next((i for i, l in enumerate(lines) if l.startswith("<!-- today")), None)


def cmd_today(day: date, dry_run: bool) -> int:
    notes = load_all_notes()
    s = plan_session(notes, day)
    block = render_session(s)
    if dry_run:
        print("\n".join(block))
        return 0

    rel = f"journal/{day}.md"
    path = os.path.join(ROOT, rel)
    # Obsidian's Daily Notes may have created the file from the template
    # already; the session goes where its `<!-- today` line is, either way.
    source = path if os.path.exists(path) else DAILY_TEMPLATE
    with open(source, encoding="utf-8") as fh:
        lines = fh.read().replace("{{date:YYYY-MM-DD}}", str(day)).splitlines()
    at = next((i for i, l in enumerate(lines) if l.startswith("<!-- today")), None)
    if at is None:
        print(f"{rel} already has today's session — open it.")
    else:
        os.makedirs(JOURNAL, exist_ok=True)
        write_generated(path, lines[:at] + block + lines[at + 1:])
        print(f"wrote {rel} — {s.area}: "
              f"{note_title(s.topic) if s.topic else 'no topic'}, "
              f"{len(s.reviews)} review(s), drill: {DRILL_NAMES[s.drill]}"
              + (f", {TRACK_TITLE}: {s.learn[0]}" if s.learn else ""))
    if day == TODAY:
        cmd_home()
    return 0


# ───────────────────────────────────────────────────────────── migrate ──

LEGACY_FIELD_RE = re.compile(
    r"^(Folder|Area|Level|Status|Created|Updated|Currency|Phase|Scenarios|Set)\b"
)
SET_RE = re.compile(r"Set\s+(\d+)\s+of\s+(\d+)")


def is_legacy_meta_line(line: str) -> bool:
    """A `>` line that is metadata, not a content blockquote."""
    if not line.startswith(">"):
        return False
    body = line.lstrip(">").strip()
    if "months old" in body:
        return True
    return any(LEGACY_FIELD_RE.match(part.strip()) for part in body.split("·"))


def git_dates(rel: str) -> tuple[str | None, str | None]:
    """(created, updated) from git history — `--follow` survives the renames."""
    def run(args):
        try:
            return subprocess.run(
                ["git"] + args, cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout.strip()
        except Exception:
            return ""
    first = run(["log", "--diff-filter=A", "--follow", "--format=%as", "--", rel])
    last = run(["log", "-1", "--format=%as", "--", rel])
    created = first.splitlines()[-1] if first else None
    return created, (last or None)


def build_meta(note: Note, legacy: dict[str, str], created, updated) -> dict:
    """Assemble frontmatter for one note from its legacy blockquote plus the body."""
    meta: dict = {"vault": note.vault}

    if note.vault == "SF_core" and "Area" in legacy:
        meta["area"] = legacy["Area"]
    elif note.vault == "Interview" and "Area" in legacy:
        meta["area"] = legacy["Area"]

    meta["format"] = note.kind if note.kind in ("light", "dense") else "dense"
    if "Level" in legacy:
        meta["level"] = legacy["Level"]

    gaps = count_open_gaps(note)
    org = count_org_checks(note)
    labs = len([
        1 for i in range(*note.sections.get("Hands-on", (0, 0)))
        if LAB_RE.match(note.lines[i])
    ]) if "Hands-on" in note.sections else 0

    # Status: derived for light notes, carried over for dense ones.
    if meta["format"] == "light":
        meta["status"] = "open" if gaps else "complete"
    else:
        parsed = parse_status(legacy.get("Status", ""))
        meta["status"] = STATUS_WORDS.get(parsed[0], parsed[0]) if parsed else "learning"

    if gaps:
        meta["gaps"] = gaps
    if org:
        meta["org_checks"] = org
    if labs:
        meta["labs"] = labs

    # An authored date always wins. Git is a backfill for the 238 notes that
    # never carried one — it must never overwrite a date you wrote by hand.
    if "Created" in legacy:
        meta["created"] = legacy["Created"]
    elif created:
        meta["created"] = created
    if "Updated" in legacy:
        meta["updated"] = legacy["Updated"]
    elif updated:
        meta["updated"] = updated

    if "Currency" in legacy:
        meta["currency"] = legacy["Currency"].replace("**", "").strip()
    if "Phase" in legacy:
        meta["phase"] = int(re.sub(r"\D", "", legacy["Phase"]) or 0)
    if "Scenarios" in legacy:
        meta["scenarios"] = int(re.sub(r"\D", "", legacy["Scenarios"]) or 0)

    # `Set 01 of 03` is a keyless token the legacy parser silently dropped.
    for raw in note.lines[1:6]:
        if raw.startswith(">") and (m := SET_RE.search(raw)):
            meta["set"], meta["set_total"] = int(m.group(1)), int(m.group(2))
            break

    # Currency flags already in the prose are the best tags the vault has.
    tags = []
    head = "\n".join(note.lines[:min(len(note.lines), 40)])
    if "⚠️" in head:
        tags.append("currency-warning")
    if "🆕" in head:
        tags.append("currency-new")
    if tags:
        meta["tags"] = tags

    return meta


def migrate_note(path: str) -> str | None:
    """Rewrite one note's metadata as frontmatter. Returns a description, or None."""
    note = load_note(path)
    if note.body_start:
        return None                                   # already migrated
    legacy = parse_meta_blockquote(note.lines)
    if not legacy:
        return None

    ed = Editor(path)
    drop = [i for i in range(min(8, len(ed.raw))) if is_legacy_meta_line(ed.get(i))]
    if not drop:
        return None

    created, updated = git_dates(note.rel)
    meta = build_meta(note, legacy, created, updated)

    for i in reversed(drop):
        ed.drop(i)
    # Collapse the blank line the blockquote left behind.
    lo = min(drop)
    while lo < len(ed.raw) and lo > 0 and ed.get(lo).strip() == "" and ed.get(lo - 1).strip() == "":
        ed.drop(lo)
    for line in reversed(dump_frontmatter(meta)):
        ed.insert(0, line)
    ed.save()
    return f"{len(meta)} keys, dropped {len(drop)} blockquote line(s)"


def cmd_migrate(only: list[str]) -> int:
    targets = [p for p in walk_md() if is_note_file(p)]
    targets += [
        p for p in walk_md(("Interview",))
        if os.path.basename(p) not in NON_NOTE_NAMES
        and not os.path.basename(p).startswith("_")
    ]
    if only:
        targets = [p for p in targets if any(o in rel_of(p) for o in only)]

    done, skipped = 0, 0
    for n, path in enumerate(sorted(targets), 1):
        result = migrate_note(path)
        if result:
            done += 1
        else:
            skipped += 1
        if n % 25 == 0 or n == len(targets):
            print(f"  {n}/{len(targets)} …", flush=True)
    print(f"\nmigrated {done}, already done or not applicable {skipped}.")
    print("Review with `git diff` before committing.")
    return 0


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

    sub.add_parser("home", help="regenerate HOME.md and every vault's RECALL.md")

    td = sub.add_parser("today", help="write today's study session into journal/YYYY-MM-DD.md")
    td.add_argument("--date", type=date.fromisoformat, default=TODAY,
                    help="plan for another day (YYYY-MM-DD) — for trying the picker")
    td.add_argument("--dry-run", action="store_true", help="print the session, write nothing")

    mg = sub.add_parser("migrate", help="one-shot: blockquote metadata -> frontmatter")
    mg.add_argument("--only", action="append", default=[],
                    help="limit to paths containing this substring (repeatable)")
    args = ap.parse_args()

    if args.cmd == "migrate":
        return cmd_migrate(args.only)

    if args.cmd == "home":
        return cmd_home()

    if args.cmd == "today":
        return cmd_today(args.date, args.dry_run)

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
