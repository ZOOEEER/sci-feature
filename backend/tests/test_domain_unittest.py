import unittest

from app.papers import normalize_doi, normalize_title


class PaperNormalizationTests(unittest.TestCase):
    def test_normalize_title(self) -> None:
        self.assertEqual(normalize_title("  A Study   ON  Alloy Catalysts "), "a study on alloy catalysts")

    def test_normalize_doi(self) -> None:
        self.assertEqual(normalize_doi(" 10.1000/ABC "), "10.1000/abc")
        self.assertIsNone(normalize_doi("    "))
        self.assertIsNone(normalize_doi(None))
from app.domain import DuplicatePaperError, PaperStore


class PaperStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = PaperStore()

    def test_add_and_list_paper(self) -> None:
        created = self.store.add_paper(
            title="Catalytic Pathways in CO2 Reduction",
            doi="10.1000/example-1",
            year=2024,
            tags=["catalysis"],
        )

        items = self.store.list_papers()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].id, created.id)
        self.assertEqual(items[0].title, "Catalytic Pathways in CO2 Reduction")

    def test_duplicate_by_doi_is_blocked(self) -> None:
        self.store.add_paper(title="Paper A", doi="10.1000/dup")
        with self.assertRaises(DuplicatePaperError):
            self.store.add_paper(title="Paper B", doi="10.1000/dup")

    def test_duplicate_by_title_is_blocked_case_insensitive(self) -> None:
        self.store.add_paper(title="A Study On Alloy Catalysts")
        with self.assertRaises(DuplicatePaperError):
            self.store.add_paper(title="a study   on   alloy catalysts")


if __name__ == "__main__":
    unittest.main()
