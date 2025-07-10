import aiosqlite
from constants import DB_FILE
from .datastructures import Team, TeamState

__all__ = [
    'set_name',
    'set_route',
    'get_route',
    'get_members',
    'get_info',
    'get_current_round',
    'set_state',
    'set_current_round'
]


async def set_name(name: str, team_id: int) -> None:
    """
    Set the name of the team with team_id
    :param name: new name of the team
    :param team_id: id of the team in the database
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('UPDATE teams SET name = ? WHERE id = ?', (name, team_id))
        await db.commit()


async def set_route(route: str, team_id: int) -> None:
    """
    Set the route for the team with team_id
    :param route: sequence of tasks to solve
    :param team_id: id of the team in the database
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('UPDATE teams SET route = ? WHERE id = ?', (route, team_id))
        await db.commit()


async def get_members(team_id: int) -> set[int]:
    """
    Get the list of telegram ids of team members
    :param team_id: id of the team
    :return: list of telegram ids
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT telegram_id FROM players WHERE team_id = ?', (team_id, )) as cursor:
            members = {row[0] async for row in cursor}
        return members


async def get_info(team_id: int) -> Team:
    """
    Get the team information by the team_id
    :param team_id: id of the team
    :return: namedtuple Team
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute(
                'SELECT name, route, current_round, state FROM teams WHERE id = ?', (team_id, )
        ) as cursor:
            state_dict = {
                'default': TeamState.DEFAULT,
                'place': TeamState.PLACE,
                'task': TeamState.TASK
            }
            row = await cursor.fetchone()
            name, route_str, current_round, state_str = row
            route = route_str.split()
            state = state_dict[state_str]
        return Team(team_id, name, route, current_round, state)


async def get_route(team_id: int) -> list[str]:
    """
    Get the route for the team with team_id
    :param team_id: id of the team in the database
    :return: sequence of tasks to solve
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT route FROM teams WHERE id = ?', (team_id, )) as cursor:
            row = await cursor.fetchone()
            route = row[0].split()
        return route


async def get_current_round(team_id: int) -> int:
    """
    Get current round for the team with team_id
    :param team_id: id of the team in the database
    :return: current task to solve
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT current_round FROM teams WHERE id = ?', (team_id, )) as cursor:
            row = await cursor.fetchone()
            current_round = int(row[0])
        return current_round


async def set_current_round(team_id: int, current_round: int) -> None:
    """
    Set the current round for the team
    :param team_id: id of the team
    :param current_round: the new current round of quest
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('UPDATE teams SET current_round = ? WHERE id = ?', (current_round, team_id))
        await db.commit()


async def set_state(team_id: int, state: TeamState) -> None:
    """
    Set the state for the team
    :param team_id: id of the team
    :param state: state to be set
    :return:
    """
    state_dict = {
        TeamState.DEFAULT: 'default',
        TeamState.TASK: 'task',
        TeamState.PLACE: 'place'
    }
    state_str = state_dict[state]
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('UPDATE teams SET state = ? WHERE id = ?', (state_str, team_id))
        await db.commit()
