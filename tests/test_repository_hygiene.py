import subprocess
import unittest
from pathlib import Path

from dotenv import dotenv_values


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class RepositoryHygieneTests(unittest.TestCase):
    def test_local_env_is_not_tracked(self):
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", ".env"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)

    def test_generated_python_files_are_not_tracked(self):
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()

        generated = [
            path for path in tracked
            if "__pycache__/" in path or path.endswith((".pyc", ".pyo"))
        ]
        self.assertEqual(generated, [])

    def test_gitignore_covers_local_and_generated_files(self):
        gitignore = PROJECT_ROOT / ".gitignore"
        self.assertTrue(gitignore.exists(), ".gitignore must exist")
        patterns = gitignore.read_text(encoding="utf-8").splitlines()

        self.assertIn(".env", patterns)
        self.assertIn("__pycache__/", patterns)
        self.assertIn("*.py[cod]", patterns)

    def test_env_example_documents_all_runtime_settings(self):
        values = dotenv_values(PROJECT_ROOT / ".env.example")
        required = {
            "GNEWS_API_KEY",
            "NEWSAPI_KEY",
            "WORLDNEWS_API_KEY",
            "DEEPL_API_KEY",
            "TELEGRAM_BOT_TOKEN",
            "WEBAPP_URL",
            "HOST",
            "PORT",
            "DEBUG",
        }

        self.assertEqual(required - values.keys(), set())


if __name__ == "__main__":
    unittest.main()
