# =============================================================
# tasks/daily_challenge.py
# ---------------------------------------------------------------
# This file contains the scheduled task that runs every day
# at 10:00 AM Cairo time. It:
# 1. Deletes yesterday's challenges and submissions
# 2. Gets today's challenge from challenges/weekly.py
# 3. Saves it to the database
# 4. Sends it as an embed to CHALLENGE_CHANNEL
# =============================================================

import discord
from discord.ext import tasks
from datetime import datetime, time

from config import TIMEZONE, CHALLENGE_CHANNEL_ID, SUBMIT_CHANNEL_ID
from database.db import db_save_challenge, db_delete_old_data
from challenges.weekly import get_today_challenge

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Shared in-memory cache — imported and used by other tasks and commands
daily_challenge = {
    "question": None,
    "expected_output": None,
    "date": None
}


def setup_task(bot):
    """Registers and starts the daily challenge task on the bot"""

    @tasks.loop(time=time(8, 0, tzinfo=TIMEZONE))  # 10 AM Cairo (UTC+2 = 8 UTC)
    async def send_daily_challenge():
        challenge_channel = bot.get_channel(CHALLENGE_CHANNEL_ID)
        if not challenge_channel:
            print(f"❌ Challenge channel not found: {CHALLENGE_CHANNEL_ID}")
            return

        today      = datetime.now(TIMEZONE)
        today_str  = today.strftime("%Y-%m-%d")
        day_index  = (today.weekday() + 1) % 7

        # Delete old data and load today's challenge
        db_delete_old_data()
        challenge = get_today_challenge()

        # Save to DB and memory cache
        db_save_challenge(today_str, challenge["question"], challenge["expected_output"])
        daily_challenge["question"]         = challenge["question"]
        daily_challenge["expected_output"]  = challenge["expected_output"]
        daily_challenge["date"]             = today_str

        embed = discord.Embed(
            title=f"🧩 Daily Coding Challenge — {DAYS[day_index]}!",
            description=challenge["question"],
            color=discord.Color.blue()
        )
        embed.add_field(
            name="📤 How to submit?",
            value=f"Go to <#{SUBMIT_CHANNEL_ID}> and use:\n`!start` followed by your code",
            inline=False
        )
        embed.add_field(name="⏰ Deadline", value="10:00 PM today", inline=False)
        embed.set_footer(text=f"📅 {today_str}")

        await challenge_channel.send(embed=embed)
        print(f"✅ Challenge sent for {today_str} ({DAYS[day_index]})")

    send_daily_challenge.start()
    return send_daily_challenge