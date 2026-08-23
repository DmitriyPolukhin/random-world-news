import logging
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import bot.telegram_bot  # noqa: E402,F401


class BotLoggingTests(unittest.TestCase):
    def test_http_client_loggers_suppress_sensitive_request_urls(self):
        self.assertEqual(logging.getLogger("httpx").level, logging.WARNING)
        self.assertEqual(logging.getLogger("httpcore").level, logging.WARNING)


if __name__ == "__main__":
    unittest.main()
