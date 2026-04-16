# =============================================================
# tasks/grading.py
# ---------------------------------------------------------------
# This file contains the scheduled task that runs every day
# at 10:00 PM Cairo time. It:
# 1. Gets all submissions for today from the database
# 2. Adds +10 points to members who solved correctly
# 3. Sends results embed to CHALLENGE_CHANNEL (correct/incorrect)
# 4. Sends a separate embed showing the correct expected output
# =============================================================

import discord
from discord.ext import tasks
from datetime import datetime, time

from config import TIMEZONE, CHALLENGE_CHANNEL_ID
from database.db import db_get_today_submissions, db_add_points, db_get_challenge


def setup_task(bot, daily_challenge: dict):
    """Registers and starts the grading task on the bot"""

    @tasks.loop(time=time(20, 0, tzinfo=TIMEZONE))  # 10 PM Cairo (UTC+2 = 20 UTC)
    async def grade_submissions():
        challenge_channel = bot.get_channel(CHALLENGE_CHANNEL_ID)
        if not challenge_channel:
            return

        today_str = datetime.now(TIMEZONE).strftime("%Y-%m-%d")

        # Load today's challenge from DB if bot restarted
        if not daily_challenge["question"]:
            challenge = db_get_challenge(today_str)
            if not challenge:
                return
            daily_challenge.update(challenge)
            daily_challenge["date"] = today_str

        submissions_today = db_get_today_submissions(today_str)

        if not submissions_today:
            await challenge_channel.send("😔 **No one submitted today!** Try again tomorrow.")
            return

        correct_users = []
        wrong_users   = []

        for user_id, is_correct, code in submissions_today:
            if is_correct:
                correct_users.append(user_id)
                db_add_points(user_id, 10)
            else:
                wrong_users.append(user_id)

        # Results embed
        embed = discord.Embed(title="📊 Today's Challenge Results!", color=discord.Color.gold())

        if correct_users:
            winners_text = "\n".join([f"✅ <@{uid}>" for uid in correct_users])
            embed.add_field(
                name=f"🏆 Correct ({len(correct_users)} members) — +10 points each",
                value=winners_text,
                inline=False
            )

        if wrong_users:
            losers_text = "\n".join([f"❌ <@{uid}>" for uid in wrong_users])
            embed.add_field(
                name=f"📚 Incorrect ({len(wrong_users)} members)",
                value=losers_text,
                inline=False
            )

        await challenge_channel.send(embed=embed)

        # Correct answer embed
        answer_embed = discord.Embed(title="✅ Today's Correct Solution", color=discord.Color.green())
        answer_embed.add_field(
            name="Expected Output:",
            value=f"```\n{daily_challenge['expected_output']}\n```",
            inline=False
        )
        answer_embed.add_field(
            name="Example Solution:",
            value="```python\n# One of many correct solutions\n# Check your own approach!\n```",
            inline=False
        )

        await challenge_channel.send(embed=answer_embed)
        print("✅ Grading complete, results sent.")

    grade_submissions.start()
    return grade_submissions