from bot import bot
from telebot.types import Message
from constants import ADMIN_SET, BOT_ADMIN_ID
from .messages import HELP_MESSAGE, PLAYER_MAIN_MENU_MESSAGE
from .markups import ADMIN_MAIN_MENU_MARKUP, get_player_main_menu_markup
from . import players_dict
from .datastructures import PlayerInfo
import db.players


@bot.message_handler(commands=['start'])
async def greet(message: Message) -> None:
    telegram_id = message.chat.id
    name = message.chat.first_name
    if telegram_id in ADMIN_SET:
        await bot.send_message(chat_id=telegram_id, text='Quest',
                               reply_markup=ADMIN_MAIN_MENU_MARKUP)
    else:
        await register_player(telegram_id=telegram_id, name=name)
        await bot.send_message(chat_id=telegram_id, text=PLAYER_MAIN_MENU_MESSAGE,
                               reply_markup=get_player_main_menu_markup())


async def register_player(telegram_id: int, name: str) -> None:
    players_dict[telegram_id] = PlayerInfo(telegram_id=telegram_id, name=name, team_id=0)
    await db.players.add_new(telegram_id=telegram_id, name=name)
    await bot.send_message(chat_id=BOT_ADMIN_ID, text=f'{name} registered to the Quest')


@bot.message_handler(commands=['help'])
async def show_help(message: Message) -> None:
    telegram_id = message.chat.id
    if telegram_id in ADMIN_SET:
        await bot.send_message(telegram_id, text=HELP_MESSAGE, parse_mode='HTML')
