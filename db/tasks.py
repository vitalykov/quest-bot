import aiosqlite
from constants import DB_FILE
from .datastructures import Task
from .media import get_photos, get_audios, get_videos

__all__ = [
    'add_new',
    'get_info',
    'delete',
    'get_all'
]


async def add_new(task_id: str, text: str, answer: str, points: int) -> None:
    """
    Add new task to the database
    :param task_id: id of the task
    :param text: description of the task
    :param answer: Right answer to the task
    :param points: Maximum points for the task
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT INTO tasks (id, text, answer, points) VALUES (?, ?, ?, ?)',
                         (task_id, text, answer, points))
        await db.commit()


async def get_info(task_id: str) -> Task | None:
    """
    Get the information about specific task
    :param task_id: id of the task
    :return: Task object
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT text, answer, points FROM tasks WHERE id = ?',
                              (task_id, )) as cursor:
            # Getting the first record of the query
            row = await cursor.fetchone()
            if not row:
                return None
            text, answer, points = row
        photo_ids = await get_photos(task_id)
        video_ids = await get_videos(task_id)
        audio_ids = await get_audios(task_id)
    return Task(
        task_id=task_id, text=text, answer=answer, points=points,
        photo_ids=photo_ids, video_ids=video_ids, audio_ids=audio_ids
    )


async def delete(task_id: str) -> None:
    """
    Delete task record from the database
    :param task_id: id of the task
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM tasks WHERE id = ?', (task_id, ))
        await db.commit()


async def get_all() -> list[str]:
    """
    Get the list of all tasks in theQuest
    :return: list of task ids
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT id FROM tasks') as cursor:
            tasks = [row[0] async for row in cursor]
        return tasks
