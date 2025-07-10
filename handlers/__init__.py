"""
Message handlers used in the Quest bot
"""
import asyncio

from constants import ADMIN_SET, TEAM_1_CURATOR_ID, TEAM_2_CURATOR_ID
from .datastructures import (
    AdminInfo, AdminState,
    TeamState, TeamInfo,
    PlayerInfo
)
import db.teams
import db.answers
import db.players
import db.tasks

__all__ = [
    'admins_dict',
    'team_id_from_admin',
    'teams_dict',
    'players_dict',
    'tasks_list',
    'quest_started',
    'round_blocked'
]

teams_dict: dict[int, TeamInfo] = {}
team_id_from_admin = {
    TEAM_1_CURATOR_ID: 1,
    TEAM_2_CURATOR_ID: 2,
}
admins_dict: dict[int, AdminInfo] = {telegram_id: AdminInfo(AdminState.DEFAULT, '') for telegram_id in ADMIN_SET}
quest_started = False
round_blocked = False
players_dict: dict[int, PlayerInfo] = {}
tasks_list = []


async def initialize_players_dict() -> None:
    global players_dict
    player_ids = await db.players.get_all()
    for telegram_id in player_ids:
        player = await db.players.get_info(telegram_id)
        players_dict[telegram_id] = PlayerInfo(*player)


async def initialize_teams_dict() -> None:
    global teams_dict
    team_admins = {
        1: TEAM_1_CURATOR_ID,
        2: TEAM_2_CURATOR_ID,
    }
    for i in range(1, 3):
        team = await db.teams.get_info(team_id=i)
        members = await db.teams.get_members(team_id=i)
        scores = await db.answers.get_team_results(team_id=i)
        team_admin = team_admins[team.team_id]
        teams_dict[i] = TeamInfo(team.team_id, team.name, team.route, team.current_round,
                                 team.state, members, scores, team_admin)


async def initialize_task_list() -> None:
    global tasks_list
    tasks_list = await db.tasks.get_all()


async def initialize_data() -> None:
    await initialize_task_list()
    await initialize_players_dict()
    await initialize_teams_dict()


asyncio.run(initialize_data())
