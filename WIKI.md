# QuizBot — Project Wiki

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Class Hierarchy](#class-hierarchy)
4. [Database Schema](#database-schema)
5. [Handler Flow](#handler-flow)
6. [Adding Questions](#adding-questions)
7. [Configuration Reference](#configuration-reference)

---

## Overview

QuizBot is a Telegram bot that delivers timed, categorised trivia quizzes to one or more users. Each game draws questions from a shared question bank, awards points by difficulty, and rewards streaks of consecutive correct answers. Results are persisted to SQLite so users can compete via a live leaderboard.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Telegram Server                   │
└──────────────────────┬──────────────────────────────┘
                       │  HTTPS long-polling
┌──────────────────────▼──────────────────────────────┐
│                     bot.py                          │
│   Application  ──  registers handlers               │
└──────┬────────────────────────────┬─────────────────┘
       │                            │
┌──────▼──────────┐       ┌─────────▼──────────┐
│ handlers/        │       │ handlers/           │
│ commands.py      │       │ quiz.py             │
│  /start /help    │       │  /play              │
│  /stats          │       │  category_selected  │
│  /leaderboard    │       │  answer_received    │
└──────┬──────────┘       └────────┬────────────┘
       │                           │
       │           ┌───────────────┘
       │           │
┌──────▼───────────▼────────────────────────────────┐
│                  database/manager.py               │
│              DatabaseManager (SQLite)              │
└──────────────────────────┬────────────────────────┘
                           │
               ┌───────────▼──────────┐
               │      quiz_bot.db     │
               │  users | game_history│
               └──────────────────────┘
```

---

## Class Hierarchy

```
BaseQuestion  (ABC — models/question.py)
├── MultipleChoiceQuestion
│     Stores one correct + three wrong answers.
│     Shuffles options once per instance.
└── TrueFalseQuestion
      Accepts True/False answers only.

User  (dataclass — models/user.py)
      Mirrors a row in the `users` table.
      Computed properties: accuracy, display_name.

QuizSession  (models/session.py)
      Tracks all mutable state for one active game:
      current question index, score, streak, max_streak.
      Exposes session.answer(str) → bool.

DatabaseManager  (database/manager.py)
      get_or_create_user()  →  User
      save_game()           →  None  (also updates aggregate stats)
      get_leaderboard()     →  List[User]
```

---

## Database Schema

### Table: `users`

| Column           | Type    | Description                          |
|------------------|---------|--------------------------------------|
| user_id          | INTEGER | Primary key (Telegram user ID)       |
| username         | TEXT    | Telegram @username (may be empty)    |
| first_name       | TEXT    | Telegram first name                  |
| total_score      | INTEGER | Cumulative score across all games    |
| games_played     | INTEGER | Number of completed games            |
| correct_answers  | INTEGER | Total correct answers given          |
| total_answers    | INTEGER | Total answers given                  |

### Table: `game_history`

| Column    | Type      | Description                              |
|-----------|-----------|------------------------------------------|
| id        | INTEGER   | Auto-increment primary key               |
| user_id   | INTEGER   | Foreign key → users.user_id              |
| category  | TEXT      | Category played                          |
| score     | INTEGER   | Points scored in this game               |
| correct   | INTEGER   | Correct answers in this game             |
| total     | INTEGER   | Total questions in this game             |
| played_at | TIMESTAMP | UTC timestamp of completion              |

---

## Handler Flow

```
User sends /play
        │
        ▼
   play()  ──►  sends InlineKeyboard with categories
        │
User taps a category button  (callback: "cat_<name>")
        │
        ▼
category_selected()
   ├── calls get_questions(category, N)
   ├── creates QuizSession
   ├── stores in context.user_data["quiz_session"]
   └── calls _send_current_question()
                │
                ▼
         Sends question + InlineKeyboard of answer options
                │
User taps an answer button  (callback: "ans_<text>")
                │
                ▼
        answer_received()
         ├── session.answer(answer)  → bool
         ├── removes buttons from question message
         ├── sends ✅/❌ feedback
         └── if session.is_finished → _finish_quiz()
                              else  → _send_current_question()
                                              │
                                        (loop until done)
```

---

## Adding Questions

Open `questions/data.py` and append to the relevant category list inside `_BANK`.

**Multiple choice:**
```python
MultipleChoiceQuestion(
    "Your question text?",
    "Category",          # must be in CATEGORIES list
    "medium",            # "easy" | "medium" | "hard"
    "Correct answer",
    ["Wrong 1", "Wrong 2", "Wrong 3"],
)
```

**True / False:**
```python
TrueFalseQuestion(
    "Statement to evaluate.",
    "Category",
    "easy",
    True,   # or False
)
```

To add a brand-new category, add its name to the `CATEGORIES` list at the top of `data.py` and add a matching key in `_BANK`.

---

## Configuration Reference

All options live in `.env` (copy from `.env.example`).

| Variable            | Default        | Description                              |
|---------------------|----------------|------------------------------------------|
| `BOT_TOKEN`         | *(required)*   | Token from @BotFather                    |
| `DATABASE_PATH`     | `quiz_bot.db`  | Path to the SQLite file                  |
| `QUESTIONS_PER_GAME`| `10`           | Questions dealt per game                 |
