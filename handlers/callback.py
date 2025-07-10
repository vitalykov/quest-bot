import db.players
from bot import bot
from telebot.types import CallbackQuery

from constants import BOT_ADMIN_ID
from .default import show_help, register_player
from .messages import PLAYER_MAIN_MENU_MESSAGE, PLAYER_TEAM_CHOICE_MESSAGE
from .markups import get_player_main_menu_markup, PLAYER_RESELECT_MARKUP, LEADERBOARD_MARKUP
from .leaderboard import get_leaderboard
import handlers
from . import teams_dict, players_dict


@bot.callback_query_handler(lambda call: True)
async def callback_response(call: CallbackQuery) -> None:
    message = call.message
    telegram_id = message.chat.id
    name = message.chat.first_name
    match call.data:
        case 'admin_mode':
            await bot.send_message(chat_id=telegram_id, text=f'Hello, {name}! Welcome to Admin mode of this bot!')
            await show_help(message)
        case 'player_mode':
            await register_player(telegram_id=telegram_id, name=name)
            await show_player_menu(telegram_id)
        case 'team1':
            if handlers.quest_started:
                await bot.delete_message(chat_id=telegram_id, message_id=message.id)
            players_dict[telegram_id].team_id = 1
            teams_dict[1].members.add(telegram_id)
            if telegram_id in teams_dict[2].members:
                teams_dict[2].members.remove(telegram_id)
            team_name = teams_dict[1].name
            await db.players.set_team(team_id=1, telegram_id=telegram_id)
            await bot.edit_message_text(text=f'{PLAYER_TEAM_CHOICE_MESSAGE} {team_name}', chat_id=telegram_id,
                                        message_id=message.id, reply_markup=PLAYER_RESELECT_MARKUP)
            player = await db.players.get_info(telegram_id)
            await bot.send_message(chat_id=BOT_ADMIN_ID, text=f'{player.name} choose {team_name}')
        case 'team2':
            if handlers.quest_started:
                await bot.delete_message(chat_id=telegram_id, message_id=message.id)
            players_dict[telegram_id].team_id = 2
            teams_dict[2].members.add(telegram_id)
            if telegram_id in teams_dict[1].members:
                teams_dict[1].members.remove(telegram_id)
            team_name = teams_dict[2].name
            await db.players.set_team(team_id=2, telegram_id=telegram_id)
            await bot.edit_message_text(text=f'{PLAYER_TEAM_CHOICE_MESSAGE} {team_name}', chat_id=telegram_id,
                                        message_id=message.id, reply_markup=PLAYER_RESELECT_MARKUP)
            player = await db.players.get_info(telegram_id)
            await bot.send_message(chat_id=BOT_ADMIN_ID, text=f'{player.name} choose {team_name}')
        case 'reselect':
            if handlers.quest_started:
                await bot.delete_message(chat_id=telegram_id, message_id=message.id)
            await bot.edit_message_text(text=PLAYER_MAIN_MENU_MESSAGE, chat_id=telegram_id, message_id=message.id,
                                        reply_markup=get_player_main_menu_markup())
            player = await db.players.get_info(telegram_id)
            await bot.send_message(chat_id=BOT_ADMIN_ID, text=f'{player.name} want to reselect team')
        case 'refresh':
            leaderboard = get_leaderboard()
            try:
                await bot.edit_message_text(text=leaderboard, chat_id=telegram_id, message_id=message.id,
                                            parse_mode='HTML', reply_markup=LEADERBOARD_MARKUP)
            except:
                pass
    await bot.answer_callback_query(call.id)


async def show_player_menu(telegram_id: int) -> None:
    await bot.send_message(chat_id=telegram_id, text=PLAYER_MAIN_MENU_MESSAGE, reply_markup=get_player_main_menu_markup())
