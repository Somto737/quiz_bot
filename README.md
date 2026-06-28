# 🎯 QuizBot

A Telegram quiz bot written in Python that tests players across five knowledge categories with score tracking, streaks, and a global leaderboard.

## Features
- 5 categories: Science, History, Geography, Sports, Technology (+ Random mix)
- Multiple choice and true/false questions
- Three difficulty levels with matching point values
- Streak bonus — answer 3+ in a row correctly for extra points
- Persistent SQLite leaderboard
- Personal stats via /stats

## How to Run
1. Clone the repo
2. Run `pip3 install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your bot token from @BotFather
4. Run `python3 bot.py`

## Commands
- /start — Welcome message
- /play — Start a quiz
- /leaderboard — Top players
- /stats — Your personal stats
- /help — Scoring rules

## Project Structure
- `bot.py` — Entry point
- `models/` — Question, Session, User classes
- `database/` — SQLite manager
- `handlers/` — Telegram command handlers
- `questions/` — Question bank (60+ questions)
- `utils/` — Helper functions
