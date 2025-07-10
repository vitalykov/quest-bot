"""
Message handlers for admins of the bot
"""

from bot import bot
from constants import ADMIN_SET, BOT_ADMIN_ID
from verification import private_access
from telebot.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaAudio
from .datastructures import AdminState, TeamState
import handlers
from . import admins_dict, teams_dict, players_dict, team_id_from_admin
from .messages import *
import db.tasks
import db.teams
import db.answers
import db.media
import db.places
import db.media
import re
from .senders import send_place
from .leaderboard import get_leaderboard
from .markups import LEADERBOARD_MARKUP

__all__ = [
    'new_task',
    'end_task',
    'show',
    'add_video',
    'add_audio',
    'add_photo',
    'delete_task',
    'set_get_route',
]

@bot.message_handler(commands=['newtask'])
@private_access
async def new_task(message: Message) -> None:
    """
    Command which turn on the task adding mode of the bot
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    admins_dict[telegram_id].state = AdminState.TASK_ADDING
    await bot.send_message(telegram_id, NEW_TASK_MESSAGE)


@bot.message_handler(commands=['newplace'])
@private_access
async def new_place(message: Message) -> None:
    """
    Command which turn on the place adding mode of the bot
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    admins_dict[telegram_id].state = AdminState.PLACE_ADDING
    await bot.send_message(telegram_id, NEW_PLACE_MESSAGE)


@bot.message_handler(commands=['endtask'])
@private_access
async def end_task(message: Message) -> None:
    """
    Command which turn off the task adding mode of the bot
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    admins_dict[telegram_id].state = AdminState.DEFAULT
    admins_dict[telegram_id].task_id = ''
    await bot.send_message(telegram_id, END_TASK_MESSAGE)


@bot.message_handler(commands=['show'])
@private_access
async def show(message: Message) -> None:
    """
    Command to show the task or the place with specific id
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    object_id = message.text.split()[1]
    task = await db.tasks.get_info(task_id=object_id)
    place = await db.places.get_info(place_id=object_id)
    if task is not None:
        text = f'ID: {task.task_id}\nAnswer: {task.answer}\nPoints: {task.points}'
        await bot.send_message(telegram_id, text=text)
        await bot.send_message(telegram_id, text=task.text)
        if task.photo_ids:
            await bot.send_media_group(telegram_id, [InputMediaPhoto(photo_id) for photo_id in task.photo_ids])
        if task.video_ids:
            await bot.send_media_group(telegram_id, [InputMediaVideo(video_id) for video_id in task.video_ids])
        if task.audio_ids:
            await bot.send_media_group(telegram_id, [InputMediaAudio(audio_id) for audio_id in task.audio_ids])
    elif place is not None:
        text = f'ID: {place.place_id}\nPassword: {place.password}'
        await bot.send_message(telegram_id, text=text)
        await bot.send_photo(telegram_id, photo=place.photo_id, caption=place.text)
    else:
        await bot.send_message(telegram_id, text='Nothing with such id')


@bot.message_handler(commands=['delete'])
@private_access
async def delete_task(message: Message) -> None:
    """
    Command which delete the task with specific id
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    object_id = message.text.split()[1]
    if await db.tasks.get_info(object_id) is not None:
        await db.tasks.delete(object_id)
        await db.media.delete_media(object_id)
        await bot.send_message(telegram_id, f'{DELETE_TASK_MESSAGE}: {object_id}')
    elif await db.places.get_info(object_id) is not None:
        await db.places.delete(object_id)
        await db.media.delete_media(object_id)
        await bot.send_message(telegram_id, f'{DELETE_PLACE_MESSAGE}: {object_id}')
    else:
        await bot.send_message(telegram_id, f'No such object: {object_id}')


@bot.message_handler(commands=['route'])
@private_access
async def set_get_route(message: Message) -> None:
    """
    Command which add the sequence of tasks for specific team
    :param message: message from the admin of the bot
    :return:
    """
    telegram_id = message.chat.id
    command_args = message.text.split()[1:]
    team_id = int(command_args[0])
    task_list = command_args[1:]
    if task_list:
        # setting the route
        team = teams_dict[team_id]
        team.route = task_list
        route = ' '.join(task_list)
        await db.teams.set_route(route=route, team_id=team_id)
        await bot.send_message(telegram_id, f'{SET_ROUTE_MESSAGE} {team_id}')
    else:
        # showing the route
        route = await db.teams.get_route(team_id)
        text = ''
        for i, place_id in enumerate(route, start=1):
            text += f'{i}) {place_id}\n'
        await bot.send_message(telegram_id, text=text)


@bot.message_handler(commands=['score'])
@private_access
async def set_score(message: Message) -> None:
    """
    Set score for task with specific id
    :param message: message from the admin of the bot
    :return:
    """
    telegram_id = message.chat.id
    command_args = message.text.split()[1:]
    task_id = command_args[0].upper()
    team_id = team_id_from_admin[telegram_id]
    score = int(command_args[1])
    task = await db.tasks.get_info(task_id)
    team = teams_dict[team_id]
    team.scores.append(score)
    await db.answers.add_new(text='', task_id=task_id, team_id=team_id, points=score)
    player_message = f'Стали известны баллы за задание {task_id}. Вы получили {score} из {task.points} баллов'
    for player_id in team.members:
        await bot.send_message(player_id, text=player_message)
    await bot.send_message(telegram_id, f'{SET_SCORE_MESSAGE} {task_id}')
    await bot.send_message(chat_id=BOT_ADMIN_ID, text=f'{telegram_id} gave {score} points for task {task_id} to the {team.name}')


@bot.message_handler(commands=['go'])
@private_access
async def start_quest(message: Message) -> None:
    """
    Start the Quest
    :param message: message from the admin of the bot
    :return:
    """
    telegram_id = message.chat.id
    if handlers.quest_started:
        await bot.send_message(telegram_id, text=QUEST_ALREADY_STARTED_MESSAGE)
        return
    leaderboard = get_leaderboard()
    for admin_id in ADMIN_SET:
        await bot.send_message(admin_id, text=leaderboard, parse_mode='HTML',
                               reply_markup=LEADERBOARD_MARKUP)
    for player_id in players_dict:
        await bot.send_message(player_id, text=leaderboard, parse_mode='HTML',
                               reply_markup=LEADERBOARD_MARKUP)
    for team_id in teams_dict:
        await send_place(team_id)
    handlers.quest_started = True
    await bot.send_message(chat_id=BOT_ADMIN_ID, text='Quest is started')


@bot.message_handler(commands=['waste'])
@private_access
async def unblock_tasks_sending(message: Message) -> None:
    """
    Unblock the task sending to the players
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    if not handlers.round_blocked:
        await bot.send_message(telegram_id, text=UNBLOCKED_ALREADY_MESSAGE)
        return
    for team_id, team in teams_dict.items():
        team.current_round += 1
        await db.teams.set_current_round(team_id=team_id, current_round=team.current_round)
        await send_place(team_id)
    handlers.round_blocked = False


