import asyncio
from bot import bot
import handlers.default
import handlers.admins
import handlers.text
import handlers.callback

asyncio.run(bot.polling())
