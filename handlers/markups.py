from telebot.types import InlineKeyboardMarkup
from telebot.util import quick_markup
from . import teams_dict

__all__ = [
    'ADMIN_MAIN_MENU_MARKUP',
    'PLAYER_RESELECT_MARKUP',
    'LEADERBOARD_MARKUP',
    'get_player_main_menu_markup'
]

ADMIN_MAIN_MENU_MARKUP = quick_markup(
    {
        'Admin Mode': {'callback_data': 'admin_mode'},
        'Player Mode': {'callback_data': 'player_mode'}
    },
    row_width=1
)


def get_player_main_menu_markup() -> InlineKeyboardMarkup:
    return quick_markup(
        {
            teams_dict[1].name: {'callback_data': 'team1'},
            teams_dict[2].name: {'callback_data': 'team2'}
        },
        row_width=1
    )


PLAYER_RESELECT_MARKUP = quick_markup(
    {
        'Перевыбрать команду': {'callback_data': 'reselect'}
    },
    row_width=1
)

LEADERBOARD_MARKUP = quick_markup(
    {
        'Обновить': {'callback_data': 'refresh'}
    },
    row_width=1
)