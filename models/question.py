"""
question.py
-----------
Defines the question class hierarchy for the quiz bot.

Classes:
    BaseQuestion          -- abstract base for all question types
    MultipleChoiceQuestion -- four-option multiple choice question
    TrueFalseQuestion      -- simple true/false question
"""

import random
from abc import ABC, abstractmethod
from typing import List


class BaseQuestion(ABC):
    """Abstract base class for all question types.

    Subclasses must implement :meth:`get_options`, :meth:`check_answer`,
    and :meth:`get_correct_answer`.

    Attributes:
        text (str): The question text shown to the user.
        category (str): The category this question belongs to.
        difficulty (str): One of ``"easy"``, ``"medium"``, or ``"hard"``.
    """

    POINTS = {"easy": 1, "medium": 2, "hard": 3}

    def __init__(self, text: str, category: str, difficulty: str) -> None:
        self.text = text
        self.category = category
        self.difficulty = difficulty

    @abstractmethod
    def get_options(self) -> List[str]:
        """Return the list of selectable answer options."""

    @abstractmethod
    def check_answer(self, answer: str) -> bool:
        """Return True if *answer* is correct, False otherwise."""

    @abstractmethod
    def get_correct_answer(self) -> str:
        """Return the correct answer as a string."""

    def get_points(self) -> int:
        """Return the base point value for this question.

        Returns:
            int: Points awarded for a correct answer (1, 2, or 3).
        """
        return self.POINTS.get(self.difficulty, 1)


class MultipleChoiceQuestion(BaseQuestion):
    """A question with one correct answer among four choices.

    Options are shuffled once and cached so the order stays consistent
    within a single quiz session.

    Args:
        text (str): The question text.
        category (str): The question category.
        difficulty (str): ``"easy"``, ``"medium"``, or ``"hard"``.
        correct_answer (str): The one correct answer.
        wrong_answers (List[str]): Exactly three wrong answers.
    """

    def __init__(
        self,
        text: str,
        category: str,
        difficulty: str,
        correct_answer: str,
        wrong_answers: List[str],
    ) -> None:
        super().__init__(text, category, difficulty)
        self._correct = correct_answer
        self._wrong = wrong_answers
        self._cached_options: List[str] = []

    def get_options(self) -> List[str]:
        """Return shuffled options (result is cached after first call)."""
        if not self._cached_options:
            options = [self._correct] + self._wrong
            random.shuffle(options)
            self._cached_options = options
        return self._cached_options

    def check_answer(self, answer: str) -> bool:
        return answer.strip().lower() == self._correct.strip().lower()

    def get_correct_answer(self) -> str:
        return self._correct


class TrueFalseQuestion(BaseQuestion):
    """A question with only True or False as valid answers.

    Args:
        text (str): The statement to evaluate.
        category (str): The question category.
        difficulty (str): ``"easy"``, ``"medium"``, or ``"hard"``.
        correct_answer (bool): The correct boolean answer.
    """

    def __init__(
        self,
        text: str,
        category: str,
        difficulty: str,
        correct_answer: bool,
    ) -> None:
        super().__init__(text, category, difficulty)
        self._correct = correct_answer

    def get_options(self) -> List[str]:
        """Return the two fixed options."""
        return ["True", "False"]

    def check_answer(self, answer: str) -> bool:
        return answer.strip().lower() == str(self._correct).lower()

    def get_correct_answer(self) -> str:
        return str(self._correct)
