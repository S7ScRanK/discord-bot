# =============================================================
# commands/start.py
# ---------------------------------------------------------------
# This file contains the !start command.
# Members use it to submit their Python code solution.
# Only works in SUBMIT_CHANNEL (enforced by on_message in main.py).
# Runs the code using Piston API, compares output to expected,
# and saves the submission to the database.
# =============================================================

from datetime import datetime
from config import TIMEZONE
from database.db import db_has_submitted, db_add_submission, db_get_challenge
from executor.code_runner import run_code, clean_code


def setup(bot, daily_challenge: dict):
    """Registers the !start command on the bot"""

    @bot.command(name="start")
    async def start(ctx, *, code: str = None):
        today_str = datetime.now(TIMEZONE).strftime("%Y-%m-%d")

        # Load today's challenge from DB if bot restarted
        if not daily_challenge["question"]:
            challenge = db_get_challenge(today_str)
            if not challenge:
                return await ctx.send("❌ No challenge today! Wait for the next one.")
            daily_challenge.update(challenge)
            daily_challenge["date"] = today_str

        if code is None:
            return await ctx.send(
                "❌ You need to include your code after the command!\n"
                "Example:\n```\n!start\nprint(5050)\n```"
            )

        if db_has_submitted(str(ctx.author.id), today_str):
            return await ctx.send("⚠️ You already submitted today! Wait for grading at 10 PM.")

        clean = clean_code(code)

        async with ctx.typing():
            result = await run_code(clean)

        if result["stderr"]:
            return await ctx.send(
                f"❌ **Your code has an error:**\n```\n{result['stderr'][:500]}\n```\n"
                f"Fix the error and try again!"
            )

        actual_output = result["stdout"].strip()
        expected      = daily_challenge["expected_output"].strip()
        is_correct    = actual_output == expected

        db_add_submission(str(ctx.author.id), today_str, clean, actual_output, is_correct)

        if is_correct:
            await ctx.send(
                "✅ **Submission recorded!**\n"
                "Grading will happen at 10 PM — you'll see the results then. 🎯"
            )
        else:
            await ctx.send(
                "📬 **Submission recorded!**\n"
                "Grading will happen at 10 PM. Good luck! 🤞"
            )