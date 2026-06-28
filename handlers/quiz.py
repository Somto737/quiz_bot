"""
quiz.py
-------
Handlers for the interactive quiz flow: category selection,
question delivery, and answer processing.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

import config
from database.manager import DatabaseManager
from models.session import QuizSession
from questions.data import CATEGORIES, get_questions
from utils.helpers import build_result_grade, difficulty_emoji

db = DatabaseManager(config.DATABASE_PATH)

# Key used to store the active QuizSession in context.user_data
_SESSION_KEY = "quiz_session"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /play command — show the category selection menu.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Callback context.
    """
    keyboard = [
        [InlineKeyboardButton(cat, callback_data=f"cat_{cat}")]
        for cat in CATEGORIES
    ]
    keyboard.append(
        [InlineKeyboardButton("🎲 Random mix", callback_data="cat_Random")]
    )

    await update.message.reply_text(
        "🎮 *Choose a category to begin:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ---------------------------------------------------------------------------
# Category selection
# ---------------------------------------------------------------------------


async def category_selected(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle a category button press and start a new quiz session.

    Args:
        update (Update): Incoming Telegram update (callback query).
        context (ContextTypes.DEFAULT_TYPE): Callback context.
    """
    query = update.callback_query
    await query.answer()

    category = query.data.replace("cat_", "")
    user = query.from_user

    db.get_or_create_user(user.id, user.username or "", user.first_name)

    questions = get_questions(category, config.QUESTIONS_PER_GAME)
    if not questions:
        await query.edit_message_text("⚠️ No questions available. Try another category.")
        return

    session = QuizSession(user_id=user.id, category=category, questions=questions)
    context.user_data[_SESSION_KEY] = session

    await query.edit_message_text(
        f"🎯 Category: *{category}*\n"
        f"📝 {len(questions)} questions | Good luck!",
        parse_mode="Markdown",
    )
    await _send_current_question(context, update, session)


# ---------------------------------------------------------------------------
# Answer handling
# ---------------------------------------------------------------------------


async def answer_received(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle an answer button press, give feedback, and advance the quiz.

    Args:
        update (Update): Incoming Telegram update (callback query).
        context (ContextTypes.DEFAULT_TYPE): Callback context.
    """
    query = update.callback_query
    await query.answer()

    session: QuizSession | None = context.user_data.get(_SESSION_KEY)
    if session is None:
        await query.message.reply_text(
            "⚠️ No active quiz found. Start one with /play."
        )
        return

    answer = query.data.replace("ans_", "")
    correct_answer = session.current_question.get_correct_answer()
    is_correct = session.answer(answer)

    # Remove the answer buttons from the question message
    await query.edit_message_reply_markup(reply_markup=None)

    # Send feedback
    if is_correct:
        streak_note = (
            f"  🔥 Streak ×{session.streak}!" if session.streak >= 3 else ""
        )
        feedback = f"✅ *Correct!*{streak_note}"
    else:
        feedback = f"❌ *Wrong!*  The answer was: _{correct_answer}_"

    await query.message.reply_text(feedback, parse_mode="Markdown")

    if session.is_finished:
        await _finish_quiz(update, context, session)
    else:
        await _send_current_question(context, update, session)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


async def _send_current_question(
    context: ContextTypes.DEFAULT_TYPE,
    update: Update,
    session: QuizSession,
) -> None:
    """Render and send the current question with answer buttons.

    Args:
        context (ContextTypes.DEFAULT_TYPE): Callback context (used for bot).
        update (Update): The originating update (used to find the chat).
        session (QuizSession): The active quiz session.
    """
    question = session.current_question
    options = question.get_options()

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"ans_{opt}")]
        for opt in options
    ]

    diff_icon = difficulty_emoji(question.difficulty)
    text = (
        f"❓ *Question {session.progress}*\n"
        f"{diff_icon} {question.difficulty.capitalize()}  •  📁 {question.category}\n\n"
        f"{question.text}"
    )

    chat_id = (
        update.callback_query.message.chat_id
        if update.callback_query
        else update.message.chat_id
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def _finish_quiz(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: QuizSession,
) -> None:
    """Persist results and send the end-of-quiz summary.

    Args:
        update (Update): The originating update.
        context (ContextTypes.DEFAULT_TYPE): Callback context.
        session (QuizSession): The completed quiz session.
    """
    user = update.callback_query.from_user
    db.save_game(
        user_id=user.id,
        category=session.category,
        score=session.score,
        correct=session.correct,
        total=session.total,
    )

    accuracy = session.correct / session.total * 100 if session.total else 0
    grade = build_result_grade(accuracy)

    text = (
        "🎉 *Quiz Complete!*\n\n"
        f"📁 Category:    {session.category}\n"
        f"⭐ Score:       *{session.score} pts*\n"
        f"✅ Correct:     {session.correct}/{session.total}\n"
        f"🎯 Accuracy:    {accuracy:.1f}%\n"
        f"🔥 Best streak: {session.max_streak}\n\n"
        f"{grade}\n\n"
        "Play again? → /play\n"
        "See rankings? → /leaderboard"
    )

    # Clean up session
    context.user_data.pop(_SESSION_KEY, None)

    await update.callback_query.message.reply_text(text, parse_mode="Markdown")