@bot.message_handler(commands=['teamname'])
@private_access
async def change_team_name(message: Message) -> None:
    """
    Change/show name of specific team or of all teams
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    command_args = message.text.split()[1:]
    team_id = int(command_args[0])
    name_words = command_args[1:]
    name = ' '.join(name_words)
    team = teams_dict[team_id]
    team.name = name
    await db.teams.set_name(name=name, team_id=team_id)
    await bot.send_message(telegram_id, text=f'Name of the Team {team_id} has changed to {name}')


@bot.message_handler(commands=['results'])
@private_access
async def show_leaderboard(message: Message) -> None:
    """
    Show leaderboard table with the button to update it
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    leaderboard = get_leaderboard()
    await bot.send_message(telegram_id, text=leaderboard, parse_mode='HTML', reply_markup=LEADERBOARD_MARKUP)


@bot.message_handler(commands=['finish'])
@private_access
async def finish_quest(message: Message) -> None:
    """
    Finish the quest and send the leaderboard to all players of the Quest
    :param message:
    :return:
    """
    for team in teams_dict.values():
        team.state = TeamState.DEFAULT
    leaderboard = get_leaderboard()
    for player_id in players_dict:
        await bot.send_message(player_id, text=leaderboard, parse_mode='HTML', reply_markup=LEADERBOARD_MARKUP)
    await bot.send_message(chat_id=BOT_ADMIN_ID, text='Quest is finished')


@bot.message_handler(content_types=['photo'])
@private_access
async def add_photo(message: Message) -> None:
    """
    Handler for adding the photo to the existing task
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    state = admins_dict[telegram_id].state
    if state == AdminState.TASK_ADDING:
        task_id = admins_dict[telegram_id].task_id
        photo_id = message.photo[0].file_id
        await db.media.add_photo(task_id=task_id, photo_id=photo_id)
        await bot.send_message(telegram_id, PHOTO_ADDED_MESSAGE)
    elif state == AdminState.PLACE_ADDING:
        photo_id = message.photo[0].file_id
        pattern = r'[Ii][Dd]:([\s\S]+)[Tt]ext:([\s\S]+)[Pp]assword:([\s\S]+)'
        description_list = [s.strip() for s in re.findall(pattern, message.caption)[0]]
        if len(description_list) != 3:
            bot.send_message(telegram_id, WRONG_PLACE_FORMAT_ERROR_MESSAGE)
            return
        place_id, text, password = description_list
        await db.places.add_new(place_id=place_id, text=text, password=password, photo_id=photo_id)
        admins_dict[telegram_id].state = AdminState.DEFAULT
        await bot.send_message(telegram_id, PLACE_ADDED_MESSAGE)


@bot.message_handler(content_types=['video'])
@private_access
async def add_video(message: Message) -> None:
    """
    Handler for adding the video to the existing task
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    task_id = admins_dict[telegram_id].task_id
    video_id = message.video.file_id
    await db.media.add_video(task_id=task_id, video_id=video_id)
    await bot.send_message(telegram_id, VIDEO_ADDED_MESSAGE)


@bot.message_handler(content_types=['audio'])
@private_access
async def add_audio(message: Message) -> None:
    """
    Handler for adding the audio to the existing task
    :param message: message from the admin
    :return:
    """
    telegram_id = message.chat.id
    task_id = admins_dict[telegram_id].task_id
    audio_id = message.audio.file_id
    await db.media.add_audio(task_id=task_id, audio_id=audio_id)
    await bot.send_message(telegram_id, AUDIO_ADDED_MESSAGE)

