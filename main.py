import asyncio
import os

from bot import bot
from constants import DB_FILE
from db import create_tables
from handlers import initialize_data
import handlers.default
import handlers.admins
import handlers.text
import handlers.callback


async def main():
    if not os.path.isfile(DB_FILE):
        tables_task = asyncio.create_task(create_tables())
        await tables_task

    init_data_task = asyncio.create_task(initialize_data())
    await init_data_task
    bot_launch_task = asyncio.create_task(bot.polling())
    await bot_launch_task


if __name__ == '__main__':
    asyncio.run(main())
