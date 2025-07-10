from telebot.async_telebot import AsyncTeleBot
from constants import TOKEN

__all__ = [
    'bot'
]

bot = AsyncTeleBot(token=TOKEN)
