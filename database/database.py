# =============================================================
# database/db.py
# ---------------------------------------------------------------
# This file handles everything related to the SQLite database.
# Contains: table creation, saving/reading submissions,
# managing points, saving/reading challenges, deleting old data.
# All other files import database functions from here.
# =============================================================

import sqlite3
from datetime import datetime
from config import DB_PATH, TIMEZONE


def init_db():
    """Creates the 3 tables if they don't exist: points, submissions, challenges"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS points (
            user_id TEXT PRIMARY KEY,
            total_points INTEGER DEFAULT 0
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            date TEXT NOT NULL,
            code TEXT,
            output TEXT,
            is_correct INTEGER DEFAULT 0,
            UNIQUE(user_id, date)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS challenges (
            date TEXT PRIMARY KEY,
            question TEXT,
            expected_output TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized!")


def db_add_submission(user_id, date, code, output, is_correct):
    """Saves a member's submission for today"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO submissions (user_id, date, code, output, is_correct)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, date, code, output, 1 if is_correct else 0))
    conn.commit()
    conn.close()


def db_has_submitted(user_id, date) -> bool:
    """Returns True if the member already submitted today"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM submissions WHERE user_id=? AND date=?', (user_id, date))
    result = c.fetchone()
    conn.close()
    return result is not None


def db_get_today_submissions(date) -> list:
    """Returns all submissions for a given date as a list of (user_id, is_correct, code)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id, is_correct, code FROM submissions WHERE date=?', (date,))
    result = c.fetchall()
    conn.close()
    return result


def db_add_points(user_id, pts):
    """Adds points to a member — creates a record if they don't exist yet"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO points (user_id, total_points) VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET total_points = total_points + ?
    ''', (user_id, pts, pts))
    conn.commit()
    conn.close()


def db_get_leaderboard() -> list:
    """Returns the top 10 members sorted by points as a list of (user_id, total_points)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id, total_points FROM points ORDER BY total_points DESC LIMIT 10')
    result = c.fetchall()
    conn.close()
    return result


def db_save_challenge(date, question, expected_output):
    """Saves today's challenge to the database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO challenges (date, question, expected_output)
        VALUES (?, ?, ?)
    ''', (date, question, expected_output))
    conn.commit()
    conn.close()


def db_get_challenge(date) -> dict:
    """Returns the challenge for a given date as a dict, or None if not found"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT question, expected_output FROM challenges WHERE date=?', (date,))
    result = c.fetchone()
    conn.close()
    if result:
        return {"question": result[0], "expected_output": result[1]}
    return None


def db_delete_old_data():
    """Deletes challenges and submissions from all previous days — keeps today only"""
    today = datetime.now(TIMEZONE).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM challenges WHERE date != ?', (today,))
    c.execute('DELETE FROM submissions WHERE date != ?', (today,))
    conn.commit()
    conn.close()
    print("🗑️ Old data deleted.")