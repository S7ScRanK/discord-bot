# =============================================================
# commands/test_grade.py
# ---------------------------------------------------------------
# This file contains the !testgrade command.
# Admin only — triggers grade_submissions() immediately
# without waiting for 10 PM, useful for testing results.
# Only works in ADMIN_CHANNEL (enforced by on_message in main.py).
# =============================================================

from discord.ext import commands


def is_admin(ctx) -> bool:
    return ctx.author.guild_permissions.administrator


def setup(bot, grade_submissions_func):
    """Registers the !testgrade command on the bot"""

    @bot.command(name="testgrade")
    @commands.check(is_admin)
    async def testgrade(ctx):
        await grade_submissions_func()
        await ctx.send("✅ Test grading done!")