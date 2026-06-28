"""
manager.py
----------
SQLite database layer for the quiz bot.

All reads and writes go through :class:`DatabaseManager`.
"""

import sqlite3
from typing import List

from models.user import User


class DatabaseManager:
    """Handles all persistence for the quiz bot.

    Uses a SQLite file-based database with two tables:
    ``users`` and ``game_history``.

    Args:
        db_path (str): Filesystem path to the SQLite database file.
    """

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._init_db()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        """Open and return a database connection with row-factory set."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Create tables if they do not already exist."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id       INTEGER PRIMARY KEY,
                    username      TEXT    NOT NULL DEFAULT '',
                    first_name    TEXT    NOT NULL DEFAULT '',
                    total_score   INTEGER NOT NULL DEFAULT 0,
                    games_played  INTEGER NOT NULL DEFAULT 0,
                    correct_answers INTEGER NOT NULL DEFAULT 0,
                    total_answers   INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS game_history (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id   INTEGER NOT NULL,
                    category  TEXT    NOT NULL,
                    score     INTEGER NOT NULL,
                    correct   INTEGER NOT NULL,
                    total     INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            conn.commit()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_or_create_user(
        self, user_id: int, username: str, first_name: str
    ) -> User:
        """Fetch an existing user or insert a new one.

        Args:
            user_id (int): Telegram user ID.
            username (str): Telegram @username (may be empty).
            first_name (str): Telegram first name.

        Returns:
            User: The user object populated from the database.
        """
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ).fetchone()

            if row is None:
                conn.execute(
                    "INSERT INTO users (user_id, username, first_name) "
                    "VALUES (?, ?, ?)",
                    (user_id, username, first_name),
                )
                conn.commit()
                return User(
                    user_id=user_id, username=username, first_name=first_name
                )

            return User(
                user_id=row["user_id"],
                username=row["username"],
                first_name=row["first_name"],
                total_score=row["total_score"],
                games_played=row["games_played"],
                correct_answers=row["correct_answers"],
                total_answers=row["total_answers"],
            )

    def save_game(
        self,
        user_id: int,
        category: str,
        score: int,
        correct: int,
        total: int,
    ) -> None:
        """Persist a completed game and update user aggregate stats.

        Args:
            user_id (int): The player's Telegram ID.
            category (str): The category played.
            score (int): Points scored in this game.
            correct (int): Number of correct answers.
            total (int): Total questions answered.
        """
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO game_history "
                "(user_id, category, score, correct, total) "
                "VALUES (?, ?, ?, ?, ?)",
                (user_id, category, score, correct, total),
            )
            conn.execute(
                """
                UPDATE users
                SET total_score     = total_score     + ?,
                    games_played    = games_played    + 1,
                    correct_answers = correct_answers + ?,
                    total_answers   = total_answers   + ?
                WHERE user_id = ?
                """,
                (score, correct, total, user_id),
            )
            conn.commit()

    def get_leaderboard(self, limit: int = 10) -> List[User]:
        """Return the top *limit* players ordered by total score.

        Args:
            limit (int): Maximum number of entries to return.

        Returns:
            List[User]: Players sorted descending by ``total_score``.
        """
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM users ORDER BY total_score DESC LIMIT ?",
                (limit,),
            ).fetchall()

        return [
            User(
                user_id=r["user_id"],
                username=r["username"],
                first_name=r["first_name"],
                total_score=r["total_score"],
                games_played=r["games_played"],
                correct_answers=r["correct_answers"],
                total_answers=r["total_answers"],
            )
            for r in rows
        ]
