"""English study records and journal preservation. Uses only temporary files."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import vault


class EnglishPracticeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="mylearning-english-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / "General" / "english"
        self.folder.mkdir(parents=True)
        self.journal = self.root / "journal"
        self.journal.mkdir()
        template = self.root / "daily.md"
        template.write_text(
            "# {{date:YYYY-MM-DD}}\n\n<!-- today — insert session -->\n\n"
            "## Notes\n\n- \n\n## What broke\n\n- \n", encoding="utf-8")
        readme = self.folder / "README.md"
        # Deliberately reverse alphabetical order to test the written path.
        readme.write_text(
            "# English\n\n| Topic | Note |\n|---|---|\n"
            "| Work updates | [Updates](z-updates.md) |\n"
            "| Clarification | [Questions](a-questions.md) |\n", encoding="utf-8")
        for name, title in (("z-updates.md", "Work updates"), ("a-questions.md", "Clarification")):
            (self.folder / name).write_text(
                "---\ntrack: general\ncreated: 2026-01-01\nupdated: 2026-01-01\n---\n"
                f"# {title}\n\n**One line:** Prepared practice.\n\n## My recall\n\n",
                encoding="utf-8")
        for name, value in {
            "ROOT": str(self.root), "JOURNAL": str(self.journal),
            "DAILY_TEMPLATE": str(template), "ENGLISH_README": str(readme),
            "STORIES": str(self.root / "missing-stories.md"),
        }.items():
            p = patch.object(vault, name, value)
            p.start()
            self.addCleanup(p.stop)
        for name, value in {"cmd_home": 0, "load_bank": []}.items():
            p = patch.object(vault, name, return_value=value)
            p.start()
            self.addCleanup(p.stop)
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)

    def record(self, day, text):
        path = self.journal / f"{day}.md"
        path.write_text(text, encoding="utf-8")
        return path

    def pick(self, day):
        studied, _ = vault.journal_record(day)
        return vault.pick_english(vault.general_notes(), studied, day)

    def test_prepared_dates_do_not_count_as_practice(self):
        session = vault.plan_session({}, date(2026, 1, 10))
        self.assertEqual(session.english[0].rel, "General/english/z-updates.md")
        self.assertFalse(session.reviews)
        self.assertTrue(all(not vault.recall_lines(n) for n in vault.general_notes()))

    def test_filing_and_unchecked_attempts_do_not_advance(self):
        self.record("2026-01-09", vault.ENGLISH_HEADING + "\n"
                    "- [ ] [Updates](../General/english/z-updates.md)\n"
                    "## Notes\n### Filed\n"
                    "- [x] [Updates](../General/english/z-updates.md)\n"
                    "- [x] [Other note](../SF_core/example.md)\n")
        studied, _ = vault.journal_record(date(2026, 1, 10))
        self.assertNotIn("General/english/z-updates.md", studied)
        self.assertIn("SF_core/example.md", studied)
        self.assertEqual(self.pick(date(2026, 1, 10))[0].rel, "General/english/z-updates.md")

    def test_due_review_beats_new_lesson_and_progresses_after_tick(self):
        self.record("2026-01-07", vault.ENGLISH_HEADING + "\n"
                    "- [x] [Updates](../General/english/z-updates.md)\n")
        self.assertEqual(self.pick(date(2026, 1, 9))[0].rel, "General/english/a-questions.md")
        note, why = self.pick(date(2026, 1, 10))
        self.assertEqual(note.rel, "General/english/z-updates.md")
        self.assertEqual(why, "due spoken review")
        self.record("2026-01-10", vault.ENGLISH_HEADING + "\n"
                    "- [x] [Updates](../General/english/z-updates.md)\n"
                    "- [x] [Updates again](../General/english/z-updates.md)\n")
        self.assertEqual(self.pick(date(2026, 1, 16))[0].rel, "General/english/a-questions.md")
        self.assertEqual(self.pick(date(2026, 1, 17))[0].rel, "General/english/z-updates.md")

    def test_same_day_and_future_records_do_not_change_daily_pick(self):
        self.record("2026-01-10", vault.ENGLISH_HEADING + "\n"
                    "- [x] [Updates](../General/english/z-updates.md)\n")
        self.record("2026-01-11", vault.ENGLISH_HEADING + "\n"
                    "- [x] [Questions](../General/english/a-questions.md)\n")
        self.assertEqual(self.pick(date(2026, 1, 10))[0].rel, "General/english/z-updates.md")

    def test_english_preserves_existing_notes_and_is_idempotent(self):
        original = "# 2026-01-10\n\n## Notes\n\nஎன் குறிப்புகள் — my original sentence.\n"
        path = self.record("2026-01-10", original)
        vault.cmd_english(date(2026, 1, 10), False)
        first = path.read_bytes()
        self.assertIn("## Notes\n\nஎன் குறிப்புகள் — my original sentence.", first.decode("utf-8"))
        vault.cmd_english(date(2026, 1, 10), False)
        self.assertEqual(path.read_bytes(), first)
        self.assertNotIn("- [x]", first.decode("utf-8"))

    def test_english_then_today_preserves_attempt_and_does_not_duplicate(self):
        day = date(2026, 1, 10)
        vault.cmd_english(day, False)
        path = self.journal / f"{day}.md"
        text = path.read_text(encoding="utf-8").replace("## Notes\n", "## Notes\nMy attempt stays.\n")
        path.write_text(text, encoding="utf-8")
        vault.cmd_today(day, False)
        result = path.read_text(encoding="utf-8")
        self.assertEqual(result.count(vault.ENGLISH_HEADING), 1)
        self.assertIn("My attempt stays.", result)
        self.assertIn("## Cards", result)
        first = path.read_bytes()
        vault.cmd_today(day, False)
        self.assertEqual(path.read_bytes(), first)

    def test_today_then_english_does_not_duplicate(self):
        day = date(2026, 1, 10)
        vault.cmd_today(day, False)
        path = self.journal / f"{day}.md"
        first = path.read_bytes()
        vault.cmd_english(day, False)
        self.assertEqual(path.read_bytes(), first)
        self.assertEqual(first.decode("utf-8").count(vault.ENGLISH_HEADING), 1)

    def test_today_adds_english_to_an_existing_session_without_rewriting_it(self):
        day = date(2026, 1, 10)
        path = self.record(str(day), "# My session\n\n## Notes\n\nMy original wording.\n")
        vault.cmd_today(day, False)
        result = path.read_text(encoding="utf-8")
        self.assertTrue(result.startswith("# My session\n"))
        self.assertIn("## Notes\n\nMy original wording.", result)
        self.assertEqual(result.count(vault.ENGLISH_HEADING), 1)

    def test_dry_run_writes_nothing(self):
        vault.cmd_english(date(2026, 1, 10), True)
        self.assertEqual(list(self.journal.iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
