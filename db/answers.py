import aiosqlite
from constants import DB_FILE

__all__ = [
    'add_new',
    'set_points',
    'get_team_results'
]


async def add_new(text: str, task_id: str, team_id: int, points: int) -> None:
    """
    Add new answer to the task with task_id
    :param text: text of the answer
    :param task_id: id of the task from the database
    :param team_id: id of the team
    :param points: max points for the task
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            'INSERT INTO answers (text, task_id, team_id, points) VALUES (?, ?, ?, ?)',
            (text, task_id, team_id, points)
        )
        await db.commit()


async def set_points(task_id: str, team_id: int, points: int) -> None:
    """
    Set points for the answer with answer_id
    :param task_id: id of the answer from the database
    :param team_id: id of the team
    :param points: number of points for the task
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('UPDATE answers SET score = ? WHERE task_id = ? AND team_id = ?', (points, task_id, team_id))
        await db.commit()


async def get_team_results(team_id: int) -> list[int]:
    """
    Get results of the specific team
    :param team_id: id of the team
    :return: the list of the points scored on different tasks
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT points FROM answers WHERE team_id = ?', (team_id, )) as cursor:
            results: list[int] = [row[0] async for row in cursor]
        return results
