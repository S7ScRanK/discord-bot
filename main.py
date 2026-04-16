# =============================================================
# main.py
# ---------------------------------------------------------------
# This is the entry point of the bot. Run this file to start.
# It:
# 1. Creates the bot instance
# 2. Initializes the database
# 3. Loads all commands from the commands/ folder
# 4. Starts all scheduled tasks from the tasks/ folder
# 5. Enforces channel rules via on_message
# 6. Connects to Discord using the token from config.py
# =============================================================

import asyncio
import discord
from discord.ext import commands
from datetime import datetime

from config import TOKEN, TIMEZONE, CHALLENGE_CHANNEL_ID, SUBMIT_CHANNEL_ID, ADMIN_CHANNEL_ID
from database.db import init_db, db_get_challenge

# Commands
import commands.start         as cmd_start
import commands.points        as cmd_points
import commands.today         as cmd_today
import commands.test_challenge as cmd_test_challenge
import commands.test_grade     as cmd_test_grade

# Tasks
import tasks.daily_challenge  as task_daily
import tasks.grading          as task_grading
import tasks.leaderboard      as task_leaderboard

# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Shared in-memory cache for today's challenge ---
daily_challenge = {
    "question": None,
    "expected_output": None,
    "date": None
}

# --- Channel Guard ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Only allow !start in SUBMIT_CHANNEL
    if message.content.startswith("!start"):
        if message.channel.id != SUBMIT_CHANNEL_ID:
            await message.delete()
            warn = await message.channel.send(
                f"⚠️ {message.author.mention} Please use `!start` in <#{SUBMIT_CHANNEL_ID}> only!"
            )
            await asyncio.sleep(5)
            await warn.delete()
            return

    # Only allow admin commands in ADMIN_CHANNEL
    admin_commands = ["!testchallenge", "!testgrade", "!points", "!today"]
    if any(message.content.startswith(cmd) for cmd in admin_commands):
        if message.channel.id != ADMIN_CHANNEL_ID:
            await message.delete()
            warn = await message.channel.send(
                f"⚠️ {message.author.mention} This command is not allowed here!"
            )
            await asyncio.sleep(5)
            await warn.delete()
            return

    await bot.process_commands(message)

# --- on_ready ---
@bot.event
async def on_ready():
    # Initialize database tables
    init_db()

    # Load today's challenge into memory if it exists
    today_str = datetime.now(TIMEZONE).strftime("%Y-%m-%d")
    challenge = db_get_challenge(today_str)
    if challenge:
        daily_challenge.update(challenge)
        daily_challenge["date"] = today_str
        print("✅ Loaded today's challenge from database.")

    # Register all commands
    cmd_start.setup(bot, daily_challenge)
    cmd_points.setup(bot)
    cmd_today.setup(bot, daily_challenge)

    # Start all tasks and get references for test commands
    send_daily_challenge_func = task_daily.setup_task(bot)
    grade_submissions_func    = task_grading.setup_task(bot, daily_challenge)
    task_leaderboard.setup_task(bot)

    # Register test commands with task references
    cmd_test_challenge.setup(bot, send_daily_challenge_func)
    cmd_test_grade.setup(bot, grade_submissions_func)

    print(f'🚀 Bot is online: {bot.user.name}')
    print(f'📌 Challenge channel : {CHALLENGE_CHANNEL_ID}')
    print(f'📝 Submit channel    : {SUBMIT_CHANNEL_ID}')
    print(f'🔒 Admin channel     : {ADMIN_CHANNEL_ID}')
    print('⏰ Scheduled tasks are running!')
    print('-----------------------------------------')

# --- Error Handler ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ You don't have permission to use this command!")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(f"Error: {error}")

# --- Run ---
bot.run(TOKEN)