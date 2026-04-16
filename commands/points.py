# =============================================================
# commands/points.py
# ---------------------------------------------------------------
# This file contains the !points command.
# Admin only — shows the top 10 members leaderboard.
# Only works in ADMIN_CHANNEL (enforced by on_message in main.py).
# Reads points from the database and displays them as an embed.
# =============================================================

import discord
from discord.ext import commands
from database.db import db_get_leaderboard


def is_admin(ctx) -> bool:
    return ctx.author.guild_permissions.administrator


def setup(bot):
    """Registers the !points command on the bot"""

    @bot.command(name="points")
    @commands.check(is_admin)
    async def points(ctx):
        leaderboard = db_get_leaderboard()

        if not leaderboard:
            return await ctx.send("😅 No points yet! Start solving challenges.")

        medals = ["🥇", "🥈", "🥉"]
        leaderboard_text = ""

        for i, (user_id, pts) in enumerate(leaderboard):
            medal = medals[i] if i < 3 else f"#{i+1}"
            leaderboard_text += f"{medal} <@{user_id}> — **{pts}** points\n"

        embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.gold())
        embed.description = leaderboard_text
        await ctx.send(embed=embed)