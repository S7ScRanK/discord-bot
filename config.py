# =============================================================
# config.py
# ---------------------------------------------------------------
# This file loads all environment variables and settings.
# Every other file imports from here instead of reading .env directly.
# Contains: bot token, channel IDs, timezone, DB path, Piston URL.
# =============================================================

import os
import pytz
from dotenv import load_dotenv

current_folder = os.path.dirname(os.path.abspath(__file__))
env_file_path  = os.path.join(current_folder, '.env')

if os.path.exists(env_file_path):
    load_dotenv(dotenv_path=env_file_path)
else:
    print("❌ Warning: .env file not found!")

TOKEN                = os.getenv('DISCORD_TOKEN')
CHALLENGE_CHANNEL_ID = int(os.getenv('CHALLENGE_CHANNEL_ID', 0))
SUBMIT_CHANNEL_ID    = int(os.getenv('SUBMIT_CHANNEL_ID', 0))
ADMIN_CHANNEL_ID     = int(os.getenv('ADMIN_CHANNEL_ID', 0))
DB_PATH              = os.getenv('DB_PATH', 'bot_data.db')

PISTON_URL = "https://emkc.org/api/v2/piston/execute"
TIMEZONE   = pytz.timezone("Africa/Cairo")

if not TOKEN:
    print("❌ Error: DISCORD_TOKEN not found in .env file")
    exit(1)

if not CHALLENGE_CHANNEL_ID or not SUBMIT_CHANNEL_ID or not ADMIN_CHANNEL_ID:
    print("❌ Error: One or more channel IDs are missing in .env file")
    exit(1)

print("✅ Config loaded!")
print(f"📌 Challenge channel : {CHALLENGE_CHANNEL_ID}")
print(f"📝 Submit channel    : {SUBMIT_CHANNEL_ID}")
print(f"🔒 Admin channel     : {ADMIN_CHANNEL_ID}")