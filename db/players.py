import aiosqlite
from constants import DB_FILE
from .datastructures import Player

__all__ = [
    'add_new',
    'set_team',
    'get_info',
    'get_all'
]


async def add_new(telegram_id: int, name: str) -> None:
    """
    Add new player of theQuest into the database
    :param telegram_id: telegram id of the player
    :param name: name of the player
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT INTO players (telegram_id, name) VALUES (?, ?)', (telegram_id, name))
        await db.commit()


async def set_team(team_id: int, telegram_id: int) -> None:
    """
    Set the team for the player with telegram_id
    :param telegram_id: telegram id of the player
    :param team_id: id of the team in the database
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('UPDATE players SET team_id = ? WHERE telegram_id = ?', (team_id, telegram_id))
        await db.commit()


async def get_info(telegram_id: int) -> Player:
    """
    Get the name of the player from the telegram id
    :param telegram_id: telegram id of the player
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT telegram_id, name, team_id FROM players WHERE telegram_id = ?', (telegram_id, )) as cursor:
            row = await cursor.fetchone()
        return Player(*row)


async def get_all() -> list[int]:
    """
    Get the list of the players of theQuest
    :return: list of telegram ids
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT telegram_id FROM players') as cursor:
            players = [row[0] async for row in cursor]
        return players
