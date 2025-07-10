import aiosqlite
from constants import DB_FILE
from .datastructures import Place

__all__ = [
    'add_new',
    'delete',
    'get_info'
]


async def add_new(place_id: str, text: str, password: str, photo_id: str) -> None:
    """
    Add new place to the database
    :param place_id: id of the place
    :param text: description of the place
    :param password: password to be found in the place
    :param photo_id: id of the photo in the telegram server
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT INTO places (id, text, password, photo_id) VALUES (?, ?, ?, ?)',
                         (place_id, text, password, photo_id))
        await db.commit()


async def delete(place_id: str) -> None:
    """
    Delete a place from the database
    :param place_id: id of the place
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM places WHERE id = ?', (place_id, ))
        await db.commit()


async def get_info(place_id: str) -> Place | None:
    """
    Get the place by place_id
    :param place_id: id of the place
    :return: namedtuple which contains information about the place
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT id, text, password, photo_id FROM places WHERE id = ?', (place_id, )) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None
    return Place(*row)
