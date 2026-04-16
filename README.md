# 🧩 Daily Coding Challenge Discord Bot

A Discord bot that sends a daily Python programming challenge at 10 AM, collects member submissions, and automatically grades them at 10 PM. Members earn points for correct solutions, tracked on a leaderboard.

---

## ✨ Features

- 📌 Sends a daily coding challenge automatically at **10:00 AM** (Cairo time)
- 📥 Accepts code submissions from members via `!solve`
- ⚡ Runs submitted code using **Piston API** (free, no setup required)
- 🤖 Automatically grades all submissions at **10:00 PM**
- 🏆 Tracks member points in a **SQLite database**
- 💾 Data persists across restarts using **Railway Volume**
- 🔒 One submission per member per day

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Main language |
| discord.py | Discord bot framework |
| Piston API | Runs submitted code safely |
| SQLite | Stores points, submissions, challenges |
| Railway | Hosts the bot 24/7 |
| GitHub | Version control & auto-deploy |

---

## 📁 Project Structure

```
bot_enviroment/
├── bot.py            # Main bot code
├── requirements.txt  # Python dependencies
├── Procfile          # Railway start command
└── .env              # Secret tokens (never push this!)
```

---

## ⚙️ Setup & Installation

### 1 — Clone the repository

```bash
git clone https://github.com/S7ScRanK/discord-bot.git
cd discord-bot
```

### 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### 3 — Create your `.env` file

```
DISCORD_TOKEN=your_discord_bot_token
CHANNEL_ID=your_channel_id
DB_PATH=bot_data.db
```

### 4 — Run the bot locally

```bash
python bot.py
```

---

## 🤖 Discord Developer Portal Setup

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application** and give it a name
3. Go to **Bot** → Click **Add Bot**
4. Under **Privileged Gateway Intents**, enable **Message Content Intent** ✅
5. Go to **OAuth2 → URL Generator**:
   - Scopes: `bot`
   - Permissions: `Send Messages`, `Read Messages`, `Embed Links`, `Read Message History`
6. Open the generated URL and invite the bot to your server

---

## 🚀 Deploying to Railway (Free Hosting)

1. Push your code to GitHub (without `.env`)
2. Go to [railway.app](https://railway.app) and sign in with GitHub
3. Click **New Project → GitHub Repository** → select `discord-bot`
4. Go to **Variables** and add:
   ```
   DISCORD_TOKEN = your_token
   CHANNEL_ID = your_channel_id
   DB_PATH = /data/bot_data.db
   ```
5. Go to **Settings → Volumes → Add Volume**
   - Mount Path: `/data`
6. Railway will auto-deploy on every GitHub push ✅

---

## 💬 Bot Commands

| Command | Who | Description |
|---------|-----|-------------|
| `!solve [code]` | Everyone | Submit your solution for today's challenge |
| `!today` | Everyone | Show today's challenge |
| `!points` | Everyone | Show the leaderboard |
| `!testchallenge` | Admin only | Send a challenge immediately (for testing) |
| `!testgrade` | Admin only | Grade submissions immediately (for testing) |

---

## 🗄️ Database Structure

The bot uses **SQLite** with 3 tables:

**`challenges`** — stores each day's challenge
```
date | question | expected_output
```

**`submissions`** — stores each member's daily submission
```
id | user_id | date | code | output | is_correct
```

**`points`** — stores each member's total points
```
user_id | total_points
```

---

## 🔄 How It Works

```
10:00 AM  →  Bot sends daily challenge to the channel
    ↓
Members use !solve to submit their Python code
    ↓
Bot runs the code on Piston API and saves the output
    ↓
10:00 PM  →  Bot compares each output to the expected answer
    ↓
Correct members get +10 points saved to the database
    ↓
Bot announces results in the channel
```

---

## 📦 Requirements

```
discord.py
aiohttp
python-dotenv
pytz
```

---

## 📄 License

MIT License — feel free to use and modify this project.
