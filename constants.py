"""
Some constants used in the Quest bot
"""
from dotenv import load_dotenv
import os

__all__ = [
    'TOKEN',
    'BOT_ADMIN_ID',
    'TEAM_1_CURATOR_ID',
    'TEAM_2_CURATOR_ID',
    'ADMIN_SET',
    'DB_FILE',
    'DB_TABLES_SCRIPT'
]

load_dotenv()

# Token for telegram bot of Quest
TOKEN = os.getenv("TOKEN")

# Admins of the Quest bot
BOT_ADMIN_ID = int(os.getenv("BOT_ADMIN_ID"))
TEAM_1_CURATOR_ID = int(os.getenv("TEAM_1_CURATOR_ID"))
TEAM_2_CURATOR_ID = int(os.getenv("TEAM_2_CURATOR_ID"))
ADMIN_SET = {BOT_ADMIN_ID, TEAM_1_CURATOR_ID, TEAM_2_CURATOR_ID}

# Database files for the Quest bot
DB_FILE = 'db/quest.db'
DB_TABLES_SCRIPT = 'db/tables.sql'
