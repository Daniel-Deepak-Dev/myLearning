#!/usr/bin/env python3
"""flashcards.py — the interview flashcard bank in Flashcards/, for Obsidian and Anki.

The bank is hand-written markdown in the Obsidian Spaced Repetition plugin's
format, so Obsidian needs no build step. This script checks it and pushes it to
Anki. The format is described in Flashcards/README.md.

    python scripts/flashcards.py check            validate the bank, print counts
    python scripts/flashcards.py ids              give every card without an ID one
    python scripts/flashcards.py export           Anki TSV files into ./cards/
    python scripts/flashcards.py sync             push to Anki through AnkiConnect
    python scripts/flashcards.py sync --dry-run   show what sync would change
    python scripts/flashcards.py sync --preset    also apply the deck-options preset

Sync is one-way, bank -> Anki, and keyed on each card's ID, so editing a card
updates the same Anki note and keeps its review history. It never touches flags,
scheduling or tags you add yourself (leech, marked, ...).

Standard library only, so it runs anywhere Python 3.9+ runs.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass, field

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(ROOT, "Flashcards")
DECK_ROOT = "Salesforce"
LEVELS = {"foundations": "Foundations", "hard": "Hard"}
AREA_KEYS = {"core", "agentforce", "data-360", "experience-cloud", "service", "sales"}

DECK_TAG_RE = re.compile(r"^#flashcards/([a-z0-9-]+)/([a-z0-9-]+)/([a-z0-9-]+)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
ID_RE = re.compile(r"\s*<!--id:([a-z0-9-]+)-->")
SR_RE = re.compile(r"\s*<!--SR:.*?-->")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
CLOZE_RE = re.compile(r"==(.+?)==")
SPECIAL = ("Hint:", "Trap:", "Exact:", "Source:")


# ───────────────────────────────────────────────────────────── model ──

@dataclass
class Card:
    file: str            # repo-relative bank file
    line: int            # 1-based line of the card's first line
    kind: str            # basic | cloze
    id: str | None
    question: list[str]  # basic: question lines; cloze: text lines
    answer: list[str]    # basic: answer lines (special lines removed)
    hint: str = ""
    trap: str = ""
    exact: str = ""
    sources: list[tuple[str, str]] = field(default_factory=list)  # (label, repo path)
    area_key: str = ""
    area: str = ""
    topic_key: str = ""
    topic: str = ""
    level_key: str = ""
    sub: str = ""
    errors: list[str] = field(default_factory=list)

    @property
    def level(self) -> str:
        return LEVELS.get(self.level_key, self.level_key)

    @property
    def deck(self) -> str:
        return "::".join([DECK_ROOT, self.area, self.topic, self.level])

    @property
    def has_code(self) -> bool:
        return any(l.lstrip().startswith("```") for l in self.question)

    @property
    def style(self) -> str:
        """kind:: tag — derived from the card's shape, never authored."""
        if self.kind == "cloze":
            return "cloze"
        if self.exact:
            return "exact"
        if self.has_code:
            return "code"
        return "scenario" if self.level_key == "hard" else "concept"


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower().replace("&", " ")).strip("-")


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT).replace("\\", "/")


def read_frontmatter(lines: list[str]) -> tuple[dict, int]:
    """Flat `key: value` frontmatter only — that is all the bank uses."""
    meta: dict = {}
    if not lines or lines[0].strip() != "---":
        return meta, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return meta, i + 1
        if ":" in lines[i]:
            k, v = lines[i].split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, 0


def note_tags(path: str) -> list[str]:
    """The `tags:` of a source note, for currency:: tags."""
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError:
        return []
    meta, _ = read_frontmatter(lines)
    raw = meta.get("tags", "")
    return [t.strip() for t in raw.strip("[]").split(",") if t.strip()]


def bank_files() -> list[str]:
    out = []
    for dirpath, _, names in os.walk(BANK):
        for n in sorted(names):
            if n.endswith(".md") and n != "README.md":
                out.append(os.path.join(dirpath, n))
    return sorted(out)


# ─────────────────────────────────────────────────────────── parsing ──

