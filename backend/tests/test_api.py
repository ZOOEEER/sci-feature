import unittest

from app.api_contract import ApiContractService


class ApiContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = ApiContractService()

    def test_health_like_create_and_list_paper_flow(self) -> None:
        status, created = self.api.create_paper(
            {
                "title": "A review of catalytic pathways",
                "doi": "10.1000/example",
                "year": 2024,
                "tags": ["catalysis", "review"],
                "source": "manual",
            }
        )
        self.assertEqual(status, 201)
        self.assertEqual(created["title"], "A review of catalytic pathways")

        list_status, papers = self.api.list_papers()
        self.assertEqual(list_status, 200)
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["id"], created["id"])

    def test_duplicate_paper_returns_conflict(self) -> None:
        self.api.create_paper({"title": "Catalysis 101", "doi": "10.1/dup", "source": "manual"})
        status, payload = self.api.create_paper(
            {"title": "Catalysis 101", "doi": "10.1/dup", "source": "manual"}
        )
        self.assertEqual(status, 409)
        self.assertEqual(payload["detail"], "Paper already exists")

    def test_create_note_and_filter_by_paper(self) -> None:
        _, paper = self.api.create_paper({"title": "Paper for Notes", "source": "manual"})

        note_status, note = self.api.create_note(
            {
                "paper_id": paper["id"],
                "research_question": "What drives selectivity?",
                "method": "DFT + experiment",
                "result": "Ligand tuning improves yield",
                "limitation": "Small sample",
                "insight": "Try bimetallic catalyst",
            }
        )
        self.assertEqual(note_status, 201)
        self.assertEqual(note["paper_id"], paper["id"])

        all_status, all_notes = self.api.list_notes()
        self.assertEqual(all_status, 200)
        self.assertEqual(len(all_notes), 1)

        filtered_status, filtered = self.api.list_notes(paper_id=paper["id"])
        self.assertEqual(filtered_status, 200)
        self.assertEqual(len(filtered), 1)

    def test_note_create_returns_404_for_missing_paper(self) -> None:
        status, payload = self.api.create_note({"paper_id": "49fb0f3e-b2a3-4b1f-bab0-bf1741ce59fd"})
        self.assertEqual(status, 404)
        self.assertEqual(payload["detail"], "Paper not found")


if __name__ == "__main__":
    unittest.main(verbosity=2)
