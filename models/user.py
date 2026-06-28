"""
user.py
-------
Data model for a registered quiz-bot user.
"""

from dataclasses import dataclass, field


@dataclass
class User:
    """Represents a player stored in the database.

    Attributes:
        user_id (int): Telegram user ID (primary key).
        username (str): Telegram @username (may be empty).
        first_name (str): Telegram first name.
        total_score (int): Cumulative score across all games.
        games_played (int): Total number of completed games.
        correct_answers (int): Total correct answers given.
        total_answers (int): Total answers given (correct + wrong).
    """

    user_id: int
    username: str
    first_name: str
    total_score: int = 0
    games_played: int = 0
    correct_answers: int = 0
    total_answers: int = 0

    @property
    def accuracy(self) -> float:
        """Return the percentage of correct answers (0–100).

        Returns:
            float: Accuracy percentage, or 0.0 if no answers have been given.
        """
        if self.total_answers == 0:
            return 0.0
        return self.correct_answers / self.total_answers * 100

    @property
    def display_name(self) -> str:
        """Return the best available display name for this user."""
        return self.username or self.first_name or f"Player{self.user_id}"
