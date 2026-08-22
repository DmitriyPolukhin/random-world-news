import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

for key in ("GNEWS_API_KEY", "NEWSAPI_KEY", "WORLDNEWS_API_KEY", "DEEPL_API_KEY"):
    os.environ[key] = f"your_{key.lower()}_here"

import main  # noqa: E402


class BrokenFetcher:
    async def fetch_random_news(self):
        raise RuntimeError("private upstream detail")


class AppRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app, follow_redirects=False)
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.client.__exit__(None, None, None)

    def test_root_redirects_to_canonical_webapp(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 307)
        self.assertEqual(response.headers["location"], "/app/")

    def test_legacy_webapp_url_redirects_to_canonical_webapp(self):
        response = self.client.get("/webapp")

        self.assertEqual(response.status_code, 307)
        self.assertEqual(response.headers["location"], "/app/")

    def test_api_metadata_has_a_dedicated_route(self):
        response = self.client.get("/api")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["app"], "Random World News")

    def test_wildcard_cors_does_not_allow_credentials(self):
        response = self.client.get(
            "/api/health",
            headers={"Origin": "https://example.com"},
        )

        self.assertEqual(response.headers["access-control-allow-origin"], "*")
        self.assertNotEqual(response.headers.get("access-control-allow-credentials"), "true")

    def test_internal_errors_are_not_returned_to_clients(self):
        with (
            patch.object(main, "get_fetcher", return_value=BrokenFetcher()),
            patch.object(main.logger, "exception"),
        ):
            response = self.client.get("/api/random-news")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Internal server error"})
        self.assertNotIn("private upstream detail", response.text)


if __name__ == "__main__":
    unittest.main()
