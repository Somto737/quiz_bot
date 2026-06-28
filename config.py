"""
config.py
---------
Central configuration for QuizBot.

All values are read from environment variables (or a .env file via
python-dotenv). Sensible defaults are provided for everything except
``BOT_TOKEN``, which must be set explicitly.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Required
# ---------------------------------------------------------------------------

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
"""Telegram Bot API token obtained from @BotFather. **Must be set.**"""

# ---------------------------------------------------------------------------
# Optional (with defaults)
# ---------------------------------------------------------------------------

DATABASE_PATH: str = os.getenv("DATABASE_PATH", "quiz_bot.db")
"""Filesystem path to the SQLite database file."""

QUESTIONS_PER_GAME: int = int(os.getenv("QUESTIONS_PER_GAME", "10"))
"""Number of questions per quiz game."""
