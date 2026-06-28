"""
helpers.py
----------
Shared utility functions used across multiple handlers.
"""

from typing import Optional


def build_result_grade(accuracy: float) -> str:
    """Return an emoji + label that reflects the player's accuracy.

    Args:
        accuracy (float): Percentage of correct answers (0–100).

    Returns:
        str: A short grade string, e.g. ``"🏆 Perfect!"``.
    """
    if accuracy == 100:
        return "🏆 Perfect score!"
    if accuracy >= 80:
        return "⭐ Excellent!"
    if accuracy >= 60:
        return "👍 Good job!"
    if accuracy >= 40:
        return "📚 Keep studying!"
    return "💪 Keep trying!"


def difficulty_emoji(difficulty: str) -> str:
    """Map a difficulty string to a coloured circle emoji.

    Args:
        difficulty (str): One of ``"easy"``, ``"medium"``, or ``"hard"``.

    Returns:
        str: The matching emoji, defaulting to ⚪ for unknown values.
    """
    mapping = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    return mapping.get(difficulty, "⚪")


def format_leaderboard(players: list, medals: Optional[list] = None) -> str:
    """Format a list of User objects into a leaderboard string.

    Args:
        players (list): Iterable of :class:`~models.user.User` objects.
        medals (list, optional): Override medal symbols for top positions.

    Returns:
        str: Markdown-formatted leaderboard text.
    """
    if medals is None:
        medals = ["🥇", "🥈", "🥉"]

    lines = ["🏆 *Top Players*\n"]
    for i, player in enumerate(players):
        prefix = medals[i] if i < len(medals) else f"{i + 1}."
        lines.append(f"{prefix} {player.display_name} — {player.total_score} pts")
    return "\n".join(lines)
