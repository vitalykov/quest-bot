"""
Data structures used in the message handlers for the bot
"""

from enum import Enum
from dataclasses import dataclass

__all__ = [
    'AdminInfo',
    'AdminState',
    'TeamInfo',
    'TeamState',
    'PlayerInfo'
]


class AdminState(Enum):
    DEFAULT = 1
    TASK_ADDING = 2
    TASK_SCORING = 3
    PLACE_ADDING = 4


class TeamState(Enum):
    DEFAULT = 1
    TASK = 2
    PLACE = 3


@dataclass
class AdminInfo:
    state: AdminState
    task_id: str


@dataclass
class TeamInfo:
    team_id: int
    name: str
    route: list[str]
    current_round: int
    state: TeamState
    members: set[int]
    scores: list[int]
    admin: int


@dataclass
class PlayerInfo:
    telegram_id: int
    name: str
    team_id: int