def _blocks(lines: list[str], start: int):
    """Yield (first_line_index, [lines]) for each blank-line-separated block.

    A fenced code block is consumed whole, so a blank line inside it does not
    end the block — the same rule the Spaced Repetition plugin's parser uses.
    """
    i, n = start, len(lines)
    while i < n:
        if not lines[i].strip():
            i += 1
            continue
        first, block = i, []
        while i < n and lines[i].strip():
            block.append(lines[i])
            if lines[i].lstrip().startswith("```"):
                i += 1
                while i < n and not lines[i].lstrip().startswith("```"):
                    block.append(lines[i])
                    i += 1
                if i < n:
                    block.append(lines[i])
            i += 1
        yield first, block


def _outside_code(text: str) -> str:
    return re.sub(r"`[^`]*`", "", text)


def parse_file(path: str) -> list[Card]:
    lines = open(path, encoding="utf-8").read().splitlines()
    meta, body = read_frontmatter(lines)
    area = meta.get("area", "")
    fm_topic = meta.get("topic", "")
    cards: list[Card] = []
    deck: tuple[str, str, str] | None = None
    last_h2, topic_name, sub = "", "", ""

    for first, block in _blocks(lines, body):
        head = block[0]
        if len(block) == 1 and (m := HEADING_RE.match(head)) and not DECK_TAG_RE.match(head):
            level, text = len(m.group(1)), m.group(2)
            if level == 2:
                last_h2 = text
            if deck is not None and level >= 3 and text.lower() not in LEVELS:
                sub = text
            elif level <= 3:
                sub = ""
            continue
        if len(block) == 1 and (m := DECK_TAG_RE.match(head)):
            deck = (m.group(1), m.group(2), m.group(3))
            topic_name = fm_topic or last_h2
            sub = ""
            continue

        is_basic = any(l.strip() == "?" for l in block)
        is_cloze = not is_basic and bool(CLOZE_RE.search(_outside_code(" ".join(block))))
        if not (is_basic or is_cloze):
            continue                       # prose: intros, notes to self

        clean = [SR_RE.sub("", l) for l in block if not l.strip().startswith("<!--SR:")]
        card_id = None
        if (m := ID_RE.search(clean[0])):
            card_id = m.group(1)
            clean[0] = ID_RE.sub("", clean[0])

        card = Card(file=rel(path), line=first + 1, kind="cloze" if is_cloze else "basic",
                    id=card_id, question=[], answer=[])
        if is_basic:
            sep = next(i for i, l in enumerate(clean) if l.strip() == "?")
            card.question, rest = clean[:sep], clean[sep + 1:]
        else:
            card.question, rest = [], clean
        body_lines = []
        for l in rest:
            key = next((s for s in SPECIAL if l.startswith(s)), None)
            if key is None:
                body_lines.append(l)
                continue
            value = l[len(key):].strip()
            if key in ("Hint:", "Trap:") and value:
                value = value[0].upper() + value[1:]
            if key == "Hint:":
                card.hint = value
            elif key == "Trap:":
                card.trap = value
            elif key == "Exact:":
                card.exact = value
            else:
                card.sources = [(lab, _resolve(path, tgt)) for lab, tgt in LINK_RE.findall(value)]
                if not card.sources:
                    card.errors.append("Source: line has no markdown link")
        if is_cloze:
            card.question = body_lines
        else:
            card.answer = body_lines

        if deck is None:
            card.errors.append("card appears before any #flashcards/<area>/<topic>/<level> tag line")
        else:
            card.area_key, card.topic_key, card.level_key = deck
            card.area, card.topic, card.sub = area, topic_name, sub
        cards.append(card)
    return cards


def _resolve(from_file: str, target: str) -> str:
    return rel(os.path.normpath(os.path.join(os.path.dirname(from_file), target)))


def load_bank() -> list[Card]:
    cards: list[Card] = []
    for f in bank_files():
        cards += parse_file(f)
    return cards


# ──────────────────────────────────────────────────────────── checks ──

