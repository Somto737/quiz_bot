"""
session.py
----------
Manages the state of an active quiz session for one user.
"""

from typing import List, Optional
from models.question import BaseQuestion

STREAK_BONUS_THRESHOLD = 3


class QuizSession:
    """Tracks all state for a single in-progress quiz.

    Args:
        user_id (int): Telegram ID of the player.
        category (str): The category chosen for this game.
        questions (List[BaseQuestion]): The ordered list of questions.

    Attributes:
        score (int): Points accumulated so far.
        correct (int): Number of correct answers so far.
        streak (int): Current consecutive-correct-answer streak.
        max_streak (int): Highest streak reached in this session.
    """

    def __init__(
        self,
        user_id: int,
        category: str,
        questions: List[BaseQuestion],
    ) -> None:
        self.user_id = user_id
        self.category = category
        self.questions = questions
        self.current_index = 0
        self.score = 0
        self.correct = 0
        self.streak = 0
        self.max_streak = 0

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def total(self) -> int:
        """Total number of questions in this session."""
        return len(self.questions)

    @property
    def is_finished(self) -> bool:
        """True when all questions have been answered."""
        return self.current_index >= self.total

    @property
    def current_question(self) -> Optional[BaseQuestion]:
        """The question currently awaiting an answer, or None if finished."""
        if self.is_finished:
            return None
        return self.questions[self.current_index]

    @property
    def progress(self) -> str:
        """Human-readable progress string, e.g. ``'3/10'``."""
        return f"{self.current_index + 1}/{self.total}"

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def answer(self, answer: str) -> bool:
        """Process the player's answer and advance to the next question.

        Applies streak bonuses: every correct answer in a streak of
        :data:`STREAK_BONUS_THRESHOLD` or more awards +1 extra point.

        Args:
            answer (str): The answer selected by the player.

        Returns:
            bool: True if the answer was correct, False otherwise.
        """
        question = self.current_question
        if question is None:
            return False

        is_correct = question.check_answer(answer)

        if is_correct:
            self.streak += 1
            self.max_streak = max(self.max_streak, self.streak)
            bonus = 1 if self.streak >= STREAK_BONUS_THRESHOLD else 0
            self.score += question.get_points() + bonus
            self.correct += 1
        else:
            self.streak = 0

        self.current_index += 1
        return is_correct
