# =============================================================
# challenges/weekly.py
# ---------------------------------------------------------------
# This file contains the 7 weekly coding challenges.
# One challenge per day, starting from Sunday (index 0).
# To update challenges each week, edit WEEKLY_CHALLENGES below.
# get_today_challenge() returns the correct challenge for today.
# =============================================================

from datetime import datetime
from config import TIMEZONE

# ---------------------------------------------------------------
# WEEKLY CHALLENGES — Edit these every week with new problems
# Index 0 = Sunday, Index 1 = Monday, ..., Index 6 = Saturday
# ---------------------------------------------------------------
WEEKLY_CHALLENGES = [
    # 0 - الأحد (Sunday)
    {
        "question": """📌 **Today's Challenge — Sunday:**
Write a Python program that prints the sum of numbers from 1 to 100.
**Expected output:** A single number on one line.""",
        "expected_output": "5050"
    },
    # 1 - الاثنين (Monday)
    {
        "question": """📌 **Today's Challenge — Monday:**
Write a Python program that prints all even numbers from 1 to 20.
**Expected output:** Each number on a separate line.""",
        "expected_output": "2\n4\n6\n8\n10\n12\n14\n16\n18\n20"
    },
    # 2 - الثلاثاء (Tuesday)
    {
        "question": """📌 **Today's Challenge — Tuesday:**
Write a Python program that calculates the factorial of 5.
**Expected output:** Print the result only.""",
        "expected_output": "120"
    },
    # 3 - الأربعاء (Wednesday)
    {
        "question": """📌 **Today's Challenge — Wednesday:**
Write a Python program that reverses the word "python".
**Expected output:** Print the reversed word only.""",
        "expected_output": "nohtyp"
    },
    # 4 - الخميس (Thursday)
    {
        "question": """📌 **Today's Challenge — Thursday:**
Write a Python program that prints a star triangle with height 5.
**Expected output:** Each row has stars equal to the row number.""",
        "expected_output": "*\n**\n***\n****\n*****"
    },
    # 5 - الجمعة (Friday)
    {
        "question": """📌 **Today's Challenge — Friday:**
Write a Python program that checks if the number 17 is prime.
**Expected output:** Print True or False only.""",
        "expected_output": "True"
    },
    # 6 - السبت (Saturday)
    {
        "question": """📌 **Today's Challenge — Saturday:**
Write a Python program that prints the first 10 numbers of the Fibonacci sequence.
**Expected output:** Each number on a separate line.""",
        "expected_output": "0\n1\n1\n2\n3\n5\n8\n13\n21\n34"
    },
]


def get_today_challenge() -> dict:
    """Returns today's challenge based on the current day of the week (Sunday=0, Saturday=6)"""
    today = datetime.now(TIMEZONE)
    day_index = (today.weekday() + 1) % 7
    return WEEKLY_CHALLENGES[day_index]