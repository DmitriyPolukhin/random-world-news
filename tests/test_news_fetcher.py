import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from news_fetcher import NewsFetcher  # noqa: E402


class NewsFetcherTests(unittest.IsolatedAsyncioTestCase):
    async def test_gnews_key_is_sent_in_header_not_query_string(self):
        captured_request = None

        def handler(request):
            nonlocal captured_request
            captured_request = request
            return httpx.Response(
                200,
                json={
                    "articles": [
                        {
                            "title": "Test article",
                            "description": "Test description",
                            "url": "https://example.com/article",
                            "image": "",
                            "source": {"name": "Test source"},
                            "publishedAt": "2026-08-22T00:00:00Z",
                        }
                    ]
                },
            )

        fetcher = NewsFetcher()
        await fetcher.client.aclose()
        fetcher.client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

        try:
            with patch.dict(os.environ, {"GNEWS_API_KEY": "test-secret"}):
                result = await fetcher._fetch_from_gnews()
        finally:
            await fetcher.close()

        self.assertIsNotNone(result)
        self.assertIsNotNone(captured_request)
        self.assertEqual(captured_request.headers.get("x-api-key"), "test-secret")
        self.assertNotIn("token", captured_request.url.params)
        self.assertNotIn("apikey", captured_request.url.params)

    async def test_worldnews_key_is_sent_in_header_not_query_string(self):
        captured_request = None

        def handler(request):
            nonlocal captured_request
            captured_request = request
            return httpx.Response(
                200,
                json={
                    "news": [
                        {
                            "title": "Test article",
                            "text": "Test description",
                            "url": "https://example.com/article",
                            "image": "",
                            "author": "Test author",
                            "publish_date": "2026-08-23 00:00:00",
                            "language": "en",
                        }
                    ]
                },
            )

        fetcher = NewsFetcher()
        await fetcher.client.aclose()
        fetcher.client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

        try:
            with patch.dict(os.environ, {"WORLDNEWS_API_KEY": "test-secret"}):
                result = await fetcher._fetch_from_worldnews()
        finally:
            await fetcher.close()

        self.assertIsNotNone(result)
        self.assertIsNotNone(captured_request)
        self.assertEqual(captured_request.headers.get("x-api-key"), "test-secret")
        self.assertNotIn("api-key", captured_request.url.params)

    async def test_newsapi_key_is_sent_in_header_not_query_string(self):
        captured_request = None

        def handler(request):
            nonlocal captured_request
            captured_request = request
            return httpx.Response(
                200,
                json={
                    "articles": [
                        {
                            "title": "Test article",
                            "description": "Test description",
                            "url": "https://example.com/article",
                            "urlToImage": "",
                            "source": {"name": "Test source"},
                            "publishedAt": "2026-08-23T00:00:00Z",
                        }
                    ]
                },
            )

        fetcher = NewsFetcher()
        await fetcher.client.aclose()
        fetcher.client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

        try:
            with patch.dict(os.environ, {"NEWSAPI_KEY": "test-secret"}):
                result = await fetcher._fetch_from_newsapi()
        finally:
            await fetcher.close()

        self.assertIsNotNone(result)
        self.assertIsNotNone(captured_request)
        self.assertEqual(captured_request.headers.get("x-api-key"), "test-secret")
        self.assertNotIn("apiKey", captured_request.url.params)


if __name__ == "__main__":
    unittest.main()
