import aiosqlite
import asyncio
from constants import DB_FILE, DB_TABLES_SCRIPT

__all__ = [
    'create_tables'
]


async def create_tables() -> None:
    """
    CreateQuest database with all tables needed
    :return:
    """
    # Read sql script with database scheme from file
    with open(DB_TABLES_SCRIPT, 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute sql script
    async with aiosqlite.connect(DB_FILE) as db:
        await db.executescript(sql_script)
        await db.commit()
