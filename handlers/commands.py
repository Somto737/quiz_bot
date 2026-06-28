"""
commands.py
-----------
Handlers for basic Telegram commands: /start, /help, /leaderboard, /stats.
"""

from telegram import Update
from telegram.ext import ContextTypes

from database.manager import DatabaseManager
from utils.helpers import format_leaderboard
import config

db = DatabaseManager(config.DATABASE_PATH)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command — greet the user and register them.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Callback context.
    """
    user = update.effective_user
    db.get_or_create_user(user.id, user.username or "", user.first_name)

    text = (
        f"👋 Hello, *{user.first_name}*!\n\n"
        "🎯 Welcome to *QuizBot* — test your knowledge across five categories!\n\n"
        "📋 *Commands*\n"
        "/play — Start a new quiz\n"
        "/leaderboard — See the top players\n"
        "/stats — View your personal stats\n"
        "/help — How to play\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command — explain the game rules.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Callback context.
    """
    text = (
        "📖 *How to Play*\n\n"
        f"1. Use /play and choose a category\n"
        f"2. Answer {config.QUESTIONS_PER_GAME} questions\n"
        "3. Earn points based on difficulty\n\n"
        "⭐ *Points per correct answer*\n"
        "• 🟢 Easy  — 1 pt\n"
        "• 🟡 Medium — 2 pts\n"
        "• 🔴 Hard   — 3 pts\n\n"
        "🔥 *Streak Bonus*\n"
        "Answer 3+ in a row correctly to earn +1 bonus pt per answer!\n\n"
        ""📊 Your scores are saved for the /leaderboard — good luck! 🍀""
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /leaderboard command — show the top 10 players.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Callback context.
    """
    players = db.get_leaderboard(limit=10)

    if not players:
        await update.message.reply_text(
            "No scores yet — be the first with /play! 🎮"
        )
        return

    await update.message.reply_text(
        format_leaderboard(players), parse_mode="Markdown"
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /stats command — show the calling user's statistics.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Callback context.
    """
    user = update.effective_user
    player = db.get_or_create_user(user.id, user.username or "", user.first_name)

    text = (
        f"📊 *Your Stats*\n\n"
        f"🎮 Games played:  {player.games_played}\n"
        f"⭐ Total score:   {player.total_score} pts\n"
        f"✅ Correct:       {player.correct_answers}/{player.total_answers}\n"
        f"🎯 Accuracy:      {player.accuracy:.1f}%"
    )
    await update.message.reply_text(text, parse_mode="Markdown")
