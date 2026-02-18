import importlib.util
import unittest

FASTAPI_AVAILABLE = importlib.util.find_spec("fastapi") is not None
HTTPX_AVAILABLE = importlib.util.find_spec("httpx") is not None
API_TEST_DEPS_AVAILABLE = FASTAPI_AVAILABLE and HTTPX_AVAILABLE

if API_TEST_DEPS_AVAILABLE:
    from fastapi.testclient import TestClient

    from app.main import app


@unittest.skipUnless(
    API_TEST_DEPS_AVAILABLE,
    "Skipping API integration tests because fastapi/httpx are not installed in this environment.",
)
class ApiIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health(self) -> None:
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"status": "ok"})

    def test_create_and_list_paper(self) -> None:
        payload = {
            "title": "A review of catalytic pathways",
            "doi": "10.1000/example",
            "year": 2024,
            "tags": ["catalysis", "review"],
            "source": "manual",
        }

        create_resp = self.client.post("/api/papers", json=payload)
        self.assertEqual(create_resp.status_code, 201)
        created = create_resp.json()
        self.assertEqual(created["title"], payload["title"])

        list_resp = self.client.get("/api/papers")
        self.assertEqual(list_resp.status_code, 200)
        items = list_resp.json()
        self.assertTrue(any(item["id"] == created["id"] for item in items))


if __name__ == "__main__":
    unittest.main(verbosity=2)
