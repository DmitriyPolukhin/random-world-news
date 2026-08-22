"""Validated configuration for the Telegram bot."""

from dataclasses import dataclass
from os import environ as process_environ
from pathlib import Path
from typing import Mapping
from urllib.parse import urlparse

from dotenv import dotenv_values


PROJECT_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


class BotConfigError(ValueError):
    """Raised when required Telegram bot settings are missing or invalid."""


@dataclass(frozen=True)
class BotSettings:
    token: str
    webapp_url: str


def _is_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    return not normalized or "your_" in normalized or "your-domain" in normalized


def _is_valid_webapp_url(value: str) -> bool:
    parsed = urlparse(value)
    if not parsed.scheme or not parsed.hostname:
        return False
    if parsed.scheme == "https":
        return True
    return parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1"}


def load_bot_settings(
    env_path: Path = PROJECT_ENV_PATH,
    environ: Mapping[str, str] | None = None,
) -> BotSettings:
    """Load settings from the project .env, overridden by process variables."""
    values = {key: value or "" for key, value in dotenv_values(env_path).items()}
    values.update(process_environ if environ is None else environ)

    token = values.get("TELEGRAM_BOT_TOKEN", "").strip()
    webapp_url = values.get("WEBAPP_URL", "").strip().rstrip("/") + "/"

    errors = []
    if _is_placeholder(token):
        errors.append("TELEGRAM_BOT_TOKEN is missing")
    if _is_placeholder(webapp_url) or not _is_valid_webapp_url(webapp_url):
        errors.append("WEBAPP_URL must be a valid HTTPS URL or a localhost URL")

    if errors:
        raise BotConfigError("; ".join(errors))

    return BotSettings(token=token, webapp_url=webapp_url)
