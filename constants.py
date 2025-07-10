"""
Some constants used in the Quest bot
"""
from dotenv import load_dotenv
import os

__all__ = [
    'TOKEN',
    'ADMIN_SET',
    'DB_FILE',
    'BOT_ADMIN_ID',
    'TEAM_1_CURATOR_ID',
    'TEAM_2_CURATOR_ID'
]

load_dotenv()

# Token for telegram bot of Quest
TOKEN = os.getenv("TOKEN")

# Admins of the Quest bot
BOT_ADMIN_ID = int(os.getenv("BOT_ADMIN_ID"))
TEAM_1_CURATOR_ID = int(os.getenv("TEAM_1_CURATOR_ID"))
TEAM_2_CURATOR_ID = int(os.getenv("TEAM_2_CURATOR_ID"))
ADMIN_SET = {BOT_ADMIN_ID, TEAM_1_CURATOR_ID, TEAM_2_CURATOR_ID}

# Database file for the Quest bot
DB_FILE = 'db/quest.db'
