from typing import NamedTuple
from handlers.datastructures import TeamState

__all__ = [
    'Task',
    'Player',
    'Place',
    'Team',
]


class Task(NamedTuple):
    """
    Named tuple corresponds to the task of theQuest

    Task(task_id, text, answer, points, photo_ids, video_ids, audio_ids)
    """
    task_id: str
    text: str
    answer: str
    points: int
    photo_ids: list[str]
    video_ids: list[str]
    audio_ids: list[str]


class Player(NamedTuple):
    """
    Named tuple corresponds to the player of theQuest

    Player(telegram_id, name, team_id)
    """
    telegram_id: int
    name: str
    team_id: int


class Place(NamedTuple):
    """
    Named tuple corresponds to the place of theQuest

    Place(place_id, text, password, photo_id)
    """
    place_id: str
    text: str
    password: str
    photo_id: str


class Team(NamedTuple):
    """
    Named tuple corresponds to the team of theQuest

    Team(team_id, name, route, current_round, state)
    """
    team_id: int
    name: str
    route: list[str]
    current_round: int
    state: TeamState
