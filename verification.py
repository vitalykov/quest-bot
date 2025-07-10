from constants import ADMIN_SET
from functools import wraps
from telebot import types


def private_access(func):
    """
    Decorator for checking if the user of the bot is the admin. Should wrap a function before message_handler.\n
    Otherwise, decorator will not work.
    :param func: function to be decorated
    :return: wrapper around the function func
    """
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        chat_id = message.chat.id
        if chat_id in ADMIN_SET:
            return await func(message, *args, **kwargs)
        else:
            return None
    return wrapper
