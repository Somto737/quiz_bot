import asyncio
import logging
import sys
from telegram.ext import Application, CallbackQueryHandler, CommandHandler
import config
from handlers.commands import help_command, leaderboard, start, stats
from handlers.quiz import answer_received, category_selected, play

logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    level=logging.INFO, stream=sys.stdout,
)
logger = logging.getLogger(__name__)

def build_application():
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN is not set.")
        sys.exit(1)
    app = Application.builder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(category_selected, pattern=r"^cat_"))
    app.add_handler(CallbackQueryHandler(answer_received, pattern=r"^ans_"))
    return app

async def main():
    app = build_application()
    logger.info("QuizBot is running — press Ctrl+C to stop.")
    async with app:
        await app.start()
        await app.updater.start_polling()
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
