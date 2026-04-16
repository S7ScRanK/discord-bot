# =============================================================
# tasks/leaderboard.py
# ---------------------------------------------------------------
# This file contains the scheduled task that runs every Friday
# at 10:00 PM Cairo time. It:
# 1. Checks if today is Friday — if not, does nothing
# 2. Gets the top 10 members by points from the database
# 3. Sends a weekly leaderboard embed to CHALLENGE_CHANNEL
# =============================================================

import discord
from discord.ext import tasks
from datetime import datetime, time

from config import TIMEZONE, CHALLENGE_CHANNEL_ID
from database.db import db_get_leaderboard


def setup_task(bot):
    """Registers and starts the weekly leaderboard task on the bot"""

    @tasks.loop(time=time(20, 0, tzinfo=TIMEZONE))  # Runs daily at 10 PM, checks if Friday
    async def weekly_leaderboard():
        today = datetime.now(TIMEZONE)

        # Only run on Fridays (weekday 4 in Python)
        if today.weekday() != 4:
            return

        challenge_channel = bot.get_channel(CHALLENGE_CHANNEL_ID)
        if not challenge_channel:
            return

        leaderboard = db_get_leaderboard()

        if not leaderboard:
            await challenge_channel.send("😅 No points on the leaderboard yet! Start solving challenges.")
            return

        medals = ["🥇", "🥈", "🥉"]
        leaderboard_text = ""

        for i, (user_id, pts) in enumerate(leaderboard):
            medal = medals[i] if i < 3 else f"#{i+1}"
            leaderboard_text += f"{medal} <@{user_id}> — **{pts}** points\n"

        embed = discord.Embed(
            title="🏆 Weekly Leaderboard!",
            description=leaderboard_text,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"📅 Week ending {today.strftime('%Y-%m-%d')}")

        await challenge_channel.send(embed=embed)
        print("✅ Weekly leaderboard sent.")

    weekly_leaderboard.start()
    return weekly_leaderboard