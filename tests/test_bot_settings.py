import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
SETTINGS_MODULE_EXISTS = importlib.util.find_spec("bot.settings") is not None


class BotSettingsTests(unittest.TestCase):
    def test_settings_module_exists(self):
        self.assertTrue(SETTINGS_MODULE_EXISTS)

    @unittest.skipUnless(SETTINGS_MODULE_EXISTS, "bot.settings is not implemented yet")
    def test_settings_load_from_explicit_project_env(self):
        from bot.settings import load_bot_settings

        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "TELEGRAM_BOT_TOKEN=test-token\n"
                "WEBAPP_URL=http://localhost:8000/app/\n",
                encoding="utf-8",
            )
            old_cwd = Path.cwd()
            try:
                os.chdir("/")
                settings = load_bot_settings(env_path=env_path, environ={})
            finally:
                os.chdir(old_cwd)

        self.assertEqual(settings.token, "test-token")
        self.assertEqual(settings.webapp_url, "http://localhost:8000/app/")

    @unittest.skipUnless(SETTINGS_MODULE_EXISTS, "bot.settings is not implemented yet")
    def test_settings_reject_placeholders(self):
        from bot.settings import BotConfigError, load_bot_settings

        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here\n"
                "WEBAPP_URL=https://your-domain.com/app/\n",
                encoding="utf-8",
            )

            with self.assertRaises(BotConfigError):
                load_bot_settings(env_path=env_path, environ={})


if __name__ == "__main__":
    unittest.main()
