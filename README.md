# 🎯 QuizBot

A Telegram quiz bot written in Python that tests players across five knowledge categories with score tracking, streaks, and a global leaderboard.

---

## Features

- 5 categories: **Science, History, Geography, Sports, Technology** (+ Random mix)
- Two question types: multiple-choice and true/false
- Three difficulty levels (Easy 🟢 / Medium 🟡 / Hard 🔴) with matching point values
- **Streak bonus** — answer 3+ in a row correctly to earn extra points
- Persistent **SQLite** leaderboard shared across all players
- Personal stats via `/stats`

---

## Project Structure

```
quiz_bot/
├── bot.py                  # Entry point — registers handlers and starts polling
├── config.py               # Reads settings from environment / .env
├── requirements.txt
├── .env.example
├── models/
│   ├── question.py         # BaseQuestion (ABC), MultipleChoiceQuestion, TrueFalseQuestion
│   ├── session.py          # QuizSession — tracks state for one active game
│   └── user.py             # User dataclass
├── database/
│   └── manager.py          # DatabaseManager — all SQLite reads/writes
├── handlers/
│   ├── commands.py         # /start  /help  /leaderboard  /stats
│   └── quiz.py             # /play, category selection, answer flow
├── questions/
│   └── data.py             # Question bank (60+ questions) + get_questions()
└── utils/
    └── helpers.py          # Shared formatting utilities
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-org/quiz_bot.git
cd quiz_bot
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Open .env and set BOT_TOKEN to the token from @BotFather
```

### 4. Run the bot

```bash
python bot.py
```

---

## Bot Commands

| Command        | Description                          |
|----------------|--------------------------------------|
| `/start`       | Register and see the welcome message |
| `/play`        | Start a new quiz (choose category)   |
| `/leaderboard` | See the top 10 players               |
| `/stats`       | View your personal statistics        |
| `/help`        | Explain scoring and streak rules     |

---

## Scoring System

| Difficulty | Base points | Streak bonus (3+ in a row) |
|------------|-------------|---------------------------|
| 🟢 Easy    | 1 pt        | +1 pt                     |
| 🟡 Medium  | 2 pts       | +1 pt                     |
| 🔴 Hard    | 3 pts       | +1 pt                     |

---

## Dependencies

| Package               | Version | Purpose                     |
|-----------------------|---------|-----------------------------|
| python-telegram-bot   | 21.3    | Telegram Bot API wrapper    |
| python-dotenv         | 1.0.1   | Load `.env` configuration   |

---

## Contributing (Team Git Workflow)

Each team member should work on a separate branch and open a pull request:

```bash
git checkout -b feature/your-name/what-you-did
# make changes
git add .
git commit -m "feat: add true/false question support"
git push origin feature/your-name/what-you-did
```

**Commit message convention:**

```
feat:  new feature
fix:   bug fix
docs:  documentation change
style: formatting only
refactor: code restructure without behaviour change
test:  adding tests
```

---

## Documentation

Full documentation (class diagrams, database schema, handler flow) is available on the [project Wiki](../../wiki).

---

## License

MIT
