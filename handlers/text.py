"""
Message handlers for text messages from the admins and the players
"""

from telebot.types import Message
from bot import bot
from constants import ADMIN_SET, BOT_ADMIN_ID
from .datastructures import AdminState, TeamState
import handlers
from . import admins_dict, players_dict, teams_dict, tasks_list
from .messages import *
from .senders import send_task, send_place
import re
import db.tasks
import db.places
import db.teams


@bot.message_handler(content_types=['text'])
async def text_message(message: Message) -> None:
    """
    Handler for adding the new task in the database with the base description
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    if telegram_id in ADMIN_SET:
        if admins_dict[telegram_id].state == AdminState.TASK_ADDING:
            await parse_task_description(text=message.text, telegram_id=telegram_id)
    if telegram_id in players_dict:
        team_id = players_dict[telegram_id].team_id
        team = teams_dict[team_id]
        state = team.state
        if state == TeamState.PLACE:
            current_round = team.current_round
            place_id = team.route[current_round]
            await check_password(password=message.text, place_id=place_id, team_id=team_id, player_id=telegram_id)
        elif state == TeamState.TASK:
            await send_answer(team_id=team_id, answer_text=message.text)
            if handlers.round_blocked:
                return
            team.current_round += 1
            await db.teams.set_current_round(team_id=team_id, current_round=team.current_round)
            await send_place(team_id)


async def send_answer(team_id: int, answer_text: str) -> None:
    """
    Send answer text for the task to the admin of the team
    :param team_id: id of the team
    :param answer_text: text of the answer
    :return:
    """
    team = teams_dict[team_id]
    admin_id = team.admin
    task_id = tasks_list[team.current_round]
    task = await db.tasks.get_info(task_id)
    message_answer = f'Задание {task_id}\nКоманда {team.name}\nОтвет:\n\n{answer_text}'
    message_right_answer = f'Правильный ответ:\n\n{task.answer}\n\nМаксимальный балл: {task.points}'
    await bot.send_message(admin_id, text=message_answer)
    await bot.send_message(admin_id, text=message_right_answer)
    await bot.send_message(chat_id=BOT_ADMIN_ID, text=f'{team.name} send answer to task {task_id}.\n{message_answer}')
    for player_id in team.members:
        await bot.send_message(chat_id=player_id, text=PLAYER_ANSWER_SENDED_MESSAGE)


async def parse_task_description(text: str, telegram_id: int) -> None:
    pattern = r'[Ii][Dd]:([\s\S]+)[Tt]ext:([\s\S]+)[Aa]nswer:([\s\S]+)[Pp]oints:([\s\S]+)'
    # raw_match = re.findall(pattern, text)
    description_list = [s.strip() for s in re.findall(pattern, text)[0]]

    if len(description_list) != 4:
        await bot.send_message(telegram_id, WRONG_TASK_FORMAT_ERROR_MESSAGE)
        return

    task_id = description_list[0]
    text = description_list[1]
    answer = description_list[2]
    points = int(description_list[3])

    await db.tasks.add_new(task_id=task_id, text=text, answer=answer, points=points)
    admins_dict[telegram_id].task_id = task_id
    await bot.send_message(telegram_id, TASK_ADDED_MESSAGE)


async def check_password(password: str, place_id: str, team_id: int, player_id: int) -> None:
    place = await db.places.get_info(place_id)
    team = teams_dict[team_id]
    if password.lower() == place.password.lower():
        await send_task(team_id)
        team.state = TeamState.TASK
        await bot.send_message(chat_id=BOT_ADMIN_ID, text=f'{team.name} guess correctly the password to the {place_id}')
    else:
        await bot.send_message(chat_id=player_id, text=PLAYER_WRONG_PASSWORD_MESSAGE)
        await bot.send_message(chat_id=BOT_ADMIN_ID, text=f'{team.name} choose "{password}" as a password for {place_id} and was wrong')