def validate(cards: list[Card]) -> list[tuple[Card, str]]:
    problems: list[tuple[Card, str]] = []
    seen: dict[str, Card] = {}
    for c in cards:
        for e in c.errors:
            problems.append((c, e))
        if c.area_key and c.area_key not in AREA_KEYS:
            problems.append((c, f"unknown area '{c.area_key}' in deck tag; expected one of {sorted(AREA_KEYS)}"))
        if c.level_key and c.level_key not in LEVELS:
            problems.append((c, f"level must be foundations or hard, not '{c.level_key}'"))
        if not c.area or not c.topic:
            problems.append((c, "file needs `area:` frontmatter and a topic (frontmatter `topic:` or an H2)"))
        if c.id is None:
            problems.append((c, "no ID — run `python scripts/flashcards.py ids`"))
        elif c.id in seen:
            problems.append((c, f"duplicate ID {c.id} (also {seen[c.id].file}:{seen[c.id].line})"))
        else:
            seen[c.id] = c
        if not c.sources:
            problems.append((c, "no `Source:` line — every card links the note that holds the reasoning"))
        for _, p in c.sources:
            if "_archive/" in p:
                problems.append((c, f"Source links into _archive/: {p}"))
            elif not os.path.exists(os.path.join(ROOT, p.split("#")[0])):
                problems.append((c, f"Source does not exist: {p}"))
        if c.hint and c.level_key != "hard":
            problems.append((c, "`Hint:` is for Hard cards only"))
        if c.kind == "basic" and not any(l.strip() for l in c.question):
            problems.append((c, "empty question"))
        if c.kind == "basic" and not any(l.strip() for l in c.answer):
            problems.append((c, "empty answer"))
        if c.kind == "cloze":
            try:
                to_anki_cloze("\n".join(c.question))
            except ValueError as e:
                problems.append((c, str(e)))
        if c.kind == "basic" and any("::" in _outside_code(l) for l in c.question + c.answer):
            problems.append((c, "`::` outside backticks turns a line into a single-line card in Obsidian"))
    return problems


# ───────────────────────────────────────────────────── conversions ──

def to_anki_cloze(text: str) -> str:
    """Plugin cloze syntax -> Anki's. Raises ValueError on what Anki cannot express.

    ==answer==            -> {{cN::answer}}       (N counts up)
    ==answer;;hint==      -> {{cN::answer::hint}}
    ==2;;answer==         -> {{c2::answer}}       (a group: all c2 hide together)
    ==2;;answer;;hint==   -> {{c2::answer::hint}}
    """
    numbered = simple = 0
    counter = 0

    def repl(m: re.Match) -> str:
        nonlocal numbered, simple, counter
        parts = m.group(1).split(";;")
        if len(parts) == 3:
            seq, ans, hint = parts
        elif len(parts) == 2 and parts[0].isdigit():
            seq, ans, hint = parts[0], parts[1], ""
        elif len(parts) == 2:
            seq, ans, hint = "", parts[0], parts[1]
        else:
            seq, ans, hint = "", parts[0], ""
        if seq and not seq.isdigit():
            raise ValueError(f"overlapping cloze '{seq}' has no Anki equivalent — use numbered groups")
        if seq:
            numbered += 1
            n = int(seq)
        else:
            simple += 1
            counter += 1
            n = counter
        return "{{c%d::%s%s}}" % (n, ans, f"::{hint}" if hint else "")

    out = CLOZE_RE.sub(repl, text)
    if numbered and simple:
        raise ValueError("cloze mixes numbered and plain deletions — the plugin forbids that too")
    if not (numbered or simple):
        raise ValueError("cloze card has no ==deletion==")
    return out


def obsidian_uri(path: str, vault: str) -> str:
    target = path[:-3] if path.endswith(".md") else path
    return "obsidian://open?" + urllib.parse.urlencode({"vault": vault, "file": target},
                                                       quote_via=urllib.parse.quote)


