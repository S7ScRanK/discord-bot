# =============================================================
# executor/code_runner.py
# ---------------------------------------------------------------
# This file handles running member-submitted Python code safely.
# Sends the code to Piston API (free, no key needed) and returns
# the output (stdout) or error (stderr).
# Also contains clean_code() to strip markdown backticks.
# =============================================================

import re
import aiohttp
import asyncio
from config import PISTON_URL


async def run_code(code: str) -> dict:
    """
    Sends code to Piston API and returns the result.
    Returns: {"stdout": "...", "stderr": "..."}
    """
    async with aiohttp.ClientSession() as session:
        payload = {
            "language": "python",
            "version": "3.10.0",
            "files": [{"content": code}]
        }
        timeout = aiohttp.ClientTimeout(total=15)
        try:
            async with session.post(PISTON_URL, json=payload, timeout=timeout) as response:
                data = await response.json()
            return {
                "stdout": data.get('run', {}).get('stdout', '').strip(),
                "stderr": data.get('run', {}).get('stderr', '').strip()
            }
        except asyncio.TimeoutError:
            return {"stdout": "", "stderr": "Timeout — your code took too long to run."}
        except Exception as e:
            return {"stdout": "", "stderr": str(e)}


def clean_code(raw: str) -> str:
    """
    Removes markdown code block backticks from submitted code.
    Example: ```python\\nprint(1)\\n``` → print(1)
    """
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r'^```[\w]*\n?', '', raw)
        raw = re.sub(r'```$', '', raw)
    return raw.strip()