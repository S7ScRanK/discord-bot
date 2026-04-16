# =============================================================
# commands/today.py
# ---------------------------------------------------------------
# This file contains the !today command.
# Admin only — shows today's challenge in the admin channel.
# Only works in ADMIN_CHANNEL (enforced by on_message in main.py).
# Reads the challenge from memory cache or database if bot restarted.
# =============================================================

import discord
from discord.ext import commands
from datetime import datetime
from config import TIMEZONE
from database.db import db_get_challenge


def is_admin(ctx) -> bool:
    return ctx.author.guild_permissions.administrator


def setup(bot, daily_challenge: dict):
    """Registers the !today command on the bot"""

    @bot.command(name="today")
    @commands.check(is_admin)
    async def today(ctx):
        today_str = datetime.now(TIMEZONE).strftime("%Y-%m-%d")

        if not daily_challenge["question"]:
            challenge = db_get_challenge(today_str)
            if not challenge:
                return await ctx.send("❌ No challenge posted yet today!")
            daily_challenge.update(challenge)
            daily_challenge["date"] = today_str

        embed = discord.Embed(
            title="🧩 Today's Challenge",
            description=daily_challenge["question"],
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)