def _inline(text: str, vault: str, from_file: str) -> str:
    """Escape, then apply code spans, links, bold and italic."""
    codes: list[str] = []

    def stash(m):
        codes.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    # Cloze markers survive escaping untouched: they contain no <>&".
    text = html.escape(text, quote=False)

    def link(m):
        label, target = m.group(1), m.group(2)
        if re.match(r"^[a-z]+://", target):
            href = target
        else:
            href = obsidian_uri(_resolve(os.path.join(ROOT, from_file), target), vault)
        return f'<a href="{html.escape(href)}">{label}</a>'

    text = LINK_RE.sub(link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def md_to_html(lines: list[str], vault: str, from_file: str) -> str:
    out: list[str] = []
    para: list[str] = []
    lst: list[str] = []
    lst_tag = ""
    i = 0

    def flush():
        nonlocal para, lst, lst_tag
        if para:
            out.append("<div>" + "<br>".join(para) + "</div>")
            para = []
        if lst:
            out.append(f"<{lst_tag}>" + "".join(f"<li>{x}</li>" for x in lst) + f"</{lst_tag}>")
            lst, lst_tag = [], ""

    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            flush()
            lang = line.strip()[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].lstrip().startswith("```"):
                code.append(lines[i])
                i += 1
            cls = f' class="lang-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(code))}</code></pre>")
            i += 1
            continue
        if (m := re.match(r"^\s*(?:[-*]|(\d+)\.)\s+(.*)$", line)):
            tag = "ol" if m.group(1) else "ul"
            if para or (lst and tag != lst_tag):
                flush()
            lst_tag = tag
            lst.append(_inline(m.group(2), vault, from_file))
        elif lst:
            lst[-1] += "<br>" + _inline(line.strip(), vault, from_file)
        else:
            para.append(_inline(line.strip(), vault, from_file))
        i += 1
    flush()
    return "".join(out)


# ────────────────────────────────────────────────── Anki note types ──

CARD_MODEL = "myLearning Card"
CLOZE_MODEL = "myLearning Cloze"
CARD_FIELDS = ["ID", "Front", "Back", "Hint", "Trap", "Exact",
               "Area", "AreaKey", "Topic", "Sub", "Level", "Source"]
CLOZE_FIELDS = ["ID", "Text", "Extra", "Trap",
                "Area", "AreaKey", "Topic", "Sub", "Level", "Source"]

_HEADER = (
    '<div class="crumb"><span class="area-name">{{Area}}</span> › {{Topic}}'
    '{{#Sub}} › {{Sub}}{{/Sub}}<span class="pill">{{Level}}</span></div>'
)
_OPEN = '<div class="ml area-{{text:AreaKey}} lvl-{{text:Level}}">' + _HEADER
_FOOT = (
    '{{#Trap}}<div class="trap"><b>⚠ Trap</b> {{Trap}}</div>{{/Trap}}'
    '<div class="src">📄 {{Source}}</div></div>'
)

CARD_FRONT = (
    _OPEN + '<div class="q">{{Front}}</div>'
    '{{#Hint}}<div class="hint">{{hint:Hint}}</div>{{/Hint}}'
    '{{#Exact}}<div class="exact">{{type:Exact}}</div>{{/Exact}}</div>'
)
CARD_BACK = (
    _OPEN + '<div class="q">{{Front}}</div><hr id="answer">'
    '{{#Exact}}<div class="exact">{{type:Exact}}</div>{{/Exact}}'
    '<div class="a">{{Back}}</div>' + _FOOT
)
CLOZE_FRONT = _OPEN + '<div class="q cloze-text">{{cloze:Text}}</div></div>'
CLOZE_BACK = (
    _OPEN + '<div class="q cloze-text">{{cloze:Text}}</div><hr id="answer">'
    '{{#Extra}}<div class="a">{{Extra}}</div>{{/Extra}}' + _FOOT
)

CSS = """
.card { font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 19px; line-height: 1.5; text-align: left; color: #1f2328; background: #ffffff; }
.ml { --accent: #64748b; border-left: 6px solid var(--accent); padding: 4px 4px 4px 16px;
  max-width: 760px; margin: 0 auto; }
.area-core { --accent: #2563eb; }
.area-agentforce { --accent: #7c3aed; }
.area-data-360 { --accent: #0d9488; }
.area-service { --accent: #16a34a; }
.area-sales { --accent: #ea580c; }
.area-experience-cloud { --accent: #db2777; }
.crumb { display: flex; flex-wrap: wrap; align-items: center; gap: 0 6px;
  font-size: 13px; color: #57606a; letter-spacing: .02em; margin-bottom: 14px; }
.area-name { color: var(--accent); font-weight: 700; text-transform: uppercase; }
.pill { margin-left: auto; font-size: 11px; font-weight: 700; padding: 2px 10px; border-radius: 999px;
  text-transform: uppercase; letter-spacing: .06em; color: #fff; background: #64748b; }
.lvl-Foundations .pill { background: #15803d; }
.lvl-Hard .pill { background: #b91c1c; }
.q { font-size: 21px; font-weight: 600; }
.a { margin-top: 6px; }
.a ul, .a ol { margin: 6px 0; padding-left: 22px; }
hr#answer { border: 0; border-top: 1px solid #d0d7de; margin: 16px 0; }
.hint { margin-top: 14px; font-size: 16px; }
.hint a { color: var(--accent); }
.exact { margin-top: 14px; }
.exact input { font-size: 18px; width: 100%; padding: 6px; }
.trap { margin-top: 14px; padding: 8px 12px; border-radius: 6px; font-size: 16px;
  background: #fef2f2; color: #991b1b; border-left: 4px solid #dc2626; }
.src { margin-top: 14px; font-size: 14px; color: #57606a; }
.src a, .a a { color: var(--accent); }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .88em;
  background: #eff1f3; padding: 1px 5px; border-radius: 4px; }
pre { background: #0d1117; color: #e6edf3; padding: 12px; border-radius: 8px;
  overflow-x: auto; font-size: 14px; line-height: 1.45; font-weight: 400; }
pre code { background: none; padding: 0; color: inherit; }
.cloze { font-weight: 700; color: var(--accent); }
.mobile .card, .mobile .q { font-size: 17px; }
.mobile .ml { padding-left: 10px; border-left-width: 4px; }
.card.nightMode { color: #e6edf3; background: #0d1117; }
.nightMode .crumb, .nightMode .src { color: #8b949e; }
.nightMode code { background: #262c36; }
.nightMode pre code { background: none; }
.nightMode pre { background: #161b22; border: 1px solid #30363d; }
.nightMode hr#answer { border-top-color: #30363d; }
.nightMode .trap { background: #3b1219; color: #fecaca; border-left-color: #f87171; }
.nightMode .area-core { --accent: #60a5fa; }
.nightMode .area-agentforce { --accent: #a78bfa; }
.nightMode .area-data-360 { --accent: #2dd4bf; }
.nightMode .area-service { --accent: #4ade80; }
.nightMode .area-sales { --accent: #fb923c; }
.nightMode .area-experience-cloud { --accent: #f472b6; }
""".strip()


def anki_note(c: Card, vault: str) -> dict:
    src = " · ".join(
        f'<a href="{html.escape(obsidian_uri(p, vault))}">{html.escape(lab)}</a>' for lab, p in c.sources
    )
    common = {
        "ID": c.id or "", "Trap": _inline(c.trap, vault, c.file) if c.trap else "",
        "Area": html.escape(c.area), "AreaKey": c.area_key, "Topic": html.escape(c.topic),
        "Sub": html.escape(c.sub), "Level": c.level, "Source": src,
    }
    if c.kind == "cloze":
        fields = {"Text": md_to_html([to_anki_cloze(l) for l in c.question], vault, c.file),
                  "Extra": ""}
        fields.update(common)
        model = CLOZE_MODEL
    else:
        fields = {"Front": md_to_html(c.question, vault, c.file),
                  "Back": md_to_html(c.answer, vault, c.file),
                  "Hint": _inline(c.hint, vault, c.file) if c.hint else "",
                  "Exact": html.escape(c.exact)}
        fields.update(common)
        model = CARD_MODEL
    return {"model": model, "deck": c.deck, "fields": fields, "tags": anki_tags(c)}


def anki_tags(c: Card) -> list[str]:
    tags = ["myLearning", f"area::{c.area_key}", f"topic::{c.area_key}::{c.topic_key}",
            f"level::{c.level_key}", f"kind::{c.style}"]
    if c.sub:
        tags.append(f"sub::{slug(c.sub)}")
    for _, p in c.sources:
        for t in note_tags(os.path.join(ROOT, p)):
            if t.startswith("currency-"):
                tags.append("currency::" + t[len("currency-"):])
    return sorted(set(tags))


MANAGED_TAG_PREFIXES = ("myLearning", "area::", "topic::", "sub::", "level::", "kind::", "currency::")


def is_managed(tag: str) -> bool:
    return tag.startswith(MANAGED_TAG_PREFIXES)


# ─────────────────────────────────────────────────────── AnkiConnect ──

class AnkiConnect:
    def __init__(self, url: str):
        self.url = url

    def __call__(self, action: str, **params):
        payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
        req = urllib.request.Request(self.url, payload, {"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                reply = json.load(r)
        except urllib.error.URLError as e:
            raise SystemExit(
                f"Cannot reach AnkiConnect at {self.url} ({e.reason}).\n"
                "Open Anki and check the AnkiConnect add-on is installed (code 2055492159)."
            )
        if reply.get("error"):
            raise RuntimeError(f"AnkiConnect {action}: {reply['error']}")
        return reply.get("result")

    def multi(self, actions: list[dict]) -> list:
        if not actions:
            return []
        results = self("multi", actions=[{"action": a["action"], "version": 6,
                                          "params": a.get("params", {})} for a in actions])
        for a, res in zip(actions, results):
            if isinstance(res, dict) and res.get("error"):
                raise RuntimeError(f"AnkiConnect {a['action']}: {res['error']}")
        return [r["result"] if isinstance(r, dict) and "result" in r else r for r in results]


def ensure_models(anki: AnkiConnect, dry: bool) -> None:
    specs = [
        (CARD_MODEL, CARD_FIELDS, False, "Card", CARD_FRONT, CARD_BACK),
        (CLOZE_MODEL, CLOZE_FIELDS, True, "Cloze", CLOZE_FRONT, CLOZE_BACK),
    ]
    existing = set(anki("modelNames"))
    for name, fields, is_cloze, tmpl, front, back in specs:
        if name not in existing:
            print(f"  + note type {name}")
            if not dry:
                anki("createModel", modelName=name, inOrderFields=fields, css=CSS, isCloze=is_cloze,
                     cardTemplates=[{"Name": tmpl, "Front": front, "Back": back}])
            continue
        have = anki("modelFieldNames", modelName=name)
        for f in fields:
            if f not in have:
                print(f"  + field {name}.{f}")
                if not dry:
                    anki("modelFieldAdd", modelName=name, fieldName=f, index=len(have))
                    have.append(f)
        if not dry:
            current = anki("modelTemplates", modelName=name)
            tname = next(iter(current), tmpl)
            anki("updateModelTemplates", model={"name": name, "templates": {tname: {"Front": front, "Back": back}}})
            anki("updateModelStyling", model={"name": name, "css": CSS})


def cmd_sync(args) -> int:
    cards = load_bank()
    problems = validate(cards)
    if problems:
        report(problems)
        print("\nFix these first — sync only runs on a clean bank.")
        return 1

    anki = AnkiConnect(args.url)
    version = anki("version")
    if version < 6:
        raise SystemExit(f"AnkiConnect API version {version} is too old; update the add-on.")
    dry = args.dry_run
    print(f"AnkiConnect v{version} · {len(cards)} cards in the bank" + (" · DRY RUN" if dry else ""))

    ensure_models(anki, dry)
    wanted = {c.id: anki_note(c, args.vault) for c in cards}
    decks = sorted({n["deck"] for n in wanted.values()})
    have_decks = set(anki("deckNames"))
    for d in decks:
        if d not in have_decks:
            print(f"  + deck {d}")
    if not dry:
        anki.multi([{"action": "createDeck", "params": {"deck": d}} for d in decks if d not in have_decks])

    ids = anki("findNotes", query=f'"note:{CARD_MODEL}" OR "note:{CLOZE_MODEL}"')
    infos = anki("notesInfo", notes=ids) if ids else []
    by_id = {}
    for info in infos:
        key = info["fields"].get("ID", {}).get("value", "")
        if key:
            by_id[key] = info

    card_ids = [cid for info in infos for cid in info.get("cards", [])]
    deck_of = {}
    if card_ids:
        for ci in anki("cardsInfo", cards=card_ids):
            deck_of[ci["cardId"]] = ci["deckName"]

    to_add, actions = [], []
    added = updated = moved = retagged = unchanged = 0
    for cid, note in wanted.items():
        info = by_id.get(cid)
        if info is None:
            to_add.append(note)
            continue
        if info["modelName"] != note["model"]:
            print(f"  ! {cid}: note type changed ({info['modelName']} -> {note['model']}); "
                  f"delete it in Anki and sync again to recreate it")
            continue
        changed = False
        current = {k: v["value"] for k, v in info["fields"].items()}
        diff = {k: v for k, v in note["fields"].items() if current.get(k, "") != v}
        if diff:
            actions.append({"action": "updateNoteFields",
                            "params": {"note": {"id": info["noteId"], "fields": diff}}})
            updated += 1
            changed = True
        have_tags = {t for t in info["tags"] if is_managed(t)}
        want_tags = set(note["tags"])
        if have_tags != want_tags:
            if have_tags - want_tags:
                actions.append({"action": "removeTags", "params": {
                    "notes": [info["noteId"]], "tags": " ".join(sorted(have_tags - want_tags))}})
            if want_tags - have_tags:
                actions.append({"action": "addTags", "params": {
                    "notes": [info["noteId"]], "tags": " ".join(sorted(want_tags - have_tags))}})
            retagged += 1
            changed = True
        stray = [c for c in info.get("cards", []) if deck_of.get(c) != note["deck"]]
        if stray:
            actions.append({"action": "changeDeck", "params": {"cards": stray, "deck": note["deck"]}})
            moved += 1
            changed = True
        unchanged += not changed

    if to_add:
        added = len(to_add)
        if not dry:
            result = anki("addNotes", notes=[{
                "deckName": n["deck"], "modelName": n["model"], "fields": n["fields"], "tags": n["tags"],
                "options": {"allowDuplicate": False, "duplicateScope": "collection"},
            } for n in to_add])
            failed = [n["fields"]["ID"] for n, r in zip(to_add, result or []) if r is None]
            if failed:
                print(f"  ! Anki refused {len(failed)} new notes (duplicates?): {', '.join(failed)}")
                added -= len(failed)
    if not dry:
        anki.multi(actions)

    orphans = sorted(set(by_id) - set(wanted))
    print(f"\n  added {added} · updated {updated} · re-tagged {retagged} · moved {moved} · unchanged {unchanged}")
    if orphans:
        verb = "deleting" if args.prune else "in Anki but not in the bank (keep, or rerun with --prune)"
        print(f"  {len(orphans)} orphan notes {verb}: {', '.join(orphans)}")
        if args.prune and not dry:
            anki("deleteNotes", notes=[by_id[o]["noteId"] for o in orphans])

    if args.preset:
        apply_preset(anki, decks, dry)
    return 0


PRESET_NAME = "Salesforce Interview"


def apply_preset(anki: AnkiConnect, decks: list[str], dry: bool) -> None:
    """Best effort: 10 new cards a day and leeches tagged, not suspended.

    FSRS, desired retention and Easy Days are set in Anki's deck options screen;
    AnkiConnect's deck-config actions only cover the legacy keys reliably.
    """
    parents = {DECK_ROOT}
    for d in decks:
        parts = d.split("::")
        for i in range(1, len(parts) + 1):
            parents.add("::".join(parts[:i]))
    targets = sorted(parents)
    config = anki("getDeckConfig", deck=DECK_ROOT) if DECK_ROOT in set(anki("deckNames")) else None
    print(f"\n  preset '{PRESET_NAME}' -> {len(targets)} decks" + (" (dry run)" if dry else ""))
    if dry:
        return
    if not config or config.get("name") != PRESET_NAME:
        cid = anki("cloneDeckConfigId", name=PRESET_NAME, cloneFrom=(config or {}).get("id", 1))
        anki("setDeckConfigId", decks=[DECK_ROOT], configId=cid)
        config = anki("getDeckConfig", deck=DECK_ROOT)
    config["new"]["perDay"] = 10
    config["lapse"]["leechAction"] = 1      # 1 = tag only; 0 would suspend the card
    anki("saveDeckConfig", config=config)
    anki("setDeckConfigId", decks=targets, configId=config["id"])
    print("  new cards/day = 10, leeches tagged not suspended. Set FSRS in Anki: see Flashcards/README.md")


# ──────────────────────────────────────────────────────────── export ──

def cmd_export(args) -> int:
    cards = load_bank()
    problems = validate(cards)
    if problems:
        report(problems)
        return 1
    os.makedirs(args.out, exist_ok=True)
    by_model: dict[str, list[dict]] = defaultdict(list)
    for c in cards:
        note = anki_note(c, args.vault)
        by_model[note["model"]].append(note)
    for model, notes in by_model.items():
        fields = CLOZE_FIELDS if model == CLOZE_MODEL else CARD_FIELDS
        path = os.path.join(args.out, slug(model) + ".tsv")
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write("#separator:tab\n#html:true\n")
            fh.write(f"#notetype:{model}\n#deck column:1\n#tags column:{len(fields) + 2}\n")
            for n in notes:
                row = [n["deck"]] + [n["fields"].get(f, "") for f in fields] + [" ".join(n["tags"])]
                fh.write("\t".join(re.sub(r"[\t\r\n]+", " ", v) for v in row) + "\n")
        print(f"  {len(notes):>4} notes -> {rel(path)}")
    print("Anki: File > Import. The note types must exist first — one `sync` creates them.")
    return 0


# ─────────────────────────────────────────────────────── check / ids ──

def report(problems: list[tuple[Card, str]]) -> None:
    for c, msg in problems:
        print(f"  {c.file}:{c.line}  {msg}")


def cmd_check(args) -> int:
    cards = load_bank()
    problems = validate(cards)
    report(problems)
    decks = Counter(c.deck for c in cards)
    kinds = Counter(c.style for c in cards)
    if not args.quiet:
        print(f"\n{len(cards)} cards in {len(decks)} decks")
        for d, n in sorted(decks.items()):
            print(f"  {n:>4}  {d}")
        print("  kinds: " + ", ".join(f"{k} {n}" for k, n in sorted(kinds.items())))
    if problems:
        print(f"\n{len(problems)} problem(s).")
    return 1 if problems else 0


def cmd_ids(args) -> int:
    changed = 0
    taken = {c.id for c in load_bank() if c.id}
    for path in bank_files():
        lines = open(path, encoding="utf-8").read().splitlines()
        meta, _ = read_frontmatter(lines)
        prefix = meta.get("id_prefix")
        missing = [c for c in parse_file(path) if c.id is None]
        if not missing:
            continue
        if not prefix:
            print(f"  {rel(path)}: needs `id_prefix:` in its frontmatter")
            continue
        nums = [int(t.rsplit("-", 1)[1]) for t in taken if t.startswith(prefix + "-") and t.rsplit("-", 1)[1].isdigit()]
        nxt = max(nums, default=0) + 1
        for c in missing:
            new = f"{prefix}-{nxt:03d}"
            lines[c.line - 1] = lines[c.line - 1].rstrip() + f" <!--id:{new}-->"
            taken.add(new)
            nxt += 1
            changed += 1
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"  {rel(path)}: {len(missing)} new ID(s)")
    print(f"{changed} ID(s) assigned.")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    ck = sub.add_parser("check", help="validate the bank")
    ck.add_argument("--quiet", action="store_true")
    sub.add_parser("ids", help="assign IDs to cards that have none")
    vault_default = os.path.basename(ROOT)
    for name in ("export", "sync"):
        sp = sub.add_parser(name)
        sp.add_argument("--vault", default=vault_default,
                        help=f"Obsidian vault name for Source links (default: {vault_default})")
        if name == "export":
            sp.add_argument("--out", default=os.path.join(ROOT, "cards"))
        else:
            sp.add_argument("--url", default="http://127.0.0.1:8765")
            sp.add_argument("--dry-run", action="store_true")
            sp.add_argument("--prune", action="store_true", help="delete Anki notes no longer in the bank")
            sp.add_argument("--preset", action="store_true", help=f"apply the '{PRESET_NAME}' deck options")
    args = p.parse_args(argv)
    return {"check": cmd_check, "ids": cmd_ids, "export": cmd_export, "sync": cmd_sync}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
