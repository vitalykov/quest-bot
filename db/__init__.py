import aiosqlite
import asyncio

__all__ = [
    'create_tables'
]


async def create_tables() -> None:
    """
    CreateQuest database with all tables needed
    :return:
    """
    # Read sql script with database scheme from file
    with open('tables.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute sql script
    async with aiosqlite.connect('quest.db') as db:
        await db.executescript(sql_script)
        await db.commit()


async def main():
    task = asyncio.create_task(create_tables())
    await task


if __name__ == '__main__':
    asyncio.run(main())
