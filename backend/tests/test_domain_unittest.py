import unittest

from app.notes import normalize_note_text
from app.papers import normalize_doi, normalize_title


class PaperAndNoteNormalizationTests(unittest.TestCase):
    def test_normalize_title(self) -> None:
        self.assertEqual(normalize_title("  A Study   ON  Alloy Catalysts "), "a study on alloy catalysts")

    def test_normalize_doi(self) -> None:
        self.assertEqual(normalize_doi(" 10.1000/ABC "), "10.1000/abc")
        self.assertIsNone(normalize_doi("    "))
        self.assertIsNone(normalize_doi(None))

    def test_normalize_note_text(self) -> None:
        self.assertEqual(normalize_note_text("  key insight  "), "key insight")


if __name__ == "__main__":
    unittest.main()
